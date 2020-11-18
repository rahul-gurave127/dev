# - convert booking.com json file into csv file.
from glob import glob
import json
import csv
import os

json_files = glob(os.path.join(os.getcwd(), "*.json"))

headers = [
    "latitude", "longitude", "address", "city", "state", "postal", "country"
]

for jsonfile in json_files:
    fname = os.path.basename(jsonfile).split('.')[0]
    print("process started for country: %s" % fname)
    with open(jsonfile) as json_file:
        data = json.load(json_file)
        data = data.get('result')
        with open('%s.csv' % fname, 'w', encoding='utf-8') as data_file:
            csv_writer = csv.writer(data_file)
            count = 0
            for row in data:
                row = row.get('hotel_data')
                lat = row.get('location').get('latitude')
                lon = row.get('location').get('longitude')
                address = row.get('address')
                city = row.get('city')
                state = None
                postal = row.get('zip')
                country = row.get('country')

                if count == 0:
                    # Writing headers of CSV file
                    csv_writer.writerow(headers)
                    count += 1
                # Writing data of CSV file
                csv_writer.writerow(
                    [lat, lon, address, city, state, postal, country]
                )
