#!/usr/bin/env python3
"""
Convert CET-4 vocabulary TXT file to CSV format for Notion import
"""
import csv
import sys

def convert_txt_to_csv(input_path, output_path):
    """Convert the vocabulary TXT file to a proper CSV format"""
    
    with open(input_path, 'r', encoding='utf-8') as txt_file:
        with open(output_path, 'w', encoding='utf-8', newline='') as csv_file:
            # Read all lines from txt file
            lines = txt_file.readlines()
            
            # Create CSV writer
            writer = csv.writer(csv_file)
            
            # Process each line
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # Split by comma, but be careful with commas in definitions
                parts = line.split(',', 2)  # Split into max 3 parts
                
                if len(parts) >= 3:
                    word = parts[0].strip()
                    pos = parts[1].strip()
                    definition = parts[2].strip()
                    
                    # Write to CSV
                    writer.writerow([word, pos, definition])
                elif len(parts) == 2:
                    # Some entries might not have definitions
                    word = parts[0].strip()
                    pos = parts[1].strip()
                    writer.writerow([word, pos, ''])
    
    return True

def main():
    input_file = '四级高频词汇.txt'
    output_file = '四级高频词汇.csv'
    
    print(f"Converting {input_file} to {output_file}...")
    
    try:
        convert_txt_to_csv(input_file, output_file)
        
        # Count entries in the output file
        with open(output_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for line in f)
        
        print(f"✓ Successfully converted {line_count} entries to CSV format")
        print(f"✓ Output file: {output_file}")
        
        # Show first few entries
        print("\nFirst 5 entries:")
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                if len(row) >= 3:
                    print(f"{i+1}. {row[0]} ({row[1]}) - {row[2]}")
                elif len(row) >= 2:
                    print(f"{i+1}. {row[0]} ({row[1]})")
        
        return 0
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
