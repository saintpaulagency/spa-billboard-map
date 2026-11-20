# Saint Paul Agency · Digital Billboard Map

An interactive map of digital billboard locations for Saint Paul Agency presentations.

**Live map (3D):** https://saintpaulagency.github.io/spa-billboard-map/ (add `#stcloud` or `#all` to open on that view)
**Classic map (flat, lighter):** https://saintpaulagency.github.io/spa-billboard-map/classic/ (the old `/3d/` link forwards to the main map)

## The 3D map (main link)

- Opens on a turning globe and flies down into the Twin Cities on a tilted night map with 3D buildings and glowing highways. **Skip intro** jumps straight in.
- Each board is a small billboard on a pole (14' x 48' bulletin shape) drawn by the map itself, so it stays smooth. Sample ads (Your Ad Here, Saint Paul Agency, Grand Opening and so on; nothing client-specific) hold 8 seconds each, like a real digital board, and change in staggered waves.
- Click a board for the company, location, board ID and a one-click **Google Street View** link.
- **Your ad:** choose an ad image (1400 x 400 fits best) to show it on every board, or mixed in with the samples. It stays in that browser; nothing is uploaded.
- **Near address:** type an address or business; it circles 3, 5 or 10 miles, dims the boards outside, and lists the count by company and the closest boards. Address lookup uses OpenStreetMap's free geocoder.
- **Guided tour** flies between the busiest areas with captions; **Present** goes full screen and slowly circles the city.
- Views (Twin Cities, St. Cloud, All), search, company filters, **3D / 2D**, **Night / Day** and **SPA blue / By company** switches. If a computer can't keep up, it lowers the drawing resolution by itself.

## The classic map (/classic/)

- Every board is a blue pin; boards on the same pole share one pin with a count. Click a pin for the details and Street View.
- Same views, search, company filters, One color / By company pins, Streets / Light map, and Present full screen.
- Use it on older computers, or if the 3D map runs slowly.

Both maps read the same `data/boards.js`, so updating the boards updates both.

## Updating the boards

The map reads `data/boards.js`. To load a new inventory (same layout as Basis's "Digital Billboards" export: Billboard Company, ID, Direction 1 = latitude, Direction 2 = longitude, City/State, Zip):

```bash
pip install openpyxl
python3 tools/build_boards.py "Basis Digital Billboards - MSP Metro (all venues).xlsx" "Digital billboard inventory · Twin Cities & St. Cloud"
```

It rewrites `data/boards.js` and `data/boards.csv`. The Twin Cities and St. Cloud view areas are set at the top of the script.

Current data: 157 boards at 133 locations from 6 companies (Basis export, Nov 19, 2026). The export lists 161 rows; 4 boards appear twice (same company and board ID at the same spot) and are shown once.

## Credits

Map tiles: [OpenFreeMap](https://openfreemap.org) · © [OpenMapTiles](https://www.openmaptiles.org) · data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors. Map library: [MapLibre GL JS](https://maplibre.org).

Prepared by [Saint Paul Agency](https://saintpaulagency.com).
