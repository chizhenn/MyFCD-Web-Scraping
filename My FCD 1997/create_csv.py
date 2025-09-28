#!/usr/bin/env python3
"""
Essential CSV converter for MyFCD JSON files
Creates CSV with JSON arrays for nutrients by category
"""

import json
import pandas as pd
import os
from typing import Dict, List, Any

def create_csv_row(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create CSV row with JSON arrays for nutrients by category"""
    
    # Basic food information
    row = {
        'NDB_No': data.get('NDB No', ''),
        'Description': data.get('Description', ''),
        'Food_Group': data.get('Food Group', ''),
        'Image': data.get('Image', ''),
        'Source': data.get('Source', ''),
        'Published_Date': data.get('Published Date', '')
    }
    
    # Process nutrients by category
    nutrients = data.get('Nutrient', [])
    current_category = None
    category_counter = 1
    
    for nutrient_entry in nutrients:
        # Check if this is a category header
        if 'category' in nutrient_entry and 'name' not in nutrient_entry:
            current_category = nutrient_entry['category']
            
            # Create columns for this category
            category_col = f"Category_{category_counter}"
            nutrients_col = f"Nutrients_{category_counter}"
            
            row[category_col] = current_category
            
            # Collect all nutrients for this category
            category_nutrients = []
            
            # Look ahead to find all nutrients in this category
            start_collecting = False
            for next_entry in nutrients:
                if next_entry == nutrient_entry:
                    start_collecting = True
                    continue
                
                if start_collecting:
                    # Stop if we hit another category
                    if 'category' in next_entry and 'name' not in next_entry:
                        break
                    
                    # Add nutrient if it has a name
                    if 'name' in next_entry:
                        category_nutrients.append(next_entry)
            
            # Store nutrients as JSON string
            row[nutrients_col] = json.dumps(category_nutrients, ensure_ascii=False)
            category_counter += 1
    
    return row

def convert_all_json_to_csv(datasets_dir: str = "/Users/ooichienzhen/Desktop/myFCD1997/datasets") -> None:
    """Convert all JSON files to one comprehensive CSV"""
    
    print("Creating CSV from JSON files...")
    
    # Get all JSON files
    json_files = [f for f in os.listdir(datasets_dir) if f.endswith('.json') and not f.startswith('summary')]
    
    if not json_files:
        print("ERROR: No JSON files found!")
        return
    
    print(f"Found {len(json_files)} JSON files")
    
    # Process all files
    all_rows = []
    processed = 0
    
    for json_file in sorted(json_files):
        json_path = os.path.join(datasets_dir, json_file)
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            row = create_csv_row(data)
            all_rows.append(row)
            processed += 1
            
            if processed % 50 == 0:
                print(f"Processed {processed}/{len(json_files)} files...")
        
        except Exception as e:
            print(f"ERROR processing {json_file}: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(all_rows)
    
    # Save CSV
    csv_path = os.path.join(datasets_dir, "myfcd_complete.csv")
    df.to_csv(csv_path, index=False)
    
    print(f"SUCCESS: CSV created!")
    print(f"File: {csv_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    
    return csv_path

def main():
    """Convert all JSON files to CSV"""
    try:
        csv_path = convert_all_json_to_csv()
        
        print(f"\nCSV conversion completed!")
        print(f"Use: pandas.read_csv('myfcd_complete.csv')")
        print(f"Parse JSON arrays: json.loads(csv_row['Nutrients_1'])")
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())