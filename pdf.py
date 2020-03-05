import PyPDF2
import sys
from class_schedule import Class_schedule


def extract_pdf_info():
    pdf_info = []  # all info we're going to extract from the pdf here
    pdf_filename = get_PDF_filename()  # getting the pdf path
    pdf_file = get_PDF_object(pdf_filename)  # creating pdf object
    pdf_fileReader = PyPDF2.PdfFileReader(pdf_file)  # creating pdf reader obj
    categories = get_categories(pdf_fileReader)  # based on index page
    # print(categories)

    # writting ouput to file for testing purposes
    f = open("output.txt", "w")

    category_pos = 0
    pdf_total_pages = pdf_fileReader.getNumPages()
    skip_next_page = False
    for num_page in range(0, pdf_total_pages):
        # omit index pages
        page = get_content_from_page(pdf_fileReader, num_page)
        if not 'Week' in page:
            continue

        # skip next page if we already read it joined with the previous one
        if skip_next_page:
            skip_next_page = False
            continue

        is_last_page = (num_page == pdf_total_pages - 1)
        type = categories[category_pos][0]
        category = categories[category_pos][1]
        next_category = ''
        next_page = ''
        next_page_shared = False
        # page_shared = False
        continues_next_page = False

        if not is_last_page:
            next_category = categories[category_pos + 1][1]
            next_page = get_content_from_page(pdf_fileReader, (num_page + 1))

            # check if next page is shared with another category
            try:
                next_next_category = categories[category_pos + 2][1]
                if next_next_category != '':
                    next_page_shared = is_page_shared(
                        next_page, next_category, next_next_category)
            except:
                next_page_shared = False

            # check if this page is shared with another category
            # page_shared = is_page_shared(page, category, next_category)

            # check if next page belongs to this category
            if not next_category in next_page and 'Week' in next_page:
                continues_next_page = True

            # omit next page if it's related only with the current one
            if not next_page_shared and continues_next_page:
                skip_next_page = True

            # remove next category info in next page if needed
            if next_page_shared and continues_next_page:
                next_page = next_page.split(categories[category_pos+1][1])[0]

            if continues_next_page:
                page = [page, next_page]
            else:
                page = [page]

        else:
            page = [page]

        class_sch = Class_schedule(type, category, page)

        if not category_pos == 0:
            f.write('\n\n------------------------------------\n\n')
        f.write(str(class_sch))
        pdf_info.append(class_sch)

        category_pos = category_pos + 1

    f.close()
    return pdf_info


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


def is_page_shared(page, category, next_category):
    page_split1 = page.split(category)
    if len(page_split1) > 1 and 'Week' in page_split1[0] and 'Week' in page_split1[1]:
        return True

    page_split2 = page.split(next_category)
    if len(page_split2) > 1:
        if 'Week' in page_split2[0] and 'Week' in page_split2[1]:
            return True
    return False