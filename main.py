import sys
from pdf import extract_pdf_info
from class_schedule import Class_schedule
from free_content import get_free_content
from cell import set_cell_styles
from legend import *
import xlsxwriter
from dics import *


def main():
    workbook = xlsxwriter.Workbook('output.xlsx')
    cell_format_main = workbook.add_format()
    cell_format_main.set_align('vcenter')
    set_cell_styles(cell_format_main)

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

    worksheet_R = workbook.add_worksheet('ROAD')
    worksheet_O = workbook.add_worksheet('OVAL')
    worksheet_DR = workbook.add_worksheet('DIRT ROAD')
    worksheet_DO = workbook.add_worksheet('DIRT OVAL')
    col_R = 4
    col_O = 4
    col_DR = 4
    col_DO = 4
    weeks_done_R = False
    weeks_done_O = False
    weeks_done_DR = False
    weeks_done_DO = False
    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        cell_format_temp = workbook.add_format()
        cell_format_temp.set_align('vcenter')
        set_cell_styles(cell_format_temp)

        if pdf_obj.get_type() == 'ROAD':
            update_page(workbook, pdf_obj, worksheet_R, col_R,
                        cell_format_temp, cell_format_main, cell_format_content, weeks_done_R, content['bg_colors'], content['colors'], licenses)
            col_R = col_R + 1
        elif pdf_obj.get_type() == 'OVAL':
            update_page(workbook, pdf_obj, worksheet_O, col_O,
                        cell_format_temp, cell_format_main, cell_format_content, weeks_done_O, content['bg_colors'], content['colors'], licenses)
            col_O = col_O + 1
        elif pdf_obj.get_type() == 'DIRT ROAD':
            update_page(workbook, pdf_obj, worksheet_DR, col_DR,
                        cell_format_temp, cell_format_main, cell_format_content, weeks_done_DR, content['bg_colors'], content['colors'], licenses)
            col_DR = col_DR + 1
        elif pdf_obj.get_type() == 'DIRT OVAL':
            update_page(workbook, pdf_obj, worksheet_DO, col_DO,
                        cell_format_temp, cell_format_main, cell_format_content, weeks_done_DO, content['bg_colors'], content['colors'], licenses)
            col_DO = col_DO + 1

        tracks = pdf_obj.get_tracks()
        for track in tracks:
            if not track in tracks_list:
                tracks_list.append(track)

    # TODO: track text size for each column
    # then set the column size according to that
    worksheet_R.set_column(3, col_R, 25)
    worksheet_O.set_column(3, col_O, 25)
    worksheet_DR.set_column(3, col_DR, 25)
    worksheet_DO.set_column(3, col_DO, 25)
    worksheets = [worksheet_R, worksheet_O, worksheet_DR, worksheet_DO]

    for worksheet in worksheets:
        worksheet.set_column(1, 1, 12)
        worksheet.set_column(2, 2, 4)

    # ---------- LEGEND ----------
    # link buttons
    button(workbook, worksheets, row=4)
    button(workbook, worksheets, type='TWITTER', row=5)
    button(workbook, worksheets, type='GITHUB', row=6)

    owned_or_not_legend(workbook, worksheets)
    colors_legend(workbook, worksheets)

    # add tracks list in a new page
    worksheet_content = workbook.add_worksheet('CONTENT')
    worksheet_content.set_column(2, 2, 45)
    worksheet_content.write(1, 1, 'OWNED')
    tracks_list = sorted(tracks_list)
    free_tracks = get_free_content()[0]
    cell_green = workbook.add_format()
    cell_gray = workbook.add_format()
    cell_title1 = workbook.add_format()
    cell_title2 = workbook.add_format()
    set_cell_styles(cell_title1, bold=True)
    set_cell_styles(cell_title2, bold=True)
    set_cell_styles(
        cell_green, bg_color=content['bg_colors']['owned'])
    set_cell_styles(
        cell_gray, bg_color=content['bg_colors']['missing'])
    worksheet_content.write(1, 1, 'OWNED', cell_title1)
    worksheet_content.write(1, 2, 'TRACKS', cell_title1)

    row = 2
    count = 0

    for track in tracks_list:
        tracks_list[count] = clean_track_name(track)
        count = count + 1
    # remove duplicate tracks
    tracks_list = list(dict.fromkeys(tracks_list))
    total_tracks = len(tracks_list) + 2
    for track in tracks_list:
        cell_track = workbook.add_format()
        if track in free_tracks:
            worksheet_content.write(row, 1, 'Y')
        else:
            worksheet_content.write(row, 1, 'N')

        # condition to paint the bg_color depending on the row OWNED
        criteria_Y = '=$B'+str(row+1)+'="Y"'
        criteria_N = '=$B'+str(row+1)+'="N"'
        worksheet_content.conditional_format(2, 1, total_tracks, 2, {'type': 'formula',
                                                                     'criteria': criteria_Y, 'format': cell_green})
        worksheet_content.conditional_format(2, 1, total_tracks, 2, {'type': 'formula',
                                                                     'criteria': criteria_N, 'format': cell_gray})

        worksheet_content.write(row, 2, track, cell_track)
        row = row + 1

    # set conditional color in owned and track columns

    # worksheet_content.conditional_format(2, 1, total_rows, 1, {'type': 'cell',
    #                                                            'criteria': '==', 'value': '"Y"', 'format': cell_green})
    # worksheet_content.conditional_format(2, 1, total_rows, 1, {'type': 'cell',
    #                                                            'criteria': '==', 'value': '"N"', 'format': cell_gray})

    workbook.close()


def update_page(workbook, pdf_obj, worksheet, col, cell_format, cell_format_main, cell_format_content, weeks_done, bg_colors, colors, licenses):
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
        track_short = clean_track_name(track)

        if 'Oval' in track_short:
            track_short = track_short.replace('Oval', '').strip()
        if 'Roval' in track_short:
            track_short = track_short.replace('Roval', '').strip()
        if 'Legends' in track_short:
            track_short = track_short.replace('Legends', '').strip()

        # colorise background depending if it is owned content or not
        if track_short in free_content[0]:
            cell_format_track = cell_format_content[0]
        else:
            cell_format_track = cell_format_content[1]

        # special check for rallycross weird lap length
        if not ':' in races_length[row-4]:
            content = track_short + \
                ' (' + races_length[row-4] + ' ' + races_type + ')'
        else:
            content = track_short + ' (' + races_length[row-4] + ')'
        set_cell_styles(cell_format_track)
        worksheet.write(row, col, content, cell_format_track)


def get_license_colors(bg_colors, colors, sel_ir_license, ir_licenses):

    # creting an array because I have no way to go to the previous item in a dictionary
    all_colors = [[], []]
    for bg_color in ir_licenses['bg_colors']:
        all_colors[0].append(ir_licenses['bg_colors'][bg_color])
    for color in ir_licenses['colors']:
        all_colors[1].append(ir_licenses['colors'][color])

    count = 0
    for name in ir_licenses['names']:
        if ir_licenses['names'][name] == sel_ir_license:
            if count > 0:
                pos = count-1
            else:
                count = 0
            bg_color = all_colors[0][pos]
            color = all_colors[1][pos]
            return [bg_color, color]
        count = count + 1
    return ['gray', 'white']

 # clear track name removing ' - '


def clean_track_name(track):
    return [t.strip() for t in track.split(' -')][0]


main()

# FIXME: iRLMS series and endurance not getting correct schedule
# TODO: extra tab with "what can I race", based on the content
# TODO: A way to filter the owned content
# TODO: Set automatic width for columns
# TODO: Print all tracks in another page
