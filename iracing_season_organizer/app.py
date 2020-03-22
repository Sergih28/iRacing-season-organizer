import sys
from .pdf.pdf import extract_pdf_info
from .classes.class_schedule import Class_schedule
from .data.free_content import get_free_content
from .xlsx.cell import set_cell_styles
from .xlsx.legend import print_buttons, print_owned_missing, print_classes
import xlsxwriter
from .data.dics import col_sizes
from .data.colors import content
from .xlsx.ir_license import get_license_colors


def run():
    # create xlsx file
    ir_season = "2020S2"
    workbook = xlsxwriter.Workbook(
        'iracing_season_organizer/output/iRacing_' + ir_season + '_organizer.xlsx')

    # starting columns for non-content pages
    tracks_col = 2
    cars_col = 6
    legends_col = 5
    weeks_col = 7
    categories_col = 8

    # create cell formats
    cell_format_main = workbook.add_format()
    cell_format_content_owned = workbook.add_format()
    cell_format_content_not_owned = workbook.add_format()

    # style cell formats
    set_cell_styles(cell_format_main, align='vcenter')
    set_cell_styles(cell_format_content_owned,
                    bg_color=content['bg_colors']['owned'])
    set_cell_styles(cell_format_content_not_owned,
                    bg_color=content['bg_colors']['missing'], color=content['colors']['alt'])

    cell_format_content = [cell_format_content_owned,
                           cell_format_content_not_owned]

    pdf_info = extract_pdf_info()

    # ---------- CONTENT PAGE ----------
    worksheet_content = workbook.add_worksheet('CONTENT')

    tracks_list = []
    cars_list = []
    tracks_cells_list = {}  # 'name':{ 'row': N, 'col': N}
    cars_cells_list = {}  # 'name':{ 'row': N, 'col': N}

    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        fill_tracks_list(pdf_obj, tracks_list)
        fill_cars_list(pdf_obj, cars_list)

    # --- TRACKS ---
    print_content(workbook, worksheet_content, tracks_list,
                  tracks_col, 'tracks', tracks_cells_list)

    # --- CARS ---
    print_content(workbook, worksheet_content,
                  cars_list, cars_col, 'cars', cars_cells_list)
    # ----------------------------------

    categories = {}
    fill_categories_dic(workbook, categories, categories_col)

    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        cell_format_temp = workbook.add_format()
        set_cell_styles(cell_format_temp, align='vcenter')

        # Fill pages data
        type = pdf_obj.get_type().replace(' ', '_').lower()
        if type != 'fun':
            print_content(workbook, categories[type]['worksheet'], tracks_list,
                          tracks_col, 'tracks', tracks_cells_list, linked_content=True)
            update_page(workbook, pdf_obj, categories,
                        cell_format_temp, cell_format_main, cell_format_content, type, content, tracks_cells_list, weeks_col)

    set_auto_col_width(categories, legends_col, categories_col)

    # ---------- LEGEND ----------
    print_buttons(workbook, categories, 4, legends_col)
    print_owned_missing(workbook, categories, 8, legends_col)
    print_classes(workbook, categories, 11, legends_col)

    workbook.close()


def update_page(workbook, pdf_obj, categories, cell_format, cell_format_main, cell_format_content, category, content, tracks_cells_list, start_col):
    free_content = get_free_content()
    worksheet = categories[category]['worksheet']
    col = categories[category]['col']
    weeks_done = categories[category]['weeks_done']

    # set bg color and font color for that cell
    cell_format_colorised = cell_format
    license_colors = get_license_colors(pdf_obj.get_ir_license())
    cell_format_colorised.set_bg_color(license_colors[0])
    cell_format_colorised.set_font_color(license_colors[1])
    set_cell_styles(cell_format_colorised, bold=True)

    worksheet.write(2, col, pdf_obj.get_name(),
                    cell_format_colorised)

    cars = pdf_obj.get_cars()
    for car in cars:
        if car in free_content[1]:
            cell_format_cars = cell_format_content[0]
            break
        else:
            cell_format_cars = cell_format_content[1]
    cell_format_cars.set_align('vcenter')
    set_cell_styles(cell_format_cars)
    worksheet.write(3, col, '\n'.join(cars), cell_format_cars)

    # set week column
    if not weeks_done:
        row = 3
        cell_format_week = workbook.add_format()
        cell_format_week.set_bg_color('yellow')
        set_cell_styles(cell_format_week, bold=True)
        # write week num headers
        dates = pdf_obj.get_dates()
        if len(dates) == 12:
            for week in range(1, 13):
                row = row + 1

                # get the first 12 week race Series
                worksheet.write(row, start_col, 'Week ' +
                                str(week) + ' (' + str(dates[week-1]) + ')', cell_format_week)
            weeks_done = True

    tracks = pdf_obj.get_tracks()
    races_type = pdf_obj.get_races_type()
    races_length = pdf_obj.get_races_length()
    row = 3

    for track in tracks:
        row = row + 1

        # save track length if it's higher than current
        track_length = len(track)
        if col in col_sizes[category]:
            category_row_size = col_sizes[category][col]
            if category_row_size < track_length:
                col_sizes[category][col] = track_length
        else:
            col_sizes[category][col] = track_length

        if not ':' in races_length[row-4]:
            content_text = ' (' + races_length[row-4] + ' ' + races_type + ')'
        else:
            content_text = ' (' + races_length[row-4] + ')'

        cell_format_track = workbook.add_format()
        set_cell_styles(cell_format_track)
        # hhh
        track_row = tracks_cells_list[track]['row']
        track_col = tracks_cells_list[track]['col']
        track_letter = num_to_letter(track_col)
        track_letter_prev = num_to_letter(track_col - 1)
        criteria = '=CONCAT(CONTENT!' + track_letter + \
            str(track_row) + ', "' + content_text + '")'

        worksheet.write(row, col, criteria, cell_format_track)

        criteria_Y = '='+track_letter_prev+str(track_row)+'="Y"'
        criteria_N = '='+track_letter_prev+str(track_row)+'="N"'

        cell_green = workbook.add_format()
        cell_gray = workbook.add_format()
        set_cell_styles(
            cell_green, bg_color=content['bg_colors']['owned'], color=content['colors']['normal'])
        set_cell_styles(
            cell_gray, bg_color=content['bg_colors']['missing'], color=content['colors']['alt'])

        worksheet.conditional_format(row, col, row, col, {
                                     'type': 'formula', 'criteria': criteria_Y, 'format': cell_green})
        worksheet.conditional_format(row, col, row, col, {
                                     'type': 'formula', 'criteria': criteria_N, 'format': cell_gray})

    categories[category]['col'] += 1

    # hide content rows in non-content pages
    worksheet.set_column('A:D', None, None, {'hidden': True})


def fill_categories_dic(workbook, categories, start_col):
    categories_list = ['road', 'oval', 'dirt_road', 'dirt_oval']
    for category in categories_list:
        categories[category] = {}
        categories[category]['worksheet'] = workbook.add_worksheet(
            category.upper())
        categories[category]['col'] = start_col
        categories[category]['weeks_done'] = False


def fill_tracks_list(pdf_obj, tracks_list):
    tracks = pdf_obj.get_tracks()
    for track in tracks:
        tracks_list.append(track)


def fill_cars_list(pdf_obj, cars_list):
    cars = pdf_obj.get_cars()
    for car in cars:
        cars_list.append(car)


def set_auto_col_width(categories, legend_col, categories_col):
    for category in categories:
        worksheet = categories[category]['worksheet']
        # fixed column widths for first fixed rows
        worksheet.set_column(legend_col, legend_col, 12)
        worksheet.set_column(legend_col + 1, legend_col + 1, 4)
        worksheet.set_column(legend_col + 2, legend_col + 2, 25)

        # auto column widths // +4
        for col in range(categories_col, categories[category]['col']):
            if category == 'dirt_oval':
                col_size = col_sizes[category][col] * 1.9
            else:
                col_size = col_sizes[category][col] * 1.55

            worksheet.set_column(col, col, col_size)


def print_content(workbook, worksheet_content, content_list, col, content_type, cells_list, linked_content=False):
    worksheet_content.set_column(col, col, 45)
    content_list = sorted(content_list)
    if content_type == 'tracks':
        free_content = get_free_content()[0]
        letter_row = 'B'
    else:
        free_content = get_free_content()[1]
        letter_row = 'F'
    cell_green = workbook.add_format()
    cell_gray = workbook.add_format()
    cell_title = workbook.add_format()
    set_cell_styles(cell_title, bold=True)
    set_cell_styles(
        cell_green, bg_color=content['bg_colors']['owned'], color=content['colors']['normal'])
    set_cell_styles(
        cell_gray, bg_color=content['bg_colors']['missing'], color=content['colors']['alt'])

    worksheet_content.write(1, col-1, 'OWNED', cell_title)
    worksheet_content.write(1, col, content_type.upper(), cell_title)
    worksheet_content.write(1, col+1, 'USAGE', cell_title)

    row = 2
    count = 0
    content_usage = {}

    for content_item in content_list:
        content_list[count] = content_item
        if content_item in content_usage:
            content_usage[content_item] += 1
        else:
            content_usage[content_item] = 1
        count = count + 1

    # remove duplicate content
    content_list = list(dict.fromkeys(content_list))
    total_content = len(content_list) + 1
    for content_item in content_list:
        cell_content = workbook.add_format()
        if linked_content:
            worksheet_content.write(row-1, col-1, '=CONTENT!B' + str(row))
            worksheet_content.write(row-1, col, '=CONTENT!C' + str(row))
            worksheet_content.write(row-1, col+1, '=CONTENT!D' + str(row))
            row = row + 1
            continue
        if content_item in free_content:
            worksheet_content.write(row, col-1, 'Y')
        else:
            worksheet_content.write(row, col-1, 'N')

        # condition to paint the bg_color depending on the row OWNED
        criteria_Y = '=$'+letter_row+str(row+1)+'="Y"'
        criteria_N = '=$'+letter_row+str(row+1)+'="N"'

        worksheet_content.conditional_format(2, col-1, total_content, col+1, {'type': 'formula',
                                                                              'criteria': criteria_Y, 'format': cell_green})
        worksheet_content.conditional_format(2, col-1, total_content, col+1, {'type': 'formula',
                                                                              'criteria': criteria_N, 'format': cell_gray})
        worksheet_content.data_validation(
            2, col-1, total_content, col-1, {'validate': 'list', 'source': ['Y', 'N']})

        content_usage_temp = content_usage[content_item]
        worksheet_content.write(row, col, content_item, cell_content)
        worksheet_content.write(row, col+1, content_usage_temp, cell_content)

        # save cell position to be able to link it later
        cells_list[content_item] = {}
        cells_list[content_item]['row'] = row + 1
        cells_list[content_item]['col'] = col

        row = row + 1


def num_to_letter(n):
    return chr(n + 65)
