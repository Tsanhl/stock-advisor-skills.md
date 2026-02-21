---
name: stock-trading-advisor
description: Professional trading-advisory workflow for options and equities across indices, ETFs, forex, crypto, and commodities (including gold, silver, oil). Use when the user asks for `1`/`news report` (market-related latest news PDF) or `2`/`stock recommendations` (long-short opportunities PDF), or asks for options suggestions and stock long/short ideas. Always use the most up-to-date available market data and news, combine cross-asset indicators (for example USD, rates, oil, gold, silver, geopolitics, equity indices), and generate a polished PDF saved to the user's Desktop.
---

# Stock Trading Advisor

## Mission
Deliver objective, professional financial analysis with real, current data and produce a PDF report on the Desktop.

## User Shortcut Routing (mandatory)
- `1` or `News report` -> Run Function `2) Market-Related News Analysis`.
- `2` or `Stock recommendations` -> Run Function `1) Recommendations (Options + Stocks)`.
- `3` or `Research on <topic>` -> Do not run this skill; route to the `research` skill.
- If the user request is ambiguous, ask one short disambiguation question using the `1/2/3` mapping.

## Core Requirements (non-negotiable)
- Use latest available data for every claim.
- Provide direct source links for every key claim and each news card.
- Use explicit data comparisons (current vs prior period and, when relevant, vs pre-COVID baseline).
- Distinguish fact from inference.
- Never rely on vague wording without data support.
- Anchor all analysis to the user-requested timestamp and timezone when provided.

## Excellence Protocol (always-on)
- Accuracy target is maximum practical accuracy in-turn using latest available verifiable data.
- Do not present uncertain or unavailable data as fact.
- For every numerical claim, include:
  - value
  - unit
  - date/time
  - comparator (prior/baseline where relevant)
  - source URL
- For market-moving claims, confirm with at least one primary source (official release or issuer filing/press release) and one market-source context when available.
- If sources conflict:
  - state conflict explicitly
  - prioritize primary/official source for facts
  - downgrade confidence until reconciled
- No logic gaps allowed:
  - every conclusion must show full chain:
    - data -> mechanism -> earnings/cost/valuation impact -> actionable implication
- No vague wording:
  - banned unless explained with data: `supportive`, `headwind`, `risk-on`, `risk-off`, `strong`, `weak`, `healthy fundamentals`.
- Fluent professional standard:
  - clear subject, causal direction, and time horizon in each analytical paragraph.

## Perfection Protocol (mandatory)
- Absolute perfection cannot be guaranteed in live markets; target is maximum practical completeness and accuracy in-turn.
- Use two-pass coverage for each report:
  - Pass 1: full scan and initial synthesis
  - Pass 2: final delta rescan immediately before output (target within 10 minutes of output timestamp)
- If pass 2 finds new material:
  - update affected news cards/recommendations
  - add a `Delta Update` note describing what changed
- Add a `Coverage Matrix` in news mode with these categories:
  - macro data releases
  - central-bank communication
  - fiscal/treasury/policy actions
  - geopolitics/sanctions/security
  - politician/public-official statements
  - rates/FX/commodities
  - equity/credit/volatility tape
- Keep Coverage Matrix simple and audit-friendly.
- For each coverage-matrix category, use this strict one-line format:
  - `- <category> | Scan: <source groups scanned> | Covered: <material items N or no material update in window>`
- High-impact rule:
  - for items likely to move major index/sector materially intraday, require two independent sources when possible
  - if only one source is available, downgrade confidence and flag single-source risk

## Core Functions (mandatory)

### 1) Recommendations (Options + Stocks)
Provide actionable opportunities using current market data, macro context, company fundamentals, and price structure.

Direction-first output structure (mandatory):
- `Long` section:
  - `Opportunity 1`, `Opportunity 2`, ...
- `Short` section:
  - `Opportunity 1`, `Opportunity 2`, ...

Expression rule per opportunity:
- `Stock Suggestion` (required):
  - `Long` or `Short`
  - horizon tag:
    - `Short term` (weeks to months)
    - `Long term` (>= 5 months to 1 year+)
- `Options Suggestion` (optional, reference only):
  - `Call (swing)` for long-direction ideas
  - `Put (swing)` for short-direction ideas
  - include indicative swing horizon

Options inclusion rule:
- Options are not mandatory.
- Include options only when liquidity/spread quality and macro event-risk conditions are acceptable.
- If options are not suggested, state the reason (for example poor liquidity, expensive implied volatility, or elevated macro/event risk).

Opportunity count rule:
- No fixed minimum or maximum count.
- Number of opportunities must be determined by market breadth, signal quality, and request time window.
- Include only setups that pass data-quality and risk/reward thresholds; if conditions are poor, fewer setups are acceptable.

For each opportunity include all of the following:
- `Direction` (`Long` or `Short`)
- `Stock Suggestion` (required): direction + horizon tag (`Short term` or `Long term`)
- `Options Suggestion` (optional, reference only): `Call (swing)` or `Put (swing)` + indicative swing horizon
- `Entry zone`
- `Stop loss`
- `Target 1` and `Target 2`
- `Invalidation trigger`
- `Time horizon`
- `Risk/Reward`
- `Confidence`
- `Thesis Type` (`structural`, `cyclical`, `event-driven`, or mixed)
- `Data Evidence (company)`: latest reported revenue growth, margin trend, guidance change, balance-sheet signal, and valuation context with exact figures and periods
- `Data Evidence (company)` (strict format per metric):
  - metric name
  - value + unit
  - period/date
  - change vs prior (`y/y`, `q/q`, or prior period)
  - direct source URL
- `Option Structure` (required only when options are suggested):
  - strategy (`Long Call`, `Long Put`, or defined-risk spread)
  - expiry and why it matches swing horizon
  - strike selection rationale (ATM/OTM/ITM with delta/convexity logic when available)
  - premium/debit, max loss, breakeven, and target plan
  - liquidity check (volume/open interest/bid-ask quality) when available
  - implied-volatility context (rich/fair/cheap versus recent regime) when available
  - greek risk profile (delta/gamma/theta/vega direction) when available
- `Price Structure & Technical Context`:
  - current price with timestamp
  - distance to major historical support/resistance levels (daily/weekly)
  - drawdown from 52-week high and, when relevant, from prior cycle high
  - buyer-reaction evidence at similar prior pullbacks (for example: prior -10%/-15% zones and subsequent reaction)
  - whether current zone is `buying zone`, `neutral zone`, or `sell-into-strength zone`
- `Macro Fit`: include only macro channels that are directly relevant to the specific opportunity (no filler channels), and for each included channel state:
  - current value + prior comparator + direction
  - transmission mechanism to this company/asset
  - whether that channel is supportive or restrictive now
  - expected time horizon of impact (immediate / 1-4 weeks / multi-quarter)
- `Causal Chain` (mandatory):
  - explicit sequence: data change -> business mechanism -> earnings/cost/multiple effect -> trade action
- `Valuation Transmission` (mandatory):
  - why valuation should re-rate/de-rate now
  - include at least one concrete sensitivity/threshold when available
- `Commodity Direction Add-on` (mandatory at recommendation-set level):
  - directional view for `Oil`, `Gold`, `Silver`
  - for each commodity, include:
    - `Current` (exact level/price, timestamp, source)
    - `Prior comparator` (previous session/day/week level + change in % or bps)
    - `Baseline comparator` (for example 1M/3M average or pre-event level)
    - `Driver` (what changed and why, source-backed)
    - `Transmission` (how this affects earnings/costs/valuation for selected names)
    - `Net impact` (`Positive`/`Negative`/`Neutral`) with horizon
    - `Invalidation trigger` (observable level/event that weakens this commodity view)
  - relevant tradable proxies (for example `USO/CL`, `GLD/GDX`, `SLV/SIL`, `XLE/CVX/XOM`)
  - explicit mapping from commodity view -> Long/Short opportunity selection
  - mapping must name exact opportunities affected and direction of effect
  - if commodity signal is mixed, state mixed and lower confidence accordingly
  - formatting rule:
    - use `Mapping:` as a standalone subsection label (not `- Mapping:` bullet)
    - leave one blank line before `Mapping:`
- `Why now`: catalyst timing path tied to dated events/data
- `Catalyst Calendar`:
  - next dated events (earnings, CPI/FOMC/jobs, and geopolitical events only if material) relevant to the setup
  - expected volatility window around those events
- `Key Risks Worth Noting`:
  - top downside risks specific to this setup (macro, company, positioning, liquidity/event risk)
  - risk trigger levels (numeric/observable where possible; for example 10Y real yield threshold, CPI surprise size, support-break level)
  - explicit mechanism from risk trigger -> thesis damage
  - probability-weighted relevance for the stated horizon
- `Trigger Grid`:
  - bull trigger(s)
  - bear trigger(s)
  - invalidation trigger(s)
  - required action per trigger (add / reduce / exit / hedge)
- `Overturn Conditions`:
  - explicit conditions that would reverse or cancel the recommendation
  - observable triggers/thresholds (price, revisions, macro prints, guidance changes)
- `Sizing and Correlation Note`:
  - position sizing guidance by conviction and volatility
  - correlation overlap warning versus existing top exposures (for example mega-cap tech concentration, oil beta stacking)
- `Conclusion`: mandatory 2-3 sentence professional conclusion explaining why the opportunity is actionable now

Do not use generic statements such as "fundamentals are healthy" without numbers and source-backed evidence.
Do not use placeholder text such as \"use latest filing\" in final output.
Do not use unexplained phrases such as "USD/oil/gold/silver channel" without explicitly stating:
- what moved,
- why it moved,
- how that changes revenue/cost/margin/valuation for the specific name.
Do not publish options suggestions without an explicit max-loss statement and invalidation plan.
If options are suggested, provide full contract-level details (strategy, expiry, strike(s), premium/debit, max loss, breakeven, and exit logic). Otherwise omit options suggestion.
Do not omit stock direction/horizon even when an options suggestion is provided.
Do not mix long-term horizon labels with purely short-swing setup logic; horizon and trigger design must be coherent.
Do not claim support/resistance without referencing observable historical price behavior.
Do not include non-relevant macro channels for completeness; include only channels with clear causal relevance to that opportunity.
If technical structure and fundamentals disagree, lower confidence and explain which signal dominates.
Every recommendation must state what can go wrong and what would overturn the thesis.

### 2) Market-Related News Analysis
When user asks for latest news, include all market-relevant items in scope and analyze impact deeply.

Time window rule:
- Default capture window for news mode is fixed at `24 hours` ending at the report cutoff.
- If user provides explicit time/timezone (example: `13:36 Europe/London`), use that as the report cutoff.
- Compute window as: `Window start = cutoff - 24 hours`; `Window end = cutoff`.
- If user explicitly asks for a different window, follow user instruction and state the override.
- Convert and present all event times in the same report timezone (the user-requested timezone).
- In `Coverage Summary`, always print both absolute timestamps clearly as:
  - `Window start (24h capture)`
  - `Window end (cutoff)`

Coverage and accuracy rule:
- Run broad market scan first (macro, policy, geopolitics, rates, commodities, indices).
- Run sector and asset scan second.
- Include all relevant items in window; deduplicate only repeated coverage of the same event.
- Add a `Coverage Summary` with source groups, item count, dedupe count, and any coverage gaps.
- Add one accurate `Reference:` link in each news card.
- Normalize times to a single timezone in the report.
- Include a `Policy and Public-Statement Sweep`:
  - heads of government/state, central-bank officials, treasury/finance ministers, and other market-moving policymakers
  - official channels (official websites, transcripts, verified official accounts on X/Truth Social, press briefings, major-wire confirmed remarks)
  - if a statement is potentially market-moving, include it as a news card even when no hard data release occurs
- For social-post-driven items, require verification before use:
  - verified official account or official transcript
  - exact post/speech timestamp
  - one independent confirmation source when available (for example Reuters/Bloomberg/AP)
  - if not verifiable, mark as unconfirmed and exclude directional recommendation from that item

Per news card required structure:

```text
News 1: <headline> (<time>)
Fact Brief: <who did what, where, and when; include key number(s)>
Comparator: <current vs prior/baseline with date>
Reference: <direct source URL>
Public-Signal Verification (if applicable):
- <speaker/role/channel/time/verification status>
Impact on Market: Positive | Negative | Neutral
Reason:
- Primary channel: <policy/rates/inflation/commodities/liquidity/positioning>
- Mechanism: <explicit cause -> effect -> pricing/earnings/valuation path>
- Why now: <what changed in this 24h window versus prior>
Macro + Transmission Context:
- <indicator + current value + prior comparator + direction + time horizon>
- <full chain: fact -> mechanism -> earnings/cost/valuation impact -> tradable implication>
Sector Impacted and Its Impact: <sector/subsector>
Impact: Positive | Negative | Neutral
Sector Reason:
- Sector exposure channel: <input-cost/demand/duration/FX/credit/regulation>
- Sector mechanism: <how this factor moves sector performance>
- Sector timing: <intraday / 1-4 weeks / multi-quarter>
- Sector metric: <one concrete metric/threshold>
Stocks: <symbols or />
Impact: Positive | Negative | Neutral
Stock Reason:
- Stock exposure channel: <company-specific channel>
- Stock mechanism: <how this changes earnings/cost/valuation for these names>
- Stock timing: <intraday / 1-4 weeks / multi-quarter>
- Stock metric: <one concrete metric/threshold>
Counter-risk / Invalidation:
- <what would reverse or weaken this call>
Recommendations: <actionable implication>
```

Rules:
- If no stock impact is identifiable: `Stocks: /`.
- If impact is `Neutral`, mark neutral explicitly and explain when needed.
- No sentence cap; explain fully and precisely.
- Per news card, include full logic chain with explicit comparators:
  - what changed (fact, number/date/source)
  - comparator (prior/baseline)
  - transmission mechanism
  - tradable implication
  - invalidation or counter-risk
- Every market-impact card must answer these six checks explicitly:
  - What happened?
  - Compared with what?
  - Why does that move this market/sector/stock?
  - Over what horizon?
  - What could invalidate this interpretation?
  - What action follows?
- Do not use vague terms (for example "cooling breadth", "risk-off", "supportive") unless explicitly defined with the metric and comparator.
- If using breadth language, specify breadth of what:
  - index/universe (for example S&P 500, Russell 2000)
  - metric (advance-decline line, % above 50DMA/200DMA, new highs-lows)
  - current value vs prior value/date

### 3) Specific Topic Financial Analysis
For any requested topic, deliver comprehensive research with current real data.

Minimum content:
- `Question definition`: what is being evaluated and timeframe.
- `Indicator comparison block`: current vs prior vs baseline comparisons (with dates and units).
  - Use either:
    - a true rendered table supported by the output channel, or
    - a non-table `Indicator Card` format per row:
      - `Indicator 1: <name>` / `Indicator 2: <name>` / `Indicator 3: <name>`
      - `Current`
      - `Prior`
      - `Baseline`
      - `Interpretation`
      - `Why it matters now`
      - `Source`
  - Do not use Markdown pipe-table syntax (`|...|`) in report markdown unless you are certain the renderer outputs a real table.
- `Macro analysis`: transmission channels and direction.
- `Fundamental/market analysis`: earnings, margins, credit, labor, demand, valuation, or other relevant pillars.
- `Counter-arguments`: what could invalidate thesis.
- `Professional conclusion`: comprehensive decision-oriented summary.

## Cross-Asset Synthesis (mandatory for swing/macro calls)
Use at least three indicators and explain combined signal:
- Dollar trend
- Real yields or treasury yields
- Oil trend
- Gold trend
- Silver trend
- Geopolitical risk state (optional, include only if material)
- Equity-index risk tone

State how each indicator affects the thesis and whether the net effect is supportive or conflicting.
For recommendations, oil/gold/silver directional analysis is mandatory at recommendation-set level; geopolitics is optional and included only if materially relevant.

## Required Output Standard
- Current information only; verify before concluding.
- Every key statement supported by data and source.
- Professional detail level suitable for institutional-style memo quality.
- Generate PDF to Desktop for every output.

## Workflow
1. Classify request by function.
2. Gather latest data/news and verify sources.
3. Build analysis with explicit data comparisons.
4. Write report using templates/references.
5. Generate PDF on Desktop.

## PDF Output Command
```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/stock-trading-advisor"
TS="$(date +%Y%m%d_%H%M)"
TZ_TAG="$(date +%Z)"

# Mode 1: News report
python3 "$SKILL_ROOT/scripts/validate_report_structure.py" \
  --input /tmp/market_news_report.md \
  --mode news

python3 "$SKILL_ROOT/scripts/write_market_report_pdf.py" \
  --input /tmp/market_news_report.md \
  --output "$HOME/Desktop/Market_News_Report_${TS}_${TZ_TAG}.pdf"

# Mode 2: Stock recommendations
python3 "$SKILL_ROOT/scripts/validate_report_structure.py" \
  --input /tmp/stock_recommendations.md \
  --mode recommendations

python3 "$SKILL_ROOT/scripts/write_market_report_pdf.py" \
  --input /tmp/stock_recommendations.md \
  --output "$HOME/Desktop/Stock_Recommendations_${TS}_${TZ_TAG}.pdf"
```

PDF naming rule (strict):
- Mode `1` must output: `/Users/hltsang/Desktop/Market_News_Report_<YYYYMMDD_HHMM>_<TZ>.pdf`
- Mode `2` must output: `/Users/hltsang/Desktop/Stock_Recommendations_<YYYYMMDD_HHMM>_<TZ>.pdf`

## Quality Gate Before Final Answer
- Latest data/news verified in this turn.
- Data comparisons included (current vs prior/baseline where relevant).
- No vague unsupported statements.
- Macro channel logic is explicit and complete (no missing causal steps).
- Per-opportunity conclusion present.
- Direction-first structure present (`Long` and `Short` sections with numbered opportunities).
- Per-opportunity price-structure evidence present (support/resistance/drawdown/reaction context).
- Per-opportunity `Key Risks Worth Noting` and `Overturn Conditions` present and specific.
- Per-opportunity `Trigger Grid` present with numeric/observable triggers.
- Per-opportunity macro channels are relevant (no non-causal filler).
- Per-opportunity `Causal Chain` and `Valuation Transmission` are explicit.
- Per-opportunity stock suggestion and horizon tag present.
- If options are suggested, full contract-level option details and max-loss/breakeven fields are present.
- If options are not suggested, omission reason is stated.
- No placeholder language or missing source URLs in `Data Evidence`.
- Horizon label is consistent with setup, targets, and catalyst timeline.
- Recommendation-set includes `Commodity Direction Add-on` for oil/gold/silver with explicit mapping to Long/Short list.
- Per-news card reference present and accurate.
- Coverage summary present.
- Coverage matrix present with required categories.
- News depth gate:
  - each news card includes fact/comparator/mechanism/implication/invalidation chain,
  - include at least 6 materially distinct items unless fewer are truly available (if fewer, state why).
- News clarity gate:
  - each card uses `Fact Brief` and `Comparator` explicitly,
  - `Reason` uses `Primary channel`, `Mechanism`, and `Why now`,
  - `Macro + Transmission Context` includes indicator value + prior comparator + impact horizon,
  - `Sector Reason` and `Stock Reason` include channel/mechanism/timing/metric fields.
- Market-coverage completeness gate:
  - scan and document results for macro data, policy releases, central-bank communication, geopolitical updates, commodities, rates, equity-index flow, and material politician/public-official statements.
  - if a category has no material update, state "no material update in window."
- Public-statement verification gate:
  - all politician/public-official statement items include source authenticity and timestamp checks.
  - social posts are included only when verified as official or independently confirmed.
- Final delta-check gate:
  - document second-pass rescan time near output.
  - if no new items, state `Delta Update: no new material items after final rescan`.
- Structure-validator gate:
  - `scripts/validate_report_structure.py` must return `PASS` for the active mode before PDF generation.
- Each recommendation/news thesis passes logic-chain audit:
  - What changed?
  - Why did it change?
  - Why does that matter for this asset/company?
  - Why now?
  - What would invalidate the view?
  - What is the risk-control action?
- If critical data is unavailable at cutoff, report gap explicitly instead of inferring.
- PDF generated on Desktop.
