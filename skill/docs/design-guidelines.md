# Diretrizes de Design

Referencia completa de hierarquia visual, tipografia, cores, estilos e acessibilidade para geracao de imagens.

---

## 1. Hierarquia Visual (CRITICO)

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

---

## 2. Combinacoes Tipograficas

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

Para mais opcoes, use: `python3 <skill-path>/scripts/search.py "<humor/estilo>" --domain typography -n 5`

---

## 3. Paletas de Cores por Industria

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

Para paletas especificas, use: `python3 <skill-path>/scripts/search.py "<industria>" --domain color -n 5`

---

## 4. Estilos Visuais

### Glassmorphism
```css
backdrop-filter: blur(15px);
background: rgba(255, 255, 255, 0.15);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 20px;
```
Melhor para: moderno, premium, tech. Requer um fundo vibrante atras do vidro.

### Minimalismo
Preto + branco + 1 cor de destaque apenas. Tipografia grande, whitespace extremo.
Melhor para: luxo, editorial, corporativo.

### Blocos Vibrantes
Formas geometricas ousadas, cores neon, tipografia 32px+, alto contraste.
Melhor para: redes sociais, startups, marcas jovens.

### Aurora / Gradiente
Gradientes mesh com 2-3 cores complementares, transicoes suaves.
Melhor para: SaaS, agencias criativas, musica.

### Dark Mode
Fundo #000000 ou #121212, texto branco, destaques neon.
Melhor para: tech, entretenimento, gaming.

### Neubrutalism
Bordas grossas (3-4px), sombras solidas deslocadas, cores primarias, sem border-radius.
```css
border: 3px solid #000;
box-shadow: 6px 6px 0 #000;
border-radius: 0;
```
Melhor para: Gen Z, marcas disruptivas, marketing ousado.

Para mais estilos, use: `python3 <skill-path>/scripts/search.py "<estilo>" --domain style -n 5`

---

## 5. Elementos Visuais

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

---

## 6. Acessibilidade (CRITICO)

Mesmo em imagens estaticas, acessibilidade importa para alcance e legibilidade.

- **Contraste minimo**: 4.5:1 para texto normal, 3:1 para texto grande (48px+)
- **Tamanho minimo de texto**: 20px para feed, 24px para stories
- **Teste gradientes**: verifique contraste nos pontos mais claros E mais escuros
- **Solucao para gradientes**: adicione overlay semi-transparente atras do texto
- **Nao dependa apenas de cor**: use icone + texto para transmitir significado
- **Evite**: vermelho + verde juntos (daltonismo), azul claro sobre branco, amarelo sobre branco
