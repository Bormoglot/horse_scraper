# About
This is a web scraper for https://hippodrom.ru
The output is an .xlsx or .csv file with fields:
- `horse_name`: name of the horse,
- `horse_url`: link to the horse's page,
-  `race_url`: link to race page,
- `race_date`: date of the race,
- `owner`: name of the horse owner at the time of the race,
- `prize`: prize money that the horse won,
- `currency`: currency of the prize.
# Installation
1. `git clone https://github.com/Bormoglot/horse_scraper`
2. `cd horse_scraper`
3. `python3 -m venv .`
4. `pip3 install -r requirements.txt`
# Running
`python3 horse_scraper.py <owner_id> --min_year <2010> --path <somewhere/there> -csv`
- `<owner_id>` - the last digits in urls like https://hippodrom.ru/modules/owners/owner.php?owner_id=582
- `--min_year <2010>` - optional, the earliest race year to parse. Default year is 2005.
- `--path <somewhere/there>` - optional, path to the place to save results. By default creates directory 'results'.
- `-csv` - change default .xlsx output format to .csv

For help on arguments use `python3 horse_scraper.py --help`.