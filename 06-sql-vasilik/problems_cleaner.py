"""
Script to clean text copied from Apple Books.
Removes quotes around problem descriptions and "Excerpt From..." attribution.
Formats the output with proper line wrapping.
"""

import re
import textwrap


def wrap_text(text, width=80):
    """
    Wrap text to specified width while preserving paragraph structure.
    
    Args:
        text: Text to wrap
        width: Maximum line width (default 80)
        
    Returns:
        Wrapped text
    """
    # First, normalize the text: replace multiple spaces with single space
    # and join everything into one paragraph
    text = ' '.join(text.split())
    
    # Now wrap to the specified width
    wrapped = textwrap.fill(text, width=width)
    
    return wrapped


def clean_apple_books_text(text):
    """
    Clean text copied from Apple Books.
    
    Args:
        text: Raw text from Apple Books
        
    Returns:
        Cleaned text with quotes and attribution removed, properly formatted
    """
    # Remove the "Excerpt From..." section (from "Excerpt From" to end)
    text = re.sub(
        r'Excerpt From.*?This material may be protected by copyright\.',
        '',
        text,
        flags=re.DOTALL
    )
    
    # Remove smart quotes (curly quotes) around the problem description
    # Apple Books uses UTF-8 smart quotes: " (U+201C) and " (U+201D)
    text = text.replace('\u201c', '').replace('\u201d', '')
    
    # Also remove regular straight quotes in case they're used
    text = text.replace('"', '')
    
    # Strip whitespace from the entire text
    text = text.strip()
    
    # Split into title and content
    lines = text.split('\n', 1)
    
    if len(lines) == 1:
        # Only title, no content
        return lines[0].strip()
    
    title = lines[0].strip()
    content = lines[1].strip()
    
    # Ensure title format: number. Title (with single space after dot)
    # Match pattern like "22. Title" or "22.Title" or "22 .Title"
    title = re.sub(r'^(\d+)\s*\.\s*', r'\1. ', title)
    
    # Wrap content to 80 characters
    wrapped_content = wrap_text(content, width=80)
    
    # Combine title and wrapped content
    return f"{title}\n{wrapped_content}"


def main():
    """Read from problems_raw.txt and write cleaned text to problems_clean.txt"""
    
    # Read the raw file
    with open('problems_raw.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    # Clean the text
    cleaned_text = clean_apple_books_text(raw_text)
    
    # Write to clean file
    with open('problems_clean.txt', 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    
    print("✓ Text cleaned successfully!")
    print(f"\nCleaned text:\n{cleaned_text}")


if __name__ == '__main__':
    main()
