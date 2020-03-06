from cell import set_cell_styles


def button(workbook, worksheets, type='DONATION', row=1, col=1):
    cell_button = workbook.add_format()
    if type == 'TWITTER':
        button_text = 'TWITTER'
        button_url = 'https://twitter.com/sergiheras'
        bg_color = '#1DA1F2'
        color = '#FFFFFF'
    elif type == 'GITHUB':
        button_text = 'GITHUB'
        button_url = 'https://github.com/Sergih28/iRacing-season-organiser'
        bg_color = '#333000'
        color = '#FAFAFA'
    else:
        button_text = 'DONATE'
        button_url = 'https://www.button.me/sergih'
        bg_color = '#003087'
        color = '#009CDE'

    set_cell_styles(cell_button, bg_color=bg_color,
                    color=color, align='center')
    for worksheet in worksheets:
        worksheet.write_url(
            row, col, button_url, cell_format=cell_button, string=button_text)
