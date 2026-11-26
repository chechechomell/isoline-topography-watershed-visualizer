# A Python-based Isoline Topography and Watershed Visualizer

An open-source Python web application designed for processing Digital Elevation Models (DEM) data, generating topographic isolines (or contour lines), and trace regional watersheds (or hydrological drainage paths).

## Project Overview
Topographic mapping and hydrological analysis are fundamental pillars of geographic information systems (GIS). Understanding how land is shaped and how water flows across hills and valleys is usually done using expensive, complicated professional software (e.g. Proprietary GIS Software). This project is a lightweight, interactive web tool that lets users load elevation grids data, measure the landscape, and view land shapes clearly on their screen without needing any heavy mapping programs.

## Tech Stack & Environment
![Tech Stack and Environment](assets/tech_stack.png)

## Project Classes & Methods
![Project Classes and Methods](assets/classes_and_methods.png)

## System Architecture & Code Structure

```text
isoline-topography-watershed-visualizer/
├── data/
│   └── sample_dem.csv          # Sample 2D elevation grid
├── parser.py                   # DEM ingestion and basic terrain statistics
├── contourgenerator.py         # Elevation contour lines and filled band plots
├── watershedanalyzer.py        # D8 flow direction, flow accumulation, and overlay plots
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation and roadmap
```

### 1. Data Ingestion Module (parser.py)
The system uses a custom DigitalElevationModelParser class to ingest raw elevation grids safely and efficiently :

NumPy Integration : Built using np.loadtxt to read delimited elevation text and CSV grids directly into 2D floating-point arrays. This will avoids compiled binary DLL conflicts (such as those associated with Pandas in restricted environments) while maintaining maximum computational performance.

Topographic Statistics Extraction : Automatically computes core terrain parameters including absolute minimum elevation (lowest single point in the terrain dataset), maximum elevation peak bounds (highest altitude point in the entire dataset), global mean elevation (overall average height across the entire map), and peak cell frequency distribution (how many individual grid squares share that absolute highest elevation).

### 2. Contour Generation Module (contourgenerator.py)
The system uses a ContourGenerator class to render 2D topographic visualizations from any 2D elevation grid :

Elevation Level Calculation : Supports plotting by a fixed number of levels or by a custom elevation interval (interval) computed from the dataset's elevation bounds.

Isoline & Filled Contour Rendering : Generates labeled contour lines (contourAxes.contour with contourAxes.clabel) alongside optional filled elevation bands (contourAxes.contourf), colorbars, and colormaps (terrain by default) across both square and non-square grids, with support for displaying or saving figures.

### 3. Watershed Analysis Module (watershedanalyzer.py)
The system uses a WatershedAnalyzer class to trace downhill water movement and identify drainage pathways from any 2D elevation grid :

D8 Flow Direction Calculation : Evaluates all eight surrounding neighbors (North, North-East, East, South-East, South, South-West, West, and North-West) for every grid cell and computes distance-weighted slope drop ((centerElevation - neighborElevation) / stepDistance, accounting for diagonal $\sqrt{2}$ spacing). Assigns direction codes (1–8) toward the steepest downhill neighbor, or 0 for local sinks and flat cells with no lower outlet.

Flow Accumulation & Drainage Tracing : Initializes every cell with a base runoff contribution of 1 and processes cells in descending elevation order (highest to lowest) so upstream flow is resolved before downstream accumulation. Propagates contributing cell counts into each cell's D8 target neighbor to reveal converging channels, stream networks, and main basin outlets across both square and non-square grids.

Logarithmic Flow & Contour Overlay Visualization : Renders flow accumulation grids using LogNorm color scaling (pcolormesh) so wide ranges of contributing cell counts remain visually clear without washing out smaller channels. Also supports elevation contour overlays (contour and clabel), per-cell accumulation labels, axis tick alignment, and figure display or export to disk.

## Getting Started 
Set up the environment and run modules with uv or standard Python :

```text
uv venv
uv pip install -r requirements.txt
uv run python watershedanalyzer.py
```

## Project Development Roadmap
**[DONE on 11.15!] Phase 1 [parser.py]: Core Data Ingestion & Architecture**
- Build DigitalElevationModelParser class with pure NumPy grid loading and statistical summaries.
- Establish version control workflow and project repository structure.

**[DONE on 11.22!] Phase 2 [contourgenerator.py]: 2D Isoline & Contour Generation**
Implement Matplotlib contour mapping algorithms to render topographic height lines.

**[DONE on 11.27!] Phase 3 [watershedanalyzer.py]: Watershed Tracing Logic**
Compute flow direction matrices and accumulation grids to trace drainage basins.

**[] Phase 4: Streamlit Web Dashboard UI**
Build an interactive web frontend allowing users to upload custom DEM files and adjust contour intervals in real time.

## License
This project is open-source and available under the terms of the MIT License.