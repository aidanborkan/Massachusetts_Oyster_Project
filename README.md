Massachusetts Oyster Project – Interactive Mapping & Analytics Dashboard

This project provides an interactive, browser-based dashboard for visualizing Massachusetts Oyster Project shell recycling program data across restaurants and community events. This intends to support public reporting, grant applications, community outreach, and stakeholder engagement by making it easier to explore participation and shell diversion trends over time.
The dashboard is generated programmatically in Python and rendered in the browser using Plotly.js. It includes an animated geospatial map, synchronized bar charts, dynamic legends, and multiple data exploration modes.

Overview of What the Dashboard Does
1. Animated geospatial map of participating restaurants

The left panel shows a year-by-year animation of all restaurants with geocoded latitude/longitude coordinates. Features include:

A Cape-Cod-focused map window (fixed bounding box).

Smooth animated transitions across years.

Zoom and pan controls that persist while the animation runs.

Marker colors that uniquely identify each restaurant or event contributor.

Automatic jittering of overlapping restaurant locations so individual points remain visible and clickable.

2. Three data-view modes

The right panel contains a bar chart that updates based on a selected mode:

By Year

Shows total shell weight collected from all restaurants in a given year, with each restaurant represented as a stacked color segment. This mode synchronizes with the map’s animation slider.

By Restaurant

Shows longitudinal contributions for one restaurant across all years. A dropdown menu is populated automatically with every restaurant that appears in the data.

By Event

Identifies event-based contributions automatically (rows without coordinates or full address) and summarizes their shell weight.
Behavior adapts to the data:

If only one event year exists → a simple bar chart.

If multiple years exist → a stacked horizontal bar chart using hatch patterns to represent different years (rather than colors, which remain mapped to event names).

Long event names are accommodated with expanded left-margin spacing.

How Event Detection Works

An entry is treated as an event if:

It has no latitude, no longitude, and no full street address.
This prevents event contributions from appearing on the map while allowing them to be analyzed on the right side. Events retain unique names and colors, and they are included in legends and bar charts.

How Jittering Works (Sliding-Window Cluster Method)

Many restaurants in Cape Cod share identical or nearly identical coordinates (for example, multiple restaurants inside the same marina or retail complex). Without adjustments, these markers would overlap, making them impossible to distinguish or click.

To resolve this, the dashboard uses a sliding-window algorithm:

The latitude/longitude points for a given year are scanned in order.
For each point, the script checks whether it is within a small physical distance (e.g., 60 meters) of an existing cluster.
Distance is computed using approximate meters-per-degree latitude and longitude.
If the point falls inside a cluster window → it is assigned to that cluster.
If not → a new cluster window begins.

After all points are assigned, each cluster is jittered by placing its members around a small radius, distributed at evenly spaced random angles.

This approach maintains the overall geographic accuracy while ensuring individual restaurants remain visible and interactive. The jitter is reproducible (random seed fixed) and scale-appropriate so that markers do not drift off their intended map locations.

Technical Architecture
Python Layer (Data Preparation + HTML Generation)

The Python script:

Loads and normalizes the input CSV.
Identifies restaurants and events.

& Computes aggregates for:

Shell weight by year.
Shell weight by restaurant over time.
Shell weight by event by year.

Performs geospatial filtering using Cape Cod bounding boxes.

Applies the sliding-window jitter algorithm to clustered coordinates.

Assembles a self-contained docs/index.html file that includes:

The Plotly map.

The right-hand bar charts.

All JSON-serialized data structures used by the JavaScript layer.

This design makes publishing updates as simple as running the Python script and pushing to GitHub.

JavaScript Layer (Dynamic Browser Interactions)

The JS embedded in index.html controls:

Map animation and year slider behavior.
Mode switching among Year, Restaurant, and Event views.
Responsive bar chart rendering.
Legend generation for all modes.
Synchronization between the map animation and the Year bar chart.
