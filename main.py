import pdfreader
import argparse
import glob
from pdfreader import SimplePDFViewer


def generateCsvFile(filesPaths):
    print()
    for path in filesPaths:
        fd = open(path, "rb")
        viewer = SimplePDFViewer(fd)
        for canvas in viewer:
            pageStrings = canvas.strings
            print(pageStrings)


def getFilesPaths(filesFolderPath):
    paths = glob.glob(filesFolderPath + "*.pdf")
    if paths:
        print("Processing your bills")
    else:
        print("The folder do not have any pdf file or the path is incorrect!")

    return paths


def getArgs():
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "-p", "--path", help="path to your bills (*.pdf) folder")
    args = argParser.parse_args()

    return args


def main():
    args = getArgs()
    paths = getFilesPaths(args.path)

    if not paths:
        return

    generateCsvFile(paths)


if __name__ == '__main__':
    main()
