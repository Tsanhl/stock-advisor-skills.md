#!/usr/bin/env python3
"""Validate trading-advisor markdown structure before PDF generation.

This is a strict format validator to reduce missing sections and logic gaps.
It checks required labels for:
- news mode
- recommendations mode
- research mode
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def count_lines(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def require(text: str, token: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"Missing required token: {token}")


def require_any(text: str, tokens: list[str], label: str, errors: list[str]) -> None:
    if not any(token in text for token in tokens):
        errors.append(f"Missing required token group `{label}`: expected one of {tokens}")


def has_placeholder_tokens(text: str) -> bool:
    # Reject unresolved template placeholders in final reports.
    return bool(re.search(r"<[^>\n]{2,}>", text))


REF_HEADING_RE = re.compile(r"(?im)^##\s*(?:\d+\)\s*)?(references|sources)\s*$")
REF_LINE_RE = re.compile(r"(?im)^\[(\d+)\]\s+.+https?://\S+.*$")
INLINE_CITE_RE = re.compile(r"\[(\d+)\]")
SOURCE_LABEL_RE = re.compile(r"(?im)^\s*(?:-\s*)?source:\s*")


def split_reference_block(text: str) -> tuple[str, str]:
    m = REF_HEADING_RE.search(text)
    if not m:
        return text, ""
    return text[: m.start()], text[m.end() :]


def validate_reference_system(
    text: str,
    errors: list[str],
    *,
    min_reference_lines: int,
    min_inline_cites: int,
    mode_name: str,
) -> None:
    body, ref_block = split_reference_block(text)

    if not REF_HEADING_RE.search(text):
        errors.append("Missing `## References` section (or equivalent numbered heading)")
        return

    ref_numbers = [int(n) for n in REF_LINE_RE.findall(ref_block)]
    if len(ref_numbers) < min_reference_lines:
        errors.append(
            f"{mode_name}: expected at least {min_reference_lines} numbered reference lines `[n] ... URL`, found {len(ref_numbers)}"
        )

    if SOURCE_LABEL_RE.search(body):
        errors.append(
            "Do not use standalone `Source:` lines in body sections; use inline `[n]` citations and map them in `References`"
        )

    inline_numbers = [int(n) for n in INLINE_CITE_RE.findall(body)]
    if len(inline_numbers) < min_inline_cites:
        errors.append(
            f"{mode_name}: expected at least {min_inline_cites} inline citation markers like `[1]`, found {len(inline_numbers)}"
        )

    unique_refs = sorted(set(ref_numbers))
    if unique_refs and unique_refs != list(range(1, unique_refs[-1] + 1)):
        errors.append("Reference numbering must be sequential from `[1]` without gaps")

    if len(unique_refs) != len(ref_numbers):
        errors.append("Reference numbering contains duplicates; each `[n]` entry in `References` must be unique")

    missing = sorted(set(inline_numbers) - set(ref_numbers))
    if missing:
        errors.append(f"Inline citation numbers missing from `References`: {missing}")

    unused = sorted(set(ref_numbers) - set(inline_numbers))
    if unused:
        errors.append(f"Unused reference entries in `References` (not cited in body): {unused}")


def validate_news(text: str, errors: list[str]) -> None:
    for token in [
        "Coverage Summary",
        "Coverage Check",
        "Delta Update",
        "Policy/Public-statement sweep",
    ]:
        require(text, token, errors)

    recency_pat = r"^Data recency note:\s+.*(?:\d{4}[-/]\d{2}[-/]\d{2}).*(?:\b(?:EST|EDT|UTC|GMT|CST|CDT|PST|PDT)\b|timezone|as-of).*$"
    if count_lines(text, recency_pat) < 1:
        errors.append("Missing/weak `Data recency note:` with date and timezone/as-of context")

    summary_patterns = [
        r"^-\s*Analysis timezone used:\s+.+$",
        r"^-\s*Window start \(24h capture\):\s+.+$",
        r"^-\s*Window end \(cutoff\):\s+.+$",
        r"^-\s*Window applied:.*24[- ]hour|^-\s*Window applied:.*24h",
        r"^-\s*Source groups scanned:\s+.+$",
        r"^-\s*Relevant items found:\s+\d+\s*$",
        r"^-\s*Deduplicated duplicates:\s+\d+\s*$",
        r"^-\s*Coverage gaps:\s+.+$",
    ]
    for pat in summary_patterns:
        if count_lines(text, pat) < 1:
            errors.append(f"Missing required coverage-summary field matching `{pat}`")

    sweep_patterns = [
        r"^-\s*Leaders/officials scanned:\s+.+$",
        r"^-\s*Official channels scanned:\s+.+$",
        r"^-\s*Statement-driven items included:\s+.+$",
        r"^-\s*Unverified items excluded:\s+.+$",
    ]
    for pat in sweep_patterns:
        if count_lines(text, pat) < 1:
            errors.append(f"Missing required policy-sweep field matching `{pat}`")

    categories = [
        "macro data releases",
        "central-bank communication",
        "fiscal/treasury/policy actions",
        "geopolitics/sanctions/security",
        "politician/public-official statements",
        "rates/FX/commodities",
        "equity/credit/volatility tape",
    ]
    for cat in categories:
        pat = rf"(?i)^-\s*{re.escape(cat)}\s*:\s*(?:material items\s+\d+|no material update in window).*$"
        if count_lines(text, pat) < 1:
            errors.append(
                f"Missing required Coverage Check row for `{cat}` in format "
                "`- <category>: <material items N or no material update in window>`"
            )

    news_count = count_lines(text, r"^News\s+\d+\s*:")
    if news_count < 6:
        errors.append(f"Expected at least 6 news cards, found {news_count}")

    label_patterns = [
        r"^Fact Brief:",
        r"^Comparator:",
        r"^Reference:",
        r"^Impact on Market:",
        r"^Reason:",
        r"^Macro \+ Transmission Context:",
        r"^Sector Reason:",
        r"^Stock Reason:",
        r"^Counter-risk / Invalidation:",
        r"^Recommendations:",
    ]
    for pat in label_patterns:
        n = count_lines(text, pat)
        if n < news_count:
            errors.append(f"Label count too low for pattern `{pat}`: {n} < {news_count}")

    reference_line_quality = count_lines(text, r"^Reference:\s+\[\d+\]\s+https?://\S+")
    if reference_line_quality < news_count:
        errors.append(
            f"Reference format too weak: {reference_line_quality} < {news_count} "
            "(each news card must use `Reference: [n] <URL>`)"
        )

    detail_patterns = [
        r"^-\s*Primary channel:",
        r"^-\s*Mechanism:",
        r"^-\s*Why now:",
        r"^-\s*Sector exposure channel:",
        r"^-\s*Sector mechanism:",
        r"^-\s*Sector timing:",
        r"^-\s*Sector metric:",
        r"^-\s*Stock exposure channel:",
        r"^-\s*Stock mechanism:",
        r"^-\s*Stock timing:",
        r"^-\s*Stock metric:",
    ]
    for pat in detail_patterns:
        n = count_lines(text, pat)
        if n < news_count:
            errors.append(f"Detail-field count too low for `{pat}`: {n} < {news_count}")

    mechanism_quality_patterns = [
        r"(?i)^-\s*Mechanism:\s+.*(?:because|via|through|drives|reduces|increases|raises|lowers|leads to|->).+$",
        r"(?i)^-\s*Sector mechanism:\s+.*(?:because|via|through|drives|reduces|increases|raises|lowers|leads to|->).+$",
        r"(?i)^-\s*Stock mechanism:\s+.*(?:because|via|through|drives|reduces|increases|raises|lowers|leads to|->).+$",
    ]
    for pat in mechanism_quality_patterns:
        n = count_lines(text, pat)
        if n < news_count:
            errors.append(f"Mechanism quality too weak for `{pat}`: {n} < {news_count}")

    comparator_quality = count_lines(
        text,
        r"(?i)^Comparator:\s+.*(?:vs|versus|compared with).*(?:\d{4}[-/]\d{2}[-/]\d{2}|[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}|Q[1-4]\s*\d{4}).+$",
    )
    if comparator_quality < news_count:
        errors.append(
            f"Comparator quality too weak: {comparator_quality} < {news_count} "
            "(must include explicit comparison and date/period)"
        )

    sector_metric_quality = count_lines(
        text,
        r"(?i)^-\s*Sector metric:\s+.*(?:\d|%|bps|x|\$|>|<|above|below).*$",
    )
    if sector_metric_quality < news_count:
        errors.append(
            f"Sector metric quality too weak: {sector_metric_quality} < {news_count} "
            "(must include at least one concrete number/threshold)"
        )

    stock_metric_quality = count_lines(
        text,
        r"(?i)^-\s*Stock metric:\s+.*(?:\d|%|bps|x|\$|>|<|above|below).*$",
    )
    if stock_metric_quality < news_count:
        errors.append(
            f"Stock metric quality too weak: {stock_metric_quality} < {news_count} "
            "(must include at least one concrete number/threshold)"
        )

    vague_mechanism_terms = re.compile(r"(?i)\b(supportive?|headwind|tailwind|risk-on|risk-off|favorable|unfavorable)\b")
    transmission_terms = re.compile(r"(?i)\b(because|via|through|due to|as .* rises|as .* falls|drives|reduces|increases|raises|lowers|leads to|->)\b")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith(("- Mechanism:", "- Sector mechanism:", "- Stock mechanism:")):
            if vague_mechanism_terms.search(line) and not transmission_terms.search(line):
                errors.append(
                    f"Weak mechanism line lacks transmission detail: `{line}` "
                    "(avoid vague support/headwind wording without explaining how)"
                )

    validate_reference_system(
        text,
        errors,
        min_reference_lines=max(4, news_count),
        min_inline_cites=max(6, news_count),
        mode_name="news",
    )

    if has_placeholder_tokens(text):
        errors.append("Template placeholders detected in news report (remove `<...>` tokens)")


def validate_recommendations(text: str, errors: list[str]) -> None:
    for token in ["Long", "Short", "Mapping:"]:
        require(text, token, errors)

    recency_pat = r"^Data recency note:\s+.*(?:\d{4}[-/]\d{2}[-/]\d{2}).*(?:\b(?:EST|EDT|UTC|GMT|CST|CDT|PST|PDT)\b|timezone|as-of).*$"
    if count_lines(text, recency_pat) < 1:
        errors.append("Missing/weak `Data recency note:` with date and timezone/as-of context")

    require_any(
        text,
        ["Commodity Analysis", "Commodity Direction Add-on"],
        "commodity section header",
        errors,
    )
    require_any(text, ["Oil Analysis:", "Oil Direction:"], "oil commodity subsection", errors)
    require_any(text, ["Gold Analysis:", "Gold Direction:"], "gold commodity subsection", errors)
    require_any(text, ["Silver Analysis:", "Silver Direction:"], "silver commodity subsection", errors)

    opp_count = count_lines(text, r"^Opportunity\s+\d+\s*:")
    if opp_count < 2:
        errors.append(f"Expected at least 2 opportunities total, found {opp_count}")

    require(text, "Cross-Asset Dashboard", errors)
    dashboard_indicator_count = count_lines(text, r"^Indicator\s+\d+\s*:")
    if dashboard_indicator_count < 3:
        errors.append(f"Cross-Asset Dashboard requires at least 3 indicators, found {dashboard_indicator_count}")

    dashboard_field_patterns = [
        r"^Current:",
        r"^Prior:",
        r"^Baseline:",
        r"^Interpretation:",
        r"^Why it matters now:",
    ]
    for pat in dashboard_field_patterns:
        n = count_lines(text, pat)
        if n < dashboard_indicator_count:
            errors.append(f"Dashboard field count too low for `{pat}`: {n} < {dashboard_indicator_count}")

    dashboard_current_quality = count_lines(
        text,
        r"(?i)^Current:\s+.*(?:\d{4}[-/]\d{2}[-/]\d{2}|[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}).*(?:\b(?:EST|EDT|UTC|GMT|CST|CDT|PST|PDT)\b|timezone|as-of).*$",
    )
    if dashboard_current_quality < dashboard_indicator_count:
        errors.append(
            f"Cross-Asset Dashboard `Current:` quality too weak: {dashboard_current_quality} < {dashboard_indicator_count} "
            "(must include value + date + timezone/as-of context)"
        )

    dashboard_prior_quality = count_lines(
        text,
        r"(?i)^Prior:\s+.*(?:\d{4}[-/]\d{2}[-/]\d{2}|[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}).*$",
    )
    if dashboard_prior_quality < dashboard_indicator_count:
        errors.append(
            f"Cross-Asset Dashboard `Prior:` quality too weak: {dashboard_prior_quality} < {dashboard_indicator_count} "
            "(must include prior comparator with date)"
        )

    total_current_lines = count_lines(text, r"(?i)^Current:\s+.+$")
    commodity_current_quality = count_lines(
        text,
        r"(?i)^Current:\s+.*(?:\d{4}[-/]\d{2}[-/]\d{2}|[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}).*(?:\b(?:EST|EDT|UTC|GMT|CST|CDT|PST|PDT)\b|as-of|context).*$",
    )
    if commodity_current_quality < total_current_lines:
        errors.append(
            "One or more `Current:` lines are missing clear as-of date/time context; "
            "all live market levels should include date + timezone/as-of markers"
        )

    label_patterns = [
        r"^Direction:",
        r"^Stock Suggestion:",
        r"^Entry Zone:",
        r"^Stop Loss:",
        r"^Target 1:",
        r"^Target 2:",
        r"^Invalidation Trigger:",
        r"^Time Horizon:",
        r"^Risk/Reward:",
        r"^Confidence:",
        r"^Thesis Type:",
        r"^Data Evidence \(company\):",
        r"^Price Structure and Technical Context:",
        r"^Macro Fit:",
        r"^Causal Chain:",
        r"^Valuation Transmission:",
        r"^Why Now:",
        r"^Catalyst Calendar:",
        r"^Key Risks Worth Noting:",
        r"^Trigger Grid:",
        r"^Overturn Conditions:",
        r"^Sizing and Correlation Note:",
        r"^Conclusion:",
    ]
    for pat in label_patterns:
        n = count_lines(text, pat)
        if n < opp_count:
            errors.append(f"Label count too low for pattern `{pat}`: {n} < {opp_count}")

    chain_quality = count_lines(text, r"^Causal Chain:\s+.+->.+->.+$")
    if chain_quality < opp_count:
        errors.append(f"Causal Chain quality too weak: {chain_quality} < {opp_count} (require at least two transmission arrows)")

    valuation_quality = count_lines(
        text,
        r"(?i)^Valuation Transmission:\s+.*(?:%|bps|x|times|multiple|yield|threshold|above|below|if|when).+$",
    )
    if valuation_quality < opp_count:
        errors.append(
            f"Valuation Transmission quality too weak: {valuation_quality} < {opp_count} (must include threshold/sensitivity language)"
        )

    validate_reference_system(
        text,
        errors,
        min_reference_lines=max(6, opp_count),
        min_inline_cites=max(6, opp_count),
        mode_name="recommendations",
    )

    if has_placeholder_tokens(text):
        errors.append("Template placeholders detected in recommendations report (remove `<...>` tokens)")


def validate_research(text: str, errors: list[str]) -> None:
    recency_pat = r"^-\s*Date cutoff for information:\s+.*(?:\d{4}[-/]\d{2}[-/]\d{2}).*(?:\b(?:EST|EDT|UTC|GMT|CST|CDT|PST|PDT)\b|timezone|as-of).*$"
    if count_lines(text, recency_pat) < 1:
        errors.append("Missing/weak `Date cutoff for information:` with date and timezone/as-of context")

    required_sections = [
        r"^## Question Definition$",
        r"^## Indicator Comparison Block$",
        r"^## Macro Analysis",
        r"^## Upside Catalysts",
        r"^## Downside Catalysts",
        r"^## Cross-Asset Synthesis$",
        r"^## Counter-Arguments$",
        r"^## Professional Conclusion$",
        r"^##\s*(?:\d+\)|\d+\.)?\s*(References|Sources)\s*$",
    ]
    for pat in required_sections:
        if count_lines(text, pat) < 1:
            errors.append(f"Missing research section matching `{pat}`")

    indicator_count = count_lines(text, r"^Indicator\s+\d+:")
    if indicator_count < 3:
        errors.append(f"Expected at least 3 indicators, found {indicator_count}")

    validate_reference_system(
        text,
        errors,
        min_reference_lines=5,
        min_inline_cites=max(5, indicator_count),
        mode_name="research",
    )

    if has_placeholder_tokens(text):
        errors.append("Template placeholders detected in research report (remove `<...>` tokens)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate report markdown structure.")
    parser.add_argument("--input", required=True, help="Path to markdown input")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["news", "recommendations", "research"],
        help="Validation profile",
    )
    args = parser.parse_args()

    path = Path(args.input).expanduser().resolve()
    if not path.exists():
        print(f"FAIL: file not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if args.mode == "news":
        validate_news(text, errors)
    elif args.mode == "recommendations":
        validate_recommendations(text, errors)
    else:
        validate_research(text, errors)

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
