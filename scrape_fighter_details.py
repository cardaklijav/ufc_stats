import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from scraper import get_full_page_html
import os

output_path = "fighter_career_stats.csv"

if os.path.exists(output_path):
    already_done_df = pd.read_csv(output_path)
    already_done_urls = set(already_done_df["fighter_url"])
else:
    already_done_urls = set()

print(f"Already finished: {len(already_done_urls)} fighters")

def scrape_one_fighter(url):
    html = get_full_page_html(url, wait_selector="table.b-fight-details__table")
    soup = BeautifulSoup(html, "html.parser")

    stats_list = soup.find_all("li", class_="b-list__box-list-item")

    career_stats = {}
    for li in stats_list:
        label_tag = li.find("i")
        if not label_tag:
            continue

        label = label_tag.text.strip().rstrip(":")
        full_text = li.text.strip()
        value = full_text.replace(label_tag.text.strip(), "").strip()

        career_stats[label] = value

    table = soup.find("table", class_="b-fight-details__table")
    fight_history_df = pd.read_html(StringIO(str(table)))[0]

    career_stats.pop('', None)
    fight_history_df = fight_history_df.dropna(how="all")

    career_stats["fighter_url"] = url
    fight_history_df["fighter_url"] = url

    return career_stats, fight_history_df