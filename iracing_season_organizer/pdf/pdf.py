import PyPDF2
import sys
from ..class_schedule import Class_schedule


def extract_pdf_info():
    pdf_info = []  # all info we're going to extract from the pdf here
    pdf_filename = get_PDF_filename()  # getting the pdf path
    pdf_file = get_PDF_object(pdf_filename)  # creating pdf object
    pdf_fileReader = PyPDF2.PdfFileReader(pdf_file)  # creating pdf reader obj
    categories = get_categories(pdf_fileReader)  # based on index page

    # writting ouput to file for testing purposes
    f = open("iracing_season_organizer/output/output.txt", "w")

    category_pos = 0
    pdf_total_pages = pdf_fileReader.getNumPages()
    skip_next_page = False
    for num_page in range(0, pdf_total_pages):
        page = get_content_from_page(pdf_fileReader, num_page)
        omit_page = omit_index_page(page)
        if omit_page:
            continue

        # skip next page if we already read it joined with the previous one
        if skip_next_page:
            skip_next_page = False
            continue

        is_last_page = (num_page == pdf_total_pages - 1)
        type = categories[category_pos][0]

        # Do not show FUN races
        if type == 'FUN':
            continue

        category = categories[category_pos][1]
        next_category = ''
        next_page = ''
        next_page_shared = False
        # page_shared = False
        continues_next_page = False

        if not is_last_page:
            next_page_num = num_page + 1
            next_category = categories[category_pos + 1][1]
            next_page = get_content_from_page(pdf_fileReader, (next_page_num))
            omit_next_page = omit_index_page(next_page)
            if omit_next_page:
                next_page_num = num_page + 2
                next_page = get_content_from_page(
                    pdf_fileReader, (next_page_num))

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

            last_week = get_last_week(page)
            next_page_first_week = get_first_week(next_page)

            # extra check if week 1 and week 12 are on the same next page
            # check if the first week on the next page is +1 of last week of current page
            if next_category in next_page and last_week == (next_page_first_week - 1):
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
        # pdf_info.append(class_sch)
        pdf_info.append([class_sch.get_name(), class_sch.get_type(
        ), class_sch.get_cars(), class_sch.get_ir_license(), class_sch.get_schedule()])

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


def omit_index_page(page):
    if not 'Week' in page:
        return True
    return False


def get_last_week(page):
    weeks_split = page.split('Week ')
    weeks_split = weeks_split[len(weeks_split)-1].split(' (')
    last_week = int(weeks_split[0])
    return last_week


def get_first_week(page):
    weeks2_split = page.split('Week ')
    weeks2_split = weeks2_split[1].split(' (')
    first_week = int(weeks2_split[0])
    return first_week
