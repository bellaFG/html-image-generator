# Gerador de Imagens HTML — Skill do Claude Code

Uma skill do Claude Code que transforma o Claude no **designer da sua empresa**. Gera imagens PNG de alta qualidade a partir de HTML/CSS, com consciencia de marca, aprendizado continuo e planejamento de conteudo.

## O que faz

O Claude atua como designer que **conhece sua marca** — na primeira interacao, pesquisa ativamente seu site/Instagram, sugere identidade visual e aprende com cada geracao. A partir dai, todas as imagens saem on-brand sem voce precisar repetir instrucoes.

### Funcionalidades

- **10 formatos pre-definidos**: feed, story, carousel, portrait, banner, twitter-post, og-image, youtube-thumb, square, landscape
- **Renderizacao retina 2x** via Puppeteer headless browser
- **Onboarding colaborativo**: pesquisa ativa no site/Instagram + conversa pra definir identidade visual
- **Inteligencia de design integrada** (powered by UI/UX Pro Max): 161 paletas, 57 tipografias, 50+ estilos, 99 diretrizes UX
- **Contexto persistente**: `brand.json` + `company.md` + memoria do Claude Code
- **Campanhas**: series de posts com identidade visual coesa e variacao controlada
- **Templates reutilizaveis**: salve posts aprovados como base para futuros
- **Biblioteca de assets**: prioriza fotos proprias sobre stock
- **Calendario brasileiro**: feriados nacionais, SP, RJ + 40 datas comerciais + meses tematicos
- **Aprendizado continuo**: historico de geracoes, anti-patterns, sugestao de variacao
- **Revisao de identidade**: alerta automatico quando e hora de revisar a marca

## Instalacao

### 1. Copie a skill para o seu projeto

```bash
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

### 3. Comece a usar

Abra o Claude Code no seu projeto e peca:

- "Gere um post de Instagram sobre o lancamento do nosso novo produto"
- "Vamos configurar a identidade visual da empresa"
- "Cria uma campanha de Black Friday com 5 posts"
- "Faca uma thumbnail do YouTube com tema escuro"

Na primeira vez, o Claude vai sugerir um onboarding pra conhecer sua marca. Leva uns 5 minutos e a partir dai tudo sai on-brand.

## Como Funciona

```
Pedido do usuario
  |
  [1] Carregar contexto (brand.json + company.md + historico)
  [2] Consultar conceitos visuais (design-learning.md)
  [3] Verificar assets proprios → templates → design system
  [4] Gerar HTML auto-contido
  [5] Renderizar PNG via Puppeteer (2x retina)
  [6] Mostrar, iterar, aprender
```

### Arquivos do projeto (gerados no onboarding)

| Arquivo | O que contem |
|---------|-------------|
| `brand.json` | Cores, fontes, logo, estilo preferido, layouts |
| `company.md` | Voz, tom, publico, pilares de conteudo, calendario |
| `.image-gen/assets/` | Fotos proprias (equipe, produtos, escritorio) |
| `.image-gen/templates/` | Templates pre-aprovados |
| `.image-gen/campaigns/` | Campanhas ativas com regras visuais |
| `.image-gen/history/` | Historico de geracoes (aprovacoes, rejeicoes, feedback) |

## Script de Renderizacao Standalone

```bash
# Com formato pre-definido
node .claude/skills/html-image-gen/scripts/render.js input.html output.png --format feed

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

Banco de dados pesquisavel integrado:

- **161 paletas de cores** por industria e tipo de produto
- **57 combinacoes tipograficas** com URLs do Google Fonts
- **50+ estilos visuais** com snippets CSS (glassmorphism, neubrutalism, aurora, etc.)
- **161 padroes de tipo de produto** com recomendacoes de layout
- **99 diretrizes de UX** (acessibilidade, touch targets, animacao, formularios)
- **Gerador de design system** que combina tudo em uma unica recomendacao

### Pre-requisitos

- Node.js (para renderizacao via Puppeteer)
- Python 3 (para buscas de design — sem dependencias externas)

## Estrutura da Skill

```
skill/
  SKILL.md                    # Entrada principal
  docs/
    design-guidelines.md      # Hierarquia, tipografia, cores, estilos, acessibilidade
    social-media-rules.md     # Design grafico para redes sociais (CRITICO)
    workflow.md               # Fluxo de 11 passos + campanhas + revisao
    onboarding-guide.md       # Roteiro do onboarding colaborativo
  scripts/
    render.js                 # HTML → PNG via Puppeteer
    search.py                 # CLI de busca BM25
    core.py                   # Motor BM25 + configs CSV
    design_system.py          # Gerador de design system
    context.py                # Consolida contexto da empresa
  data/
    design-learning.md        # Conceitos visuais, metaforas, anti-patterns
    calendario-brasil.md      # Feriados + datas comerciais (BR, SP, RJ)
    *.csv                     # Banco de dados de design
  templates/
    _exemplo/                 # Template de referencia
```

Veja [skill/SKILL.md](skill/SKILL.md) para a referencia completa.

## Licenca

MIT
