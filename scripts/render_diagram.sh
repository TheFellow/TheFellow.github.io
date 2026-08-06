#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 INPUT.tex OUTPUT.png" >&2
  exit 2
fi

input=$1
output=$2
repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

if [[ $input != /* ]]; then
  input="$PWD/$input"
fi

if [[ $output != /* ]]; then
  output="$PWD/$output"
fi

build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT
cd "$repo_root"
tectonic --outdir "$build_dir" "$input"
pdf="$build_dir/$(basename "${input%.tex}").pdf"
mkdir -p "$(dirname "$output")"
pdftocairo -png -r 240 -singlefile -transp "$pdf" "${output%.png}"
