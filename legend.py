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
                    color=color)
    for worksheet in worksheets:
        worksheet.write_url(
            row, col, button_url, cell_format=cell_button, string=button_text)


def owned_or_not_legend(workbook, worksheets, content_colors, content_bg_colors):
    for worksheet in worksheets:
        cell = workbook.add_format()
        cell2 = workbook.add_format()
        set_cell_styles(
            cell, color=content_colors['normal'], bg_color=content_bg_colors['owned'], bold=True)
        set_cell_styles(
            cell2, color=content_colors['alt'], bg_color=content_bg_colors['missing'], bold=True)
        worksheet.write(8, 1, 'Owned', cell)
        worksheet.write(9, 1, 'Missing', cell2)


def colors_legend(workbook, worksheets, bg_colors, colors, license_names):
    for worksheet in worksheets:
        count = 0
        for key in bg_colors:
            cell = workbook.add_format()
            row = count + 11
            set_cell_styles(
                cell, color=colors[key], bg_color=bg_colors[key], bold=True)
            worksheet.write(
                row, 1, license_names[list(license_names)[count]], cell)
            count = count + 1
