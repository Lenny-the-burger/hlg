#!/usr/bin/env python3
"""
Process wiki data files to remove the first line inside <doc> elements
and any empty newlines after it.
"""

import re
import os
from pathlib import Path
import xml.etree.ElementTree as ET


def process_file(filepath, out_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use regex to find and process each <doc> element
    def process_doc(match):
        opening_tag = match.group(1)  # The <doc ...> tag
        doc_content = match.group(2)   # Everything between <doc> and </doc>

        # Check if this is a disambiguation page - discard immediately
        if 'may refer to:' in doc_content:
            return ""

        # Split content into lines - note that after the opening tag there's a newline,
        # then the title line, then more content
        lines = doc_content.split('\n')

        # Skip the first non-empty line (title) and any empty lines after it
        new_lines = []
        first_line_skipped = False
        skip_empty = False

        for line in lines:
            # Skip first non-empty line (the title)
            if not first_line_skipped and line.strip():
                first_line_skipped = True
                skip_empty = True  # Now skip empty lines after title
                continue

            # Skip empty lines immediately after title
            if skip_empty and line.strip() == "":
                continue

            skip_empty = False
            new_lines.append(line)

        # if we have ended up with no lines, the element is pruned entirely
        if not any(line.strip() for line in new_lines):
            return ""

        # Reconstruct the doc element
        return f'{opening_tag}\n' + '\n'.join(new_lines) + '</doc>\n'

    # Process all <doc> elements
    output = re.sub(r'(<doc[^>]*>)(.*?)</doc>', process_doc, content, flags=re.DOTALL)

    # Remove extra newlines between doc elements
    output = re.sub(r'</doc>\n+<doc', '</doc>\n<doc', output)

    # Write back to file preserving subdirectory structure
    # Get the parent directory name (AA, AB, etc.)
    subdir_name = filepath.parent.name
    out_subdir = out_dir / subdir_name
    out_file = out_subdir / filepath.name

    # Ensure output subdirectory exists
    os.makedirs(out_subdir, exist_ok=True)

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Processed: {filepath}")


def main():
    """Process all wiki files in the current directory structure."""
    current_dir = Path('C:\\Users\\tednb\\source\\repos\\hlg\\data\\data-train\\text')
    out_dir = Path('C:\\Users\\tednb\\source\\repos\\hlg\\data\\data-train\\text-clean')

    # Find all directories (AA, AB, AC, etc.)
    directories = [d for d in current_dir.iterdir() if d.is_dir() and len(d.name) == 2]

    file_count = 0
    for directory in sorted(directories):
        # Process all files in each directory
        for filepath in sorted(directory.iterdir()):
            if filepath.is_file():
                process_file(filepath, out_dir)
                file_count += 1

    print(f"\nTotal files processed: {file_count}")


if __name__ == '__main__':
    main()
