import PyPDF2
import pprint
import sys
import re


class Class_schedule:
    def __init__(self, type, title, page_content):
        self.title = title
        self.type = type
        self.page_content = page_content
        self.set_name()
        self.set_cars()
        self.set_ir_license()
        self.set_schedule()

    def __str__(self):
        r = 'Name: ' + self.name + '\n'
        r += 'Cars: ' + str(self.cars) + '\n'
        r += 'Ir_license: ' + self.ir_license + '\n'
        r += 'Schedule: ' + str(self.schedule)
        return r

    def set_name(self):
        self.name = self.title.split('-')[0].strip()

    def set_cars(self):
        self.cars = []
        cars = self.page_content.split(
            self.title)[1].strip()
        if 'Rookie' in cars:
            cars = cars.split('Rookie')[0].strip()
        elif 'Class D' in cars:
            cars = cars.split('Class D')[0].strip()
        elif 'Class C' in cars:
            cars = cars.split('Class C')[0].strip()
        elif 'Class B' in cars:
            cars = cars.split('Class B')[0].strip()
        elif 'Class A' in cars:
            cars = cars.split('Class A')[0].strip()

        self.cars = [car.strip() for car in cars.split(',')]

    def set_ir_license(self):
        ir_lic = self.page_content.split(
            self.cars[len(self.cars) - 1])[1].strip()
        self.ir_license = re.split(
            'races', ir_lic, flags=re.IGNORECASE)[0].strip()

    def set_schedule(self):
        weeks = self.page_content.split('Week')
        week_nums = []
        dates = []
        tracks = []
        laps = []
        counter = 0
        for week in weeks:
            counter = counter+1
            if counter == 1:
                continue
            split_week_num = week.split(' (')
            split_date = split_week_num[1].strip().split(')')
            split_track = split_date[1].strip().split('(')
            split_lap = week.split('.')
            split_lap2 = split_lap[len(split_lap)-1].strip().split('laps')
            week_num = split_week_num[0].strip()
            date = split_date[0].strip()
            track = split_track[0].strip()
            lap = split_lap2[0].strip()
            # print('Week ' + week_num)
            # print(date)
            # print(track)
            # print(lap + ' laps')
            # print('---------')
            week_nums.append(week_num)
            dates.append(date)
            tracks.append(track)
            laps.append(lap)

        self.schedule = [week_nums, dates, tracks, laps]


def main():
    pdf_filename = get_PDF_filename()  # getting the pdf path
    pdf_file = get_PDF_object(pdf_filename)  # creating pdf object
    pdf_fileReader = PyPDF2.PdfFileReader(pdf_file)  # creating pdf reader obj
    categories = get_categories(pdf_fileReader)  # based on index page
    # print(categories)

    category_pos = 0
    for num_page in range(0, pdf_fileReader.getNumPages()):
        if category_pos == 9:
            break
        # check if page is index
        page = get_content_from_page(pdf_fileReader, num_page)
        if not 'Week' in page:
            continue

        # check if page is continuation of the previous one

        # create class_schedule and print it out
        type = categories[category_pos][0]
        category = categories[category_pos][1]
        class_sch = Class_schedule(type, category, page)
        category_pos = category_pos + 1
        print(class_sch)

    # title = 'Skip Barber Race Series - 2020 Season 2'
    # skippy_class = Class_schedule(
    #     title, get_content_from_page(pdf_fileReader, 22))
    # print(skippy_class)

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


def get_content_from_page(pdf_fileReader, n):
    return pdf_fileReader.getPage(n).extractText()


def get_categories(pdf_fileReader):
    initial_page = get_content_from_page(pdf_fileReader, 0)
    initial_page = initial_page.split('\n')
    categories = []
    type = 'UNKNOWN'
    pdf_total_pages = pdf_fileReader.getNumPages()

    for num_page in range(0, pdf_total_pages):
        page = get_content_from_page(pdf_fileReader, num_page)
        if 'Week' in page:
            break
        page = page.split('\n')
        for line in page:
            if not 'Season' in line:
                if '(OVAL)' in line:
                    type = 'OVAL'
                elif '(ROAD)' in line:
                    type = 'ROAD'
                elif '(DIRT OVAL)' in line:
                    type = 'DIRT OVAL'
                elif '(DIRT ROAD)' in line:
                    type = 'DIRT ROAD'
                elif '(FUN)' in line:
                    type = 'FUN'
            else:
                categories.append([type, line.replace('.', '').strip()])

    return categories

# if there is next page, and it starts with week 7, join last class obj


main()

# print the number of pages in pdf file
# print(fileReader.getPage(4))
# pageObj = fileReader.getPage(41)
# text = pageObj.extractText()
# text = text.split('Week')
