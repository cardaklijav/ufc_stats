from scraper import scrape_page
import pandas as pd
from io import StringIO

table_html = scrape_page(
    url="http://ufcstats.com/statistics/events/completed",
    table_selector="table.b-statistics__table-events", # table class that we acquired inspecting the website
    click_selector=".b-statistics__paginate a[href*='page=all']"
)

df = pd.read_html(StringIO(table_html))[0]
df.to_csv("events.csv", index=False, encoding="utf-8")