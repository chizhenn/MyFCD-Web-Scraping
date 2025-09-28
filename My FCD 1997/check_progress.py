#!/usr/bin/env python3
"""
Simple progress monitor for MyFCD scraping
"""

import os
import json


def check_progress():
    """Check scraping progress"""
    
    data_dir = "/Users/ooichienzhen/Desktop/myFCD1997/datasets"
    
    if not os.path.exists(data_dir):
        print(" Datasets folder not found")
        return
    
    # Count JSON files
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    total_expected = 233
    completed = len(json_files)
    
    print(f" MyFCD Scraping Progress")
    print(f"=" * 40)
    print(f" Completed: {completed}/{total_expected} ({completed/total_expected*100:.1f}%)")
    
    if completed > 0:
        # Progress bar
        bar_length = 30
        filled_length = int(bar_length * completed / total_expected)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f" Progress: [{bar}] {completed/total_expected*100:.1f}%")
        
        # Quick quality check
        if completed >= 3:
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
    
    if completed >= total_expected:
        print(f"\n Scraping COMPLETE!")
    elif completed > 0:
        print(f"\n  Scraping in progress...")
    else:
        print(f"\n Scraping not started")


if __name__ == "__main__":
    check_progress()