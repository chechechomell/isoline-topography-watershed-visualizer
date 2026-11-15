import numpy as np
import os

class DigitalElevationModelParser:

    #initialise the DEM parser with -> path of an elevation grid file
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.elevation_grid = None

    #load the elevation text/csv file into 2d numpy array
    def load_elevation_grid(self, file_delimiter: str = ',') -> np.ndarray:
        try:
            self.elevation_grid = np.loadtxt(self.file_path, delimiter=file_delimiter)
            
            print(f"[SUCCESS] Loaded DEM grid from {self.file_path}")
            print(f"Grid Dimensions (Rows, Columns): {self.elevation_grid.shape}")
            return self.elevation_grid
            
        except Exception as error_message:
            print(f"[ERROR] Failed to load DEM data: {error_message}")
            return None

    #calculate n return topographic metrics for the loaded grid
    def calculate_terrain_statistics(self) -> dict:
        if self.elevation_grid is None:
            raise ValueError("Elevation grid has not been loaded yet. Call load_elevation_grid() first.")
            
        terrain_statistics = {
            "min_elevation": np.min(self.elevation_grid),
            "max_elevation": np.max(self.elevation_grid),
            "mean_elevation": np.mean(self.elevation_grid),
            "peak_count": np.int64(np.sum(self.elevation_grid == np.max(self.elevation_grid)))
        }
        return terrain_statistics

#execution testtt
if __name__ == "__main__":
    #ensure the data directory exists and write sample elevation data
    os.makedirs("data", exist_ok=True)
    sample_elevation_data = np.array([
        [100, 105, 120, 110],
        [95,  150, 180, 115],
        [90,  130, 140, 100],
        [85,   88,  92,  95]
    ])
    np.savetxt("data/sample_dem.csv", sample_elevation_data, delimiter=",")
    
    #instantiate and test the parser
    dem_parser = DigitalElevationModelParser("data/sample_dem.csv")
    parsed_elevation_grid = dem_parser.load_elevation_grid()
    
    print("Elevation Grid Matrix :\n", parsed_elevation_grid)
    print("Terrain Statistics Summary :", dem_parser.calculate_terrain_statistics())