#!/usr/bin/env bash
# Build the 珍丸茶室 Pearl & Co. demo assets locally (no paid backend).
# Architecture A: continuous forward flight — one forward push-in "leg" per scene,
# no connectors (the engine crossfades consecutive legs, crossfade:0.12).
# stills -> webp (cwebp); legs -> ffmpeg zoompan; scrubbing encode per pipeline.md §5;
# plus 720p -g4 mobile variants (pipeline.md §6).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
WORK="$(mktemp -d)"
ASSETS="$ROOT/assets"
NAMES="farm kitchen shop delivery finale"
mkdir -p "$ASSETS/vid"

echo "== stills (Pillow) =="
python3 "$HERE/gen_stills.py" "$WORK"

echo "== stills -> webp (cwebp) =="
for n in $NAMES; do
  cwebp -quiet -q 84 -resize 1800 0 "$WORK/$n.png" -o "$ASSETS/$n.webp"
  echo "webp $ASSETS/$n.webp $(du -h "$ASSETS/$n.webp" | cut -f1)"
done

echo "== legs (forward camera push-in, ffmpeg zoompan) =="
gen_leg() { # name
  ffmpeg -v error -y -loop 1 -i "$WORK/$1.png" -t 4 -r 30 \
    -vf "scale=1920:1280,zoompan=z='min(zoom+0.0016,1.34)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1920x1080:fps=30,format=yuv420p" \
    "$WORK/leg_$1.mp4"
  echo "leg $1 ok"
}
for n in $NAMES; do gen_leg "$n"; done

echo "== scrubbing encode (crf20, GOP8, faststart, no audio) =="
enc() { ffmpeg -v error -y -i "$1" -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$2"; echo "enc $2 $(du -h "$2"|cut -f1)"; }
for n in $NAMES; do enc "$WORK/leg_$n.mp4" "$ASSETS/vid/$n.mp4"; done

echo "== mobile variants (720p, GOP4, crf23) =="
encm() { ffmpeg -v error -y -i "$1" -an -vf "scale=-2:720,unsharp=5:5:0.6:5:5:0.0" \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$2"; echo "encm $2 $(du -h "$2"|cut -f1)"; }
for n in $NAMES; do encm "$WORK/leg_$n.mp4" "$ASSETS/vid/$n-m.mp4"; done

echo "== done =="
find "$ASSETS" -type f | sort
rm -rf "$WORK"
