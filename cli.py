import argparse

parser = argparse.ArgumentParser(
    description='Scrape horse info for some owner from https://hippodrom.ru/. Get an .xlsx of horses and races, where they won money.')

parser.add_argument('--path', default='results/',
    help='path to the place to save results. By default creates directory "results"')
parser.add_argument('owner_id', type=int,
    help='last digits in an URL like https://hippodrom.ru/modules/owners/owner.php?owner_id=112')
parser.add_argument('--min_year', type=int, default=2005,
    help='sets the earliest race year to scrape. Four-digit year YYYY. Default is 2005.')
parser.add_argument('-csv', action='store_true',
    help='output table as a csv')

args = parser.parse_args()