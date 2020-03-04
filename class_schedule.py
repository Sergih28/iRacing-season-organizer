import re


class Class_schedule:
    def __init__(self, type, title, page_content):
        self.title = title
        self.type = type
        self.clear_page_content(page_content)
        self.set_name()
        self.set_cars()
        self.set_ir_license()
        self.set_schedule()

    def __str__(self):
        r = 'Name: ' + self.name + '\n'
        r += 'Type: ' + self.type + '\n'
        r += 'Cars: ' + str(self.cars) + '\n'
        r += 'Ir_license: ' + self.ir_license + '\n'
        r += 'Schedule: ' + str(self.schedule)
        return r

    def clear_page_content(self, page_content):
        left_part = page_content[0].split(self.title)[0]
        if not 'Week' in left_part:
            page_content[0] = page_content[0][len(left_part):]
        self.page_content = page_content

    def set_name(self):
        self.name = self.title.split('-')[0].strip()

    def set_cars(self):
        self.cars = []
        cars = self.page_content[0].split(
            self.title)[1].strip()
        self.cars = cars
        if 'Rookie' in cars:
            cars = cars.split('Rookie')[0].strip()
        elif 'Class D' in cars:
            cars = cars.split('Class D')[0].strip()
        elif 'Class C' in cars:
            cars = cars.split('Class C')[0].strip()
        elif 'Class B' in cars:
            cars = cars.split('Class B')[0].strip()
        elif 'Class A' in cars:
            cars = cars.split('Class A')[0].strip()

        self.cars = [car.strip() for car in cars.split(',')]

    def set_ir_license(self):
        ir_lic = self.page_content[0].split(
            self.cars[len(self.cars) - 1])[1].strip()
        self.ir_license = re.split(
            'races', ir_lic, flags=re.IGNORECASE)[0].strip()

    def set_schedule(self):
        weeks = self.page_content[0].split('Week')
        if len(self.page_content) > 1:  # 2 pages
            new_week = self.page_content[1].split('Week')
            for w in new_week:
                if w != '':
                    weeks.append(w)

        week_nums = []
        dates = []
        tracks = []
        races_length = []
        counter = 0
        for week in weeks:
            counter = counter+1
            if counter == 1:
                continue
            split_week_num = week.split(' (')
            split_date = split_week_num[1].strip().split(')')
            split_track = split_date[1].strip().split('(')
            split_race_length = week.split('.')
            split_race_length2 = split_race_length[len(
                split_race_length)-1].strip()

            if not 'laps' in split_race_length2:
                split_race_length2 = split_race_length2.split('mins')
            else:
                split_race_length2 = split_race_length2.split('laps')

            week_num = split_week_num[0].strip()
            date = split_date[0].strip()
            track = split_track[0].strip()
            race_length = split_race_length2[0].strip()
            week_nums.append(week_num)
            dates.append(date)
            tracks.append(track)
            races_length.append(race_length)
            # TODO: be able to differenciate between laps and mins race length

        self.schedule = [week_nums, dates, tracks, races_length]
