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

## Dataset Columns (`output/training_dataset.csv`)

One row = one fight. `fighter_*` / `opponent_*` prefixes mark which side
of the fight each stat belongs to.

### Fight info
| Column | Description |
|---|---|
| `Event` | Name and date of the event the fight took place at |
| `Method` | How the fight ended (e.g. `S-DEC`, `KO/TKO`, `SUB`) |
| `Round` | Round the fight ended in |
| `Time` | Time within that round the fight ended |
| `fighter_won` | **Target column.** `1` if `fighter_name` won, `0` if they lost |

### Fight-specific stats (this fight only)
| Column | Description |
|---|---|
| `fighter_name` / `opponent_name` | Fighter names for this fight |
| `fighter_kd` / `opponent_kd` | Knockdowns landed in this fight |
| `fighter_str` / `opponent_str` | Significant strikes landed in this fight |
| `fighter_td` / `opponent_td` | Takedowns landed in this fight |
| `fighter_sub` / `opponent_sub` | Submission attempts in this fight |
| `Kd`, `Str`, `Td`, `Sub` | Raw unparsed originals (both fighters' values glued in one string) — superseded by the split columns above, kept for reference/debugging only |

### Career stats (as of scrape date, not fight date)
| Column | Description |
|---|---|
| `fighter_Height` / `opponent_Height` | Height |
| `fighter_Weight` / `opponent_Weight` | Weight |
| `fighter_Reach` / `opponent_Reach` | Reach |
| `fighter_STANCE` / `opponent_STANCE` | Fighting stance (Orthodox, Southpaw, etc.) |
| `fighter_DOB` / `opponent_DOB` | Date of birth |
| `fighter_SLpM` / `opponent_SLpM` | Significant strikes landed per minute (career avg.) |
| `fighter_Str. Acc.` / `opponent_Str. Acc.` | Significant striking accuracy (career avg.) |
| `fighter_SApM` / `opponent_SApM` | Significant strikes absorbed per minute (career avg.) |
| `fighter_Str. Def` / `opponent_Str. Def` | Significant strike defense — % of opponent strikes that did not land (career avg.) |
| `fighter_TD Avg.` / `opponent_TD Avg.` | Average takedowns landed per 15 minutes (career avg.) |
| `fighter_TD Acc.` / `opponent_TD Acc.` | Takedown accuracy (career avg.) |
| `fighter_TD Def.` / `opponent_TD Def.` | Takedown defense — % of opponent takedowns that did not land (career avg.) |
| `fighter_Sub. Avg.` / `opponent_Sub. Avg.` | Average submission attempts per 15 minutes (career avg.) |

**Note:** career stats reflect the fighter's stats *at scrape time*, not
their stats as of that specific historical fight — keep this in mind for
older fights if using career stats as a feature.
