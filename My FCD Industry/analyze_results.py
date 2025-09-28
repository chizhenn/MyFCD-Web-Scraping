#!/usr/bin/env python3
"""
Analyze the scraped MyFCD Industry data and generate a summary
"""

import json
import os
import time
from collections import defaultdict, Counter
from typing import Dict, List


def analyze_scraped_data(data_dir: str = "/Users/ooichienzhen/Desktop/myFCD_Industry/datasets"):
    """Analyze the scraped JSON files and generate summary statistics"""
    
    print(" Analyzing scraped MyFCD Industry data...")
    print(f" Directory: {data_dir}")
    
    # Find all JSON files
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json') and not f.startswith('summary')]
    
    if not json_files:
        print("No JSON files found!")
        return
    
    print(f" Found {len(json_files)} JSON files")
    
    # Statistics
    stats = {
        'total_files': len(json_files),
        'successful_scrapes': 0,
        'with_images': 0,
        'with_source': 0,
        'with_published_date': 0,
        'total_nutrients': 0,
        'food_groups': Counter(),
        'nutrients_by_food': [],
        'serving_sizes': Counter(),
        'files_with_serving_sizes': 0
    }
    
    all_nutrients = set()
    problems = []
    
    # Process each file
    for filename in json_files:
        filepath = os.path.join(data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats['successful_scrapes'] += 1
            
            # Check completeness
            if data.get('Image'):
                stats['with_images'] += 1
            if data.get('Source'):
                stats['with_source'] += 1
            if data.get('Published Date'):
                stats['with_published_date'] += 1
            
            # Food group
            food_group = data.get('Food Group', 'Unknown')
            stats['food_groups'][food_group] += 1
            
            # Nutrients
            nutrients = data.get('Nutrient', [])
            nutrient_count = len([n for n in nutrients if n.get('name') and not n.get('name').lower() in ['proximates', 'minerals', 'vitamins']])
            stats['nutrients_by_food'].append(nutrient_count)
            stats['total_nutrients'] += nutrient_count
            
            # Track unique nutrients
            for nutrient in nutrients:
                if nutrient.get('name'):
                    all_nutrients.add(nutrient['name'])
            
            # Check for serving sizes
            has_serving_sizes = False
            for nutrient in nutrients:
                for key in nutrient.keys():
                    if 'piece' in key.lower() or 'cup' in key.lower() or 'slice' in key.lower():
                        has_serving_sizes = True
                        stats['serving_sizes'][key] += 1
            
            if has_serving_sizes:
                stats['files_with_serving_sizes'] += 1
                
        except Exception as e:
            problems.append(f"Error processing {filename}: {e}")
    
    # Generate summary
    print("\n" + "="*60)
    print(" SCRAPING SUMMARY - MyFCD Industry")
    print("="*60)
    
    print(f" Total files processed: {stats['total_files']}")
    print(f" Successful scrapes: {stats['successful_scrapes']}")
    print(f" Files with images: {stats['with_images']} ({stats['with_images']/stats['successful_scrapes']*100:.1f}%)")
    print(f" Files with source: {stats['with_source']} ({stats['with_source']/stats['successful_scrapes']*100:.1f}%)")
    print(f" Files with published date: {stats['with_published_date']} ({stats['with_published_date']/stats['successful_scrapes']*100:.1f}%)")
    print(f" Files with serving sizes: {stats['files_with_serving_sizes']} ({stats['files_with_serving_sizes']/stats['successful_scrapes']*100:.1f}%)")
    
    print(f"\n Total unique nutrients: {len(all_nutrients)}")
    print(f" Total nutrient entries: {stats['total_nutrients']}")
    if stats['nutrients_by_food']:
        avg_nutrients = sum(stats['nutrients_by_food']) / len(stats['nutrients_by_food'])
        print(f" Average nutrients per food: {avg_nutrients:.1f}")
    
    print(f"\n Food Groups Distribution:")
    for food_group, count in stats['food_groups'].most_common():
        percentage = count / stats['successful_scrapes'] * 100
        print(f"  • {food_group}: {count} items ({percentage:.1f}%)")
    
    if stats['serving_sizes']:
        print(f"\n Common Serving Sizes:")
        for serving_size, count in stats['serving_sizes'].most_common(10):
            print(f"  • {serving_size}: {count} occurrences")
    
    if problems:
        print(f"\n Problems encountered:")
        for problem in problems[:10]:  # Show first 10 problems
            print(f"  • {problem}")
        if len(problems) > 10:
            print(f"  ... and {len(problems) - 10} more problems")
    
    # Save summary to file
    summary_data = {
        'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'database_type': 'MyFCD Industry',
        'source_url': 'https://myfcd.moh.gov.my/myfcdindustri/',
        'statistics': stats,
        'unique_nutrients': sorted(list(all_nutrients)),
        'problems': problems
    }
    
    summary_file = os.path.join(data_dir, 'summary_analysis.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n Detailed analysis saved to: summary_analysis.json")
    print("="*60)


if __name__ == "__main__":
    analyze_scraped_data()
