import pdfreader
import argparse
import glob
from pdfreader import PDFDocument


def getArgs():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-p", "--path", help="path to your bills folder")
    args = argParser.parse_args()

    return args


def main():
    args = getArgs()
    print("path=%s" % args.path)
    print(glob.glob(args.path + "*.pdf"))


if __name__ == '__main__':
    main()
