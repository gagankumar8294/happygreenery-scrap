#!/usr/bin/env python3
"""
Happy Greenery - Scraped Topics Manifest Generator
==================================================
Scans outputs/ directory and generates outputs/manifest.json for static React UI consumption.
"""

import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

def generate_manifest():
    topics = []
    if not os.path.exists(OUTPUTS_DIR):
        print("[ERROR] outputs directory not found.")
        return

    for item in os.listdir(OUTPUTS_DIR):
        if item == "manifest.json":
            continue
            
        folder_path = os.path.join(OUTPUTS_DIR, item)
        if os.path.isdir(folder_path):
            sources_file = os.path.join(folder_path, "site_sources.json")
            payload_file = os.path.join(folder_path, "content_payload.json")
            
            site_count = 0
            title = item.replace("-", " ").title()
            media_count = 0
            
            if os.path.exists(sources_file):
                try:
                    with open(sources_file, "r", encoding="utf-8") as f:
                        sources = json.load(f)
                        site_count = len(sources)
                        for s in sources:
                            media_count += s.get("images_urls_count", 0) + s.get("pdfs_urls_count", 0) + s.get("models_3d_urls_count", 0)
                except Exception:
                    pass
                    
            if os.path.exists(payload_file):
                try:
                    with open(payload_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        title = data.get("title", title)
                except Exception:
                    pass

            topics.append({
                "slug": item,
                "title": title,
                "site_count": site_count,
                "media_count": media_count
            })

    topics.sort(key=lambda x: x["slug"])
    
    manifest_path = os.path.join(OUTPUTS_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)
        
    print(f"[SUCCESS] Generated manifest.json with {len(topics)} topic records at: {manifest_path}")

if __name__ == "__main__":
    generate_manifest()
