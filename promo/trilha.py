"""Gera a trilha (120 BPM, pop solar em Dó maior) do vídeo convite, sincronizada com video.html.
Os tempos dos efeitos (POPS, BLIPS, PINS...) espelham os tempos das animações.
Uso: python3 promo/trilha.py saida.wav"""
import sys, numpy as np, wave

SR = 44100
DUR = 33.0
BEAT = 0.5  # 120 BPM
N = int(SR * DUR)
out = np.zeros((N, 2))
rng = np.random.default_rng(7)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    sig = sig[: N - i] * gain
    out[i:i + len(sig), 0] += sig * (1 - max(pan, 0))
    out[i:i + len(sig), 1] += sig * (1 + min(pan, 0))

def tt(dur): return np.arange(int(dur * SR)) / SR

def lowpass(x, alpha):
    # filtro passa-baixa de um polo (usado só em sinais curtos)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc); y[i] = acc
    return y

def noise(dur): return rng.standard_normal(int(dur * SR))

# ---------- Instrumentos ----------
def kick():
    t = tt(.4); f = 50 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8)

def clap():
    t = tt(.25); n = np.diff(noise(.25), prepend=0)
    e = np.exp(-t * 20) + .6 * np.exp(-((t - .012) ** 2) / 1e-5) + .5 * np.exp(-((t - .024) ** 2) / 1e-5)
    return n * e * .22

def shaker():
    t = tt(.08); s = np.diff(np.diff(noise(.08), prepend=0), prepend=0)
    return s * np.sin(np.pi * t / .08) ** 2 * .05

def marimba(freq, dur=.35):
    t = tt(dur)
    return (np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t * 40)) * np.exp(-t * 9) * np.minimum(t / .002, 1)

def pluck_bass(freq, dur=.24):
    t = tt(dur)
    s = np.sin(2 * np.pi * freq * t) + .5 * np.sign(np.sin(2 * np.pi * freq * t)) * .3
    return s * np.exp(-t * 7) * np.minimum(t / .003, 1)

def pad(freqs, dur):
    t = tt(dur)
    s = sum(np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.003 * t) for f in freqs) / len(freqs)
    return s * np.minimum(t / .08, 1) * np.minimum((dur - t) / .12, 1)

# ---------- Efeitos ----------
def pop(pitch=1.0):  # "bloop" de adesivo: seno com glissando para cima
    t = tt(.16); f = (300 + 900 * (1 - np.exp(-t * 40))) * pitch
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 26) * .55

def blip(freq):
    t = tt(.09); return np.sin(2 * np.pi * freq * t) * np.exp(-t * 45) * .3

def boing():  # mola
    t = tt(.5); f = 180 + 70 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * .45

def whoosh(dur, up=True):
    t = tt(dur); n = noise(dur)
    a = (t / dur) if up else (1 - t / dur)
    y = np.zeros_like(n); acc = 0.0
    cut = .02 + .35 * a
    # filtro variável simples por blocos
    for s in range(0, len(n), 256):
        c = cut[s]
        seg = n[s:s + 256]
        for j, v in enumerate(seg):
            acc += c * (v - acc); y[s + j] = acc
    return y * np.sin(np.pi * t / dur) * .5

def vinyl_roll(dur):  # rolar + "scratch"
    t = tt(dur); n = lowpass(noise(dur), .08) * .3
    wob = np.sin(2 * np.pi * np.cumsum(60 + 300 * (t / dur)) / SR) * .25
    return (n + wob) * np.minimum(t / .05, 1) * (1 - t / dur) ** .5

def scratch():
    t = tt(.35); f = 400 + 900 * np.abs(np.sin(2 * np.pi * 4.3 * t))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .4 + lowpass(noise(.35), .3) * .3
    return s * np.sin(np.pi * t / .35)

def popper():  # lança-confete
    t = tt(.5)
    return (lowpass(noise(.5), .5) * np.exp(-t * 18) * .8 + np.sin(2 * np.pi * np.cumsum(900 - 600 * t) / SR) * np.exp(-t * 10) * .3)

def impact():
    t = tt(1.6)
    return np.sin(2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 7)) / SR) * np.exp(-t * 2.5) * .8 + lowpass(noise(1.6), .2) * np.exp(-t * 5) * .25

# ---------- Harmonia: C G Am F (um acorde por compasso de 2 s) ----------
C4 = 261.63
def note(semi, base=C4): return base * 2 ** (semi / 12)
CHORDS = [[0, 4, 7], [-5, -1, 2], [-3, 0, 4], [-7, -3, 0]]   # C, G, Am, F
ROOTS = [0, -5, -3, -7]
# Melodia de marimba (semitons sobre Dó4, por colcheia; None = pausa) — 2 compassos, repete
MEL = [12, None, 7, 9, None, 12, 14, None,   11, None, 7, None, 14, 12, 11, 7,
       9, None, 12, 9, None, 7, 4, None,     5, None, 9, 12, None, 14, 12, None]

DRUMS = [(2.0, 9.5), (10.0, 29.0)]
def in_drums(t): return any(a <= t < b for a, b in DRUMS)

beats = np.arange(0, DUR, BEAT)
side = np.ones(N)
for b in beats:
    if not in_drums(b): continue
    bi = int(round(b / BEAT))
    add(kick(), b, .9)
    i = int(b * SR); L = int(.2 * SR); L2 = min(L, N - i)
    side[i:i + L2] = np.minimum(side[i:i + L2], .45 + .55 * np.arange(L2) / L)
    if bi % 2 == 1: add(clap(), b, 1.0)
    for k in range(4): add(shaker(), b + k * BEAT / 4, 1.0 if k % 2 else .6, .4 if k % 2 else -.4)

music = np.zeros((N, 2))
def addm(sig, t, gain, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    music[i:i + len(s), 0] += s * (1 - max(pan, 0)); music[i:i + len(s), 1] += s * (1 + min(pan, 0))

for bar_t in np.arange(2.0, 29.0, 2.0):
    k = int((bar_t - 2.0) / 2.0) % 4
    if in_drums(bar_t):
        addm(pad([note(s) for s in CHORDS[k]], 2.0), bar_t, .16)
    for j in range(8):
        t0 = bar_t + j * BEAT / 2
        if not in_drums(t0): continue
        # baixo saltitante: tônica / oitava alternadas
        addm(pluck_bass(note(ROOTS[k] + (12 if j % 2 else 0), C4 / 4)), t0, .5)
        m = MEL[(int((bar_t - 2.0) / 2.0) % 4) * 8 + j]
        if m is not None and t0 >= 4.0:
            addm(marimba(note(m)), t0, .32, .25 * (1 if j % 2 else -1))
music[:, 0] *= side; music[:, 1] *= side
out += music

# Intro (0–2 s): vinil rolando, "pop" ao parar, Psiu e olhinhos
add(vinyl_roll(.55), 0.0, .9)
add(impact(), .5, .5)
for f, t in [(note(12), .5), (note(16), .6), (note(19), .7), (note(24), .8)]: add(marimba(f, .6), t, .35)
add(pop(1.0), .85, 1.0); add(boing(), 1.15, .9)

# Efeitos de adesivo (mesmos tempos do video.html)
POPS = [(2.5, 1.0), (3.0, 1.15), (3.5, 1.3),           # um disco? um EP? um single?
        (6.5, .8),                                     # +400 artistas!
        (8.0, 1.0), (8.5, 1.12), (9.0, 1.25),          # tiles
        (12.5, 1.1), (15.6, 1.2), (21.0, .9),          # comunidade, março, sua banda
        (26.5, .85), (27.0, 1.0), (27.5, 1.12), (28.0, 1.25), (27.6, 1.4),  # Bora! preenche envia tá no mapa, sem login
        (30.4, 1.0)]                                   # CTA
for t, p in POPS: add(pop(p), t, .9, (p - 1.1) * 1.5)

# Parede de artistas: blips subindo a escala a cada adesivo (4,2 s + 0,1 s × i)
SCALE = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24, 26]
for i in range(24): add(blip(note(SCALE[i % 12] + (12 if i >= 12 else 0))), 4.2 + i * .1 + .08, .9, ((i % 4) - 1.5) * .3)
# Pins no mapa
for i in range(8): add(blip(note([0, 4, 7, 12, 7, 4, 12, 16][i] + 12)), 17.6 + i * .25 + .25, 1.2)
# "Chega mais, ___!" — troca a cada meia batida
for i in range(8): add(blip(note([12, 16, 19, 24, 19, 16, 19, 24][i])), 30.0 + i * .25, 1.0)
add(pop(1.3), 32.0, 1.0)

# Transições
add(whoosh(.45), 9.55, 1.0)        # íris
add(scratch(), 9.55, .5)
add(impact(), 10.0, .7)
add(whoosh(.4), 16.8, .6)          # câmera vai ao mapa
add(whoosh(.45), 28.55, .8)
add(popper(), 27.6, .9); add(popper(), 29.0, 1.0); add(impact(), 29.0, .6)
# Acorde final em Dó com marimba
for j, s in enumerate([0, 4, 7, 12, 16, 19, 24]): add(marimba(note(s), 1.2), 29.0 + j * .06, .3)
fin = pad([note(s) for s in [0, 4, 7, 12]], 4.0) * np.exp(-tt(4.0) / 2.0)
add(fin, 29.0, .35)

fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
out = np.tanh(out * 1.1); out /= np.abs(out).max() * 1.05

with wave.open(sys.argv[1] if len(sys.argv) > 1 else "trilha.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
