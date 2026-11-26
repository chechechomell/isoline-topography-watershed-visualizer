#watershedanalyzer.py 25101198 체 아담 하리스 빈 체 모하마드 슈크리

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from parser import DigitalElevationModelParser

#D8 neighbor offset : (rowDelta, columnDelta, directionCode)
D8_NEIGHBORS = (
    (-1, 0, 1),   #north
    (-1, 1, 2),   #northeast
    (0, 1, 3),    #east
    (1, 1, 4),    #southeast
    (1, 0, 5),    #south
    (1, -1, 6),   #southwest
    (0, -1, 7),   #west
    (-1, -1, 8),  #northwest
)

#map D8 direction code -> (rowDelta, columnDelta)
D8_CODE_TO_OFFSET = {
    1: (-1, 0),   #north
    2: (-1, 1),   #northeast
    3: (0, 1),    #east
    4: (1, 1),    #southeast
    5: (1, 0),    #south
    6: (1, -1),   #southwest
    7: (0, -1),   #west
    8: (-1, -1),  #northwest
}

#calculate D8 flow direction and flow accumulation from a 2D elevation grid
class WatershedAnalyzer:

    def __init__(self, elevationGrid: np.ndarray) -> None:
        if elevationGrid.ndim != 2:
            raise ValueError("Elevation grid must be a 2D NumPy array!!! try again!")
        self.elevationGrid = np.asarray(elevationGrid, dtype=float)
        self.rowsNum, self.columnsNum = self.elevationGrid.shape

    #return a 2D grid of D8 direction codes (1 to8) ORRRR 0 if no lower neighbor exist
    def compute_flow_direction(self) -> np.ndarray:
        flowDirection = np.zeros((self.rowsNum, self.columnsNum), dtype=np.int8)
        steepestDrop = np.zeros((self.rowsNum, self.columnsNum), dtype=float)

        for rowIndex in range(self.rowsNum):
            for columnIndex in range(self.columnsNum):
                centerElevation = self.elevationGrid[rowIndex, columnIndex]

                for rowDelta, columnDelta, directionCode in D8_NEIGHBORS:
                    neighborRow = rowIndex + rowDelta
                    neighborColumn = columnIndex + columnDelta

                    if 0 <= neighborRow < self.rowsNum and 0 <= neighborColumn < self.columnsNum:
                        neighborElevation = self.elevationGrid[neighborRow, neighborColumn]
                        stepDistance = np.hypot(rowDelta, columnDelta)
                        slopeDrop = (centerElevation - neighborElevation) / stepDistance

                        if slopeDrop > steepestDrop[rowIndex, columnIndex]:
                            steepestDrop[rowIndex, columnIndex] = slopeDrop
                            flowDirection[rowIndex, columnIndex] = directionCode

        return flowDirection

    #return a 2D grid counting upstream contributing cells (plus self) per cell
    def compute_flow_accumulation(self, flowDirection: np.ndarray) -> np.ndarray:
        if flowDirection.shape != self.elevationGrid.shape:
            raise ValueError("Flow direction grid must match elevation grid shape!!")

        flowAccumulation = np.ones((self.rowsNum, self.columnsNum), dtype=np.int32)

        #process cells from highest elevation to lowest so upstream flow arrives first
        sortedFlatIndices = np.argsort(self.elevationGrid, axis=None)[::-1]

        for flatIndex in sortedFlatIndices:
            rowIndex, columnIndex = np.unravel_index(flatIndex, (self.rowsNum, self.columnsNum))
            dirCode = int(flowDirection[rowIndex, columnIndex])

            if dirCode in D8_CODE_TO_OFFSET:
                rowDelta, colDelta = D8_CODE_TO_OFFSET[dirCode]
                nextRow = rowIndex + rowDelta
                nextCol = columnIndex + colDelta

                if 0 <= nextRow < self.rowsNum and 0 <= nextCol < self.columnsNum:
                    flowAccumulation[nextRow, nextCol] += flowAccumulation[rowIndex, columnIndex]

        return flowAccumulation

    #plot flow accumulation with elevation contour and cell count overlays
    def plot_flow_accumulation(
        self,
        flowAccumulation: np.ndarray | None = None,
        flowDirection: np.ndarray | None = None,
        cmap: str = "Blues",
        title: str = "D8 Flow Accumulation & Elevation Contours",
        showContours: bool = True, #contourswitchh
        showValues: bool = True,
        outputPath: str | Path | None = None,
        show: bool = True,
    ) -> plt.Figure:
        
        if flowAccumulation is None:
            flowAccumulation = self.compute_flow_accumulation(flowDirection=flowDirection)
        elif flowAccumulation.shape != self.elevationGrid.shape:
            raise ValueError("Flow accumulation grid must match elevation grid shape!!")

        xCoordinates = np.arange(self.columnsNum)
        yCoordinates = np.arange(self.rowsNum)
        xGrid, yGrid = np.meshgrid(xCoordinates, yCoordinates)

        accumulationFigure, accumulationAxes = plt.subplots(figsize=(8, 6))
        maxAccumulation = max(int(np.max(flowAccumulation)), 2)

        accumulationMesh = accumulationAxes.pcolormesh(
            xGrid,
            yGrid,
            flowAccumulation,
            norm=LogNorm(vmin=1, vmax=maxAccumulation),
            cmap=cmap,
            shading="nearest",
        )

        accumulationFigure.colorbar(
            accumulationMesh, ax=accumulationAxes, label="Contributing Cells (Log Scale)"
        )

        if showContours:
            contourLines = accumulationAxes.contour(
                xGrid,
                yGrid,
                self.elevationGrid,
                levels=6,
                colors="darkorange",
                linewidths=1.2,
                alpha=0.85,
            )
            accumulationAxes.clabel(contourLines, inline=True, fontsize=8, fmt="%.0f")

        if showValues:
            midpointLog = np.sqrt(maxAccumulation)
            for rowIndex in range(self.rowsNum):
                for columnIndex in range(self.columnsNum):
                    cellValue = int(flowAccumulation[rowIndex, columnIndex])
                    textColor = "white" if cellValue >= midpointLog else "black"
                    accumulationAxes.text(
                        columnIndex,
                        rowIndex,
                        str(cellValue),
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color=textColor,
                    )

        accumulationAxes.set_xticks(xCoordinates)
        accumulationAxes.set_yticks(yCoordinates)
        accumulationAxes.set_xlim(-0.5, self.columnsNum - 0.5)
        accumulationAxes.set_ylim(-0.5, self.rowsNum - 0.5)
        accumulationAxes.set_title(title)
        accumulationAxes.set_xlabel("X Grid Index")
        accumulationAxes.set_ylabel("Y Grid Index")
        accumulationAxes.set_aspect("equal", adjustable="box")
        accumulationFigure.tight_layout()

        if outputPath is not None:
            outputFile = Path(outputPath)
            outputFile.parent.mkdir(parents=True, exist_ok=True)
            accumulationFigure.savefig(outputFile, dpi=150)

        if show:
            plt.show()

        return accumulationFigure


if __name__ == "__main__":
    sampleFile = Path("data/sample_dem.csv")
    if sampleFile.exists():
        demParser = DigitalElevationModelParser(sampleFile)
        grid = demParser.load_elevation_grid()
    else:
        grid = np.array(
            [
                [100, 105, 120, 110],
                [95, 150, 180, 115],
                [90, 130, 140, 100],
                [85, 88, 92, 95],
            ],
            dtype=float,
        )

    analyzer = WatershedAnalyzer(grid)
    flowDirectionGrid = analyzer.compute_flow_direction()
    flowAccumulationGrid = analyzer.compute_flow_accumulation(flowDirectionGrid)
    print("Elevation Grid :\n", grid)
    print("Flow Direction Grid (D8 codes 1-8, 0=sink/flat) :\n", flowDirectionGrid)
    print("Flow Accumulation Grid :\n", flowAccumulationGrid)

    analyzer.plot_flow_accumulation(flowAccumulationGrid)