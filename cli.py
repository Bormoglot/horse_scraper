import argparse

parser = argparse.ArgumentParser(
    description='Scrape horse info for some owner from https://hippodrom.ru/. Get a CSV of horses and races, where they won money.')

parser.add_argument('owner_id', type=int,
    help='last digits in an URL like https://hippodrom.ru/modules/owners/owner.php?owner_id=112')
parser.add_argument('--min_year', type=int, default=2005,
    help='sets the earliest race year to scrape. Four-digit year YYYY')

args = parser.parse_args()