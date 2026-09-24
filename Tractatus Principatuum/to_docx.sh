#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

pandoc tractate.md \
  --from markdown \
  --to docx \
  --shift-heading-level-by=-1 \
  --output tractate.docx

echo "wrote $(pwd)/tractate.docx"
