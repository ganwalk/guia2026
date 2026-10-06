"""Gera a trilha (120 BPM) do vídeo promocional, sincronizada com os cortes de cena.
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
    if i >= N: return
    sig = sig[: N - i] * gain
    out[i:i + len(sig), 0] += sig * (1 - max(pan, 0))
    out[i:i + len(sig), 1] += sig * (1 + min(pan, 0))

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 1.0

def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    e = np.exp(-t * 18) + 0.6 * np.exp(-((t - 0.012) ** 2) / 1e-5) + 0.5 * np.exp(-((t - 0.024) ** 2) / 1e-5)
    # passa-alta simples
    hp = np.diff(noise, prepend=0)
    return hp * e * 0.25

def hat(open_=False):
    n = int((0.25 if open_ else 0.05) * SR); t = np.arange(n) / SR
    s = np.diff(np.diff(rng.standard_normal(n), prepend=0), prepend=0)
    return s * np.exp(-t * (12 if open_ else 70)) * 0.06

def saw(freq, dur, detune=0.006):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(2 * ((t * freq * (1 + d)) % 1) - 1 for d in (-detune, 0, detune)) / 3
    return s

def lowpass(x, alpha):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc); y[i] = acc
    return y

def impact():
    n = int(2.5 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(30 + 80 * np.exp(-t * 6)) / SR) * np.exp(-t * 1.8)
    noise = rng.standard_normal(n) * np.exp(-t * 4) * 0.25
    return boom * 0.9 + lowpass(noise, 0.15)

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out_ = np.zeros(n); acc = 0.0
    for i in range(n):  # filtro abrindo
        a = 0.01 + 0.5 * (t[i] / dur) ** 2
        acc += a * (noise[i] - acc); out_[i] = acc
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1200 * (t / dur) ** 2) / SR) * 0.15
    return (out_ * 0.5 + sweep) * (t / dur) ** 1.5

# Progressão (Lá menor): Am F C G — um acorde por compasso (2 s)
ROOTS = [55.0, 43.65, 65.41, 49.0]
CHORDS = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]

# Seções: (início, fim)
DRUMS = [(2.0, 9.5), (10.0, 29.0)]
def in_drums(t): return any(a <= t < b for a, b in DRUMS)

# Abertura: drone + impacto no "2026"
drone = lowpass(saw(55, 2.2), 0.02) * np.minimum(np.arange(int(2.2 * SR)) / SR / 1.5, 1)
add(drone, 0.0, 0.5)
add(impact(), 0.5, 0.9)

beats = np.arange(0, DUR, BEAT)
side = np.ones(N)  # sidechain
for b in beats:
    if in_drums(b):
        add(kick(), b, 0.95)
        i = int(b * SR); L = int(0.25 * SR)
        side[i:i + L] = np.minimum(side[i:i + L], 0.35 + 0.65 * (np.arange(min(L, N - i)) / L))
        if int(round(b / BEAT)) % 2 == 1:
            add(clap(), b, 1.0)
        add(hat(), b + BEAT / 2, 1.0, 0.3)
        add(hat(open_=int(round(b / BEAT)) % 4 == 3), b + BEAT / 2, 0.6, -0.3)
        if 4.0 <= b < 7.0:  # rajada de nomes: semicolcheias
            add(hat(), b + BEAT / 4, 0.7, 0.4); add(hat(), b + 3 * BEAT / 4, 0.7, -0.4)

# Baixo + pad
bass = np.zeros(N); pad = np.zeros(N)
for bar_t in np.arange(2.0, 29.0, 2.0):
    k = int((bar_t - 2.0) / 2.0) % 4
    for j in range(8):  # colcheias
        t0 = bar_t + j * BEAT / 2
        if not in_drums(t0): continue
        s = saw(ROOTS[k] * (2 if j % 2 else 1), BEAT / 2 * 0.9, 0.002) * env(int(BEAT / 2 * 0.9 * SR), 0.003, 0.12)
        i = int(t0 * SR); bass[i:i + len(s)] += s[: N - i]
    chord = sum(saw(f, 2.0) for f in CHORDS[k]) / 3
    e = np.minimum(np.arange(len(chord)) / SR / 0.05, 1) * np.minimum((2.0 - np.arange(len(chord)) / SR) / 0.1, 1)
    i = int(bar_t * SR); pad[i:i + len(chord)] += (chord * e)[: N - i]
bass = lowpass(bass, 0.08)
pad = lowpass(pad, 0.06)
out[:, 0] += (bass * 0.55 + pad * 0.22) * side
out[:, 1] += (bass * 0.55 + pad * 0.26) * side

# Build-up antes da revelação do site (10 s) e do logo final (29 s)
add(riser(2.0), 8.0, 0.9)
add(impact(), 10.0, 0.8)
add(riser(2.0), 27.0, 0.8)
add(impact(), 29.0, 1.0)
# Acorde final sustentado
fin = sum(saw(f, 4.0) for f in [220, 261.6, 329.6, 440]) / 4
fin = lowpass(fin, 0.05) * np.exp(-np.arange(len(fin)) / SR / 1.6)
add(fin, 29.0, 0.6)

# Fade out e normalização com soft clip
fade = int(1.0 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
out = np.tanh(out * 1.2); out /= np.abs(out).max() * 1.05

with wave.open(sys.argv[1] if len(sys.argv) > 1 else "trilha.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
