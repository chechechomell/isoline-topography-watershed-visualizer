# A Python-based Isoline Topography and Watershed Visualizer

An open-source Python web application designed for processing Digital Elevation Models (DEM) data, generating topographic isolines (or contour lines), and trace regional watersheds (or hydrological drainage paths).

## Project Overview
Topographic mapping and hydrological analysis are fundamental pillars of geographic information systems (GIS). Understanding how land is shaped and how water flows across hills and valleys is usually done using expensive, complicated professional software (e.g. Proprietary GIS Software). This project is a lightweight, interactive web tool that lets users load elevation grids data, measure the landscape, and view land shapes clearly on their screen without needing any heavy mapping programs.

## Tech Stack & Environment
* **Core Language:** Python 
* **Data Processing & Grid Handling:** NumPy (array parsing and aggregation)
* **Visualization Engine:** Matplotlib (for 2D contour maps and isoline generation)
* **Web User Interface:** Streamlit (for interactive web dashboard deployment)
* **Dependency & Environment Manager:** "uv" (for high performance virtual environments and fast package installation)

## System Architecture & Code Structure
The project is structured sectionally to separate data ingestion, numerical computation, spatial rendering, and user interface layers.

```text
isoline-topography-watershed-visualizer/
│
├── data/                  #for elevation grid datasets (e.g. sample_dem.csv)
├── .venv/                 #python virtual environment (managed via uv)
├── parser.py              #Core Digital Elevation Model (DEM) data parser
├── requirements.txt       #project dependency and requirements
└── README.md              #project documentations and technical report
```

### 1. Data Ingestion Module (parser.py)
The system uses a custom DigitalElevationModelParser class to ingest raw elevation grids safely and efficiently :

NumPy Integration : Built using np.loadtxt to read delimited elevation text and CSV grids directly into 2D floating-point arrays. This will avoids compiled binary DLL conflicts (such as those associated with Pandas in restricted environments) while maintaining maximum computational performance.

Topographic Statistics Extraction : Automatically computes core terrain parameters including absolute minimum elevation (lowest single point in the terrain dataset), maximum elevation peak bounds (highest altitude point in the entire dataset), global mean elevation (overall average height across the entire map), and peak cell frequency distribution (how many individual grid squares share that absolute highest elevation).

## Installation & Getting Started 
Follow these steps to set up the development environment and run the project locally using uv.

Prerequisites
Ensure you have Python installed and uv configured on your system.

1. Clone the Repository
git clone [https://github.com/chechechomell/isoline-topography-watershed-visualizer.git](https://github.com/chechechomell/isoline-topography-watershed-visualizer.git)
cd isoline-topography-watershed-visualizer

2. Set Up the Virtual Environment with uv
```text
uv venv
```

To activate the environment:
```text
in Powershell: .venv\Scripts\Activate
in macOS/Linux: source .venv/bin/activate
```

3. Install Dependencies
Install the required packages listed in requirements.txt:
```text
uv pip install -r requirements.txt
```

4. Run the DEM Parser Test
Execute the parser script to verify data loading and test the sample elevation grid:
```text
python parser.py
```

## Project Development Roadmap

[DONE on 11.15!] Phase 1: Core Data Ingestion & Architecture
- Build DigitalElevationModelParser class with pure NumPy grid loading and statistical summaries.
- Establish version control workflow and project repository structure.

[ ] Phase 2: 2D Isoline & Contour Generation
Implement Matplotlib contour mapping algorithms to render topographic height lines.

[ ] Phase 3: Watershed Tracing Logic
Compute flow direction matrices and accumulation grids to trace drainage basins.

[ ] Phase 4: Streamlit Web Dashboard UI
Build an interactive web frontend allowing users to upload custom DEM files and adjust contour intervals in real time.

## License
This project is open-source and available under the terms of the MIT License.