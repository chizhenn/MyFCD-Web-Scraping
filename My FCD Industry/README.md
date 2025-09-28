# MyFCD Industry Scraper

Extracts nutritional data from Malaysian Food Composition Database - Industry Edition (https://myfcd.moh.gov.my/myfcdindustri/).

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
myFCD_Industry/
├── scrape_all_foods.py    # Main scraper
├── create_csv.py          # JSON to CSV converter  
├── myfcd_industry_scraper.py  # Scraper engine
├── check_progress.py      # Progress monitor
├── analyze_results.py     # Data analysis
├── requirements.txt       # Dependencies
├── README.md             # This file
└── datasets/             # Output folder
    ├── [NDB_No].json     # Individual food files
    ├── ...
    └── myfcd_industry_complete.csv # All data in CSV format
```

## What You Get

- **Industry food items** with complete nutritional data
- **JSON format**: Individual files with full structure  
- **CSV format**: Single file for analysis
- **Data includes**: NDB No, Description, Food Group, Image, Source, Published Date, Nutrients (by category)

## Technical Approach

1. **AJAX call** - Get all food IDs quickly from industry database
2. **Selenium** - Visit each detail page for JavaScript calculations  
3. **Extract** - Copy exact values (no calculations)
4. **Save** - Individual JSON + combined CSV

## Requirements

- Python 3.8+
- Chrome browser  
- Internet connection

## Usage Examples

### Basic Scraping
```bash
python scrape_all_foods.py
```

### Monitor Progress
```bash
python check_progress.py
```

### Analyze Results
```bash
python analyze_results.py
```

### Convert to CSV
```bash
python create_csv.py
```


## Data Structure

Each JSON file contains:
```json
{
  "NDB No": "1200001",
  "Description": "F&N, ICE MOUNTAIN, MINERAL WATER, NATURAL",
  "Food Group": "Beverages",
  "Image": "https://myfcd.moh.gov.my/myfcdindustri/uploads/FN_Ice_mountain.jpg",
  "Source": "F&N Beverages Manufacturing Sdn Bhd",
  "Published Date": "2018-02-06",
  "Nutrient": [
    {
      "category": "Proximates"
    },
    {
      "name": "Energy",
      "unit": "Kcal",
      "value_per_100ml": "0",
      "1_bottle_(_600_ml_)": "0"
    },
    {
      "category": "Minerals"
    },
    {
      "name": "Calcium",
      "unit": "mg",
      "value_per_100ml": "4.08",
      "1_bottle_(_600_ml_)": "24"
    }
  ]
}
```

## Features

- **Targeted scraping** for industry food database
- **Accurate food groups** (22 categories: Beverages, Cereals, etc.)
- **Correct source attribution** (actual manufacturer names)
- **Category-organized nutrients** (Proximates, Minerals, Vitamins, etc.)
- **Actual calculated values** from website JavaScript
- **Serving size data** with real portions
- **Flexible output** (JSON + CSV formats)
- **Progress monitoring** during scraping
- **Data analysis** tools included

## Output

- Individual JSON files for each food item
- Combined CSV file for easy analysis
- Summary statistics and quality reports

**Time**: Varies based on industry database size (~20-40 minutes typical)
