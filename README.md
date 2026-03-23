# HTML Image Generator — Claude Code Skill

A Claude Code skill that generates production-quality PNG images from HTML/CSS. Works with any project — just install and ask Claude to create images.

Supports Instagram posts, stories, banners, OG images, YouTube thumbnails, and any visual format that can be expressed as HTML.

## Features

- **10 preset formats**: feed, story, carousel, portrait, banner, twitter-post, og-image, youtube-thumb, square, landscape
- **2x retina rendering** via Puppeteer headless browser
- **Integrated design intelligence** (powered by UI/UX Pro Max): searchable database with 161 color palettes, 57 font pairings, 50+ visual styles, 161 product types, and 99 UX guidelines
- **Design system generator**: auto-recommends style, colors, typography, and effects based on product type and industry
- **Brand support**: optional `brand.json` for consistent brand identity across all images
- **Zero config**: works out of the box with sensible defaults, no configuration needed

## Installation

### 1. Copy the skill into your project

```bash
# From this repo
cp -r skill/ /path/to/your-project/.claude/skills/html-image-gen/
```

Or clone directly:

```bash
cd /path/to/your-project
mkdir -p .claude/skills
git clone https://github.com/YOUR_USER/html-image-gen-skill .claude/skills/html-image-gen
```

### 2. Install Puppeteer

```bash
cd /path/to/your-project
npm install puppeteer
```

### 3. (Optional) Create a brand.json

```json
{
  "company": {
    "name": "Your Company",
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
  }
}
```

### 4. Start using

Open Claude Code in your project and ask:

- "Generate an Instagram post about our new product launch"
- "Create an OG image for the blog post at /content/my-post.md"
- "Make a YouTube thumbnail with dark theme"
- "Design a LinkedIn banner for our company page"

## How It Works

1. Claude reads the SKILL.md and understands your request
2. It generates a self-contained HTML file with inline CSS and Google Fonts
3. The HTML is rendered to PNG via Puppeteer at 2x resolution
4. Claude shows you the image and iterates based on your feedback

## Standalone Render Script

The render script can also be used directly:

```bash
# Basic usage
node .claude/skills/html-image-gen/scripts/render.js input.html output.png

# With format preset
node .claude/skills/html-image-gen/scripts/render.js input.html output.png --format story

# Custom dimensions
node .claude/skills/html-image-gen/scripts/render.js input.html output.png --width 1200 --height 630

# From stdin
cat template.html | node .claude/skills/html-image-gen/scripts/render.js --stdin -o output.png
```

## Available Formats

| Format          | Dimensions   | Use Case                          |
|-----------------|--------------|-----------------------------------|
| `feed`          | 1080 x 1080  | Instagram/Facebook square posts   |
| `story`         | 1080 x 1920  | Instagram/Facebook stories, Reels |
| `carousel`      | 1080 x 1080  | Instagram carousel slides         |
| `portrait`      | 1080 x 1350  | Instagram portrait posts          |
| `banner`        | 1200 x 628   | Facebook/LinkedIn banners         |
| `twitter-post`  | 1200 x 675   | Twitter/X posts                   |
| `og-image`      | 1200 x 630   | Open Graph preview images         |
| `youtube-thumb`  | 1280 x 720  | YouTube thumbnails                |
| `square`        | 1080 x 1080  | General square format             |
| `landscape`     | 1920 x 1080  | Landscape/presentation format     |

## Design Intelligence

The skill includes a complete searchable design database:

- **161 color palettes** by industry and product type
- **57 font pairings** with Google Fonts URLs and mood keywords
- **50+ visual styles** with CSS snippets (glassmorphism, neubrutalism, aurora, etc.)
- **161 product type patterns** with layout and CTA recommendations
- **99 UX guidelines** covering accessibility, touch targets, animation, forms
- **Design system generator** that combines all of the above into a single recommendation

Plus built-in guidelines for visual hierarchy, type scales, spacing, composition, and accessibility.

### Prerequisites

- Node.js (for Puppeteer rendering)
- Python 3 (for design intelligence searches — no external dependencies)

See [skill/SKILL.md](skill/SKILL.md) for the full reference.

## License

MIT
