# Happy Greenery - SEO Blog Generation Guidelines & Persistent Rules

> **Version**: 1.0.0  
> **Target Audience**: Bengaluru & Indian Urban Plant Enthusiasts  
> **Target Domain**: `https://www.happygreenery.in`  
> **API Endpoint**: `https://green-world-backend-85h0.onrender.com/api/blogs`  

---

## 📌 1. Core Principles & Operational Mandates

Every AI agent or script generating blog post content for Happy Greenery **MUST** follow these strict guidelines:

1. **Zero Copyright / 100% Original Content**:
   - Content must be written in fresh, human-like, unique phrasing.
   - Do **NOT** copy-paste text blocks verbatim from scraped competitor websites. Use scraped datasets solely as factual & technical reference points (light conditions, watering cycles, plant taxonomy, regional adaptability).

2. **Geographic Localization & Intent**:
   - Focus heavily on **Bengaluru / Karnataka / South Indian climate conditions**: monsoon care, balcony sunlight, high-rise apartment airflow, potted soil mixes, red soil conditioning, humidity management.

3. **SEO & Keyword Optimization**:
   - Seamlessly integrate primary, secondary, and long-tail LSI keywords.
   - Structure articles with clear hierarchy (`H1` title, `H2` core sections, `H3` plant care breakdown, `P` body paragraphs, bullet lists).
   - Generate SEO-optimized `metaDescription` (140–160 chars), OpenGraph tags, and Twitter cards.

4. **5 Unique Angles / Posts Per Scraped Topic**:
   For every scraped topic, generate 5 distinct blog post variations targeting different user search intents:
   - **Angle 1**: *The Ultimate Comprehensive Guide* (In-depth care & species overview).
   - **Angle 2**: *Bengaluru / Apartment Living Focus* (Balconies, low light, indoor space efficiency).
   - **Angle 3**: *Low Maintenance & Beginner Friendly* (Easy-care routines for busy working professionals).
   - **Angle 4**: *Styling, Aesthetics & Home Decor* (Interior styling, pot choices, vertical/terrace layout).
   - **Angle 5**: *Seasonal Care & Troubleshooting* (Monsoon/summer watering, pest control, soil mix hacks).

---

## 🏗️ 2. Happy Greenery JSON Blog Payload Schema

All generated blog variations must strictly follow this JSON schema for direct API posting:

```json
{
  "title": "SEO Optimized Catchy H1 Title",
  "slug": "url-friendly-slug",
  "metaDescription": "Concise SEO meta description including target keywords.",
  "canonicalUrl": "https://www.happygreenery.in/blog/url-friendly-slug",
  "ogTitle": "OpenGraph Title",
  "ogDescription": "OpenGraph Description",
  "ogImage": "https://res.cloudinary.com/... or scraped image URL",
  "twitterTitle": "Twitter Card Title",
  "twitterDescription": "Twitter Card Description",
  "twitterImage": "https://res.cloudinary.com/... or scraped image URL",
  "sections": [
    { "type": "paragraph", "value": "Introduction text..." },
    { "type": "h2", "value": "Section H2 Header" },
    { "type": "paragraph", "value": "Detailed body content..." },
    { "type": "image", "value": "https://...", "alt": "Descriptive SEO Alt Text" }
  ]
}
```
