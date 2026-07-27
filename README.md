# UFC Stats Scraper & Dataset Builder

Scrapes fighter and fight data from `ufcstats.com`, and builds a clean,
merged dataset for training a machine learning model to predict UFC fight
winners.

## What it does

1. Scrapes the full list of UFC fighters and their profile URLs
2. Scrapes each fighter's career stats and complete fight history
3. Merges everything into a single, deduplicated, ML-ready CSV — one row
   per fight, with both fighters' stats side by side and a binary
   win/loss target

## Project Structure

```
ufc_stats/
├── scraper.py                    # Core reusable scraping functions (Playwright)
├── scrape_events.py              # Scrapes the Events (Completed) table (unused in final dataset)
├── scrape_fighters.py            # Scrapes the full Fighters list (A-Z)
├── scrape_fighter_details.py     # Scrapes each fighter's career stats + fight history
├── scrape_record_book.py         # Scrapes statleaders.ufc.com leaderboards (optional, unused)
├── build_dataset.py              # Merges everything into one training-ready CSV
├── requirements.txt
├── .gitignore
└── output/
    ├── events.csv
    ├── fighters.csv
    ├── fighter_career_stats.csv
    ├── fighter_fight_history.csv
    ├── record_book.csv
    └── training_dataset.csv        # FINAL dataset — 11,200 rows, 45 columns
```

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage (run in order, from a clean project)

```bash
python scrape_fighters.py          # builds fighters.csv with profile URLs
python scrape_fighter_details.py   # slow (hours), resume-safe if interrupted
python build_dataset.py            # produces output/training_dataset.csv
```

`scrape_events.py` and `scrape_record_book.py` are optional — their output
is not used in the final training dataset.
