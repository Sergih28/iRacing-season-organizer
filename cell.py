import xlsxwriter


def set_cell_styles(cell, border_color='#575757', align=False, color=False, bg_color=False, bold=False):
    cell.set_border(1)
    cell.set_border_color(border_color)
    cell.set_font_name('Courier')
    cell.set_font_size(10)
    if align:
        cell.set_align(align)
    if color:
        cell.set_font_color(color)
    if bg_color:
        cell.set_bg_color(bg_color)
    if bold:
        cell.set_bold()
