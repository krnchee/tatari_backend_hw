import csv
import time
import datetime

cost_per_view = []
creatives = {}
dates = {}
rotations = {}

# Create rotations object that will hold all available rotations
with open('rotations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # Skip header
        if line_count == 0:
            line_count += 1
        else:
            if row[2] not in rotations:
                rotations[row[2]] = {}

            start_time_str = time.strptime(row[0],'%I:%M %p')
            start_time = int(start_time_str.tm_hour) + (int(start_time_str.tm_min * 0.01))

            end_time_str = time.strptime(row[1],'%I:%M %p')
            end_time = int(end_time_str.tm_hour) + (int(end_time_str.tm_min * 0.01))

            rotations[row[2]]['start'] = start_time
            rotations[row[2]]['end'] = end_time

# Create dates and creatives objects that will hold their respective info
with open('spots.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # Skip header
        if line_count == 0:
            line_count += 1
        else:
            if row[2] not in creatives:
                creatives[row[2]] = {}
                creatives[row[2]]['spend'] = 0
                creatives[row[2]]['views'] = 0
                creatives[row[2]]['cpv_creative'] = 0

            # Update CPV for creative
            creatives[row[2]]['spend'] += float(row[3])
            creatives[row[2]]['views'] += float(row[4])
            creatives[row[2]]['cpv_creative'] = creatives[row[2]]['spend'] / \
                                                 creatives[row[2]]['views']

            if row[0] not in dates:
                dates[row[0]] = {}

            row_time = time.strptime(row[1],'%I:%M %p')
            row_time = int(row_time.tm_hour) + (int(row_time.tm_min)*0.01)

            # Update CPV for rotation
            for rotation, times in rotations.iteritems():
                if row_time > times['start'] and row_time < times['end']:
                    if rotation not in dates[row[0]]:
                        dates[row[0]][rotation] = {}
                        dates[row[0]][rotation]['spend'] = 0
                        dates[row[0]][rotation]['views'] = 0
                        dates[row[0]][rotation]['cpv_rotation'] = 0

                    dates[row[0]][rotation]['spend'] += float(row[3])
                    dates[row[0]][rotation]['views'] += float(row[4])
                    dates[row[0]][rotation]['cpv_rotation'] = dates[row[0]][rotation]['spend']/ \
                                                              dates[row[0]][rotation]['views']

            line_count += 1

print('\n')
print('\n')

for creative, prices in creatives.iteritems():
    for price, value in prices.iteritems():
        if price == 'cpv_creative':
            print("For the Creative {} the Cost per View is {}".format(creative, value))

print('\n')
print('\n')

for date, times in dates.iteritems():
    for rotation, prices in times.iteritems():
        for price, value in prices.iteritems():
            if price == 'cpv_rotation':
                print("For the {} Rotation on the {} the Cost per View is {}".format(rotation, date, value))


# print(creatives)
# print(dates)
