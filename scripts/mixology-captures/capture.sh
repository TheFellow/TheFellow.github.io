#!/usr/bin/env bash
set -euo pipefail

# Usage: capture.sh /path/to/go-modular-monolith [output-directory]
site=$(cd "$(dirname "$0")/../.." && pwd)
source_repo=${1:?Pass the local go-modular-monolith repository}
output=${2:-"$site/assets/images/mixology"}
mkdir -p "$output"
output=$(cd "$output" && pwd)
revision=635c59b4101bdc614beb973cef83e8c2073a9787
scratch=$(mktemp -d "${TMPDIR:-/tmp}/mixology-capture.XXXXXX")
trap 'rm -rf "$scratch"' EXIT
mkdir -p "$scratch/source" "$scratch/frames"
git -C "$source_repo" archive "$revision" | tar -x -C "$scratch/source"
cp "$site/scripts/mixology-captures/tui_test.go" "$scratch/source/main/tui/deck_capture_test.go"
cp "$site/scripts/mixology-captures/gui_test.go" "$scratch/source/main/gui/deck_capture_test.go"
mkdir -p "$scratch/source/deckcapture" "$scratch/source/main/deck-error-probe"
cp "$site/scripts/mixology-captures/errors/cases.go" "$scratch/source/deckcapture/cases.go"
cp "$site/scripts/mixology-captures/errors/cli.go" "$scratch/source/main/deck-error-probe/main.go"
cp "$site/scripts/mixology-captures/errors/tui_test.go" "$scratch/source/main/tui/deck_errors_test.go"
cp "$site/scripts/mixology-captures/errors/gui_test.go" "$scratch/source/main/gui/deck_errors_test.go"
export MIXOLOGY_DB="$scratch/demo.db"
export MIXOLOGY_RENDER_DIR="$scratch/frames"
export LANG=en_US.UTF-8
cd "$scratch/source"
go run ./main/seed > "$scratch/seed.log" 2>&1 || { cat "$scratch/seed.log"; exit 1; }
go test -tags ci ./main/tui -run '^TestDeckCapture' -count=1
go test -tags ci ./main/gui -run '^TestDeckCapture' -count=1
go build -o "$scratch/mixology" ./main/cli
go build -o "$scratch/deck-error-probe" ./main/deck-error-probe
python3 "$site/scripts/mixology-captures/errors/capture_cli.py" "$scratch" "$output"
cp "$scratch/frames"/gui-*.png "$output/"
uv run "$site/scripts/mixology-captures/render_terminal.py" "$scratch/frames" "$output"
