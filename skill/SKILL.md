# Gerador de Imagens HTML

Gera imagens de alta qualidade (PNG) a partir de HTML/CSS. Suporta posts de redes sociais, banners, imagens OG, thumbnails e qualquer recurso visual que possa ser expresso como HTML.

Inclui um banco de dados de inteligencia de design integrado (powered by UI/UX Pro Max) com 161 paletas de cores, 57 combinacoes tipograficas, 50+ estilos visuais, 161 tipos de produto e 99 diretrizes de UX — todos pesquisaveis via scripts Python.

## Quando Aplicar

### Deve Usar

- Usuario pede para **gerar uma imagem**, post, banner, thumbnail ou recurso visual
- Usuario pede para **criar conteudo de redes sociais** (Instagram, Twitter/X, LinkedIn, YouTube)
- Usuario pede para **criar** um card, flyer, badge, certificado ou infografico
- Usuario pede para criar **imagens OG** ou previews open graph
- Usuario quer **converter HTML para PNG/imagem**

### Pular

- Usuario quer editar uma imagem raster existente (edicao de fotos)
- Usuario precisa de output apenas SVG sem rasterizacao
- Tarefa e desenvolvimento de UI puro (paginas web, apps) — nao geracao de imagem

---

## Documentacao

| Documento | Conteudo |
|-----------|----------|
| **[docs/design-guidelines.md](docs/design-guidelines.md)** | Hierarquia visual, tipografia, cores, estilos, elementos, acessibilidade |
| **[docs/social-media-rules.md](docs/social-media-rules.md)** | CRITICO: "Isto NAO e web design" — regras de design grafico para redes sociais |
| **[docs/workflow.md](docs/workflow.md)** | Fluxo completo de 11 passos: contexto → onboarding → geracao → aprendizado |
| **[docs/onboarding-guide.md](docs/onboarding-guide.md)** | Roteiro do onboarding colaborativo com pesquisa ativa |
| **[data/design-learning.md](data/design-learning.md)** | Conceitos visuais, metaforas, anti-patterns, padroes que funcionaram |
| **[data/calendario-brasil.md](data/calendario-brasil.md)** | Feriados nacionais, SP, RJ + datas comerciais + meses tematicos |

**Ordem de leitura para primeira geracao:**
1. `docs/social-media-rules.md` — entender a estetica correta
2. `data/design-learning.md` — processo criativo e conceitos visuais
3. `docs/workflow.md` — seguir o fluxo completo
4. `docs/design-guidelines.md` — consultar referencia tecnica conforme necessidade

---

## Contexto da Empresa

O Claude atua como **designer da empresa**. Antes de gerar qualquer imagem, carregar o contexto:

```bash
python3 <skill-path>/scripts/context.py --project-root <raiz-do-projeto>
```

O script consolida: brand.json, company.md, templates, campanhas, assets, historico e alertas.

- **Se retornar "Sem Contexto"** → seguir `docs/onboarding-guide.md` para configurar
- **Se retornar contexto** → usar como base. Valores da marca sobrescrevem recomendacoes da busca
- **Alertas** → agir sobre variacao de layout, revisao de identidade, datas proximas

---

## Script de Renderizacao

O script esta em `scripts/render.js` relativo a esta skill. Requer `puppeteer` instalado no projeto.

```bash
# Renderizar um arquivo HTML para PNG
node <skill-path>/scripts/render.js input.html output.png --format feed

# Com dimensoes customizadas
node <skill-path>/scripts/render.js input.html output.png --width 1200 --height 630

# Via stdin
cat template.html | node <skill-path>/scripts/render.js --stdin -o output.png --format story
```

### Formatos Disponiveis

| Formato         | Dimensoes    | Uso                               |
|----------------|--------------|-----------------------------------|
| `feed`         | 1080 x 1080  | Posts quadrados Instagram/Facebook |
| `story`        | 1080 x 1920  | Stories/Reels Instagram/Facebook  |
| `carousel`     | 1080 x 1080  | Slides de carrossel Instagram     |
| `portrait`     | 1080 x 1350  | Posts retrato Instagram           |
| `banner`       | 1200 x 628   | Banners Facebook/LinkedIn         |
| `twitter-post` | 1200 x 675   | Posts Twitter/X                   |
| `og-image`     | 1200 x 630   | Imagens Open Graph                |
| `youtube-thumb` | 1280 x 720  | Thumbnails YouTube                |
| `square`       | 1080 x 1080  | Formato quadrado geral            |
| `landscape`    | 1920 x 1080  | Formato paisagem/apresentacao     |

Todos renderizados em escala 2x por padrao (ex: feed = 2160x2160px real).

---

## Estrutura do Template HTML

Sempre use esta estrutura base para imagens geradas:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=...');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    .canvas {
      width: {LARGURA}px;
      height: {ALTURA}px;
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
    <!-- conteudo aqui -->
  </div>
</body>
</html>
```

Regras:
- **Auto-contido**: todo CSS inline, fontes via Google Fonts `@import`
- **Dimensoes fixas**: `.canvas` deve ter `width` e `height` explicitos em px
- **Fotos reais**: baixar do Unsplash, converter para base64, embutir como `data:image/jpeg;base64,...`
- **Use caminhos `file://`** apenas para imagens locais que o usuario fornece
- **Pense como designer grafico**, nao como desenvolvedor web — veja `docs/social-media-rules.md`

---

## Busca de Inteligencia de Design

Banco de dados pesquisavel integrado. **Sempre use antes de gerar imagens.**

Todos os scripts sao relativos ao diretorio desta skill. Substitua `<skill-path>` pelo caminho real.

### Design System Completo (PRIMEIRO PASSO)

```bash
python3 <skill-path>/scripts/search.py "<tipo_produto> <industria> <palavras-chave>" --design-system [-p "Nome do Projeto"]
```

### Buscas por Dominio

```bash
# Paletas de cores por industria (161 paletas)
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain color -n 5

# Combinacoes tipograficas por humor (57 combinacoes)
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain typography -n 5

# Estilos visuais (50+ estilos)
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain style -n 5

# Padroes por tipo de produto (161 tipos)
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain product -n 5

# Melhores praticas de UX (99 diretrizes)
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain ux -n 5
```

### Quando Buscar

| Situacao | O que Executar |
|----------|----------------|
| Nova imagem, estilo incerto | `--design-system` com contexto do produto |
| Usuario pede "faca parecer com X" | `--domain style "<palavras-chave de X>"` |
| Precisa de cores adequadas a marca | `--domain color "<industria>"` |
| Escolhendo fontes | `--domain typography "<humor>"` |
| Infografico / imagem de dados | `--domain chart "<tipo de grafico>"` |

---

## Checklist Pre-Entrega

Antes de entregar qualquer imagem:

**Design:**
- [ ] Parece post de Canva/design grafico, NAO screenshot de site
- [ ] Usa fotografia real como fundo (quando aplicavel) com overlay gradiente
- [ ] Texto e o heroi — bold, grande, preenchendo o espaco
- [ ] Sem componentes de UI: sem cards, pills, botoes, steppers
- [ ] Maximo 3-4 elementos total (foto + texto + logo + um destaque)

**Tipografia:**
- [ ] Hierarquia clara: titulo > subtitulo > corpo > legenda
- [ ] Maximo 2 fontes, maximo 4 cores
- [ ] Peso do titulo bold (700+), 64-82px para feed
- [ ] Tamanho minimo de texto 20px (feed) / 24px (story)

**Tecnico:**
- [ ] Contraste do texto >= 4.5:1 contra o fundo
- [ ] Padding >= 40px das bordas, zona segura de 60px
- [ ] Pelo menos 30% de espaco vazio / respiro
- [ ] Cores/fontes da marca respeitadas (se brand.json existir)
- [ ] Foto embutida como base64 (nao URL externa)

**Contexto:**
- [ ] brand.json carregado e aplicado (se existir)
- [ ] company.md consultado para tom e voz (se existir)
- [ ] Variacao de layout verificada (nao repetir os ultimos posts)
- [ ] Campanha ativa respeitada (se aplicavel)
