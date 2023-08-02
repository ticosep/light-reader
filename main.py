import argparse
import glob
import easyocr
import numpy as np
import cv2
import os
import csv
import time
import boundingBoxSorting
from pdf2image import convert_from_path


def getCroppedImagesPath(image, count):
    image.save(
        f'image_{count}.png', 'PNG')
    imageCv2 = cv2.imread(f'image_{count}.png')
    # Load image, convert to grayscale, and find edges
    gray = cv2.cvtColor(imageCv2, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 9)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255, 255, 255), -1)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    # Draw rectangles, the 'area_treshold' value was determined empirically
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    area_treshold = 4000
    count2 = 0
    croppedImages = []
    for c in cnts:
        if cv2.contourArea(c) > area_treshold:
            x, y, w, h = cv2.boundingRect(c)
            imagePath = f'image_{count}_{count2}.png'
            print(imagePath)
            image.crop((x, y, x + w, y + h)).save(
                imagePath, 'PNG')
            croppedImages.append("./" + imagePath)
        count2 += 1
    return croppedImages


def clearImages():
    print("Deleting old images")
    dirName = "./"
    files = os.listdir(dirName)

    for file in files:
        if file.endswith(".png"):
            try:
                path = os.path.join(dirName, file)
                os.remove(path)
                print("removed: " + path)
            except OSError as e:
                print("Failed with:", e.strerror)
                print("Error code:", e.code)


def getBillsInfo(filesPaths):
    count = 0
    reader = easyocr.Reader(['pt'], verbose=False, gpu=False, quantize=True)
    results = []
    sorter = boundingBoxSorting.BoundingBoxSorting()

    for path in filesPaths:
        print("Converting PDF to image")
        images = convert_from_path(
            path, poppler_path=r"C:\Users\tico\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin", first_page=1, last_page=1, dpi=800, grayscale=True)

        print("Cropping image for better usage")
        croppedImages = getCroppedImagesPath(images[0], count)

        for croppedImage in croppedImages:
            print("Extracting information form the bill image")

            result = reader.readtext(croppedImage, batch_size=10)
            sorter.getSortedValues(result)
            results.append(result)

            print(result)

        count += 1

    return results


def writeCsvFile(results):
    print("Generating table with light bills data")

    header = ['Data', 'Consumption', 'Value']

    f = open("./billsTable.csv", "w+")

    writer = csv.writer(f)
    writer.writerow(header)

    for result in results:
        writer.writerow([result[5], result[19], result[4]])

    print("DONE! :)")

    f.close()


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
    start = time.time()
    args = getArgs()
    paths = getFilesPaths(args.path)

    if not paths:
        return

    clearImages()

    results = getBillsInfo(paths)

    writeCsvFile(results)

    end = time.time()

    print('it took ' + time.strftime('%H:%M:%S', time.gmtime(end - start)) +
          ' to get your light data, use a computer with GPU for better performance')


if __name__ == '__main__':
    main()
