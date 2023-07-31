import argparse
import glob
import easyocr
from pdf2image import convert_from_path


def generateCsvFile(filesPaths):
    count = 0
    for path in filesPaths:
        images = convert_from_path(
            path, poppler_path=r"C:\Users\tico\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin")
        images[0].save(f'image_{count}.png', 'PNG')
        count += 1


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
