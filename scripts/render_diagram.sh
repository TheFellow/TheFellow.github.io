#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 INPUT.tex OUTPUT.png" >&2
  exit 2
fi

input=$1
output=$2
build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT
tectonic --outdir "$build_dir" "$input"
pdf="$build_dir/$(basename "${input%.tex}").pdf"
mkdir -p "$(dirname "$output")"
pdftocairo -png -r 240 -singlefile "$pdf" "${output%.png}"
