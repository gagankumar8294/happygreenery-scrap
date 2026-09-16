#!/usr/bin/env python3
"""
Happy Greenery - Scraped Data Viewer & Dashboard Server
======================================================
FastAPI application that serves an interactive 3-column dashboard for viewing, exploring,
and managing all scraped plant data stored in datascrapping/outputs/.
"""

import os
import sys
import json
import subprocess
from typing import Optional
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app = FastAPI(title="Happy Greenery Scraped Data Viewer")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def get_all_topics():
    topics = []
    if not os.path.exists(OUTPUTS_DIR):
        return topics
        
    for item in os.listdir(OUTPUTS_DIR):
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
                "media_count": media_count,
                "folder_path": folder_path
            })
            
    topics.sort(key=lambda x: x["slug"])
    return topics

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, slug: Optional[str] = None):
    topics = get_all_topics()
    selected_topic = None
    
    if slug:
        selected_topic = next((t for t in topics if t["slug"] == slug), None)
    elif topics:
        selected_topic = topics[0]
        
    topic_data = {}
    if selected_topic:
        slug_dir = os.path.join(OUTPUTS_DIR, selected_topic["slug"])
        
        sources_path = os.path.join(slug_dir, "site_sources.json")
        if os.path.exists(sources_path):
            with open(sources_path, "r", encoding="utf-8") as f:
                topic_data["sources"] = json.load(f)
                
        raw_path = os.path.join(slug_dir, "raw_content.json")
        if os.path.exists(raw_path):
            with open(raw_path, "r", encoding="utf-8") as f:
                topic_data["raw_content"] = json.load(f)
                
        brief_path = os.path.join(slug_dir, "blog_research_brief.md")
        if os.path.exists(brief_path):
            with open(brief_path, "r", encoding="utf-8") as f:
                topic_data["research_brief"] = f.read()
                
        payload_path = os.path.join(slug_dir, "content_payload.json")
        if os.path.exists(payload_path):
            with open(payload_path, "r", encoding="utf-8") as f:
                topic_data["payload"] = json.load(f)
                
    return templates.TemplateResponse("index.html", {
        "request": request,
        "topics": topics,
        "selected_topic": selected_topic,
        "data": topic_data
    })

@app.get("/api/topics")
async def api_list_topics():
    return get_all_topics()

@app.get("/api/topic/{slug}")
async def api_get_topic(slug: str):
    slug_dir = os.path.join(OUTPUTS_DIR, slug)
    if not os.path.exists(slug_dir):
        return JSONResponse({"error": "Topic not found"}, status_code=404)
        
    result = {}
    for filename in ["site_sources.json", "raw_content.json", "content_payload.json"]:
        filepath = os.path.join(slug_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                result[filename.replace(".json", "")] = json.load(f)
                
    brief_path = os.path.join(slug_dir, "blog_research_brief.md")
    if os.path.exists(brief_path):
        with open(brief_path, "r", encoding="utf-8") as f:
            result["research_brief"] = f.read()
            
    return result

def run_scraper_task(title: str):
    script_path = os.path.join(BASE_DIR, "scraper.py")
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
