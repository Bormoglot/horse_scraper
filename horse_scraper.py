import requests
import re
import time
import sys
import pathlib

from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

import cli
import output

def get_soup(url):
    try:
        r = requests.get(url,timeout=60)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print ("Unknown Error: Something broke",err)
        sys.exit(1)
   
    soup = BeautifulSoup(r.text, 'html.parser')
    time.sleep(3)
    return soup

def parse_owner_page(owner_id):
    """
    Parses owner page (like https://hippodrom.ru/modules/owners/owner.php?owner_id=123)
    Input: int
    Returns: list
    """
    soup = get_soup('https://hippodrom.ru/modules/owners/owner.php?owner_id=' + str(owner_id))
    
    horse_lst = []
    
    # The horse table is the only element with cellspacing = 1
    horse_table = soup.find('table', {'cellspacing':'1'})
    
    # Horse rows have style="font-size:12px;"
    horse_rows = horse_table.find_all('tr', {'style': 'font-size:12px;'})
    
    for row in horse_rows:
        # If the cells for wins and prize places are not empty
        if row.select_one("td:nth-of-type(3)").text or row.select_one("td:nth-of-type(4)").text:
            horse_info = {}
            # Get url
            raw_url = row.select_one("td:nth-of-type(2)").a['href']
            sep = '&lang'
            horse_info['horse_url'] = raw_url.split(sep, 1)[0]
            # Get horse name
            horse_info['horse_name'] = row.select_one("td:nth-of-type(2)").text
            horse_lst.append(horse_info)
    
    return horse_lst

def parse_horse_page(url, start_year):
    """
    Parses horse page (like https://hippodrom.ru/modules/horses/horse.php?horse_id=123)
    Input: string
    Returns: list
    """
    
    def get_race_table_results(soup):
        """
        Helper function to find and parse horse's racing career table
        Input: Beautiful Soup object
        Returns: list
        """
        data = []
        
        # Find racing career table
        races_table = soup.find('h2', text = 'Скаковая карьера').find_next('table')

        # Find rows with prizes
        for row in races_table.select('tr'):
            price_cell = row.find('td', {'class': 'price'})

            # If there are non-empty prize cells
            if price_cell and price_cell.text:
                # Get the race date 
                race_date_text = row.select_one('td.date').text
                race_date = datetime.strptime(race_date_text, '%d-%m-%y').date()

                if race_date.year >= start_year:

                    race_info = {}

                    race_info['race_date'] = str(race_date)

                    # Get race url
                    race_info['race_url'] = row.select_one("td:nth-of-type(3)").a['href']

                    # Get prize currency
                    race_info['currency'] = row.select_one("td:nth-of-type(8)").text

                    # Get the prize money
                    prize_raw = row.select_one('td.price').text
                    race_info['prize'] = int(prize_raw.replace(' ', ''))
                    
                    data.append(race_info)
                    
        return data
    
    soup = get_soup(url)
    
    all_races = []
    
    # if there is a non-empty div with class = 'PageNav', table has multiple pages 
    page_nav = soup.find('div', {'class': 'PageNav'})
    
    if page_nav and page_nav.contents:
        links = page_nav.findChildren('a')

        # if link text is a digit, get the largest - number of pages
        num_pages = max([int(link.text) for link in links if link.text.isdigit()])
        
        next_pages = []
        
        # query for next table pages is &start=N, where N changes
        # in increments of 10 for each next page
        for page_num in range(num_pages - 1):
            query_param = (page_num + 1) * 10
            page_url = url + '&start=' + str(query_param)
            next_pages.append(page_url)
            
        for page in next_pages:
            soup_new = get_soup(page)
            data = get_race_table_results(soup_new)
            all_races.extend(data)    
    
    
    data = get_race_table_results(soup)
    all_races.extend(data)
    
    return all_races

def parse_race_page(race_url, horse_url):
    """
    Parses race page (like https://hippodrom.ru/modules/results/race.php?race_id=123)
    Input: string, string
    Returns: string
    """
    soup = get_soup(race_url)
    
    # Find a row with a link to horse's page
    link_tag = soup.find('a', href=horse_url)
    row = link_tag.find_parent('tr')

    # Get owner name
    owner = row.select_one("td:nth-of-type(7)").a.text

    return owner


def main(owner_id, start_year, path, csv):
    
    print(f'Starting scraping info for user ID {owner_id}...')
    
    horse_lst = parse_owner_page(owner_id)

    print('Scraping horse info...')

    for horse in tqdm(horse_lst):
        races = parse_horse_page(horse['horse_url'], start_year)
        
        for race in races:
            race['owner'] = parse_race_page(race['race_url'], horse['horse_url'])
        
        horse['races'] = races

    output_path = pathlib.Path(path)
    # Create dir if not there
    output_path.mkdir(parents=True, exist_ok=True)
        
    header = ['horse_name', 'horse_url', 'race_url', 'race_date', 'owner', 'prize', 'currency']
    if not csv:
        output.write_xlsx(horse_lst=horse_lst, owner_id=owner_id, header=header, path=output_path)
    else:
        output.write_csv(horse_lst=horse_lst, owner_id=owner_id, header=header, path=output_path)

    print('Table is ready!')

if __name__ == "__main__":
    main(owner_id=cli.args.owner_id, start_year=cli.args.min_year, path=cli.args.path, csv=cli.args.csv)