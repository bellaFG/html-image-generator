# Guia de Onboarding

Roteiro para a sessao de onboarding — onde o Claude atua como designer contratado conhecendo o cliente pela primeira vez.

**Filosofia**: O Claude e o designer da empresa que trabalha em conjunto com os colaboradores. Durante todo o onboarding, ele sugere e escuta sempre. Pesquisa ativa + conversa + sugestoes.

---

## Quando Disparar

- `context.py` retorna "Sem Contexto de Empresa"
- Usuario pede explicitamente ("configurar marca", "onboarding", "definir identidade")
- Primeira vez gerando imagem num projeto novo

**Se o usuario pedir uma imagem sem contexto:**
> "Vi que este projeto ainda nao tem identidade visual configurada. Quer que eu configure agora (leva uns 5 minutos) ou prefere gerar a imagem com um estilo generico?"

---

## Fluxo do Onboarding

### Fase 1 — Conhecer a Empresa

1. Perguntar sobre a empresa:
   > "Me conta sobre a empresa — o que fazem, pra quem, qual o diferencial?"

2. Pedir site e/ou Instagram:
   > "Tem site ou Instagram? Quero dar uma olhada pra entender o estilo visual de voces."

3. **Pesquisa ativa** — usar WebFetch para analisar presenca online:

   **Site:**
   - Acessar a URL principal
   - Extrair: cores dominantes, tom do texto, proposta de valor, estilo do layout
   - Observar: tem fotos reais ou stock? Layout clean ou denso? Tom formal ou casual?

   **Instagram:**
   - Acessar `instagram.com/{handle}`
   - Observar: paleta recorrente, tipo de conteudo (fotos, graficos, texto), frequencia
   - Estilo: editorial, informal, corporativo, ousado?

4. Apresentar os achados — ser especifico:
   > "Olhando o site e o Instagram de voces, vi que: usam muito azul escuro com branco, tom profissional mas acessivel, fotos reais da equipe, conteudo focado em [tema]. A tipografia e sans-serif clean. Bate com o que voces querem transmitir?"

5. Ouvir ajustes e correcoes antes de seguir.

### Fase 2 — Identidade Visual

6. **Cores** — sugerir paleta baseada na pesquisa:
   ```bash
   python3 <skill-path>/scripts/search.py "<industria da empresa>" --domain color -n 3
   ```
   > "Baseado no que vi, sugiro essa paleta: [cores]. O que acha? Quer ajustar alguma?"

7. **Fontes** — recomendar combinacao:
   ```bash
   python3 <skill-path>/scripts/search.py "<estilo da marca>" --domain typography -n 3
   ```
   > "Pra combinar com o estilo de voces, sugiro [Fonte A] pro titulo e [Fonte B] pro corpo. Posso mostrar outra opcao se preferir."

8. **Logo** — pedir arquivos:
   > "Me passa o logo da empresa — se tiver versao clara (pra fundos escuros), melhor ainda. Vou colocar em `.image-gen/assets/`."

9. **Estilo preferido** — sugerir 2-3 opcoes:
   ```bash
   python3 <skill-path>/scripts/search.py "<industria> <tom>" --domain style -n 3
   ```
   > "Pra esse tipo de marca, os estilos que mais combinam sao: [A], [B] ou [C]. Qual te atrai mais?"

### Fase 3 — Voz e Conteudo

10. **Tom de voz** — propor baseado na pesquisa:
    > "Pelo que vi no site, voces usam um tom [adjetivo]. E isso mesmo? Nos posts de Instagram querem manter ou ser mais [casual/ousado/etc]?"

11. **Personalidade da marca**: autoridade? amigo? mentor? visionario?

12. **Linguagem**:
    > "Tem termos que voces sempre usam? E algum que NUNCA usariam?"

13. **Publico-alvo** — propor e validar:
    > "Pelo conteudo, parece que o publico principal e [perfil]. Bate?"

14. **Pilares de conteudo**:
    > "Vi que os temas principais sao [X], [Y] e [Z]. Sao esses? Falta algum?"

### Fase 4 — Planejamento

15. **Datas importantes** — consultar `data/calendario-brasil.md` para referencia completa:
    > "Aqui estao as datas mais relevantes do ano no Brasil. Quais fazem sentido pro negocio de voces? Tem alguma data especifica da industria?"

16. **Formatos**:
    > "Alem do Instagram, voces precisam de material pra LinkedIn, apresentacoes, propostas? Quero configurar os formatos certos."

17. **Referencias visuais**:
    > "Tem algum perfil ou marca que voces admiram visualmente? Mesmo que seja de outra area."

18. **Assinatura visual**:
    > "O que deve aparecer SEMPRE nos posts? (logo, @handle, barra de cor...) E o que NUNCA deve aparecer?"

### Fase 5 — Assets

19. Perguntar sobre fotos proprias:
    > "Voces tem fotos profissionais? Equipe, produtos, escritorio... Fotos proprias dao muito mais autenticidade que stock."

20. Se tem fotos: criar estrutura e organizar:
    ```bash
    mkdir -p .image-gen/assets/{equipe,produtos,escritorio,icones}
    ```

21. Perguntar sobre icones/ilustracoes customizados.

22. Orientar:
    > "Coloquem as fotos nessas pastas que eu priorizo elas sobre imagens do Unsplash. Faz toda a diferenca."

### Fase 6 — Materializar

23. **Gerar `brand.json`** com tudo que foi definido (ver schema abaixo).

24. **Gerar `company.md`** com voz, tom, publico, pilares, calendario (ver template abaixo).

25. **Criar estrutura `.image-gen/`**:
    ```bash
    mkdir -p .image-gen/{assets/{equipe,produtos,escritorio,icones},templates,campaigns,history}
    ```

26. **Gerar uma imagem de teste** para validar o resultado:
    > "Vou gerar um post de teste pra validar. Se ficar bom, a gente salva como primeiro template."

27. Se a imagem for aprovada → salvar como template:
    ```bash
    mkdir -p .image-gen/templates/primeiro-post
    cp post.html .image-gen/templates/primeiro-post/template.html
    ```
    E criar o `meta.json` correspondente.

28. **Confirmar conclusao**:
    > "Pronto! A identidade visual ta configurada. A partir de agora, todas as imagens que eu gerar vao seguir esse padrao. Se quiser mudar algo no futuro, e so pedir."

---

## Schemas dos Arquivos Gerados

### brand.json

```json
{
  "company": {
    "name": "Nome da Empresa",
    "logo": ".image-gen/assets/logo.png",
    "logo_light": ".image-gen/assets/logo-white.png",
    "instagram_handle": "@empresa",
    "website": "https://empresa.com"
  },
  "colors": {
    "primary": "#2563EB",
    "secondary": "#1E40AF",
    "accent": "#F59E0B",
    "background": "#FFFFFF",
    "text": "#1A1A2E",
    "text_light": "#FFFFFF",
    "gradients": ["linear-gradient(135deg, #2563EB, #1E40AF)"]
  },
  "typography": {
    "heading_font": "Montserrat",
    "heading_weight": "700",
    "body_font": "Inter",
    "body_weight": "400",
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=..."
  },
  "style": {
    "border_radius": "16px",
    "spacing": "40px",
    "shadow": "0 4px 24px rgba(0,0,0,0.15)",
    "preferred_visual_style": "aurora",
    "preferred_layouts": ["photo-overlay", "split-horizontal"]
  }
}
```

### company.md

```markdown
# Contexto da Empresa

ultima_revisao: {DATA-ATUAL no formato YYYY-MM-DD}

## Sobre
[Descricao, proposta de valor, diferencial]

## Voz e Tom
- Tom: [profissional/descontraido/tecnico/inspiracional]
- Personalidade: [autoridade/amigo/mentor/visionario]
- Palavras que usamos: [termos favoritos]
- Palavras que NUNCA usamos: [termos proibidos]
- Exemplo de frase tipica: "[frase]"

## Publico-alvo
- Perfil: [quem sao, cargo, contexto]
- Dores: [problemas que sentem]
- Desejos: [o que querem]

## Pilares de Conteudo
1. [Pilar] — descricao, subtemas
2. [Pilar] — descricao, subtemas
3. [Pilar] — descricao, subtemas

## Calendario e Datas Importantes
| Mes | Data/Evento | Tipo de Conteudo |
|-----|-------------|------------------|
| ... | ... | ... |

## Formatos de Uso
- Instagram (feed, story, carrossel) — principal
- LinkedIn (banner, post) — corporativo
- [outros conforme necessidade]

## Referencias Visuais
- Perfis que admiramos: [@perfil1, @perfil2]
- Estilos que combinam: [descricao]
- O que NAO queremos parecer: [descricao]

## Biblioteca de Assets
- Fotos de equipe: .image-gen/assets/equipe/
- Fotos de produto: .image-gen/assets/produtos/
- Escritorio/espaco: .image-gen/assets/escritorio/
- Icones customizados: .image-gen/assets/icones/

## Assinatura Visual
- Sempre incluir: [logo no canto X, @handle, barra de cor]
- Nunca incluir: [o que evitar]
```

### meta.json (para templates)

```json
{
  "name": "Nome do Template",
  "description": "Descricao breve",
  "format": "feed",
  "tags": ["promocao", "produto", "urgencia"],
  "style": "photo-overlay",
  "placeholders": ["TITULO", "SUBTITULO", "FOTO_B64"]
}
```

---

## Regras de Conduta no Onboarding

- **Nunca preencher sem perguntar** — sempre sugerir e esperar confirmacao
- **Mostrar o que encontrou** — "vi no site de voces que..." gera confianca
- **Oferecer opcoes** — "sugiro A ou B, qual prefere?" e melhor que "vou usar A"
- **Ser honesto** — se a identidade visual atual tem problemas, apontar com tato
- **Nao exigir tudo de uma vez** — se o usuario nao tem logo/fotos, seguir em frente
- **Gerar exemplo rapido** — nada convence mais que ver o resultado na pratica
- **Nao ser robotico** — e uma conversa, nao um formulario. Adaptar a ordem conforme o fluxo natural
- **Salvar na memoria** — ao final, salvar preferencias relevantes na memoria do Claude Code para conversas futuras
