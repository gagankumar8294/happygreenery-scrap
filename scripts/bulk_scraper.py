#!/usr/bin/env python3
"""
Happy Greenery - Bulk Topics Scraper
====================================
Scrapes a list of multiple plant titles sequentially and updates manifest.json.
"""

import sys
import subprocess
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TOPICS = [
    "Plants for modern villa landscaping",
    "Ground covers that replace grass at Indian condition",
    "Ornamental trees for terrace garden",
    "Fast growing privacy plants",
    "Plants for hospitals",
    "Vertical garden plants"
]

def main():
    script_path = os.path.join(os.path.dirname(__file__), "scraper.py")
    total = len(TOPICS)
    
    print(f"🚀 Starting Bulk Scraping for {total} topics...\n")
    
    for idx, title in enumerate(TOPICS, 1):
        print(f"=======================================================")
        print(f"[{idx}/{total}] Scraping Topic: '{title}'")
        print(f"=======================================================")
        try:
            subprocess.run([sys.executable, script_path, "--title", title], check=True)
            print(f"✅ Completed topic [{idx}/{total}]: '{title}'\n")
        except Exception as e:
            print(f"❌ Error scraping '{title}': {e}\n")
            
    print("\n🎉 Bulk scraping for all 6 topics finished!")

if __name__ == "__main__":
    main()
