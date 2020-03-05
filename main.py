import sys
from pdf import extract_pdf_info
from class_schedule import Class_schedule
import xlsxwriter


def main():
    # print('Name: ' + str(pdf_obj.get_name()))
    # print('Type: ' + str(pdf_obj.get_type()))
    # print('Cars: ' + str(pdf_obj.get_cars()))
    # print('Ir License: ' + str(pdf_obj.get_ir_license()))
    # print('Schedule: ' + str(pdf_obj.get_schedule()))

    bg_colors = ['#000000', '#0153DB', '#00C702',
                 '#FEEC04', '#FC8A27', '#FC0706']

    workbook = xlsxwriter.Workbook('output.xlsx')
    cell_format_main = workbook.add_format()
    cell_format_main.set_align('vcenter')
    worksheet_main = workbook.add_worksheet('OLD')
    worksheet_main.write('B2', 'TYPE', cell_format_main)
    worksheet_main.write('C2', 'NAME', cell_format_main)
    worksheet_main.write('D2', 'CARS', cell_format_main)

    pdf_info = extract_pdf_info()
    row = 2
    header_done = False
    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        cell_format_temp = workbook.add_format()
        cell_format_temp.set_align('vcenter')

        if not header_done:
            column = 3
            # write week num headers
            dates = pdf_obj.get_dates()
            if len(dates) == 12:
                for week in range(1, 13):
                    column = column + 1

                    # get the first 12 week race Series
                    worksheet_main.write(1, column, 'Week ' +
                                         str(week) + ' (' + str(dates[week-1]) + ')'), cell_format_main
                header_done = True
        cell_format_temp.set_bg_color(bg_colors[3])
        worksheet_main.write(row, 1, pdf_obj.get_type(), cell_format_main)
        worksheet_main.write(row, 2, pdf_obj.get_name(), cell_format_temp)
        worksheet_main.write(row, 3, '\n'.join(
            pdf_obj.get_cars()), cell_format_main)

        tracks = pdf_obj.get_tracks()
        races_type = pdf_obj.get_races_type()
        races_length = pdf_obj.get_races_length()
        column = 3
        for track in tracks:
            column = column + 1

            # remove piece of track text after last '-'
            track_short = [t.strip() for t in track.split('-')]
            if len(track_short) > 1:
                track_short = ' '.join(track_short[:-1])
            else:
                track_short = track_short[0]

            # special check for rallycross weird lap length
            if not ':' in races_length[column-4]:
                content = track_short + \
                    ' (' + races_length[column-4] + ' ' + races_type + ')'
            else:
                content = track_short + ' (' + races_length[column-4] + ')'
            worksheet_main.write(row, column, content, cell_format_main)

        row = row+1

    worksheet_R = workbook.add_worksheet('ROAD')
    worksheet_O = workbook.add_worksheet('OVAL')
    worksheet_DR = workbook.add_worksheet('DIRT ROAD')
    worksheet_DO = workbook.add_worksheet('DIRT OVAL')
    col_R = 2
    col_O = 2
    col_DR = 2
    col_DO = 2
    weeks_done_R = False
    weeks_done_O = False
    weeks_done_DR = False
    weeks_done_DO = False
    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)
        cell_format_temp = workbook.add_format()
        cell_format_temp.set_align('vcenter')

        if pdf_obj.get_type() == 'ROAD':
            update_page(pdf_obj, worksheet_R, col_R,
                        cell_format_temp, cell_format_main, weeks_done_R)
            col_R = col_R + 1
        elif pdf_obj.get_type() == 'OVAL':
            update_page(pdf_obj, worksheet_O, col_O,
                        cell_format_temp, cell_format_main, weeks_done_O)
            col_O = col_O + 1
        elif pdf_obj.get_type() == 'DIRT ROAD':
            update_page(pdf_obj, worksheet_DR, col_DR,
                        cell_format_temp, cell_format_main, weeks_done_DR)
            col_DR = col_DR + 1
        elif pdf_obj.get_type() == 'DIRT OVAL':
            update_page(pdf_obj, worksheet_DO, col_DO,
                        cell_format_temp, cell_format_main, weeks_done_DO)
            col_DO = col_DO + 1

    # TODO: track text size for each column
    # then set the column size according to that
    worksheet_R.set_column(1, col_R, 25)
    worksheet_O.set_column(1, col_O, 25)
    worksheet_DR.set_column(1, col_DR, 25)
    worksheet_DO.set_column(1, col_DO, 25)
    worksheet_main.set_column(2, 3, 17)
    worksheet_main.set_column(4, 17, 25)

    workbook.close()


def update_page(pdf_obj, worksheet, col, cell_format, cell_format_main, weeks_done):
    worksheet.write(2, col, pdf_obj.get_name(), cell_format)
    worksheet.write(3, col, '\n'.join(
        pdf_obj.get_cars()), cell_format_main)

    # set week column
    if not weeks_done:
        row = 3
        # write week num headers
        dates = pdf_obj.get_dates()
        if len(dates) == 12:
            for week in range(1, 13):
                row = row + 1

                # get the first 12 week race Series
                worksheet.write(row, 1, 'Week ' +
                                str(week) + ' (' + str(dates[week-1]) + ')'), cell_format_main
            weeks_done = True

    tracks = pdf_obj.get_tracks()
    races_type = pdf_obj.get_races_type()
    races_length = pdf_obj.get_races_length()
    row = 3
    for track in tracks:
        row = row + 1

        # remove piece of track text after last '-'
        track_short = [t.strip() for t in track.split('-')]
        if len(track_short) > 1:
            track_short = ' '.join(track_short[:-1])
        else:
            track_short = track_short[0]

        # special check for rallycross weird lap length
        if not ':' in races_length[row-4]:
            content = track_short + \
                ' (' + races_length[row-4] + ' ' + races_type + ')'
        else:
            content = track_short + ' (' + races_length[row-4] + ')'
        worksheet.write(row, col, content, cell_format_main)


main()

# TODO: color the name and its background according to the license
# TODO: fix iRLMS series and endurance not getting correct schedule
# TODO: Do not split by '-' on the name, Mazda and next name are cut
