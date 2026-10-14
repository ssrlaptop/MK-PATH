#!/usr/bin/env python3
"""Build the MK-PATH academic project report as a .docx, mirroring the reference report's
structure and style (CHAPTER N + ALL-CAPS sub-headings, captioned tables and figures).

Sources: the 20 MK-PATH repository documents + 13 approved external references.
No features, metrics or technologies are invented beyond those sources.
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FIG = "/workspaces/MK-PATH/report/figs"
OUT = "/workspaces/MK-PATH/MK-PATH_Project_Report.docx"
CENTRE = WD_ALIGN_PARAGRAPH.CENTER
JUST = WD_ALIGN_PARAGRAPH.JUSTIFY

doc = Document()

# ------------------------------------------------------------------ base styles
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.alignment = JUST


def _font(run, size=12, bold=False, italic=False, color=None, name="Times New Roman"):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def para(text, size=12, bold=False, italic=False, align=JUST, space_after=6, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    _font(p.add_run(text), size=size, bold=bold, italic=italic, color=color)
    return p


def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = JUST
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        _font(p.add_run(bold_prefix), bold=True)
    _font(p.add_run(text))
    return p


def chapter(num, title, first=False):
    if not first:
        doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = CENTRE
    p.paragraph_format.space_after = Pt(2)
    _font(p.add_run(f"CHAPTER {num}"), size=16, bold=True)
    p2 = doc.add_paragraph()
    p2.alignment = CENTRE
    p2.paragraph_format.space_after = Pt(14)
    _font(p2.add_run(title.upper()), size=14, bold=True)


def section(num, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    _font(p.add_run(f"{num}  {title.upper()}"), size=12.5, bold=True)


def subsection(num, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    _font(p.add_run(f"{num}  {title}"), size=12, bold=True, italic=True)


def table(caption, headers, rows, font_size=9.5):
    cap = doc.add_paragraph()
    cap.alignment = CENTRE
    cap.paragraph_format.space_before = Pt(8)
    cap.paragraph_format.space_after = Pt(3)
    _font(cap.add_run(caption), size=11, bold=True)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        pr = c.paragraphs[0]
        pr.paragraph_format.line_spacing = 1.0
        _font(pr.add_run(h), size=font_size, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            pr = cells[i].paragraphs[0]
            pr.paragraph_format.line_spacing = 1.0
            _font(pr.add_run(str(val)), size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def figure(path, caption, width=6.1):
    p = doc.add_paragraph()
    p.alignment = CENTRE
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(path, width=Inches(width))
    c = doc.add_paragraph()
    c.alignment = CENTRE
    c.paragraph_format.space_after = Pt(10)
    _font(c.add_run(caption), size=10.5, italic=True)


def placeholder(caption, lines=4):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cell = t.rows[0].cells[0]
    cell.text = ""
    pr = cell.paragraphs[0]
    pr.alignment = CENTRE
    for _ in range(lines):
        _font(pr.add_run("\n"), size=12)
    _font(pr.add_run("[ Insert screenshot / captured image here ]"), size=10, italic=True,
          color=(0x88, 0x88, 0x88))
    c = doc.add_paragraph()
    c.alignment = CENTRE
    c.paragraph_format.space_after = Pt(10)
    _font(c.add_run(caption), size=10.5, italic=True)


def footer_page_numbers():
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = CENTRE
    run = p.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    _font(run, size=10)


footer_page_numbers()

# ================================================================== DOCUMENT TITLE
tp = doc.add_paragraph(); tp.alignment = CENTRE
tp.paragraph_format.space_after = Pt(4)
_font(tp.add_run("MK-PATH"), size=20, bold=True)
st = doc.add_paragraph(); st.alignment = CENTRE
st.paragraph_format.space_after = Pt(16)
_font(st.add_run("A Multi-Agent, Evidence-Gated Platform for Autonomous Data "
                 "Transformation and Healing"), size=13, bold=True, italic=True)

# ================================================================== CHAPTER 1
chapter(1, "Introduction", first=True)

section("1.1", "Introduction and Definition")
para("MK-PATH (Multi-agent Knowledge Platform for Autonomous Transformation and Healing) is an "
     "evidence-gated autonomous data platform. It automates the journey from raw, heterogeneous "
     "datasets to verified, deployable machine-learning artifacts while keeping every transformation "
     "auditable and every consequential business decision under human control. The platform is built on "
     "a single governing principle: all measurable data operations are performed by deterministic "
     "components, and language models, where they are used at all, may only propose interpretations "
     "and never finalise them.")
para("In practical terms, MK-PATH ingests multi-format data (CSV, TSV, TXT, JSON, Parquet, Excel and "
     "SQL, individually or bundled in ZIP archives), registers each normalised dataset as a queryable "
     "DuckDB view, profiles it deterministically, grounds its columns in a semantic knowledge layer, "
     "pauses for human clarification when meaning is ambiguous, plans and executes analytical queries, "
     "trains and compares models in a tournament, evaluates a set of mandatory verification gates, "
     "heals data-quality problems without ever mutating the original data, and finally generates a "
     "self-contained FastAPI inference service. The positioning recorded in the project README is "
     "simply \u201cEvidence-Gated Autonomous Data Platform\u201d.")

section("1.2", "The Data Preparation and Trust Problem")
para("In most organisations the path from raw data to a deployable model is fragmented across ad-hoc "
     "spreadsheets, personal scripts and disconnected tools. Each step is subjective, difficult to "
     "reproduce and rarely accompanied by provenance. The consequences are well documented in the "
     "literature surveyed in Chapter 2: inconsistent profiling, undetected temporal leakage, "
     "unexplained model behaviour and silent data corruption. When large language models are inserted "
     "into this pipeline naively, a further risk appears \u2014 fabricated metrics and ungrounded business "
     "claims that cannot be traced to real rows.")
para("MK-PATH addresses this problem by separating what is provable from what is proposed. Anything "
     "that can be computed \u2014 row and column statistics, quality scores, aggregations, model metrics "
     "\u2014 is computed deterministically and independently reproducible. Anything that concerns business "
     "meaning is treated as a proposal that must be confirmed by a human decision, recorded with "
     "evidence in an immutable audit trail.")

section("1.3", "Deterministic Profiling and Zero-LLM Quality Scoring")
para("Profiling is performed entirely without a language model. The profiling engine "
     "(deterministic:v1:duckdb+pyarrow+pandas) computes the full set of required metrics over a "
     "dataset's normalized Parquet representation using DuckDB SQL: row and column counts, types, "
     "missing counts and percentages, distinct counts, cardinality ratios, exact duplicate rows, "
     "constant columns, numeric statistics (min, max, mean, median, standard deviation, quartiles), "
     "IQR-based outlier indicators, date/time detection, potential-identifier detection, column roles, "
     "target and leakage candidates, and a capped correlation summary. These metrics are reduced to a "
     "documented, reproducible quality score on a 0\u2013100 scale with letter grades. Because the score is "
     "a closed-form formula rather than a model output, re-profiling the same data produces byte-identical "
     "results \u2014 a property explicitly verified in the project's own audits.")

section("1.4", "Multi-Agent Orchestration and LLM Grounding")
para("The end-to-end workflow is expressed as a typed LangGraph StateGraph that chains deterministic "
     "and AI-assisted stages: INGEST, PROFILE, SEMANTIC_ANALYSIS, AMBIGUITY_CHECK, HUMAN_BREAKPOINT, "
     "ANALYSIS_PLANNING, DATA_ANALYST, DATA_SCIENTIST, VERIFICATION, MODEL_TOURNAMENT, ML_ENGINEER, "
     "ARTIFACT_GENERATION, AUDIT and END. Where a language model contributes an analytical plan, that "
     "plan is validated against the real table schema before any query is generated, which eliminates "
     "SQL binder errors and keeps every reported number traceable to verified rows. The orchestrator "
     "checkpoints its state through a MemorySaver so that a workflow paused at a human breakpoint is not "
     "lost while awaiting a decision.")

section("1.5", "Evidence-Gated Verification and Explainability")
para("No artifact is treated as deployable merely because it runs. A central verification engine "
     "aggregates eight deterministic gates \u2014 Data Quality, Semantic Validity, Temporal Leakage, Causal "
     "Validation, Explainability, Fairness, Performance and Artifact Validation. If any mandatory gate "
     "fails, the deployment status defaults to BLOCKED, and the frontend is structurally prevented from "
     "overriding that verdict \u2014 it may only request a re-run, record a human review decision, or "
     "acknowledge the result. Explainability is provided through SHAP-based feature attribution, and "
     "fairness is evaluated conditionally when protected or group attributes genuinely exist in a "
     "dataset. Temporal leakage is intercepted deterministically by checking that each feature's "
     "availability time does not exceed the prediction time.")

section("1.6", "Motivation")
para("The motivation for MK-PATH is threefold. First, reproducibility: deterministic computation "
     "over a fixed dataset should yield the same answer every time. Second, trust: a stakeholder should "
     "be able to see exactly which rows and which SQL produced each reported figure, and to know that a "
     "model was blocked from deployment when it failed a gate. Third, safety of transformation: data "
     "healing must never destroy the original evidence, so MK-PATH always writes corrections to a new "
     "derived dataset and reports the quality change before and after.")

section("1.7", "Objectives")
para("The objectives of the work reported here are:")
bullet("ingest heterogeneous data formats, individually or in archives, through a hardened, "
       "traversal-safe pipeline;")
bullet("normalise every ingested source into a columnar representation queryable through an embedded "
       "analytical engine without loading the full dataset into memory;")
bullet("produce deterministic, zero-LLM quality profiles and a reproducible quality score;")
bullet("ground columns in a semantic knowledge layer whose business meaning is confirmed by a human "
       "wherever it is ambiguous, with no language model permitted to finalise meaning;")
bullet("plan and execute schema-grounded analytical queries that yield empirical conclusions and an "
       "actionable decision matrix;")
bullet("train and compare candidate models under a tournament with a multi-objective selection "
       "criterion and an out-of-time validation option;")
bullet("enforce mandatory, deterministic verification gates that can block deployment;")
bullet("heal data-quality problems into an auditable, immutable-original derived dataset;")
bullet("generate a deployable, self-validating FastAPI inference artifact with genuine model weights; "
       "and")
bullet("record every stage in an append-only audit trail.")

section("1.8", "Scope and Implementation-Status Convention")
para("This report distinguishes four states of maturity for each capability, and the same convention "
     "is used consistently in the chapters that follow:")
table("Table 1.1: Implementation-status convention used throughout this report.",
      ["Tag", "Meaning"],
      [["[Tested]", "Implemented and independently exercised by automated tests and/or the end-to-end real-data validation."],
       ["[Implemented]", "Present and reachable in code, but not independently exercised by the validation audit."],
       ["[Partial]", "Implemented with a documented gap (a missing dependency, an unexercised path, or a limited scope)."],
       ["[Planned]", "Specified or recommended but not implemented in the validated prototype."]])
para("This convention matters because the project's own documentation records both successes and "
     "honest shortcomings, and this report preserves that distinction rather than smoothing it over.")

# ================================================================== CHAPTER 2
chapter(2, "Literature Survey")

section("2.1", "Survey of Related Work")
para("MK-PATH draws on several research streams: data profiling and cleaning, data-centric AI, "
     "automated model selection, multi-agent orchestration with language models, semantic and schema "
     "matching, explainability, causal inference, leakage detection, human-in-the-loop learning, and "
     "fairness. Table 2.1 surveys representative work in each area and records how it relates to the "
     "platform. The references are real, published works with stable identifiers; they are cited as "
     "background and motivation, not as claims that MK-PATH reproduces any specific published method "
     "unless the project sources state so.")
table("Table 2.1: Survey of related work and its relevance to MK-PATH.",
      ["#", "Authors (Year)", "Publication", "Area", "Approach", "Relevance to MK-PATH"],
      [
        ["1", "Abedjan, Golab & Naumann (2015)", "The VLDB Journal 24(4):557\u2013581",
         "Data profiling",
         "Comprehensive survey of relational data-profiling techniques and metadata.",
         "Motivates the deterministic, metadata-first profiling stage."],
        ["2", "Rekatsinas, Chu, Ilyas & R\u00e9 (2017)", "PVLDB 10(11):1190\u20131201",
         "Data repair (HoloClean)",
         "Probabilistic-inference repair unifying integrity constraints, external data and statistics.",
         "Informs the healing engine, which keeps the original dataset immutable."],
        ["3", "Zha et al. (2023)", "arXiv:2303.10158",
         "Data-centric AI",
         "Systematic survey of data development and data maintenance for AI.",
         "Frames the platform\u2019s data-first design and placement of verification gates."],
        ["4", "He, Zhao & Chu (2021)", "Knowledge-Based Systems 212:106622",
         "AutoML / model selection",
         "Survey of automated model, hyper-parameter and pipeline search.",
         "Context for the automated model tournament and Pareto selection."],
        ["5", "Wu et al. (2023)", "arXiv:2308.08155",
         "Multi-agent LLM systems (AutoGen)",
         "Conversable-agent framework for composing LLM applications.",
         "Related work for MK-PATH\u2019s multi-agent orchestration (built on LangGraph)."],
        ["6", "Qin et al. (2022)", "arXiv:2208.13629",
         "Text-to-SQL parsing",
         "Survey of natural-language-to-SQL generation.",
         "Background for schema-grounded analytical query generation."],
        ["7", "Shvaiko & Euzenat (2013)", "IEEE TKDE 25(1):158\u2013176",
         "Ontology / schema matching",
         "Survey of matching techniques and open challenges.",
         "Background for the semantic knowledge layer\u2019s structural grounding."],
        ["8", "Lundberg & Lee (2017)", "NeurIPS 2017 (arXiv:1705.07874)",
         "Explainable AI (SHAP)",
         "Unified additive feature-attribution framework.",
         "Technique adopted by the explainability gate."],
        ["9", "Sharma & Kiciman (2020)", "arXiv:2011.04216",
         "Causal inference (DoWhy)",
         "End-to-end causal inference: identify, estimate and refute.",
         "Intended causal-analysis capability; not bundled in the validated runtime."],
        ["10", "Kaufman, Rosset, Perlich & Stitelman (2012)", "ACM TKDD 6(4)",
         "Leakage detection",
         "Formulation, detection and avoidance of data leakage.",
         "Direct basis for the temporal-leakage interceptor."],
        ["11", "Mosqueira-Rey et al. (2023)", "Artificial Intelligence Review 56:3005\u20133054",
         "Human-in-the-loop ML",
         "State-of-the-art survey of interactive learning.",
         "Justifies the human semantic breakpoint and approval workflows."],
        ["12", "Mehrabi et al. (2021)", "ACM Computing Surveys 54(6):115",
         "Bias & fairness",
         "Taxonomy of bias sources and fairness metrics.",
         "Grounds the conditional fairness gate."],
        ["13", "Barocas, Hardt & Narayanan (2023)", "MIT Press (open access)",
         "Fairness & ML (book)",
         "Foundations and limitations of fairness in machine learning.",
         "Normative framing for the fairness gate\u2019s warnings."],
      ], font_size=8.2)

section("2.2", "Research Gap and Positioning")
para("Taken together, the surveyed work provides strong individual components \u2014 profiling, repair, "
     "automated model selection, orchestration, explainability, leakage detection, human oversight and "
     "fairness \u2014 but each is typically studied in isolation. Few systems bind them into a single, "
     "auditable pipeline in which every quantitative claim is deterministic and independently "
     "reproducible, every business interpretation is human-confirmed, and deployment is genuinely "
     "gated by verification rather than by convention.")
para("MK-PATH is positioned precisely in that gap. Its contribution is architectural rather than "
     "algorithmic: it composes existing, well-understood techniques behind a strict evidence gate and a "
     "deterministic execution core, and it refuses to let a language model produce a number or finalise a "
     "meaning. The remainder of this report describes that architecture, its modules and the results of "
     "its end-to-end validation.")

# ================================================================== CHAPTER 3
chapter(3, "System Analysis")

section("3.1", "Overview")
para("This chapter analyses the approaches that predominate in current data-to-model workflows, "
     "summarises their limitations, and states the problem that MK-PATH sets out to solve. The analysis "
     "is grounded in the surveyed literature (Chapter 2) and in MK-PATH\u2019s own recorded design "
     "rationale; it does not invent competing products or vendors.")

section("3.2", "Methodologies in Existing Approaches")
para("Four broad methodology families can be identified from the surveyed work and the project\u2019s "
     "stated positioning.")
bullet("Manual, script-driven pipelines. ", bold_prefix="\u2022  ")
para("Analysts move data through spreadsheets and bespoke scripts. Profiling is informal, quality "
     "decisions are subjective, and reproducibility depends on the individual.")
bullet("Standalone automated machine learning. ", bold_prefix="\u2022  ")
para("Model-search tools automate algorithm and hyper-parameter selection but generally assume the "
     "input data has already been cleaned and semantically understood.")
bullet("Unguarded LLM analytics. ", bold_prefix="\u2022  ")
para("Emerging assistants translate natural language directly into code, SQL or narrative conclusions; "
     "without schema grounding and deterministic execution, such systems can produce plausible but "
     "incorrect results.")
bullet("Single-purpose business-intelligence tools. ", bold_prefix="\u2022  ")
para("Visualisation and dashboarding layers present results well but neither verify data quality nor "
     "gate deployment on evidence.")

section("3.3", "Limitations of Current Approaches")
para("The following limitations, drawn from the literature and from MK-PATH\u2019s recorded rationale, "
     "motivate the proposed system.")
bullet("Subjectivity and non-reproducibility: profiling and cleaning decisions are often undocumented "
       "and differ between runs or analysts.")
bullet("Hallucination risk: ungrounded language models can fabricate metrics, targets and business "
       "claims that cannot be traced to real rows.")
bullet("Temporal leakage: features that would not be available at prediction time can silently inflate "
       "apparent model performance.")
bullet("Absent verification gating: a model that trains successfully is frequently assumed to be "
       "deployable, with no mandatory check on quality, leakage, explainability or fairness.")
bullet("Destructive transformation: cleaning frequently overwrites the source data, erasing the "
       "evidence needed to audit or reverse it.")
bullet("Weak human oversight: meaningful ambiguities in column semantics are resolved by guesswork "
       "rather than recorded human decisions.")
bullet("Poor explainability and fairness coverage: feature attribution and group-fairness checks are "
       "often omitted or performed post hoc without documentation.")

section("3.4", "Problem Statement")
para("The problem addressed by MK-PATH can therefore be stated as follows: to build a platform that "
     "carries raw, heterogeneous data through profiling, semantic grounding, analysis, modelling, "
     "verification and healing to a deployable artifact, such that (i) every quantitative result is "
     "produced by deterministic, reproducible computation; (ii) every business meaning is grounded in "
     "real columns and confirmed by a human where ambiguous; (iii) deployment is permitted only when "
     "all mandatory verification gates pass; (iv) data transformation never destroys the original; and "
     "(v) every action is recorded in an auditable trail.")

# ================================================================== CHAPTER 4
chapter(4, "Proposed System")

section("4.1", "Overview")
para("MK-PATH is organised as a layered platform. A React/TypeScript front end communicates with a "
     "FastAPI back end over a REST API. The back end hosts a LangGraph orchestrator that sequences "
     "deterministic and AI-assisted stages, a deterministic compute core built on DuckDB, pandas and "
     "PyArrow, a semantic knowledge layer, a verification engine and a healing engine. Metadata and "
     "audit state are stored in MongoDB Atlas (with a local JSON fallback), while raw datasets, "
     "normalized Parquet, profiles, models and generated artifacts live on disk in an isolated storage "
     "root. This chapter describes each part of the proposed system and tags its maturity.")

section("4.2", "Proposed System Architecture")
para("Figure 4.1 shows the layered architecture. The presentation layer exposes the product domains "
     "(dashboard, upload, dataset explorer, knowledge, agents, analysis, verification, healing, "
     "artifacts and audit). The API layer maps these to FastAPI routers. The orchestration layer is the "
     "LangGraph state machine. Beneath it sits the deterministic compute layer, and at the base the "
     "data and metadata layer enforces storage isolation and the single source of truth for project "
     "state.")
figure(f"{FIG}/fig_4_1_architecture.png",
       "Fig. 4.1: Layered architecture of the MK-PATH platform.")

section("4.3", "Universal Data Ingestion and Data Model Development")
para("Ingestion is designed for untrusted input. Uploads are streamed to disk and pass size and "
     "content-signature checks before any parsing. ZIP archives are extracted entry-by-entry under a "
     "strict security model: traversal and absolute-path entries, symlinks, special files and encrypted "
     "entries are rejected before extraction; entry-count, estimated-size and compression-ratio budgets "
     "are enforced; and a running byte budget guards against lying headers. Duplicate names are "
     "disambiguated, and corrupt entries are reported rather than allowed to crash the pipeline. "
     "Uploaded filenames are never used as paths. [Tested]")
para("Each supported source (CSV, TSV, TXT, JSON, Parquet, XLSX, XLS and SQL) is parsed deterministically "
     "and normalised to Parquet. SQL files are treated as untrusted and executed only through a narrow "
     "allow-list (CREATE TABLE and INSERT \u2026 VALUES) inside a throwaway in-memory DuckDB; destructive or "
     "filesystem-capable statements are rejected before execution. Every normalised source is registered "
     "as a lazy DuckDB view named ds_<dataset_id> over its Parquet file, and a metadata document is "
     "written to the datasets collection together with audit events. Figure 4.2 summarises the pipeline.")
figure(f"{FIG}/fig_4_2_ingestion.png",
       "Fig. 4.2: Universal ingestion pipeline and normalized result contract.")
para("The normalized result contract for every ingested source is: dataset_id, source_file_id, "
     "original_filename, source_format, storage_path, normalized_path, table_name, schema, row_count, "
     "column_count, ingestion_status, warnings, errors, created_at, upload_id, archive_member, "
     "parent_archive, view_name and profile. Large-archive ingestion is configured for payloads up to "
     "500 MB, with archive entry and decompressed-size quotas. [Tested]")

section("4.4", "Deterministic Profiling and Quality Scoring")
para("The profiling engine (deterministic:v1:duckdb+pyarrow+pandas) computes all required metrics with "
     "DuckDB SQL over the normalized Parquet: counts, types, missingness, distinctness, cardinality, "
     "exact duplicates, constant columns, numeric statistics, IQR outlier indicators, date detection, "
     "identifier detection, column roles, target candidates, leakage candidates and a capped correlation "
     "summary. The quality score is a documented closed-form formula:")
para("score = 100 \u2212 min(40, 40 \u00d7 missing_ratio) \u2212 min(20, 20 \u00d7 duplicate_ratio) "
     "\u2212 min(20, 10 \u00d7 constant_columns) \u2212 min(20, 10 \u00d7 high_severity_issues) "
     "\u2212 min(10, 5 \u00d7 medium_severity_issues),", align=CENTRE, italic=True)
para("floored at zero and reported to one decimal place, with grades A \u2265 90, B \u2265 80, C \u2265 70, "
     "D \u2265 60 and F < 60. Because the formula is deterministic, re-profiling the same data yields "
     "identical statistics and issue counts; the project\u2019s audits assert byte-identical results and "
     "hand-computed scores of exactly 63.8 (grade D) for a dirty fixture and 90.0 (grade A) for a clean "
     "one. The full report is written to disk and a summary is stored in MongoDB. [Tested]")

section("4.5", "Semantic Knowledge Layer and Human-in-the-Loop Breakpoint")
para("The semantic layer represents 13 concept types \u2014 dataset, table, column, metric, dimension, "
     "target, feature, event, business_term, definition, relationship, ambiguity and user_decision. A "
     "deterministic builder derives structural roles from the profile (falling back to schema types and "
     "name patterns), attaches a small business glossary, detects ambiguities and computes a documented "
     "confidence value. An optional pluggable provider (for example Google Gemini) may propose "
     "interpretations, but every such proposal is recorded with source llm_proposed and status "
     "needs_review: the provider layer cannot finalise semantics. [Tested]")
para("When confidence falls below a configurable threshold (default 0.7), the workflow interrupts and a "
     "clarification question is created. Blocking ambiguities include target selection (zero or two or "
     "more candidates) and value mapping for coded columns. The same question signature is never asked "
     "twice while it remains open. A human resolves the question through a dedicated endpoint, which "
     "records a UserDecision \u2014 the only mechanism capable of setting business meaning \u2014 recomputes "
     "confidence and resumes the workflow. Without an LLM key configured, the layer runs "
     "deterministic-only, states so in warnings, and invents nothing. [Tested]")

section("4.6", "LangGraph Multi-Agent Orchestrator")
para("The orchestrator is a typed StateGraph (MKPathState) carrying schema, profile, semantic context, "
     "ambiguities, human decisions, models and artifacts between nodes. The stage sequence is shown in "
     "Figure 4.3. A MemorySaver checkpoints state so that a workflow paused at HUMAN_BREAKPOINT is "
     "retained until the clarification is resolved, and every transition is written to the audit system. "
     "The nodes were verified to operate on real dataset metadata, real DuckDB profiles, real semantic "
     "context, real analytical plans, real verification gates, real model tournaments and real artifact "
     "generation \u2014 mock dataset identifiers and fabricated status transitions were removed during "
     "remediation. [Tested]")
figure(f"{FIG}/fig_4_3_pipeline.png",
       "Fig. 4.3: LangGraph agent execution pipeline with the human breakpoint.")

section("4.7", "Data Analyst Agent and Decision Framework")
para("The analyst stage accepts a natural-language business goal and matches the requested metrics and "
     "dimensions against columns that actually exist in the active view, inspecting the DuckDB DESCRIBE "
     "output before generating any query; if a requested column is absent, the engine falls back to the "
     "leading statistical numeric or categorical columns rather than failing. This schema grounding "
     "eliminates SQL binder errors. Execution is performed by the deterministic DuckDB engine, which "
     "computes real aggregations (SUM, AVG, MIN, MAX, STDDEV), primary-segment concentration and "
     "filter-segment evidence, and captures full provenance (dataset, table context, exact SQL and "
     "timestamp). The results are packaged into an executive summary, empirical conclusions and an "
     "actionable decision matrix whose rows carry a focus area, key finding, strategic recommendation, "
     "impact rating and confidence score. Figure 4.4 illustrates the flow. [Tested]")
figure(f"{FIG}/fig_4_4_decision.png",
       "Fig. 4.4: Business-goal analysis, empirical conclusions and decision framework.")

section("4.8", "Data Scientist Agent and Model Tournament")
para("The model tournament fits candidate models on a real feature matrix and target array and records "
     "genuine evaluation metrics (accuracy, precision, recall, F1, ROC-AUC, training time, inference "
     "latency and model size), selecting a champion through a multi-objective (Pareto) criterion that "
     "trades off performance, latency and a resource-cost proxy rather than absolute accuracy alone. "
     "Chronological (out-of-time) validation is available for temporal datasets to avoid leaky random "
     "splits, and linear models are wrapped in a scaling pipeline with convergence limits to eliminate "
     "convergence warnings. In the validated end-to-end run, candidate selection, training and "
     "evaluation all used real rows; LightGBM was skipped because its native runtime library was "
     "unavailable, and the tournament fell back to scikit-learn models. The causal-analysis stage "
     "(DoWhy) is present as a specified capability but was reported NOT_IMPLEMENTED in the validated "
     "runtime because the package was not bundled. [Partial]")

section("4.9", "Evidence-Gated Verification Engine")
para("The verification engine aggregates eight mandatory checks \u2014 Data Quality, Semantic Validity, "
     "Temporal Leakage, Causal Validation, Explainability, Fairness, Performance and Artifact Validation "
     "\u2014 and determines the deployment status. If any mandatory gate fails, the status defaults to "
     "BLOCKED, and the resulting DeploymentReadinessReport is passed downstream with an explicit "
     "instruction that the language model may not override it. Temporal leakage is checked "
     "deterministically by requiring every feature\u2019s available time to be no later than the prediction "
     "time. Explainability uses SHAP to produce global and local feature attributions, and fairness "
     "evaluates the true-positive rate, false-positive rate and selection rate across groups, but only "
     "when protected or group attributes genuinely exist; a disparity raises a warning gate rather than "
     "an undocumented hard block. Figure 4.5 shows the gate structure. [Partial \u2014 gates implemented; "
     "fairness and explanation gates depend on suitable columns being present.]")
figure(f"{FIG}/fig_4_5_gates.png",
       "Fig. 4.5: Evidence-gated verification engine and deployment decision.")

section("4.10", "Transformation and Healing Engine")
para("Healing is governed by an absolute tenet: the original data is immutable. Corrections such as "
     "median or forward/backward imputation and categorical normalisation are written to a new derived "
     "dataset, and a BeforeAfterQualityReport records the before and after quality scores with explicit, "
     "tracked improvements so a human can accept or reject the change without any risk of data loss. "
     "During remediation the engine was changed from hard-coded scores to real computation of missing "
     "cell counts and real before/after scores from the actual dataframes. Figure 4.6 illustrates the "
     "flow. [Tested]")
figure(f"{FIG}/fig_4_6_healing.png",
       "Fig. 4.6: Immutable-original healing with before/after quality reporting.")

section("4.11", "ML Engineer and FastAPI Artifact Generation")
para("On a READY deployment report, the ML engineer stage provisions a complete, self-contained "
     "inference service: Pydantic request/response schemas generated from the dataset\u2019s final semantic "
     "feature dictionary, a FastAPI application exposing /predict, /health, /metadata and /model-card, "
     "generated integration tests, a model card and a deployment README. Genuine trained model binaries "
     "are exported and loaded, and an automated validation routine executes a real inference before the "
     "artifact is marked PASS. If the deployment report is blocked, the stage returns a structured "
     "diagnostic report instead of exposing failed logic. All outputs are stored under "
     "artifacts/<project_id>/<run_id>/ and excluded from version control. [Tested]")

section("4.12", "Visualization Suite and Decision Framework")
para("The platform ships an 18-chart visualization suite implemented as pure, responsive React SVG in "
     "DataVisualizer.tsx, embedded in the Data Analyst Workspace and the Dataset Explorer. The charts "
     "are grouped into five categories: comparison and ranking (vertical bar, horizontal bar, grouped "
     "bar, stacked bar, line, area); composition and part-to-whole (pie/donut, treemap, stacked area, "
     "waterfall); distribution and spread (histogram, box-and-whisker, density, violin); correlation and "
     "relationship (scatter, bubble, heatmap); and specialised workflows (Sankey, choropleth, radar). "
     "Because the suite is implemented client-side without a charting dependency, it builds and lints "
     "cleanly. [Implemented]")
placeholder("Fig. 4.7: The 18-chart analytics visualization suite in the Data Analyst Workspace "
            "(screenshot placeholder).", lines=5)

section("4.13", "Advantages of the Proposed System")
bullet("Deterministic core: profiling, aggregation and metric computation are reproducible and "
       "auditable, not probabilistic.")
bullet("Grounded language models: LLM output is advisory and schema-validated, never authoritative for "
       "numbers or business meaning.")
bullet("Human-accountable semantics: ambiguities pause the workflow and are resolved by recorded human "
       "decisions.")
bullet("Fail-safe deployment: mandatory gates can block deployment and cannot be overridden by the "
       "frontend.")
bullet("Immutable-original healing: transformations are reversible and reported before/after.")
bullet("Provenance by default: every stage writes to an append-only audit trail.")
bullet("Storage isolation: datasets, models, artifacts and logs remain confined to the project storage "
       "root.")

# ================================================================== CHAPTER 5
chapter(5, "System Specification")

section("5.1", "Hardware Requirements")
para("MK-PATH is deliberately CPU-oriented. The validated runtime installed no deep-learning "
     "frameworks: PyTorch, TensorFlow, CUDA, local large language models, Spark, Kubernetes and Docker "
     "all registered zero matches in the pinned dependency set. Table 5.1 lists the hardware envelope "
     "consistent with the recorded environment and the project\u2019s own storage audit.")
table("Table 5.1: Hardware requirements.",
      ["Component", "Requirement", "Notes"],
      [["Processor", "64-bit x86-64 CPU",
        "Recorded end-to-end environment: Python 3.10.7 (x64); analytical work is CPU-bound."],
       ["Graphics card", "Not required",
        "No CUDA / GPU dependency; no PyTorch or TensorFlow in the runtime."],
       ["Memory", "Moderate; sized to the working dataset",
        "DuckDB performs disk-backed analytical processing; the evaluation reported no out-of-memory events."],
       ["Storage", "Dedicated volume for the project root",
        "Validated footprint under 1 GB including the virtual environment; datasets, models, artifacts and logs isolated from the OS drive."],
       ["Display / input", "Standard display, keyboard, mouse",
        "The interface is a web application served by the front-end tooling."],
       ["Network", "Optional",
        "Needed for MongoDB Atlas and optional LLM providers; the platform degrades to a local JSON fallback offline."]])

section("5.2", "Software Requirements")
table("Table 5.2: Software requirements.",
      ["Category", "Software"],
      [["Operating system", "Windows 10/11 (64-bit); Linux/macOS are viable with path adjustments."],
       ["Backend runtime", "Python 3.10.x"],
       ["Backend framework", "FastAPI with Uvicorn and Pydantic; python-multipart for uploads."],
       ["Analytical engine", "DuckDB, PyArrow, pandas, NumPy"],
       ["Machine learning", "scikit-learn (LightGBM optional; not active in the validated run)."],
       ["Orchestration", "LangGraph / LangChain"],
       ["Database", "MongoDB Atlas (or the built-in local JSON fallback)."],
       ["Explainability", "SHAP"],
       ["Causal analysis (optional)", "DoWhy (specified; not bundled in the validated runtime)."],
       ["LLM providers (optional)", "Google Gemini and Groq."],
       ["Testing", "pytest (backend)."],
       ["Front end", "Node.js 20+, React 19, TypeScript, Vite, Tailwind CSS v4, Radix UI primitives, Lucide icons."],
       ["Version control", "Git / GitHub"]])

section("5.3", "Technologies Used")
subsection("5.3.1", "Python")
para("Python is the implementation language of the back end. It provides the ecosystem on which the "
     "platform depends \u2014 FastAPI for the API, pandas and PyArrow for data handling, DuckDB for "
     "analytics, scikit-learn for modelling, and LangGraph for orchestration \u2014 while its readability "
     "supports the platform\u2019s emphasis on auditable, deterministic code.")
subsection("5.3.2", "FastAPI")
para("FastAPI provides the REST API layer, request validation (through Pydantic) and the generated "
     "deployment services. It also renders interactive API documentation, which was used during testing. "
     "Its asynchronous model suits the platform\u2019s streamed uploads and asynchronous database access.")
subsection("5.3.3", "DuckDB")
para("DuckDB is the deterministic analytical engine. Each normalized dataset is exposed as a lazy view "
     "over Parquet, so profiling and business aggregations run in SQL directly over columnar storage "
     "without loading full datasets into memory. The same engine underpins the schema-grounded SQL used "
     "by the analyst stage.")
subsection("5.3.4", "MongoDB Atlas")
para("MongoDB Atlas stores metadata and audit state only \u2014 project and dataset documents, versioned "
     "semantic contexts, clarification questions, human decisions, validation results, models, "
     "artifacts, healing events and audit events. It never stores raw datasets, Parquet files or model "
     "binaries. When Atlas is unreachable, the platform degrades gracefully to a local, persistent JSON "
     "fallback so that the API continues to serve without crashing.")
subsection("5.3.5", "LangGraph and LangChain")
para("LangGraph expresses the orchestration as a typed state machine, with conditional interruption for "
     "the human breakpoint and checkpointed state. LangChain supplies the optional model-provider "
     "integration used for advisory semantic proposals and analytical plans, always behind "
     "deterministic validation.")
subsection("5.3.6", "scikit-learn")
para("scikit-learn implements the model tournament. Linear and logistic models are wrapped in a scaling "
     "pipeline with explicit convergence limits and fixed random state, ensuring deterministic ranking "
     "and eliminating convergence warnings. Candidate metrics are computed from real predictions.")
subsection("5.3.7", "LightGBM")
para("LightGBM is listed as a tournament candidate because gradient-boosted trees are a natural "
     "complement to the scikit-learn models. In the validated environment its native runtime library "
     "was unavailable, so the tournament skipped it and fell back to scikit-learn candidates; this is "
     "recorded as a partial capability rather than a completed one.")
subsection("5.3.8", "React and TypeScript")
para("The front end is a React 19 application written in TypeScript and built with Vite. TypeScript "
     "provides compile-time type safety across the API client and components, and the production build "
     "was used as a front-end verification signal.")
subsection("5.3.9", "Tailwind CSS")
para("Tailwind CSS v4 provides the styling system, with Radix UI primitives and Lucide icons for "
     "accessible, composable components. The interface is deliberately derived from real backend state "
     "rather than presentation-layer constants.")
subsection("5.3.10", "Custom SVG Visualization Engine")
para("The 18-chart suite is rendered as hand-written responsive SVG rather than a third-party charting "
     "library. This avoids an external dependency, keeps the bundle small and allows the charts to be "
     "driven directly by deterministic query results.")
subsection("5.3.11", "Git and GitHub")
para("All source is version-controlled with Git and hosted on GitHub. Generated models, artifacts, "
     "datasets and the virtual environment are intentionally excluded from the repository to keep it "
     "clean and free of large binaries.")

# ================================================================== CHAPTER 6
chapter(6, "Module Description")
para("The platform is decomposed into ten modules. Table 6.1 summarises them and their maturity; the "
     "sub-sections that follow describe each in turn.")
table("Table 6.1: MK-PATH module summary.",
      ["Module", "Name", "Responsibility", "Status"],
      [["1", "Ingestion", "Multi-format parsing, ZIP security, normalization to Parquet, DuckDB registration.", "[Tested]"],
       ["2", "Profiling", "Zero-LLM data-quality metrics and reproducible quality scoring.", "[Tested]"],
       ["3", "Semantic Knowledge", "Concept grounding, ambiguity detection and human clarification.", "[Tested]"],
       ["4", "Orchestrator", "LangGraph state machine and audit-integrated transitions.", "[Tested]"],
       ["5", "Analysis", "Schema-grounded SQL analytics, conclusions and decision matrix; causal interface.", "[Tested] / [Planned] for causal"],
       ["6", "Modeling", "Model tournament with multi-objective selection.", "[Partial]"],
       ["7", "Verification", "Eight mandatory gates and deployment readiness.", "[Partial]"],
       ["8", "Healing", "Immutable-original derived-data repair with before/after reporting.", "[Tested]"],
       ["9", "Engineering", "FastAPI artifact generation and self-validation.", "[Tested]"],
       ["10", "Frontend & Visualization", "React workspace and 18-chart SVG suite.", "[Implemented]"]])

section("6.1", "Module 1 \u2014 Ingestion")
para("The ingestion module validates the upload signature and size, stores the original securely, "
     "extracts archives under strict budgets, selects a deterministic parser per format, normalises to "
     "Parquet, and registers a lazy DuckDB view. It emits a complete normalized result contract and "
     "audit events, and it maps every failure to a structured HTTP status without leaking internals. "
     "[Tested]")

section("6.2", "Module 2 \u2014 Profiling")
para("The profiling module computes the full metric set and the documented quality score entirely "
     "without an LLM, stores the detailed report on disk and a summary in the metadata store, and "
     "guarantees determinism. [Tested]")

section("6.3", "Module 3 \u2014 Semantic Knowledge")
para("The semantic module builds a versioned semantic context, detects ambiguities, computes a "
     "confidence value, raises clarification questions, records human decisions and enforces the "
     "non-finalisation guarantee for language-model proposals. [Tested]")

section("6.4", "Module 4 \u2014 Orchestrator")
para("The orchestrator sequences the pipeline stages, checkpoints state at the human breakpoint, routes "
     "only on real data, and writes every transition to the audit trail. [Tested]")

section("6.5", "Module 5 \u2014 Analysis")
para("The analysis module translates a business goal into schema-grounded SQL, executes it "
     "deterministically, and produces empirical conclusions and a decision matrix with provenance. A "
     "causal-analysis interface exists but its runtime dependency (DoWhy) is not bundled, so causal "
     "estimation was reported as not implemented in the validated environment. [Tested] for analytical "
     "SQL; [Planned] for causal analysis.")

section("6.6", "Module 6 \u2014 Modeling")
para("The modelling module runs the model tournament, computes real evaluation metrics, applies a "
     "Pareto selection criterion and supports out-of-time validation for temporal data. LightGBM is a "
     "declared candidate but was inactive in the validated run. [Partial]")

section("6.7", "Module 7 \u2014 Verification")
para("The verification module evaluates the eight mandatory gates, defaults to BLOCKED on any "
     "mandatory failure, produces the deployment readiness report, and provides explainability (SHAP) "
     "and conditional fairness checks. [Partial \u2014 gate engine implemented; some gates depend on "
     "suitable columns or optional packages being present.]")

section("6.8", "Module 8 \u2014 Healing")
para("The healing module applies deterministic corrections to a derived dataset, never mutating the "
     "original, and reports the before/after quality change for human accept/reject. [Tested]")

section("6.9", "Module 9 \u2014 Engineering")
para("The engineering module generates a self-contained FastAPI inference service with genuine model "
     "weights, Pydantic schemas, tests, a model card and a deployment README, and validates the artifact "
     "with a real inference before marking it PASS. [Tested]")

section("6.10", "Module 10 \u2014 Frontend and Visualization")
para("The front-end module provides the navigation workspace across all product domains and the "
     "18-chart SVG visualization suite, driven by real backend responses. [Implemented]")

# ================================================================== CHAPTER 7
chapter(7, "Implementation Results and Discussion")

section("7.1", "Test Environment and Methodology")
para("Verification combined automated backend tests, a front-end production build and a strict, "
     "zero-mock end-to-end audit on real data. The end-to-end audit ingested a real public retail "
     "benchmark (Superstore sales dataset.csv, 2,278,523 bytes, SHA-256 "
     "b548064635dc84b40a7286a0b53abd5013b95da6081036bcd2f7e8d65264b175) and re-derived key metrics "
     "independently with pure pandas and NumPy, without importing product code. Where a metric was "
     "recomputed independently it matched the system value exactly. The governing constraint "
     "throughout was the project\u2019s \u201cno mock data\u201d rule: fabricated metrics, fake API responses and "
     "synthetic generators are treated as defects.")
para("The recorded environment was a Windows 11 Enterprise workstation (build 10.0.26100) with Python "
     "3.10.7 (x64), Node.js 20+ with Vite, MongoDB Atlas (with local JSON fallback), DuckDB with PyArrow, "
     "and scikit-learn with NumPy and pandas. Optional LLM providers were Google Gemini and Groq.")

section("7.2", "Ingestion, Profiling and Data-Model Results")
para("The ingestion and profiling stages were covered by 42 automated tests at Phases 4\u20135 (all "
     "passing), which exercised every supported format, ZIP archives with mixed formats, invalid and "
     "over-deep archives, duplicate names, unsupported and binary-masquerade files, malformed inputs, "
     "unsafe SQL (with non-execution proof), sheet selection, headerless and BOM-prefixed CSV, the full "
     "contract, preview and profiling determinism. The suite found and fixed eight real defects rather "
     "than suppressing them. A subsequent full suite reported 54 tests passing with zero failures. In "
     "the end-to-end run, all 9,994 rows and 21 columns were ingested with zero row drops and zero column "
     "truncations, and an independent re-profile matched null counts for all 21 columns. [Tested]")
table("Table 7.1: Representative backend test results (as reported in the project sources).",
      ["Suite / stage", "Result"],
      [["Phases 4\u20135 (ingestion + profiling)", "42 passed, 0 failed (34.51 s)"],
       ["Phase 6 (full suite incl. semantic)", "54 passed, 0 failed"],
       ["Semantic tests", "12 scenarios, including scripted-LLM non-finalisation proof"],
       ["test_projects (E2E audit)", "1 passed (13.77 s)"],
       ["test_remediation (E2E audit)", "1 passed (17.87 s)"],
       ["Front-end production build", "Built in 32.00 s with 0 TypeScript and 0 Vite errors"]])
placeholder("Fig. 7.1: Dataset Explorer showing the deterministic profiling result and quality score "
            "(screenshot placeholder).", lines=5)

section("7.3", "Semantic Resolution and Human-in-the-Loop Results")
para("The semantic layer was validated with both unit tests and live smoke tests. On a dataset with a "
     "coded status column, the workflow correctly interrupted with a confidence of 0.65, created a "
     "value-mapping clarification question, then resumed at confidence 1.0 after the human supplied "
     "{\u201c4=cancelled;1=active;2=test order;3=fraud hold\u201d}, recording business meaning with source "
     "user_decision and emitting the expected audit sequence. In the end-to-end run, the layer grounded "
     "six metrics and fifteen dimensions plus ten terms directly to real columns, and a human breakpoint "
     "was entered and resolved by selecting Profit as the modelling target. [Tested]")
table("Table 7.2: Semantic and human-breakpoint evidence.",
      ["Observation", "Result"],
      [["Grounded metrics / dimensions / terms", "6 / 15 / 10 (all mapped to real columns)"],
       ["Human breakpoint decision", "Target = Profit; status = resolved"],
       ["Interrupt confidence (coded column)", "0.65, resolved to 1.0 after clarification"],
       ["LLM finalisation", "Not permitted; proposals remain needs_review"]])
placeholder("Fig. 7.2: Semantic Knowledge view with an open human clarification breakpoint "
            "(screenshot placeholder).", lines=5)

section("7.4", "Model Tournament Results")
para("In the end-to-end run the tournament trained on 7,995 rows and evaluated on 1,999 rows (an 80/20 "
     "split of the real data). Two candidate learners were available once LightGBM was skipped, and "
     "Linear Regression was selected as the champion under the Pareto criterion, achieving a root mean "
     "squared error of 287.93 and a mean absolute error of 71.88 with an inference latency of "
     "approximately 0.003 ms on the numeric Profit target. These regression metrics are the real, "
     "independently re-derived figures for that run; the platform also computes classification metrics "
     "(accuracy, precision, recall, F1 and ROC-AUC) when the target is categorical, but the validated "
     "end-to-end target was numeric, so no classification accuracy figures are claimed here. [Partial]")
table("Table 7.3: End-to-end champion model (real, independently re-derived).",
      ["Metric", "System value", "Independent value", "Result"],
      [["Champion model", "Linear Regression", "\u2014", "Selected via Pareto frontier"],
       ["Training / test rows", "7,995 / 1,999", "7,995 / 1,999", "PASS"],
       ["RMSE (Profit)", "287.93", "287.93", "PASS (1e-4)"],
       ["MAE (Profit)", "71.88", "71.88", "PASS (1e-4)"],
       ["Inference latency", "\u2248 0.003 ms", "\u2014", "Recorded"]])
placeholder("Fig. 7.3: Model Tournament view with candidate metrics and the selected champion "
            "(screenshot placeholder).", lines=5)

section("7.5", "Verification Gates and Healing Results")
para("The verification engine evaluated the dataset and model as READY, and a deliberately forced "
     "failure correctly produced BLOCKED, demonstrating that the gate logic genuinely blocks deployment. "
     "The healing engine produced a derived dataset while the original remained byte-identical "
     "(verified by hash), with a before/after quality report computed from real missing-cell counts "
     "rather than hard-coded values. Deployment artifacts were packaged with genuine model weights and "
     "live inference was executed on held-out transactions, returning predictions [117.37, 227.16, "
     "20.74]. The run recorded 20 real audit events. [Tested] for the exercised gates and healing; "
     "[Partial] overall because the causal gate was not active.")
placeholder("Fig. 7.4: Verification Center showing the eight gates and deployment readiness "
            "(screenshot placeholder).", lines=5)

section("7.6", "End-to-End Real-Data Validation")
para("The master end-to-end audit reached an overall verdict of PASS on real data with zero mocks. All "
     "applicable stages completed: multi-format ingestion, DuckDB Parquet registration, deterministic "
     "profiling, semantic grounding, human breakpoint resolution, analytical SQL KPI generation, "
     "scikit-learn model tournament, verification gating, autonomous healing, deployment artifact "
     "generation and real-time inference. The dataset scored 85.0/100 (grade B), the analytical SQL "
     "computed 2,297,200.86 in total sales, 286,397.02 in total profit and 37,873 units, and every "
     "independently re-derived metric matched exactly. Re-running profiling reproduced identical scores, "
     "confirming determinism. [Tested]")
table("Table 7.4: End-to-end (Track A) stage outcomes for the audited run.",
      ["Stage", "Outcome"],
      [["Dataset selection & ingestion", "2.28 MB CSV; 9,994 rows \u00d7 21 columns; SHA-256 matched"],
       ["Integrity verification", "9,994 rows ingested exactly; zero drops or truncations"],
       ["Profiling & independent recomputation", "21/21 columns matched; score 85.0/100 (grade B)"],
       ["Semantic grounding & human breakpoint", "6 metrics, 15 dimensions, 10 terms; target = Profit"],
       ["Analysis KPIs", "Sales 2,297,200.86; Profit 286,397.02; Quantity 37,873; diff 0.00"],
       ["Temporal leakage check", "Order Date / Ship Date verified non-leaky"],
       ["Model tournament", "Champion Linear Regression; RMSE 287.93; MAE 71.88"],
       ["Verification gates", "READY (and BLOCKED when forced)"],
       ["Autonomous healing", "Original byte-identical; nulls healed in derived dataset"],
       ["Artifacts & live inference", "Predictions [117.37, 227.16, 20.74]"],
       ["Audit trail", "20 events recorded"],
       ["Reproducibility", "Run 1 = Run 2 = 85.0"]])
placeholder("Fig. 7.5: End-to-end audit trail of the validated run (screenshot placeholder).", lines=5)

section("7.7", "Performance Metrics and Comparison")
para("Because MK-PATH is an integrated platform rather than a single algorithm, a direct numerical "
     "comparison against a single baseline would be misleading. Table 7.5 therefore compares the "
     "platform\u2019s design properties against the methodology families identified in Chapter 3, using "
     "only properties that the project sources support.")
table("Table 7.5: Qualitative comparison of MK-PATH against common methodology families.",
      ["Property", "Manual scripts", "Standalone AutoML", "Unguarded LLM analytics", "MK-PATH"],
      [["Deterministic, reproducible metrics", "No", "Partial", "No", "Yes (zero-LLM profiling)"],
       ["Schema-grounded query generation", "No", "N/A", "Rarely", "Yes"],
       ["Human-confirmed business meaning", "Ad hoc", "No", "No", "Yes (breakpoint)"],
       ["Mandatory verification gates", "No", "No", "No", "Yes (8 gates)"],
       ["Deployment block on failure", "No", "No", "No", "Yes"],
       ["Original data preserved", "Rarely", "N/A", "N/A", "Yes (immutable original)"],
       ["End-to-end audit trail", "Rarely", "Partial", "No", "Yes"]])
para("The storage audit further showed that the entire platform, including its virtual environment, "
     "occupies under 1 GB, with zero leakage of user data to the operating-system drive, and no hidden "
     "large-model caches. [Tested]")

section("7.8", "Verification Timeline and Remediation History")
para("The project\u2019s verification record is instructive because it preserves both a failure and its "
     "correction. An early Phase 1\u20136 verification returned NOT READY FOR PHASE 7 because the front end "
     "did not yet exist; a later real-time functional verification then returned FAIL / NOT READY because "
     "the front end and several back-end paths still relied on fabricated state, hard-coded metrics and "
     "mock handoffs. A remediation effort removed every such path \u2014 replacing fabricated project "
     "endpoints, hard-coded semantic concepts, mocked orchestrator state, synthetic tournament targets, "
     "fake model binaries and hard-coded healing scores with real database, DuckDB, scikit-learn and "
     "FastAPI behaviour \u2014 after which the master real-data end-to-end audit returned PASS. This report "
     "treats the final PASS as the current status and records the earlier verdicts as history, because "
     "transparency about the remediation is itself evidence of the platform\u2019s commitment to the "
     "no-mock rule.")
table("Table 7.6: Verification timeline.",
      ["Report", "Verdict", "Notes"],
      [["Phase 1\u20136 verification", "NOT READY (Phase 1 FAIL)", "Back end robust and tested; front end absent."],
       ["Real-time functional verification", "FAIL / NOT READY", "Mock state and hard-coded metrics found across the stack."],
       ["Remediation report", "PASS", "All mocked/disconnected paths converted to real behaviour."],
       ["Master real-data E2E (v2)", "PASS", "9,994-row real dataset, zero mocks, metrics independently re-derived."]])

section("7.9", "Consolidated Implementation-Status Matrix")
table("Table 7.7: Consolidated capability status (see the Table 1.1 convention).",
      ["Capability", "Status", "Evidence / note"],
      [["Multi-format ingestion & ZIP security", "[Tested]", "42 tests; traversal- and bomb-safe."],
       ["DuckDB normalized views", "[Tested]", "ds_<dataset_id> over Parquet."],
       ["Deterministic profiling (25 metrics)", "[Tested]", "Byte-identical re-runs; 85.0/100 on E2E data."],
       ["Semantic knowledge layer (13 concept types)", "[Tested]", "Non-finalisation proof; live smoke test."],
       ["Human-in-the-loop breakpoint", "[Tested]", "Interrupt at 0.65; resolve to 1.0."],
       ["LangGraph orchestrator", "[Tested]", "14-stage graph; audit-integrated."],
       ["Data Analyst agent & KPIs", "[Tested]", "Exact match to independent Pandas recomputation."],
       ["Decision matrix & conclusions", "[Implemented]", "Generated in smoke/user verification."],
       ["Model tournament (scikit-learn)", "[Tested]", "Champion Linear Regression; RMSE 287.93."],
       ["LightGBM candidate", "[Partial]", "Skipped: native runtime library unavailable."],
       ["Out-of-time validation", "[Implemented]", "Available for temporal datasets; not exercised in E2E."],
       ["Explainability gate (SHAP)", "[Implemented]", "Global and local attributions implemented."],
       ["Fairness gate", "[Implemented]", "TPR/FPR/selection rate when group attributes exist."],
       ["Causal analysis (DoWhy)", "[Planned]", "Package not bundled; NOT_IMPLEMENTED in E2E."],
       ["Healing (immutable original)", "[Tested]", "Original byte-identical; before/after report."],
       ["ML artifacts & live inference", "[Tested]", "Real weights; predictions [117.37, 227.16, 20.74]."],
       ["Audit trail", "[Tested]", "20 events in E2E; secrets filtered."],
       ["18-chart visualization suite", "[Implemented]", "Pure SVG; clean build."],
       ["Authentication / authorization", "[Planned]", "Not enforced on endpoints in the prototype."],
       ["Hyper-parameter tuning (Optuna)", "[Planned]", "scikit-learn defaults used in the prototype."],
       ["Cross-platform storage paths", "[Planned]", "Windows-oriented paths in the prototype."]])

section("7.10", "Discussion and Limitations")
para("The results support the central architectural claim: a deterministic core with an evidence gate "
     "can carry real, messy data end-to-end and produce reproducible results, while keeping a language "
     "model strictly advisory. The end-to-end audit\u2019s exact agreement with independent recomputation "
     "is the strongest available evidence that the reported numbers are real.")
para("Several limitations are recorded honestly and are carried forward rather than hidden:")
bullet("Authentication and authorisation are not enforced on the prototype endpoints; user scoping is a "
       "future concern.")
bullet("Causal analysis (DoWhy) is specified but not bundled, so causal estimation was not active in the "
       "validated runtime.")
bullet("LightGBM is a declared candidate but was inactive because its native runtime library was "
       "missing.")
bullet("Hyper-parameter tuning used scikit-learn defaults rather than a full optimisation budget.")
bullet("Some storage paths and commands in the documentation are Windows-oriented (for example, drive-"
       "letter roots and PowerShell-style invocations).")
bullet("The upload-size limit appears as 500 MB in the current configuration while an earlier ingestion "
       "document recorded a 50 MB default, a documentation drift worth reconciling.")
bullet("Fairness and explainability gates depend on suitable columns or optional packages being present; "
       "their conditional nature means they are not exercised on every dataset.")
para("None of these limitations affect the validity of the deterministic results reported above; they "
     "define the boundary between what the prototype proves and what remains to be built.")

# ================================================================== CHAPTER 8
chapter(8, "Conclusion and Future Works")

section("8.1", "Conclusion")
para("This report has described MK-PATH, a multi-agent, evidence-gated platform for autonomous data "
     "transformation and healing, and has evaluated it against its own recorded evidence. The platform "
     "ingests heterogeneous data through a hardened pipeline, normalises it into an embedded analytical "
     "engine, profiles it deterministically with a reproducible quality score, grounds its columns in a "
     "semantic layer whose meaning is confirmed by recorded human decisions, plans and executes "
     "schema-grounded analytics, runs a multi-objective model tournament, enforces mandatory verification "
     "gates that can block deployment, heals data quality without mutating the original, and generates a "
     "self-validating deployable inference service \u2014 all recorded in an append-only audit trail.")
para("The end-to-end real-data validation returned an overall verdict of PASS on a 9,994-row benchmark "
     "dataset with zero mock data. Crucially, every reported metric was independently re-derived and "
     "matched exactly: the profiling score of 85.0/100, the analytical totals, and the champion "
     "model\u2019s RMSE of 287.93 and MAE of 71.88. The project\u2019s verification history \u2014 an initial NOT "
     "READY verdict, a subsequent FAIL audit that found mock state, a thorough remediation and a final "
     "PASS \u2014 demonstrates a working commitment to the no-mock principle that is unusual and valuable in "
     "itself. The principal contribution of MK-PATH is therefore architectural: it shows that "
     "deterministic computation, human-confirmed semantics and hard verification gates can be composed "
     "into a trustworthy data-to-deployment workflow.")

section("8.2", "Future Work")
para("The platform\u2019s own reports identify a clear set of next steps, which this report adopts as the "
     "future-work agenda:")
bullet("Bundle causal-inference dependencies (DoWhy and causal-learn) and integrate observational "
       "causal estimation into the verification pipeline.")
bullet("Provide LightGBM and other gradient-boosted learners with their native runtime libraries, and "
       "add further candidates such as XGBoost.")
bullet("Introduce full hyper-parameter optimisation (for example Optuna) under a bounded search budget.")
bullet("Implement authentication and authorisation with per-user data scoping across all endpoints.")
bullet("Remove legacy cosmetic UI timeouts in the semantic breakpoint component in favour of pure state "
       "props.")
bullet("Add native database connectors (for example PostgreSQL or Snowflake) so that ingestion is not "
       "limited to file and archive uploads.")
bullet("Extend the generated artifact service with live monitoring hooks to detect inference drift.")
bullet("Generalise storage paths and commands so the platform is not tied to a Windows drive-letter "
       "layout.")
bullet("Reconcile minor documentation drift (for example the upload-size default) and keep the phase "
       "documentation consolidated under a single numbering scheme.")
para("Taken together, these steps move MK-PATH from a verified prototype toward a production-grade, "
     "cross-platform evidence-gated data platform without compromising the deterministic and "
     "human-accountable principles that define it.")

doc.save(OUT)
print("saved", OUT)
