import PyPDF2
import pprint
import sys
import re


class Class_schedule:
    def __init__(self, type, title, page_content):
        self.title = title
        self.type = type
        self.clear_page_content(page_content)
        self.set_name()
        self.set_cars()
        self.set_ir_license()
        self.set_schedule()

    def __str__(self):
        r = 'Name: ' + self.name + '\n'
        r += 'Type: ' + self.type + '\n'
        r += 'Cars: ' + str(self.cars) + '\n'
        r += 'Ir_license: ' + self.ir_license + '\n'
        r += 'Schedule: ' + str(self.schedule)
        return r

    def clear_page_content(self, page_content):
        left_part = page_content[0].split(self.title)[0]
        page_content[0] = page_content[0][len(left_part):]
        self.page_content = page_content

    def set_name(self):
        self.name = self.title.split('-')[0].strip()

    def set_cars(self):
        self.cars = []
        cars = self.page_content[0].split(
            self.title)[1].strip()
        self.cars = cars
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
        ir_lic = self.page_content[0].split(
            self.cars[len(self.cars) - 1])[1].strip()
        self.ir_license = re.split(
            'races', ir_lic, flags=re.IGNORECASE)[0].strip()

    def set_schedule(self):
        weeks = self.page_content[0].split('Week')
        if len(self.page_content) > 1:  # 2 pages
            print('MULTIPAGEEEEEEEEE')
            print(str(weeks))
            new_week = self.page_content[1].split('Week')
            for w in new_week:
                if w != '':
                    weeks.append(w)

            print('weeks len: ', str(len(weeks)))
            print(str(weeks))
        week_nums = []
        dates = []
        tracks = []
        races_length = []
        counter = 0
        # print(str(len(self.page_content)) + 'WIIIIIKS: ' + str(weeks))
        for week in weeks:
            counter = counter+1
            if counter == 1:
                continue
            split_week_num = week.split(' (')
            split_date = split_week_num[1].strip().split(')')
            split_track = split_date[1].strip().split('(')
            split_race_length = week.split('.')
            split_race_length2 = split_race_length[len(
                split_race_length)-1].strip()
            if not 'laps' in split_race_length2:
                split_race_length2 = split_race_length2.split('mins')
            else:
                split_race_length2 = split_race_length2.split('laps')
            # split_race_length2 = split_race_length[len(split_race_length)-1].strip().split('laps')
            week_num = split_week_num[0].strip()
            date = split_date[0].strip()
            track = split_track[0].strip()
            race_length = split_race_length2[0].strip()
            # print('Week ' + week_num)
            # print(date)
            # print(track)
            # print(lap + ' laps')
            # print('---------')
            week_nums.append(week_num)
            dates.append(date)
            tracks.append(track)
            races_length.append(race_length)
            # TODO: be able to differenciate between laps and mins race length

        self.schedule = [week_nums, dates, tracks, races_length]


def main():
    pdf_filename = get_PDF_filename()  # getting the pdf path
    pdf_file = get_PDF_object(pdf_filename)  # creating pdf object
    pdf_fileReader = PyPDF2.PdfFileReader(pdf_file)  # creating pdf reader obj
    categories = get_categories(pdf_fileReader)  # based on index page
    # print(categories)

    category_pos = 0
    pdf_total_pages = pdf_fileReader.getNumPages()
    skip_next_page = False
    pr_nxt_cat = False
    for num_page in range(0, pdf_total_pages):
        # if category_pos == 44:
        #     break

        # skip next page if we already read it joined with the previous one
        if skip_next_page:
            print('\n\n\nSkipping page ' + str(num_page))
            skip_next_page = False
            continue

        # check if page is index
        page = get_content_from_page(pdf_fileReader, num_page)
        if not 'Week' in page:
            continue

        # check if next page is continuation of the previous one
        is_last_page = (num_page == pdf_total_pages - 1)
        if not is_last_page:
            next_page = get_content_from_page(pdf_fileReader, (num_page + 1))
        if next_page.strip().startswith('Week '):
            if not 'Season' in next_page:
                print('\n\nSKIPPING PAGEEEEEE ' + str(num_page) + ' \n\n')
                skip_next_page = True

        # create class_schedule and print it out
        type = categories[category_pos][0]
        category = categories[category_pos][1]
        if not is_last_page and skip_next_page:
            next_page = get_content_from_page(pdf_fileReader, (num_page + 1))
            # # remove content not related to this category on next page
            # print('\n\nCACA ' + categories[category_pos+1][1] + '\n\n')

            # if categories[category_pos+1][1] in next_page:
            #     print('\n\n\nSUUUUUUUUUUUH\n\n\n')
            #     next_page = next_page.split(categories[category_pos+1][1])[0]

            page = [page, next_page]
            print('\n\n PAGE: ' + str(page) + '\n\n')
            print('\n\n NEXT PAGE: ' + str(next_page) + '\n\n')
            # check if next page is shared with another category
            if not categories[category_pos+1][1] in next_page:
                skip_next_page = True
        else:
            # if category == 'iRacing Le Mans Series- 2020 Season 2':
            #     import pdb
            #     pdb.set_trace()
            if not page.startswith(category):
                temp_page = page.split(categories[category_pos][1])[1]
                temp_page = categories[category_pos][1] + temp_page
                page = temp_page
            page = [page]
        class_sch = Class_schedule(type, category, page)
        print(category)
        if pr_nxt_cat:
            print(class_sch)
        if category == 'iRacing Le Mans Series- 2020 Season 2' or category == 'IMSA Sportscar Championship - 2020 Season 2':
            print(class_sch)
            pr_nxt_cat = True
        else:
            pr_nxt_cat = False
        category_pos = category_pos + 1
        # print(class_sch)

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
                # remove dots so we can get the name clean
                line_1 = line.split('Season')
                line_2 = line_1[1].replace('.', '')
                line_final = line_1[0] + 'Season' + line_2
                categories.append([type, line_final.strip()])

    return categories

# if there is next page, and it starts with week 7, join last class obj


main()

# print the number of pages in pdf file
# print(fileReader.getPage(4))
# pageObj = fileReader.getPage(41)
# text = pageObj.extractText()
# text = text.split('Week')
