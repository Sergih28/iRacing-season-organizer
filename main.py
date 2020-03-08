import sys
from pdf import extract_pdf_info
from class_schedule import Class_schedule
from free_content import get_free_content
from cell import set_cell_styles
from legend import print_buttons, print_owned_missing, print_classes
import xlsxwriter
from dics import content, col_sizes
from xlsx import get_license_colors


def main():
    # create xlsx file
    workbook = xlsxwriter.Workbook('output.xlsx')

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

    tracks_list = []
    cars_list = []

    pdf_info = extract_pdf_info()

    categories = {}
    fill_categories_dic(workbook, categories, 4)

    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        cell_format_temp = workbook.add_format()
        set_cell_styles(cell_format_temp, align='vcenter')

        # Fill pages data
        type = pdf_obj.get_type().replace(' ', '_').lower()
        if type != 'fun':
            update_page(workbook, pdf_obj, categories,
                        cell_format_temp, cell_format_main, cell_format_content, type, content)

        fill_tracks_list(pdf_obj, tracks_list)
        fill_cars_list(pdf_obj, cars_list)

    set_auto_col_width(categories)

    # ---------- LEGEND ----------
    print_buttons(workbook, categories, 4)
    print_owned_missing(workbook, categories, 8)
    print_classes(workbook, categories, 11)

    # ---------- CONTENT PAGE ----------
    worksheet_content = workbook.add_worksheet('CONTENT')
    # --- TRACKS ---
    worksheet_content.set_column(2, 2, 45)
    tracks_list = sorted(tracks_list)
    free_tracks = get_free_content()[0]
    cell_green = workbook.add_format()
    cell_gray = workbook.add_format()
    # cell_blank = workbook.add_format()
    cell_title = workbook.add_format()
    set_cell_styles(cell_title, bold=True)
    set_cell_styles(
        cell_green, bg_color=content['bg_colors']['owned'], color=content['colors']['normal'])
    set_cell_styles(
        cell_gray, bg_color=content['bg_colors']['missing'], color=content['colors']['alt'])

    worksheet_content.write(1, 1, 'OWNED', cell_title)
    worksheet_content.write(1, 2, 'TRACKS', cell_title)
    worksheet_content.write(1, 3, 'USAGE', cell_title)

    row = 2
    count = 0
    tracks_usage = {}

    for track in tracks_list:
        track_clean_name = track
        tracks_list[count] = track_clean_name
        if track_clean_name in tracks_usage:
            tracks_usage[track_clean_name] += 1
        else:
            tracks_usage[track_clean_name] = 1
        count = count + 1

    # remove duplicate tracks
    tracks_list = list(dict.fromkeys(tracks_list))
    total_tracks = len(tracks_list) + 1
    for track in tracks_list:
        cell_track = workbook.add_format()
        if track in free_tracks:
            worksheet_content.write(row, 1, 'Y')
        else:
            worksheet_content.write(row, 1, 'N')

        # condition to paint the bg_color depending on the row OWNED
        criteria_Y = '=$B'+str(row+1)+'="Y"'
        criteria_N = '=$B'+str(row+1)+'="N"'

        worksheet_content.conditional_format(2, 1, total_tracks, 3, {'type': 'formula',
                                                                     'criteria': criteria_Y, 'format': cell_green})
        worksheet_content.conditional_format(2, 1, total_tracks, 3, {'type': 'formula',
                                                                     'criteria': criteria_N, 'format': cell_gray})
        worksheet_content.data_validation(
            2, 1, total_tracks, 1, {'validate': 'list', 'source': ['Y', 'N']})

        track_usage = tracks_usage[track]
        worksheet_content.write(row, 2, track, cell_track)
        worksheet_content.write(row, 3, track_usage, cell_track)
        row = row + 1

    # --- CARS ---
    worksheet_content.set_column(6, 6, 45)
    cars_list = sorted(cars_list)
    free_cars = get_free_content()[1]
    cell_green_cars = workbook.add_format()
    cell_gray_cars = workbook.add_format()
    cell_title = workbook.add_format()
    set_cell_styles(cell_title, bold=True)
    set_cell_styles(
        cell_green_cars, bg_color=content['bg_colors']['owned'], color=content['colors']['normal'])
    set_cell_styles(
        cell_gray_cars, bg_color=content['bg_colors']['missing'], color=content['colors']['alt'])

    worksheet_content.write(1, 5, 'OWNED', cell_title)
    worksheet_content.write(1, 6, 'CARS', cell_title)
    worksheet_content.write(1, 7, 'USAGE', cell_title)

    row = 2
    count = 0
    cars_usage = {}

    for car in cars_list:
        cars_list[count] = car
        if car in cars_usage:
            cars_usage[car] += 1
        else:
            cars_usage[car] = 1
        count = count + 1

    # remove duplicate tracks
    cars_list = list(dict.fromkeys(cars_list))
    total_cars = len(cars_list) + 1
    for car in cars_list:
        cell_car = workbook.add_format()
        if car in free_cars:
            worksheet_content.write(row, 5, 'Y')
        else:
            worksheet_content.write(row, 5, 'N')

        # condition to paint the bg_color depending on the row OWNED
        criteria_Y = '=$F'+str(row+1)+'="Y"'
        criteria_N = '=$F'+str(row+1)+'="N"'

        worksheet_content.conditional_format(2, 5, total_cars, 7, {'type': 'formula',
                                                                   'criteria': criteria_Y, 'format': cell_green_cars})
        worksheet_content.conditional_format(2, 5, total_cars, 7, {'type': 'formula',
                                                                   'criteria': criteria_N, 'format': cell_gray_cars})
        worksheet_content.data_validation(
            2, 5, total_cars, 5, {'validate': 'list', 'source': ['Y', 'N']})

        car_usage = cars_usage[car]
        worksheet_content.write(row, 6, car, cell_car)
        worksheet_content.write(row, 7, car_usage, cell_car)
        row = row + 1

    workbook.close()


def update_page(workbook, pdf_obj, categories, cell_format, cell_format_main, cell_format_content, category, content):
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

    worksheet.write(2, col, pdf_obj.get_name(), cell_format_colorised)

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
                worksheet.write(row, 3, 'Week ' +
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

        # colorise background depending if it is owned content or not
        if track in free_content[0]:
            cell_format_track = cell_format_content[0]
        else:
            cell_format_track = cell_format_content[1]

        # special check for rallycross weird lap length
        if not ':' in races_length[row-4]:
            content = track + \
                ' (' + races_length[row-4] + ' ' + races_type + ')'
        else:
            content = track + ' (' + races_length[row-4] + ')'
        set_cell_styles(cell_format_track)
        worksheet.write(row, col, content, cell_format_track)

    categories[category]['col'] += 1


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


def set_auto_col_width(categories):
    for category in categories:
        worksheet = categories[category]['worksheet']
        # fixed column widths for first fixed rows
        worksheet.set_column(1, 1, 12)
        worksheet.set_column(2, 2, 4)
        worksheet.set_column(3, 3, 25)

        # auto column widths
        for col in range(4, categories[category]['col']):
            if category == 'dirt_oval':
                col_size = col_sizes[category][col] * 1.9
            else:
                col_size = col_sizes[category][col] * 1.55

            worksheet.set_column(col, col, col_size)


main()

# FIXME: iRLMS series and endurance not getting correct schedule
# TODO: Extra tab with "what can I race", based on the content
# TODO: A way to filter the owned content
# TODO: Check if tracks count is working properly
# TODO: link track names in the pages with the CONTENT page
# TODO: Link cars in the pages with the CONTENT page (therefore sepparate them in individual cells)
# TODO: Lock cells
# TODO: Ability to hide series (with VBA)
# TODO: move below the series that don't have 12 weeks, so they can get the correct dates on the weeks
# TODO: Make fun page
# TODO: Porsche 911RSR and Porsche 911 RSR should be the same car, right?
