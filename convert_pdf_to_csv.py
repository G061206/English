#!/usr/bin/env python3
"""
Convert CET-4 vocabulary PDF to CSV format
"""
import pdfplumber
import csv
import re
import sys
import argparse

def extract_vocabulary_from_pdf(pdf_path):
    """Extract vocabulary entries from PDF"""
    all_text = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    
    # Join all pages
    full_text = "\n".join(all_text)
    
    return full_text

def parse_vocabulary(text):
    """Parse vocabulary entries from text"""
    vocabulary = []
    seen_words = set()  # Track seen words to avoid duplicates
    
    # Pattern to match vocabulary entries more precisely
    # Components:
    # 1. Word: English letters, may include parentheses for variants like "cigaret(te)"
    # 2. Part of speech: Common abbreviations (n, v, a, vi, vt, ad, prep, conj, etc.)
    # 3. Definition: Non-English characters (Chinese text and punctuation)
    # Lookahead ensures we stop at the next word entry
    pattern = (
        r'([a-zA-Z]+(?:\([a-zA-Z]+\))?)'  # Word
        r'\s*(n|v|a|vi|vt|ad|prep|conj|pron|num|int|aux)'  # Part of speech
        r'[\.．]\s*'  # Separator (dot)
        r'([^a-zA-Z]+?)'  # Definition
        r'(?=\s*[a-zA-Z]+\s*(?:n|v|a|vi|vt|ad|prep|conj|pron|num|int|aux)[\.．]|\s*$)'  # Lookahead
    )
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        word = match[0].strip()
        pos = match[1].strip() + '.'
        definition = match[2].strip()
        
        # Skip single letter words that are section headers
        if len(word) == 1 and word.upper() == word:
            continue
        
        # Remove "A " prefix if present (section header)
        if word.startswith('A '):
            word = word[2:]
        
        # Skip if word is too short or clearly not valid
        if len(word) < 2:
            continue
        
        # Skip entries with numbers in the word
        if any(c.isdigit() for c in word):
            continue
        
        # Clean up the definition
        # Remove newlines and excessive whitespace
        definition = re.sub(r'\s+', ' ', definition)
        definition = definition.strip()
        
        # Remove trailing punctuation and incomplete fragments
        definition = re.sub(r'[；，。、\s]+$', '', definition)
        
        # Remove trailing fragments from two-column layout
        # These are common incomplete phrases that appear due to PDF layout extraction
        # General approach: remove space + 1-3 trailing Chinese characters that likely don't complete the meaning
        definition = re.sub(r'\s+[\u4e00-\u9fff]{1,3}$', '', definition)
        
        # Only add if definition is not empty and contains Chinese characters
        if definition and re.search(r'[\u4e00-\u9fff]', definition):
            # Avoid duplicates
            word_lower = word.lower()
            if word_lower not in seen_words:
                seen_words.add(word_lower)
                vocabulary.append({
                    'word': word,
                    'part_of_speech': pos,
                    'definition': definition
                })
    
    return vocabulary

def save_to_csv(vocabulary, output_path):
    """Save vocabulary to CSV file"""
    with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['word', 'part_of_speech', 'definition']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in vocabulary:
            writer.writerow(entry)

def main():
    parser = argparse.ArgumentParser(
        description='Convert CET-4 vocabulary PDF to CSV format'
    )
    parser.add_argument(
        '-i', '--input',
        default='四级高频词汇.pdf',
        help='Input PDF file path (default: 四级高频词汇.pdf)'
    )
    parser.add_argument(
        '-o', '--output',
        default='四级高频词汇.csv',
        help='Output CSV file path (default: 四级高频词汇.csv)'
    )
    
    args = parser.parse_args()
    
    pdf_path = args.input
    output_path = args.output
    
    print(f"Reading PDF: {pdf_path}")
    try:
        text = extract_vocabulary_from_pdf(pdf_path)
    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    
    print(f"Parsing vocabulary...")
    vocabulary = parse_vocabulary(text)
    
    print(f"Found {len(vocabulary)} vocabulary entries")
    
    print(f"Saving to CSV: {output_path}")
    try:
        save_to_csv(vocabulary, output_path)
    except Exception as e:
        print(f"Error saving CSV: {e}")
        sys.exit(1)
    
    print(f"Done! CSV file created with {len(vocabulary)} entries")
    
    # Show first few entries
    print("\nFirst 5 entries:")
    for i, entry in enumerate(vocabulary[:5], 1):
        print(f"{i}. {entry['word']} ({entry['part_of_speech']}) - {entry['definition']}")

if __name__ == "__main__":
    main()
