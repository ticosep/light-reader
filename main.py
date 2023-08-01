import argparse
import glob
import easyocr
import os
from PIL import Image
from pdf2image import convert_from_path


def cropImageForFastProcess(image, count):
    left = image.width / 2
    top = 750
    right = image.width - 1800
    bottom = image.height / 3.7


    image.crop((left, top, right, bottom)).save(
        f'image_{count}.png', 'PNG')


def clearImage(imagePath):
    print("Clearing old image")
    if os.path.exists(imagePath):
        try:
            os.remove(imagePath)
            print("removed" + imagePath)
        except OSError as e:
            print("Failed with:", e.strerror)
            print("Error code:", e.code)


def generateCsvFile(filesPaths):
    count = 0
    reader = easyocr.Reader(['pt'], verbose=False, gpu=False, quantize=True)
    for path in filesPaths:
        imageName = f'image_{count}.png'
        imagePath = './' + imageName

        clearImage(imagePath)

        images = convert_from_path(
            path, poppler_path=r"C:\Users\tico\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin", first_page=1, last_page=1, dpi=800, grayscale=True)

        cropImageForFastProcess(images[0], count)

        result = reader.readtext(imagePath, detail = 0)

        print(result)

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
