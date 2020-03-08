import sys
from pdf import extract_pdf_info
from class_schedule import Class_schedule
from free_content import get_free_content
from cell import set_cell_styles
from legend import print_buttons, print_owned_missing, print_classes
import xlsxwriter
from dics import *


def main():
    workbook = xlsxwriter.Workbook('output.xlsx')
    cell_format_main = workbook.add_format()
    set_cell_styles(cell_format_main, align='vcenter')

    cell_format_content_owned = workbook.add_format()
    cell_format_content_not_owned = workbook.add_format()
    set_cell_styles(cell_format_content_owned)
    set_cell_styles(cell_format_content_not_owned)
    cell_format_content_owned.set_bg_color(
        content['bg_colors']['owned'])
    cell_format_content_not_owned.set_bg_color(
        content['bg_colors']['missing'])
    cell_format_content_not_owned.set_font_color(content['colors']['alt'])
    cell_format_content = [cell_format_content_owned,
                           cell_format_content_not_owned]

    tracks_list = []

    pdf_info = extract_pdf_info()

    categories = {
        'road': {
            'worksheet': workbook.add_worksheet('ROAD'),
            'col': 4,
            'weeks_done': False
        },
        'oval': {
            'worksheet': workbook.add_worksheet('OVAL'),
            'col': 4,
            'weeks_done': False
        },
        'dirt_road': {
            'worksheet': workbook.add_worksheet('DIRT ROAD'),
            'col': 4,
            'weeks_done': False
        },
        'dirt_oval': {
            'worksheet': workbook.add_worksheet('DIRT OVAL'),
            'col': 4,
            'weeks_done': False
        }
    }

    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        cell_format_temp = workbook.add_format()
        cell_format_temp.set_align('vcenter')
        set_cell_styles(cell_format_temp)

        if pdf_obj.get_type() == 'ROAD':
            update_page(workbook, pdf_obj, categories['road']['worksheet'], categories['road']['col'],
                        cell_format_temp, cell_format_main, cell_format_content, categories['road']['weeks_done'], content['bg_colors'], content['colors'], licenses, 'road')
            categories['road']['col'] = categories['road']['col'] + 1
        elif pdf_obj.get_type() == 'OVAL':
            update_page(workbook, pdf_obj, categories['oval']['worksheet'], categories['oval']['col'],
                        cell_format_temp, cell_format_main, cell_format_content, categories['oval']['weeks_done'], content['bg_colors'], content['colors'], licenses, 'oval')
            categories['oval']['col'] = categories['oval']['col'] + 1
        elif pdf_obj.get_type() == 'DIRT ROAD':
            update_page(workbook, pdf_obj, categories['dirt_road']['worksheet'], categories['dirt_road']['col'],
                        cell_format_temp, cell_format_main, cell_format_content, categories['dirt_road']['weeks_done'], content['bg_colors'], content['colors'], licenses, 'dirt_road')
            categories['dirt_road']['col'] = categories['dirt_road']['col'] + 1
        elif pdf_obj.get_type() == 'DIRT OVAL':
            update_page(workbook, pdf_obj, categories['dirt_oval']['worksheet'], categories['dirt_oval']['col'],
                        cell_format_temp, cell_format_main, cell_format_content, categories['dirt_oval']['weeks_done'], content['bg_colors'], content['colors'], licenses, 'dirt_oval')
            categories['dirt_oval']['col'] = categories['dirt_oval']['col'] + 1

        tracks = pdf_obj.get_tracks()
        for track in tracks:
            tracks_list.append(track)

    # Set automatic colum width
    for category in categories:
        worksheet = categories[category]['worksheet']
        worksheet.set_column(1, 1, 12)
        worksheet.set_column(2, 2, 4)
        worksheet.set_column(3, 3, 25)
        for col in range(4, categories[category]['col']):
            col_size = col_sizes[category][col] * 1.55
            worksheet.set_column(col, col, col_size)

    # ---------- LEGEND ----------
    print_buttons(workbook, categories)
    print_owned_missing(workbook, categories)
    print_classes(workbook, categories)

    # ---------- CONTENT PAGE ----------
    worksheet_content = workbook.add_worksheet('CONTENT')
    worksheet_content.set_column(2, 2, 45)
    worksheet_content.write(1, 1, 'OWNED')
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
    # set_cell_styles(cell_blank, bg_color=content['bg_colors']['twitter'])
    worksheet_content.write(1, 1, 'OWNED', cell_title)
    worksheet_content.write(1, 2, 'TRACKS', cell_title)
    worksheet_content.write(1, 3, 'USED', cell_title)

    row = 2
    count = 0
    tracks_usage = {}

    for track in tracks_list:
        # track_clean_name = clean_track_name(track)
        track_clean_name = track
        tracks_list[count] = track_clean_name
        if track_clean_name in tracks_usage:
            tracks_usage[track_clean_name] = tracks_usage[track_clean_name] + 1
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

    workbook.close()


def update_page(workbook, pdf_obj, worksheet, col, cell_format, cell_format_main, cell_format_content, weeks_done, bg_colors, colors, licenses, category):
    free_content = get_free_content()

    # set bg color and font color for that cell
    cell_format_colorised = cell_format
    license_colors = get_license_colors(
        bg_colors, colors, pdf_obj.get_ir_license(), licenses)
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


def get_license_colors(bg_colors, colors, sel_ir_license, ir_licenses):
    # creting an array because I have no way to go to the previous item in a dictionary
    all_colors = [[], []]
    for bg_color in ir_licenses['bg_colors']:
        all_colors[0].append(ir_licenses['bg_colors'][bg_color])
    for color in ir_licenses['colors']:
        all_colors[1].append(ir_licenses['colors'][color])

    sel_license_name = sel_ir_license[0]
    sel_license_num = sel_ir_license[1]
    count = 0
    for name in ir_licenses['names']:
        if ir_licenses['names'][name] == sel_license_name:
            if sel_license_num == float(4.0):
                if count > 0:
                    pos = count-1
                else:
                    count = 0
            else:
                pos = count
            bg_color = all_colors[0][pos]
            color = all_colors[1][pos]
            return [bg_color, color]
        count = count + 1
    return ['gray', 'white']


main()

# FIXME: iRLMS series and endurance not getting correct schedule
# TODO: Extra tab with "what can I race", based on the content
# TODO: A way to filter the owned content
# TODO: Set automatic width for columns
# TODO: Check if tracks count is working properly
# TODO: link track names in the pages with the CONTENT page
# TODO: Link cars in the pages with the CONTENT page (therefore sepparate them in individual cells)
# TODO: Leave the year on the track names
# TODO: Lock cells
# TODO: List cars in CONTENT pages, like done with tracks
# TODO: Take into account the 4.0 in license requirements, bc some should be rookie, not D class (like Rookie 1.0 license)
# TODO: Ability to hide series (with VBA)
