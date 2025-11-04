#!/usr/bin/env python3
"""
Combine all wiki files from subdirectories into a single flat directory,
renumbering them sequentially (000, 001, 002, etc.)
"""

import os
from pathlib import Path
import shutil


def main():
    """Combine all files from text-clean subdirectories into one directory."""
    source_dir = Path('C:\\Users\\tednb\\source\\repos\\hlg\\data\\data-train\\text-clean')
    output_dir = Path('C:\\Users\\tednb\\source\\repos\\hlg\\data\\data-train\\text-combined')

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Find all subdirectories (AA, AB, AC, etc.)
    subdirs = sorted([d for d in source_dir.iterdir() if d.is_dir() and len(d.name) == 2])

    file_counter = 0
    total_files = 0

    # First, count total files to determine padding
    for subdir in subdirs:
        total_files += len([f for f in subdir.iterdir() if f.is_file()])

    # Determine number of digits needed for padding
    num_digits = len(str(total_files - 1))

    # Process all files from all subdirectories
    for subdir in subdirs:
        files = sorted([f for f in subdir.iterdir() if f.is_file()])

        for filepath in files:
            # Create new filename with sequential numbering
            new_filename = f"wiki_{str(file_counter).zfill(num_digits)}.txt"
            new_filepath = output_dir / new_filename

            # Copy file to new location
            shutil.copy2(filepath, new_filepath)

            file_counter += 1

            if file_counter % 100 == 0:
                print(f"Processed {file_counter}/{total_files} files...")

    print(f"\nComplete! Combined {file_counter} files into {output_dir}")
    print(f"Files numbered from wiki_{'0' * num_digits} to wiki_{str(file_counter - 1).zfill(num_digits)}")


if __name__ == '__main__':
    main()
