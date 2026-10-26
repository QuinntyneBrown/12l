"""Build the 30-second 12L pitch video.

Inputs  LINES below                       one narrated line per slide (caption text, spoken text)
        music/energetic-hip-hop-excerpt.mp3  "Energetic Hip-Hop" (SoundSurfer, Pixabay), ducked under the voice
        kokoro/                           Kokoro-82M ONNX + af_bella voice from Hugging Face (auto-downloaded)
Outputs 12l-pitch.mp4 (H.264/AAC), 12l-pitch.webm (VP9/Opus), 12l-pitch.vtt, 12l-pitch.txt,
        12l-pitch-poster.png and ATTRIBUTION.md, written to the app's public media folder
        (src/frontend/projects/twelvel/public/media/) and copied to docs/mocks/assets/media/.

Needs: kokoro-onnx, onnxruntime, huggingface_hub, numpy, ffmpeg/ffprobe, python playwright (chromium).
Run:   python -I docs/mocks/_build/video/build_video.py   (from any directory)
"""
import pathlib, shutil, subprocess, tempfile, wave

import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from kokoro_onnx.tokenizer import Tokenizer
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT_DIRS = [REPO / "src/frontend/projects/twelvel/public/media", REPO / "docs/mocks/assets/media"]
NAME = "12l-pitch"
HF_REPO, VOICE, SPEED = "onnx-community/Kokoro-82M-v1.0-ONNX", "af_bella", 1.12
MUSIC, MUSIC_DB = HERE / "music/energetic-hip-hop-excerpt.mp3", -9
TARGET, LEAD, TAIL, MIN_GAP = 30.0, 0.6, 1.8, 0.25  # total length; seconds before the first line and after the last

# (caption and transcript text, text the narrator speaks)
LINES = [
    ("Size 12 feet? Built large? Tired of hunting for your size? Welcome to 12L.",
     "Size twelve feet? Built large? Tired of hunting for your size? Welcome to twelve L!"),
    ("Big sizes, finally in one place: men’s 12 shoes and men’s large clothes.",
     "Big sizes, finally in one place. Men's twelve shoes, and men's large clothes."),
    ("Shopping? Every pair, every jacket, every tee. Everything already fits you.",
     "Shopping? Every pair, every jacket, every tee. Everything already fits you!"),
    ("Selling? List in minutes and sell to people your size.", "Selling? List in minutes, and sell to people your size."),
    ("Snap a photo. Set a price. Ship it. Get paid.", "Snap a photo. Set a price. Ship it. Get paid!"),
    ("12L. Built for size 12 and L. Come on in.", "Twelve L. Built for size twelve and L. Come on in!"),
]

LOGO = ('<svg class="logo" viewBox="-4 -4 192 108" aria-hidden="true">'
        '<polygon class="ink" points="0,14 20,0 40,0 40,100 20,100 20,24 0,38"/>'
        '<polygon class="ink" points="52,0 112,0 112,50 78,80 112,80 112,100 52,100 52,76 92,41 92,20 52,20"/>'
        '<polygon class="l" points="124,0 144,0 144,80 170,80 184,66 184,88 172,100 124,100"/></svg>')
# The page's decorative shapes: chamfered blocks and a striped band in ink, paper and signal red.
SHAPES = ('<div class="shape s1"></div><div class="shape s2"></div><div class="shape s3"></div><div class="stripes"></div>')
SLIDES = [
    f'<p class="k">Men’s US 12 · Men’s L</p><h1>Size 12 feet?<br>Built large?</h1><p class="sub">Welcome to <b>12L</b>.</p>',
    f'{LOGO}<h1 style="margin-top:56px">Big sizes, <em>finally<br>in one place.</em></h1>',
    '<p class="k">For shoppers</p><h1>Everything<br><em>already fits you.</em></h1>'
    '<div class="tags"><span>Shoes <b>US 12</b></span><span>Tops <b>L</b></span><span>Outerwear <b>L</b></span><span>Bottoms <b>L</b></span></div>',
    '<p class="k">For sellers</p><h1>List in minutes.<br><em>Sell to people your size.</em></h1>',
    '<ol class="steps"><li><b>1</b>Snap it</li><li><b>2</b>Price it</li><li><b>3</b>Ship it</li><li><b>4</b>Get paid</li></ol>',
    f'{LOGO}<h1 style="margin-top:56px">Built for size 12 and L.</h1><p class="cta">Come on in → <em>12L</em></p>',
]
# 12L tokens (docs/design-system/tokens): ink #0b0b0b to #242424 gradient, paper #f4f1ea, signal red #e1251b,
# Archivo display type, sharp corners with the logo's 45° chamfer.
CSS = """@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;800&family=Inter:wght@500;700&display=swap');
html,body{margin:0;width:1920px;height:1080px;overflow:hidden}
body{background:linear-gradient(135deg,#0b0b0b 0%,#141414 45%,#242424 100%);color:#f4f1ea;font-family:Inter,sans-serif;
  display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:0 180px;box-sizing:border-box;position:relative}
h1{font:800 124px/1.04 Archivo,sans-serif;letter-spacing:-.035em;margin:0;position:relative;z-index:1}
em{font-style:normal;color:#ff6b5e}
.k{font:700 40px Inter,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#e6e1d6;margin:0 0 40px;position:relative;z-index:1}
.sub,.cta{font:600 64px Archivo,sans-serif;margin:48px 0 0;position:relative;z-index:1}.cta em{color:#ff6b5e}
.logo{width:300px;position:relative;z-index:1}.logo .ink{fill:#f4f1ea}.logo .l{fill:#e1251b}
.tags{display:flex;gap:28px;margin-top:64px;position:relative;z-index:1}
.tags span{font:600 40px Inter,sans-serif;padding:18px 30px;border:3px solid #f4f1ea;clip-path:polygon(0 0,calc(100% - 22px) 0,100% 22px,100% 100%,0 100%)}
.tags b{color:#ff6b5e;margin-left:10px}
.steps{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:40px;margin:0;padding:0;width:100%;position:relative;z-index:1}
.steps li{font:800 72px Archivo,sans-serif;letter-spacing:-.03em;border-top:8px solid #e1251b;padding-top:36px}
.steps b{display:block;font:700 44px Inter,sans-serif;color:#e6e1d6;margin-bottom:20px}
.shape{position:absolute;z-index:0;clip-path:polygon(0 0,calc(100% - 90px) 0,100% 90px,100% 100%,0 100%)}
.s1{right:-60px;top:-80px;width:620px;height:520px;background:#e1251b;clip-path:polygon(0 0,100% 0,100% 100%,200px 100%,0 calc(100% - 200px))}
.s2{right:300px;bottom:-120px;width:360px;height:360px;background:#3a3a3a}
.s3{right:80px;bottom:140px;width:180px;height:180px;background:#f4f1ea;opacity:.9}
.stripes{position:absolute;left:0;bottom:0;width:100%;height:28px;background:repeating-linear-gradient(135deg,#e1251b 0 28px,transparent 28px 56px);opacity:.85}"""


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).strip())


def ts(t):
    return f"{int(t // 3600):02}:{int(t % 3600 // 60):02}:{t % 60:06.3f}"


class Narrator:
    """Kokoro-82M via onnxruntime; model and voice come from Hugging Face on first run."""

    def __init__(self):
        k = HERE / "kokoro"
        k.mkdir(exist_ok=True)
        for sub, name in (("onnx", "model.onnx"), ("voices", f"{VOICE}.bin")):
            if not (k / name).exists():
                shutil.copy(hf_hub_download(HF_REPO, f"{sub}/{name}"), k / name)
        self.tok = Tokenizer()
        self.sess = ort.InferenceSession(str(k / "model.onnx"))
        self.style = np.fromfile(k / f"{VOICE}.bin", dtype=np.float32).reshape(-1, 1, 256)

    def say(self, text, out):
        ids = self.tok.tokenize(self.tok.phonemize(text, lang="en-us"))
        audio = self.sess.run(None, {"input_ids": np.array([[0, *ids, 0]], dtype=np.int64),
                                     "style": self.style[len(ids)],
                                     "speed": np.array([SPEED], dtype=np.float32)})[0].reshape(-1)
        audio = np.trim_zeros(np.where(np.abs(audio) < 0.004, 0, audio))  # trim leading/trailing silence
        with wave.open(str(out), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    if not MUSIC.exists():
        raise SystemExit(f"{MUSIC} is missing; see README.md next to this script for the track and how to cut it")
    tmp = pathlib.Path(tempfile.mkdtemp())
    narrator = Narrator()
    voices = []
    for i, (_, spoken) in enumerate(LINES):
        out = tmp / f"v{i}.wav"
        narrator.say(spoken, out)
        voices.append((out, dur(out)))

    # Timeline: the gaps between lines stretch so the video lands on TARGET seconds.
    speech = sum(d for _, d in voices)
    gap = (TARGET - LEAD - TAIL - speech) / (len(voices) - 1)
    if gap < MIN_GAP:
        raise SystemExit(f"narration is {speech:.1f}s; shorten LINES or raise SPEED to fit {TARGET:.0f}s")
    starts, t = [], LEAD
    for _, d in voices:
        starts.append(t)
        t += d + gap
    total = TARGET
    slide_d = [(starts[i + 1] if i + 1 < len(starts) else total) - (0 if i == 0 else starts[i]) for i in range(len(starts))]

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for i, html in enumerate(SLIDES):
            pg.set_content(f"<style>{CSS}</style>{SHAPES if i in (0, 2, 4, 5) else ''}{html}")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(tmp / f"s{i}.png"))
        b.close()

    # Narration placed at its start times, music ducked under it by a sidechain compressor.
    inputs, filt = [], []
    for i, (p, _) in enumerate(voices):
        inputs += ["-i", str(p)]
        ms = int(starts[i] * 1000)
        filt.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms}[a{i}]")
    n = len(voices)
    filt.append("".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{total:.3f},volume=1.7,asplit=2[vx][key]")
    inputs += ["-i", str(MUSIC)]
    filt.append(f"[{n}:a]aresample=48000,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={MUSIC_DB}dB,"
                f"afade=t=in:d=0.6,afade=t=out:st={total - 2.0:.3f}:d=2.0[bg0];"
                "[bg0][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[bg];"
                "[vx][bg]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]")
    n += 1

    # Video: slides with short crossfades.
    for i in range(len(SLIDES)):
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{slide_d[i] + 0.4:.3f}", "-i", str(tmp / f"s{i}.png")]
    prev, off = f"[{n}:v]", 0.0
    for i in range(1, len(SLIDES)):
        off += slide_d[i - 1]
        filt.append(f"{prev}[{n + i}:v]xfade=transition=slideleft:duration=0.35:offset={off - 0.2:.3f}[x{i}]")
        prev = f"[x{i}]"
    filt.append(f"{prev}fade=t=in:d=0.3,fade=t=out:st={total - 0.5:.3f}:d=0.5,format=yuv420p[v1]")
    graph = ";".join(filt)

    out = OUT_DIRS[0]
    out.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
                           "-map", "[v1]", "-map", "[aout]", "-t", f"{total:.3f}", "-r", "30",
                           "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-tune", "stillimage",
                           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out / f"{NAME}.mp4")])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
                           "-map", "[v1]", "-map", "[aout]", "-t", f"{total:.3f}", "-r", "30",
                           "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "38", "-row-mt", "1", "-deadline", "good",
                           "-c:a", "libopus", "-b:a", "96k", str(out / f"{NAME}.webm")])
    shutil.copy(tmp / "s5.png", out / f"{NAME}-poster.png")

    vtt = ["WEBVTT", ""]
    for i, ((caption, _), (_, d)) in enumerate(zip(LINES, voices)):
        vtt += [str(i + 1), f"{ts(starts[i])} --> {ts(starts[i] + d)}", caption, ""]
    (out / f"{NAME}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (out / f"{NAME}.txt").write_text("12L in 30 seconds: transcript\n\n" + "\n".join(c for c, _ in LINES) + "\n", encoding="utf-8")
    shutil.copy(HERE / "ATTRIBUTION.md", out / "ATTRIBUTION.md")
    for other in OUT_DIRS[1:]:
        other.mkdir(parents=True, exist_ok=True)
        for f in out.iterdir():
            shutil.copy(f, other / f.name)
    print(f"built {total:.1f}s video, speech {speech:.1f}s, gap {gap:.2f}s")


if __name__ == "__main__":
    main()
