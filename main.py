import PyPDF2
import pprint
import sys
from class_schedule import Class_schedule


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
