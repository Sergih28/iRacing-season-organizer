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
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('B2', 'TYPE')
    worksheet.write('C2', 'NAME')
    worksheet.write('D2', 'CARS')

    pdf_info = extract_pdf_info()
    pdf_obj = Class_schedule(data_type='from_data', data=pdf_info[0])
    row = 2
    header_done = False
    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)

        if not header_done:
            column = 3
            # write week num headers
            dates = pdf_obj.get_dates()
            if len(dates) == 12:
                for week in range(1, 13):
                    column = column + 1

                    # get the first 12 week race Series
                    worksheet.write(1, column, 'Week ' +
                                    str(week) + ' (' + str(dates[week-1]) + ')')
                header_done = True

        worksheet.write(row, 1, pdf_obj.get_type())
        worksheet.write(row, 2, pdf_obj.get_name())
        worksheet.write(row, 3, '\n'.join(pdf_obj.get_cars()))

        tracks = pdf_obj.get_tracks()
        races_type = pdf_obj.get_races_type()
        races_length = pdf_obj.get_races_length()
        column = 3
        for track in tracks:
            column = column + 1
            track_short = track.split('-')[0].strip()
            # special check for rallycross weird lap length
            if not ':' in races_length[column-4]:
                content = track_short + \
                    ' (' + races_length[column-4] + ' ' + races_type + ')'
            else:
                content = track_short + ' (' + races_length[column-4] + ')'
            worksheet.write(row, column, content)

        row = row+1

    # track text size for each column
    # then set the column size according to that
    worksheet.set_column(2, 3, 17)
    worksheet.set_column(4, 17, 25)

    workbook.close()


main()
