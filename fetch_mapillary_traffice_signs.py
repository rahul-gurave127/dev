import requests
import json
import re
import os


class Mapillary_API():
    """Mappillary class to download traffic signs from Mapiillary API"""
    def __init__(self):
        self.page_no = 1
        self.client_id = "VmZBcXVUM0lhaE93d0habWdldElEYjpiYzg0MTQwNjFlZWQ1NzMy"
        self.token = (
            'xMkJ8SMaDe6lz3HHaQuWmRvcnAANXn8PneCeJQd9d1qKIyO6t10yg'
            'BnrLdNGA5k4flc0w4yhTGieBihrN9vebqtWxFPazldBaGGir'
            'B1ONYtm0iXP0kaYcTxhKHmpbMCCXqKVUqv6u0ArDYLMigVtVJev64e3oXh7'
        )
        self.header = {
            "Authorization": "Bearer {}".format(self.token)
        }
        # - Create sample json
        self.status = {
            "country": "",
            "details": [],
            "status": "Not Started"
        }
        # - Create sample geojson
        self.mapillary_geojson = {
            "type": "FeatureCollection",
            "features": []
        }

    def create_dir(self, dirname):
        """Method to create directory"""
        if not os.path.isdir(dirname):
            print("Creating '%s' data directory locally." % dirname)
            os.makedirs(dirname)

    def fetch_traffice_sign(self, url, country, last_token, page_no):
        "Method to download traffice sings with restriction."
        print("Fetching URL: %s" % url)
        res = requests.get(url, timeout=None, headers=self.header)
        # - Fetch again if timeout.
        if res.status_code != 200:
            print("Trying Again.. Page No: %s" % self.page_no)
            self.fetch_traffice_sign(url, country, last_token, page_no)

        if res.status_code == 200:
            data = res.json()
            json_file = (os.path.join(
                os.getcwd(), "PAGES", "%s_%s.json" % (country, page_no))
            )
            with open(json_file, 'w', encoding='utf-8') as fh:
                json.dump(data, fh)
            row = {
                'url': url,
                'token': last_token,
                'page_number': page_no
            }
            if row not in self.status['details']:
                self.status['details'].append(row)
            # store mapillary traffice_url, page_token, and page_no
            with open(fname, 'w', encoding='utf-8') as json_fh:
                json.dump(self.status, json_fh)

            print("Page Number: %s => Features: %s" % (
                self.page_no, len(data['features']))
            )

            for feature in data['features']:
                if feature not in self.mapillary_geojson['features']:
                    self.mapillary_geojson['features'].append(feature)

            if len(data['features']) == 1000:
                next_url = res.links['next']['url']
                get_token = re.search(r'&_next_page_token=(.*?)&', next_url)
                if get_token is None:
                    get_token = re.search(r'&_next_page_token=(.*)', next_url)
                current_token = get_token.group(1)
                self.page_no += 1
                if current_token != last_token:
                    last_token = current_token
                    self.fetch_traffice_sign(
                        next_url, country, last_token, self.page_no
                    )
                return self.mapillary_geojson
            return self.mapillary_geojson


if __name__ == '__main__':
    country_dict = {
        'France': 'FR',
        'Netherlands': 'NL',
        'Spain': 'ES',
        'Portugal': 'PT',
        'Germany': 'DE'
    }
    # -  Mapillary_API class instance.
    api = Mapillary_API()
    # - Create output dir
    api.create_dir("PAGES")
    api.create_dir("URLS")
    api.create_dir("OUTPUT")
    for country in country_dict.keys():
        api.page_no = 1
        api.status = {
            "country": "",
            "details": [],
            "status": "Not Started"
        }
        print("Started Process For Country: %s" % country)
        region = country_dict.get(country)
        fname = (os.path.join(os.getcwd(), "URLS", "%s_urls.json" % country))
        url = (
            "https://a.mapillary.com/v3/map_features?"
            "layers=trafficsigns&sort_by=key"
            "&client_id=%s&per_page=%s&values=%s&iso_countries=%s" % (
                api.client_id,
                '1000',
                '*height*,*width*,*weight*,*axle*,*water*,*dangerous*',
                region
            )
        )
        # Read existing fetched data
        if os.path.isfile(fname):
            with open(fname) as json_file:
                data = json.load(json_file)
                if data['status'] == 'Done':
                    continue
                for row in data['details']:
                    if row not in api.status['details']:
                        api.status['details'].append(row)
        if len(api.status.get('details')) > 0:
            details = api.status['details'][-1]
            url = details['url']
            token = details['token']
            page_no = details['page_number']
        output = api.fetch_traffice_sign(url, country, api.token, api.page_no)
        api.status['status'] = 'Done'
        with open(fname, 'w', encoding='utf-8') as json_fh:
            json.dump(api.status, json_fh)
        geojosn_file = os.path.join(
            os.getcwd(), "OUTPUT", "%s_output.geojson" % country
        )
        with open(geojosn_file, "w", encoding='utf-8') as fh:
            json.dump(output, fh)
        print("Process Finish For Country: %s" % country)
