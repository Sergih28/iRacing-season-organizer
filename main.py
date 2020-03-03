import PyPDF2
import pprint
import sys


class Class_schedule:
    def __init__(self, title, page_content):
        self.title = title
        self.page_content = page_content
        self.set_name()
        self.set_cars()
        self.ir_license = ''
        self.schedule = ''
        self.dates = ''
        self.tracks = ''
        self.duration = ''

    def __str__(self):
        r = 'name: ' + self.name + '\n'
        r += 'cars: ' + self.cars + '\n'
        r += 'ir_license: ' + self.ir_license + '\n'
        r += 'schedule: ' + self.schedule + '\n'
        r += 'dates: ' + self.dates + '\n'
        r += 'tracks: ' + self.tracks + '\n'
        r += 'duration: ' + self.duration
        return r

    def set_name(self):
        self.name = self.title.split('-')[0].strip()
        # self.name = page_content.split('-')[0].strip()

    def set_cars(self):
        cars = self.page_content.split(
            self.title)[1]
        if 'Rookie' in cars:
            self.cars = cars.split('Rookie')[0].strip()
        elif 'Class D' in cars:
            self.cars = cars.split('Class D')[0].strip()
        elif 'Class C' in cars:
            self.cars = cars.split('Class C')[0].strip()
        elif 'Class B' in cars:
            self.cars = cars.split('Class B')[0].strip()
        elif 'Class A' in cars:
            self.cars = cars.split('Class A')[0].strip()
        # self.cars = page_content.split(
        #     'Season 2')[1].split('Rookie')[0].strip()


def main():
    pdf_filename = get_PDF_filename()  # getting the pdf path
    pdf_file = get_PDF_object(pdf_filename)  # creating pdf object
    pdf_fileReader = PyPDF2.PdfFileReader(pdf_file)  # creating pdf reader obj
    # pdf_total_pages = pdf_fileReader.getNumPages()
    # test = getContentFromPage(pdf_fileReader, 0)
    # print(test)
    title = 'Skip Barber Race Series - 2020 Season 2'
    skippy_class = Class_schedule(
        title, getContentFromPage(pdf_fileReader, 22))
    print(skippy_class)

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(skippy_class)


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
