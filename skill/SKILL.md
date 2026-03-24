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

## Como Funciona

1. Voce escreve um arquivo HTML com CSS inline (auto-contido, arquivo unico)
2. O script de renderizacao abre no navegador headless e tira screenshot
3. Output e um PNG de alta resolucao em escala 2x

## Script de Renderizacao

O script de renderizacao esta em `scripts/render.js` relativo a esta skill. Requer `puppeteer` instalado no projeto.

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

## Setup

O projeto precisa do `puppeteer` instalado:

```bash
npm install puppeteer
# ou
yarn add puppeteer
```

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
    <!-- conteudo aqui -->
  </div>
</body>
</html>
```

Regras principais:
- **Auto-contido**: todo CSS inline, fontes via Google Fonts `@import`
- **Dimensoes fixas**: `.canvas` deve ter `width` e `height` explicitos em px
- **Fotos reais**: baixar do Unsplash, converter para base64, embutir como `data:image/jpeg;base64,...` no CSS `background`
- **Use caminhos `file://`** apenas para imagens locais que o usuario fornece
- **Pense como designer grafico**, nao como desenvolvedor web — veja Secao 5

## Configuracao de Marca (Opcional)

Se o projeto tiver um `brand.json` na raiz, leia-o antes de gerar imagens para respeitar a identidade visual. Estrutura esperada:

```json
{
  "company": {
    "name": "Nome da Empresa",
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

Se nao existir `brand.json`, pergunte ao usuario sobre preferencias de cores ou use uma paleta profissional padrao.

---

## Diretrizes de Design

### 1. Hierarquia Visual (CRITICO)

Toda imagem deve ter um ponto focal claro e no maximo 3 niveis de hierarquia.

**Escala tipografica por formato:**

| Elemento  | Feed/Square (1080px) | Story (1080px larg.) | Banner (1200px) |
|-----------|----------------------|----------------------|-----------------|
| Titulo    | 56 - 80px            | 64 - 96px            | 48 - 72px       |
| Subtitulo | 28 - 36px            | 32 - 42px            | 24 - 32px       |
| Corpo     | 22 - 28px            | 24 - 32px            | 18 - 24px       |
| CTA       | 20 - 26px            | 22 - 28px            | 18 - 22px       |
| Legenda   | 16 - 20px            | 18 - 22px            | 14 - 18px       |

**Regras:**
- Titulo deve ser pelo menos **2x maior** que o texto corpo
- Maximo **2 fontes** por imagem (1 titulo + 1 corpo)
- Peso do titulo: **700 - 900** (bold/black)
- Peso do corpo: **400 - 500** (regular/medium)
- Line-height: **1.0 - 1.15** para titulos, **1.4 - 1.6** para corpo
- Max caracteres por linha: **20 - 25** para titulos, **35 - 45** para corpo
- Max palavras total: **40 - 50** para feed, **20 - 30** para stories

**Anti-patterns (NUNCA faca):**
- Texto menor que 20px (ilegivel no celular)
- Mais de 3 tamanhos de fonte diferentes
- Texto tocando as bordas (sem respiro)
- Titulo e subtitulo com tamanhos parecidos (sem hierarquia)

### 2. Combinacoes Tipograficas

Combinacoes recomendadas do Google Fonts:

| Nome                | Titulo           | Corpo          | Estilo                       | Melhor Para                      |
|---------------------|------------------|----------------|------------------------------|----------------------------------|
| Bold Statement      | Bebas Neue       | Source Sans 3  | Impactante, dramatico        | Marketing, promos, eventos       |
| Startup Bold        | Outfit           | Rubik          | Moderno, confiante           | Startups, lancamentos, tech      |
| Geometric Modern    | Outfit           | Work Sans      | Limpo, equilibrado           | Uso geral, agencias              |
| Modern Professional | Poppins          | Open Sans      | Profissional, amigavel       | SaaS, corporativo, servicos      |
| Tech Startup        | Space Grotesk    | DM Sans        | Futurista, inovador          | Tech, IA, dev tools              |
| Neubrutalist Bold   | Lexend Mega      | Public Sans    | Bold, geometrico             | Gen Z, marketing ousado          |
| Elegant Serif       | Playfair Display | Lato           | Sofisticado, classico        | Luxo, moda, gastronomia          |
| Loud Impact         | Anton            | Epilogue       | Brutal, alto                 | Campanhas virais, streetwear     |
| Clean Corporate     | Montserrat       | Inter          | Versatil, profissional       | Qualquer marca, apresentacoes    |
| Editorial           | DM Serif Display | DM Sans        | Editorial, refinado          | Revistas, blogs, conteudo        |

### 3. Paletas de Cores por Industria

| Industria           | Primaria  | Secundaria | Destaque  | Fundo      | Texto     |
|---------------------|-----------|-----------|-----------|------------|-----------|
| Tech / SaaS         | #2563EB   | #3B82F6   | #8B5CF6   | #EFF6FF    | #1E3A5F   |
| Marketing / Agencia | #EC4899   | #F472B6   | #06B6D4   | #FDF2F8    | #831843   |
| Redes Sociais       | #E11D48   | #FB7185   | #2563EB   | #FFF1F2    | #881337   |
| E-commerce          | #DC2626   | #F59E0B   | #16A34A   | #FFFBEB    | #78350F   |
| Saude               | #059669   | #34D399   | #0891B2   | #ECFDF5    | #064E3B   |
| Educacao            | #7C3AED   | #A78BFA   | #F59E0B   | #F5F3FF    | #4C1D95   |
| Gastronomia         | #EA580C   | #F97316   | #DC2626   | #FFF7ED    | #7C2D12   |
| Financas            | #1E40AF   | #3B82F6   | #059669   | #EFF6FF    | #1E3A5F   |
| Moda / Luxo         | #18181B   | #71717A   | #D4AF37   | #FAFAFA    | #18181B   |
| Fitness / Esportes  | #0F172A   | #334155   | #EF4444   | #F8FAFC    | #0F172A   |
| Imobiliario         | #14532D   | #166534   | #CA8A04   | #F0FDF4    | #14532D   |
| Criativo / Arte     | #7C3AED   | #EC4899   | #F59E0B   | #FAF5FF    | #3B0764   |

**Regras de cores:**
- Contraste: minimo **4.5:1** entre texto e fundo (WCAG AA)
- Maximo **3 - 4 cores** por imagem
- CTA deve usar uma **cor diferente** de todo o resto
- Fundos escuros: use texto branco (#FFFFFF), opacidade minima 0.9
- Nunca: cinza sobre cinza, neon sobre branco, vermelho sobre verde

### 4. Estilos Visuais

#### Glassmorphism
```css
backdrop-filter: blur(15px);
background: rgba(255, 255, 255, 0.15);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 20px;
```
Melhor para: moderno, premium, tech. Requer um fundo vibrante atras do vidro.

#### Minimalismo
Preto + branco + 1 cor de destaque apenas. Tipografia grande, whitespace extremo.
Melhor para: luxo, editorial, corporativo.

#### Blocos Vibrantes
Formas geometricas ousadas, cores neon, tipografia 32px+, alto contraste.
Melhor para: redes sociais, startups, marcas jovens.

#### Aurora / Gradiente
Gradientes mesh com 2-3 cores complementares, transicoes suaves.
Melhor para: SaaS, agencias criativas, musica.

#### Dark Mode
Fundo #000000 ou #121212, texto branco, destaques neon.
Melhor para: tech, entretenimento, gaming.

#### Neubrutalism
Bordas grossas (3-4px), sombras solidas deslocadas, cores primarias, sem border-radius.
```css
border: 3px solid #000;
box-shadow: 6px 6px 0 #000;
border-radius: 0;
```
Melhor para: Gen Z, marcas disruptivas, marketing ousado.

### 5. Design para Redes Sociais (CRITICO — LEIA PRIMEIRO)

**Isto NAO e web design. Isto e design grafico para redes sociais.**

Posts de redes sociais devem parecer feitos no Canva ou por um designer grafico — NAO como um site, landing page ou UI de app. O maior erro e fazer posts que parecem screenshots de uma pagina web.

#### O que FUNCIONA (faca isto):

- **Fotografia full-bleed** como fundo com overlay de gradiente para legibilidade do texto
- **Texto E o design** — tipografia bold enorme preenchendo o espaco, nao texto pequeno em caixas
- **Elementos minimos** — foto + texto + logo. So isso. Maximo impacto.
- **Fotos reais** do Unsplash (baixar, converter para base64, embutir inline). Sempre prefira fotografia real a formas abstratas
- **Overlays de gradiente** nas fotos: mais escuro embaixo onde o texto vai, transparente em cima onde a foto respira
- **Titulos bold uppercase** — 64-82px, peso 800-900, preenchendo a largura
- **Cores de destaque como realce de texto**, nao como fundo de caixas
- **Elementos de marca sutis**: barras finas de destaque, faixas laterais, logo pequeno — nunca dominando
- **Textura de granulado/ruido** como overlay para calor e sensacao analogica

#### O que NAO funciona (nunca faca isto):

- **Cards com bordas** — isto e um componente de site, nao design de redes sociais
- **Pills/tags que parecem botoes** — labels de texto sim, elementos clicaveis NAO
- **Layouts de grid** — posts nao sao dashboards
- **Multiplas caixas/containers pequenos** — isto grita "landing page"
- **Botoes de CTA** — nao existem botoes no Instagram. Use texto simples com seta (→) no maximo
- **Cards de info com icones** — isto e uma secao de features de um site SaaS
- **Componentes de timeline/stepper** — padrao de UI, nao padrao de design
- **Qualquer coisa que pareca interativa** — imagens de redes sociais sao estaticas, nao finja UI

#### Tecnica de Foto de Fundo:

```bash
# 1. Baixar foto do Unsplash
curl -sL "https://images.unsplash.com/photo-{ID}?w=1100&q=80" -o /tmp/photo.jpg

# 2. Converter para base64
base64 -w0 /tmp/photo.jpg > /tmp/photo-b64.txt

# 3. Injetar no HTML via Python
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

CSS para foto + overlay:
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
    rgba(0, 0, 0, 0.15) 0%,      /* foto visivel no topo */
    rgba(0, 0, 0, 0.10) 25%,
    rgba(0, 0, 0, 0.55) 48%,      /* zona de transicao */
    rgba(0, 0, 0, 0.90) 65%,      /* escuro para texto */
    rgba(0, 0, 0, 0.97) 80%,
    rgba(0, 0, 0, 1) 100%
  );
}
```

#### Bons Layouts para Redes Sociais:

**Feed / Quadrado (1080x1080):**
1. **Foto + texto bold** — foto full-bleed, overlay gradiente, titulo enorme embaixo
2. **Split horizontal** — foto real metade de cima, cor solida/gradiente embaixo com texto grande
3. **Circulo de fundo** — circulo colorido grande centralizado, ilustracoes flutuando, texto bold abaixo
4. **Full tipografico** — fundo escuro solido, apenas texto, letras bold italic uppercase massivas preenchendo o espaco
5. **Split diagonal** — foto com bloco de cor cortando em diagonal

**Story (1080x1920):**
1. **Foto hero** — foto full-bleed com overlay de texto no terco inferior
2. **Impacto empilhado** — texto grande em cima, foto no meio, texto CTA embaixo
3. **Fluxo gradiente** — fundo gradiente suave, texto centralizado, elementos minimos

**Regras de composicao:**
- **Zona segura**: mantenha conteudo importante 60px das bordas (plataformas cortam)
- **Padding**: minimo 40px de todas as bordas
- **Respiro**: pelo menos 30% da area deve ser espaco vazio
- **Logo**: pequeno e sutil, 36-48px, canto superior esquerdo ou centro. Nunca dominante.
- **Menos e mais**: se voce esta adicionando um 4o elemento, remova um

### 6. Elementos Visuais

**Elementos de marca (sutis, nao dominantes):**
- Faixas/barras finas de cor nas bordas (5-8px) — assinatura da marca
- Logo pequeno — nunca maior que o titulo
- Destaques de cor em palavras especificas — chamar atencao sem caixas

**Elementos decorativos:**
- Textura de granulado/ruido como overlay (opacidade 0.03-0.05) para calor
- Blobs de gradiente (position: absolute, opacidade baixa) para profundidade
- CSS `::before` / `::after` para toques decorativos sutis

**Icones (use com moderacao):**
- Apenas quando ilustrando um conceito (documentos flutuantes, graficos)
- SVG inline, estilo consistente
- Parte da composicao, nao dentro de componentes de UI

**O que NAO usar como elementos visuais:**
- Cards ou containers com borda
- Tags em formato de pill
- Formas que parecem botoes
- Barras de progresso ou steppers
- Qualquer elemento que implique interatividade

### 7. Acessibilidade (CRITICO)

Mesmo em imagens estaticas, acessibilidade importa para alcance e legibilidade.

- **Contraste minimo**: 4.5:1 para texto normal, 3:1 para texto grande (48px+)
- **Tamanho minimo de texto**: 20px para feed, 24px para stories
- **Teste gradientes**: verifique contraste nos pontos mais claros E mais escuros
- **Solucao para gradientes**: adicione overlay semi-transparente atras do texto
- **Nao dependa apenas de cor**: use icone + texto para transmitir significado
- **Evite**: vermelho + verde juntos (daltonismo), azul claro sobre branco, amarelo sobre branco

### 8. Busca de Inteligencia de Design

Esta skill inclui um banco de dados pesquisavel integrado. **Sempre use essas buscas** antes de gerar imagens para obter recomendacoes especificas ao contexto.

Todos os scripts sao relativos ao diretorio desta skill. Substitua `<skill-path>` pelo caminho real (ex: `.claude/skills/html-image-gen`).

#### Gerar um Design System Completo (PRIMEIRO PASSO RECOMENDADO)

Para qualquer novo pedido de imagem, execute isto primeiro para obter estilo, cores, tipografia e efeitos de uma vez:

```bash
python3 <skill-path>/scripts/search.py "<tipo_produto> <industria> <palavras-chave>" --design-system [-p "Nome do Projeto"]
```

Exemplo:
```bash
python3 <skill-path>/scripts/search.py "fitness gym moderno bold" --design-system -p "PowerGym"
```

#### Buscas por Dominio Especifico

Use para se aprofundar em uma dimensao especifica:

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

# Padroes de landing page
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain landing -n 5

# Tipos de graficos/visualizacao de dados
python3 <skill-path>/scripts/search.py "<palavra-chave>" --domain chart -n 5
```

#### Quando Buscar

| Situacao | O que Executar |
|----------|----------------|
| Nova imagem, estilo incerto | `--design-system` com contexto do produto |
| Usuario pede "faca parecer com X" | `--domain style "<palavras-chave de X>"` |
| Precisa de cores adequadas a marca | `--domain color "<industria>"` |
| Escolhendo fontes | `--domain typography "<humor>"` |
| Infografico / imagem de dados | `--domain chart "<tipo de grafico>"` |

Os resultados incluem snippets CSS, URLs do Google Fonts, codigos hex e anti-patterns a evitar — use-os diretamente no HTML que voce gerar.

---

## Fluxo de Trabalho

### Passo 1: Consultar Design Learning

**Antes de qualquer coisa**, leia `data/design-learning.md` (relativo a esta skill). Este arquivo contem:
- Conceitos visuais por tema (mapeamento palavra → elemento visual)
- Anti-patterns aprendidos de feedbacks anteriores
- Padroes que funcionaram bem
- O processo criativo a seguir

Responda estas 4 perguntas antes de desenhar:
1. Qual e a mensagem central? (1 frase)
2. Qual emocao/reacao deve provocar? (medo, curiosidade, confianca, urgencia)
3. Qual e a metafora visual? (palavra-chave → elemento visual concreto)
4. O visual reforca o texto? (tampe o texto — da pra adivinhar o tema so pelos visuais?)

Se nao conseguir responder a pergunta 3, busque referencias primeiro. NAO comece a desenhar.

### Passo 2: Entender o Pedido

Extraia da mensagem do usuario:
- **O que**: tipo de imagem (post, banner, thumbnail, imagem OG, etc.)
- **Formato**: dimensoes ou plataforma (Instagram feed, Twitter, etc.)
- **Conteudo**: texto, dados ou informacao a incluir
- **Estilo**: preferencias de estilo mencionadas
- **Industria/contexto**: para busca de design system

### Passo 3: Buscar Recomendacoes de Design

**Sempre execute a busca de design system** antes de gerar HTML:

```bash
python3 <skill-path>/scripts/search.py "<tipo_produto> <industria> <palavras_estilo>" --design-system
```

Isto retorna uma recomendacao completa: estilo, cores (codigos hex), tipografia (com URL do Google Fonts), efeitos e anti-patterns. Use diretamente.

Se o usuario tiver necessidades especificas (ex: "quero tema escuro"), complemente com buscas por dominio:

```bash
python3 <skill-path>/scripts/search.py "dark mode minimal" --domain style -n 3
```

### Passo 4: Verificar Marca

Procure `brand.json` na raiz do projeto. Se existir, **valores da marca sobrescrevem** as recomendacoes da busca para cores, fontes e logo. Os resultados da busca ainda guiam layout, estilo e efeitos.

Se nao existir `brand.json`, use os resultados da busca diretamente.

### Passo 5: Encontrar Foto de Fundo

Para posts de redes sociais, busque no Unsplash uma foto relevante:

1. Busque uma foto que combine com o tema (ex: "container porto" para comex, "reuniao equipe" para corporativo)
2. Baixe: `curl -sL "https://images.unsplash.com/photo-{ID}?w=1100&q=80" -o /tmp/photo.jpg`
3. Verifique se baixou: `file /tmp/photo.jpg` (deve dizer JPEG)
4. Converta para base64 para embutir

Se nenhuma foto se encaixar (posts abstratos/tipograficos), pule este passo e use cores solidas ou gradientes.

### Passo 6: Gerar HTML

Escreva um arquivo HTML auto-contido seguindo:
1. **Secao 5 (Design para Redes Sociais)** — esta e a referencia mais importante
2. As recomendacoes de design system do Passo 2
3. As diretrizes de design neste documento (hierarquia, espacamento, contraste)
4. Identidade visual do Passo 3 (se disponivel)

Consideracoes importantes:
- Pense como designer grafico, nao como desenvolvedor web
- Foto de fundo + overlay gradiente + texto bold = formula comprovada
- Use as dimensoes corretas para o formato escolhido
- Aplique a escala tipografica das diretrizes
- Garanta que as taxas de contraste sejam atendidas (4.5:1 minimo)
- Use Google Fonts via `@import` (URL dos resultados da busca)
- Embutir fotos como data URIs base64
- SEM componentes de UI (cards, botoes, pills, timelines)

### Passo 7: Renderizar para PNG

Execute o script de renderizacao:

```bash
node <skill-path>/scripts/render.js <arquivo-html> <output.png> --format <formato>
```

### Passo 8: Mostrar e Iterar

Mostre a imagem gerada ao usuario. Pergunte se querem ajustes. Ajustes comuns:
- "maior/menor" — ajustar tamanhos de fonte
- "mais escuro/claro" — ajustar cores de fundo/texto
- "mais espaco" — aumentar padding
- "mudar a cor" — executar `--domain color` com novas palavras-chave
- "estilo diferente" — executar `--domain style` com novas palavras-chave
- "adicionar mais texto" — mas avise se exceder contagem de palavras recomendada

## Checklist Pre-Entrega

Antes de entregar qualquer imagem:

**Qualidade de design:**
- [ ] Parece um post de Canva/design grafico, NAO um screenshot de site
- [ ] Usa fotografia real como fundo (quando aplicavel) com overlay gradiente adequado
- [ ] Texto e o heroi — bold, grande, preenchendo o espaco
- [ ] Sem componentes de UI: sem cards com borda, sem pills que parecem botoes, sem componentes stepper/timeline
- [ ] Maximo 3-4 elementos total (foto + texto + logo + um destaque)

**Tipografia:**
- [ ] Hierarquia clara: titulo > subtitulo > corpo > legenda
- [ ] Maximo 2 fontes, maximo 4 cores
- [ ] Peso do titulo bold (700+), 64-82px para feed
- [ ] Tamanho minimo de texto 20px (feed) / 24px (story)

**Tecnico:**
- [ ] Contraste do texto >= 4.5:1 contra o fundo
- [ ] Padding >= 40px das bordas, zona segura de 60px respeitada
- [ ] Pelo menos 30% de espaco vazio / respiro
- [ ] Estilo consistente em toda a imagem
- [ ] Cores/fontes da marca respeitadas (se brand.json existir)
- [ ] Foto carregada e embutida como base64 (nao URL externa)
