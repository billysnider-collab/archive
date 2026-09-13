#!/usr/bin/env python3
"""Convert the 2026-09-13 OSINT brief markdown to a styled HTML page."""
import re, html, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026-09-13.md")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026-09-13.html")

TAGS = ["SPECULATION", "ASSESSMENT", "INFERENCE", "UNCONFIRMED", "ESTIMATE", "FACT"]
CONF = ["HIGH", "MODERATE", "LOW"]

def inline(s):
    s = html.escape(s)
    # tag pills — longest first to avoid partial matches
    for t in TAGS:
        s = re.sub(r"\*\*(%s(?:,?\s*%s)*)\*\*" % t,
                   lambda m: '<span class="tag tag-%s">%s</span>' % (t.lower(), m.group(1)),
                   s) if False else s
    # generic bold that is exactly a tag (optionally with confidence)
    def tagrep(m):
        inner = m.group(1)
        for t in TAGS:
            if inner == t or inner.startswith(t + ",") or inner.startswith(t + " "):
                return '<span class="pill pill-%s">%s</span>' % (t.lower(), inner)
        return "<strong>%s</strong>" % inner
    s = re.sub(r"\*\*(.+?)\*\*", tagrep, s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    # confidence bands
    for c in CONF:
        s = re.sub(r"\b(%s)\b" % c, r'<span class="conf conf-\1">\1</span>', s)
    return s

lines = open(SRC).read().split("\n")
out = []
i = 0
in_list = None
banner_lines = []

def close_list():
    global in_list
    if in_list:
        out.append("</%s>" % in_list)
        in_list = None

while i < len(lines):
    ln = lines[i].rstrip()
    if i < 6 and ln.startswith("**"):
        banner_lines.append(re.sub(r"\*\*", "", ln))
        i += 1
        continue
    if ln.strip() == "---":
        close_list(); out.append("<hr>"); i += 1; continue
    if ln.strip() == "":
        close_list(); i += 1; continue
    m = re.match(r"^## (\d+)\.\s+(.*)$", ln)
    if m:
        close_list()
        out.append('<h2><span class="secnum">%s</span> %s</h2>' % (m.group(1), inline(m.group(2))))
        i += 1; continue
    m = re.match(r"^### ([A-Z])\.\s+(.*)$", ln)
    if m:
        close_list()
        out.append('<h3><span class="secnum">%s</span> %s</h3>' % (m.group(1), inline(m.group(2))))
        i += 1; continue
    m = re.match(r"^### (.*)$", ln)
    if m:
        close_list(); out.append("<h3>%s</h3>" % inline(m.group(1))); i += 1; continue
    if re.match(r"^\|.*\|$", ln.strip()):
        close_list()
        rows = []
        while i < len(lines) and re.match(r"^\|.*\|$", lines[i].strip()):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        # drop separator row
        rows = [r for r in rows if not all(re.match(r"^:?-{2,}:?$", c) for c in r)]
        tbl = ["<table>"]
        for ri, r in enumerate(rows):
            tag = "th" if ri == 0 else "td"
            tbl.append("<tr>" + "".join("<%s>%s</%s>" % (tag, inline(c), tag) for c in r) + "</tr>")
        tbl.append("</table>")
        out.append("\n".join(tbl))
        continue
    m = re.match(r"^- (.*)$", ln)
    if m:
        if in_list != "ul": close_list(); out.append("<ul>"); in_list = "ul"
        out.append("<li>%s</li>" % inline(m.group(1))); i += 1; continue
    m = re.match(r"^\d+\.\s+(.*)$", ln)
    if m:
        if in_list != "ol": close_list(); out.append("<ol>"); in_list = "ol"
        out.append("<li>%s</li>" % inline(m.group(1))); i += 1; continue
    close_list()
    out.append("<p>%s</p>" % inline(ln))
    i += 1
close_list()
body = "\n".join(out)

banner = "\n".join("<div>%s</div>" % html.escape(b) for b in banner_lines)

page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Strategic Intelligence Brief — 13 September 2026</title>
<meta name="description" content="UNCLASSIFIED OSINT strategic intelligence brief for Sunday, 13 September 2026: Hormuz, East-West pipeline, Bab el-Mandeb, Ukraine, US-China summit, DPRK.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='4' y='9' width='24' height='17' rx='2' fill='%237c2e2a'/%3E%3Crect x='4' y='13' width='24' height='3' fill='%23f5f1e8'/%3E%3Crect x='13' y='6' width='6' height='4' rx='1' fill='%237c2e2a'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../archive-bar.css">
<script src="../archive-bar.js" defer></script>
<style>
  :root { --bg:#f5f1e8; --ink:#1c1916; --muted:#6b655c; --line:#d4cbb8; --accent:#7c2e2a; --amber:#b97a1f; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--ink); font-family:'Source Serif 4',Georgia,serif; font-size:16px; line-height:1.6; max-width:720px; margin:0 auto; padding:40px 24px 90px; }
  .classbanner { background:#1c1916; color:#f5f1e8; font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:.08em; padding:14px 18px; border-left:6px solid var(--amber); margin-bottom:30px; }
  .classbanner div:first-child { color:var(--amber); font-weight:600; }
  .backnav { font-family:'IBM Plex Mono',monospace; font-size:12px; margin-bottom:26px; }
  .backnav a { color:var(--muted); text-decoration:none; }
  .backnav a:hover { color:var(--accent); }
  h1.doc { font-family:'IBM Plex Mono',monospace; font-size:15px; letter-spacing:.1em; text-transform:uppercase; margin-bottom:4px; }
  .docdate { font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--muted); margin-bottom:26px; }
  h2 { font-size:21px; margin:38px 0 12px; padding-top:18px; border-top:2px solid var(--ink); }
  h3 { font-size:17px; margin:26px 0 8px; }
  .secnum { font-family:'IBM Plex Mono',monospace; color:var(--accent); margin-right:6px; }
  p { margin:0 0 12px; }
  ul, ol { margin:0 0 14px 22px; }
  li { margin-bottom:8px; }
  hr { border:none; border-top:1px solid var(--line); margin:26px 0; }
  table { width:100%; border-collapse:collapse; margin:14px 0 18px; font-size:13.5px; }
  th, td { text-align:left; padding:8px 10px; border:1px solid var(--line); vertical-align:top; }
  th { font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.06em; text-transform:uppercase; background:#ece5d3; }
  .pill { font-family:'IBM Plex Mono',monospace; font-size:10.5px; font-weight:600; letter-spacing:.06em; padding:2px 7px; border-radius:3px; white-space:nowrap; }
  .pill-fact { background:#1c1916; color:#f5f1e8; }
  .pill-assessment { background:#b97a1f; color:#fff; }
  .pill-inference { background:#3d5a80; color:#fff; }
  .pill-speculation { background:transparent; border:1px dashed var(--muted); color:var(--muted); }
  .pill-unconfirmed { background:transparent; border:1px solid var(--accent); color:var(--accent); }
  .pill-estimate { background:#ece5d3; border:1px solid var(--line); color:var(--ink); }
  .conf { font-family:'IBM Plex Mono',monospace; font-size:11px; font-weight:600; }
  .conf-HIGH { color:#2d6a4f; } .conf-MODERATE { color:#b97a1f; } .conf-LOW { color:var(--accent); }
  a { color:var(--accent); }
  footer { margin-top:56px; padding-top:18px; border-top:1px solid var(--line); font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--muted); text-align:center; }
</style>
</head>
<body>
<nav class="backnav"><a href="../index.html">&larr; Archive</a></nav>
<div class="classbanner">
__BANNER__
</div>
<h1 class="doc">Daily Strategic Intelligence Brief</h1>
<p class="docdate">Sunday, 13 September 2026 &middot; 0735 CDT (America/Chicago) &middot; UNCLASSIFIED // OSINT + INFERENCE</p>
__BODY__
<footer>archive &middot; unclassified osint brief &middot; 13 september 2026</footer>
</body>
</html>
"""
page = page.replace("__BANNER__", banner).replace("__BODY__", body)
open(DST, "w").write(page)
print("wrote", DST, len(page), "chars")
