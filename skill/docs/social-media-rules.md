# Design para Redes Sociais (CRITICO — LEIA PRIMEIRO)

**Isto NAO e web design. Isto e design grafico para redes sociais.**

Posts de redes sociais devem parecer feitos no Canva ou por um designer grafico — NAO como um site, landing page ou UI de app. O maior erro e fazer posts que parecem screenshots de uma pagina web.

---

## O que FUNCIONA (faca isto)

- **Fotografia full-bleed** como fundo com overlay de gradiente para legibilidade do texto
- **Texto E o design** — tipografia bold enorme preenchendo o espaco, nao texto pequeno em caixas
- **Elementos minimos** — foto + texto + logo. So isso. Maximo impacto.
- **Fotos reais** do Unsplash (baixar, converter para base64, embutir inline). Sempre prefira fotografia real a formas abstratas
- **Overlays de gradiente** nas fotos: mais escuro embaixo onde o texto vai, transparente em cima onde a foto respira
- **Titulos bold uppercase** — 64-82px, peso 800-900, preenchendo a largura
- **Cores de destaque como realce de texto**, nao como fundo de caixas
- **Elementos de marca sutis**: barras finas de destaque, faixas laterais, logo pequeno — nunca dominando
- **Textura de granulado/ruido** como overlay para calor e sensacao analogica

---

## O que NAO funciona (nunca faca isto)

- **Cards com bordas** — isto e um componente de site, nao design de redes sociais
- **Pills/tags que parecem botoes** — labels de texto sim, elementos clicaveis NAO
- **Layouts de grid** — posts nao sao dashboards
- **Multiplas caixas/containers pequenos** — isto grita "landing page"
- **Botoes de CTA** — nao existem botoes no Instagram. Use texto simples com seta (->) no maximo
- **Cards de info com icones** — isto e uma secao de features de um site SaaS
- **Componentes de timeline/stepper** — padrao de UI, nao padrao de design
- **Qualquer coisa que pareca interativa** — imagens de redes sociais sao estaticas, nao finja UI

---

## Tecnica de Foto de Fundo

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

---

## Bons Layouts para Redes Sociais

### Feed / Quadrado (1080x1080)

1. **Foto + texto bold** — foto full-bleed, overlay gradiente, titulo enorme embaixo
2. **Split horizontal** — foto real metade de cima, cor solida/gradiente embaixo com texto grande
3. **Circulo de fundo** — circulo colorido grande centralizado, ilustracoes flutuando, texto bold abaixo
4. **Full tipografico** — fundo escuro solido, apenas texto, letras bold italic uppercase massivas preenchendo o espaco
5. **Split diagonal** — foto com bloco de cor cortando em diagonal

### Story (1080x1920)

1. **Foto hero** — foto full-bleed com overlay de texto no terco inferior
2. **Impacto empilhado** — texto grande em cima, foto no meio, texto CTA embaixo
3. **Fluxo gradiente** — fundo gradiente suave, texto centralizado, elementos minimos

---

## Regras de Composicao

- **Zona segura**: mantenha conteudo importante 60px das bordas (plataformas cortam)
- **Padding**: minimo 40px de todas as bordas
- **Respiro**: pelo menos 30% da area deve ser espaco vazio
- **Logo**: pequeno e sutil, 36-48px, canto superior esquerdo ou centro. Nunca dominante.
- **Menos e mais**: se voce esta adicionando um 4o elemento, remova um
