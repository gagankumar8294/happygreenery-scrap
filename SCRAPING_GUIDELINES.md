# Happy Greenery - Data Scraping Guidelines & Persistent Rules

> **Version**: 1.0.0  
> **Target Region**: Bengaluru / Karnataka / All-India & Global Top Plant Authorities  
> **Niche**: Plants, Gardening, Indoor Plants, Aquatic Gardens, Balcony Setup, Green Gifting, Plant Care  

---

## 📌 1. Operational Overview & Guidelines

This document serves as the persistent rulebook and specification standard for all data scraping operations within the `datascrapping/` module. Every prompt execution, automated run, or manual script execution **MUST** strictly adhere to the standards set forth below.

---

## 🎯 2. Core Scraping Mandates

### Rule A: Authority & Regional Domain Targeting
1. **Top ~20 High-Ranking Websites Only**: Scrape data exclusively from top-ranked, highly-rated, and authoritative websites in the plant, nursery, e-commerce, and gardening ecosystem.
2. **Geographic Localization (Bengaluru / India)**:
   - Prioritize regional authorities such as *Ugaoo*, *Nurserylive*, *Balcony Garden Web*, *MyBageecha*, *Plantify*, *Kisan Nursery*, *Gardening in India*, *Housing.com Gardening*, *Architectural Digest India*, alongside global authority sites like *The Spruce*, *Gardening Know How*, *Planterina*, *Epic Gardening*.
   - Filter and adapt climate data specifically for Bengaluru/South Indian conditions (monsoon patterns, moderate year-round temperatures, balcony lighting, tropical foliage care).

### Rule B: Media Extraction Protocol (URLs ONLY)
- ❌ **DO NOT** download binary image files (`.png`, `.jpg`, `.webp`), PDFs, or 3D models directly to the filesystem.
- ✅ **DO** extract and capture all full media URLs (`src`, `data-src`, `srcset`, `.pdf`, `.glb`, `.gltf`, `.usdz`, YouTube embeds).
- Store media metadata alongside each URL (e.g., `alt_text`, `media_type`, `caption`, `original_source_page`).

### Rule C: Structured Content Output
Scraped content must be organized to directly map to the **Happy Greenery Blog Payload Schema**:
- **Title**: SEO-optimized article title.
- **Slug**: URL-friendly slug.
- **Sections**: Array of content section objects:
  - `type`: `"h2"` | `"h3"` | `"paragraph"` | `"image"` | `"link"` | `"list"`
  - `value`: Main text or media URL
  - `alt`: Descriptive SEO alt text for images
  - `linkText`: Anchor text for links

---

## 🏗️ 3. Input & Output Directory Layout

```
datascrapping/
├── SCRAPING_GUIDELINES.md   # Persistent rules & prompt terms (THIS FILE)
├── scraper.py               # Main multi-site scraping & synthesis engine
├── requirements.txt         # Python dependencies
└── outputs/                 # Directory holding scraped research & blog payloads
    └── <blog-slug>/
        ├── site_sources.json         # Top ~20 targeted websites & site info
        ├── raw_content.json          # Raw extracted content & media URLs per site
        ├── blog_research_brief.md    # Consolidated markdown brief
        └── content_payload.json      # Backend-ready JSON blog payload
```

---

## 📋 4. Targeted High-Authority Websites (Plant & Gardening Niche)

| Domain | Focus / Niche | Region | Authority Tier |
| :--- | :--- | :--- | :--- |
| `ugaoo.com` | E-commerce, Plant Care Guides | India | Tier 1 |
| `nurserylive.com` | Plant Encyclopedia & Shop | India | Tier 1 |
| `balconygardenweb.com` | Balcony & Small Space Gardening | India / Global | Tier 1 |
| `mybageecha.com` | Plants, Terrariums, Water Gardens | India | Tier 1 |
| `thespruce.com` | Comprehensive Plant Care | Global | Tier 1 |
| `gardeningknowhow.com` | Botanical & Horticultural Guides | Global | Tier 1 |
| `epicgardening.com` | Soil, Urban Gardening, Hydroponics | Global | Tier 1 |
| `plantify.co.za` | Indoor Plant Styling | Global | Tier 2 |
| `housing.com/news` | Urban Indian Balcony Gardening | India | Tier 1 |
| `architecturaldigest.in` | Luxury Plant & Interior Decor | India | Tier 1 |

---

## ⚙️ 5. Automated Execution Workflow

1. **Input Phase**: User inputs a blog title, topic, or keyword (e.g., *"Best Indoor Plants for Bengaluru Low-Light Apartments"*).
2. **Domain Discovery Phase**: Script queries search engines to find top 15–20 high-ranking articles for that exact query.
3. **Information Scraping Phase**:
   - Extract Site Info (URL, Title, Domain Rating, Summary).
   - Scrape textual body content (H2/H3 headers, subpoints, care tips).
   - Harvest Image/Media URLs without downloading binaries.
4. **Synthesis & JSON Payload Formatting**: Format scraped findings into `content_payload.json` matching Happy Greenery backend requirements (`http://green-world-backend-85h0.onrender.com/api/blogs`).
