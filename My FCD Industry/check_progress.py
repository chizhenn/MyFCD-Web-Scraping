#!/usr/bin/env python3
"""
Simple progress monitor for MyFCD Industry scraping
"""

import os
import json


def check_progress():
    """Check scraping progress"""
    
    data_dir = "/Users/ooichienzhen/Desktop/myFCD_Industry/datasets"
    
    if not os.path.exists(data_dir):
        print(" Datasets folder not found")
        return
    
    # Count JSON files
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    print(f" MyFCD Industry Scraping Progress")
    print(f"=" * 40)
    print(f" Completed: {len(json_files)} files")
    
    if len(json_files) > 0:
        # Progress bar (estimated based on typical industry DB size)
        estimated_total = 500  # Estimate for industry database
        bar_length = 30
        filled_length = min(int(bar_length * len(json_files) / estimated_total), bar_length)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        progress_pct = min(len(json_files) / estimated_total * 100, 100)
        print(f" Progress: [{bar}] {progress_pct:.1f}%")
        
        # Quick quality check
        if len(json_files) >= 3:
            recent_files = sorted(json_files)[-3:]
            print(f"\n Recent files check:")
            
            for filename in recent_files:
                try:
                    filepath = os.path.join(data_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    nutrients = data.get('Nutrient', [])
                    categories = len(set([n.get('category') for n in nutrients if n.get('category')]))
                    nutrient_count = len([n for n in nutrients if n.get('name')])
                    
                    print(f"   {filename[:12]}: {categories} categories, {nutrient_count} nutrients")
                    
                except Exception as e:
                    print(f"  ⚠ Error checking {filename}: {e}")
    
    if len(json_files) == 0:
        print(f"\n Scraping not started")
        print(f" Run: python scrape_all_foods.py")
    else:
        print(f"\n Scraping in progress...")
        print(f" {len(json_files)} industry foods processed so far")


if __name__ == "__main__":
    check_progress()
