Built for Python 3.

### Required Packages
- `pyyaml`
- `openpyxl`
- `pandas`
- `requests`

`pip install pyyaml openpyxl pandas requests`

## Usage

### Data File Format

- Input xlsx file must have 2 columns on the first sheet.
  - One must be labeled `Address` and contain patient addresses
  - The other must be labeled `Groceries` and contain legitimate grocery store locations
  - Both should contain a list of addresses.
- Create a file called `API_token.txt` and put your Google maps API token on the first line.
- Create a file called `map_id.txt` and put a Google map ID on the first line.

### Running

- Pass the xlsx file path into the heatmap.py as the first argument.
  - This will begin the geolocating process and generate a marker_map.html heatmap.
  - It will also generate a yaml file that can be passed into the heatmap.py to regenerate the heatmap.
- Open the maker_map.html to view the heatmap.
  - Groceries are in blue.
  - Bus stops located near patient addresses are loaded dynamically and are in red.
    - Not all bus stops are loaded if there is another stop within 500m.
   
This may cost a dollar or so to run in API fees depending on the number of addresses.
Note that the html will contain your map ID and API key, so distribute carefully.
