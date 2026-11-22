#countourgenerator.py 25101198 체 아담 하리스 빈 체 모하마드 슈크리

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from parser import DigitalElevationModelParser

#class tht generates 2D topographic contour/isoline plots from a 2D elevation grid
class ContourGenerator:

    def __init__(self, elevationGrid: np.ndarray) -> None:
        if elevationGrid.ndim != 2:
            raise ValueError("Elevation grid must be a 2D NumPy array!!!")
        self.elevationGrid = elevationGrid

    #method to compute contour levels either by fixed count ORRR by elevation interval
    def _build_levels(
        self,
        levels: int | np.ndarray | list[float] | None = 10,
        interval: float | None = None,
    ) -> int | np.ndarray:
        
        if interval is not None:
            if interval <= 0:
                raise ValueError("Contour interval must be a positive number. Try again!")
            minElevationValue = float(np.min(self.elevationGrid))
            maxElevationValue = float(np.max(self.elevationGrid))
            lowerElevationBound = np.floor(minElevationValue / interval) * interval
            upperElevationBound = np.ceil(maxElevationValue / interval) * interval + interval * 0.5
            return np.arange(lowerElevationBound, upperElevationBound, interval)
        return levels if levels is not None else 10

    #method to plot 2D contour lines and filled elevation bands across the grid
    def plot_isolines(
        self,
        levels: int | np.ndarray | list[float] | None = 10,
        interval: float | None = None,
        cmap: str = "terrain",
        filled: bool = True,
        title: str = "2D Topographic Isolines",
        output_path: str | Path | None = None,
        show: bool = True,
    ) -> plt.Figure:
        
        rowsNum, columnsNum = self.elevationGrid.shape
        columnCoordinate = np.arange(columnsNum)
        rowCoordinate = np.arange(rowsNum)
        xGrid, yGrid = np.meshgrid(columnCoordinate, rowCoordinate)
        computedLevels = self._build_levels(levels=levels, interval=interval)

        contourFigure, contourAxes = plt.subplots(figsize=(8, 6))

        if filled:
            filled_contours = contourAxes.contourf(
                xGrid, yGrid, self.elevationGrid, levels=computedLevels, cmap=cmap, alpha=0.75
            )
            contourFigure.colorbar(filled_contours, ax=contourAxes, label="Elevation")

        contourLines = contourAxes.contour(
            xGrid,
            yGrid,
            self.elevationGrid,
            levels=computedLevels,
            colors="black" if filled else None,
            cmap=None if filled else cmap,
            linewidths=1.0,
        )
        contourAxes.clabel(contourLines, inline=True, fontsize=8, fmt="%.1f")

        contourAxes.set_title(title)
        contourAxes.set_xlabel("X Grid Index")
        contourAxes.set_ylabel("Y Grid Index")
        contourAxes.set_aspect("equal", adjustable="box")
        contourFigure.tight_layout()

        if output_path is not None:
            outputFile = Path(output_path)
            outputFile.parent.mkdir(parents=True, exist_ok=True)
            contourFigure.savefig(outputFile, dpi=150)

        if show:
            plt.show()

        return contourFigure


if __name__ == "__main__":
    sampleFile = Path("data/sample_dem.csv")
    if sampleFile.exists():
        demParser = DigitalElevationModelParser(sampleFile)
        grid = demParser.load_elevation_grid()
    else:
        #fallback sample grid if data/sample_dem.csv isn't present yet
        yIndex, xIndex = np.mgrid[0:20, 0:20]
        grid = (
            100.0
            + 80.0 * np.exp(-((xIndex - 10) ** 2 + (yIndex - 10) ** 2) / 35.0)
            + 15.0 * np.sin(xIndex / 3.0) * np.cos(yIndex / 3.0)
        )

    generator = ContourGenerator(grid)
    generator.plot_isolines(levels=8) #or use interval value