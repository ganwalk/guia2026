// Renderiza promo/video.html quadro a quadro e monta o MP4 com a trilha.
// Uso: node promo/render.js <saida.mp4> [fps] [tempos-para-prévia...]
// Requer: servidor estático na raiz do repo (python3 -m http.server 8765), playwright, ffmpeg.
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

(async () => {
  const [out = 'guia26-promo.mp4', fpsArg = '30', ...stills] = process.argv.slice(2);
  const fps = Number(fpsArg), DURATION = 33;
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('http://localhost:8765/promo/video.html?render', { waitUntil: 'load' });
  await page.evaluate(() => window.ready);
  await page.waitForTimeout(500);

  if (stills.length) {  // modo prévia: só alguns quadros em PNG
    for (const t of stills) {
      await page.evaluate(t => render(t), Number(t));
      await page.screenshot({ path: `${out}-${t}.png` });
    }
    return browser.close();
  }

  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'frames-'));
  const total = Math.round(DURATION * fps);
  for (let f = 0; f < total; f++) {
    await page.evaluate(t => render(t), f / fps);
    await page.screenshot({ path: path.join(dir, `${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 95 });
    if (f % 100 === 0) console.log(`quadro ${f}/${total}`);
  }
  await browser.close();

  const wav = path.join(dir, 'trilha.wav');
  execFileSync('python3', [path.join(__dirname, 'trilha.py'), wav], { stdio: 'inherit' });
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', path.join(dir, '%05d.jpg'), '-i', wav,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '25', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
    '-movflags', '+faststart', '-shortest', out], { stdio: 'inherit' });
  fs.rmSync(dir, { recursive: true });
  console.log('ok →', out);
})();
