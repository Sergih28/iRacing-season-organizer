from cell import set_cell_styles


def donation_button(workbook, worksheets):
    cell_paypal = workbook.add_format()
    paypal_text = 'DONATE'
    paypal_url = 'https://www.paypal.me/sergih'
    set_cell_styles(cell_paypal, bg_color='#003087',
                    color='#009CDE', align='center')
    for worksheet in worksheets:
        worksheet.write_url(
            1, 1, paypal_url, cell_format=cell_paypal, string=paypal_text)
