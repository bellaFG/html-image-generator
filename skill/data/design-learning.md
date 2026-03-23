# Design Learning — Conhecimento Visual Acumulado

Este arquivo cresce a cada conversa. Antes de gerar qualquer imagem, consulte este arquivo para encontrar conceitos visuais, metaforas, padroes de layout e licoes aprendidas.

---

## 1. Processo Criativo (seguir SEMPRE)

Antes de abrir o HTML, responda mentalmente:

1. **Qual a mensagem central?** (1 frase)
2. **Qual a emocao/reacao desejada?** (medo, curiosidade, confianca, urgencia)
3. **Qual a metafora visual?** (palavra-chave → elemento visual concreto)
4. **Qual a relacao texto ↔ imagem?** (o visual reforça, complementa ou contrasta o texto?)
5. **Qual a linguagem visual?** (so foto, so ilustracao, so tipografia — NUNCA misturar)
6. **Os elementos conversam?** (imagina todos juntos — parecem do mesmo projeto?)

Se nao conseguir responder o item 3, NAO comece a desenhar. Pesquise referências primeiro.
Se a resposta do item 6 for "nao", redesenhe antes de renderizar.

---

## 1B. Harmonia Visual (regra mais importante)

**O maior erro é misturar linguagens visuais que nao combinam.**

### Linguagens visuais — escolha UMA e mantenha:

| Linguagem | Quando usar | Elementos permitidos |
|---|---|---|
| **Fotografica** | Quando tem foto real de fundo | Foto + texto + formas de cor solida (overlays, barras). SEM ilustracoes cartoon. |
| **Ilustrativa** | Quando nao tem foto | Ilustracoes flat, icones, formas geometricas — tudo no mesmo estilo. SEM fotos reais. |
| **Tipografica** | Quando o texto E o design | Texto grande + fundo solido + formas decorativas sutis. SEM fotos e SEM ilustracoes. |
| **Mista (avancado)** | So se souber integrar | Foto com tratamento de cor que combine com elementos graficos (mesma paleta, mesmo tom). |

### Regras de unidade:

1. **Proximidade**: elementos relacionados ficam perto. Elementos soltos parecem colagem.
2. **Linguagem unica**: todos os elementos visuais devem parecer do MESMO projeto. Foto real + desenho cartoon = colagem.
3. **Repeticao**: repita formas, cores, pesos. Se usou circulo num lugar, use em outro.
4. **Paleta restrita**: max 3 cores. Todas as formas/fundos/textos usam as mesmas cores.
5. **Fluxo visual**: o olho segue um caminho natural (topo → meio → baixo, ou Z-pattern).
6. **Escala proporcional**: elementos devem ter relacao de tamanho entre si, nao aleatoria.

### Teste de harmonia (fazer ANTES de renderizar):

Olhe o design e pergunte:
- Se eu tirar o texto, os elementos visuais parecem do mesmo projeto? ✅
- Tem algum elemento que parece "colado de fora"? Se sim, remova ou adapte. ❌
- Os elementos se conectam visualmente (overlap, proximidade, cor)? ✅
- A composicao tem um fluxo claro? O olho sabe pra onde ir? ✅

---

## 2. Conceitos Visuais por Tema

### Comex / Importacao / Exportacao
| Palavra/Tema | Elemento Visual | Como usar |
|---|---|---|
| Planilha | Planilha/tabela sendo riscada, com X vermelho, quebrando | Mostrar o problema, a planilha como vila |
| DUIMP | Documento com check verde, selos de aprovacao | Mostrar modernizacao, o novo substituindo o velho |
| Multa / Penalidade | Cifrao com alerta vermelho, triangulo de warning | Criar urgencia/medo |
| Container | Containers empilhados coloridos, sendo carregados por guindaste | Contexto portuario real |
| Navio | Navio cargueiro, vista lateral ou aerea | Escala da operacao |
| Porto | Foto real de porto com guindastes | Cenario, contexto, autoridade |
| Embarque | Globo com rotas/linhas, aviao + navio | Movimento, logistica global |
| Classificacao fiscal | Lupa sobre documento, codigo NCM | Detalhe tecnico, precisao |
| ERP / Sistema | Telas/dashboards modernos, dados organizados | Solucao, controle, ordem |
| Desembaraco | Relogio + documento, ampulheta | Tempo, agilidade |
| Catalogo de produtos | Lista organizada, fichas de produto | Organizacao, padronizacao |
| Custo / Margem | Graficos, cifrao, setas subindo/descendo | Impacto financeiro |

### Emocoes / Tom
| Tom desejado | Elementos visuais | Cores dominantes |
|---|---|---|
| Urgencia / Medo | Alerta vermelho, X, coisas quebrando, numeros grandes | Vermelho, laranja, fundo escuro |
| Confianca / Autoridade | Checks verdes, selos, graficos subindo | Azul marinho, verde, branco |
| Curiosidade | Pergunta grande, "?", elementos parcialmente revelados | Cores vibrantes, contraste alto |
| Modernizacao | Antes/depois, velho riscado → novo brilhando | Cinza (velho) vs cores vivas (novo) |

---

## 3. Relacao Texto ↔ Imagem (regra de ouro)

**Todo elemento visual precisa ter relacao direta com o texto.**

- Se o texto fala de "planilha" → mostra planilha (nao um cubo generico)
- Se o texto fala de "importacao" → mostra navio/container (nao formas abstratas)
- Se o texto fala de "multa" → mostra dinheiro/alerta (nao um icone decorativo)

**Teste**: tampe o texto e olhe so os elementos visuais. Da pra adivinhar o tema? Se nao, os visuais estao errados.

---

## 4. Padroes de Layout — Aprendidos de Referencias Reais

### Fonte: 18 referencias analisadas em 2026-03-22
Inclui: posts da Maino, grid GJN Logistics, Azlogistika, Cargo Facil, Dinamica Transportadora, CS Designer, Eleks case study, IBIXPO grid, templates russos de apresentacao, perfil completo @mainotecnologia.

### PADRAO A: Foto recortada + fundo colorido (MAIS COMUM em comex)
**Visto em**: GJN Logistics grid, Azlogistika, Cargo Facil, Maino posts, Eleks
- Foto real (porto, navio, container, aviao, caminhao) recortada com forma organica
- Foto ocupa ~40-50% da area, com recorte diagonal, arredondado ou forma irregular
- Fundo solido colorido (azul marinho, azul royal) na outra metade
- Texto bold por cima ou ao lado da foto
- **Tecnica CSS**: `clip-path` na foto, ou foto posicionada com `border-radius` grande

```
Layout tipico:
┌──────────────────┐
│ LOGO     TAG     │
│                  │
│  ┌────────┐      │
│  │ FOTO   │      │
│  │recortada      │
│  └──/     │      │
│    /      │      │
│   TITULO BOLD    │
│   subtitulo      │
│   @handle        │
└──────────────────┘
```

### PADRAO B: Split horizontal — foto em cima, conteudo embaixo
**Visto em**: Maino post 2 (nova regra), Dinamica Transportadora
- Foto real na metade superior (com ou sem overlay)
- Divisao diagonal ou com faixa de cor (verde na Maino)
- Metade inferior: fundo claro (branco, azul claro, gradiente suave)
- Texto bold escuro (navy) centralizado
- Destaque em cor diferente (laranja para numeros, verde para CTA)

```
┌──────────────────┐
│    FOTO REAL     │
│   (porto/navio)  │
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← faixa colorida diagonal
│                  │
│  TITULO BOLD     │
│  texto destaque  │
│     →  CTA       │
└──────────────────┘
```

### PADRAO C: Circulo grande como fundo + elementos flutuantes
**Visto em**: Maino post 3 (planilha), CS Designer, post "guarda este post"
- Grande circulo/blob de cor como elemento dominante
- Objetos/ilustracoes flutuando sobre o circulo
- Texto bold abaixo ou sobre o circulo
- Fundo pode ser escuro (Maino) ou claro (CS Designer)
- As formas organicas (blobs) dao sensacao moderna

```
┌──────────────────┐
│      LOGO        │
│                  │
│    ╭──────╮      │
│   ╱ CIRCULO╲     │
│  │ilustracoes│   │
│   ╲________╱     │
│                  │
│  TITULO BOLD     │
│  ITALIC VERDE    │
│  subtitulo       │
└──────────────────┘
```

### PADRAO D: Foto pessoa + overlay de conteudo
**Visto em**: Maino post 4 (preparacao e sistemica), IBIXPO, perfil @mainotecnologia
- Foto de pessoa (especialista, CEO, palestrante) como fundo ou lateral
- Overlay escuro ou bloco de cor sobre/ao lado da foto
- Texto como se fosse uma fala/citacao da pessoa
- Passa autoridade e humaniza a marca
- Logo e marca sempre presentes

```
┌──────────────────┐
│ LOGO       marca │
│                  │
│  ┌──── PESSOA    │
│  │       foto    │
│  │               │
│  TEXTO BOLD      │
│  "citacao ou     │
│   afirmacao"     │
│              CTA │
└──────────────────┘
```

### PADRAO E: Full typographic — fundo solido, so texto
**Visto em**: post "guarda este post", slides educativos, carrosseis
- Fundo solido (azul forte, navy, verde)
- Icone grande relacionado ao tema (bookmark, alerta, check)
- Texto ENORME ocupando a maior parte do espaco
- Mistura de pesos: regular + bold + italic na mesma frase
- Muito respiro / espaco vazio
- Formas organicas (blob, curva) no canto como decoracao sutil

```
┌──────────────────┐
│ @handle   pagina │
│                  │
│                  │
│   [icone]        │
│   Texto em       │
│   BOLD e         │
│   tamanhos       │
│   diferentes.    │
│                  │
│            LOGO  │
└──────────────────┘
```

### PADRAO F: Grid de dados / numeros de impacto
**Visto em**: Eleks case study, IBIXPO "upcoming events"
- Numeros GIGANTES (5x, 230%, R$10.000)
- Texto pequeno explicativo abaixo do numero
- Lado a lado ou empilhado
- Foto recortada como contexto visual
- Funciona pra mostrar resultados, dados, estatisticas

```
┌──────────────────┐
│  TITULO          │
│                  │
│  ┌─FOTO──┐      │
│  │recort.│      │
│  └───────┘      │
│                  │
│  5x     230%    │
│  desc   desc    │
└──────────────────┘
```

---

## 5. Tecnicas de CSS para Efeitos Visuais de Social Media

### Foto recortada com forma organica
```css
.photo-cut {
  clip-path: polygon(0 0, 100% 0, 100% 70%, 0 85%);
  /* ou diagonal: */
  clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
  /* ou com curva: */
  border-radius: 0 0 50% 50% / 0 0 15% 15%;
}
```

### Blob/forma organica
```css
.blob {
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  /* gerar variacoes: mudar os % */
}
```

### Foto com recorte arredondado
```css
.photo-rounded {
  border-radius: 0 0 40px 40px;
  /* ou circular: */
  border-radius: 50%;
  /* ou um lado so: */
  border-radius: 0 40px 40px 0;
}
```

### Texto com mistura de pesos (hierarquia na mesma frase)
```css
.title { font-weight: 400; }          /* parte normal */
.title strong { font-weight: 900; }   /* parte de impacto */
.title em { font-style: italic; color: #accent; }  /* destaque */
```

### Sobreposicao de elementos (layering)
```css
.element-behind { z-index: 1; opacity: 0.1; transform: scale(1.2); }
.element-front { z-index: 5; }
/* Elementos sobrepostos criam profundidade */
```

---

## 6. Identidade Visual da Maino (extraida dos posts reais)

### Padroes observados no @mainotecnologia
- **Fundo principal**: navy escuro (#0D1817, #121426) ou azul (#033860)
- **Cor de destaque**: verde (#6ED161, #2A7221) — SEMPRE presente
- **Barra verde no topo**: 5px, gradient horizontal — marca registrada
- **Faixa verde lateral**: 7px esquerda, gradient vertical
- **Logo**: estrela verde + "maino" em branco, topo centralizado ou topo-esquerdo
- **Tipografia**: bold/black uppercase para titulos, italic pra destaque
- **Fotos reais**: portos, containers, guindastes, navios — contexto comex
- **Faixa diagonal verde**: separando foto de conteudo (post split)
- **Post com pessoa**: CEO/especialista com citacao, passa autoridade
- **Slide counter**: "X/Y" no canto do carrossel
- **Cores de destaque secundario**: laranja (#F97316) pra numeros/dados, azul claro pra subtitulos

### O que a Maino NAO faz
- Nao usa formas abstratas sem significado
- Nao usa elementos de UI (cards, buttons, pills)
- Nao usa fundos totalmente lisos sem nenhum elemento visual
- Nao usa mais de 3 cores por post
- Nao coloca texto demais — sempre respiro

---

## 7. Anti-patterns Aprendidos

### Sessao 2026-03-22

| O que fiz | Por que nao funcionou | O que deveria ter feito |
|---|---|---|
| Cards com borda e icones | Parece landing page / UI de site | Texto solto + foto de fundo |
| Pills/tags que parecem botoes | Parece elemento interativo, nao design grafico | Texto simples, sem caixa |
| Timeline/stepper horizontal | Componente de UI, nao design | Se precisar, usar algo mais visual |
| Icone de cubo 3D generico no post de comex | Nenhuma relacao com o tema | Navio, container, globo — algo de comex |
| Layout muito retilineo/angular | Parece dashboard ou site | Usar formas redondas, circulos, elementos organicos |
| Formas decorativas sem significado | Enche o design sem comunicar nada | Cada elemento deve reforcar a mensagem |
| Fundo liso sem elementos visuais relevantes | Fica vazio e generico | Adicionar elementos que se relacionem com o texto |
| Circulos decorativos + icone generico | Design "bonito" mas vazio de significado | Cada forma/elemento precisa reforcar a mensagem |
| Foto real + ilustracao cartoon juntas | Linguagens visuais diferentes = colagem, nao design | Escolher UMA linguagem: so foto OU so ilustracao |
| Elementos soltos sem conexao visual | Parecem colados aleatoriamente, sem composicao | Usar proximidade, overlap e fluxo pra conectar |
| Planilha desenhada + foto de porto | Estilos visuais incompativeis lado a lado | Se for usar foto, fazer overlay/tratamento. Se for ilustrar, ilustrar tudo |

---

## 8. Padroes que Funcionaram

### Post DUIMP v4 (foto de fundo) — aprovado
- Foto real de porto (Unsplash) com gradient overlay
- Texto bold grande na parte inferior
- Hierarquia: kicker verde > titulo enorme > descricao suave > CTA texto
- Elementos minimos: green strip, logo pequeno, foto + texto
- **Por que funcionou**: a foto JA comunica "comex/porto", o texto complementa
- **Padrao**: A (foto recortada) + overlay

### Post Maino v3 (circulo azul + ilustracoes) — parcialmente aprovado
- Grande circulo azul como fundo (padrao C)
- Ilustracoes de documentos flutuando (relacionados ao tema)
- Texto bold italic uppercase
- **Por que funcionou parcialmente**: layout OK, mas os docs poderiam ter mais relacao com o tema especifico

---

## 9. Regras de Ouro (resumo rapido)

1. **Conceito antes de layout** — primeiro a metafora visual, depois o design
2. **Texto ↔ Imagem** — todo visual reforça o texto, teste tampando o texto
3. **Formas organicas** — circulos, blobs, recortes arredondados, nunca so retangulos
4. **Foto real > ilustracao > forma abstrata** — preferencia nesta ordem
5. **Menos e mais** — 3-4 elementos max, muito respiro
6. **Mistura de pesos tipograficos** — regular + bold + italic na mesma composicao
7. **Cor de destaque em palavras-chave** — nao em caixas/fundos
8. **Nada que pareca interativo** — sem botoes, pills, cards com borda
9. **Cada elemento justifica sua existencia** — se nao comunica, remove

---

## 10. Como Crescer Este Arquivo

Apos cada conversa sobre design, adicionar:
- Novos conceitos visuais por tema (secao 2)
- Novos padroes de layout aprendidos de referencias (secao 4)
- Novas tecnicas CSS (secao 5)
- Novos anti-patterns aprendidos (secao 7)
- Novos padroes que funcionaram (secao 8)

**Regra**: so adicionar o que foi VALIDADO pelo usuario (feedback positivo ou negativo). Nao adicionar suposicoes.
