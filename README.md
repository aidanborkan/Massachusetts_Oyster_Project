# Massachusetts Oyster Project – Interactive Mapping & Analytics Dashboard

This project provides an interactive, browser-based dashboard for visualizing data from the Massachusetts Oyster Project shell recycling program across participating restaurants and community events.

The dashboard supports public reporting, grant applications, community outreach, and stakeholder engagement by making it easier to explore trends in participation and shell diversion from landfill over time.

The dashboard is generated programmatically in Python and rendered in the browser using Plotly.js. It includes an animated geospatial map, synchronized bar charts, dynamic legends, and multiple data exploration modes.

---

## Overview of the Shell Recycling Program Dashboard

### 1. Animated geospatial map of participating restaurants

The left panel shows a year-by-year animation of all restaurants with geocoded latitude and longitude coordinates.

**Features include:**
- A Cape Cod–focused map window with a fixed bounding box
- Smooth animated transitions across years
- Zoom and pan controls that persist while the animation runs
- Marker colors that uniquely identify each restaurant or event contributor
- Automatic jittering of overlapping restaurant locations to keep individual points visible and clickable

---

### 2. Data view modes, regional slicing, and visualization logic

The right-hand panel displays a dynamically updating bar chart based on the selected view mode and regional filters. All views are driven directly from the underlying dataset and remain synchronized with the map where applicable.

---

#### Across Years

The **Across Years** view aggregates shell recycling contributions over the full time span of the dataset.

- Each bar represents the total shell-only weight for a given year
- Contributions from individual restaurants are rendered as stacked segments
- This view provides a high-level summary of program growth and annual participation trends

When a regional filter is applied, totals are recalculated in real time to reflect only the selected geographic region(s), allowing direct comparison of regional participation patterns over time.

---

#### By Region

The dashboard supports geographic slicing using predefined regions that correspond to meaningful geographic and programmatic boundaries.

- Region selection filters both the map and the bar chart simultaneously
- Only restaurants and events belonging to the selected region(s) are included in summaries and totals
- Regions can be viewed individually or in combination, enabling comparison of local versus program-wide trends

---

### Region definition and assignment

Regions are assigned using latitude-based geographic boundaries chosen to reflect natural and administrative divisions along the Massachusetts coastline.

Each restaurant or event with valid geographic coordinates is assigned to a region based on its latitude and longitude:

- Mid-Cape
- Outer Cape

Latitude thresholds are applied consistently across all years, ensuring that regional classification remains stable as new restaurants are added over time.

This approach was selected because it:
- Avoids reliance on inconsistent address formatting or municipal names
- Produces deterministic, reproducible regional assignments
- Aligns with how shell recycling programs are administered operationally

Event-based entries (which lack coordinates) are excluded from regional map views but remain visible in aggregate totals and event-specific summaries.

---

### Interaction between regions, years, and events

Regional filters apply uniformly across all view modes:

- **Across Years:** totals are recomputed per year using only restaurants in the selected region(s)
- **By Restaurant:** the restaurant list is restricted to the active region(s)
- **By Event:** event summaries are shown independently of region, since events are catalogued non-spatially

This design allows users to move fluidly between temporal, geographic, and organizational perspectives without losing context or interpretability.

---

### Sliding-window clustering

For each selected year (after regional filters are applied), restaurant coordinates are processed sequentially:

1. Latitude and longitude points are scanned in order
2. Each point is tested against existing clusters using a small distance threshold (~60 meters)
3. Distances are computed using approximate meters-per-degree conversions
4. Points within an existing threshold are assigned to that cluster
5. Otherwise, a new cluster is created

This sliding-window approach groups co-located restaurants while avoiding aggressive spatial aggregation that would obscure true geographic distribution.

---

### Jittering within clusters

Once clusters are identified, individual points within each cluster are slightly displaced:

- Points are positioned around a small radius from the cluster center
- Each point is assigned a unique angle, evenly spaced around the circle
- A fixed random seed ensures reproducible placement across interactions

The result is a stable, deterministic layout where:
- Markers remain close to their true locations
- Overlapping points become individually visible and clickable
- Marker positions do not jump unpredictably when filters or years change

---

### Technical Architecture

#### Python Layer (Data Preparation + HTML Generation)

The Python script:
- Loads and normalizes the input CSV
- Identifies restaurants and events
- Applies Cape Cod bounding-box filtering
- Performs sliding-window clustering and jittering
- Computes aggregates for:
  - Shell weight by year  
    **Note:** shell-only weight is calculated by subtracting bucket weight from the totals
  - Shell weight by restaurant over time
  - Shell weight by event by year

The script assembles a self-contained `docs/index.html` file containing:
- The Plotly map
- The synchronized bar charts

All data structures are JSON-serialized and consumed by the JavaScript layer.

Publishing updates requires only rerunning the Python script and pushing changes to GitHub.

---

#### JavaScript Layer (Dynamic Browser Interactions)

The embedded JavaScript controls:
- Map animation and year slider behavior
- Mode switching between Year, Restaurant, and Event views
- Responsive bar chart rendering
- Dynamic legend generation
- Synchronization between the animated map and the Year bar chart


