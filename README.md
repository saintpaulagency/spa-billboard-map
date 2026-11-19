# Saint Paul Agency · Digital Billboard Map

An interactive map of digital billboard locations for Saint Paul Agency presentations.

**Live map:** https://saintpaulagency.github.io/spa-billboard-map/

- Every board is a blue pin. Boards on the same pole share one pin with a count.
- Click a pin for the operator, location, board ID and a one-click **Google Street View** link.
- **Show:** Twin Cities, St. Cloud or all boards. Add `#stcloud` or `#all` to the link to open on that view.
- **Search** a city, road or board ID; press Enter to zoom to the matches.
- **Operators:** click one to hide or show its boards. **One color / By company** switches the pins between SPA blue and one color per company (with a key).
- **Present full screen:** hides the panel behind a small Saint Paul Agency badge with the view buttons; Exit or Esc returns.
- Saint Paul Agency branding only. Works on phones (the panel folds away).

## Updating the boards

The map reads `data/boards.js`. To load a new inventory (same layout as Basis's "Digital Billboards" export: Billboard Company, ID, Direction 1 = latitude, Direction 2 = longitude, City/State, Zip):

```bash
pip install openpyxl
python3 tools/build_boards.py "Basis Digital Billboards - MSP Metro (all venues).xlsx" "Digital billboard inventory · Twin Cities & St. Cloud"
```

It rewrites `data/boards.js` and `data/boards.csv`. The Twin Cities and St. Cloud view areas are set at the top of the script.

Current data: 161 boards at 135 locations from 6 operators (Basis export, Nov 19, 2026).

## Credits

Map tiles: [OpenFreeMap](https://openfreemap.org) · © [OpenMapTiles](https://www.openmaptiles.org) · data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors. Map library: [MapLibre GL JS](https://maplibre.org).

Prepared by [Saint Paul Agency](https://saintpaulagency.com).
