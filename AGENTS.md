# 🤖 AGENTS.md - Persistent Project Rules & Execution Standards

> **Project**: Happy Greenery Scraped Data & SEO Blog Engine  
> **Repository**: `https://github.com/gagankumar8294/happygreenery-scrap`  
> **Target Domain**: `https://www.happygreenery.in`  
> **Backend API**: `https://green-world-backend-85h0.onrender.com/api/blogs`  

---

## 📌 1. Project Purpose & Core Architecture

This repository is a dual-component ecosystem:
1. **Root (Static React Application)**: Serves a 3-Column responsive dashboard UI on Vercel displaying scraped data & 5-angle SEO blog payloads.
2. **`scripts/` (Python Scraping & Generation Engine)**: Harvests web data from top ~20 plant authorities, extracts media URLs (no binary downloads), generates 5 unique SEO blog post variations, and updates `outputs/manifest.json`.

```
.
├── AGENTS.md                # Persistent instructions for AI agents (THIS FILE)
├── index.html               # 3-Column React Dashboard UI (Vercel Root Deployment)
├── package.json             # Static Vercel build override
├── vercel.json              # Vercel outputDirectory configuration
├── README.md                # General project documentation
├── outputs/                 # Tracked scraped datasets & JSON manifest
│   ├── manifest.json        # Topic registry loaded by React UI
│   └── <topic-slug>/
│       ├── site_sources.json
│       ├── raw_content.json
│       ├── blog_research_brief.md
│       ├── content_payload.json
│       └── generated_blogs.json
└── scripts/                 # Isolated Python Engine & Utilities
    ├── scraper.py           # Multi-site scraping engine
    ├── generate_blogs.py    # 5-Angle SEO blog post generator
    ├── generate_manifest.py # Scraped topic manifest generator
    ├── bulk_scraper.py      # Bulk topic execution utility
    ├── BLOG_GENERATION_GUIDELINES.md
    └── AGENTS.md
```

---

## 🎯 2. Strict Rules for AI Agents & Automated Scripts

### Rule 1: Media Extraction Protocol (URLs ONLY)
- ❌ **NEVER** download raw binary media files (`.png`, `.jpg`, `.webp`, `.pdf`, `.glb`).
- ✅ **ALWAYS** capture and store remote media URLs (`src`, `data-src`, `srcset`, `.pdf`, `.glb`) along with descriptive `alt` tags and source domain badges.

### Rule 2: 100% Unique & Copyright-Free Content Standard
- ❌ **NEVER** copy-paste text blocks, sentences, or paragraphs verbatim from competitor websites.
- ✅ **ALWAYS** use scraped data purely as technical/factual reference points (light needs, watering cycles, soil ratios).
- ✅ **ALWAYS** write introductory text, section headers, care checklists, and advice in fresh, original phrasing.

### Rule 3: Bengaluru & Indian Localization Intent
- All blog posts and advice must be tailored specifically for **Bengaluru & Indian urban living conditions**:
  - High-rise apartment balcony sunlight angles & wind control.
  - Monsoon humidity, heavy rain saucer care, and root rot prevention.
  - Red soil conditioning, coco peat, perlite, and neem oil organic pest sprays.

### Rule 4: 5 SEO Angles per Scraped Topic
For every scraped topic, `scripts/generate_blogs.py` MUST create 5 distinct blog angles in `generated_blogs.json`:
1. **Angle #1**: *Ultimate Comprehensive Guide* (In-depth species care).
2. **Angle #2**: *Bengaluru Apartment & Balcony Focus* (Space, light, balcony tips).
3. **Angle #3**: *Low Maintenance & Busy Lifestyle* (Hassle-free professional routines).
4. **Angle #4**: *Interior Styling & Aesthetics* (Planters, pedestals, focal points).
5. **Angle #5**: *Seasonal Care & Troubleshooting* (Monsoon/summer watering & neem pest defense).

### Rule 5: Vercel Static Deployment Standard
- ❌ **NEVER** configure serverless Python routes or backend rewrites on Vercel.
- ✅ Root `index.html` is a pure static React single-page application.
- ✅ `vercel.json` must contain `"outputDirectory": "."` to deploy root as a static site.
- ✅ `package.json` must override build script to `echo "Build skipped: Static React deployment"`.

---

## 🛠️ 3. Standard Execution Workflow

### Scraping a New Topic
```bash
cd scripts
python scraper.py --title "Your Topic Title"
```

### Generating 5 SEO Blog Angles
```bash
python scripts/generate_blogs.py
```

### Updating Manifest for React UI
```bash
python scripts/generate_manifest.py
```

### Pushing Changes to Live Vercel Site
```bash
git add outputs/
git commit -m "Add new scraped datasets and 5-angle SEO blogs"
git push origin main
```
