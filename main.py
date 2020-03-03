import PyPDF2
import pprint
import sys


class class_schedule:
    def __init__(self, page_content):
        self.name = ''
        self.cars = ''
        self.ir_license = ''
        self.schedule = ''
        self.dates = ''
        self.tracks = ''
        self.duration = ''


def main():
    pdf_filename = get_PDF_filename()  # getting the pdf path
    pdf_file = get_PDF_object(pdf_filename)  # creating pdf object
    pdf_fileReader = PyPDF2.PdfFileReader(pdf_file)  # creating pdf reader obj
    print(getContentFromPage(pdf_fileReader, 11))
    print('\n\n' + str(pdf_fileReader.getNumPages()))


def get_PDF_filename():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return sys.exit('You need to specify the pdf location as the first argument!')


def get_PDF_object(pdf_filename):
    try:
        return open(pdf_filename, 'rb')
    except:
        sys.exit('Can\'t find the specified file')


def getContentFromPage(pdf_fileReader, n):
    return pdf_fileReader.getPage(n).extractText()


main()

# print the number of pages in pdf file
# print(fileReader.getPage(4))
# pageObj = fileReader.getPage(41)
# text = pageObj.extractText()
# text = text.split('Week')

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(text)
