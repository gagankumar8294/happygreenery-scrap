#!/usr/bin/env python3
"""
Happy Greenery - Scraped Data Viewer & Dashboard Server
======================================================
FastAPI application configured for local execution & 1-click Vercel Serverless deployment.
Serves an interactive 3-column dashboard for viewing, exploring, and managing scraped plant data.
"""

import os
import sys
import json
import subprocess
from typing import Optional
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, Response

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Calculate ROOT_DIR reliably whether run directly or imported from api/index.py on Vercel
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(CURRENT_DIR) == "api":
    ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
else:
    ROOT_DIR = CURRENT_DIR

PRIMARY_OUTPUTS_DIR = os.path.join(ROOT_DIR, "outputs")
TMP_OUTPUTS_DIR = "/tmp/outputs" if os.name != "nt" else os.path.join(ROOT_DIR, "outputs")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
INDEX_HTML_PATH = os.path.join(TEMPLATES_DIR, "index.html")

os.makedirs(PRIMARY_OUTPUTS_DIR, exist_ok=True)
if os.name != "nt":
    os.makedirs(TMP_OUTPUTS_DIR, exist_ok=True)

app = FastAPI(title="Happy Greenery Scraped Data Viewer")

def load_index_html():
    if os.path.exists(INDEX_HTML_PATH):
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Happy Greenery Viewer Dashboard</h1><p>index.html template not found.</p>"

def get_all_topics():
    topics = []
    seen_slugs = set()
    
    target_dirs = [PRIMARY_OUTPUTS_DIR]
    if os.path.exists(TMP_OUTPUTS_DIR) and TMP_OUTPUTS_DIR != PRIMARY_OUTPUTS_DIR:
        target_dirs.append(TMP_OUTPUTS_DIR)
        
    for out_dir in target_dirs:
        if not os.path.exists(out_dir):
            continue
            
        for item in os.listdir(out_dir):
            if item in seen_slugs:
                continue
                
            folder_path = os.path.join(out_dir, item)
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
                    "media_count": media_count,
                    "folder_path": folder_path
                })
                seen_slugs.add(item)
                
    topics.sort(key=lambda x: x["slug"])
    return topics

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, slug: Optional[str] = None):
    html_content = load_index_html()
    return HTMLResponse(content=html_content)

@app.get("/api/topics")
async def api_list_topics():
    return get_all_topics()

@app.get("/api/topic/{slug}")
async def api_get_topic(slug: str):
    topics = get_all_topics()
    target_topic = next((t for t in topics if t["slug"] == slug), None)
    
    if not target_topic:
        return JSONResponse({"error": "Topic not found"}, status_code=404)
        
    folder_path = target_topic["folder_path"]
    result = {}
    
    for filename in ["site_sources.json", "raw_content.json", "content_payload.json"]:
        filepath = os.path.join(folder_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                result[filename.replace(".json", "")] = json.load(f)
                
    brief_path = os.path.join(folder_path, "blog_research_brief.md")
    if os.path.exists(brief_path):
        with open(brief_path, "r", encoding="utf-8") as f:
            result["research_brief"] = f.read()
            
    return result

def run_scraper_task(title: str):
    script_path = os.path.join(ROOT_DIR, "scraper.py")
    subprocess.run([sys.executable, script_path, "--title", title], check=True)

@app.post("/api/scrape")
async def api_scrape(background_tasks: BackgroundTasks, title: str = Form(...)):
    if not title.strip():
        return JSONResponse({"error": "Title required"}, status_code=400)
        
    background_tasks.add_task(run_scraper_task, title.strip())
    return {"message": f"Scraping task launched for '{title}'", "status": "processing"}

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Happy Greenery Scraped Data Viewer Dashboard...")
    print("🌐 Open URL: http://localhost:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
