import os
import re
import time
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd


class fetch_booking_dot_com(object):
    def __init__(self):    
        self.output_dir = 'output'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
        }
        self.session = requests.Session()
        self.today = datetime.datetime.today()
        self.tomorrow = self.today + datetime.timedelta(1)
        self.home_url = 'https://www.booking.com/'
        self.offset_value = 0
        self.max_offset = 10

    def create_dir(self, dirname):
        """Method to create directory"""
        if not os.path.isdir(dirname):
            print('Creating data directory locally: %s' % dirname)
            os.makedirs(dirname)
            print('Successfully created data directory: %s' % dirname)

    def create_url(self, country, lang_code, offset_value, label, sid):
        url = "https://www.booking.com/searchresults.{lang_code}.html?"\
            "label={label}&sid={sid}&sb=1&src=searchresults&src_elem=sb&"\
            "&ss={country}&dest_type=country&checkin_year={in_year}"\
            "&checkin_month={in_month}&checkin_monthday={in_day}"\
            "&checkout_year={out_year}&checkout_month={out_month}"\
            "&checkout_monthday={out_day}&group_adults={people}"\
            "&group_children=0&no_rooms=1&from_sf=1"\
            "&ac_click_type=b&offset={offset}"\
            .format(
                lang_code=lang_code,
                label=label,
                sid=sid,
                country=country.replace(' ', '+'),
                in_year=str(self.today.year),
                in_month=str(self.today.month),
                in_day=str(self.today.day),
                out_year=str(self.tomorrow.year),
                out_month=str(self.tomorrow.month),
                out_day=str(self.tomorrow.day),
                people=2,
                offset=offset_value
            )
        return url

    def fetch_page(self, url, fname):
        """ Fetch booking.com pages."""
        page = None
        if os.path.isfile(fname):
            print("Reading booking.com page: %s" % fname)
            with open(fname, 'r', encoding='utf-8') as fh:
                page = fh.read()
        else:
            print("Fetching booking.com page: %s" % url)
            res = self.session.get(url, headers=self.headers)
            if res.status_code == 200:
                page = res.text
                with open(fname, 'w', encoding='utf-8') as fh:
                    fh.write(page)
            else:
                print(
                    "Requests module failed."
                    "To fetch booking.com page: %s" % (url)
                )
            time.sleep(5)
        soup = BeautifulSoup(page, 'html.parser')
        soup.prettify()
        return soup

    def fetch_hotel_page(self, soup, country, offset_value):
        """ Fetch hotel details url."""
        hotel_links = soup.find_all('a', {'class': 'hotel_name_link url'})
        if len(hotel_links) == 0:
            hotel_links = soup.find_all(
                'a',
                {'class': 'js-sr-hotel-link hotel_name_link url'}
            )
        for page_no, link in enumerate(hotel_links):
            html_file = os.path.join(
                os.getcwd(),
                self.output_dir,
                country,
                '%s_page_%s_hotel_%s.html' % (
                    country, offset_value, page_no
                )
            )
            print('>> Looking for %s page %s hotel %s' % (
                country, offset_value, page_no+1)
            )
            hotel_url = "%s%s" % (
                "https://www.booking.com",
                link.get('href').strip()
            )
            soup = self.fetch_page(hotel_url, html_file)
            self.parse_data(soup, country)

    def parse_data(self, soup, country):
        """Parse data."""
        if soup is not None:
            details = {}
            hotel_name = soup.find('h2', {'id': 'hp_hotel_name'}).text.strip()
            name = hotel_name.split('\n')
            if len(name) > 1:
                name = name[1]
            else:
                name = hotel_name
            name = name.replace(',', '')
            get_latlng = soup.find('a', {'id': 'hotel_sidebar_static_map'})
            if get_latlng is None:
                get_latlng = soup.find('a', {'id': 'hotel_address'})
            latlng = get_latlng.get('data-atlas-latlng')
            # find address
            address = re.search(
                r'\"addressLocality\"\s*:\s*\"(.*?)\"',
                str(soup)
            ).group(1)
            address = address.replace(',', '')
            # find city
            city = re.search(
                r"city_name\s*:\s*'(.*?)'",
                str(soup)
            ).group(1)
            city = city.replace(',', '')
            # find postal code
            postal = re.search(
                r'\"postalCode\"\s*:\s*\"(.*?)\"',
                str(soup)
            ).group(1)
            postal = postal.replace(' ', '')
            # find country
            country_name = re.search(
                r'\"addressCountry\"\s*:\s*\"(.*?)\"',
                str(soup)
            ).group(1)
            # store data
            (lat, lng) = latlng.split(',')
            details['lat'] = lat
            details['long'] = lng
            details['name'] = name
            details['street'] = address
            details['city'] = city
            details['postal_code'] = postal
            details['country'] = country_name
            self.data.append(details)

    def start_process(self):
        """Method to fetch the hotels from booking.com."""
        self.create_dir(os.path.join(self.output_dir))
        (homepage, countries) = (None, {})
        print('Fetching booking.com homepage...')
        res = self.session.get(self.home_url, headers=self.headers)
        if res.status_code == 200:
            homepage = res.text
        soup = BeautifulSoup(homepage, 'html.parser')
        soup.prettify()
        # - Collect ISO country code.
        get_country_code = soup.find_all('link', {'rel': 'alternate'})
        # - Collect label land sid
        link_help = soup.find('link', {'rel': 'help'})
        help_link = link_help.get('href')
        label = re.search('label=(.*?);', help_link).group(1)
        sid = re.search('sid=(.*?);', help_link).group(1)
        for link in get_country_code:
            language = link.get('hreflang')
            if language:
                if language == 'th':
                    countries['Thailand'] = [language, link.get('title')]
                elif language == 'ar':
                    countries['UAE'] = [language, link.get('title')]
                elif language == 'sv':
                    countries['Sweden'] = [language, link.get('title')]
                elif language == 'en-gb':
                    countries['United Kingdom'] = [language, link.get('title')]
                    countries['India'] = [language, link.get('title')]
                    
        for country in countries.keys():
            self.data = []
            csv_file = os.path.join(
                os.getcwd(),
                '%s_poi.csv' % country.replace(' ', '_')
            )
            if os.path.isfile(csv_file):
                continue
            print('Started searching hotel for country: %s' % country)
            offset_value = 0  # first page offset.
            lang_code = countries.get(country)[0]
            self.create_dir(os.path.join(self.output_dir, country))
            html_file = os.path.join(
                os.getcwd(),
                self.output_dir,
                country,
                '%s_page_%s.html' % (country, offset_value)
            )
            url = self.create_url(country, lang_code, offset_value, label, sid)
            res = self.fetch_page(url, html_file)
            soup = self.fetch_hotel_page(
                res, country, offset_value
            )
            self.parse_data(soup, country)
            if res.find_all(
                'li', {'class': 'sr_pagination_item'}
            ) is not None:
                offset_max = res.find_all(
                    'li', {'class': 'sr_pagination_item'}
                )[-1].get_text().splitlines()[-1]
                if int(offset_max) > self.max_offset:
                    self.max_offset = self.max_offset
                else:
                    self.max_offset = int(offset_max)
                for i in range(self.max_offset):
                    offset_value += 25  # next page offset
                    html_file = os.path.join(
                        os.getcwd(),
                        self.output_dir,
                        country,
                        '%s_page_%s.html' % (country, offset_value)
                    )
                    next_page_url = self.create_url(
                        country, lang_code, offset_value, label, sid
                    )
                    res = self.fetch_page(next_page_url, html_file)
                    soup = self.fetch_hotel_page(
                        res, country, offset_value
                    )
                print('Searching of hotel for country: %s completed.' % (
                    country)
                )
                df = pd.DataFrame(self.data)
                df.to_csv("%s_poi.csv" % (
                    country.replace(' ', '_')),
                    index=False
                )


# - main method
if __name__ == '__main__':
    booking = fetch_booking_dot_com()
    booking.start_process()
