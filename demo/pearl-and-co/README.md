# 珍丸茶室 Pearl & Co. — scroll-world demo

A runnable [`scroll-world`](../../skills/scroll-world/SKILL.md) landing page: scroll drives a
camera that flies through five isometric diorama scenes — 茶園 → 珍珠工坊 → 旗艦茶室 →
外送 → 招牌 — as one continuous flight (Architecture A, `connectors: []`).

`index.html` and `scrub-engine.js` are the exact demo config + portable engine. The
`assets/` (webp stills + mp4 clips) are **local stand-ins** generated with Pillow +
ffmpeg (`build/`), so the full scroll-scrub experience runs with **zero credits**.

## Run

```bash
cd demo/pearl-and-co
python3 -m http.server 8100
# open http://localhost:8100
```

It is plain static files — deploy the folder to GitHub Pages, Netlify, S3, or any
static host as-is.

## Rebuild the placeholder assets

```bash
bash build/build_assets.sh   # needs python3-pil, webp (cwebp), ffmpeg
```

## Swap in the real AI-generated film

The stand-in art is a structural placeholder for the paid pipeline. To ship the real
photoreal diorama flight, run the skill's pipeline (`skills/scroll-world/references/pipeline.md`)
with the required backends and replace the files in `assets/` — `index.html` and
`scrub-engine.js` stay unchanged:

- **Monid CLI** (default video backend, Seedance 2.0, pay-per-clip) — needs an API key + balance.
- **Higgsfield CLI** (scene stills + fallback chain) — needs auth + credits.
- **ffmpeg/ffprobe** — frame extraction + scrubbing encode.

Add those credentials as Cloud Agent secrets to generate the real assets here.
