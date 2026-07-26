import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://statleaders.ufc.com/en/career"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("div", class_="results-table")
articles = soup.find_all("article", class_="results-group")

fighters_data = {}

for article in articles:
    title_tag = article.find("h3")
    category = title_tag.text.strip()

    table_div = article.find("div", class_="results-table")
    rows = table_div.find_all("div", class_="results-table--tr")

    for row in rows:
        if "results-table--th" in row.get("class", []):
            continue

        spans = row.find_all("span")
        fighter_name = spans[1].text.strip()
        value = spans[2].text.strip()

        if fighter_name not in fighters_data:
            fighters_data[fighter_name] = {}

        fighters_data[fighter_name][category] = value

df = pd.DataFrame.from_dict(fighters_data, orient="index")
df.index.name = "Fighter"
df = df.reset_index()

print(df.shape)
print(df.head())

df.to_csv("output/record_book.csv", index=False, encoding="utf-8-sig")