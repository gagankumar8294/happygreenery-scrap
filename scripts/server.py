#!/usr/bin/env python3
"""
Happy Greenery - Local Server Engine
====================================
Optional local FastAPI server for running the scraper viewer locally.
"""

import os
import sys
import json
import subprocess
from typing import Optional
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, Response

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIMARY_OUTPUTS_DIR = os.path.join(ROOT_DIR, "outputs")
INDEX_HTML_PATH = os.path.join(ROOT_DIR, "index.html")

app = FastAPI(title="Happy Greenery Scraped Data Viewer")

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    if os.path.exists(INDEX_HTML_PATH):
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Index.html not found</h1>"

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Happy Greenery Local Server...")
    print("🌐 Open URL: http://localhost:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
