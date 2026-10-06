# Vídeo promocional — "brag" do Guia 26

Vídeo de 33 s (1920×1080, 30 fps) vendendo o site, montado como uma composição HTML com
linha do tempo determinística e renderizado quadro a quadro.

- **`guia26-promo.mp4`** — vídeo final, com trilha.
- **`video.html`** — a composição. Aberta no navegador, roda em loop (clique para tocar com som, espaço pausa).
- **`trilha.py`** — sintetiza a trilha de 120 BPM; cada corte de cena cai numa batida.
- **`render.js`** — captura os quadros com Playwright e monta o MP4 com ffmpeg.
- **`telas/`** — capturas reais do site em modo escuro (desktop, lista, formulário e mobile).

## Roteiro

| Tempo | Cena |
|---|---|
| 0–2 s | **2026** entra com impacto |
| 2–4 s | DISCOS. EPS. SINGLES. TUDO. — uma palavra por batida |
| 4–7 s | Rajada de 24 artistas reais da base, 1/4 de batida cada |
| 7–10 s | Contador até **432 lançamentos**, 90+ cidades, 120+ fontes |
| 10–14 s | Revelação do site em perspectiva — "Tudo num só lugar." |
| 14–20 s | Câmera na linha do tempo ("Saiba quando sai.") e no mapa ("Saiba de onde vem.") |
| 20–23 s | Lista em perspectiva — "Filtre. Busque. Descubra." |
| 23–26 s | Celular rolando o site — "No seu bolso." |
| 26–29 s | Formulário sendo preenchido — "Ficou de fora?" |
| 29–33 s | Assinatura **GUIA 26** + guiadelancamentos.com.br |

## Renderizar de novo

```bash
python3 -m http.server 8765 &          # na raiz do repositório
node promo/render.js promo/guia26-promo.mp4 30
# prévia de quadros soltos (PNG): node promo/render.js /tmp/prev 30 1.5 12 31
```

Requer Node com `playwright`, Chromium, Python 3 com `numpy` e `ffmpeg`.
