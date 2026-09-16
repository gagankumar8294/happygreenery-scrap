# 🪴 Happy Greenery Data Scraper & 3-Column Intelligence Dashboard

> **Standalone Scraper & Visual Viewer Project**  
> **Repository**: `https://github.com/gagankumar8294/happygreenery-scrap.git`  
> **Target Region**: Bengaluru / India & Global Top Plant Authorities  

---

## 📌 Project Overview

This repository contains the complete end-to-end data scraping pipeline, persistent guidelines, dataset storage, and interactive 3-column React dashboard for **Happy Greenery**.

### 🌟 Key Features:
1. **Multi-Site Scraper Engine (`scraper.py`)**:
   - Searches and scrapes top 10–20 high-ranking plant & gardening websites (*Ugaoo, Nurserylive, Foliages.in, Balcony Garden Web, The Spruce, Gardening Know How, Abana Homes, etc.*).
   - Extracts full article headings (`H1`-`H4`), body paragraphs, meta summaries, and bullet lists.
   - **Media URLs Only**: Harvests image URLs, PDF guide links, 3D model links (`.glb`, `.gltf`, `.usdz`), and video embeds without downloading raw binary files.
2. **Persistent Guidelines (`SCRAPING_GUIDELINES.md`)**:
   - Maintains strict operational rules, media URL standards, domain targeting, and output schemas across all scraping sessions.
3. **3-Column React Viewer Dashboard (`server.py` & `templates/index.html`)**:
   - **Column 1**: Table of all recorded searched blog topics with filter search & media count badges.
   - **Column 2**: List of all top websites scraped for the selected topic (*Rank order, domain name, authority rating badges, media counts*).
   - **Column 3**: Formatted reader UI displaying article content, live image URL gallery, research briefs, and 1-click copyable Happy Greenery backend JSON payloads.

---

## 📁 Repository Structure

```
.
├── SCRAPING_GUIDELINES.md   # Persistent scraping rules & prompt guidelines
├── requirements.txt         # Python dependencies
├── scraper.py               # Data scraping CLI & automation script
├── server.py              # FastAPI server serving the web dashboard
├── templates/
│   └── index.html         # React 3-column UI dashboard template
└── outputs/                 # Persistent storage for all scraped JSON & Markdown datasets
    ├── best-air-purifying-indoor-plants-for-bengaluru-apartments/
    │   ├── site_sources.json
    │   ├── raw_content.json
    │   ├── blog_research_brief.md
    │   └── content_payload.json
    └── top-20-low-maintenance-indoor-plants/
        ├── site_sources.json
        ├── raw_content.json
        ├── blog_research_brief.md
        └── content_payload.json
```

---

## 🚀 Getting Started

### 1. Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

---

### 2. Running the 3-Column Viewer Dashboard

To view and interact with all scraped data in your browser:
```bash
python server.py
```
Open **`http://localhost:8000`** in your browser.

---

### 3. Scraping a New Blog Topic

You can trigger a scrape directly from the dashboard header UI at `http://localhost:8000`, or run the command line tool:

```bash
python scraper.py --title "Best Indoor Plants for Bengaluru Apartments"
```

Or run interactively:
```bash
python scraper.py
```

---

## 📤 Backend API Integration

The `content_payload.json` generated for each topic directly matches the **Happy Greenery Backend API** schema. You can post the payload directly to:
```
POST https://green-world-backend-85h0.onrender.com/api/blogs
```
