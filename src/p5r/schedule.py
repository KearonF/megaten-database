#!/usr/bin/python3
import yaml
import calendar

with open('walkthrough/confidant-calendar.yaml') as yamlfile:
    availability = yaml.safe_load(yamlfile)
with open('walkthrough/calendar.tsv') as tsvfile:
    next(tsvfile)
    weather = {}
    for line in tsvfile:
        date, dow, daytime, evening = line.split()
        weather[date] = (dow, 'Rain' in daytime, 'Rain' in evening)

arcanas = [x[:3] if x != 'Empress' else 'Ems' for x in availability['columns']]
night_cut = availability['nightCutoff']

def arcana_col(arcana, is_free):
    return f"{arcana}?" if is_free == 'X' else (arcana if is_free == 'O' else '')
def table_row(row):
    return f"| {' | '.join(row)} |"

rows = []
for date_num, available in availability['calendar'].items():
    date_str = f"{int(str(date_num)[2:4])}/{str(date_num)[4:]}"
    dow, day_rain, eve_rain = weather[date_str]
    rows.append([date_str, 'Rain' if day_rain else ''] + [arcana_col(arcanas[i], x) for i, x in enumerate(available[:night_cut])])
    rows.append([dow, 'Rain' if eve_rain else ''] + [arcana_col(arcanas[i + night_cut], x) for i, x in enumerate(available[night_cut:])] + [''])

underline = table_row(['---'] * (night_cut + 2))
print(table_row([calendar.month_abbr[4]] + [''] * (night_cut + 1)))
print(underline)

for row in rows:
    date = row[0]
    if date.endswith('/01'):
        print()
        print(table_row([calendar.month_abbr[int(date.split('/')[0])]] + [''] * (night_cut + 1)))
        print(underline)
    print(table_row(row))
