#!/usr/bin/env python3
"""
GitHub Upload Preparation Script
=================================
This script helps prepare the Lo Shu Algorithm project for GitHub upload.
It replaces placeholder values with your actual information.

Usage:
    python setup_github.py
"""

import os
import re
import sys

def get_user_info():
    """Get user information for replacement."""
    print("=" * 60)
    print("GitHub Upload Preparation")
    print("=" * 60)
    print("\nPlease enter your information (press Enter to skip):")
    
    info = {
        'YOUR_USERNAME': input("\nGitHub Username (e.g., john-doe): ").strip(),
        'YourFirstName': input("Your First Name: ").strip(),
        'YourLastName': input("Your Last Name: ").strip(),
        'your.email@example.com': input("Your Email: ").strip(),
        'Your University/Organization': input("Your University/Organization: ").strip(),
        'YOUR_USERNAME/lo_shu_algorithm': input("GitHub Repository (default: username/lo_shu_algorithm): ").strip(),
    }
    
    # Use username for repository if not provided
    if not info['YOUR_USERNAME/lo_shu_algorithm'] and info['YOUR_USERNAME']:
        info['YOUR_USERNAME/lo_shu_algorithm'] = f"{info['YOUR_USERNAME']}/lo_shu_algorithm"
    
    return {k: v for k, v in info.items() if v}  # Remove empty values


def replace_in_file(filepath, replacements):
    """Replace text in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return False


def main():
    """Main function."""
    print("\nThis script will help you prepare the project for GitHub upload.")
    print("It will replace placeholder values with your actual information.\n")
    
    # Get user info
    replacements = get_user_info()
    
    if not replacements:
        print("\nNo replacements provided. Exiting.")
        sys.exit(0)
    
    print("\n" + "=" * 60)
    print("Replacements to be made:")
    print("=" * 60)
    for old, new in replacements.items():
        print(f"  {old} → {new}")
    
    confirm = input("\nProceed with replacements? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    # Files to process
    files_to_process = [
        'README.md',
        'CITATION.cff',
        'PROJECT_SUMMARY.md',
        '.github/workflows/ci.yml',
    ]
    
    # Add docs files
    docs_files = [
        'docs/ACADEMIC_PAPER.md',
    ]
    
    print("\n" + "=" * 60)
    print("Processing files...")
    print("=" * 60)
    
    modified_count = 0
    
    # Process root files
    for filename in files_to_process:
        if os.path.exists(filename):
            print(f"\nProcessing {filename}...")
            if replace_in_file(filename, replacements):
                print(f"  ✓ Modified")
                modified_count += 1
            else:
                print(f"  - No changes needed")
        else:
            print(f"  ⚠ File not found: {filename}")
    
    # Process docs files
    for filename in docs_files:
        if os.path.exists(filename):
            print(f"\nProcessing {filename}...")
            if replace_in_file(filename, replacements):
                print(f"  ✓ Modified")
                modified_count += 1
            else:
                print(f"  - No changes needed")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Files modified: {modified_count}")
    
    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("""
1. Initialize git repository:
   git init
   git add .
   git commit -m "Initial commit: Lo Shu Balance Algorithm v1.0.0"

2. Create GitHub repository:
   - Go to https://github.com/new
   - Repository name: lo_shu_algorithm
   - Description: A novel image denoising algorithm based on Lo Shu Magic Square
   - License: GNU AGPL v3.0
   - DO NOT initialize with README (we already have one)

3. Push to GitHub:
   git remote add origin https://github.com/YOUR_USERNAME/lo_shu_algorithm.git
   git branch -M main
   git push -u origin main

4. Enable GitHub Actions:
   - Go to repository Settings > Actions
   - Enable workflows

5. Optional - Create DOI:
   - Go to https://zenodo.org
   - Link your GitHub repository
   - Get DOI for CITATION.cff
""")
    
    print("\n✓ Setup complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
