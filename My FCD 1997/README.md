# MyFCD 1997 Scraper

Extracts nutritional data from Malaysian Food Composition Database (https://myfcd.moh.gov.my/myfcd97/).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper (creates JSON files)
python scrape_all_foods.py

# Convert to CSV format
python create_csv.py
```

## File Structure

```
myFCD1997/
├── scrape_all_foods.py    # Main scraper
├── create_csv.py          # JSON to CSV converter  
├── myfcd97_scraper.py       # Scraper engine
├── check_progress.py      # Progress monitor
├── analyze_results.py     # Data analysis
├── requirements.txt       # Dependencies
├── README.md             # Documentation
└── datasets/             # Output folder
    ├── 101001.json      # Individual food files (233 total)
    ├── 101002.json
    ├── ...
    └── myfcd97_complete.csv # All data in CSV format
```

## What You Get

- **1033 food items** with complete nutritional data
- **JSON format**: Individual files with full structure  
- **CSV format**: Single file for analysis
- **Data includes**: NDB No, Description, Food Group, Nutrients (by category)

## Technical Approach

1. **AJAX call** - Get all food IDs quickly
2. **Selenium** - Visit each detail page for JavaScript calculations  
3. **Extract** - Copy exact values (no calculations)
4. **Save** - Individual JSON + combined CSV

## Requirements

- Python 3.8+
- Chrome browser  
- Internet connection

**Time**: ~75 minutes for all 1033 foods
