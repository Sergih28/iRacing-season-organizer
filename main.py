import PyPDF2
import pprint
import sys


def get_PDF_file():
    if len(sys.argv) > 1:
        return sys.argv[1]
    print('You need to specify the pdf location as the first argument!')
    return sys.exit()


# print(get_PDF_file())

# creating an object
# file = open('2020S2.pdf', 'rb')

# creating a pdf reader object
# fileReader = PyPDF2.PdfFileReader(file)

# print the number of pages in pdf file
# print(fileReader.getPage(4))
# pageObj = fileReader.getPage(41)
# text = pageObj.extractText()
# text = text.split('Week')

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(text)
