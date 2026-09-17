#!/usr/bin/env python3
"""
Happy Greenery - Multi-Site Plant Data Scraper
==============================================
Scrapes high-ranking, top-rated plant & gardening websites for a given blog title/topic.
Stores full text content (headings, paragraphs, lists, specs) and media URLs ONLY (images, PDFs, 3D models).

Target Region: Bengaluru / India / Global Top Authorities
"""

import os
import sys
import re
import json
import time
import argparse
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from generate_manifest import generate_manifest

# Ensure standard output handles UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

AUTHORITY_DOMAINS = [
    "ugaoo.com", "nurserylive.com", "balconygardenweb.com", "mybageecha.com",
    "thespruce.com", "gardeningknowhow.com", "epicgardening.com", "plantify.co.za",
    "housing.com", "architecturaldigest.in", "naturebring.com", "flourishplant.com",
    "houseplantsexpert.com", "plantcaretoday.com", "apartmenttherapy.com",
    "rollingnature.com", "greendna.in", "gardeningtips.in", "plantssparkjoy.com",
    "urbanmali.com"
]

DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
]

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def fetch_search_results(query: str, num_results: int = 20) -> list:
    print(f"\n[SEARCH] Searching top {num_results} authoritative websites for: '{query}'...")
    urls = []
    
    headers = {"User-Agent": DEFAULT_USER_AGENTS[0]}
    search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query + ' plant care guide bengaluru india')}"
    
    try:
        resp = requests.post(search_url, data={"q": query}, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            results = soup.find_all("a", class_="result__url")
            for r in results:
                href = r.get("href", "").strip()
                if href and href.startswith("http"):
                    domain = urlparse(href).netloc.lower()
                    if not any(ignored in domain for ignored in ["youtube.com", "facebook.com", "pinterest.com", "instagram.com", "reddit.com"]):
                        if href not in urls:
                            urls.append(href)
                if len(urls) >= num_results:
                    break
    except Exception as e:
        print(f"[NOTE] Search engine query notice: {e}")

    if len(urls) < 5:
        print("[INFO] Augmenting search results from known top authority plant domains...")
        encoded = requests.utils.quote(query)
        fallback_seeds = [
            f"https://www.ugaoo.com/blogs/green-lifestyle/search?q={encoded}",
            f"https://nurserylive.com/search?q={encoded}",
            f"https://balconygardenweb.com/?s={encoded}",
            f"https://www.thespruce.com/search?q={encoded}",
            f"https://www.gardeningknowhow.com/search?q={encoded}",
            f"https://mybageecha.com/search?q={encoded}"
        ]
        for seed in fallback_seeds:
            if seed not in urls and len(urls) < num_results:
                urls.append(seed)

    print(f"[SUCCESS] Found {len(urls)} target URLs to scrape.\n")
    return urls

def scrape_single_url(url: str) -> dict:
    domain = urlparse(url).netloc.replace("www.", "")
    result = {
        "url": url,
        "domain": domain,
        "site_title": "",
        "meta_description": "",
        "is_authority_domain": any(auth in domain for auth in AUTHORITY_DOMAINS),
        "headings": [],
        "paragraphs": [],
        "list_items": [],
        "media": {
            "images": [],
            "pdfs": [],
            "models_3d": [],
            "videos": []
        },
        "success": False,
        "error": None
    }
    
    headers = {"User-Agent": DEFAULT_USER_AGENTS[0]}
    
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result
        
        soup = BeautifulSoup(resp.content, "html.parser")
        
        title_tag = soup.find("title")
        result["site_title"] = title_tag.get_text(strip=True) if title_tag else domain
        
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc and meta_desc.get("content"):
            result["meta_description"] = meta_desc["content"].strip()
            
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            element.decompose()
            
        for h in soup.find_all(["h1", "h2", "h3", "h4"]):
            text = h.get_text(strip=True)
            if text and len(text) > 3:
                result["headings"].append({"level": h.name, "text": text})
                
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text and len(text) > 35:
                result["paragraphs"].append(text)

        for li in soup.find_all("li"):
            text = li.get_text(strip=True)
            if text and len(text) > 15 and len(text) < 300:
                result["list_items"].append(text)
                
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if src:
                full_url = urljoin(url, src)
                alt = img.get("alt", "").strip() or "Plant care image"
                if full_url.startswith("http") and not any(ext in full_url.lower() for ext in [".svg", "icon", "logo", "avatar"]):
                    result["media"]["images"].append({
                        "url": full_url,
                        "alt": alt
                    })
                    
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                full_url = urljoin(url, href)
                result["media"]["pdfs"].append({
                    "url": full_url,
                    "title": a.get_text(strip=True) or "Plant Care PDF Guide"
                })
                
        for link in soup.find_all(["a", "source"], href=True):
            href = link.get("href") or link.get("src", "")
            if any(href.lower().endswith(ext) for ext in [".glb", ".gltf", ".usdz"]):
                full_url = urljoin(url, href)
                result["media"]["models_3d"].append({
                    "url": full_url,
                    "type": href.split(".")[-1].upper()
                })
                
        for iframe in soup.find_all("iframe"):
            src = iframe.get("src", "")
            if "youtube.com" in src or "vimeo.com" in src:
                result["media"]["videos"].append({"url": urljoin(url, src)})
                
        result["success"] = True
    except Exception as e:
        result["error"] = str(e)
        
    return result

def generate_blog_payload(title: str, scraped_results: list) -> dict:
    slug = slugify(title)
    sections = []
    
    sections.append({
        "type": "paragraph",
        "value": f"{title} is a complete, expert-backed guide for urban gardeners, apartment dwellers, and plant enthusiasts in Bengaluru and South India. Below is a structured synthesis of care instructions, light needs, watering routines, and species details compiled from top-ranking plant authorities."
    })
    
    image_pool = []
    for site in scraped_results:
        if not site["success"]:
            continue
            
        for img in site["media"]["images"]:
            if img["url"] not in [i["value"] for i in image_pool]:
                image_pool.append({"type": "image", "value": img["url"], "alt": img["alt"]})
                
        if site["headings"]:
            top_h2 = next((h["text"] for h in site["headings"] if h["level"] == "h2"), None)
            if top_h2:
                sections.append({"type": "h2", "value": f"{top_h2} (Key Guidance from {site['domain']})"})
                
        p_count = 0
        for p in site["paragraphs"]:
            if len(p) > 60 and p_count < 2:
                sections.append({"type": "paragraph", "value": p})
                p_count += 1
                
        if image_pool and len(sections) % 4 == 0:
            sections.append(image_pool.pop(0))
            
    meta_description = f"Complete guide to {title.lower()}. Learn top care tips, watering routines, lighting requirements, and balcony setup for Bengaluru homes."
    
    payload = {
        "title": title,
        "slug": slug,
        "sections": sections,
        "metaDescription": meta_description,
        "canonicalUrl": f"https://www.happygreenery.in/blog/{slug}",
        "ogTitle": title,
        "ogDescription": meta_description,
        "ogImage": image_pool[0]["value"] if image_pool else "https://www.happygreenery.in/placeholder.jpg",
        "twitterTitle": title,
        "twitterDescription": meta_description,
        "twitterImage": image_pool[0]["value"] if image_pool else "https://www.happygreenery.in/placeholder.jpg"
    }
    
    return payload

def main():
    parser = argparse.ArgumentParser(description="Happy Greenery Multi-Site Plant Data Scraper")
    parser.add_argument("--title", type=str, help="Blog title or plant category/topic to scrape")
    args = parser.parse_args()
    
    blog_title = args.title
    if not blog_title:
        print("[INIT] Welcome to Happy Greenery Plant Data Scraper!")
        blog_title = input("Enter the Blog Title / Plant Topic to scrape: ").strip()
        
    if not blog_title:
        print("[ERROR] No blog title provided. Exiting.")
        sys.exit(1)
        
    slug = slugify(blog_title)
    
    base_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
    os.makedirs(base_out, exist_ok=True)
    output_dir = os.path.join(base_out, slug)
    os.makedirs(output_dir, exist_ok=True)
    
    print("=======================================================")
    print(f"[SCRAPING TOPIC] '{blog_title}'")
    print(f"[OUTPUT DIR] {output_dir}")
    print("=======================================================\n")
    
    urls = fetch_search_results(blog_title, num_results=20)
    
    scraped_data = []
    site_sources = []
    
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Scraping: {url} ...")
        res = scrape_single_url(url)
        scraped_data.append(res)
        
        site_sources.append({
            "rank": idx,
            "url": res["url"],
            "domain": res["domain"],
            "site_title": res["site_title"],
            "is_authority": res["is_authority_domain"],
            "status": "Success" if res["success"] else f"Failed: {res['error']}",
            "headings_count": len(res["headings"]),
            "paragraphs_count": len(res["paragraphs"]),
            "list_items_count": len(res["list_items"]),
            "images_urls_count": len(res["media"]["images"]),
            "pdfs_urls_count": len(res["media"]["pdfs"]),
            "models_3d_urls_count": len(res["media"]["models_3d"])
        })
        time.sleep(0.3)
        
    sources_path = os.path.join(output_dir, "site_sources.json")
    with open(sources_path, "w", encoding="utf-8") as f:
        json.dump(site_sources, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVE] Saved website sources metadata to: {sources_path}")
    
    raw_content_path = os.path.join(output_dir, "raw_content.json")
    with open(raw_content_path, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    print(f"[SAVE] Saved raw content & media URLs to: {raw_content_path}")
    
    brief_path = os.path.join(output_dir, "blog_research_brief.md")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(f"# Research Brief: {blog_title}\n\n")
        f.write(f"- **Target Region**: Bengaluru / India & Global Plant Authorities\n")
        f.write(f"- **Scraped Sources**: {len(scraped_data)} websites\n")
        f.write(f"- **Generated Slug**: `{slug}`\n\n")
        f.write("--- \n\n## Scraped Website Sources & Ratings\n\n")
        for s in site_sources:
            auth_badge = "(Authority Site)" if s["is_authority"] else ""
            f.write(f"### {s['rank']}. [{s['site_title']}]({s['url']}) {auth_badge}\n")
            f.write(f"- **Domain**: `{s['domain']}`\n")
            f.write(f"- **Extracted Headings**: {s['headings_count']} | **Paragraphs**: {s['paragraphs_count']} | **Lists**: {s['list_items_count']}\n")
            f.write(f"- **Media URLs Found**: Images: {s['images_urls_count']} | PDFs: {s['pdfs_urls_count']} | 3D Models: {s['models_3d_urls_count']}\n\n")
            
        f.write("---\n\n## Extracted Media URLs Sample (No Binary Downloads)\n\n")
        for site in scraped_data:
            if site["media"]["images"]:
                f.write(f"#### Images from `{site['domain']}`:\n")
                for img in site["media"]["images"][:5]:
                    f.write(f"- **URL**: {img['url']}\n  - **Alt**: _{img['alt']}_\n")
                f.write("\n")
                
    print(f"[SAVE] Saved consolidated research brief to: {brief_path}")
    
    payload = generate_blog_payload(blog_title, scraped_data)
    payload_path = os.path.join(output_dir, "content_payload.json")
    with open(payload_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[SAVE] Saved Happy Greenery Backend-Ready JSON Payload to: {payload_path}")
    
    # Auto-generate manifest.json for React UI
    generate_manifest()
    
    print("\n=======================================================")
    print("[COMPLETE] Scraping and data structuring completed successfully!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
