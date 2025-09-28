#!/usr/bin/env python3
"""
Production Selenium MyFCD Industry Scraper - Scrapes all foods with proper categories and actual values
"""

import json
import os
import stat
import time
import re
import requests
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class ProductionSeleniumScraper:
    """Production Selenium-based scraper for complete MyFCD Industry data"""
    
    def __init__(self, output_dir: str = "/Users/ooichienzhen/Desktop/myFCD_Industry/datasets"):
        """Initialize the production scraper"""
        self.base_url = "https://myfcd.moh.gov.my/myfcdindustri/"
        self.ajax_url = "https://myfcd.moh.gov.my/myfcdindustri/static/DataTables-1.10.12/examples/server_side/scripts/server_processing.php"
        self.output_dir = output_dir
        self.driver = None
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set up requests session for AJAX calls
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        })
    
    def setup_driver(self) -> None:
        """Set up Selenium WebDriver with performance optimizations"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-images')  # Faster loading
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--window-size=1280,720')  # Smaller window
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        try:
            try:
                driver_path = ChromeDriverManager().install()
                os.chmod(driver_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                service = webdriver.chrome.service.Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except:
                print("WARNING: ChromeDriverManager failed, trying system driver...")
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.implicitly_wait(5)  # Reduced from 10s to 5s
            print("SUCCESS: Selenium WebDriver initialized")
        except Exception as e:
            print(f"ERROR: Failed to initialize WebDriver: {e}")
            raise
    
    def close_driver(self) -> None:
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def get_all_food_items(self) -> List[Dict[str, str]]:
        """Get complete food list from AJAX endpoint"""
        print(" Fetching complete food list from AJAX endpoint...")
        
        all_foods = []
        start = 0
        page_size = 100
        
        # Food group mapping (actual from website)
        food_group_mapping = {
            '-1': 'Ungrouped',
            '1': 'Cereals and grain products',
            '2': 'Nuts, seeds and products',
            '3': 'Legumes and legume products',
            '4': 'Vegetables and vegetable products',
            '5': 'Fruits and fruit products',
            '6': 'Sugars and syrups',
            '7': 'Meat and meat products',
            '8': 'Eggs',
            '9': 'Milk and milk products',
            '10': 'Fish, shellfish and products',
            '11': 'Oils and fats',
            '12': 'Beverages',
            '13': 'Miscellaneous',
            '14': 'Starchy roots, tubers and products',
            '15': 'Ice cream and ice confection',
            '16': 'Chocolate and chocolate confectionery products',
            '17': 'Seasoning',
            '18': 'Sweets',
            '19': 'Snacks',
            '20': 'Franchised Food and Beverages',
            '21': 'Fast Foods'
        }
        
        while True:
            data = {
                'my_food_group': 0,  # All food groups
                'my_manufacturer': 0,  # All manufacturers
                'start': start,
                'length': page_size
            }
            
            try:
                response = self.session.post(self.ajax_url, data=data, timeout=30)
                response.raise_for_status()
                ajax_data = response.json()
                
                food_items = []
                for row in ajax_data.get('data', []):
                    if len(row) >= 3:
                        ndb_no = str(row[0]).strip()
                        description = str(row[1]).strip()
                        food_group_id = str(row[2]).strip()
                        
                        food_group = food_group_mapping.get(food_group_id, f"Food Group {food_group_id}")
                        detail_url = f"{self.base_url}index.php/site/detail_product/{ndb_no}/1/10/-1/0/0/"
                        
                        food_items.append({
                            'ndb_no': ndb_no,
                            'description': description,
                            'food_group': food_group,
                            'detail_url': detail_url
                        })
                
                all_foods.extend(food_items)
                print(f"  Page {start//page_size + 1}: {len(food_items)} items")
                
                # Check if we're done
                total_records = ajax_data.get('recordsTotal', 0)
                if len(food_items) < page_size or start + page_size >= total_records:
                    break
                
                start += page_size
                time.sleep(0.1)  # Reduced from 0.5s to 0.1s
                
            except Exception as e:
                print(f"ERROR: Error fetching page {start//page_size + 1}: {e}")
                break
        
        print(f"SUCCESS: Retrieved {len(all_foods)} total food items")
        return all_foods
    
    def scrape_food_detail(self, detail_url: str, basic_info: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Scrape detailed food information using Selenium"""
        try:
            # Navigate to the detail page
            self.driver.get(detail_url)
            
            # Wait for the table to load and JavaScript to execute
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "tableDetailNutrient"))
            )
            # No additional sleep - let WebDriverWait handle timing
            
            # Initialize food data
            food_data = {
                'NDB No': basic_info['ndb_no'],
                'Description': basic_info['description'],
                'Food Group': basic_info['food_group'],
                'Image': '',
                'Source': '',
                'Published Date': '',
                'Nutrient': []
            }
            
            # Extract image
            try:
                img_elements = self.driver.find_elements(By.TAG_NAME, "img")
                for img in img_elements:
                    src = img.get_attribute('src') or ''
                    if 'uploads' in src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        food_data['Image'] = src
                        break
            except Exception as e:
                print(f"    WARNING: Image extraction error: {e}")
            
            # Extract metadata from the detail page table
            try:
                # Extract source from the table
                table_rows = self.driver.find_elements(By.XPATH, "//table//tr")
                for row in table_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:
                        header = cells[0].text.strip()
                        if header.lower() == 'source':
                            source_text = cells[2].text.strip()
                            if source_text:
                                food_data['Source'] = source_text
                            break
                
                # Extract published date from page source
                page_source = self.driver.page_source
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', page_source)
                if date_match:
                    food_data['Published Date'] = date_match.group(1)
                    
            except Exception as e:
                print(f"    WARNING: Metadata extraction error: {e}")
            
            # Extract nutrient data with categories and actual values
            try:
                table = self.driver.find_element(By.ID, "tableDetailNutrient")
                
                # Get headers for serving sizes
                header_cells = table.find_elements(By.XPATH, ".//thead//th")
                headers = []
                for cell in header_cells:
                    header_text = cell.text.strip()
                    # Clean up header text
                    header_text = re.sub(r'\n', ' ', header_text)
                    headers.append(header_text)
                
                # Get all rows from tbody
                rows = table.find_elements(By.XPATH, ".//tbody//tr")
                
                current_category = None
                
                for row in rows:
                    try:
                        # Check if this is a category header row
                        row_style = row.get_attribute('style') or ''
                        row_html = row.get_attribute('innerHTML')
                        
                        if ('background-color:#f2f2f2' in row_style or 
                            'background-color: rgb(242, 242, 242)' in row_style or
                            'colspan' in row_html):
                            
                            # Extract category name
                            category_cell = row.find_element(By.TAG_NAME, "td")
                            category_text = category_cell.text.strip()
                            
                            if category_text:
                                current_category = category_text
                                food_data['Nutrient'].append({
                                    'category': category_text
                                })
                            continue
                        
                        # Process nutrient data rows
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) < 3:
                            continue
                        
                        # Extract nutrient name, unit, and values
                        nutrient_name = cells[0].text.strip()
                        if not nutrient_name:
                            continue
                        
                        unit = cells[1].text.strip()
                        value_100g = cells[2].text.strip()
                        
                        # Create nutrient entry
                        nutrient_entry = {
                            'name': nutrient_name
                        }
                        
                        if unit and unit != '-':
                            nutrient_entry['unit'] = unit
                        
                        if value_100g and value_100g != '-':
                            # Check if this is per 100ml or per 100g
                            if len(headers) > 2 and '100ml' in headers[2]:
                                nutrient_entry['value_per_100ml'] = value_100g
                            else:
                                nutrient_entry['value_per_100g'] = value_100g
                        
                        # Extract serving size values (actual calculated values from website)
                        for i, cell in enumerate(cells[3:], 3):
                            serving_value = cell.text.strip()
                            if serving_value and serving_value != '-' and i < len(headers):
                                header = headers[i].strip()
                                if header:
                                    # Clean header for JSON key (preserve the exact serving format)
                                    clean_header = re.sub(r'[^\w\s\[\]().]', '_', header)
                                    clean_header = re.sub(r'\s+', '_', clean_header).strip()
                                    nutrient_entry[clean_header] = serving_value
                        
                        food_data['Nutrient'].append(nutrient_entry)
                        
                    except Exception as e:
                        print(f"    WARNING: Error processing row: {e}")
                        continue
                
            except Exception as e:
                print(f"    ERROR: Error extracting nutrient table: {e}")
            
            return food_data
            
        except Exception as e:
            print(f"    ERROR: Error loading page: {e}")
            return None
    
    def save_food_data(self, food_data: Dict[str, Any]) -> None:
        """Save food data to JSON file"""
        try:
            ndb_no = food_data.get('NDB No', 'unknown')
            safe_ndb = re.sub(r'[^\w\-.]', '_', ndb_no)
            filename = f"{safe_ndb}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(food_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"    ERROR: Error saving data: {e}")
    
    def scrape_all_foods(self, max_items: Optional[int] = None) -> None:
        """Scrape all food data with improved structure"""
        try:
            print(" Starting production Selenium scraper...")
            print(" Extracting categories and actual calculated values")
            
            # Get all food items
            food_list = self.get_all_food_items()
            
            if not food_list:
                print("ERROR: No food items found")
                return
            
            if max_items:
                food_list = food_list[:max_items]
                print(f" Limiting to {max_items} items for testing")
            
            print(f" Total items to process: {len(food_list)}")
            
            # Set up Selenium
            self.setup_driver()
            
            # Process each food item
            successful_count = 0
            
            for i, food_item in enumerate(food_list, 1):
                # Show progress less frequently to reduce overhead
                if i <= 3 or i % 50 == 0 or i == len(food_list):
                    print(f"\nProcessing {i}/{len(food_list)}: {food_item['ndb_no']} - {food_item['description']}")
                    print(f"   Progress: {i/len(food_list)*100:.1f}% complete")
                
                # Scrape detailed data
                food_data = self.scrape_food_detail(food_item['detail_url'], food_item)
                
                if food_data:
                    self.save_food_data(food_data)
                    successful_count += 1
                    
                    # Show details only for first few items to reduce overhead
                    if i <= 3:
                        categories = [n.get('category') for n in food_data['Nutrient'] if n.get('category')]
                        nutrient_count = len([n for n in food_data['Nutrient'] if n.get('name')])
                        print(f"    SUCCESS: Categories: {len(set(categories))}, Nutrients: {nutrient_count}")
                else:
                    if i <= 3:
                        print(f"    ERROR: Failed to process {food_item['ndb_no']}")
                
                # Minimal delay for faster processing
                time.sleep(0.1)
            
            print(f"\n Production scraping completed!")
            print(f" Successfully processed: {successful_count}/{len(food_list)} foods")
            print(f" Files saved to: {self.output_dir}")
            
        except Exception as e:
            print(f" Fatal error: {e}")
            raise
        finally:
            self.close_driver()


def main():
    """Main function to run production scraper"""
    print("=== Production MyFCD Industry Selenium Scraper ===")
    print(" Complete dataset with categories and actual values")
    print(" Output: /Users/ooichienzhen/Desktop/myFCD_Industry/datasets/")
    print(" Source: https://myfcd.moh.gov.my/myfcdindustri/")
    print(" Estimated time: 25-35 minutes")
    print("=" * 60)
    
    try:
        scraper = ProductionSeleniumScraper()
        
        # Ask for confirmation before full run
        print(" Ready to scrape all industry foods with improved data structure")
        print(" This will take 25-35 minutes. Press Ctrl+C to interrupt.")
        print()
        
        # Run full scraping
        scraper.scrape_all_foods(max_items=None)  # No limit = all foods
        
        print("\n" + "=" * 60)
        print(" Complete! All foods scraped with:")
        print(" Proper nutrient categories (Proximates, Minerals, etc.)")
        print(" Actual website-calculated serving size values")
        print(" Full nutrient data for all industry foods")
        
    except KeyboardInterrupt:
        print("\n  Scraping interrupted by user")
        print(" Partial results available in datasets folder")
        return 1
    except Exception as e:
        print(f"\n Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
