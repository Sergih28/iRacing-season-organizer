import re


class Class_schedule:
    def __init__(self, type=None, title=None, page_content=None, data_type=None, data=None):
        if data_type == 'from_data':
            self.from_data(data)
        else:
            self.title = title
            self.type = type
            self.clear_page_content(page_content)
            self.set_name()
            self.set_cars()
            self.set_ir_license()
            self.set_schedule()

    def from_data(self, data):
        self.name = data[0]
        self.type = data[1]
        self.cars = data[2]
        self.ir_license = data[3]
        self.schedule = data[4]

    def __str__(self):
        r = 'Name: ' + self.name + '\n'
        r += 'Type: ' + self.type + '\n'
        r += 'Cars: ' + str(self.cars) + '\n'
        r += 'Ir_license: ' + self.ir_license + '\n'
        r += 'Schedule: ' + str(self.schedule)
        return r

    def __repr__(self):
        return [self.name, self.type, self.cars, self.ir_license, self.schedule]

    def clear_page_content(self, page_content):
        left_part = page_content[0].split(self.title)[0]
        if not 'Week' in left_part:
            page_content[0] = page_content[0][len(left_part):]
        self.page_content = page_content

    def set_name(self):
        self.name = self.title.split(' -')[0].strip()

    def set_cars(self):
        self.cars = []

        # special checks for PDF EOL with 2 cars
        if '911RSR' in self.page_content[0]:
            self.page_content[0] = self.page_content[0].replace(
                '911RSR', '911 RSR')
        if 'R8LMS' in self.page_content[0]:
            self.page_content[0] = self.page_content[0].replace(
                'R8LMS', 'R8 LMS')

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
            self.title)[1]
        ir_lic = ir_lic.split(self.cars[len(self.cars)-1])
        self.ir_license = re.split(
            'team racing', ir_lic[1], flags=re.IGNORECASE)[0].strip()
        self.ir_license = re.split(
            'every ', self.ir_license, flags=re.IGNORECASE)[0].strip()
        self.ir_license = re.split(
            'races', self.ir_license, flags=re.IGNORECASE)[0].strip()
        self.ir_license = self.ir_license.replace(',', '')

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
        races_type = 'Laps'
        counter = 0
        skip_weeks = True
        for week in weeks:
            counter = counter+1
            if counter == 1:
                continue

            split_week_num = week.split(' (')
            split_date = split_week_num[1].strip().split(')')
            split_track = split_date[1].strip().split('(')
            split_race_length = week.split('.')
            split_race_length2 = split_race_length[len(
                split_race_length)-1].split('%')
            split_race_length3 = split_race_length2[len(
                split_race_length2)-1].strip()

            if not 'laps' in split_race_length3:
                split_race_length3 = split_race_length3.split('mins')
            else:
                split_race_length3 = split_race_length3.split('laps')

            week_num = int(split_week_num[0].strip())

            # skip weeks until we get week 1
            if week_num == 1:
                skip_weeks = False
            if skip_weeks:
                continue

            date = split_date[0].strip()
            track = split_track[0].strip()
            track = self.clean_track_name(track)
            race_length = split_race_length3[0].strip()
            week_nums.append(week_num)
            dates.append(date)
            tracks.append(track)
            races_length.append(race_length)
            if ' mins' in week:
                races_type = 'mins'

        self.schedule = [week_nums, dates, tracks, races_type, races_length]

    # clear track name removing ' - '
    def clean_track_name(self, track):
        track_clean_name = [t.strip() for t in track.split(' -')][0]

        # special check for le mans
        track = track.replace('- 24 Heures', '')

        # special check for tsukuba
        if not 'Tsukuba' in track:
            # append track year
            year = [int(s) for s in track if s.isdigit()]
            if len(year) == 4:
                track_clean_name += ' '
                for digit in year:
                    track_clean_name += str(digit)

        return track_clean_name

    def get_name(self): return self.name
    def get_type(self): return self.type
    def get_cars(self): return self.cars

    def get_ir_license(self):
        if type(self.ir_license) is list:
            return [self.ir_license[0], self.ir_license[1]]

        ir_license = self.ir_license.split('-->')
        ir_license = ir_license[0].strip().split('(')
        license_name = ir_license[0].strip()
        license_num = ir_license[1].split(')')[0].strip()
        return [license_name, float(license_num)]

    def get_schedule(self): return self.schedule
    def get_dates(self): return self.schedule[1]
    def get_tracks(self): return self.schedule[2]
    def get_races_type(self): return self.schedule[3]
    def get_races_length(self): return self.schedule[4]
