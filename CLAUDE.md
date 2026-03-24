# Skill de Geracao de Imagens HTML

Este repositorio contem uma skill do Claude Code que transforma o Claude no **designer da empresa** — capaz de gerar imagens de alta qualidade a partir de HTML/CSS, com consciencia de marca, aprendizado continuo e planejamento de conteudo.

## Instalacao

Copie a pasta `skill/` para o diretorio `.claude/skills/html-image-gen/` do seu projeto:

```bash
cp -r skill/ /caminho/do/seu-projeto/.claude/skills/html-image-gen/
```

Depois instale o Puppeteer no seu projeto:

```bash
npm install puppeteer
```

## Uso

Uma vez instalada, o Claude Code usara automaticamente esta skill quando voce pedir para gerar imagens, posts de redes sociais, banners, thumbnails ou qualquer recurso visual.

### Exemplos rapidos

- "Gere um post de Instagram anunciando nossa nova feature"
- "Crie uma imagem OG para este blog post"
- "Faca uma thumbnail do YouTube com o titulo 'Top 10 Dicas'"
- "Design um banner para nossa Black Friday"
- "Vamos configurar a identidade visual da empresa"
- "Cria uma campanha de 5 posts pro lancamento do produto"

### Contexto da empresa

O Claude atua como designer da empresa. Na primeira interacao, ele faz um **onboarding colaborativo** — pesquisa o site/Instagram, sugere paleta, fontes e estilo, e gera:

- **`brand.json`** — identidade visual (cores, fontes, logo, estilo)
- **`company.md`** — voz, tom, publico, pilares de conteudo, calendario
- **`.image-gen/`** — assets, templates, campanhas e historico

A partir dai, todas as imagens seguem a identidade da marca automaticamente.

## Estrutura da Skill

```
skill/
  SKILL.md                    # Entrada principal (quando usar, formatos, busca, checklist)
  docs/
    design-guidelines.md      # Hierarquia, tipografia, cores, estilos, acessibilidade
    social-media-rules.md     # CRITICO: design grafico, nao web design
    workflow.md               # Fluxo completo de 11 passos + campanhas + revisao
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
    _exemplo/                 # Template de referencia com placeholders
```

## Referencia completa

Veja [skill/SKILL.md](skill/SKILL.md) para a documentacao completa da skill.
