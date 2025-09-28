# MyFCD97 Scraper

## Production Selenium MyFCD97 Scraper

This is a production-ready Selenium-based scraper for the MyFCD97 (Malaysian Food Composition Database 1997) website. It extracts complete nutritional data for all food items with proper categorization and serving size calculations.

### Features

- **Complete Data Extraction**: Scrapes all food items from 1997 database
- **Proper Categories**: Extracts nutrient categories (Proximates, Minerals, Vitamins, etc.)
- **Accurate Values**: Gets website-calculated serving size values
- **Quality Output**: Structured JSON format with all nutrient data
- **Production Ready**: Robust error handling and progress tracking

### Target Website

- **URL**: https://myfcd.moh.gov.my/myfcd97/
- **Database**: 1997 Malaysian Food Composition Database
- **Total Items**: ~233 food items
- **Data**: Complete nutritional profiles without images/source/dates

### Requirements

```
selenium==4.15.2
beautifulsoup4==4.12.2
requests==2.31.0
pandas==2.1.4
json5==0.9.14
webdriver-manager==4.0.1
```

### Installation

```bash
pip install -r requirements.txt
```

### Usage

#### Quick Run (All Foods)
```bash
python scrape_all_foods.py
```

#### Individual Scraper
```bash
python myfcd97_scraper.py
```

### Output

- **Location**: `/Users/ooichienzhen/Desktop/myFCD1997/datasets/`
- **Format**: Individual JSON files per food item
- **Naming**: `{NDB_NO}.json`
- **Structure**: Complete nutrient data with categories and serving sizes

### Sample Output Structure

```json
{
  "NDB No": "01001",
  "Description": "Rice, white, long-grain, regular, raw",
  "Food Group": "Cereals and grain products",
  "Nutrient": [
    {
      "category": "Proximates"
    },
    {
      "name": "Energy",
      "unit": "kcal",
      "value_per_100g": "365",
      "1_cup_158g": "576"
    }
  ]
}
```

### Monitoring Progress

```bash
python check_progress.py
```

### Data Analysis

```bash
python analyze_results.py
```

### CSV Export

```bash
python create_csv.py
```

### Performance

- **Expected Time**: 20-30 minutes for all 233 items
- **Success Rate**: >95% with proper error handling
- **Data Quality**: Complete nutritional profiles with serving calculations

### Technical Details

- Uses Selenium WebDriver for JavaScript-heavy pages
- Implements respectful delays (0.8s between requests)
- Automatic ChromeDriver management
- Comprehensive error handling and logging
- Atomic file operations to prevent corruption

### Data Quality Assurance

- Extracts proper nutrient categories
- Preserves website-calculated serving size values
- Validates data completeness
- Maintains exact formatting from source

This scraper provides production-quality data extraction while respecting the source website's resources.