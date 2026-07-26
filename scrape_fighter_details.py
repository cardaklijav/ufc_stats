from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from scraper import get_full_page_html
import os

career_output_path = "output/fighter_career_stats.csv"
fight_history_output_path = "output/fighter_fight_history.csv"

if os.path.exists(career_output_path):
    already_done_df = pd.read_csv(career_output_path)
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

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    fighters_df = pd.read_csv("output/fighters.csv")

    for url in fighters_df["fighter_url"]:
        if url in already_done_urls:
            continue

        try:
            career_stats, fight_history_df = scrape_one_fighter(url)

            career_df = pd.DataFrame([career_stats])
            career_file_exists = os.path.exists(career_output_path)
            career_df.to_csv(career_output_path, mode="a", header=not career_file_exists, index=False, encoding="utf-8-sig")

            fight_history_file_exists = os.path.exists(fight_history_output_path)
            fight_history_df.to_csv(fight_history_output_path, mode="a", header=not fight_history_file_exists, index=False, encoding="utf-8-sig")

            already_done_urls.add(url)
            print(f"Finished: {url}")

        except Exception as e:
            print(f"Error for {url}: {e}")