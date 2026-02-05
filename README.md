Massachusetts Oyster Project – Interactive Mapping & Analytics Dashboard

This project provides an interactive, browser-based dashboard for visualizing data from the Massachusetts Oyster Project shell recycling program across participating restaurants and community events. This aims to support public reporting, grant applications, community outreach, and stakeholder engagement by making it easier to explore trends in participation and shell diversion from landfill over time.
The dashboard is generated programmatically in Python and rendered in the browser using Plotly.js. It includes an animated geospatial map, synchronized bar charts, dynamic legends, and multiple data exploration modes.

Overview of the Shell Recycling Program Dashboard:

1. Animated geospatial map of participating restaurants

The left panel shows a year-by-year animation of all restaurants with geocoded latitude/longitude coordinates. 
Features include:
-A Cape-Cod-focused map window (fixed bounding box).
-Smooth animated transitions across years.
-Zoom and pan controls that persist while the animation runs.
-Marker colors that uniquely identify each restaurant or event contributor.
-Automatic jittering of overlapping restaurant locations to keep individual points visible and clickable.

2. Data view modes, regional slicing, and visualization logic
   
The right-hand panel displays a dynamically updating bar chart based on the selected view mode and regional filters. All views are driven directly from the underlying dataset and remain synchronized with the map where applicable.

Across Years
The Across Years view aggregates shell recycling contributions over the full time span of the dataset. <br>
•	Each bar represents the total shell-only weight for a given year.<br>
•	Contributions from individual restaurants are rendered as stacked segments. <br>
•	This view provides a high-level summary of program growth and annual participation trends. <br>
When a regional filter is applied, totals are recalculated in real time to reflect only the selected geographic region(s), allowing direct comparison of regional participation patterns over time.
________________________________________
By Region
The dashboard supports geographic slicing of the data using predefined regions that correspond to meaningful geographic and programmatic boundaries.
•	Region selection filters both the map and the bar chart simultaneously.<br>
•	Only restaurants and events belonging to the selected region(s) are included in summaries and totals.<br>
•	Regions can be viewed individually or in combination, enabling side-by-side exploration of local versus program-wide trends.<br>
________________________________________
Region definition and assignment
Regions are assigned using latitude-based geographic boundaries chosen to reflect natural and administrative divisions along the Massachusetts coastline.
Each restaurant or event with valid geographic coordinates is assigned to a region based on its latitude and longitude:
•	Mid-Cape <br>
•	Outer Cape <br>

Latitude thresholds are applied consistently across all years, ensuring that regional classification remains stable even as new restaurants are added over time.
This approach was selected because it:
•	Avoids reliance on inconsistent address formatting or municipal names. <br>
•	Produces deterministic, reproducible regional assignments. <br>
•	Aligns well with how shell recycling programs are administered and discussed operationally. <br>

Event-based entries (which lack coordinates) are excluded from regional map views but remain visible in aggregate totals and event-specific summaries.
________________________________________
Interaction between regions, years, and events
Regional filters apply uniformly across all view modes:
•	Across Years: totals are recomputed per year using only restaurants in the selected region(s). <br>
•	By Restaurant: the restaurant list is restricted to the active region(s). <br>
•	By Event: event summaries are shown independently of region, since events are catalogued non-spatially. <br>
This design allows users to move fluidly between temporal, geographic, and organizational perspectives without changing context or losing interpretability.

Sliding-window clustering
For each selected year (and after any regional filters are applied), restaurant coordinates are processed sequentially:
1.	Latitude/longitude points are scanned in order.
2.	For each point, the script checks whether it lies within a small physical distance threshold (approximately 60 meters) of an existing cluster.
o	Distances are computed using approximate meters-per-degree conversions for latitude and longitude.
3.	If the point falls within an existing cluster window, it is assigned to that cluster.
4.	If no existing cluster falls within the threshold, a new cluster window is created.
   
This sliding-window approach groups of restaurants that are effectively co-located while avoiding aggressive spatial aggregation that would obscure true geographic distribution.

Jittering within clusters
Once clusters are identified, the individual points within each cluster are slightly displaced:
•	Points are positioned around a small radius from the cluster center. <br>
•	Each point is assigned to a unique angle, evenly spaced around the circle. <br>
•	A fixed random seed is used to ensure reproducible placement across interactions. <br>

The result is a stable, deterministic layout where:
•	Markers remain close to their true locations. <br>
•	Overlapping points become individually visible and clickable. <br>
•	Marker positions do not “jump” unpredictably when filters or years change. <br>

Interaction with years and regions
The clustering and jittering logic is applied after the year and region filters are evaluated:
•	Across Years: clustering is recomputed independently for each year, preventing artificial carryover of jitter between time points. <br>
•	By Region: clusters are computed only from restaurants within the active region(s), ensuring spatial separation remains locally meaningful. <br>
•	Events: event-based entries (which lack coordinates) bypass clustering entirely and do not appear on the map. <br>

Technical Architecture
Python Layer (Data Preparation + HTML Generation)

The Python script:
•	Loads and normalizes the input CSV. <br>
•	Identifies restaurants and events. <br>
•	Performs geospatial filtering using Cape Cod bounding boxes. <br>
•	Applies the sliding-window jitter algorithm to clustered coordinates. <br>

& Computes aggregates for:

I.	Shell weight by year. <br>
**Disclaimer: this is the shell only weight, subtracting the weight of the buckets from the totals <br>
II.	Shell weight by restaurant over time. <br>
III.	Shell weight by event by year. <br>

& Assembles a self-contained docs/index.html file that includes:
•	The Plotly map. <br>
•	The right-hand bar charts. <br>

All JSON-serialized data structures are used by the JavaScript layer.

This design makes publishing updates as simple as running the Python script and pushing to GitHub.

JavaScript Layer (Dynamic Browser Interactions)
The JS embedded in index.html controls:

•	Map animation and year slide behavior. <br>
•	Mode switching among Year, Restaurant, and Event views. <br>
•	Responsive bar chart rendering. <br>
•	Legend generation for all modes. <br>
•	Synchronization between the animation map and the Year bar chart. <br>

