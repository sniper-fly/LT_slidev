#!/usr/bin/env python3
"""findings.json + screenshots/ から人間向け HTML レポートを生成する。

使い方:
  generate_report_html.py <findings.json>

出力:
  findings.json と同じディレクトリに report.html を生成し、
  最終行に `report_html=<path>` を出力する。

レイアウト: 縦積みカード型 (slide ごと)。
  - 上部: タイムスタンプ・サマリ (critical/warning/note 件数)・全体所見・ジャンプナビ
  - 各スライド: 左にスクショ、右に findings + suggestedFix
"""

import json
import re
import sys
from html import escape
from pathlib import Path


SEVERITY_ORDER = {"critical": 0, "warning": 1, "note": 2}
SEVERITY_COLORS = {
    "critical": "#dc2626",
    "warning": "#f59e0b",
    "note": "#3b82f6",
    "ok": "#10b981",
}
SEVERITY_BG = {
    "critical": "rgba(220, 38, 38, 0.12)",
    "warning": "rgba(245, 158, 11, 0.12)",
    "note": "rgba(59, 130, 246, 0.12)",
    "ok": "rgba(16, 185, 129, 0.10)",
}

CSS = """
* { box-sizing: border-box; }
body {
  margin: 0;
  background: #0f172a;
  color: #e5e7eb;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", sans-serif;
  line-height: 1.5;
}
.container { max-width: 1400px; margin: 0 auto; padding: 24px; }

header { border-bottom: 1px solid #1f2937; padding-bottom: 16px; margin-bottom: 24px; }
h1 { margin: 0 0 4px 0; font-size: 24px; font-weight: 700; }
.meta { color: #94a3b8; font-size: 13px; margin-bottom: 16px; word-break: break-all; }

.summary-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }
.summary-box {
  flex: 1; min-width: 140px;
  border-radius: 8px; padding: 12px 16px;
  border: 1px solid rgba(255,255,255,0.08);
}
.summary-box .label { font-size: 12px; opacity: 0.7; }
.summary-box .count { font-size: 28px; font-weight: 700; }

.overall {
  background: rgba(255,255,255,0.04);
  border-left: 3px solid #3b82f6;
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 16px;
  white-space: pre-wrap;
}

.jumpnav {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-bottom: 16px; padding: 8px 0;
  border-top: 1px solid #1f2937; border-bottom: 1px solid #1f2937;
}
.jumpnav a {
  display: inline-block; padding: 4px 10px;
  border-radius: 4px; text-decoration: none;
  font-size: 12px; font-weight: 600;
  color: #e5e7eb; background: rgba(255,255,255,0.05);
  border: 1px solid transparent;
}
.jumpnav a:hover { background: rgba(255,255,255,0.10); }
.jumpnav a.has-critical { border-color: #dc2626; }
.jumpnav a.has-warning { border-color: #f59e0b; }
.jumpnav a.has-note { border-color: #3b82f6; }

.slide-card {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  gap: 20px;
  margin-bottom: 32px;
  padding: 16px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  scroll-margin-top: 12px;
}
.slide-card.no-findings { opacity: 0.65; }
.slide-card .left img {
  width: 100%; height: auto;
  border-radius: 6px; border: 1px solid rgba(255,255,255,0.08);
  display: block;
}
.slide-card .left .dims {
  margin-top: 6px; font-size: 11px; color: #64748b; text-align: center;
}

.slide-card .right { display: flex; flex-direction: column; gap: 10px; }
.slide-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.slide-header .num { font-size: 18px; font-weight: 700; }
.badge {
  display: inline-block;
  padding: 2px 10px; border-radius: 999px;
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.05em; text-transform: uppercase;
}

.finding {
  border-radius: 6px;
  padding: 10px 12px;
  border-left: 3px solid;
}
.finding .head {
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;
  margin-bottom: 6px;
}
.finding .dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
}
.finding .category { color: #94a3b8; }
.finding .human-flag {
  margin-left: auto;
  font-size: 10px; padding: 1px 6px; border-radius: 4px;
  background: rgba(167, 139, 250, 0.2); color: #c4b5fd;
}
.finding .issue { font-weight: 600; margin-bottom: 6px; }
.finding .evidence {
  font-size: 12px; color: #94a3b8; margin-bottom: 6px;
  white-space: pre-wrap;
}
.finding .fix-label {
  font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;
  margin-bottom: 2px;
}
.finding .fix {
  font-size: 12px; white-space: pre-wrap;
  background: rgba(0,0,0,0.25); border-radius: 4px; padding: 6px 8px;
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
}
.finding .fix code {
  background: rgba(255,255,255,0.08); padding: 1px 4px; border-radius: 3px;
}

.ok-msg { color: #10b981; font-size: 13px; opacity: 0.8; }

footer {
  margin-top: 32px; padding-top: 16px;
  border-top: 1px solid #1f2937;
  font-size: 12px; color: #64748b; text-align: center;
}
"""


def worst_severity(findings):
    if not findings:
        return "ok"
    return min(
        (f.get("severity", "note") for f in findings),
        key=lambda s: SEVERITY_ORDER.get(s, 99),
    )


def sort_findings(findings):
    return sorted(
        findings,
        key=lambda f: SEVERITY_ORDER.get(f.get("severity", "note"), 99),
    )


def render_inline_code(text: str) -> str:
    """`xxx` を <code>xxx</code> に置換 (text は escape 済み前提)。"""
    return re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", text)


def render_finding(f: dict) -> str:
    sev = f.get("severity", "note")
    cat = f.get("category", "")
    issue = escape(str(f.get("issue", "")))
    evidence = escape(str(f.get("evidence", "")))
    fix_raw = escape(str(f.get("suggestedFix", "")))
    fix = render_inline_code(fix_raw)
    needs_human = bool(f.get("requiresHumanDecision"))
    color = SEVERITY_COLORS.get(sev, "#6b7280")
    bg = SEVERITY_BG.get(sev, "rgba(255,255,255,0.04)")
    human_flag = '<span class="human-flag">要人間判断</span>' if needs_human else ""
    evidence_html = f'<div class="evidence">根拠: {evidence}</div>' if evidence else ""
    fix_html = (
        f'<div class="fix-label">修正案</div><div class="fix">{fix}</div>'
        if fix_raw else ""
    )
    return (
        f'<div class="finding" style="background: {bg}; border-left-color: {color};">'
        f'<div class="head">'
        f'<span class="dot" style="background: {color};"></span>'
        f'<span style="color: {color}; font-weight: 700;">{escape(sev)}</span>'
        f'<span class="category">/ {escape(cat)}</span>'
        f'{human_flag}'
        f'</div>'
        f'<div class="issue">{issue}</div>'
        f'{evidence_html}'
        f'{fix_html}'
        f'</div>'
    )


def render_badge(sev: str) -> str:
    color = SEVERITY_COLORS.get(sev, "#6b7280")
    bg = SEVERITY_BG.get(sev, "rgba(255,255,255,0.04)")
    label = sev.upper() if sev != "ok" else "OK"
    return f'<span class="badge" style="color: {color}; background: {bg};">{label}</span>'


def render_slide_card(slide_num: int, findings: list, screenshot_relpath: str) -> str:
    worst = worst_severity(findings)
    card_class = "slide-card" + (" no-findings" if not findings else "")
    findings_html = (
        "\n".join(render_finding(f) for f in sort_findings(findings))
        if findings
        else '<div class="ok-msg">指摘なし</div>'
    )
    return (
        f'<section id="slide-{slide_num:02d}" class="{card_class}">'
        f'<div class="left">'
        f'<img src="{escape(screenshot_relpath)}" alt="slide-{slide_num:02d}" />'
        f'<div class="dims">slide-{slide_num:02d}</div>'
        f'</div>'
        f'<div class="right">'
        f'<div class="slide-header">'
        f'<span class="num">slide-{slide_num:02d}</span>'
        f'{render_badge(worst)}'
        f'</div>'
        f'{findings_html}'
        f'</div>'
        f'</section>'
    )


def render_jumpnav(slide_numbers: list, by_slide: dict) -> str:
    items = []
    for n in slide_numbers:
        worst = worst_severity(by_slide.get(n, []))
        cls = f"has-{worst}" if worst != "ok" else ""
        items.append(f'<a href="#slide-{n:02d}" class="{cls}">{n:02d}</a>')
    return f'<nav class="jumpnav">{"".join(items)}</nav>'


def render_summary(summary: dict) -> str:
    crit = summary.get("criticalCount", 0)
    warn = summary.get("warningCount", 0)
    note = summary.get("noteCount", 0)
    boxes = [
        ("critical", crit, SEVERITY_COLORS["critical"]),
        ("warning", warn, SEVERITY_COLORS["warning"]),
        ("note", note, SEVERITY_COLORS["note"]),
    ]
    box_html = "".join(
        f'<div class="summary-box" style="border-color: {color};">'
        f'<div class="label" style="color: {color};">{label}</div>'
        f'<div class="count">{count}</div>'
        f'</div>'
        for label, count, color in boxes
    )
    overall = escape(str(summary.get("overallComment", "")))
    overall_html = f'<div class="overall">{overall}</div>' if overall else ""
    return f'<div class="summary-row">{box_html}</div>{overall_html}'


def main():
    if len(sys.argv) != 2:
        print("Usage: generate_report_html.py <findings.json>", file=sys.stderr)
        sys.exit(1)
    findings_path = Path(sys.argv[1]).resolve()
    if not findings_path.exists():
        print(f"Error: not found: {findings_path}", file=sys.stderr)
        sys.exit(1)

    review_dir = findings_path.parent
    screenshots_dir = review_dir / "screenshots"
    output_path = review_dir / "report.html"

    with findings_path.open(encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    findings = data.get("findings", [])

    by_slide = {}
    for f in findings:
        n = f.get("slideNumber")
        if n is None:
            continue
        by_slide.setdefault(int(n), []).append(f)

    slide_numbers = []
    if screenshots_dir.exists():
        for p in sorted(screenshots_dir.glob("*.png")):
            try:
                slide_numbers.append(int(p.stem))
            except ValueError:
                continue
    if not slide_numbers:
        slide_numbers = sorted(by_slide.keys())

    timestamp = review_dir.name
    rel_screenshots = "screenshots"

    cards_html = "\n".join(
        render_slide_card(n, by_slide.get(n, []), f"{rel_screenshots}/{n:02d}.png")
        for n in slide_numbers
    )

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<title>Slide Review Report ({escape(timestamp)})</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Slide Review Report</h1>
    <div class="meta">{escape(timestamp)} ・ {escape(str(review_dir))}</div>
    {render_summary(summary)}
    {render_jumpnav(slide_numbers, by_slide)}
  </header>
  <main>
    {cards_html}
  </main>
  <footer>
    生成: slide-review skill / generate_report_html.py
  </footer>
</div>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    print(f"report_html={output_path}")


if __name__ == "__main__":
    main()
