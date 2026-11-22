#parser.py 25101198 체 아담 하리스 빈 체 모하마드 슈크리

import numpy as np
import os

class DigitalElevationModelParser:

    #initialise the DEM parser with -> path of an elevation grid file
    def __init__(self, file_path: str):
        self.filePath = file_path
        self.elevationGrid = None

    #load the elevation text/csv file into 2d numpy array
    def load_elevation_grid(self, fileDelimiter: str = ',') -> np.ndarray:
        try:
            self.elevationGrid = np.loadtxt(self.filePath, delimiter=fileDelimiter)
            
            print(f"Success! : Loaded DEM grid from {self.filePath}")
            print(f"Grid Dimensions (Rows, Columns): {self.elevationGrid.shape}")
            return self.elevationGrid
            
        except Exception as errorMessage:
            print(f"Error : Failed to load DEM data : {errorMessage}")
            return None

    #calculate n return topographic metrics for the loaded grid
    def calculate_terrain_statistics(self) -> dict:
        if self.elevationGrid is None:
            raise ValueError("Elevation grid has not been loaded yet. Call load_elevation_grid() first!")
            
        terrainStatistics = {
            "minElevation": np.min(self.elevationGrid),
            "maxElevation": np.max(self.elevationGrid),
            "meanElevation": np.mean(self.elevationGrid),
            "peakCount": np.int64(np.sum(self.elevationGrid == np.max(self.elevationGrid)))
        }
        return terrainStatistics

#execution testtt
if __name__ == "__main__":
    #ensure the data directory exists and write sample elevation data
    os.makedirs("data", exist_ok=True)
    sampleElevationData = np.array([
        [100, 105, 120, 110],
        [95,  150, 180, 115],
        [90,  130, 140, 100],
        [85,   88,  92,  95]
    ])
    np.savetxt("data/sample_dem.csv", sampleElevationData, delimiter=",")
    
    #instantiate and test the parser
    demParser = DigitalElevationModelParser("data/sample_dem.csv")
    parsedElevationGrid = demParser.load_elevation_grid()
    
    print("Elevation Grid Matrix :\n", parsedElevationGrid)
    print("Terrain Statistics :", demParser.calculate_terrain_statistics())