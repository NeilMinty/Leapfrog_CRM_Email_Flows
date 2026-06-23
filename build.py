#!/usr/bin/env python3
"""
Combines six Leapfrog HTML files into leapfrog-strategy.html.
The SOSTAC hub embeds five docs as srcdoc iframes.
"""

SRC = '/Users/neilminty/Downloads/'
LOCAL = '/Users/neilminty/focus-strategy-deck/'
OUT = LOCAL + 'leapfrog-strategy.html'

# Read source files
with open(SRC + 'leapfrog-sostac-v29.html', 'r', encoding='utf-8') as f:
    sostac = f.read()
with open(SRC + 'leapfrog-retention-winback-v1_7.html', 'r', encoding='utf-8') as f:
    retention = f.read()
with open(SRC + 'leapfrog-subscription-cro-v1.1.html', 'r', encoding='utf-8') as f:
    cro = f.read()
with open(SRC + 'FOCUS_Strategy_Deck (1).html', 'r', encoding='utf-8') as f:
    focus = f.read()
with open(LOCAL + 'leapfrog-briefs.html', 'r', encoding='utf-8') as f:
    briefs = f.read()

# Back button — injected before </body> in each deck
BACK_BTN = (
    '<div style="position:fixed; top:16px; left:50%; transform:translateX(-50%); z-index:9999;">\n'
    '  <button onclick="parent.closeAllDecks()" style="background:rgba(0,0,0,0.7); color:#fff; '
    'border:none; padding:7px 18px; font-size:11px; font-family:sans-serif; letter-spacing:0.1em; '
    'text-transform:uppercase; cursor:pointer; border-radius:20px;">&#8592; Back to Strategy</button>\n'
    '</div>'
)

def inject_back(html):
    """Inject floating back button unless the file already has its own closeAllDecks button."""
    if 'closeAllDecks' in html:
        return html
    return html.replace('</body>', BACK_BTN + '\n</body>', 1)

retention = inject_back(retention)
cro       = inject_back(cro)
focus     = inject_back(focus)
briefs    = inject_back(briefs)


def to_srcdoc(html):
    """Escape HTML content for use as an srcdoc attribute value."""
    return html.replace('&', '&amp;').replace('"', '&quot;')


# Build overlay divs
def overlay(id_, srcdoc_content):
    return (
        f'<div id="{id_}" style="display:none; position:fixed; inset:0; z-index:999;">\n'
        f'  <iframe srcdoc="{to_srcdoc(srcdoc_content)}" style="width:100%; height:100%; border:none;"></iframe>\n'
        f'</div>'
    )

overlay_retention = overlay('overlay-retention', retention)
overlay_cro       = overlay('overlay-cro', cro)
overlay_focus     = overlay('overlay-focus', focus)
overlay_briefs    = overlay('overlay-briefs', briefs)

# CSS additions (inserted before </style>)
CSS = """
.doc-link-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid var(--green-light);
  border-radius: 6px;
  padding: 10px 16px;
  margin: 12px 0;
  background: var(--green-pale);
  font-size: 13.5px;
}
.doc-link-row span { color: var(--green); font-weight: 600; }
.doc-link-row a {
  color: var(--green);
  font-weight: 700;
  text-decoration: none;
  font-size: 12px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: 1px solid var(--green);
  padding: 4px 12px;
  border-radius: 20px;
  white-space: nowrap;
  margin-left: 16px;
}
.doc-link-row a:hover { background: var(--green); color: #fff; }"""

# JS block (inserted before </body>)
JS = """<script>
function openDeck(id) {
  document.querySelectorAll('[id^="overlay-"]').forEach(el => el.style.display = 'none');
  document.getElementById(id).style.display = 'block';
  document.getElementById('sidebar').style.display = 'none';
  document.getElementById('main').style.display = 'none';
}
function closeAllDecks() {
  document.querySelectorAll('[id^="overlay-"]').forEach(el => el.style.display = 'none');
  document.getElementById('sidebar').style.display = '';
  document.getElementById('main').style.display = '';
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAllDecks(); });
</script>"""

# Nav links (inserted before </nav> in sidebar)
NAV_LINKS = (
    '    <div class="nav-section">Supporting Decks</div>\n'
    '    <a href="#" onclick="openDeck(\'overlay-retention\'); return false;">Retention &amp; Win-Back</a>\n'
    '    <a href="#" onclick="openDeck(\'overlay-cro\'); return false;">Subscription CRO</a>\n'
    '    <a href="#" onclick="openDeck(\'overlay-focus\'); return false;">FOCUS Strategy</a>\n'
    '    <a href="#" onclick="openDeck(\'overlay-briefs\'); return false;">Klaviyo &amp; Content Briefs</a>\n'
    '  </nav>'
)

# Inline callouts
CALLOUT_RETENTION = (
    '<div class="doc-link-row"><span>Retention &amp; Win-Back Architecture — full nine-flow deck</span>'
    '<a href="#" onclick="openDeck(\'overlay-retention\'); return false;">Open document &#8594;</a></div>'
)
CALLOUT_CRO = (
    '<div class="doc-link-row"><span>Subscription CRO Strategy — full three-phase roadmap</span>'
    '<a href="#" onclick="openDeck(\'overlay-cro\'); return false;">Open document &#8594;</a></div>'
)
CALLOUT_FOCUS = (
    '<div class="doc-link-row"><span>FOCUS Product Strategy H2 2026 — full document</span>'
    '<a href="#" onclick="openDeck(\'overlay-focus\'); return false;">Open document &#8594;</a></div>'
)

# --- Apply all transformations to SOSTAC ---

# 1. CSS → before </style>
assert '</style>' in sostac
sostac = sostac.replace('</style>', CSS + '\n</style>', 1)

# 2. Nav links → replace closing </nav> inside sidebar
assert '  </nav>\n</aside>' in sostac
sostac = sostac.replace('  </nav>\n</aside>', NAV_LINKS + '\n</aside>', 1)

# 3. Inline callouts → right after each section's opening tag
assert '<section id="retention-architecture">' in sostac
sostac = sostac.replace(
    '<section id="retention-architecture">',
    '<section id="retention-architecture">\n' + CALLOUT_RETENTION,
    1
)

assert '<section id="pdp-optimisation">' in sostac
sostac = sostac.replace(
    '<section id="pdp-optimisation">',
    '<section id="pdp-optimisation">\n' + CALLOUT_CRO,
    1
)

assert '<section id="focus-tactics">' in sostac
sostac = sostac.replace(
    '<section id="focus-tactics">',
    '<section id="focus-tactics">\n' + CALLOUT_FOCUS,
    1
)

# 4. Overlays + JS → before </body>
assert '</body>' in sostac
sostac = sostac.replace(
    '</body>',
    '\n' + overlay_retention + '\n' + overlay_cro + '\n' + overlay_focus + '\n' + overlay_briefs + '\n' + JS + '\n</body>',
    1
)

# Write output
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(sostac)

size_kb = len(sostac.encode('utf-8')) / 1024
print(f"Written: {OUT}")
print(f"File size: {size_kb:.1f} KB")
