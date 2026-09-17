# 🪴 Happy Greenery Scraped Data React Dashboard

> **Vercel Static React App & Python Scraping Engine**  
> **Repository**: `https://github.com/gagankumar8294/happygreenery-scrap.git`  
> **Target Region**: Bengaluru / India & Global Top Plant Authorities  

---

## 📌 Project Architecture

This repository is organized into a clean **Static React App at root** (optimized for 1-click Vercel static deployment) and an isolated **Python Scraping Engine** inside `scripts/`.

```
.
├── index.html               # 3-Column React Dashboard UI (Vercel Static App)
├── outputs/                 # Scraped datasets & JSON manifest
│   ├── manifest.json        # Topic registry loaded by React UI
│   ├── best-air-purifying-indoor-plants-for-bengaluru-apartments/
│   │   ├── site_sources.json
│   │   ├── raw_content.json
│   │   ├── blog_research_brief.md
│   │   └── content_payload.json
│   └── top-20-low-maintenance-indoor-plants/
│       ├── site_sources.json
│       ├── raw_content.json
│       ├── blog_research_brief.md
│       └── content_payload.json
└── scripts/                 # Python Scraping Engine & Utilities
    ├── scraper.py           # Multi-site scraping engine
    ├── generate_manifest.py # Scraped topic manifest generator
    └── server.py           # Local FastAPI server
```

---

## 🚀 Vercel Deployment

Deploying on Vercel is now **100% static and instant** with **zero serverless function errors**:

1. Import `https://github.com/gagankumar8294/happygreenery-scrap` on Vercel.
2. Select **Framework Preset**: `Other` (or Static HTML).
3. Click **Deploy**. Vercel will deploy your React Dashboard UI in 1 second!

---

## 🛠️ How to Scrape New Plant Topics Locally

To harvest new plant data from top authority websites:

```bash
cd scripts
python scraper.py --title "Best Balcony Plants for Bengaluru Monsoon"
```

The scraper automatically extracts full text content, harvests media URLs (without binary file downloads), generates backend-ready blog JSON payloads, and updates `outputs/manifest.json` for the React Dashboard.

---

## 📤 Backend API Payload

The `content_payload.json` generated for each topic directly matches the **Happy Greenery Backend API** schema. You can post the payload directly to:
```
POST https://green-world-backend-85h0.onrender.com/api/blogs
```
