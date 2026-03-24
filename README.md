# Gerador de Imagens HTML — Skill do Claude Code

Uma skill do Claude Code que gera imagens PNG de alta qualidade a partir de HTML/CSS. Funciona com qualquer projeto — basta instalar e pedir ao Claude para criar imagens.

Suporta posts de Instagram, stories, banners, imagens OG, thumbnails do YouTube e qualquer formato visual que possa ser expresso como HTML.

## Funcionalidades

- **10 formatos pre-definidos**: feed, story, carousel, portrait, banner, twitter-post, og-image, youtube-thumb, square, landscape
- **Renderizacao retina 2x** via Puppeteer headless browser
- **Inteligencia de design integrada** (powered by UI/UX Pro Max): banco de dados pesquisavel com 161 paletas de cores, 57 combinacoes tipograficas, 50+ estilos visuais, 161 tipos de produto e 99 diretrizes de UX
- **Gerador de design system**: recomenda automaticamente estilo, cores, tipografia e efeitos baseado no tipo de produto e industria
- **Suporte a marca**: `brand.json` opcional para identidade visual consistente em todas as imagens
- **Zero configuracao**: funciona direto da caixa com padroes sensiveis, sem configuracao necessaria

## Instalacao

### 1. Copie a skill para o seu projeto

```bash
# A partir deste repo
cp -r skill/ /caminho/do/seu-projeto/.claude/skills/html-image-gen/
```

Ou clone diretamente:

```bash
cd /caminho/do/seu-projeto
mkdir -p .claude/skills
git clone https://github.com/SEU_USER/html-image-gen-skill .claude/skills/html-image-gen
```

### 2. Instale o Puppeteer

```bash
cd /caminho/do/seu-projeto
npm install puppeteer
```

### 3. (Opcional) Crie um brand.json

```json
{
  "company": {
    "name": "Sua Empresa",
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

### 4. Comece a usar

Abra o Claude Code no seu projeto e peca:

- "Gere um post de Instagram sobre o lancamento do nosso novo produto"
- "Crie uma imagem OG para o blog post em /content/meu-post.md"
- "Faca uma thumbnail do YouTube com tema escuro"
- "Design um banner do LinkedIn para a pagina da empresa"

## Como Funciona

1. O Claude le o SKILL.md e entende seu pedido
2. Ele gera um arquivo HTML auto-contido com CSS inline e Google Fonts
3. O HTML e renderizado em PNG via Puppeteer em resolucao 2x
4. O Claude mostra a imagem e itera com base no seu feedback

## Script de Renderizacao Standalone

O script de renderizacao tambem pode ser usado diretamente:

```bash
# Uso basico
node .claude/skills/html-image-gen/scripts/render.js input.html output.png

# Com formato pre-definido
node .claude/skills/html-image-gen/scripts/render.js input.html output.png --format story

# Dimensoes customizadas
node .claude/skills/html-image-gen/scripts/render.js input.html output.png --width 1200 --height 630

# Via stdin
cat template.html | node .claude/skills/html-image-gen/scripts/render.js --stdin -o output.png
```

## Formatos Disponiveis

| Formato          | Dimensoes    | Uso                               |
|-----------------|--------------|-----------------------------------|
| `feed`          | 1080 x 1080  | Posts quadrados Instagram/Facebook |
| `story`         | 1080 x 1920  | Stories/Reels Instagram/Facebook  |
| `carousel`      | 1080 x 1080  | Slides de carrossel Instagram     |
| `portrait`      | 1080 x 1350  | Posts retrato Instagram           |
| `banner`        | 1200 x 628   | Banners Facebook/LinkedIn         |
| `twitter-post`  | 1200 x 675   | Posts Twitter/X                   |
| `og-image`      | 1200 x 630   | Imagens Open Graph                |
| `youtube-thumb`  | 1280 x 720  | Thumbnails YouTube                |
| `square`        | 1080 x 1080  | Formato quadrado geral            |
| `landscape`     | 1920 x 1080  | Formato paisagem/apresentacao     |

## Inteligencia de Design

A skill inclui um banco de dados de design completo e pesquisavel:

- **161 paletas de cores** por industria e tipo de produto
- **57 combinacoes tipograficas** com URLs do Google Fonts e palavras-chave de humor
- **50+ estilos visuais** com snippets CSS (glassmorphism, neubrutalism, aurora, etc.)
- **161 padroes de tipo de produto** com recomendacoes de layout e CTA
- **99 diretrizes de UX** cobrindo acessibilidade, touch targets, animacao, formularios
- **Gerador de design system** que combina tudo acima em uma unica recomendacao

Alem de diretrizes integradas para hierarquia visual, escalas tipograficas, espacamento, composicao e acessibilidade.

### Pre-requisitos

- Node.js (para renderizacao via Puppeteer)
- Python 3 (para buscas de inteligencia de design — sem dependencias externas)

Veja [skill/SKILL.md](skill/SKILL.md) para a referencia completa.

## Licenca

MIT
