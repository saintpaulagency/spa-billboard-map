# Saint Paul Agency · Digital Billboard Map

An interactive map of digital billboard locations for Saint Paul Agency presentations.

**Live map:** https://saintpaulagency.github.io/spa-billboard-map/

- Every board is a blue pin. Boards on the same pole share one pin with a count. Pins get a little smaller when zoomed out, and hovering one shows its company and city.
- Click a pin for the operator, location, board ID and a one-click **Google Street View** link.
- **Show:** Twin Cities, St. Cloud or all boards. Add `#stcloud` or `#all` to the link to open on that view.
- **Search** a city, road or board ID; press Enter to zoom to the matches.
- **Billboard companies:** click one to hide or show its boards (the numbers at the top follow); Show all resets. **One color / By company** switches the pins between SPA blue and one color per company (with a key).
- **Present full screen:** hides the panel behind a small Saint Paul Agency badge with the view buttons; Exit or Esc returns.
- **Map:** Streets (default) or Light, a quieter map that makes the pins stand out.
- Saint Paul Agency branding only. The panel fits laptop screens; on phones it folds away.

**3D map (preview):** https://saintpaulagency.github.io/spa-billboard-map/3d/

- Opens on a turning globe and flies down into the Twin Cities on a tilted night map with 3D buildings and glowing highways.
- Each board is a small blue billboard on a pole, playing a loop of sample ads (Your Ad Here, Saint Paul Agency, Grand Opening and so on; nothing client-specific), with a pulsing glow on the ground under it.
- **Guided tour** flies between the busiest areas with captions; **Present** goes full screen and slowly circles the city.
- Same views, search, company filters, colors and Street View links as the classic map, plus **3D / 2D**, **Night / Day** and **SPA blue / By company** switches.
- It reads the same `data/boards.js`, so updating the boards updates both maps.

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
