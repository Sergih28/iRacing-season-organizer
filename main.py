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
    for series in pdf_info:
        pdf_obj = Class_schedule(data_type='from_data', data=series)

        column = 3
        # write week num headers
        for week in range(1, 14):
            column = column + 1
            worksheet.write(1, column, 'Week ' + str(week))

        worksheet.write(row, 1, pdf_obj.get_type())
        worksheet.write(row, 2, pdf_obj.get_name())
        worksheet.write(row, 3, ','.join(pdf_obj.get_cars()))

        tracks = pdf_obj.get_tracks()
        column = 3
        for track in tracks:
            column = column + 1
            track_short = track.split('-')[0].strip()
            worksheet.write(row, column, track_short)

        row = row+1

    # track text size for each column
    # then set the column size according to that
    worksheet.set_column(2, 3, 17)
    worksheet.set_column(4, 17, 25)

    workbook.close()


main()
