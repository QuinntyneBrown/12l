# 12L pitch video build

`build_video.py` builds the 30-second pitch video that plays on the marketing page (`/welcome`).
The narration lines, the slide markup and the 12L-token slide styles are in the script.

```
python -I docs/mocks/_build/video/build_video.py
```

It writes `12l-pitch.mp4`, `12l-pitch.webm`, `12l-pitch.vtt`, `12l-pitch.txt`,
`12l-pitch-poster.png` and `ATTRIBUTION.md` to `src/frontend/projects/twelvel/public/media/`
(served at `/media/`) and copies them to `docs/mocks/assets/media/` for the mocks.

Needs ffmpeg and ffprobe, and the Python packages `kokoro-onnx`, `onnxruntime`,
`huggingface_hub`, `numpy` and `playwright` (with `python -m playwright install chromium`).

- **Voice**: Kokoro-82M from Hugging Face, voice `af_bella` at speed 1.12. The model and voice
  download into `kokoro/` (git-ignored, about 330 MB) on the first run.
- **Music**: `music/energetic-hip-hop-excerpt.mp3` is 0:08 to 0:42 of _Energetic Hip-Hop_ by
  SoundSurfer on Pixabay (Pixabay Content Licence), committed so the build is repeatable. To cut
  it again from the full track:
  `ffmpeg -ss 8 -t 34 -i soundsurfer-energetic-hip-hop-612652.mp3 -af "afade=t=out:st=32:d=2" -b:a 160k music/energetic-hip-hop-excerpt.mp3`.
  A sidechain compressor ducks it under the voice.
- **Length**: the gaps between lines stretch so the video is exactly 30 s. The script stops if
  the narration no longer fits.
- **Size wording**: the copy says "built for size 12 and L" and "big sizes, finally in one
  place", never "only" ([ADR general/0005](../../../adr/general/0005-marketing-size-wording.md)).

Sources and licences: [`ATTRIBUTION.md`](ATTRIBUTION.md).
