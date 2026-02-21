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


def has_placeholder_tokens(text: str) -> bool:
    # Reject unresolved template placeholders in final reports.
    return bool(re.search(r"<[^>\n]{2,}>", text))


def validate_news(text: str, errors: list[str]) -> None:
    for token in [
        "Coverage Summary",
        "Coverage Matrix",
        "Delta Update",
        "Policy/Public-statement sweep",
    ]:
        require(text, token, errors)

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
        pat = rf"(?i)^-\s*{re.escape(cat)}\s*\|\s*Scan:\s+.+\|\s*Covered:\s*(?:material items\s+\d+|no material update in window)\s*$"
        if count_lines(text, pat) < 1:
            errors.append(f"Missing required coverage-matrix row for `{cat}` with `Scan` and `Covered`")

    if count_lines(text, r"(?i)^-\s*purpose:") > 0 or count_lines(text, r"(?i)why it matters:") > 0:
        errors.append("Coverage Matrix must stay simple: only `Scan` and `Covered` fields are allowed")

    news_count = count_lines(text, r"^News\s+\d+\s*:")
    if news_count < 6:
        errors.append(f"Expected at least 6 news cards, found {news_count}")

    source_count = count_lines(text, r"^https?://")
    if source_count < 4:
        errors.append(f"Expected at least 4 source URLs, found {source_count}")

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

    if has_placeholder_tokens(text):
        errors.append("Template placeholders detected in news report (remove `<...>` tokens)")


def validate_recommendations(text: str, errors: list[str]) -> None:
    for token in [
        "Long",
        "Short",
        "Commodity Direction Add-on",
        "Oil Direction:",
        "Gold Direction:",
        "Silver Direction:",
        "Mapping:",
    ]:
        require(text, token, errors)

    opp_count = count_lines(text, r"^Opportunity\s+\d+\s*:")
    if opp_count < 2:
        errors.append(f"Expected at least 2 opportunities total, found {opp_count}")

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

    if has_placeholder_tokens(text):
        errors.append("Template placeholders detected in recommendations report (remove `<...>` tokens)")


def validate_research(text: str, errors: list[str]) -> None:
    required_sections = [
        r"^## Question Definition$",
        r"^## Indicator Comparison Block$",
        r"^## Macro Analysis",
        r"^## Upside Catalysts",
        r"^## Downside Catalysts",
        r"^## Cross-Asset Synthesis$",
        r"^## Counter-Arguments$",
        r"^## Professional Conclusion$",
        r"^## Sources$",
    ]
    for pat in required_sections:
        if count_lines(text, pat) < 1:
            errors.append(f"Missing research section matching `{pat}`")

    indicator_count = count_lines(text, r"^Indicator\s+\d+:")
    if indicator_count < 3:
        errors.append(f"Expected at least 3 indicators, found {indicator_count}")

    source_count = count_lines(text, r"^https?://")
    if source_count < 5:
        errors.append(f"Expected at least 5 source URLs, found {source_count}")

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
