# About

A small webscraper for [Transparency International-Russia](https://transparency.org.ru/), which helped a [horse-related tax evasion investigation](https://transparency.org.ru/special/konikadyrova/).

## General info and background

[Hippodrom.ru](https://hippodrom.ru/) is a Russian website about horse racing. They maintain a database of [race horses](https://hippodrom.ru/modules/horses/horse.php), [horse owners](https://hippodrom.ru/modules/owners/owner.php), [breeders](https://hippodrom.ru/modules/breeders/breeder.php), race results, etc. However, you can't query the database in arbitrary way.

This script can help you inquire, how much money the horses won for their owner: it compiles a table of all the horses of a horse owner, which got prizes.

The output is an .xlsx or .csv file with fields:

- `horse_name`: name of the horse,
- `horse_url`: link to the horse's page,
- `race_url`: link to race page,
- `race_date`: date of the race,
- `owner`: name of the horse owner at the time of the race,
- `prize`: prize money that the horse won,
- `currency`: currency of the prize.

## Installation

1. Clone or download https://github.com/Bormoglot/horse_scraper
2. `cd horse_scraper`
3. Create a virtual environment: `python -m venv .`
4. Activate a virtual environment:
    - Windows cmd: `.\Scripts\activate.bat` (to deactivate use `.\Scripts\deactivate.bat`)
    - Windows PowerShell: `.\Scripts\Activate.ps1` (to deactivate use `deactivate`)
5. `pip install -r requirements.txt`

## Running

The script runs on python >= 3.6

`python horse_scraper.py <owner_id> --min_year <2010> --path <somewhere/there> -csv`

- `<owner_id>` - the last digits in urls like <https://hippodrom.ru/modules/owners/owner.php?owner_id=582>
- `--min_year <2010>` - optional, the earliest race year to parse. Default year is 2005.
- `--path <somewhere/there>` - optional, path to the place to save results. By default creates directory 'results'.
- `-csv` - optional, change default .xlsx output format to .csv

For help on arguments use `python horse_scraper.py --help`.