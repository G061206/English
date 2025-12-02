#!/usr/bin/env python3
"""
Convert CET-4 vocabulary PDF to CSV format
"""
import pdfplumber
import csv
import re

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
    # Word + part of speech + definition (Chinese characters, punctuation)
    # Looking ahead to the next word entry or end of string
    pattern = r'([a-zA-Z]+(?:\([a-zA-Z]+\))?)\s*(n|v|a|vi|vt|ad|prep|conj|pron|num|int|aux)[\.．]\s*([^a-zA-Z]+?)(?=\s*[a-zA-Z]+\s*(?:n|v|a|vi|vt|ad|prep|conj|pron|num|int|aux)[\.．]|\s*$)'
    
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
        
        # Remove common incomplete Chinese fragments at the end
        # These are often from the two-column layout split
        # Remove trailing fragments that don't form complete meanings
        incomplete_patterns = [
            r'\s+的$', r'\s+心的$', r'\s+近$', r'\s+奏$', 
            r'\s+援助$', r'\s+文摘$', r'\s+兼并$', r'\s+爱好者$',
            r'\s+报警；使惊慌$', r'\s+失$', r'\s+[一二三四五六七八九十]$',
            r'\s+国公司$', r'\s+国$', r'\s+公司$', r'\s+企业$',
            r'\s+人$', r'\s+物$', r'\s+事$', r'\s+处$'
        ]
        for pattern_str in incomplete_patterns:
            definition = re.sub(pattern_str, '', definition)
        
        # If definition ends with a space followed by 1-3 Chinese characters, it's likely a fragment
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
    pdf_path = "四级高频词汇.pdf"
    output_path = "四级高频词汇.csv"
    
    print(f"Reading PDF: {pdf_path}")
    text = extract_vocabulary_from_pdf(pdf_path)
    
    print(f"Parsing vocabulary...")
    vocabulary = parse_vocabulary(text)
    
    print(f"Found {len(vocabulary)} vocabulary entries")
    
    print(f"Saving to CSV: {output_path}")
    save_to_csv(vocabulary, output_path)
    
    print(f"Done! CSV file created with {len(vocabulary)} entries")
    
    # Show first few entries
    print("\nFirst 5 entries:")
    for i, entry in enumerate(vocabulary[:5], 1):
        print(f"{i}. {entry['word']} ({entry['part_of_speech']}) - {entry['definition']}")

if __name__ == "__main__":
    main()
