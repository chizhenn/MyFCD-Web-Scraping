#!/usr/bin/env python3
"""
Production MyFCD Industry Scraper - Scrapes ALL food items from the database
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from myfcd_industry_scraper import ProductionSeleniumScraper


def main():
    """Main function to scrape ALL food data"""
    print("=== Production MyFCD Industry Food Composition Database Scraper ===")
    print(" Target: https://myfcd.moh.gov.my/myfcdindustri/")
    print(" Output: /Users/ooichienzhen/Desktop/myFCD_Industry/datasets/")
    print(" Expected: Industry food database items")
    print(" Estimated time: ~20-30 minutes")
    print("=" * 70)
    
    try:
        print(" Starting full scraping process...")
        print(" This will scrape ALL industry food items. Press Ctrl+C to interrupt if needed.")
        print()
        
        scraper = ProductionSeleniumScraper()
        
        # Remove the max_items limit to scrape everything
        scraper.scrape_all_foods(max_items=None)
        
        print("\n" + "=" * 70)
        print(" Full scraping completed successfully!")
        print(" Check the output directory for all JSON files")
        
    except KeyboardInterrupt:
        print("\n  Scraping interrupted by user")
        print(" Partial results may be available in the output directory")
        return 1
    except Exception as e:
        print(f"\n Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
