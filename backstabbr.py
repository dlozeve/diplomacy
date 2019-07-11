import collections
import json
import re
import requests


SEASONS = ['spring', 'fall', 'winter']


def collect_info(url, max_year):
    orders = collections.defaultdict(dict)
    units = collections.defaultdict(dict)
    territories = collections.defaultdict(dict)

    years = [str(y) for y in range(1901, max_year)]
    for year in years:
        for season in SEASONS:
            print(f'Requesting data for {season} {year}')

            r = requests.get(f'{url}/{year}/{season}')
            if r.status_code != 200:
                raise ValueError('Error: ', r.status_code)

            current_orders = re.search(r'var orders = (.*);', r.text)
            if not current_orders:
                raise ValueError('No orders in ', year, season)
            orders[year][season] = json.loads(current_orders.group(1))

            current_units = re.search(r'var unitsByPlayer = (.*);', r.text)
            if not current_units:
                raise ValueError('No units in ', year, season)
            units[year][season] = json.loads(current_units.group(1))

            current_territories = re.search(r'var territories = (.*);', r.text)
            if not current_territories:
                raise ValueError('No territories in ', year, season)
            territories[year][season] = json.loads(current_territories.group(1))

    return orders, units, territories


def export_info(info, filename='orders.json'):
    print(f'Saving {filename}')
    with open(filename, 'w') as fd:
        json.dump(info, fd)


def main():
    url = 'https://www.backstabbr.com/sandbox/diplomindsay/5940277246689280'
    max_year = 1914
    orders, units, territories = collect_info(url, max_year)

    export_info(orders, 'orders.json')
    export_info(units, 'units.json')
    export_info(territories, 'territories.json')


if __name__ == '__main__':
    main()
