# Vídeo convite — Guia 26

Vídeo de 33 s, sem áudio, chamando artistas e toda a cadeia da música (bandas, selos,
assessorias, produtoras, jornalistas) para colocar seus lançamentos no guia. Tom lúdico:
adesivos que pulam com mola, vinil girando, pins caindo no mapa e confete.
É uma composição HTML com linha do tempo determinística, renderizada quadro a quadro.

- **`guia26-16x9.mp4`** — horizontal 1920×1080 (YouTube, site, apresentações).
- **`guia26-9x16.mp4`** — vertical 1080×1920 (Reels, TikTok, Stories, Shorts). Textos e elementos
  importantes ficam longe das áreas cobertas pela interface dos apps no topo e na base.
- **`video.html`** — a composição. Aberta no navegador, roda em loop; `?formato=vertical` mostra a versão 9:16.
- **`render.js`** — captura os quadros com Playwright e monta o MP4 com ffmpeg.
- **`telas/`** — capturas reais do site em modo escuro (desktop, lista, formulário e mobile).

## Roteiro

| Tempo | Cena |
|---|---|
| 0–2 s | Um vinil rola até o centro — adesivos "Psiu!" 👀 — "é, você que faz música." |
| 2–4 s | "Vai lançar" + adesivos *um disco? / um EP? / um single?*, um por batida |
| 4–7 s | "Tá em boa companhia:" — 24 artistas reais da base caem como adesivos → "+400 artistas!" |
| 7–10 s | Fundo lima: contador até **432 lançamentos no radar**, 90+ cidades, 120+ fontes, equalizador no beat |
| 10–14 s | O site entra com mola — "O mapa da música br de 2026." + "feito pela comunidade" |
| 14–20 s | Linha do tempo com março circulado ("março tá lotado!") e pins caindo nas cidades: "Seu público sabe quando sai / de onde vem." |
| 20–23 s | Lista em perspectiva com um card "SUA BANDA AQUI" encaixado — "Seu nome aqui, ó!" 👉 |
| 23–26 s | Celular soltando notas musicais — "Seu público no bolso." |
| 26–29 s | Formulário sendo preenchido + confete — "Ficou de fora? Bora! preenche, envia, tá no mapa!" |
| 29–33 s | **GUIA 26** — "Chega mais, artista! banda! selo! assessoria!…" — "Coloca seu som no mapa →" |

## Renderizar de novo

```bash
python3 -m http.server 8765 &          # na raiz do repositório
node promo/render.js promo/guia26-16x9.mp4 horizontal 30
node promo/render.js promo/guia26-9x16.mp4 vertical 30
# prévia de quadros soltos (PNG): node promo/render.js /tmp/prev vertical 30 1.5 12 31
```

Requer Node com `playwright`, Chromium e `ffmpeg`.
