# HTML Image Generator

Generate production-quality images (PNG) from HTML/CSS. Supports social media posts, banners, OG images, thumbnails, and any visual asset that can be expressed as HTML.

Includes an integrated design intelligence database (powered by UI/UX Pro Max) with 161 color palettes, 57 font pairings, 50+ visual styles, 161 product types, and 99 UX guidelines — all searchable via Python scripts.

## When to Apply

### Must Use

- User asks to **generate an image**, post, banner, thumbnail, or visual asset
- User asks to **create social media content** (Instagram, Twitter/X, LinkedIn, YouTube)
- User asks to **design** a card, flyer, badge, certificate, or infographic
- User asks to create **OG images** or open graph previews
- User wants to **convert HTML to PNG/image**

### Skip

- User wants to edit an existing raster image (photo editing)
- User needs SVG-only output without rasterization
- Task is pure UI development (web pages, apps) — not image generation

## How It Works

1. You write an HTML file with inline CSS (self-contained, single file)
2. The render script opens it in a headless browser and screenshots it
3. Output is a high-resolution PNG at 2x scale

## Render Script

The render script is at `scripts/render.js` relative to this skill. It requires `puppeteer` to be installed in the project.

```bash
# Render an HTML file to PNG
node <skill-path>/scripts/render.js input.html output.png --format feed

# With custom dimensions
node <skill-path>/scripts/render.js input.html output.png --width 1200 --height 630

# From stdin
cat template.html | node <skill-path>/scripts/render.js --stdin -o output.png --format story
```

### Available Formats

| Format         | Dimensions   | Use Case                          |
|----------------|--------------|-----------------------------------|
| `feed`         | 1080 x 1080  | Instagram/Facebook square posts   |
| `story`        | 1080 x 1920  | Instagram/Facebook stories, Reels |
| `carousel`     | 1080 x 1080  | Instagram carousel slides         |
| `portrait`     | 1080 x 1350  | Instagram portrait posts          |
| `banner`       | 1200 x 628   | Facebook/LinkedIn banners         |
| `twitter-post` | 1200 x 675   | Twitter/X posts                   |
| `og-image`     | 1200 x 630   | Open Graph preview images         |
| `youtube-thumb` | 1280 x 720  | YouTube thumbnails                |
| `square`       | 1080 x 1080  | General square format             |
| `landscape`    | 1920 x 1080  | Landscape/presentation format     |

All rendered at 2x scale by default (e.g., feed = 2160x2160px actual).

## Setup

The project needs `puppeteer` installed:

```bash
npm install puppeteer
# or
yarn add puppeteer
```

## HTML Template Structure

Always use this base structure for generated images:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=...');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    .canvas {
      width: {WIDTH}px;
      height: {HEIGHT}px;
      /* background, font-family, etc */
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      position: relative;
    }
  </style>
</head>
<body>
  <div class="canvas">
    <!-- content here -->
  </div>
</body>
</html>
```

Key rules:
- **Self-contained**: all CSS inline, fonts via Google Fonts `@import`
- **Fixed dimensions**: `.canvas` must have explicit `width` and `height` in px
- **Real photos**: download from Unsplash, convert to base64, embed as `data:image/jpeg;base64,...` in CSS `background`
- **Use `file://` paths** only for local images the user provides
- **Design like a graphic designer**, not a web developer — see Section 5

## Brand Configuration (Optional)

If the project has a `brand.json` in its root, read it before generating images to respect the brand identity. Expected structure:

```json
{
  "company": {
    "name": "Company Name",
    "logo": "assets/logo.png"
  },
  "colors": {
    "primary": "#2563EB",
    "secondary": "#1E40AF",
    "accent": "#F59E0B",
    "background": "#FFFFFF",
    "text": "#1A1A2E",
    "text_light": "#FFFFFF"
  },
  "typography": {
    "heading_font": "Montserrat",
    "heading_weight": "700",
    "body_font": "Inter",
    "body_weight": "400",
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Inter:wght@400;600&display=swap"
  },
  "style": {
    "border_radius": "16px",
    "spacing": "40px",
    "shadow": "0 4px 24px rgba(0,0,0,0.15)"
  }
}
```

If no `brand.json` exists, ask the user for color preferences or use a professional default palette.

---

## Design Guidelines

### 1. Visual Hierarchy (CRITICAL)

Every image must have a clear focal point and maximum 3 levels of hierarchy.

**Type scale by format:**

| Element   | Feed/Square (1080px) | Story (1080px wide) | Banner (1200px) |
|-----------|----------------------|---------------------|-----------------|
| Heading   | 56 - 80px            | 64 - 96px           | 48 - 72px       |
| Subhead   | 28 - 36px            | 32 - 42px           | 24 - 32px       |
| Body      | 22 - 28px            | 24 - 32px           | 18 - 24px       |
| CTA       | 20 - 26px            | 22 - 28px           | 18 - 22px       |
| Caption   | 16 - 20px            | 18 - 22px           | 14 - 18px       |

**Rules:**
- Heading must be at least **2x larger** than body text
- Maximum **2 fonts** per image (1 heading + 1 body)
- Heading weight: **700 - 900** (bold/black)
- Body weight: **400 - 500** (regular/medium)
- Line-height: **1.0 - 1.15** for headings, **1.4 - 1.6** for body
- Max characters per line: **20 - 25** for headings, **35 - 45** for body
- Max total words: **40 - 50** for feed, **20 - 30** for stories

**Anti-patterns (NEVER do):**
- Text smaller than 20px (illegible on mobile)
- More than 3 different font sizes
- Text touching the edges (no breathing room)
- Heading and subheading with similar sizes (no hierarchy)

### 2. Typography Pairings

Recommended Google Fonts combinations:

| Name                | Heading          | Body           | Style                        | Best For                         |
|---------------------|------------------|----------------|------------------------------|----------------------------------|
| Bold Statement      | Bebas Neue       | Source Sans 3  | Impactful, dramatic          | Marketing, promos, events        |
| Startup Bold        | Outfit           | Rubik          | Modern, confident            | Startups, launches, tech         |
| Geometric Modern    | Outfit           | Work Sans      | Clean, balanced              | General purpose, agencies        |
| Modern Professional | Poppins          | Open Sans      | Professional, friendly       | SaaS, corporate, services        |
| Tech Startup        | Space Grotesk    | DM Sans        | Futuristic, innovative       | Tech, AI, dev tools              |
| Neubrutalist Bold   | Lexend Mega      | Public Sans    | Bold, geometric              | Gen Z, bold marketing            |
| Elegant Serif       | Playfair Display | Lato           | Sophisticated, classic       | Luxury, fashion, food            |
| Loud Impact         | Anton            | Epilogue       | Brutal, loud                 | Viral campaigns, streetwear      |
| Clean Corporate     | Montserrat       | Inter          | Versatile, professional      | Any brand, presentations         |
| Editorial           | DM Serif Display | DM Sans        | Editorial, refined           | Magazines, blogs, content        |

### 3. Color Palettes by Industry

| Industry            | Primary   | Secondary | Accent    | Background | Text      |
|---------------------|-----------|-----------|-----------|------------|-----------|
| Tech / SaaS         | #2563EB   | #3B82F6   | #8B5CF6   | #EFF6FF    | #1E3A5F   |
| Marketing / Agency  | #EC4899   | #F472B6   | #06B6D4   | #FDF2F8    | #831843   |
| Social Media        | #E11D48   | #FB7185   | #2563EB   | #FFF1F2    | #881337   |
| E-commerce          | #DC2626   | #F59E0B   | #16A34A   | #FFFBEB    | #78350F   |
| Healthcare          | #059669   | #34D399   | #0891B2   | #ECFDF5    | #064E3B   |
| Education           | #7C3AED   | #A78BFA   | #F59E0B   | #F5F3FF    | #4C1D95   |
| Food / Restaurant   | #EA580C   | #F97316   | #DC2626   | #FFF7ED    | #7C2D12   |
| Finance             | #1E40AF   | #3B82F6   | #059669   | #EFF6FF    | #1E3A5F   |
| Fashion / Luxury    | #18181B   | #71717A   | #D4AF37   | #FAFAFA    | #18181B   |
| Fitness / Sports    | #0F172A   | #334155   | #EF4444   | #F8FAFC    | #0F172A   |
| Real Estate         | #14532D   | #166534   | #CA8A04   | #F0FDF4    | #14532D   |
| Creative / Art      | #7C3AED   | #EC4899   | #F59E0B   | #FAF5FF    | #3B0764   |

**Color rules:**
- Contrast ratio: minimum **4.5:1** between text and background (WCAG AA)
- Maximum **3 - 4 colors** per image
- CTA must use a **different color** from everything else
- Dark backgrounds: use white text (#FFFFFF), minimum opacity 0.9
- Never: gray on gray, neon on white, red on green

### 4. Visual Styles

#### Glassmorphism
```css
backdrop-filter: blur(15px);
background: rgba(255, 255, 255, 0.15);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 20px;
```
Best for: modern, premium, tech. Requires a vibrant background behind the glass.

#### Minimalism
Black + white + 1 accent color only. Large type, extreme whitespace.
Best for: luxury, editorial, corporate.

#### Vibrant Blocks
Bold geometric shapes, neon colors, 32px+ type, high contrast.
Best for: social media, startups, youth brands.

#### Aurora / Gradient
Mesh gradients with 2-3 complementary colors, smooth transitions.
Best for: SaaS, creative agencies, music.

#### Dark Mode
Background #000000 or #121212, white text, neon accents.
Best for: tech, entertainment, gaming.

#### Neubrutalism
Thick borders (3-4px), solid offset shadows, primary colors, no border-radius.
```css
border: 3px solid #000;
box-shadow: 6px 6px 0 #000;
border-radius: 0;
```
Best for: Gen Z, disruptive brands, bold marketing.

### 5. Social Media Design (CRITICAL — READ THIS FIRST)

**This is NOT web design. This is graphic design for social media.**

Social media posts must look like they were made in Canva or by a graphic designer — NOT like a website, landing page, or app UI. The biggest mistake is making posts that look like screenshots of a web page.

#### What WORKS (do this):

- **Full-bleed photography** as background with gradient overlay for text readability
- **Text IS the design** — huge bold typography filling the space, not small text in boxes
- **Minimal elements** — photo + text + logo. That's it. Maximum impact.
- **Real photos** from Unsplash (download, convert to base64, embed inline). Always prefer real photography over abstract shapes
- **Gradient overlays** on photos: darker at the bottom where text goes, transparent at top where the photo breathes
- **Bold uppercase headlines** — 64-82px, weight 800-900, filling the width
- **Accent colors as text highlights**, not as backgrounds for boxes
- **Subtle brand elements**: thin accent bars, side strips, small logo — never dominating
- **Grain/noise texture** overlay for warmth and analog feel

#### What DOES NOT work (never do this):

- **Cards with borders** — this is a website component, not social media design
- **Pills/tags that look like buttons** — text labels yes, clickable-looking elements NO
- **Grid layouts** — posts are not dashboards
- **Multiple small boxes/containers** — this screams "landing page"
- **CTA buttons** — there are no buttons on Instagram. Use simple text with an arrow (→) at most
- **Info cards with icons** — this is a features section on a SaaS website
- **Timeline/stepper components** — UI pattern, not design pattern
- **Anything that looks interactive** — social media images are static, don't fake UI

#### Photo Background Technique:

```bash
# 1. Download photo from Unsplash
curl -sL "https://images.unsplash.com/photo-{ID}?w=1100&q=80" -o /tmp/photo.jpg

# 2. Convert to base64
base64 -w0 /tmp/photo.jpg > /tmp/photo-b64.txt

# 3. Inject into HTML via Python
python3 -c "
import base64
with open('/tmp/photo.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
with open('post.html', 'r') as f:
    html = f.read()
html = html.replace('PLACEHOLDER_B64', b64)
with open('post.html', 'w') as f:
    f.write(html)
"
```

CSS for photo + overlay:
```css
.photo {
  position: absolute;
  inset: 0;
  background: url('data:image/jpeg;base64,...') center 35% / cover no-repeat;
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(0, 0, 0, 0.15) 0%,      /* photo visible at top */
    rgba(0, 0, 0, 0.10) 25%,
    rgba(0, 0, 0, 0.55) 48%,      /* transition zone */
    rgba(0, 0, 0, 0.90) 65%,      /* dark for text */
    rgba(0, 0, 0, 0.97) 80%,
    rgba(0, 0, 0, 1) 100%
  );
}
```

#### Good Social Media Layouts:

**Feed / Square (1080x1080):**
1. **Photo + bold text** — full-bleed photo, gradient overlay, huge headline at bottom
2. **Split horizontal** — real photo top half, solid/gradient color bottom with big text
3. **Circle background** — large colored circle centered, illustrations floating, bold text below
4. **Full typography** — solid dark bg, text only, massive bold italic uppercase letters filling the space
5. **Diagonal split** — photo with diagonal color block cutting across

**Story (1080x1920):**
1. **Photo hero** — full-bleed photo with text overlay at bottom third
2. **Stacked impact** — big text top, photo middle, CTA text bottom
3. **Gradient flow** — smooth gradient bg, centered text, minimal elements

**Composition rules:**
- **Safe zone**: keep important content 60px from edges (platforms crop)
- **Padding**: minimum 40px from all edges
- **Breathing room**: at least 30% of the area should be empty space
- **Logo**: small and subtle, 36-48px, top-left or top-center. Never dominant.
- **Less is more**: if you're adding a 4th element, remove one instead

### 6. Visual Elements

**Brand accents (subtle, not dominant):**
- Thin color strips/bars at edges (5-8px) — brand signature
- Small logo placement — never bigger than the headline
- Color highlights on specific words — draw attention without boxes

**Decorative elements:**
- Grain/noise texture overlay (opacity 0.03-0.05) for warmth
- Gradient blobs (position: absolute, opacity low) for depth
- CSS `::before` / `::after` for subtle decorative touches

**Icons (use sparingly):**
- Only when illustrating a concept (floating documents, charts)
- Inline SVG, consistent style
- Part of the composition, not inside UI components

**What NOT to use as visual elements:**
- Bordered cards or containers
- Pill-shaped tags
- Button-like shapes
- Progress bars or steppers
- Any element that implies interactivity

### 7. Accessibility (CRITICAL)

Even in static images, accessibility matters for reach and legibility.

- **Minimum contrast**: 4.5:1 for normal text, 3:1 for large text (48px+)
- **Minimum text size**: 20px for feed, 24px for stories
- **Test gradients**: check contrast at both lightest AND darkest points
- **Solution for gradients**: add semi-transparent overlay behind text
- **Don't rely on color alone**: use icon + text to convey meaning
- **Avoid**: red + green together (colorblindness), light blue on white, yellow on white

### 8. Design Intelligence Search

This skill includes an integrated searchable database. **Always use these searches** before generating images to get context-specific recommendations.

All scripts are relative to this skill's directory. Replace `<skill-path>` with the actual path (e.g., `.claude/skills/html-image-gen`).

#### Generate a Complete Design System (RECOMMENDED FIRST STEP)

For any new image request, run this first to get style, colors, typography, and effects all at once:

```bash
python3 <skill-path>/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

Example:
```bash
python3 <skill-path>/scripts/search.py "fitness gym modern bold" --design-system -p "PowerGym"
```

#### Domain-Specific Searches

Use these for deep-diving into a specific dimension:

```bash
# Color palettes by industry (161 palettes)
python3 <skill-path>/scripts/search.py "<keyword>" --domain color -n 5

# Font pairings by mood (57 pairings)
python3 <skill-path>/scripts/search.py "<keyword>" --domain typography -n 5

# Visual styles (50+ styles)
python3 <skill-path>/scripts/search.py "<keyword>" --domain style -n 5

# Product type patterns (161 types)
python3 <skill-path>/scripts/search.py "<keyword>" --domain product -n 5

# UX best practices (99 guidelines)
python3 <skill-path>/scripts/search.py "<keyword>" --domain ux -n 5

# Landing page patterns
python3 <skill-path>/scripts/search.py "<keyword>" --domain landing -n 5

# Chart/data visualization types
python3 <skill-path>/scripts/search.py "<keyword>" --domain chart -n 5
```

#### When to Search

| Situation | What to Run |
|-----------|-------------|
| New image, unclear style | `--design-system` with product context |
| User asks "make it look like X" | `--domain style "<X keywords>"` |
| Need brand-appropriate colors | `--domain color "<industry>"` |
| Choosing fonts | `--domain typography "<mood>"` |
| Infographic / data image | `--domain chart "<chart type>"` |

The search results include CSS snippets, Google Fonts URLs, hex codes, and anti-patterns to avoid — use them directly in the HTML you generate.

---

## Workflow

### Step 1: Consult Design Learning

**Before anything else**, read `data/design-learning.md` (relative to this skill). This file contains:
- Visual concepts by theme (word → visual element mapping)
- Anti-patterns learned from past feedback
- Patterns that worked well
- The creative process to follow

Answer these 4 questions before designing:
1. What is the core message? (1 sentence)
2. What emotion/reaction should it provoke? (fear, curiosity, trust, urgency)
3. What is the visual metaphor? (keyword → concrete visual element)
4. Does the visual reinforce the text? (cover the text — can you guess the topic from visuals alone?)

If you can't answer question 3, search for references first. Do NOT start designing.

### Step 2: Understand the Request

Extract from the user's message:
- **What**: type of image (post, banner, thumbnail, OG image, etc.)
- **Format**: dimensions or platform (Instagram feed, Twitter, etc.)
- **Content**: text, data, or information to include
- **Style**: any style preferences mentioned
- **Industry/context**: for design system search

### Step 3: Search for Design Recommendations

**Always run the design system search** before generating HTML:

```bash
python3 <skill-path>/scripts/search.py "<product_type> <industry> <style_keywords>" --design-system
```

This returns a complete recommendation: style, colors (hex codes), typography (with Google Fonts URL), effects, and anti-patterns. Use these directly.

If the user has specific needs (e.g., "I want a dark theme"), supplement with domain searches:

```bash
python3 <skill-path>/scripts/search.py "dark mode minimal" --domain style -n 3
```

### Step 4: Check for Brand

Look for `brand.json` in the project root. If it exists, **brand values override** the search recommendations for colors, fonts, and logo. The search results still guide layout, style, and effects.

If no `brand.json` exists, use the search results directly.

### Step 5: Find a Background Photo

For social media posts, search Unsplash for a relevant photo:

1. Search for a photo that fits the topic (e.g., "container port" for comex, "team meeting" for corporate)
2. Download: `curl -sL "https://images.unsplash.com/photo-{ID}?w=1100&q=80" -o /tmp/photo.jpg`
3. Verify it downloaded: `file /tmp/photo.jpg` (should say JPEG)
4. Convert to base64 for embedding

If no photo fits (abstract/typographic posts), skip this step and use solid colors or gradients.

### Step 6: Generate HTML

Write a self-contained HTML file following:
1. **Section 5 (Social Media Design)** — this is the most important reference
2. The design system recommendations from Step 2
3. The design guidelines in this document (hierarchy, spacing, contrast)
4. Brand identity from Step 3 (if available)

Key considerations:
- Think like a graphic designer, not a web developer
- Photo background + gradient overlay + bold text = proven formula
- Use the correct dimensions for the chosen format
- Apply the type scale from the guidelines
- Ensure contrast ratios are met (4.5:1 minimum)
- Use Google Fonts via `@import` (URL from search results)
- Embed photos as base64 data URIs
- NO UI components (cards, buttons, pills, timelines)

### Step 7: Render to PNG

Run the render script:

```bash
node <skill-path>/scripts/render.js <html-file> <output.png> --format <format>
```

### Step 8: Show and Iterate

Show the generated image to the user. Ask if they want adjustments. Common adjustments:
- "make it bigger/smaller" — adjust font sizes
- "darker/lighter" — adjust background/text colors
- "more space" — increase padding
- "change the color" — run `--domain color` with new keywords
- "different style" — run `--domain style` with new keywords
- "add more text" — but warn if it exceeds recommended word count

## Pre-Delivery Checklist

Before delivering any image:

**Design quality:**
- [ ] Looks like a Canva/graphic design post, NOT a website screenshot
- [ ] Uses real photography as background (when applicable) with proper gradient overlay
- [ ] Text is the hero — bold, large, filling the space
- [ ] No UI components: no bordered cards, no button-like pills, no stepper/timeline components
- [ ] Maximum 3-4 elements total (photo + text + logo + one accent)

**Typography:**
- [ ] Clear hierarchy: heading > subheading > body > caption
- [ ] Maximum 2 fonts, maximum 4 colors
- [ ] Heading weight bold (700+), 64-82px for feed
- [ ] Minimum text size 20px (feed) / 24px (story)

**Technical:**
- [ ] Text contrast >= 4.5:1 against background
- [ ] Padding >= 40px from edges, 60px safe zone respected
- [ ] At least 30% empty space / breathing room
- [ ] Style consistent across the entire image
- [ ] Brand colors/fonts respected (if brand.json exists)
- [ ] Photo loaded and embedded as base64 (not external URL)
