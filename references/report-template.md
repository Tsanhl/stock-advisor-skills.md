# Trading Advisory Report Template

Use this structure for every output.

## 1) Header
- Keep a single title only.
- Function mode: `Recommendations (Options + Stocks)` / `Market News Analysis` / `Specific Topic Analysis`
- Prepared for: `<user/request context>`
- Timestamp: `<local datetime + timezone>`
- Analysis cutoff requested by user: `<datetime + timezone>`
- Data recency note: `Market/news checked as of <timestamp>`

## 2) Executive View
- Market regime summary.
- Key macro drivers.
- Main conclusion in 3-5 lines.
- Keep language explicit and causal (avoid generic statements without mechanism).

## 3) Cross-Asset Dashboard
Show latest values (with date/time) for:
- USD index
- 2Y and 10Y yields
- 10Y real yield and breakeven inflation (if available)
- Oil
- Gold
- Silver
- Equity index tone

Add net implication for the target assets.

Indicator card format (mandatory, no standalone `Source:` line):
- `Indicator 1:`
- `<indicator name>`
- `Current:`
- `<latest value> (<as-of date/time + timezone, frequency>)`
- `Prior:`
- `<prior comparable value> (<date/time>)`
- `Baseline:`
- `<baseline reference> (<date/range>)`
- `Interpretation:`
- `<one precise sentence>`
- `Why it matters now:`
- `<one precise sentence with inline [n] citation if factual>`

## 4) Opportunities (required for recommendation mode)
Do not use markdown tables.
Use numbered opportunity cards.
Do not enforce a fixed count. Include as many opportunities as pass quality thresholds in the current market window.
Organize in this order:
- `Long`
  - `Opportunity 1`, `Opportunity 2`, ...
- `Short`
  - `Opportunity 1`, `Opportunity 2`, ...

Recommendation expression:
- `Stock Suggestion` (required): `Long`/`Short` with horizon tag:
  - `Short term` (weeks to months)
  - `Long term` (>= 5 months to 1 year+)
- `Options Suggestion` (optional, reference only): `Call (swing)` or `Put (swing)` with indicative swing horizon.
- If options are omitted, state why (liquidity/IV/macro-event risk).

Commodity direction requirement (report-level, mandatory):
- Add a `Commodity Direction Add-on` section covering:
  - Oil direction + relevant proxies/stocks
  - Gold direction + relevant proxies/stocks
  - Silver direction + relevant proxies/stocks
  - for each commodity, include:
    - current value + as-of timestamp + inline citation `[n]`
    - prior comparator and baseline comparator (with dates)
    - what changed and why
    - transmission to selected opportunities
    - net impact and horizon
    - invalidation trigger
  - explicit mapping to Long/Short opportunities
  - use this format:
    - `Oil Direction:`
    - `<signal/data lines>`
    - blank line
    - `Mapping:`
    - `<long mapping>`
    - `<short mapping>`

Required fields per opportunity:
- `Opportunity 1: <symbol> (<direction>, <horizon>)`
- `Stock Suggestion:` required
- `Options Suggestion:` optional
- `Setup:` entry, stop, targets, invalidation, risk/reward, sizing note
- `Thesis Type:` structural/cyclical/event-driven
- `Data Evidence (company):`
  - metric name
  - value + unit
  - period/date
  - prior comparator (`y/y`, `q/q`, or prior period)
  - why this metric matters for this recommendation now
  - direct source URL
- `Option Structure:` (required only when options suggestions are provided)
  - strategy (long call / long put / defined-risk spread)
  - expiry and strike(s) with rationale
  - premium/debit, max loss, breakeven
  - liquidity snapshot (volume/open interest/bid-ask) when available
  - implied-volatility context when available
  - greek risk profile (delta/gamma/theta/vega) when available
  - explicit exit logic
- `Price Structure & Technical Context:`
  - current price (timestamped)
  - key support levels and why they matter historically
  - key resistance levels and prior rejection/breakout behavior
  - drawdown context (from 52-week high and relevant prior highs)
  - historical buyer response at similar decline magnitudes
  - zone classification: buying zone / neutral zone / sell-into-strength zone
- `Macro Fit (with current data):`
  - include only channels with direct causal relevance to this opportunity
  - rates/real-yield channel (if relevant):
    - current value, prior value, direction
    - exact mechanism to financing/valuation
    - company-level impact path
  - inflation channel (if relevant):
    - current print, prior print, direction
    - policy reaction function implication
    - company-level demand/cost implication
  - USD channel (if relevant):
    - what moved and by how much
    - why it moved (if known from source)
    - company-level transmission (FX translation, input cost, demand mix, margins)
    - impact horizon
  - oil channel (if relevant to this specific opportunity):
    - what moved and why
    - transmission to inflation/costs/margins
    - impact on target setup
  - gold channel (if relevant to this specific opportunity):
    - what moved and why
    - real-yield and risk-hedging linkage
    - impact on target setup
  - silver channel (if relevant to this specific opportunity):
    - what moved and why
    - cyclical/industrial plus precious-metals linkage
    - impact on target setup
  - geopolitics channel (optional, only if materially relevant):
    - event/risk state
    - transmission to rates, commodities, risk appetite, and sector dispersion
    - impact on target setup
  - explicit net effect: Positive/Negative/Neutral
- `Why now:` dated catalyst path
- `Catalyst Calendar:`
  - next dated macro/company/geopolitical events tied to this setup
  - expected volatility window and execution caution
- `Reason:`
  - `Primary channel:` what moved
  - `Mechanism:` how that changes earnings/cost/valuation
  - `Why now:` what changed in this window
- `Causal Chain:` explicit sequence from data to trade action
- `Valuation Transmission:` why the multiple should re-rate/de-rate now
- `Key Risks Worth Noting:`
  - what can go wrong over the stated horizon
  - include at least one company-specific risk and one macro/market risk
  - include quantitative/observable trigger levels where possible
  - include direct mechanism from trigger to thesis damage
- `Trigger Grid:`
  - bull trigger(s) and action
  - bear trigger(s) and action
  - invalidation trigger(s) and action
- `Overturn Conditions:`
  - concrete conditions that invalidate/reverse the call
  - include observable thresholds or events when possible
- `Sizing and Correlation Note:`
  - sizing guidance by conviction and volatility
  - correlation overlap warning versus other recommended exposures
- `Conclusion:` mandatory 2-3 sentence professional conclusion
  - must reconcile fundamentals + price structure + macro alignment
  - must match stated horizon (`Short term` vs `Long term`)

## 5) News Coverage Summary (required for news mode)
- Analysis timezone used
- Window start (24h capture) and window end (cutoff)
- Window applied (default: fixed 24-hour capture ending at cutoff, unless user override)
- Coverage method
- Source groups scanned
- Relevant items found
- Deduplicated duplicates
- Coverage gaps
- Policy/Public-statement sweep:
  - leaders/officials scanned
  - official channels scanned (official sites, transcripts, verified official social accounts)
  - statement-driven items included
  - unverified items excluded
- Coverage Check:
  - Format rule (mandatory for each row):
    - `- <category>: <material items N or no material update in window>`
  - macro data releases: <...>
  - central-bank communication: <...>
  - fiscal/treasury/policy actions: <...>
  - geopolitics/sanctions/security: <...>
  - politician/public-official statements: <...>
  - rates/FX/commodities: <...>
  - equity/credit/volatility tape: <...>
- Delta Update:
  - final rescan timestamp
  - what changed since initial scan (or `no new material items`)

## 6) News Cards (required for news mode)
Repeat one card per relevant item:

```text
News 1: <headline> (<time + timezone>)
Fact Brief: <who did what, where, when, and key number(s)>
Comparator: <current vs prior/baseline with dates>
Reference: [n] <direct source URL>
Public-Signal Verification (if applicable):
- <speaker/role/channel/timestamp/verification status>
Impact on Market: Positive | Negative | Neutral
Reason:
- Primary channel: <policy/rates/inflation/commodities/liquidity/positioning>
- Mechanism: <explicit cause -> effect -> pricing/earnings/valuation path>
- Why now: <what changed in this 24h window versus prior>
Macro + Transmission Context:
- <indicator + current value + prior comparator + direction + horizon>
- <fact -> mechanism -> earnings/cost/valuation impact -> tradable implication>
Sector Impacted and Its Impact: <sector/subsector>
Impact: Positive | Negative | Neutral
Sector Reason:
- Sector exposure channel: <input-cost/demand/duration/FX/credit/regulation>
- Sector mechanism: <how this factor moves sector performance>
- Sector timing: <intraday / 1-4 weeks / multi-quarter>
- Sector metric: <one concrete metric/threshold with number and date>
Stocks: <symbols or />
Impact: Positive | Negative | Neutral
Stock Reason:
- Stock exposure channel: <company-specific channel>
- Stock mechanism: <how this changes earnings/cost/valuation for these names>
- Stock timing: <intraday / 1-4 weeks / multi-quarter>
- Stock metric: <one concrete metric/threshold with number and date>
Counter-risk / Invalidation:
- <what would reverse this card's directional read>
Recommendations: <actionable implication>
```

## 7) Topic Deep-Dive (for specific analysis requests)
- Research question and scope
- Data comparison block (current vs prior vs baseline with dates/units)
- Macro transmission analysis
- Fundamental/market evidence
- Counter-arguments and risks
- Professional conclusion

## 8) Logic Audit (internal quality check, include concise output when useful)
- No unsupported leap from data to conclusion.
- Every major claim has a source.
- Every recommendation includes invalidation and risk-control action.
- Any missing critical data is disclosed explicitly.

## 9) Monitoring Plan
- Key levels/events to track next.
- What changes the view.

## 10) References
Use numbered entries so users can match citations:
- [1] <title or short label>, <direct URL>
- [2] <title or short label>, <direct URL>
- [3] <title or short label>, <direct URL>

Do not output bare URLs without `[n]` numbering.

## 11) Risk Note
State analysis is probabilistic and not guaranteed.
