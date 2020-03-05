import sys
from pdf import extract_pdf_info
from class_schedule import Class_schedule
import xlsxwriter


def main():
    pdf_info = extract_pdf_info()
    pdf_obj = Class_schedule(data_type='from_data', data=pdf_info[0])
    print('type: ' + str(pdf_obj.get_type()))
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', str(pdf_info[0]))
    workbook.close()


main()
