from cell import set_cell_styles
from dics import content, ir_licenses


def button(workbook, worksheet, type='DONATION', row=1, col=1):
    cell_button = workbook.add_format()
    if type == 'TWITTER':
        button_text = 'TWITTER'
        button_url = 'https://twitter.com/sergiheras'
        bg_color = content['bg_colors']['twitter']
        color = content['colors']['twitter']
    elif type == 'GITHUB':
        button_text = 'GITHUB'
        button_url = 'https://github.com/Sergih28/iRacing-season-organiser'
        bg_color = content['bg_colors']['github']
        color = content['colors']['github']
    else:
        button_text = 'DONATE'
        button_url = 'https://www.paypal.me/sergih'
        bg_color = content['bg_colors']['paypal']
        color = content['colors']['paypal']

    set_cell_styles(cell_button, bg_color=bg_color, color=color)
    worksheet.write_url(
        row, col, button_url, cell_format=cell_button, string=button_text)


def print_buttons(workbook, categories, first_row, col):
    for category in categories:
        worksheet = categories[category]['worksheet']
        button(workbook, worksheet, row=first_row, col=col)
        button(workbook, worksheet, type='TWITTER', row=first_row+1, col=col)
        button(workbook, worksheet, type='GITHUB', row=first_row+2, col=col)


def owned_missing(workbook, worksheet, first_row, col=1):
    cell = workbook.add_format()
    cell2 = workbook.add_format()
    set_cell_styles(
        cell, color=content['colors']['normal'], bg_color=content['bg_colors']['owned'], bold=True)
    set_cell_styles(
        cell2, color=content['colors']['alt'], bg_color=content['bg_colors']['missing'], bold=True)
    worksheet.write(first_row, col, 'Owned', cell)
    worksheet.write(first_row+1, col, 'Missing', cell2)


def print_owned_missing(workbook, categories, first_row, col):
    for category in categories:
        worksheet = categories[category]['worksheet']
        owned_missing(workbook, worksheet, first_row, col)


def classes(workbook, worksheet, first_row, col=1):
    count = 0
    for key in ir_licenses['bg_colors']:
        cell = workbook.add_format()
        color = ir_licenses['colors'][key]
        bg_color = ir_licenses['bg_colors'][key]
        row = first_row + count
        class_name = ir_licenses['names'][list(ir_licenses['names'])[count]]

        set_cell_styles(cell, color=color, bg_color=bg_color, bold=True)
        worksheet.write(
            row, col, class_name, cell)
        count += 1


def print_classes(workbook, categories, first_row, col):
    for category in categories:
        worksheet = categories[category]['worksheet']
        classes(workbook, worksheet, first_row, col)
