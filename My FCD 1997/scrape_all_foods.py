#!/usr/bin/env python3
"""
Production MyFCD97 Scraper - Scrapes ALL food items from the 1997 database
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from myfcd97_scraper import ProductionSelenium1997Scraper


def main():
    """Main function to scrape ALL food data from 1997 database"""
    print("=== Production MyFCD97 Food Composition Database Scraper ===")
    print("Target: https://myfcd.moh.gov.my/myfcd97/")
    print("Output: /Users/ooichienzhen/Desktop/myFCD1997/datasets/")
    print("Note: No images, source, or published dates extracted")
    print("=" * 70)
    
    try:
        print("Starting full scraping process for 1997 database...")
        print("This will scrape ALL food items. Press Ctrl+C to interrupt if needed.")
        print()
        
        scraper = ProductionSelenium1997Scraper()
        
        # Remove the max_items limit to scrape everything
        scraper.scrape_all_foods(max_items=None)
        
        print("\n" + "=" * 70)
        print("Full scraping completed successfully!")
        print("Check the output directory for all JSON files")
        
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
