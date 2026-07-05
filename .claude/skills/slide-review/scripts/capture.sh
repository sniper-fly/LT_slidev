#!/usr/bin/env bash
set -euo pipefail

# capture.sh — Slidev スライドを 1 スライド 1 PNG で書き出す
#
# Usage:
#   capture.sh <slide-dir> [--scale N] [--range R] [--with-clicks]
#
# Example:
#   capture.sh LT_slidev/slides/heartgarden
#   capture.sh LT_slidev/slides/heartgarden --scale 2 --range 1-5
#
# Output:
#   <slide-dir>/.review/<timestamp>/screenshots/*.png

SLIDE_DIR="${1:-}"
if [[ -z "$SLIDE_DIR" ]]; then
  echo "Usage: $0 <slide-dir> [--scale N] [--range R] [--with-clicks]" >&2
  exit 1
fi
shift

if [[ ! -d "$SLIDE_DIR" ]]; then
  echo "Error: directory not found: $SLIDE_DIR" >&2
  exit 1
fi
if [[ ! -f "$SLIDE_DIR/slides.md" ]]; then
  echo "Error: slides.md not found in $SLIDE_DIR" >&2
  exit 1
fi

SCALE=2
RANGE=""
WITH_CLICKS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scale)
      SCALE="$2"; shift 2 ;;
    --range)
      RANGE="$2"; shift 2 ;;
    --with-clicks)
      WITH_CLICKS="--with-clicks"; shift ;;
    *)
      echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REL_OUT=".review/$TIMESTAMP/screenshots"
ABS_OUT="$SLIDE_DIR/$REL_OUT"
mkdir -p "$ABS_OUT"

EXPORT_ARGS=(--format png --per-slide --scale "$SCALE" --output "$REL_OUT")
if [[ -n "$RANGE" ]]; then
  EXPORT_ARGS+=(--range "$RANGE")
fi
if [[ -n "$WITH_CLICKS" ]]; then
  EXPORT_ARGS+=("$WITH_CLICKS")
fi

(
  cd "$SLIDE_DIR"
  pnpm exec slidev export "${EXPORT_ARGS[@]}" slides.md
)

echo ""
echo "=== capture.sh: done ==="
echo "screenshot_dir=$ABS_OUT"
echo "files:"
ls -1 "$ABS_OUT" | sed 's/^/  /'
