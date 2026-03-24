# Fluxo de Trabalho

Fluxo completo desde o pedido do usuario ate a entrega da imagem.

---

## Visao Geral

```
PEDIDO DO USUARIO
  |
  [1] Carregar contexto (brand.json + company.md + memoria)
  |
  [2] Detectar onboarding (se sem contexto → docs/onboarding-guide.md)
  |
  [3] Entender o pedido (tipo, formato, conteudo, estilo, industria)
  |
  [4] Consultar design-learning.md (4 perguntas criativas)
  |
  [5] Verificar assets proprios (.image-gen/assets/)
  |
  [6] Verificar templates (.image-gen/templates/)
  |
  [7] Buscar design system (search.py --design-system)
  |
  [8] Consultar historico (variacao controlada)
  |
  [9] Gerar HTML
  |
  [10] Renderizar (render.js)
  |
  [11] Mostrar + Iterar + Aprender
```

---

## Passo 1: Carregar Contexto

Antes de qualquer coisa, executar o script de contexto:

```bash
python3 <skill-path>/scripts/context.py --project-root <raiz-do-projeto>
```

O script consolida automaticamente:
- **`brand.json`** → identidade visual (cores, fontes, logo)
- **`company.md`** → voz, tom, publico, pilares, calendario
- **Templates, campanhas, assets, historico** → tudo em `.image-gen/`
- **Alertas** → variacao de layout, revisao de identidade, datas proximas

**Se a saida disser "Sem Contexto de Empresa"** → disparar onboarding (ver `docs/onboarding-guide.md`).

**Se o usuario pedir uma imagem e nao houver contexto**, nao pule o onboarding — pergunte:
> "Vi que este projeto ainda nao tem identidade visual configurada. Quer que eu configure agora (leva uns 5 minutos) ou prefere gerar a imagem com um estilo generico?"

---

## Passo 2: Consultar Design Learning

**Antes de desenhar**, leia `data/design-learning.md` (relativo a esta skill). Responda estas 4 perguntas:

1. Qual e a mensagem central? (1 frase)
2. Qual emocao/reacao deve provocar? (medo, curiosidade, confianca, urgencia)
3. Qual e a metafora visual? (palavra-chave → elemento visual concreto)
4. O visual reforca o texto? (tampe o texto — da pra adivinhar o tema so pelos visuais?)

Se nao conseguir responder a pergunta 3, busque referencias primeiro. NAO comece a desenhar.

---

## Passo 3: Entender o Pedido

Extraia da mensagem do usuario:

- **O que**: tipo de imagem (post, banner, thumbnail, imagem OG, etc.)
- **Formato**: dimensoes ou plataforma (Instagram feed, Twitter, etc.)
- **Conteudo**: texto, dados ou informacao a incluir
- **Estilo**: preferencias de estilo mencionadas
- **Industria/contexto**: para busca de design system
- **Campanha**: se faz parte de uma campanha ativa (verificar `.image-gen/campaigns/`)

---

## Passo 4: Verificar Assets Proprios

Se o projeto tem `.image-gen/assets/`, verificar ANTES de ir ao Unsplash:

| Pasta | Quando usar |
|-------|-------------|
| `assets/equipe/` | Posts sobre equipe, cultura, bastidores |
| `assets/produtos/` | Posts de produto, lancamentos, promos |
| `assets/escritorio/` | Posts institucionais, vagas, eventos |
| `assets/icones/` | Icones customizados da marca |
| `assets/logo.png` | Logo principal |
| `assets/logo-white.png` | Logo para fundos escuros |

**Regra: fotos proprias > Unsplash quando relevante.**

Para usar um asset local no HTML:
```html
<!-- Converter para base64 antes de embutir -->
background: url('data:image/jpeg;base64,...') center / cover;
```

```bash
# Converter asset local para base64
base64 -w0 .image-gen/assets/produtos/foto.jpg
```

Se nao tem assets proprios → Unsplash normalmente.

---

## Passo 5: Verificar Templates

Se o projeto tem `.image-gen/templates/`, verificar se existe template que encaixe:

1. Ler `meta.json` de cada template — comparar `tags`, `format` e `style` com o pedido
2. Se encontrar match → ler `template.html`, substituir `{{PLACEHOLDERS}}` pelo conteudo real
3. Se nao → gerar do zero

**Como usar um template:**
```bash
# Ler o meta.json pra entender os placeholders
cat .image-gen/templates/promo-basico/meta.json

# Copiar o template e substituir os placeholders
cp .image-gen/templates/promo-basico/template.html post.html
# Substituir {{TITULO}}, {{FOTO_B64}}, etc. no post.html
```

**Como salvar um novo template** (apos aprovacao excepcional do usuario):
```bash
mkdir -p .image-gen/templates/nome-do-template
cp post.html .image-gen/templates/nome-do-template/template.html
# Criar meta.json com name, format, tags, style, placeholders
```

Um template de referencia esta em `<skill-path>/templates/_exemplo/`.

---

## Passo 6: Buscar Design System

**Sempre execute a busca de design system** antes de gerar HTML:

```bash
python3 <skill-path>/scripts/search.py "<tipo_produto> <industria> <palavras_estilo>" --design-system
```

Retorna recomendacao completa: estilo, cores (hex), tipografia (Google Fonts URL), efeitos e anti-patterns.

Se o usuario tiver necessidades especificas, complemente com buscas por dominio:

```bash
python3 <skill-path>/scripts/search.py "dark mode minimal" --domain style -n 3
```

**Prioridade de aplicacao:**
1. `brand.json` sobrescreve cores, fontes e logo
2. `campaign.json` sobrescreve estilo dentro de campanhas ativas
3. Busca de design system guia layout, estilo e efeitos

---

## Passo 7: Consultar Historico

Se existir `.image-gen/history/log.jsonl`, analisar ultimas geracoes:

- **Variacao**: se ultimos 3+ posts usaram mesmo layout → sugerir variacao
- **Campanha**: se post pertence a campanha ativa → seguir `visual_rules` da campanha
- **Anti-patterns**: evitar estilos que foram rejeitados anteriormente

---

## Passo 8: Encontrar Foto de Fundo

Para posts de redes sociais que precisam de foto:

1. Verificar assets proprios primeiro (Passo 4)
2. Se nao tem → buscar no Unsplash foto relevante ao tema
3. Baixar: `curl -sL "https://images.unsplash.com/photo-{ID}?w=1100&q=80" -o /tmp/photo.jpg`
4. Verificar: `file /tmp/photo.jpg` (deve dizer JPEG)
5. Converter para base64 para embutir

Se o post e abstrato/tipografico, pule e use cores solidas ou gradientes.

---

## Passo 9: Gerar HTML

Escreva um arquivo HTML auto-contido seguindo:

1. **`docs/social-media-rules.md`** — referencia mais importante para redes sociais
2. **`docs/design-guidelines.md`** — hierarquia, tipografia, cores, acessibilidade
3. Recomendacoes do design system (Passo 6)
4. Identidade visual do brand.json (se disponivel)
5. Regras da campanha (se aplicavel)

Consideracoes:
- Pense como designer grafico, nao como desenvolvedor web
- Foto + overlay gradiente + texto bold = formula comprovada
- Use dimensoes corretas para o formato
- Aplique a escala tipografica das diretrizes
- Garanta contraste >= 4.5:1
- Google Fonts via `@import`
- Fotos como data URIs base64
- SEM componentes de UI (cards, botoes, pills, timelines)

---

## Passo 10: Renderizar para PNG

```bash
node <skill-path>/scripts/render.js <arquivo-html> <output.png> --format <formato>
```

---

## Passo 11: Mostrar, Iterar e Aprender

### Mostrar e iterar

Mostre a imagem ao usuario. Ajustes comuns:
- "maior/menor" → ajustar tamanhos de fonte
- "mais escuro/claro" → ajustar cores
- "mais espaco" → aumentar padding
- "mudar a cor" → buscar `--domain color`
- "estilo diferente" → buscar `--domain style`

### Registrar no historico

Apos a entrega final (aprovacao ou rejeicao), adicionar uma linha ao `.image-gen/history/log.jsonl`:

```jsonl
{"date":"2026-03-24","prompt":"post Black Friday","format":"feed","campaign":"black-friday-2026","template":null,"style":"photo-overlay","layout":"dark-overlay","assets_used":["assets/produtos/caixa.jpg"],"approved":true,"feedback":null}
```

**Schema do log.jsonl** (uma linha JSON por geracao):

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `date` | string | Data da geracao (YYYY-MM-DD) |
| `prompt` | string | Resumo do pedido do usuario |
| `format` | string | Formato usado (feed, story, banner, etc.) |
| `campaign` | string/null | Nome da campanha (se aplicavel) |
| `template` | string/null | Nome do template usado (se aplicavel) |
| `style` | string | Estilo visual (photo-overlay, aurora, minimal, etc.) |
| `layout` | string | Layout usado (dark-overlay, split-horizontal, tipografico, etc.) |
| `assets_used` | array | Caminhos dos assets usados (proprios ou "unsplash:{id}") |
| `approved` | boolean | Se o usuario aprovou |
| `feedback` | string/null | Feedback do usuario (especialmente em rejeicoes) |

### Aprender com o resultado

**Se aprovado:**
1. Registrar no `log.jsonl`
2. Se um padrao se repete (ex: usuario sempre aprova dark mode) → salvar na memoria do Claude Code
3. Se o resultado foi excepcional → oferecer salvar como template:
   > "Esse ficou muito bom! Quer que eu salve como template pra usar de base no futuro?"

**Se rejeitado:**
1. Registrar no `log.jsonl` com feedback
2. Salvar anti-pattern na memoria do Claude Code (ex: "empresa X nao gosta de minimalismo puro")
3. Ajustar e iterar — nao repetir o mesmo erro

**Se parte de campanha:**
1. Atualizar `campaign.json` com status do post (`approved`/`rejected`)
2. Se aprovado, registrar arquivo em `posts`

### O que salvar na memoria vs no log

| Informacao | Onde salvar | Por que |
|------------|-------------|---------|
| Fato pontual (data, formato, estilo usado) | `log.jsonl` | Historico factual, analisado por `context.py` |
| Preferencia persistente ("gosta de dark mode") | Memoria Claude Code | Influencia decisoes futuras |
| Anti-pattern ("nao gosta de minimalismo") | Memoria Claude Code | Evitar repeticao em conversas futuras |
| Padrao aprovado recorrente | Memoria Claude Code | Reforcar o que funciona |
| Feedback especifico de uma geracao | `log.jsonl` | Contexto pontual, nao generalizar |

**Regra**: log.jsonl = fatos. Memoria = padroes e preferencias generalizaveis.

### Variacao controlada

O `context.py` analisa o historico automaticamente e gera alertas:
- **Repeticao de layout**: se ultimos 3+ posts usaram mesmo layout → sugere variar
- **Repeticao de estilo**: se ultimos 3+ posts usaram mesmo estilo → sugere variar
- **Taxa de aprovacao baixa**: se < 50% em 5+ geracoes → sugere revisar abordagem
- **Anti-patterns acumulados**: lista rejeicoes com feedback pra evitar

**Fora de campanha**: variar livremente (layout, estilo, composicao).
**Dentro de campanha**: manter layout base, variar apenas foto/texto/detalhe (conforme `variation_strategy` do `campaign.json`).

---

## Adaptacao por Formato

O tom visual deve se adaptar ao formato de saida:

| Contexto | Formatos | Tom Visual |
|----------|----------|------------|
| Instagram | feed, story, carrossel | Design grafico (Canva-like), ousado |
| LinkedIn | post, banner | Mais corporativo, menos ousado |
| Apresentacoes | 1920x1080 landscape | Limpo, hierarquico, dados |
| Propostas | A4 portrait/landscape | Formal, marca sutil |
| OG Images | 1200x630 | Legivel em miniatura |
| YouTube | 1280x720 | Thumbnail impactante, rosto + texto |

---

## Campanhas

Uma campanha e um grupo de imagens com **identidade visual coesa**. Vive em `.image-gen/campaigns/{nome}/`.

### Quando Criar uma Campanha

- Serie de posts com tema comum (ex: "Black Friday", "Lancamento Feature X", "Semana do Cliente")
- Qualquer sequencia de 3+ posts que devem ter consistencia visual entre si
- Usuario pede explicitamente ("vamos fazer uma campanha de...")

### Estrutura

```
.image-gen/campaigns/{nome-campanha}/
  campaign.json     # Regras visuais e status
  posts/            # Posts gerados
    post-1.html
    post-1.png
    post-2.html
    ...
```

### campaign.json

```json
{
  "name": "Black Friday 2026",
  "description": "Serie de contagem regressiva para Black Friday",
  "status": "active",
  "created": "2026-11-01",
  "format": "feed",
  "total_planned": 5,
  "visual_rules": {
    "color_override": { "accent": "#FF0000" },
    "layout": "dark-mode + photo-overlay",
    "typography_override": null,
    "recurring_elements": "numero de contagem grande, barra vermelha no topo",
    "variation_strategy": "mesmo layout base, variar foto e texto"
  },
  "posts": [
    { "name": "post-1-faltam-7-dias", "status": "approved", "file": "posts/post-1.html" },
    { "name": "post-2-faltam-3-dias", "status": "pending" }
  ]
}
```

### Fluxo de Criacao

1. Usuario pede campanha → definir nome, descricao, quantidade de posts, formato
2. Definir `visual_rules` juntos: que layout base, que cores, que elementos recorrentes
3. Gerar o primeiro post da campanha
4. Se aprovado → esse vira a base visual. Os proximos seguem o mesmo esqueleto
5. Para cada post seguinte: manter layout base, variar foto/texto/detalhe conforme `variation_strategy`

### Variacao Controlada Dentro de Campanha

- **Manter**: layout base, paleta de cores, tipografia, elementos recorrentes
- **Variar**: foto de fundo, texto principal, detalhes decorativos menores
- **Objetivo**: quem ve 3 posts da campanha no feed reconhece que sao da mesma serie

### Finalizando uma Campanha

Quando todos os posts estiverem aprovados ou o usuario encerrar:
```json
{ "status": "completed" }
```

Campanhas completas servem de referencia para futuras campanhas similares.

---

## Calendario de Referencia

Para planejamento de conteudo, consultar `data/calendario-brasil.md` que contem:
- Feriados nacionais
- Feriados estaduais (SP e RJ)
- Datas comerciais (Dia das Maes, Black Friday, Dia do Cliente, etc.)
- Meses tematicos (Outubro Rosa, Novembro Azul, etc.)

O `context.py` automaticamente alerta sobre datas proximas (30 dias) baseado no calendario do `company.md`.

---

## Revisao de Identidade

A marca evolui. O sistema detecta quando e hora de revisar.

### Triggers Automaticos

O `context.py` sugere revisao quando detecta:

| Trigger | Condicao | Por que |
|---------|----------|---------|
| Tempo | > 3 meses desde `ultima_revisao` | Marcas evoluem, preferencias mudam |
| Rejeicoes | Taxa de aprovacao < 50% em 5+ geracoes | O estilo atual nao esta funcionando |
| Feedback recorrente | Mesmo feedback negativo aparece 2+ vezes | Problema sistematico, nao pontual |
| Pedido explicito | Usuario pede | Sempre atender |

### Revisao Parcial

Ajustar apenas um aspecto sem refazer tudo:
- "Vamos mudar so as cores" → editar `brand.json > colors`
- "Quero fontes diferentes" → editar `brand.json > typography`
- "Mudar o estilo pra algo mais ousado" → editar `brand.json > style`
- "Atualizar o calendario" → editar `company.md > Calendario`

Apos ajuste, atualizar `ultima_revisao` no `company.md`.

### Revisao Completa

Rodar o onboarding novamente, mas mostrando valores atuais como default:
> "A identidade atual esta assim: [cores], [fontes], [estilo]. O que quer mudar?"

Permite manter o que funciona e ajustar o que nao funciona. Ao final, reescrever `brand.json` e `company.md` com os novos valores e atualizar `ultima_revisao`.
