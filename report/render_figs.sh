#!/usr/bin/env bash
# Render the six Mermaid diagrams to high-resolution PNGs and rebuild the report.
set -euo pipefail

MMD=/workspaces/MK-PATH/report/mmd
FIGS=/workspaces/MK-PATH/report/figs
PCONF="$MMD/puppeteer-config.json"
mkdir -p "$FIGS"

render () { # $1 = source stem, $2 = output stem
  echo "rendering $1 -> $2.png"
  npx -y @mermaid-js/mermaid-cli@11 \
    -i "$MMD/$1.mmd" \
    -o "$FIGS/$2.png" \
    -b white -s 3 -w 1600 -p "$PCONF"
}

render fig_4_1 fig_4_1_architecture
render fig_4_2 fig_4_2_ingestion
render fig_4_3 fig_4_3_pipeline
render fig_4_4 fig_4_4_decision
render fig_4_5 fig_4_5_gates
render fig_4_6 fig_4_6_healing

echo "--- rendered files ---"
ls -la "$FIGS"

echo "--- rebuilding report ---"
python3 /workspaces/MK-PATH/report/build_report.py
