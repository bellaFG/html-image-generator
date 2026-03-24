# Skill de Geracao de Imagens HTML

Este repositorio contem uma skill do Claude Code para gerar imagens de alta qualidade a partir de HTML/CSS.

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

### Suporte a marca

Crie um `brand.json` na raiz do seu projeto para que todas as imagens sigam a identidade visual da sua marca. Veja o SKILL.md para o formato esperado.
