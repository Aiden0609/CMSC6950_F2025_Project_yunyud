from firstPlot import plotMonthly
from preprocessing import preprocessingDf


def main() -> None:
    preprocessingDf()
    outputPath = './output'
    plotMonthly(outputPath=outputPath)


if __name__ == "__main__":
    main()
