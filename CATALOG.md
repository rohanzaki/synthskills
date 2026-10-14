# SynthSkills catalog

247 public skills in 20 areas, 202 rated so far. Generated 2026-10-14 by `scripts/build_catalog.py` from `data/skills.json`.

This file lists names, one-line summaries and scores only. The skills themselves are not in this repository: an agent reads them over MCP at `https://synthskills.synthminds.pk/mcp` under the SynthSkills charter and [terms](https://synthskills.synthminds.pk/terms). The live list, with sorting and area filters, is at [https://synthskills.synthminds.pk/skills](https://synthskills.synthminds.pk/skills). Address a skill as `skill://name`.

## How scores are made

Each public skill was read in full by an AI reviewer (Claude Opus 5.5) and scored 1-10 on three axes against a fixed rubric with calibration anchors (median around 6-7; 9+ is rare). Scores are a reviewer's judgement, not a guarantee; they are refreshed when skills change.

- **Quality**: Correctness and craft: right and current commands, numbers and standards; clear, no filler.
- **Depth**: Professional detail: real parameters, thresholds, standards, failure modes and a real-order workflow.
- **Practical**: Real-life use by an AI agent: can it be applied end to end and checked, with tools an agent can drive.
- **Overall**: the mean of the three scores, to one decimal.

"not yet rated" means the skill is published but its review is not finished.

## Areas

- [3D & Blender](#3d--blender): 16
- [AI & LLM Engineering](#ai--llm-engineering): 14
- [Audio & Music](#audio--music): 4
- [Business & Operations](#business--operations): 3
- [Colour & Image](#colour--image): 6
- [Data & GIS](#data--gis): 4
- [Design & UI](#design--ui): 11
- [Film & Video](#film--video): 34
- [Finance & Accounting](#finance--accounting): 13
- [Legal, Compliance & Risk](#legal-compliance--risk): 3
- [Manufacturing & Industry](#manufacturing--industry): 8
- [Marketing & Growth](#marketing--growth): 43
- [Other](#other): 45
- [Productivity & Agents](#productivity--agents): 7
- [Publishing & Print](#publishing--print): 5
- [Religion & Scripture](#religion--scripture): 2
- [Research & Archives](#research--archives): 4
- [Sales & CRM](#sales--crm): 6
- [Software & DevOps](#software--devops): 10
- [Writing & Story](#writing--story): 9

## 3D & Blender

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://gltf-web-export-pipeline` | Exports Blender models to validated GLB for the web with baked materials, texture budgets and compression. | 7 | 8 | 8 | 7.7 |
| `skill://headless-blender-batch-render` | Command-line Blender renders per shot or camera with device choice, resumable frames, manifests and previews | 8 | 7 | 8 | 7.7 |
| `skill://blender-mcp-live-session-control` | Drives a running Blender over an MCP bridge: inspect first, small reversible changes, screenshot checks. | 7 | 7 | 8 | 7.3 |
| `skill://bpy-scene-scripting-basics` | Builds a reproducible Blender scene by script: units, collections, named shader sockets, aimed camera, lights | 8 | 6 | 8 | 7.3 |
| `skill://mesh-cleanup-meshlab-instant-meshes` | Repairs and simplifies scan or generated meshes with PyMeshLab filters and retopologises with Instant Meshes. | 8 | 7 | 7 | 7.3 |
| `skill://bird-feathers-wings-rig` | Builds feather cards, a driver-based folding wing rig, tail fan, crest and GN plumage in Blender. | 6 | 9 | 5 | 6.7 |
| `skill://bird-flight-animation` | Keys bird wingbeats, bounding flight, loops and motion blur in Blender with sourced rates and numeric QA | 7 | 8 | 5 | 6.7 |
| `skill://creature-modeling-from-orthos` | Models a rig-ready creature in Blender from orthographic sheets with ring lofting and silhouette gates | 6 | 9 | 5 | 6.7 |
| `skill://archviz-interior-render` | Renders plan-accurate interiors in Cycles with lens-shift cameras, window portals and fixture-based lights. | 7 | 6 | 6 | 6.3 |
| `skill://cg-product-packshot` | Builds faithful CG product renders: measured geometry, label accuracy, neutral colour proof, variant manifest. | 7 | 6 | 6 | 6.3 |
| `skill://gis-terrain-blender` | Builds real-world terrain in Blender from elevation and satellite tiles, with optional OpenStreetMap buildings | 6 | 8 | 5 | 6.3 |
| `skill://low-poly-game-asset-pipeline` | Takes high-poly or scanned models to game-ready assets: budgets, retopo, UVs, bakes, LODs, collision. | 7 | 7 | 5 | 6.3 |
| `skill://quick-creature-rig` | Fast hand-built armature for creatures in Blender: roll, symmetrize, auto weights, leg IK and control shapes | 6 | 8 | 5 | 6.3 |
| `skill://real-time-unreal-movie-render-queue` | Renders Sequencer shots via Unreal Movie Render Queue: sampling, warm-up, EXR passes, OCIO, scale. | 7 | 7 | 5 | 6.3 |
| `skill://model-anything-from-reference` | Six-stage method for modelling real objects in Blender from multi-view references, with bpy notes. | 6 | 6 | 6 | 6.0 |
| `skill://subd-hard-surface-modeling` | Quad-first subdivision modelling of hard-surface props in Blender, with Boolean clean-up and bmesh equivalents | 6 | 5 | 6 | 5.7 |

## AI & LLM Engineering

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://agent-tool-use-loop-and-retries` | Designs tool-calling agent loops: caps, error classes, jittered backoff, idempotency, loop detection. | 8 | 8 | 8 | 8.0 |
| `skill://llm-as-judge-bias-controls` | Builds rubric-anchored LLM judges with position, length and self-preference controls and human calibration. | 8 | 8 | 8 | 8.0 |
| `skill://llm-cost-and-latency-budgeting` | Model LLM cost per task and latency, then apply caching, batching, routing, output caps and spend alerts | 8 | 8 | 8 | 8.0 |
| `skill://llm-document-extraction-pipeline` | Builds a validated LLM document-extraction pipeline with grounding, review routing and labelled accuracy. | 8 | 8 | 8 | 8.0 |
| `skill://llm-eval-golden-set-design` | Designs a stratified, double-labelled, versioned golden test set for an LLM feature with a held-out split. | 8 | 8 | 8 | 8.0 |
| `skill://llm-structured-output-validation` | Get schema-valid model output: constrained modes, Pydantic/Zod validation, bounded repair, untrusted handling | 8 | 8 | 8 | 8.0 |
| `skill://mcp-server-design-and-testing` | Designs, builds and tests an MCP server: tool set, transport, annotations, Inspector, contract tests. | 8 | 8 | 8 | 8.0 |
| `skill://mcp-tool-schema-and-error-design` | Design MCP tool names, descriptions, schemas, pagination and isError results so models pick and recover well | 8 | 8 | 8 | 8.0 |
| `skill://multilingual-chatbot-urdu-arabic` | Makes an assistant handle Urdu, Roman Urdu, Arabic and mixed input with normalisation and native-graded tests. | 8 | 8 | 8 | 8.0 |
| `skill://rag-retrieval-evaluation` | Evaluates RAG with labelled passages, recall@k/MRR, faithfulness, failure attribution and paired comparisons. | 8 | 8 | 8 | 8.0 |
| `skill://kb-llm-eval-metrics` | Reference of eval metrics for classifiers, retrieval, RAG and agents with formulas and worked numbers | 8 | 8 | 7 | 7.7 |
| `skill://prompt-injection-defence` | Defensive design for LLM apps and agents: trust map, privilege split, output gating, injection tests | 8 | 8 | 7 | 7.7 |
| `skill://rag-pipeline-design` | End-to-end RAG design: fit check, metadata ingest, chunking, hybrid search, rerank, ACLs, abstention | 8 | 8 | 7 | 7.7 |
| `skill://system-prompt-engineering` | Writes, tests and versions production system prompts: criteria first, reasoned rules, fenced data | 8 | 7 | 8 | 7.7 |

## Audio & Music

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://loudness-and-ducking` | Mixes narration over music with ffmpeg sidechain ducking, two-pass loudnorm and measured delivery QC. | 8 | 9 | 9 | 8.7 |
| `skill://music-notation-musescore-lilypond-music21` | Convert and engrave MusicXML/MIDI with MuseScore, LilyPond, music21 and mido, guarding pitch and timing | 7 | 7 | 7 | 7.0 |
| `skill://open-music-generation-ace-step-yue` | Generate temp music with open models while recording checkpoint, seed and exact code and weight licences | 7 | 7 | 6 | 6.7 |
| `skill://podcast-hosting-castopod-and-directories` | Publishes a podcast via Castopod or hosted platforms, submits to directories and migrates feeds safely. | 7 | 7 | 6 | 6.7 |

## Business & Operations

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://business-workflow-automation-design` | Designs low-code automations with data contracts, dedup keys, bounded retries, alerts, run logs and ownership. | 8 | 7 | 7 | 7.3 |
| `skill://sap-business-one-sales-purchasing-and-mrp` | Diagnoses SAP B1 document chains, units and MRP runs and builds paged, read-first Service Layer integrations. | 7 | 8 | 7 | 7.3 |
| `skill://shared-spreadsheet-tracker-design` | Designs multi-editor team trackers: stable ids, validated lists, status rules, protection, backups | 7 | 6 | 6 | 6.3 |

## Colour & Image

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://background-removal-birefnet-rembg` | Batch cut-outs with rembg and BiRefNet models, alpha review on light/dark grounds and a per-image manifest. | 8 | 7 | 8 | 7.7 |
| `skill://image-conversion-oiiotool` | Inspects and converts EXR and image sequences with OpenImageIO: channels, colour, codecs, textures. | 8 | 7 | 8 | 7.7 |
| `skill://qwen-image-text-rendering-and-edit` | Generates text-bearing images and masked edits with Qwen-Image models via diffusers or ComfyUI, with glyph QA. | 8 | 7 | 7 | 7.3 |
| `skill://kb-color-spaces-and-transfer-functions` | Reference for primaries, transfer functions, matrices and range tags; diagnoses washed-out exports. | 8 | 7 | 6 | 7.0 |
| `skill://aces-ocio-colour-pipeline` | Sets up a colour-managed ACES/OCIO pipeline across footage, CG, comp and grade, with a chart round-trip check. | 7 | 7 | 6 | 6.7 |
| `skill://image` | Picks AI generation, design tools or screenshots for marketing images, with sizes, OG tags and compression. | 7 | 6 | 7 | 6.7 |

## Data & GIS

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://forecasting-libraries-prophet-timesfm` | Business forecasts with Prophet, statsforecast and TimesFM, using baselines, backtests and interval checks. | 7 | 8 | 8 | 7.7 |
| `skill://gis-data-qgis-and-gdal` | Prepares geodata with GDAL, QGIS and OSMnx: CRS choice, reprojection, DEM clips, vectors, layouts. | 8 | 7 | 7 | 7.3 |
| `skill://excel-power-query-pivots-and-dynamic-arrays` | Turns messy exports into refreshable Excel workbooks with Power Query, pivots, XLOOKUP and checks. | 8 | 7 | 5 | 6.7 |
| `skill://field-surveys-kobotoolbox-odk` | Designs XLSForm surveys for offline phone collection in Kobo or ODK: logic, repeats, GPS, exports. | 7 | 7 | 6 | 6.7 |

## Design & UI

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://mockup-to-code` | Implements a page from a mockup by rendering both, measuring layout in the browser and wiring every control. | 6 | 8 | 7 | 7.0 |
| `skill://redesign-existing-projects` | Audits an existing web UI for generic patterns and applies targeted type, colour, layout, state fixes. | 6 | 6 | 7 | 6.3 |
| `skill://high-end-visual-design` | Opinionated Tailwind design rules for premium-looking web UIs: archetypes, nested cards, motion and bans. | 5 | 6 | 7 | 6.0 |
| `skill://minimalist-ui` | Style rules for warm monochrome editorial web UI: fonts, hex palette, bento cards, buttons and subtle motion | 6 | 5 | 7 | 6.0 |
| `skill://design-taste-frontend-v1` | Opinionated rules for generating React/Tailwind UIs that avoid generic AI-looking layouts and motion. | 5 | 6 | 6 | 5.7 |
| `skill://stitch-design-taste` | Generates a DESIGN.md of opinionated tokens, type, layout, motion and bans for a UI-generation tool. | 5 | 5 | 6 | 5.3 |
| `skill://imagegen-frontend-web` | Art-direction rules for generating one website-section design image per section, varied yet consistent. | 5 | 5 | 5 | 5.0 |
| `skill://brandkit` | Art-directs a single generated image showing a brand identity board: logo concept, palette, type and mockups. | 5 | 4 | 5 | 4.7 |
| `skill://image-to-code` | Generate section mock images first, analyse them, then build a web page that matches them | 5 | 4 | 5 | 4.7 |
| `skill://gpt-taste` | Prescriptive rules for generating motion-heavy landing pages with GSAP, bento grids and wide hero typography. | 4 | 4 | 5 | 4.3 |
| `skill://imagegen-frontend-mobile` | Art-direction rules for generating consistent, readable mobile app screen images inside phone mockups. | 4 | 4 | 5 | 4.3 |

## Film & Video

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://ffmpeg-video` | FFmpeg recipes for conversion, 9:16 reframes, subtitle burn-in, compression, loudness and platform exports. | 7 | 8 | 9 | 8.0 |
| `skill://subtitle-tools-subtitle-edit-ffsubsync-pysubs2` | Converts, syncs and checks subtitle files with ffsubsync, pysubs2 QC code and Subtitle Edit batch fixes. | 8 | 8 | 8 | 8.0 |
| `skill://technical-metadata-mediainfo-ffprobe` | Inspects media with MediaInfo and ffprobe: streams, rational rates, VFR, colour tags, timecode, audio. | 8 | 8 | 8 | 8.0 |
| `skill://perceptual-quality-vmaf` | Score encodes against a reference with FFmpeg libvmaf, report lower-tail percentiles and pick bitrates | 7 | 8 | 8 | 7.7 |
| `skill://remotion-lower-third-system` | Data-driven Remotion lower thirds with validated rows, text fitting, RTL variants and ProRes alpha renders. | 7 | 8 | 8 | 7.7 |
| `skill://scripted-edits-kdenlive-mlt` | Assembles rough cuts by code with melt and MLT XML and hands editors a native Kdenlive project. | 8 | 8 | 7 | 7.7 |
| `skill://storyboard-previs` | Boards and timed grey-box previs with real narration, Blender cameras and ffmpeg animatics. | 8 | 8 | 7 | 7.7 |
| `skill://timeline-interchange-opentimelineio` | Moves edits between tools with OpenTimelineIO adapters, rational-time maths, pull lists and conform checks. | 8 | 8 | 7 | 7.7 |
| `skill://dub-fit-locked-picture` | Fits a translated dub to a locked cut line by line with a bounded timing ladder, wording ledger and mix QC. | 7 | 8 | 7 | 7.3 |
| `skill://exr-multilayer-and-aov-conventions` | Sets render-pass contracts for multilayer EXR: naming, precision, compression, Cryptomatte, beauty rebuild | 8 | 7 | 7 | 7.3 |
| `skill://greenscreen-keying-headless` | Pulls green/blue-screen keys with core/edge mattes, despill, AI assistance and headless batch QC | 8 | 7 | 7 | 7.3 |
| `skill://interview-transcripts-for-editorial` | Produces corrected, speaker-labelled interview transcripts mapped to source timecode, translation kept apart. | 7 | 7 | 8 | 7.3 |
| `skill://kb-subtitle-formats-and-style-rules` | Reference for choosing subtitle formats and applying sourced timing, line-length and reading-speed rules. | 7 | 8 | 7 | 7.3 |
| `skill://video-production-quote` | Prices video and ad jobs from written assumptions, phases, day rates, render time, licences and terms. | 8 | 7 | 7 | 7.3 |
| `skill://live-production-obs-websocket` | Run OBS streams and recordings with profiles, audio chain, MKV remux and authenticated obs-websocket v5 cues | 8 | 7 | 6 | 7.0 |
| `skill://music-cue-sheet` | Builds a royalty cue sheet from a locked programme: cue uses, usage types, writers, publishers, timings. | 8 | 7 | 6 | 7.0 |
| `skill://production-tracking-kitsu` | Tracks shots, assets, tasks, previews and reviews in Kitsu, with gazu API reads, publishes and weekly reports. | 7 | 7 | 7 | 7.0 |
| `skill://short-ad-preproduction-path` | Gated pre-production for 15-30 s ads: brief, treatment, timed script, animatic, shot list, sign-offs. | 8 | 7 | 6 | 7.0 |
| `skill://vfx-breakdown-sheet-and-reel` | Builds a VFX shot breakdown sheet and an honest plate-to-final reel with scoped public-use approvals. | 8 | 7 | 6 | 7.0 |
| `skill://build-material-worlds` | Writes a design brief tying sets, costume and props to character profiles and story progression. | 7 | 7 | 6 | 6.7 |
| `skill://mood-board-and-reference-deck` | Builds an annotated look deck with sectioned references, extracted hex palette, a 'not this' list and credits. | 7 | 7 | 6 | 6.7 |
| `skill://film-reviewer-panel` | Runs a multi-seat audience review of a cut and merges timed notes into a ranked fix list with blockers. | 6 | 7 | 6 | 6.3 |
| `skill://stage-action-and-performance` | Turns scene beats into a blocking plan: marks, numbered moves, props, eyelines, 24 fps key poses | 7 | 7 | 5 | 6.3 |
| `skill://title-sequence-design` | Designs openings, cards, lower-thirds and credits with legibility sizes, sound timing and a text cap | 7 | 7 | 5 | 6.3 |
| `skill://cinematographer-dp` | Sets the DP's shot design: lens, height, movement, motivated key light and exposure on a per-sequence sheet | 6 | 7 | 5 | 6.0 |
| `skill://documentary-story-structure` | Story-editor method for essay documentaries: spine, chapter turns, on-screen counts, clarity pass. | 6 | 7 | 5 | 6.0 |
| `skill://film-director` | Directs a film sequence by sequence: dramatic question, turns, event-on-word staging, notes and a review pass | 6 | 7 | 5 | 6.0 |
| `skill://film-editor` | Editor role for cutting scenes from shots: cut order, holds, transitions, repeat rule and pacing maps. | 5 | 8 | 4 | 5.7 |
| `skill://living-image-treatment` | Makes still-based shots feel alive with 2.5D depth layers, multiplane Blender setups and local video models. | 5 | 8 | 4 | 5.7 |
| `skill://motion-design-critique` | Diagnoses motion-design problems in After Effects and Blender: timing checks, script and render errors. | 5 | 6 | 6 | 5.7 |
| `skill://production-designer` | Production designer role for one coherent film world: sourced research, palette bible, motifs, still rules. | 5 | 7 | 5 | 5.7 |
| `skill://script-supervisor-continuity` | Continuity bible, per-shot sheets and an edit-data check for repeats, place, light and on-screen facts | 5 | 8 | 4 | 5.7 |
| `skill://vfx-supervisor` | Chooses a production method per shot, bids effort and risk, writes look targets and runs four approval gates | 5 | 8 | 4 | 5.7 |
| `skill://video` | Chooses between programmatic video, AI generation, avatars and repurposing tools for marketing video. | 5 | 5 | 6 | 5.3 |

## Finance & Accounting

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://quickbooks-online-bookkeeping-workflows` | Runs QuickBooks Online month-end: feeds, bank rules, matching, reconciliation, closing date and API reads. | 8 | 8 | 7 | 7.7 |
| `skill://bank-reconciliation-routine` | Reconciles bank, card and wallet accounts to the ledger with a zero-difference proof and stale-item policy | 8 | 7 | 7 | 7.3 |
| `skill://payroll-run-checks` | Pre-approval payroll checks: headcount roll, pay variance, deduction re-checks, ghosts, bank and journal ties | 8 | 7 | 7 | 7.3 |
| `skill://thirteen-week-cash-flow-forecast` | Direct-method 13-week rolling cash forecast with buffer, scenarios and weekly line-level variance | 8 | 7 | 7 | 7.3 |
| `skill://three-way-match` | Matches supplier invoices to POs and receipts with tolerances, partial deliveries and owned exceptions. | 7 | 8 | 7 | 7.3 |
| `skill://collections-dunning-cadence` | Staged B2B payment-reminder sequence with call script, promise log, dispute split and DSO/CEI. | 8 | 7 | 6 | 7.0 |
| `skill://receivables-and-collections-desk` | AR desk playbook: fast invoicing, daily cash application, disputes, escalation and weekly DSO reporting. | 8 | 7 | 6 | 7.0 |
| `skill://spreadsheet-modelling-standards` | Standards for auditable spreadsheet models: inputs-calcs-outputs, row consistency, checks, logs. | 8 | 7 | 6 | 7.0 |
| `skill://tallyprime-vouchers-ledgers-and-reports` | Keeps TallyPrime books consistent: masters, vouchers, bill-wise outstanding, alternate units, exports. | 7 | 8 | 6 | 7.0 |
| `skill://month-end-close-checklist` | Run a working-day close calendar: cut-off, accruals, reconciliations, flux review, report pack and lock | 7 | 7 | 6 | 6.7 |
| `skill://accounts-payable-desk-playbook` | Runs an AP desk: invoice intake, duplicate checks, coding, approvals, weekly payment runs and statement recs | 7 | 6 | 6 | 6.3 |
| `skill://bookkeeping-practice-playbook` | Daily, weekly and monthly bookkeeping routine with month-end pack, period lock and backlog catch-up method. | 7 | 7 | 5 | 6.3 |
| `skill://payroll-desk-playbook` | Runs the payroll cycle: calendar, signed changes, independent approval, bank-file and journal checks. | 7 | 7 | 5 | 6.3 |

## Legal, Compliance & Risk

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://sanctions-screening-opensanctions` | Sanctions and PEP screening via OpenSanctions API or yente, with tuned thresholds and logged decisions | 8 | 7 | 7 | 7.3 |
| `skill://bidding-expert` | Reads Pakistani public tenders under PPRA rules, extracts cited requirements and gives a go/no-go. | 7 | 8 | 6 | 7.0 |
| `skill://ai-acceptable-use-policy` | Drafts and rolls out a small-business staff AI-use policy with data classes, tool register and sign-offs | 7 | 6 | 6 | 6.3 |

## Manufacturing & Industry

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://cable-costing-per-km` | Builds a dated, re-runnable cost-per-km sheet for a cable from metal, compound, process and packing. | 8 | 8 | 7 | 7.7 |
| `skill://copper-yield-scrap-tracking` | Metal and compound balance for cable plants: scrap tagging, resistance-based giveaway, loss Pareto. | 8 | 8 | 7 | 7.7 |
| `skill://cable-production-sequencing` | Orders cable extrusion runs by compound, colour and tooling to cut changeovers, with SMED tracking. | 8 | 7 | 7 | 7.3 |
| `skill://shop-floor-telemetry-node-red-stack` | Read-only machine monitoring with MQTT, Node-RED, InfluxDB and Grafana, with stale-data alerting. | 7 | 8 | 7 | 7.3 |
| `skill://cable-type-test-file` | Keeps a register of cable type-test reports: size coverage, tender expiry and re-assessment after changes | 8 | 7 | 6 | 7.0 |
| `skill://odoo-manufacturing-boms-and-quality` | Configure Odoo MRP for cable output: metre units, per-km BoMs, work centres, lot/serial tracing and QC points | 7 | 8 | 6 | 7.0 |
| `skill://cable-production-planning-desk` | Runs a cable plant's monthly capacity plan and weekly schedules with bottleneck loading and promise dates. | 7 | 7 | 6 | 6.7 |
| `skill://cable-drum-labelling-traceability` | Designs cable drum labels, numbering and a lot ledger so each drum traces to materials and to customers | 7 | 7 | 5 | 6.3 |

## Marketing & Growth

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://attribution` | Chooses attribution models, reconciles conflicting channel numbers and builds first-party identity stitching | 8 | 8 | 7 | 7.7 |
| `skill://ads` | Paid-media strategy and operations on Google, Meta and LinkedIn with playbooks for audits, kill rules and RSAs | 6 | 8 | 7 | 7.0 |
| `skill://aso` | Audits App Store and Google Play listings with weighted scoring, tier adjustments and a prioritised fix plan. | 7 | 7 | 7 | 7.0 |
| `skill://seo-audit` | Audits crawlability, indexation, Core Web Vitals, on-page, international setup and content quality. | 7 | 7 | 7 | 7.0 |
| `skill://sideproject` | Builds a paste-ready marketplace sale listing from a codebase: counted stats, demo audit, screenshots | 7 | 6 | 8 | 7.0 |
| `skill://competitor-profiling` | Scrapes competitor sites and pulls SEO data into dated raw folders, then writes comparable profile files. | 7 | 6 | 7 | 6.7 |
| `skill://customer-research` | Mines transcripts, reviews and communities for themes, quotes and personas; runs interviews and surveys. | 7 | 6 | 7 | 6.7 |
| `skill://marketing-loops` | Sets up scheduled marketing workflows with triggers, self-checks, state, stop rules and a 43-loop catalog. | 7 | 7 | 6 | 6.7 |
| `skill://marketing-plan` | Resumable workflow producing a long AARRR-structured 12-month marketing plan with audit rubric and budget math | 6 | 8 | 6 | 6.7 |
| `skill://sms` | Plans compliant SMS/MMS programmes: TCPA and 10DLC checks, flows, copy with segment counts, platforms, KPIs | 6 | 8 | 6 | 6.7 |
| `skill://ad-creative` | Generates and iterates paid-ad copy and creative per platform, with specs, format tiers and video recipes. | 6 | 7 | 6 | 6.3 |
| `skill://ai-seo` | Audits and improves how a site gets cited by AI answer engines: structure, authority, presence, access. | 6 | 7 | 6 | 6.3 |
| `skill://marketing-council` | Simulate a panel of famous marketers applying their frameworks, map disagreements and synthesise a call | 7 | 7 | 5 | 6.3 |
| `skill://offers` | Designs or diagnoses an offer via the value equation, six components, guarantees, bonuses and honest scarcity. | 6 | 7 | 6 | 6.3 |
| `skill://product-marketing` | Drafts and versions a shared positioning file (ICP, pains, competitors, voice) other marketing skills read | 7 | 5 | 7 | 6.3 |
| `skill://social` | Plans and writes social posts: pillars, hooks, repurposing, calendars, short-form video and listening. | 6 | 6 | 7 | 6.3 |
| `skill://content-strategy` | Plans content pillars, topic clusters, buyer-stage keywords, idea scoring and a distribution approach | 6 | 6 | 6 | 6.0 |
| `skill://copywriting` | Drafts landing and website copy by section with headline, CTA formulas, annotations and alternatives. | 6 | 5 | 7 | 6.0 |
| `skill://directory-submissions` | Plans tiered startup/SaaS/AI directory submissions, Product Hunt prep, review drives and destination pages. | 5 | 7 | 6 | 6.0 |
| `skill://influencer-marketing` | Plan creator and ambassador partnerships: vetting, deal terms, briefs, disclosure rules and ROI tracking | 6 | 7 | 5 | 6.0 |
| `skill://pricing` | Guides SaaS pricing: value metric, tiers, research methods, price increases and pricing-page teardown. | 6 | 6 | 6 | 6.0 |
| `skill://signup` | Optimises signup flows: fewer fields, social auth, multi-step patterns, error handling and metrics. | 7 | 5 | 6 | 6.0 |
| `skill://site-architecture` | Plans website page hierarchy, navigation, URL patterns and internal linking with tree and Mermaid sitemaps. | 6 | 6 | 6 | 6.0 |
| `skill://churn-prevention` | Designs cancel flows, reason-matched save offers, health scores and failed-payment dunning for subscriptions. | 5 | 6 | 6 | 5.7 |
| `skill://competitors` | Plans and writes competitor alternative and versus pages with a central competitor data file. | 6 | 5 | 6 | 5.7 |
| `skill://emails` | Designs lifecycle email sequences (welcome, nurture, onboarding, win-back) with timing and copy templates | 6 | 5 | 6 | 5.7 |
| `skill://events` | Plans event marketing for hosting, sponsoring, speaking and attending, judged by cost per qualified meeting. | 6 | 6 | 5 | 5.7 |
| `skill://referrals` | Designs referral and affiliate programmes: trigger moments, incentives, sizing, fraud checks, metrics | 6 | 6 | 5 | 5.7 |
| `skill://sales-page-generator` | Writes technical sales and plain pitch documents for a codebase with Mermaid diagrams and self-contained HTML. | 6 | 5 | 6 | 5.7 |
| `skill://co-marketing` | Finds and scores co-marketing partners, lists joint campaign formats and outlines agreements and metrics. | 6 | 5 | 5 | 5.3 |
| `skill://cro` | Reviews a marketing page for conversion issues in value prop, CTAs, trust and friction, then lists fixes. | 6 | 4 | 6 | 5.3 |
| `skill://lead-magnets` | Plan a lead magnet: format by buyer stage, gating, landing page, delivery, promotion and conversion metrics | 6 | 5 | 5 | 5.3 |
| `skill://popups` | Design conversion popups and banners: triggers, types, copy, frequency caps, compliance and A/B test ideas | 6 | 5 | 5 | 5.3 |
| `skill://ab-testing` | Plans A/B tests and an experimentation program: hypotheses, sample size, metrics, analysis, ICE backlog. | 5 | 5 | 5 | 5.0 |
| `skill://analytics` | Sets up event tracking plans, GA4/GTM implementation, UTM conventions and validation for marketing analytics. | 5 | 5 | 5 | 5.0 |
| `skill://community-marketing` | Plans launch and growth of an online brand community with rituals, ambassador programmes and health metrics | 6 | 4 | 5 | 5.0 |
| `skill://free-tools` | Plans free calculators, graders and generators as lead-generation and SEO assets with a scoring card | 6 | 4 | 5 | 5.0 |
| `skill://onboarding` | Designs post-signup onboarding and activation: aha moment, checklists, empty states, emails, recovery. | 5 | 5 | 5 | 5.0 |
| `skill://paywalls` | Designs in-app upgrade screens and feature gates with trigger timing, components, frequency rules and tests. | 6 | 4 | 5 | 5.0 |
| `skill://marketing-ideas` | Catalogue of 139 SaaS marketing tactics grouped by category, stage, budget and timeline. | 5 | 4 | 5 | 4.7 |
| `skill://marketing-psychology` | Glossary of mental models and behavioural biases with one-line marketing applications. | 5 | 4 | 5 | 4.7 |
| `skill://schema` | Adds and validates schema.org JSON-LD for common page types to target Google rich results. | 4 | 4 | 6 | 4.7 |
| `skill://launch` | Plans product and feature launches across owned, rented and borrowed channels with phases and checklists. | 5 | 4 | 4 | 4.3 |

## Other

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://accessible-media-player-able-player` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://blender-physics-sims-and-baking` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://broadcast-playout-casparcg-vmix-atem` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://cloud-servers-hetzner-and-proxmox` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://comparative-scripture-sword-sefaria-openiti` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://compositing-nuke-scripts` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://construction-pm-procore-and-acc` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://cycles-turntable-render` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://dcc-interchange-maya-max-c4d-blender` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://fonts-licensing-subsetting-and-editing` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://freecad-technical-drawings` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://game-audio-middleware-fmod-wwise` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://game-distribution-steamworks-itch` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://gnucash-cost-tracking` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://imf-package-validation-photon` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://it-asset-and-service-management` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://kraken-arabic-script-manuscript-ocr` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://legal-research-westlaw-lexis-courtlistener` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://midi-rendering-fluidsynth-soundfonts` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://multicam-sync-audio-timecode` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://music-delivery-stems-and-alts` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://netsuite-saved-searches-and-workflows` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://open-2d-animation-opentoonz-synfig-pencil2d` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://packet-and-network-analysis-wireshark-nmap` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://pixel-art-and-tile-maps-aseprite-tiled` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://portrait-animation-liveportrait` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://preservation-conformance-mediaconch-qctools` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://preservation-master-and-archive-package` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://procedural-materials-material-maker-armorpaint` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://procedural-sound-supercollider-csound-pd` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://production-tracking-saas-flow-ftrack` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://sap-s4hana-for-business-users` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://sfx-library-metadata-ucs` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://sms-gateway-jasmin` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://statistics-r-rstudio-spss-stata` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://synth-plugins-surge-xt-vital` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://taskjuggler-text-schedules` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://telephony-asterisk-freepbx` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://verification-tools-tineye-fact-check` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://version-control-perforce-for-games` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://vfx-plate-pulls-and-turnover` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://voice-agent-call-flow-design` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://voice-cloning-chatterbox-f5-consent` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://web-archiving-archivebox` | - | not yet rated | not yet rated | not yet rated | not yet rated |
| `skill://word-alignment-whisperx-diarization` | - | not yet rated | not yet rated | not yet rated | not yet rated |

## Productivity & Agents

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://multi-agent-lanes-and-handoffs` | Split work across agents with worktree lanes, file ownership, contracts, independent review, one integrator | 8 | 8 | 8 | 8.0 |
| `skill://agent-memory-and-handoff-files` | Keeps long agent work resumable via a hand-off file, append-only ledger, memory index and resume test. | 8 | 7 | 8 | 7.7 |
| `skill://coding-agents-codex-cli-exec` | Runs the Codex CLI as a headless background worker: prompt on stdin, sandbox, output file, resume/fork | 8 | 7 | 8 | 7.7 |
| `skill://supervise` | Makes one agent session lead the others: authority, isolated lanes, file briefs, reviews, merges. | 8 | 8 | 6 | 7.3 |
| `skill://session-sync` | Coordinates agent sessions sharing one git checkout: ownership map, commit-by-path rules, watcher. | 6 | 6 | 5 | 5.7 |
| `skill://tutorial-to-skill` | Pulls a video tutorial's transcript and keyframe contact sheets with yt-dlp and ffmpeg, then distils a skill. | 5 | 5 | 6 | 5.3 |
| `skill://full-output-enforcement` | Behaviour rules that forbid truncated or placeholder output and define a clean pause-and-continue marker. | 6 | 3 | 6 | 5.0 |

## Publishing & Print

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://pandoc-document-conversion` | Converts documents with Pandoc using reference DOCX styles, citeproc/CSL, Lua filters and RTL-aware PDF. | 8 | 8 | 8 | 8.0 |
| `skill://podcast-rss-and-namespace` | Audits a served podcast feed: required tags, artwork, enclosures, Podcasting 2.0 tags, host moves. | 8 | 7 | 8 | 7.7 |
| `skill://ebook-production-calibre-sigil-epubcheck` | Builds and validates EPUB 3 books: structure, RTL, accessibility metadata, calibre and EPUBCheck. | 7 | 7 | 7 | 7.0 |
| `skill://pdf-preflight-pitstop-callas-ghostscript` | Preflights PDFs for print and archive: PDF/X, PDF/A, bleed, fonts, ppi, overprint, veraPDF. | 8 | 7 | 6 | 7.0 |
| `skill://print-layout-scribus-pdfx` | Lays out brochures and catalogues in Scribus: styles, ICC colour, bleed, data-driven pages, PDF/X. | 7 | 7 | 6 | 6.7 |

## Religion & Scripture

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://scripture-sources-quran-api-and-corpus` | Retrieves Quran text, attributed translations and word morphology from verified sources with RTL proofing. | 8 | 8 | 7 | 7.7 |
| `skill://hadith-search` | Fetches hadith texts by collection and number from a free public API, with display and caution notes. | 4 | 2 | 4 | 3.3 |

## Research & Archives

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://metadata-and-provenance-exiftool` | Audits media metadata with ExifTool, writes verified rights fields and strips location from copies. | 8 | 7 | 8 | 7.7 |
| `skill://public-archives-wikimedia-internet-archive` | Sources archive media from Commons and the Internet Archive with provenance, licence and credits. | 8 | 7 | 7 | 7.3 |
| `skill://research-world-and-culture` | Builds a sourced, confidence-graded world brief for a place, period and community, with anachronism checks. | 8 | 7 | 7 | 7.3 |
| `skill://business-claim-fact-check` | Builds a claim ledger for business documents: extract, classify, evidence, rate and reword before release | 7 | 6 | 7 | 6.7 |

## Sales & CRM

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://hubspot-crm-pipelines-properties-and-api` | Configures HubSpot stages, properties, associations and imports, with scoped, verified API calls. | 8 | 7 | 7 | 7.3 |
| `skill://prospecting` | Builds scored, source-cited prospect lists for SaaS, B2B, local SMB or early demand-signal discovery. | 7 | 7 | 7 | 7.0 |
| `skill://cold-email` | Writes short, peer-toned B2B cold emails and 3-5 touch follow-up sequences with subject-line and CTA rules. | 7 | 6 | 7 | 6.7 |
| `skill://donor-crm-civicrm-and-saas` | Sets gift-entry standards, dedupe, receipts, recurring gifts and retention reports in nonprofit donor CRMs | 7 | 6 | 6 | 6.3 |
| `skill://revops` | Lead lifecycle, scoring, routing, pipeline stages, deal desk and CRM hygiene for marketing-to-sales handoff | 6 | 7 | 6 | 6.3 |
| `skill://sales-enablement` | Templates for sales decks, one-pagers, objection docs, ROI calculators, demo scripts and playbooks. | 6 | 5 | 6 | 5.7 |

## Software & DevOps

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://coding-agents-claude-code-headless` | Runs a coding-agent CLI headless in pipelines: JSON output, permissions, guard hooks, project MCP. | 8 | 8 | 9 | 8.3 |
| `skill://libreoffice-headless-conversion` | Converts Office files headlessly, recalculates code-written workbooks and verifies the output. | 8 | 8 | 9 | 8.3 |
| `skill://lighthouse-ci-and-site-wide-audits` | Measures sites with Lighthouse, LHCI, Unlighthouse, PageSpeed API and WebPageTest; sets CI budgets. | 8 | 8 | 9 | 8.3 |
| `skill://core-web-vitals-remediation` | Diagnoses and fixes LCP, INP and CLS from field data down to traces, then verifies over the field window. | 8 | 8 | 8 | 8.0 |
| `skill://i18n-and-rtl-web-layout` | Localise a web app incl. Arabic and Urdu: lang/dir, ICU plurals, Intl formatting, logical CSS, bidi and fonts | 8 | 8 | 8 | 8.0 |
| `skill://nextjs-landing-page-server-action-form` | Ships a Next.js landing page with a server-action form, Turnstile, rate limiting and accessible states. | 8 | 8 | 8 | 8.0 |
| `skill://secrets-management-for-small-teams` | Inventory, store, scope and rotate team secrets, add scanning, and run a revoke-first leak response | 8 | 7 | 8 | 7.7 |
| `skill://backups-restic-and-rclone` | Sets up encrypted restic backups with retention and checks, plus hash-verified rclone copies. | 7 | 7 | 8 | 7.3 |
| `skill://deploy-nextjs-to-cloudflare-workers` | Deploys Next.js or static sites to Cloudflare Workers via OpenNext with secrets, CI, domain and rollback | 7 | 7 | 8 | 7.3 |
| `skill://firewalls-and-vpn-opnsense-wireguard-tailscale` | Segments a small-office network with zone rules, per-device WireGuard peers and scoped Tailscale access | 8 | 6 | 6 | 6.7 |

## Writing & Story

| Skill | Summary | Quality | Depth | Practical | Overall |
| --- | --- | --- | --- | --- | --- |
| `skill://design-symbols-and-motifs` | Plans story motifs from objects characters use, tracking plant, development, inversion and payoff by scene. | 8 | 7 | 6 | 7.0 |
| `skill://write-dialogue-and-subtext` | Drafts or revises dialogue around tactics and voice sheets, tests on-the-nose lines, outputs Fountain | 7 | 7 | 7 | 7.0 |
| `skill://analyze-relationships-and-power` | Maps needs, leverage, status shifts and tactics between characters or interview subjects scene by scene | 7 | 7 | 6 | 6.7 |
| `skill://control-point-of-view-and-information` | Maps who knows what scene by scene to choose suspense, surprise or mystery and test reveal orders. | 7 | 7 | 6 | 6.7 |
| `skill://copy-editing` | Edits existing marketing copy through seven focused sweeps plus word, sentence and refresh checklists | 7 | 6 | 7 | 6.7 |
| `skill://develop-theme-and-moral-dilemmas` | Turns a subject into a thematic question with costly dilemmas, a strong opposing case and a preachiness review | 7 | 7 | 6 | 6.7 |
| `skill://fountain-screenplay-toolchain` | Keeps screenplays in Fountain and exports PDF, FDX and HTML with scene-number and notes discipline. | 7 | 6 | 7 | 6.7 |
| `skill://observe-human-behavior` | Turns footage or notes into timecoded behaviour notes with alternative readings and cultural checks. | 8 | 7 | 5 | 6.7 |
| `skill://reason-character-motivation` | Maps each character's major choices to pressure, refused option and cost to flag unearned turns | 7 | 7 | 6 | 6.7 |
