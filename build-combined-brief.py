#!/usr/bin/env python3
"""
Combines leapfrog-retention-winback-v1_7.html and leapfrog-briefs.html
into a single standalone document: leapfrog-retention-briefs.html.
Hub page with two full-screen overlays. srcdoc pattern — no files merged.
"""

LOCAL = '/Users/neilminty/focus-strategy-deck/'
SRC   = '/Users/neilminty/Downloads/'
OUT   = LOCAL + 'leapfrog-retention-briefs.html'

with open(SRC + 'leapfrog-retention-winback-v1_7.html', 'r', encoding='utf-8') as f:
    retention = f.read()
with open(LOCAL + 'leapfrog-briefs.html', 'r', encoding='utf-8') as f:
    briefs = f.read()

BACK_BTN = (
    '<div style="position:fixed; top:16px; left:50%; transform:translateX(-50%); z-index:9999;">\n'
    '  <button onclick="parent.closeOverlay()" style="background:rgba(0,0,0,0.7); color:#fff; '
    'border:none; padding:7px 18px; font-size:11px; font-family:sans-serif; letter-spacing:0.1em; '
    'text-transform:uppercase; cursor:pointer; border-radius:20px;">&#8592; Back</button>\n'
    '</div>'
)

def inject_back(html):
    if 'closeOverlay' in html or 'closeAllDecks' in html:
        # Already has a back button — patch it to call closeOverlay instead
        return html.replace('parent.closeAllDecks()', 'parent.closeOverlay()')
    return html.replace('</body>', BACK_BTN + '\n</body>', 1)

def to_srcdoc(html):
    return html.replace('&', '&amp;').replace('"', '&quot;')

retention = inject_back(retention)
briefs    = inject_back(briefs)


HUB = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Leapfrog Remedies — Retention & Klaviyo Briefs</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600;700&display=swap');

  :root {{
    --green: #2d5a3d;
    --green-mid: #4a7c59;
    --green-light: #e4ede7;
    --cream: #f7f5f0;
    --white: #ffffff;
    --black: #1a1f1a;
    --grey: #6b6b5f;
    --grey-light: #e8e5de;
    --rule: #d4d0c8;
  }}

  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ height:100%; }}

  body {{
    font-family:'DM Sans', sans-serif;
    background:var(--cream);
    color:var(--black);
    min-height:100vh;
    display:flex;
    flex-direction:column;
  }}

  h1,h2,h3 {{ font-family:'Cormorant Garamond', serif; font-weight:700; }}

  /* ── Header ── */
  .hub-header {{
    background:var(--green);
    padding:52px 64px 44px;
  }}
  .hub-header .eyebrow {{
    font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase;
    color:rgba(255,255,255,0.5); font-weight:700; margin-bottom:14px;
  }}
  .hub-header h1 {{
    font-size:2.8rem; color:#fff; line-height:1.1; margin-bottom:12px;
  }}
  .hub-header .sub {{
    font-size:0.92rem; color:rgba(255,255,255,0.65); line-height:1.7;
  }}
  .hub-header .sub strong {{ color:rgba(255,255,255,0.9); }}
  .hub-meta {{
    display:flex; gap:32px; margin-top:24px; padding-top:24px;
    border-top:1px solid rgba(255,255,255,0.18); flex-wrap:wrap;
  }}
  .hub-meta-item {{ font-size:0.78rem; color:rgba(255,255,255,0.5); }}
  .hub-meta-item strong {{
    display:block; color:rgba(255,255,255,0.85);
    font-size:0.84rem; margin-bottom:2px;
  }}

  /* ── Cards ── */
  .hub-content {{
    padding:48px 64px 80px; flex:1;
  }}
  .card-grid {{
    display:grid; grid-template-columns:1fr 1fr; gap:28px;
    max-width:960px;
  }}
  .doc-card {{
    background:var(--white); border:1px solid var(--rule);
    border-top:4px solid var(--green-mid); border-radius:3px;
    padding:32px 36px; cursor:pointer;
    transition:box-shadow 0.2s, transform 0.2s;
    display:flex; flex-direction:column; gap:14px;
  }}
  .doc-card:hover {{
    box-shadow:0 6px 24px rgba(45,90,61,0.12);
    transform:translateY(-2px);
  }}
  .doc-card .card-num {{
    font-family:'Cormorant Garamond', serif;
    font-size:3rem; font-weight:700; color:var(--rule); line-height:1;
  }}
  .doc-card h2 {{ font-size:1.6rem; color:var(--black); line-height:1.2; }}
  .doc-card .card-tag {{
    font-size:0.6rem; font-weight:700; letter-spacing:0.16em;
    text-transform:uppercase; color:var(--green-mid);
  }}
  .doc-card p {{
    font-size:0.88rem; color:var(--grey); line-height:1.65; flex:1;
  }}
  .doc-card .open-btn {{
    display:inline-flex; align-items:center; gap:8px;
    margin-top:8px; font-size:0.78rem; font-weight:700;
    letter-spacing:0.1em; text-transform:uppercase;
    color:var(--green); border:1px solid var(--green);
    padding:8px 18px; border-radius:20px; width:fit-content;
    transition:background 0.15s, color 0.15s;
  }}
  .doc-card:hover .open-btn {{
    background:var(--green); color:#fff;
  }}

  /* ── Overlays ── */
  .overlay {{
    display:none; position:fixed; inset:0; z-index:999;
    background:#fff;
  }}
  .overlay iframe {{
    width:100%; height:100%; border:none; display:block;
  }}
</style>
</head>
<body>

<header class="hub-header">
  <div class="eyebrow">Leapfrog Remedies &middot; Personaify &middot; June 2026</div>
  <h1>Retention &amp; Briefs</h1>
  <p class="sub"><strong>Two documents.</strong> Retention &amp; Win-Back Architecture (nine-flow deck) and the Klaviyo &amp; Content Briefs synthesised from SOSTAC v29.</p>
  <div class="hub-meta">
    <div class="hub-meta-item"><strong>Source</strong>SOSTAC v29 — Working Draft, June 2026</div>
    <div class="hub-meta-item"><strong>Prepared by</strong>Personaify for Leapfrog Remedies</div>
    <div class="hub-meta-item"><strong>Status</strong>For review — not for circulation</div>
  </div>
</header>

<div class="hub-content">
  <div class="card-grid">

    <div class="doc-card" onclick="openOverlay('overlay-retention')">
      <div class="card-num">1</div>
      <div class="card-tag">Strategy deck</div>
      <h2>Retention &amp; Win-Back Architecture</h2>
      <p>Nine-flow Klaviyo retention system. Subscriber onboarding, churn prevention, win-back, pre-cancel save, December 2025 cohort re-engagement, and SMS test channel. Trigger logic, email sequences, and build prerequisites.</p>
      <div class="open-btn">Open document &rarr;</div>
    </div>

    <div class="doc-card" onclick="openOverlay('overlay-briefs')">
      <div class="card-num">2</div>
      <div class="card-tag">Strategic brief</div>
      <h2>Klaviyo &amp; Content Briefs</h2>
      <p>Audience segments, flow architecture, segmentation rules, suppression logic, tone and messaging principles, email KPIs. Content pillars, formats by pillar, audience-to-content mapping, GEO requirements, and open gaps.</p>
      <div class="open-btn">Open document &rarr;</div>
    </div>

  </div>
</div>

<div id="overlay-retention" class="overlay">
  <iframe srcdoc="{to_srcdoc(retention)}"></iframe>
</div>

<div id="overlay-briefs" class="overlay">
  <iframe srcdoc="{to_srcdoc(briefs)}"></iframe>
</div>

<script>
function openOverlay(id) {{
  document.querySelectorAll('.overlay').forEach(el => el.style.display = 'none');
  document.getElementById(id).style.display = 'block';
}}
function closeOverlay() {{
  document.querySelectorAll('.overlay').forEach(el => el.style.display = 'none');
}}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeOverlay(); }});
</script>

</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HUB)

size_kb = len(HUB.encode('utf-8')) / 1024
print(f"Written: {OUT}")
print(f"File size: {size_kb:.1f} KB")
