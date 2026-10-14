# MK-PATH Project Report — reproducible build

This folder holds the toolchain that produces `../MK-PATH_Project_Report.docx`.
The report text and tables live in `build_report.py`; the architecture diagrams
(Figs. 4.1–4.6) are authored as Mermaid source and rendered to PNG.

## What created the figures
- **Diagrams:** authored in Mermaid (`mmd/fig_4_*.mmd`), rendered with
  `@mermaid-js/mermaid-cli` 11 (headless Chromium) to high-resolution PNG.
- **Document assembly:** `python-docx` 1.2.0 (`build_report.py`).

> History: the first revision of the figures was drawn directly with matplotlib
> (`make_figs.py` in the scratch dir). They were replaced by the Mermaid set
> because hand-positioned matplotlib primitives gave cramped, inconsistent
> layout.

## Requirements
- Node.js (for `npx @mermaid-js/mermaid-cli@11`)
- Chromium runtime libraries (Ubuntu):
  `libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 libnss3 libnspr4 libx11-xcb1 libxcb-dri3-0 libxshmfence1 fonts-liberation fonts-noto-core`
- Python 3 with `python-docx`, `Pillow`, `matplotlib`

## Build
```bash
# 1. render the six diagrams into figs/
bash render_figs.sh

# 2. rebuild the .docx (overwrites ../MK-PATH_Project_Report.docx)
python3 build_report.py
```

## Editing a diagram
Edit the relevant `mmd/fig_4_*.mmd` and re-run `bash render_figs.sh`.

**Mermaid caveats learned here:**
- `direction LR` inside a `subgraph` is ignored by this Mermaid version, so
  multi-row layouts use one wide node per row instead of subgraph directions.
- With `htmlLabels` enabled, labels do **not** auto-wrap to `wrappingWidth`;
  insert explicit `<br/>` breaks and keep lines short so the diagram does not
  become a tall narrow column.
- Render with `-p mmd/puppeteer-config.json` (passes `--no-sandbox`) inside
  containers.

## Figures
| File | Report figure | Aspect | Height at 6.1 in | Label size |
|---|---|---|---|---|
| fig_4_1_architecture | Fig. 4.1 | 1.07 | 5.7 in | ~8.4 pt |
| fig_4_2_ingestion | Fig. 4.2 | 1.48 | 4.1 in | ~7.7 pt |
| fig_4_3_pipeline | Fig. 4.3 | 2.73 | 2.2 in | ~8.5 pt |
| fig_4_4_decision | Fig. 4.4 | 1.69 | 3.6 in | ~8.0 pt |
| fig_4_5_gates | Fig. 4.5 | 2.69 | 2.3 in | ~8.1 pt |
| fig_4_6_healing | Fig. 4.6 | 2.17 | 2.8 in | ~9.9 pt |
