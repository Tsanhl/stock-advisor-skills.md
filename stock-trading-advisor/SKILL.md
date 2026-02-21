---
name: stock-trading-advisor
description: Professional trading-advisory workflow for options and equities across indices, ETFs, forex, crypto, and commodities (including gold, silver, oil). Use when the user asks for `1`/`news report` (market-related latest news PDF), `2`/`stock recommendations` (long-short opportunities PDF), or `3`/`research on <topic>` (citation-backed research PDF). Always use the latest verifiable data, combine cross-asset indicators, and save a polished PDF to the user's Desktop.
---

# Stock Trading Advisor

Deliver executive-grade market and research outputs that are current, defensible, and directly useful for decision-making.
Treat the output bar as premium advisory work: differentiated insights, quantified implications, and explicit uncertainty.

## User Shortcut Routing (mandatory)
- `1` or `News report` -> Produce a market-moving news PDF.
- `2` or `Stock recommendations` -> Produce long/short and options recommendations PDF.
- `3` or `Research on <topic>` -> Produce a citation-backed topic research PDF.
- If topic is missing for mode `3`, ask one short question for the topic and proceed.

## Modes 1 and 2 Workflow (Market Tasks)

For mode `1` (`News report`):
- Cover the latest material developments across macro, rates, USD, major equity indices, forex, crypto, commodities (gold/silver/oil), and geopolitics.
- Explain market mechanism and likely directional impact for key assets.
- Include exact dates/timestamps for time-sensitive developments and cite sources.
- Include a simple `Coverage Check` block with one line per category:
  - `- macro data releases: <material items N or no material update in window>`
  - `- central-bank communication: <material items N or no material update in window>`
  - `- fiscal/treasury/policy actions: <material items N or no material update in window>`
  - `- geopolitics/sanctions/security: <material items N or no material update in window>`
  - `- politician/public-official statements: <material items N or no material update in window>`
  - `- rates/FX/commodities: <material items N or no material update in window>`
  - `- equity/credit/volatility tape: <material items N or no material update in window>`
- In `Sector Reason` and `Stock Reason`, require explicit transmission wording (`because`/`via`/`through`/`->`) and at least one concrete metric with number + date/period.

For mode `2` (`Stock recommendations`):
- Generate long and short opportunities with thesis, catalysts, invalidation triggers, and risk controls.
- Include options ideas where suitable (structure, expiry window, strike logic, and risk notes).
- Cross-check setups against macro regime and cross-asset signals before finalizing.
- Include a mandatory `Commodity Analysis` section with:
  - `Oil Analysis:`
  - `Gold Analysis:`
  - `Silver Analysis:`
- For each commodity subsection include current level, prior comparator, baseline comparator, driver, transmission, net impact, invalidation trigger, and explicit mapping to affected long/short opportunities.

For both modes:
- Use the most recent verifiable data available at response time.
- Separate facts vs inference and include source citations for consequential claims.
- Final deliverable must be a polished PDF saved to Desktop.

## Mode 3 Workflow (Research on Topic)

### 1. Define Scope and Deliverable
Capture:
- Topic, key question, and audience
- Domain specified by the user (for example: legal, finance, biotech, policy)
- Geographic scope
- Time horizon (historical window and what "latest" means)
- Desired output format and depth (final output is PDF)
- Decision context: what decision or action this research should support

Ask concise clarifying questions only when needed. If details are missing, state assumptions explicitly and proceed.
Treat user-provided structure as guidance, not a rigid template.

### 1.5 Expand Scope Beyond User Gaps
Before deep research, identify missing dimensions that are necessary for a complete and decision-useful report.

Common additions (when relevant):
- Counter-arguments and disconfirming evidence
- Data quality and revision risk
- Regime/context comparison (historical analogs)
- Distributional effects (who benefits, who is hurt)
- Forward triggers and scenario paths

Do not blindly mirror user claims. Validate first, then include, correct, or reject each claim with evidence.

### 2. Set Domain-Specific Source Priorities
Use the user-provided domain to set source hierarchy before research begins.

Domain priority rules:
- Legal: statutes/regulations, court judgments, regulator guidance, law commission or equivalent bodies, top-tier legal commentary.
- Finance: central banks, statistical agencies, market operators, company filings, multilateral institutions, high-quality financial data providers.
- Biotech/health: peer-reviewed journals, trial registries, regulators (FDA/EMA/etc.), major medical agencies, recognized medical datasets.
- Policy/public sector: government publications, parliamentary/legislative materials, public agencies, multilateral bodies, high-quality think tanks.
- If domain is unspecified or novel, ask once; if still unclear, state assumptions and proceed with the best-fit source hierarchy.

Within the chosen domain, prioritize primary sources and verify key claims across independent sources where possible.

### 3. Build a Source Plan
Prefer high-authority and primary sources first:
- Official statistics, regulators, central banks, ministries, company filings
- Peer-reviewed papers, standards bodies, and official documentation
- Reputable wire services and leading outlets for breaking developments

For critical claims, confirm with at least two independent sources where possible.
Avoid single-source conclusions on disputed or fast-moving topics.

### 4. Gather and Validate Data
For each material fact, capture:
- Exact value and units (if quantitative)
- Time reference (e.g., quarter/year/date)
- Methodology notes if they affect interpretation
- Source URL, publisher, title, and publication/update date

When user requests "latest", re-check freshness before finalizing and include exact dates.
Do not infer unavailable facts; mark missing data and provide best proxy with limitations.

### 5. Synthesize Without Logical Gaps
Build each argument as:
1. Claim
2. Evidence
3. Reasoning
4. Implication

Separate:
- Observed facts
- Interpretation/inference
- Assumptions and uncertainty

Address conflicting evidence directly instead of ignoring it.

### 6. Generate Premium Insights (Not Just Summary)
For each major finding, include:
- Why this matters now
- What is non-obvious versus baseline commentary
- Quantified impact where possible (size, sensitivity, timeline)
- Decision implications (what to do, what to monitor, what changes the thesis)

Apply the standards in `references/premium-insight-standards.md`.

### 7. Write the Report
Default structure:
1. Executive Summary
2. Scope and Method
3. Decision-Critical Insights
4. Detailed Analysis
5. Scenarios, Risks, and Trigger Points
6. Conclusion and Recommended Monitoring
7. References

Writing standard:
- Coherent flow between sections and paragraphs
- Clear topic sentences and transitions
- No contradictions in numbers, dates, or claims
- Precise language with minimal filler
- Professional tone matching analytical audience
- Add missing high-value sections even if user did not request them explicitly
- Prefer explicit channel numbering for analytical chains when useful:
  - `Channel 1`, `Channel 2`, `Channel 3`
  - each channel must show `fact -> comparator -> mechanism -> implication -> risk trigger`

## Perfection Protocol (mandatory)
- Absolute perfection cannot be guaranteed in live/fast-changing topics; target is maximum practical completeness and correctness in-turn.
- Use two-pass verification for any topic with `latest/current/today` sensitivity:
  - Pass 1: full evidence build and synthesis
  - Pass 2: final delta rescan near output time (target within 10 minutes of output timestamp)
- If pass 2 finds meaningful new information:
  - update impacted sections
  - add a `Delta Update` note explaining the change
- Coverage completeness rule:
  - explicitly list which critical dimensions were scanned (policy, macro, market, sector, legal/regulatory, or topic-relevant equivalents)
  - if a critical dimension has no update, state `No material update in window`
- Mechanism clarity rule:
  - reject vague wording like `supportive`/`headwind` unless transmission is explicitly explained (what changed -> why it changes earnings/cost/valuation -> horizon).
- If a major claim depends on a single source, mark confidence lower and disclose single-source limitation.

## Quality Gates (Must Pass)

Run the checklist in `references/research-quality-checklist.md` before final output.
If a gate fails, fix and re-check before delivering.

## PDF Output Contract

Always deliver a PDF file as the final artifact.

Preferred flow:
1. Draft report content in Markdown using `references/research-report-template.md`.
2. Write working markdown to `/tmp/<report-name>.md` (internal only, not for user delivery).
3. Convert to PDF with cleanup:
   - `python3 scripts/build_pdf.py --input /tmp/<report-name>.md --output /Users/hltsang/Desktop/<report-name>.pdf --title "<title>" --cleanup-input`
4. Do not save working markdown to Desktop.
5. Verify the PDF exists and is readable before final response.
6. In final response, provide only:
   - Desktop PDF path
   - 3-5 headline insights
   - Main caveats
7. Do not include markdown paths in user-visible output.

Mode `1` naming rule (strict):
- PDF: `/Users/hltsang/Desktop/News_Report_<YYYYMMDD_HHMM>_<TZ>.pdf`

Mode `2` naming rule (strict):
- PDF: `/Users/hltsang/Desktop/Stock_Recommendations_<YYYYMMDD_HHMM>_<TZ>.pdf`

Mode `3` naming rule (strict):
- PDF: `/Users/hltsang/Desktop/Research_<topic-slug>_<YYYYMMDD_HHMM>_<TZ>.pdf`

Indicator presentation rule (strict):
- If the renderer cannot produce true tables, do not use Markdown pipe tables (`|...|`).
- Do not output repeated anonymous labels like `Indicator:` without numbering.
- Use numbered indicator cards exactly in this format:
  - `Indicator 1: <indicator name>`
  - `Current: <value/fact> (<date>, <unit if any>)`
  - `Prior: <value/fact> (<date>, <unit if any>)`
  - `Baseline: <normal regime or pre-shock reference> (<date/range>)`
  - `Interpretation: <one clear sentence>`
  - `Why it matters now: <decision linkage + horizon>`
  - `Source: [n] <direct URL>`
- Include at least 3 indicator cards unless the topic is structurally narrow.
- If an indicator is qualitative, include an observable proxy and an explicit limitation note.

Layout standard:
- Use readable spacing and paragraph flow (no cramped line-by-line rendering).
- Remove markdown artifacts in final PDF text (for example raw `**` markers).
- Keep references legible with consistent `[n]` numbering.

## Citation and Date Rules

Always:
- Cite every non-trivial factual claim using inline numeric markers like `[1]`
- Put citation markers directly after the relevant sentence or clause
- Reuse the same number for repeated use of the same source
- Use multiple markers when needed (for example: `[3][4]`)
- Include publication/update date where available
- Distinguish event date from publication date when they differ
- Use exact calendar dates in outputs when "today/yesterday/latest" is relevant
- End each report with a `References` section listing:
  - `[n]` Title, publisher/author, URL, publication or update date

## Output Template

Use `references/research-report-template.md` when the user does not provide a custom format.

## Operational Notes

- Prefer primary sources for technical claims and official figures.
- Use secondary sources to contextualize, not to replace primary evidence.
- If access limits block verification, disclose the gap and provide the safest bounded conclusion.
- Never claim "100k-quality" work without original synthesis, quantified implications, and decision-useful recommendations.
