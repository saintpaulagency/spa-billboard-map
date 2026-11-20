"""Turn a billboard inventory spreadsheet (like Basis's "Digital Billboards" export) into the map's data.

Usage:
    python3 tools/build_boards.py "Basis Digital Billboards - MSP Metro (all venues).xlsx" ["Map title"]

Reads the first sheet (or the one named "Billboards") and writes:
    data/boards.js    what the map reads (window.BOARDS = {...})
    data/boards.csv   the same boards, cleaned, for download

Columns are found by their header names (any order, any capitalization):
    unit id      first column
    operator     "Billboard Company" / "Operator" / "Vendor"
    board        "ID" / "Board" / "Description"   (a code, two or more spaces, then the location)
    latitude     "Direction 1" / "Latitude" / "Lat"
    longitude    "Direction 2" / "Longitude" / "Lon" / "Lng"
    city         "City/State" / "City"
    zip          "Zip" / "Zip Code"
Rows without numeric coordinates are skipped and listed. A board listed twice (same company and board code
within about 200 m) is kept once.
"""
import csv, json, os, re, sys
from datetime import date
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

HEAD = {
    'operator': ['billboard company', 'operator', 'vendor', 'company', 'media owner'],
    'board': ['id', 'board', 'description', 'board description', 'location'],
    'lat': ['direction 1', 'latitude', 'lat'],
    'lon': ['direction 2', 'longitude', 'lon', 'lng', 'long'],
    'city': ['city/state', 'city', 'market'],
    'zip': ['zip', 'zip code', 'postal code'],
    'format': ['outdoor|billboards', 'format', 'type', 'media type'],
}
# Map views offered as buttons. A board belongs to the first view whose box holds it; "All boards" is always added.
VIEWS = [
    {'key': 'metro', 'label': 'Twin Cities', 'box': [44.45, -94.05, 45.47, -92.55]},
    {'key': 'stcloud', 'label': 'St. Cloud', 'box': [45.40, -94.45, 45.70, -94.00]},
]


def clean(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def split_board(text):
    """'DBP-MIN17          eastbound I94, SW ramp @ Hwy 19' -> ('DBP-MIN17', 'Eastbound I94, SW ramp @ Hwy 19')"""
    raw = str(text or '').strip()
    m = re.match(r'^(\S+)\s{2,}(.+)$', raw)
    if m:
        code, where = m.group(1), m.group(2)
    elif raw and not re.search(r'\s', raw):
        code, where = raw, ''                              # a code with no location written
    else:
        code, where = '', raw
    where = clean(where)
    return code, (where[:1].upper() + where[1:]) if where else ''


def main(path, title=None):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb['Billboards'] if 'Billboards' in wb.sheetnames else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = [clean(h).lower() for h in rows[0]]
    col = {'unit': 0}
    for k, names in HEAD.items():
        for n in names:
            if n in head:
                col[k] = head.index(n)
                break
    missing = [k for k in ('operator', 'board', 'lat', 'lon') if k not in col]
    if missing:
        sys.exit('could not find columns: %s (headers: %s)' % (missing, rows[0]))
    boards, skipped = [], []
    for n, r in enumerate(rows[1:], start=2):
        get = lambda k: r[col[k]] if k in col and col[k] < len(r) else None
        lat, lon = get('lat'), get('lon')
        try:
            lat, lon = float(lat), float(lon)
        except (TypeError, ValueError):
            if any(v not in (None, '') for v in r):
                skipped.append(n)
            continue
        code, where = split_board(get('board'))
        city = clean(get('city'))
        city = re.sub(r'^St\.(?=\S)', 'St. ', city)          # "St.Cloud, MN" -> "St. Cloud, MN"
        zp = get('zip')
        boards.append({
            'id': clean(get('unit')), 'operator': clean(get('operator')), 'code': code, 'where': where,
            'city': city, 'zip': str(int(zp)) if isinstance(zp, (int, float)) else clean(zp),
            'lat': round(lat, 6), 'lon': round(lon, 6),
        })
    # The same board can be listed twice (e.g. under two zip codes, or by two sellers): same company and board code
    # within about 200 m counts as one board. The first listing is kept.
    unique, dupes = [], []
    for x in boards:
        twin = next((u for u in unique if x['code'] and u['code'] == x['code'] and u['operator'] == x['operator']
                     and abs(u['lat'] - x['lat']) < 0.002 and abs(u['lon'] - x['lon']) < 0.0025), None)
        (dupes if twin else unique).append(x)
    boards = unique
    views = []
    for v in VIEWS:
        a, b, c, d = v['box']
        n = sum(1 for x in boards if a <= x['lat'] <= c and b <= x['lon'] <= d)
        if n:
            views.append({'key': v['key'], 'label': v['label'], 'box': v['box'], 'count': n})
    out = {
        'title': title or 'Digital billboard inventory',
        'source': os.path.basename(path), 'built': date.today().isoformat(),
        'views': views, 'boards': boards, 'listed': len(boards) + len(dupes), 'repeats': len(dupes),
    }
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'data', 'boards.js'), 'w') as f:
        f.write('/* Billboard locations for the Saint Paul Agency map. Built by tools/build_boards.py from %s. */\n' % out['source'])
        f.write('window.BOARDS = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
    with open(os.path.join(ROOT, 'data', 'boards.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['unit_id', 'operator', 'board_code', 'location', 'city_state', 'zip', 'latitude', 'longitude'])
        for x in boards:
            w.writerow([x['id'], x['operator'], x['code'], x['where'], x['city'], x['zip'], x['lat'], x['lon']])
    spots = len({(x['lat'], x['lon']) for x in boards})
    print('boards %d, map spots %d, repeats left out %d %s, skipped rows %s' % (len(boards), spots, len(dupes), [d['code'] for d in dupes], skipped or 'none'))
    print('views', [(v['label'], v['count']) for v in views])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
