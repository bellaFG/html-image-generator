# HTML Image Generator Skill

This repository contains a Claude Code skill for generating production-quality images from HTML/CSS.

## Installation

Copy the `skill/` folder into your project's `.claude/skills/html-image-gen/` directory:

```bash
cp -r skill/ /path/to/your-project/.claude/skills/html-image-gen/
```

Then install Puppeteer in your project:

```bash
npm install puppeteer
```

## Usage

Once installed, Claude Code will automatically use this skill when you ask it to generate images, social media posts, banners, thumbnails, or any visual asset.

### Quick examples

- "Generate an Instagram post announcing our new feature"
- "Create an OG image for this blog post"
- "Make a YouTube thumbnail with the title 'Top 10 Tips'"
- "Design a banner for our Black Friday sale"

### Brand support

Create a `brand.json` in your project root to have all images follow your brand identity. See the SKILL.md for the expected format.
