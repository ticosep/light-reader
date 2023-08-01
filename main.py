import argparse
import glob
import easyocr
import os
import csv
import time
from pdf2image import convert_from_path


def cropImageForFastProcess(image, count):
    left = image.width / 2
    top = 750
    right = image.width - 1800
    bottom = image.height / 3.7

    image.crop((left, top, right, bottom)).save(
        f'image_{count}.png', 'PNG')


def clearImage(imagePath):
    print("Deleting old image")
    if os.path.exists(imagePath):
        try:
            os.remove(imagePath)
            print("removed" + imagePath)
        except OSError as e:
            print("Failed with:", e.strerror)
            print("Error code:", e.code)


def getBillsInfo(filesPaths):
    count = 0
    reader = easyocr.Reader(['pt'], verbose=False, gpu=False, quantize=True)
    results = []
    for path in filesPaths:
        imageName = f'image_{count}.png'
        imagePath = './' + imageName

        clearImage(imagePath)

        print("Converting PDF to image")
        images = convert_from_path(
            path, poppler_path=r"C:\Users\tico\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin", first_page=1, last_page=1, dpi=800, grayscale=True)

        print("Cropping image for better usage")
        cropImageForFastProcess(images[0], count)

        print("Extracting information form the bill image")
        result = reader.readtext(imagePath, detail=0)

        results.append(result)

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

    results = getBillsInfo(paths)

    writeCsvFile(results)

    end = time.time()
    
    print('it took ' + time.strftime('%H:%M:%S', time.gmtime(end - start)) + ' to get your light data, use a computer with GPU for better performance')



if __name__ == '__main__':
    main()
