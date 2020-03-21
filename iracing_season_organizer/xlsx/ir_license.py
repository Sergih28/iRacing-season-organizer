from ..dics import ir_licenses


def get_license_colors(sel_ir_license):
    # creting an array because I have no way to go to the previous item in a dictionary
    all_colors = [[], []]
    for bg_color in ir_licenses['bg_colors']:
        all_colors[0].append(ir_licenses['bg_colors'][bg_color])
    for color in ir_licenses['colors']:
        all_colors[1].append(ir_licenses['colors'][color])

    sel_license_name = sel_ir_license[0]
    sel_license_num = sel_ir_license[1]
    count = 0
    for name in ir_licenses['names']:
        if ir_licenses['names'][name] == sel_license_name:
            if sel_license_num == float(4.0):
                if count > 0:
                    pos = count-1
                else:
                    count = 0
            else:
                pos = count
            bg_color = all_colors[0][pos]
            color = all_colors[1][pos]
            return [bg_color, color]
        count = count + 1
    return ['gray', 'white']
