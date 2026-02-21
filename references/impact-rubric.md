# Market Impact Rubric

Use this rubric for professional, specific, and data-backed analysis.

## Sentiment Labels
- `Positive`: expected to improve earnings outlook, liquidity, or risk appetite.
- `Negative`: expected to worsen earnings outlook, liquidity, or risk appetite.
- `Neutral`: mixed impact or low directional edge.

## Confidence Labels
- `High`: multi-source confirmation and strong data alignment.
- `Medium`: thesis is supported but at least one key variable is unresolved.
- `Low`: conflicting data or weak confirmation.

## News Coverage Standard
- Use a fixed 24-hour capture window by default.
- If user specifies time/timezone, use that exact timezone and timestamp as cutoff.
- Compute and display: `window start = cutoff - 24h`, `window end = cutoff`.
- If user requests a different window, honor that override and state it explicitly.
- Include all market-relevant items in window.
- Deduplicate only duplicate reporting of the same event.
- Provide one direct source URL in every news card.
- Add coverage summary with counts and coverage gaps.
- Include material politician/public-official statements when they are market-moving.
- Run a dedicated sweep for:
  - head-of-state/government remarks
  - central-bank and treasury/finance-ministry communication
  - sanctions/trade/security policy statements
  - verified official social posts (X/Truth Social) when materially market-relevant
- Use two-pass scan discipline:
  - initial scan and synthesis
  - final delta rescan near output time
  - update report if new material appears
- Maintain a coverage matrix with required categories using strict fields per row: `Scan` and `Covered`; use `Covered: material items N` or `Covered: no material update in window`.

## Source Priority Standard
- Use this priority for factual claims:
  - official/public institution releases (Fed, BLS, Treasury, agency data)
  - issuer reports/filings/press releases
  - major wire coverage for market context
- Do not rely on a secondary summary when a primary source is available.
- If only secondary source is available, label confidence lower and state limitation.
- For social-post items:
  - use official verified account/transcript first
  - include exact post/speech timestamp
  - confirm with one independent source when available
  - if authenticity is unclear, classify as unconfirmed and do not use as directional anchor
- For high-impact items, use at least two independent sources when possible; otherwise downgrade confidence and flag single-source limitation.

## Macro Context Standard
Each news/recommendation item must state:
- Indicator used (for example 10Y yield, real yield, USD index, oil, inflation print)
- Current value and timestamp
- Direction versus prior observation
- Transmission channel to sectors/stocks
- Net directional effect (`Positive`/`Negative`/`Neutral`)
- Clear causal chain with no logical gaps (data -> mechanism -> impact on earnings/cost/valuation -> conclusion)
- Impact horizon (intraday / 1-4 weeks / multi-quarter)
- Relevance rule: include only channels that are causally relevant to that specific opportunity.
- Geopolitics is optional and should be included only when material.
- Recommendation-set must include a separate commodity block (oil/gold/silver) and map it to Long/Short selections.
- For news cards, prefer one merged `Macro + Transmission Context` block to avoid duplicated or fragmented explanations.

## News Card Clarity Standard
- Each card must include `Fact Brief` and `Comparator` fields before interpretation.
- `Fact Brief` must answer who/what/when/where plus key number(s).
- `Comparator` must show current vs prior/baseline with exact dates.
- `Reason` must include: `Primary channel`, `Mechanism`, and `Why now`.
- `Sector Reason` must include: `Sector exposure channel`, `Sector mechanism`, `Sector timing`, and `Sector metric`.
- `Stock Reason` must include: `Stock exposure channel`, `Stock mechanism`, `Stock timing`, and `Stock metric`.
- If using breadth language, define breadth with metric and universe (for example `% of S&P 500 above 50DMA`).
- Do not use unexplained shorthand like "risk-off", "supportive", or "cooling breadth" without data definition.
- If a card is statement-driven, include `Public-Signal Verification` with speaker, role, channel, timestamp, and verification status.
- Each card must pass six logic checks:
  - What happened?
  - Compared with what?
  - Why this channel moves markets?
  - Which assets/sectors/stocks are most exposed?
  - Over what horizon?
  - What invalidates the interpretation?

## Direction-First Recommendation Standard
Recommendations must be grouped and presented by direction:
- `Long` opportunities
- `Short` opportunities

For each opportunity:
- `Stock Suggestion` is mandatory and must include horizon tag:
  - `Short term` (weeks to months), or
  - `Long term` (>= 5 months to 1 year+)
- `Options Suggestion` is optional and reference-only.
- If options are omitted, state explicit reason (liquidity/IV/macro-event risk).
- Commodity Direction Add-on is mandatory at report level:
  - Oil, Gold, Silver direction
  - relevant stocks/ETFs/futures proxies
  - per commodity: current value, prior comparator, baseline comparator, driver, transmission, net impact, invalidation trigger
  - mapping to Long/Short recommendation list
  - format enforcement:
    - use `Mapping:` as subsection label (not bullet)
    - include one blank line before `Mapping:`

## Company Fundamentals Standard (recommendations)
When recommending a stock, include explicit data:
- Metric name
- Value + unit
- Period/date
- Prior comparator (y/y, q/q, or prior period)
- Why the metric changes recommendation now
- Direct source URL

Do not use unsupported statements such as "healthy fundamentals" without figures.

## Options Recommendation Standard
If an options suggestion is provided, include:
- direction and type: `Call (swing)` or `Put (swing)`
- strategy structure (long option or defined-risk spread)
- expiry and strike rationale tied to expected move timing
- premium/debit, max loss, breakeven, and target/exit plan
- option liquidity quality (volume/open interest/bid-ask) when available
- implied-volatility context (rich/fair/cheap) when available
- greek risk profile (delta/gamma/theta/vega direction) when available
- explicit exit logic

Risk discipline rule:
- No options suggestion is valid without explicit max-loss and invalidation logic.
- If full contract-level fields are unavailable, omit options suggestion and state reason.

## Price Structure Standard (recommendations)
For each stock recommendation, include:
- current price with timestamp/source
- major support levels (daily/weekly) with historical touch/reaction context
- major resistance levels with rejection/breakout history
- drawdown math:
  - current vs 52-week high
  - current vs key prior high (if relevant)
- historical buyer behavior at comparable pullback magnitudes
- zone label: `buying zone`, `neutral zone`, or `sell-into-strength zone`

Interpretation rule:
- Fundamentals positive + price near credible support with prior buyer response = higher-quality long setup.
- Fundamentals weak + price near major resistance/failed bounce = higher-quality short/underweight setup.
- If signals conflict, downgrade confidence and tighten risk controls.

## Risk and Overturn Standard (recommendations)
Each recommendation must include:
- `Key Risks Worth Noting`:
  - at least one macro risk
  - at least one company or setup-specific risk
  - quantitative or clearly observable trigger level when possible
  - explicit mechanism from trigger -> thesis damage
- `Overturn Conditions`:
  - clear invalidation criteria tied to observable signals (price levels, estimate revisions, guidance changes, macro prints, policy path)
  - practical action if triggered (reduce, exit, hedge, or suspend setup)
- `Trigger Grid`:
  - bull/bear/invalidation triggers with explicit action
- `Catalyst Calendar`:
  - near-term dated events and expected volatility regime around those events
- `Sizing and Correlation Note`:
  - size adjusted for volatility and conviction
  - overlap risk versus other recommendations (concentration/correlation control)

## Logic-Gap Rejection Rules
Reject or rewrite any section that fails one or more checks:
- Uses conclusion words without quantified support.
- Mentions a macro channel but does not explain company-level transmission.
- Provides direction (positive/negative) without mechanism.
- Uses vague support/headwind language without explicit transmission path.
- Provides mechanism without time horizon.
- Uses data outside the analysis cutoff window without labeling it as historical context.
- Recommends a stock without both (a) fundamental evidence and (b) price-structure evidence.
- Recommends a stock without explicit downside risks and overturn conditions.
- Omits stock direction or horizon tag.
- Includes non-relevant macro channels that do not affect the specific opportunity.
- Uses breadth language without naming the breadth metric/universe and comparator.
- Uses politician/public-official statement as market driver without authenticity verification and timestamp.
- Claims complete market coverage without reporting a coverage matrix and final delta rescan.
- Fails structure validation for required sections/labels in the active report mode.
- Uses vague risk statements without trigger level or mechanism.
- Provides options suggestion without expiry/strike rationale and max-loss definition.
- Uses placeholder language (for example \"use latest filing\") instead of concrete data.
- Uses a horizon label inconsistent with setup/targets/catalyst timing.
- Missing source URL for a company fundamental data point.

## Fluency and Clarity Standard
- Each paragraph should answer one clear question.
- Avoid ambiguous references (`this`, `that`, `it`) when multiple drivers are discussed.
- Keep causal statements directional and testable.

## Data Comparison Standard
For research requests, include at least one explicit comparison block:
- current value
- prior-period value
- baseline value (when relevant, e.g. pre-COVID)
- units and dates

## Conclusion Standard
Each opportunity must end with a 2-3 sentence conclusion that states:
- why the opportunity is actionable now,
- what condition would weaken confidence,
- the practical risk-control stance.

## Cross-Asset Confirmation Rule
For swing/macro direction, use at least three indicators and explain whether they align or conflict.
If conflicting, lower confidence and tighten risk controls.
