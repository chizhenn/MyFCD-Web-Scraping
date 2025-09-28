# MyFCD Scraper

Extracts nutritional data from Malaysian Food Composition Database (https://myfcd.moh.gov.my/myfcdcurrent/).

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
myFCD/
├── scrape_all_foods.py    # Main scraper
├── create_csv.py          # JSON to CSV converter  
├── myfcd_scraper.py       # Scraper engine
├── check_progress.py      # Progress monitor
├── analyze_results.py     # Data analysis
├── requirements.txt       # Dependencies
├── README.md             # This file
└── datasets/             # Output folder
    ├── R101061.json      # Individual food files (233 total)
    ├── R101069.json
    ├── ...
    └── myfcd_complete.csv # All data in CSV format
```

## What You Get

- **233 food items** with complete nutritional data
- **JSON format**: Individual files with full structure  
- **CSV format**: Single file for analysis
- **Data includes**: NDB No, Description, Food Group, Image, Source, Published Date, Nutrients (by category)

## Technical Approach

1. **AJAX call** - Get all food IDs quickly
2. **Selenium** - Visit each detail page for JavaScript calculations  
3. **Extract** - Copy exact values (no calculations)
4. **Save** - Individual JSON + combined CSV

## Requirements

- Python 3.8+
- Chrome browser  
- Internet connection

**Time**: ~30 minutes for all 233 foods