# 珍丸茶室 Pearl & Co. — scroll-world demo

Cantonese (zh-Hant) scroll-scrubbed fly-through for **珍丸茶室 Pearl & Co.**

Architecture **A** (continuous legs, `connectors: []`): farm → kitchen → shop → delivery → finale.

## Serve locally

`scrub-engine.js` loads each clip as a `Blob`, so scrubbing works even when the static host does not support HTTP byte-range requests (including Python’s simple HTTP server).

```bash
cd demo
python3 -m http.server 8080
# open http://127.0.0.1:8080/
```

## Assets

| Path | Role |
|------|------|
| `assets/{farm,kitchen,shop,delivery,finale}.webp` | Section posters / stills |
| `assets/vid/*.mp4` | Desktop dive clips (`-g 8`, silent, `+faststart`) |
| `assets/vid/*-m.mp4` | Mobile variants |

**These are placeholders** (cream `#F5EDE0` + section accent blocks with a light zoom). Replace with real Higgsfield stills + Monid/Seedance (or Higgsfield) dive clips when regenerating via the scroll-world skill. Keep the same filenames or update `index.html`.

## Engine

`scrub-engine.js` is the portable scroll-scrub engine (blob seek, seam crossfade, mobile hardening, iOS poster/blob fallback). Mounted from `index.html` with Architecture A and empty `connectors`.
