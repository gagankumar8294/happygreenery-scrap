#!/usr/bin/env python3
"""
Happy Greenery - 5-Angle SEO Blog Post Generator
================================================
Reads scraped data for every topic in outputs/ and synthesizes 5 unique,
high-converting, SEO-optimized blog post variations tailored for Bengaluru & Indian homes.
Stores output as generated_blogs.json in each topic folder.
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def create_5_blog_angles(topic_title: str, topic_slug: str, scraped_data: list, media_pool: list) -> list:
    """Generates 5 distinct, high-converting SEO blog post variations for a topic."""
    
    # Helper image getter
    def get_img(index):
        if media_pool and index < len(media_pool):
            return media_pool[index]
        return {
            "url": "https://www.happygreenery.in/placeholder.jpg",
            "alt": f"{topic_title} guide happy greenery"
        }

    # Gather clean text snippets from scraped sources
    paragraphs = []
    headings = []
    for site in scraped_data:
        if site.get("success"):
            paragraphs.extend(site.get("paragraphs", []))
            for h in site.get("headings", []):
                if len(h.get("text", "")) > 10 and not any(ign in h["text"].lower() for ign in ["cookie", "privacy", "menu", "sign"]):
                    headings.append(h["text"])

    p_sample = paragraphs[:20] if paragraphs else ["Plant care is vital for healthy urban green spaces."]
    h_sample = headings[:10] if headings else ["Top Plant Care Tips", "Lighting & Watering Essentials"]

    img0 = get_img(0)
    img1 = get_img(1)
    img2 = get_img(2)
    img3 = get_img(3)

    # ── ANGLE 1: The Ultimate Comprehensive Guide ───────────────────────
    angle1_title = f"The Ultimate Guide to {topic_title.title()}: Care, Lighting & Soil Tips for Indian Homes"
    angle1_slug = slugify(angle1_title)
    angle1 = {
        "angle_id": 1,
        "angle_name": "Ultimate Comprehensive Guide",
        "payload": {
            "title": angle1_title,
            "slug": angle1_slug,
            "metaDescription": f"Complete guide to {topic_title.lower()} in India. Expert tips on sunlight, watering schedules, potting mix, and seasonal care for thriving green spaces.",
            "canonicalUrl": f"https://www.happygreenery.in/blog/{angle1_slug}",
            "ogTitle": angle1_title,
            "ogDescription": f"Master {topic_title.lower()} care with expert tips from Happy Greenery specialists.",
            "ogImage": img0["url"],
            "twitterTitle": angle1_title,
            "twitterDescription": f"Master {topic_title.lower()} care with expert tips from Happy Greenery specialists.",
            "twitterImage": img0["url"],
            "sections": [
                {
                    "type": "paragraph",
                    "value": f"Creating a lush green sanctuary starts with understanding {topic_title.lower()}. Whether you are starting your gardening journey or expanding your collection, selecting the right plants and maintaining ideal soil moisture is key to long-term success."
                },
                { "type": "image", "value": img0["url"], "alt": img0["alt"] },
                { "type": "h2", "value": f"Key Requirements for {topic_title.title()}" },
                {
                    "type": "paragraph",
                    "value": p_sample[0] if len(p_sample) > 0 else "Ensure well-draining soil and adequate indirect sunlight for peak foliage growth."
                },
                {
                    "type": "paragraph",
                    "value": p_sample[1] if len(p_sample) > 1 else "Regulate watering according to seasonal humidity levels, allowing topsoil to dry between waterings."
                },
                { "type": "h2", "value": "Essential Watering & Sunlight Guidelines" },
                {
                    "type": "paragraph",
                    "value": p_sample[2] if len(p_sample) > 2 else "Bright indirect sunlight prevents leaf burn while encouraging vibrant green foliage."
                },
                { "type": "image", "value": img1["url"], "alt": img1["alt"] },
                { "type": "h2", "value": "Soil Conditioning & Fertilizer Routine" },
                {
                    "type": "paragraph",
                    "value": "Mix coco peat, perlite, vermicompost, and organic neem cake to provide optimal aeration and nutrient intake."
                }
            ]
        }
    }

    # ── ANGLE 2: Bengaluru & Apartment Living Focus ──────────────────────
    angle2_title = f"{topic_title.title()} for Bengaluru Apartments & Small Balconies"
    angle2_slug = slugify(angle2_title)
    angle2 = {
        "angle_id": 2,
        "angle_name": "Bengaluru Apartment & Balcony Focus",
        "payload": {
            "title": angle2_title,
            "slug": angle2_slug,
            "metaDescription": f"Tailored {topic_title.lower()} solutions for Bengaluru flats & high-rise balconies. Overcome low-light, ventilation, and space constraints.",
            "canonicalUrl": f"https://www.happygreenery.in/blog/{angle2_slug}",
            "ogTitle": angle2_title,
            "ogDescription": f"Transform your Bengaluru balcony or living room with {topic_title.lower()}.",
            "ogImage": img1["url"],
            "twitterTitle": angle2_title,
            "twitterDescription": f"Transform your Bengaluru balcony or living room with {topic_title.lower()}.",
            "twitterImage": img1["url"],
            "sections": [
                {
                    "type": "paragraph",
                    "value": f"Apartment living in Bengaluru comes with unique microclimates: mild year-round temperatures, monsoon humidity, and varying balcony sunlight angles. {topic_title.title()} are perfectly suited to elevate urban living spaces."
                },
                { "type": "h2", "value": "Optimizing Balcony Space & Lighting in Bangalore" },
                {
                    "type": "paragraph",
                    "value": p_sample[3] if len(p_sample) > 3 else "East and North-facing balconies offer ideal morning light, preventing heat stress on delicate foliage."
                },
                { "type": "image", "value": img1["url"], "alt": img1["alt"] },
                { "type": "h2", "value": "Managing High-Rise Wind & Monsoon Humidity" },
                {
                    "type": "paragraph",
                    "value": p_sample[4] if len(p_sample) > 4 else "During Bengaluru monsoons, reduce watering frequency and ensure pots have drainage holes to prevent root rot."
                }
            ]
        }
    }

    # ── ANGLE 3: Low Maintenance & Busy Lifestyle ────────────────────────
    angle3_title = f"Top Low-Maintenance {topic_title.title()} for Busy Working Professionals"
    angle3_slug = slugify(angle3_title)
    angle3 = {
        "angle_id": 3,
        "angle_name": "Low Maintenance & Busy Lifestyle",
        "payload": {
            "title": angle3_title,
            "slug": angle3_slug,
            "metaDescription": f"Looking for easy-care plants? Discover resilient {topic_title.lower()} that thrive with minimal watering and neglect.",
            "canonicalUrl": f"https://www.happygreenery.in/blog/{angle3_slug}",
            "ogTitle": angle3_title,
            "ogDescription": f"Resilient {topic_title.lower()} for hassle-free green decor.",
            "ogImage": img2["url"],
            "twitterTitle": angle3_title,
            "twitterDescription": f"Resilient {topic_title.lower()} for hassle-free green decor.",
            "twitterImage": img2["url"],
            "sections": [
                {
                    "type": "paragraph",
                    "value": f"Busy schedules shouldn't stop you from enjoying nature at home. Low-maintenance varieties within {topic_title.lower()} require minimal attention while keeping indoor air fresh and vibrant."
                },
                { "type": "h2", "value": "Why These Plants Are Forgiving for Beginners" },
                {
                    "type": "paragraph",
                    "value": p_sample[5] if len(p_sample) > 5 else "These hardy varieties tolerate occasional missed waterings and adapt well to fluctuating light conditions."
                },
                { "type": "image", "value": img2["url"], "alt": img2["alt"] },
                { "type": "h2", "value": "Simple 5-Minute Weekly Care Checklist" },
                {
                    "type": "paragraph",
                    "value": "Check soil moisture with a finger test, wipe leaves with a moist cloth to remove dust, and water only when top layer is dry."
                }
            ]
        }
    }

    # ── ANGLE 4: Interior Styling & Aesthetics ───────────────────────────
    angle4_title = f"How to Style {topic_title.title()} for Modern Aesthetic Home Decor"
    angle4_slug = slugify(angle4_title)
    angle4 = {
        "angle_id": 4,
        "angle_name": "Interior Styling & Aesthetics",
        "payload": {
            "title": angle4_title,
            "slug": angle4_slug,
            "metaDescription": f"Elevate your home interiors with {topic_title.lower()}. Designer styling tips on planter selection, elevation, and focal points.",
            "canonicalUrl": f"https://www.happygreenery.in/blog/{angle4_slug}",
            "ogTitle": angle4_title,
            "ogDescription": f"Transform interior spaces using {topic_title.lower()}.",
            "ogImage": img3["url"],
            "twitterTitle": angle4_title,
            "twitterDescription": f"Transform interior spaces using {topic_title.lower()}.",
            "twitterImage": img3["url"],
            "sections": [
                {
                    "type": "paragraph",
                    "value": f"Plants are dynamic living design elements that bring warmth, texture, and natural elegance into modern homes. Here is how to style {topic_title.lower()} like an interior designer."
                },
                { "type": "h2", "value": "Choosing the Right Planters: Ceramic, Terracotta & Rattan" },
                {
                    "type": "paragraph",
                    "value": p_sample[6] if len(p_sample) > 6 else "Pair textured terracotta or sleek minimalist ceramic planters with lush green foliage for contemporary aesthetics."
                },
                { "type": "image", "value": img3["url"], "alt": img3["alt"] },
                { "type": "h2", "value": "Creating Layered Heights & Corner Focal Points" },
                {
                    "type": "paragraph",
                    "value": "Use wooden plant stands or brass pedestals to create vertical interest and draw eyes to empty living room corners."
                }
            ]
        }
    }

    # ── ANGLE 5: Seasonal Care & Pest Troubleshooting ───────────────────
    angle5_title = f"Monsoon & Summer Care Guide for {topic_title.title()}: Prevent Pests & Root Rot"
    angle5_slug = slugify(angle5_title)
    angle5 = {
        "angle_id": 5,
        "angle_name": "Seasonal Care & Troubleshooting",
        "payload": {
            "title": angle5_title,
            "slug": angle5_slug,
            "metaDescription": f"Protect your {topic_title.lower()} across Indian seasons. Learn root rot prevention, natural neem oil pest remedies, and summer hydration.",
            "canonicalUrl": f"https://www.happygreenery.in/blog/{angle5_slug}",
            "ogTitle": angle5_title,
            "ogDescription": f"Seasonal care tips to protect {topic_title.lower()}.",
            "ogImage": img0["url"],
            "twitterTitle": angle5_title,
            "twitterDescription": f"Seasonal care tips to protect {topic_title.lower()}.",
            "twitterImage": img0["url"],
            "sections": [
                {
                    "type": "paragraph",
                    "value": f"Weather fluctuations across Indian seasons impact plant health significantly. From heavy monsoon rains to dry summer heat waves, proactive care ensures your {topic_title.lower()} thrive year-round."
                },
                { "type": "h2", "value": "Preventing Root Rot During Heavy Monsoons" },
                {
                    "type": "paragraph",
                    "value": p_sample[7] if len(p_sample) > 7 else "Ensure saucers are emptied immediately after rainfall and move sensitive pots under covered shade."
                },
                { "type": "h2", "value": "Organic Pest Defense: Neem Oil & Soap Solution" },
                {
                    "type": "paragraph",
                    "value": "Spray cold-pressed neem oil mixed with mild liquid dish soap once every two weeks to repel mealybugs and spider mites naturally."
                }
            ]
        }
    }

    return [angle1, angle2, angle3, angle4, angle5]

def process_all_topics():
    if not os.path.exists(OUTPUTS_DIR):
        print("[ERROR] outputs/ directory not found.")
        return

    print("=======================================================")
    print("🚀 Generating 5 Unique SEO Blog Angles per Scraped Topic")
    print("=======================================================\n")

    for item in os.listdir(OUTPUTS_DIR):
        folder_path = os.path.join(OUTPUTS_DIR, item)
        if os.path.isdir(folder_path):
            raw_path = os.path.join(folder_path, "raw_content.json")
            payload_path = os.path.join(folder_path, "content_payload.json")
            
            topic_title = item.replace("-", " ").title()
            scraped_data = []
            media_pool = []

            if os.path.exists(payload_path):
                try:
                    with open(payload_path, "r", encoding="utf-8") as f:
                        payload = json.load(f)
                        topic_title = payload.get("title", topic_title)
                except Exception:
                    pass

            if os.path.exists(raw_path):
                try:
                    with open(raw_path, "r", encoding="utf-8") as f:
                        scraped_data = json.load(f)
                        for site in scraped_data:
                            for img in site.get("media", {}).get("images", []):
                                media_pool.append(img)
                except Exception:
                    pass

            print(f"📝 Generating 5 Blog Angles for: '{topic_title}'...")
            blogs_5 = create_5_blog_angles(topic_title, item, scraped_data, media_pool)
            
            out_file = os.path.join(folder_path, "generated_blogs.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(blogs_5, f, indent=2, ensure_ascii=False)
            print(f"  └─ Saved: {out_file}\n")

    print("=======================================================")
    print("🎉 All 5-Angle SEO Blog Payloads successfully generated!")
    print("=======================================================\n")

if __name__ == "__main__":
    process_all_topics()
