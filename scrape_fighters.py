import os
import string
import pandas as pd
from bs4 import BeautifulSoup
from scraper import scrape_page

TABLE_SELECTOR = "table.b-statistics__table"
OUTPUT_PATH = "output/fighters.csv"


def parse_fighters_table(table_html):
    soup = BeautifulSoup(table_html, "html.parser")
    rows = soup.find_all("tr", class_="b-statistics__table-row")

    fighters = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 10:
            continue

        link_tag = cells[0].find("a")
        fighter_url = link_tag["href"] if link_tag else None

        fighter = {
            "First": cells[0].text.strip(),
            "Last": cells[1].text.strip(),
            "Nickname": cells[2].text.strip(),
            "Ht": cells[3].text.strip(),
            "Wt": cells[4].text.strip(),
            "Reach": cells[5].text.strip(),
            "Stance": cells[6].text.strip(),
            "W": cells[7].text.strip(),
            "L": cells[8].text.strip(),
            "D": cells[9].text.strip(),
            "fighter_url": fighter_url,
        }
        fighters.append(fighter)

    return fighters


def scrape_fighters():
    all_fighters = []

    for letter in string.ascii_lowercase:
        url = f"http://ufcstats.com/statistics/fighters?char={letter}&page=all"
        table_html = scrape_page(url=url, table_selector=TABLE_SELECTOR)

        if table_html:
            fighters = parse_fighters_table(table_html)
            all_fighters.extend(fighters)
            print(f"  {letter}: {len(fighters)} fighters")
        else:
            print(f"  {letter}: table is not found")

    df = pd.DataFrame(all_fighters)

    os.makedirs("output", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")