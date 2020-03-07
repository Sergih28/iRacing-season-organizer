from cell import set_cell_styles
from dics import *


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
        button_url = 'https://www.button.me/sergih'
        bg_color = content['bg_colors']['paypal']
        color = content['colors']['paypal']

    set_cell_styles(cell_button, bg_color=bg_color,
                    color=color)
    worksheet.write_url(
        row, col, button_url, cell_format=cell_button, string=button_text)


def print_buttons(workbook, categories):
    for category in categories:
        worksheet = categories[category]['worksheet']
        button(workbook, worksheet, row=4)
        button(workbook, worksheet, type='TWITTER', row=5)
        button(workbook, worksheet, type='GITHUB', row=6)


def owned_missing(workbook, worksheet):
    cell = workbook.add_format()
    cell2 = workbook.add_format()
    set_cell_styles(
        cell, color=content['colors']['normal'], bg_color=content['bg_colors']['owned'], bold=True)
    set_cell_styles(
        cell2, color=content['colors']['alt'], bg_color=content['bg_colors']['missing'], bold=True)
    worksheet.write(8, 1, 'Owned', cell)
    worksheet.write(9, 1, 'Missing', cell2)


def print_owned_missing(workbook, categories):
    for category in categories:
        worksheet = categories[category]['worksheet']
        owned_missing(workbook, worksheet)


def classes(workbook, worksheet):
    count = 0
    for key in licenses['bg_colors']:
        cell = workbook.add_format()
        row = count + 11
        set_cell_styles(
            cell, color=licenses['colors'][key], bg_color=licenses['bg_colors'][key], bold=True)
        worksheet.write(
            row, 1, licenses['names'][list(licenses['names'])[count]], cell)
        count = count + 1


def print_classes(workbook, categories):
    for category in categories:
        worksheet = categories[category]['worksheet']
        classes(workbook, worksheet)
