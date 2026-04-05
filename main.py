import streamlit as st
import math

st.set_page_config(
    page_title="Tylosin · Macrolide Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
#  GLOBAL STYLE — dark lab / scientific terminal
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:       #080c0a;
    --panel:    #0e1510;
    --card:     #111a13;
    --border:   #1e3322;
    --border2:  #2a4535;
    --text:     #c8d9c2;
    --muted:    #5a7560;
    --bright:   #e8f5e0;
    --green:    #4caf7d;
    --lime:     #a3e635;
    --amber:    #f59e0b;
    --red:      #ef5350;
    --cyan:     #26c6da;
    --purple:   #ce93d8;
    --scanline: rgba(0,255,80,.015);
}

/* ── base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"]  { background: transparent !important; }

/* scanline overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        var(--scanline) 0px, var(--scanline) 1px,
        transparent 1px, transparent 3px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: var(--panel) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { font-family: 'JetBrains Mono', monospace !important; }

/* ── radio nav in sidebar ── */
[data-testid="stRadio"] label {
    color: var(--muted) !important;
    font-size: .82rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: .25rem 0 !important;
    transition: color .15s;
}
[data-testid="stRadio"] label:hover { color: var(--green) !important; }
[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] { display: none; }

/* ── tabs ── */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .75rem !important;
    letter-spacing: .06em !important;
    padding: .5rem 1rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--lime) !important;
    border-bottom: 2px solid var(--lime) !important;
}
[data-testid="stTabPanel"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 4px 4px 4px !important;
    padding: 1.2rem !important;
}

/* ── hr ── */
hr { border-color: var(--border) !important; }

/* ── selectbox ── */
[data-testid="stSelectbox"] > div {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .8rem !important;
    border-radius: 3px !important;
}

/* ── components ── */
.terminal-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: .65rem;
    color: var(--muted);
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-bottom: .3rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.terminal-header::before {
    content: '●';
    color: var(--green);
    font-size: .7rem;
}

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--bright);
    margin: 0 0 1rem;
    line-height: 1.2;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    margin-bottom: .9rem;
    position: relative;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--green);
    border-radius: 4px 0 0 4px;
    opacity: .6;
}
.card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    letter-spacing: .12em;
    color: var(--green);
    text-transform: uppercase;
    margin: 0 0 .8rem;
    padding-left: .4rem;
}

.kv-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .5rem;
}
.kv-item {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: .6rem .8rem;
}
.kv-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: .6rem;
    color: var(--muted);
    letter-spacing: .1em;
    text-transform: uppercase;
}
.kv-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: .88rem;
    color: var(--bright);
    margin-top: .15rem;
}

.stereo-badge {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    padding: .25rem .6rem;
    border-radius: 3px;
    margin: .2rem .2rem .2rem 0;
}
.sb-R  { background: rgba(76,175,125,.12); color: #4caf7d; border: 1px solid rgba(76,175,125,.35); }
.sb-S  { background: rgba(38,198,218,.1);  color: #26c6da; border: 1px solid rgba(38,198,218,.3); }

.smiles-terminal {
    background: #050805;
    border: 1px solid var(--border2);
    border-radius: 4px;
    padding: .9rem 1.1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .7rem;
    line-height: 1.8;
    color: #4a6650;
    word-break: break-all;
    position: relative;
}
.smiles-terminal::before {
    content: '$ SMILES';
    display: block;
    color: var(--green);
    font-size: .65rem;
    letter-spacing: .1em;
    margin-bottom: .5rem;
    opacity: .7;
}

.big-number {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    color: var(--lime);
    line-height: 1;
}
.big-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: .62rem;
    color: var(--muted);
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-top: .2rem;
}

.sugar-block {
    border: 1px solid var(--border2);
    border-radius: 4px;
    padding: .8rem 1rem;
    margin-bottom: .6rem;
    position: relative;
    overflow: hidden;
}
.sugar-block::after {
    content: attr(data-glyph);
    position: absolute;
    right: .8rem; top: .5rem;
    font-size: 1.4rem;
    opacity: .12;
}
.sugar-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: var(--bright);
    margin-bottom: .25rem;
}
.sugar-detail {
    font-family: 'JetBrains Mono', monospace;
    font-size: .7rem;
    color: var(--muted);
    line-height: 1.6;
}

.step-item {
    display: flex;
    gap: .8rem;
    padding: .55rem 0;
    border-bottom: 1px solid var(--border);
    font-size: .84rem;
    color: var(--text);
}
.step-item:last-child { border-bottom: none; }
.step-num {
    font-family: 'JetBrains Mono', monospace;
    color: var(--lime);
    font-size: .7rem;
    min-width: 24px;
    padding-top: .05rem;
}

.nav-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem;
    color: var(--muted);
    padding: .35rem .7rem;
    border-radius: 3px;
    border: 1px solid var(--border);
    display: block;
    margin-bottom: .3rem;
    cursor: pointer;
    transition: all .15s;
}

table.rtable {
    width: 100%;
    border-collapse: collapse;
    font-size: .8rem;
    font-family: 'JetBrains Mono', monospace;
}
table.rtable th {
    text-align: left;
    padding: .4rem .5rem;
    color: var(--muted);
    font-size: .65rem;
    letter-spacing: .08em;
    border-bottom: 1px solid var(--border2);
    background: transparent;
    font-weight: 400;
}
table.rtable td {
    padding: .4rem .5rem;
    border-bottom: 1px solid var(--border);
    color: var(--text);
    background: transparent;
}
table.rtable tr:last-child td { border-bottom: none; }

.note { font-size: .73rem; color: var(--muted); font-style: italic; margin-top: .4rem; }

/* section fade-in */
@keyframes fadeSlide {
    from { opacity:0; transform: translateY(8px); }
    to   { opacity:1; transform: translateY(0); }
}
.fadein { animation: fadeSlide .35s ease both; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════

SMILES_TYLOSIN = ("CC[C@H]1OC(=O)C[C@@H](O)[C@H](C)[C@@H]"
                  "(O[C@@H]2O[C@H](C)[C@@H](O[C@H]3C[C@@](C)(O)"
                  "[C@@H](O)[C@H](C)O3)[C@@H]([C@H]2O)N(C)C)"
                  "[C@@H](CC=O)C[C@@H](C)C(=O)/C=C/C(C)=C/"
                  "[C@@H]1CO[C@@H]4O[C@H](C)[C@@H](O)[C@@H](OC)[C@H]4OC")

# 22 stereocentres from InChI
STEREOCENTRES = [
    ("C4",  "R", "Macrolide ring"),
    ("C5",  "S", "Macrolide ring"),
    ("C6",  "R", "Macrolide ring — OH"),
    ("C7",  "S", "Macrolide ring"),
    ("C8",  "R", "Mycaminose junction"),
    ("C9",  "R", "Macrolide ring"),
    ("C10", "S", "Macrolide ring"),
    ("C11", "S", "Macrolide ring"),
    ("C13", "S", "Macrolide ring"),
    ("C15", "R", "Macrolide ring"),
    ("C16", "R", "Mycinose junction"),
    ("C17", "S", "Sugar C1′″ mycinose"),
    ("C18", "S", "Sugar mycinose"),
    ("C19", "S", "Sugar mycinose"),
    ("C20", "S", "Sugar mycinose"),
    ("C21", "S", "Sugar mycinose C6′″"),
    ("C1′", "S", "Mycaminose anomeric"),
    ("C2′", "R", "Mycaminose — NMe₂"),
    ("C3′", "S", "Mycaminose"),
    ("C4′", "R", "Mycaminose"),
    ("C1″", "S", "Mycarose anomeric"),
    ("C4″", "R", "Mycarose quaternary"),
]

R_count = sum(1 for _, c, _ in STEREOCENTRES if c == "R")
S_count = sum(1 for _, c, _ in STEREOCENTRES if c == "S")
n_centres = len(STEREOCENTRES)
max_stereo = 2 ** n_centres  # 2^22 = 4,194,304


# ══════════════════════════════════════════════
#  SVG DRAWING
# ══════════════════════════════════════════════

GREEN  = "#4caf7d"
LIME   = "#a3e635"
CYAN   = "#26c6da"
AMBER  = "#f59e0b"
PURPLE = "#ce93d8"
RED    = "#ef5350"
BG_SVG = "#080c0a"
CARD_S = "#111a13"
BORD_S = "#1e3322"
FG_SVG = "#7a9e80"
DIM_S  = "#2a4535"
BRIGHT = "#c8d9c2"


def svg_macrolide_2d():
    """
    Schematic 2D of tylosin:
    - 16-membered lactone ring drawn as a polygon
    - 3 sugar stubs hanging off
    - key functional groups labelled
    - stereocentre markers
    """
    W, H = 640, 400

    def T(x,y,t,col=FG_SVG,sz=10,anchor="middle",bold=False,italic=False):
        fw = "bold" if bold else "normal"
        fs_tag = "font-style='italic'" if italic else ""
        return (f"<text x='{x:.1f}' y='{y:.1f}' text-anchor='{anchor}' "
                f"font-size='{sz}' fill='{col}' font-weight='{fw}' {fs_tag} "
                f"font-family='JetBrains Mono,monospace'>{t}</text>")

    def L(x1,y1,x2,y2,col=FG_SVG,w=1.6,dash=""):
        d = f"stroke-dasharray='{dash}'" if dash else ""
        return (f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
                f"stroke='{col}' stroke-width='{w}' stroke-linecap='round' {d}/>")

    els = [f"<svg viewBox='0 0 {W} {H}' xmlns='http://www.w3.org/2000/svg' "
           f"style='width:100%;background:{BG_SVG};border-radius:4px;border:1px solid {BORD_S};'>"]

    # ── 16-membered ring as irregular hexadecagon ──
    # Place centre at (285, 195), vary radii per quadrant for visual interest
    cx, cy = 288, 200
    # 16 vertices, slight angular offsets to look natural
    base_r = 105
    # angle offsets per segment to make lactone ring look more natural
    angles = [i * (2*math.pi/16) - math.pi/2 for i in range(16)]
    r_mods = [1.0, 0.97, 1.0, 1.02, 1.0, 0.98, 1.0, 1.02,
              1.0, 0.97, 1.0, 1.02, 0.98, 1.0, 1.02, 0.98]
    ring = [(cx + base_r * r_mods[i] * math.cos(angles[i]),
             cy + base_r * r_mods[i] * math.sin(angles[i]))
            for i in range(16)]

    # Ring bonds — alternate thick/thin for unsaturation hints
    double_bonds = {10, 12}  # C11=C12, C13=C14 (conjugated diene in tylosin)
    for i in range(16):
        a, b = ring[i], ring[(i+1)%16]
        col = LIME if i in double_bonds else FG_SVG
        w = 2.0 if i in double_bonds else 1.5
        els.append(L(*a, *b, col, w))
        if i in double_bonds:
            # inner parallel double bond
            mx = (a[0]+b[0])/2 - cx; my = (a[1]+b[1])/2 - cy
            nm = math.hypot(mx,my) or 1
            ox, oy = mx/nm*4, my/nm*4
            frac = 0.7
            ax2 = (a[0]+b[0])/2 + (a[0]-(a[0]+b[0])/2)*frac - ox
            ay2 = (a[1]+b[1])/2 + (a[1]-(a[1]+b[1])/2)*frac - oy
            bx2 = (a[0]+b[0])/2 + (b[0]-(a[0]+b[0])/2)*frac - ox
            by2 = (a[1]+b[1])/2 + (b[1]-(a[1]+b[1])/2)*frac - oy
            els.append(L(ax2, ay2, bx2, by2, LIME, 1.1))

    # ── Ester bond label (C1=O ring closure) ──
    # vertex 0 is roughly top; ester is between v0 and v15
    lx = (ring[0][0]+ring[15][0])/2
    ly = (ring[0][1]+ring[15][1])/2
    els.append(T(lx-18, ly-8, "O", AMBER, 10))
    els.append(T(lx-2,  ly+14, "C=O", AMBER, 9, italic=True))

    # ── Stereocentre dots on ring vertices ──
    for i, (label, config, _) in enumerate(STEREOCENTRES[:10]):
        vi = (i * 2) % 16  # spread around ring
        px, py = ring[vi]
        col = GREEN if config == "R" else CYAN
        els.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='5' "
                   f"fill='{col}' opacity='.25' stroke='{col}' stroke-width='1.2'/>")
        els.append(T(px, py+3.5, config[0], col, 7, "middle", True))

    # ── Sugar moieties as hexagonal stubs ──
    def draw_sugar(cx2, cy2, name, colour, pos_label, chirals, r2=28):
        # small hexagon
        vv = [(cx2 + r2*math.cos(math.pi/3*i - math.pi/6),
               cy2 + r2*math.sin(math.pi/3*i - math.pi/6)) for i in range(6)]
        pts = " ".join(f"{x:.1f},{y:.1f}" for x,y in vv)
        els.append(f"<polygon points='{pts}' fill='{colour}' opacity='.08' "
                   f"stroke='{colour}' stroke-width='1.4'/>")
        els.append(T(cx2, cy2-5, name, colour, 9, "middle", True))
        els.append(T(cx2, cy2+8, chirals, colour, 7))
        els.append(T(cx2, cy2+20, pos_label, DIM_S, 8))

    # Mycaminose at C5 (vertex ~4) — left upper
    mc_attach = ring[4]
    mcx, mcy = mc_attach[0]-68, mc_attach[1]-20
    els.append(L(*mc_attach, mcx+28, mcy, GREEN, 1.4, "4 2"))
    draw_sugar(mcx, mcy, "Mycaminose", GREEN, "C5-O", "5×stereoC", r2=30)

    # Mycarose at C5 disaccharide (hangs off mycaminose)
    mrx, mry = mcx-65, mcy-30
    els.append(L(mcx-30, mcy, mrx+28, mry, CYAN, 1.4, "4 2"))
    draw_sugar(mrx, mry, "Mycarose", CYAN, "→C4′", "4×stereoC", r2=26)

    # Mycinose at C14 (vertex ~11) — right lower
    my_attach = ring[11]
    myx, myy = my_attach[0]+72, my_attach[1]+10
    els.append(L(*my_attach, myx-28, myy, PURPLE, 1.4, "4 2"))
    draw_sugar(myx, myy, "Mycinose", PURPLE, "C14-O", "5×stereoC", r2=30)

    # ── Functional group labels on ring ──
    # Aldehyde at C6 (vertex 5)
    av = ring[5]
    els.append(L(*av, av[0]+28, av[1]-22, AMBER, 1.3))
    els.append(T(av[0]+34, av[1]-28, "CHO", AMBER, 9))
    els.append(T(av[0]+34, av[1]-17, "aldehyde", DIM_S, 7, italic=True))

    # Ketone at C9 (vertex ~8)
    kv = ring[8]
    els.append(L(*kv, kv[0]-30, kv[1]+22, AMBER, 1.3))
    els.append(T(kv[0]-36, kv[1]+32, "C=O", AMBER, 9))

    # OH groups at C4, C10
    for vi2, lbl in [(3,"OH"),(9,"OH"),(14,"OH")]:
        pv = ring[vi2]
        ox = pv[0] + 22 * math.cos(angles[vi2])
        oy = pv[1] + 22 * math.sin(angles[vi2])
        els.append(L(*pv, ox, oy, FG_SVG, 1.2))
        els.append(T(ox, oy+3, lbl, FG_SVG, 9))

    # ── Ring atom markers (C numbering on selected vertices) ──
    labels_at = {0:"C1",2:"C3",5:"C6",7:"C8",10:"C11",12:"C13",15:"C16"}
    for vi2, lbl in labels_at.items():
        px, py = ring[vi2]
        ang = angles[vi2]
        lox = px + 16 * math.cos(ang)
        loy = py + 16 * math.sin(ang)
        els.append(T(lox, loy+3, lbl, DIM_S, 8))

    # ── Centre ring label ──
    els.append(T(cx, cy-10, "16-membered", DIM_S, 9, italic=True))
    els.append(T(cx, cy+6,  "Lactone Ring", DIM_S, 9, italic=True))
    els.append(T(cx, cy+22, "Tylonolide", FG_SVG, 8))

    # ── Legend ──
    lx2, ly2 = 10, H-44
    for col2, lbl2 in [(GREEN,"R-config"),(CYAN,"S-config"),(LIME,"C=C"),(AMBER,"C=O"),(PURPLE,"Mycinose"),(FG_SVG,"C-O")]:
        els.append(f"<rect x='{lx2}' y='{ly2}' width='9' height='9' rx='2' fill='{col2}' opacity='.5'/>")
        els.append(T(lx2+13, ly2+8, lbl2, col2, 8, "start"))
        lx2 += 72

    els.append(T(W-8, H-6, "Tylosin A · C46H77NO17 · MW 916.1 g/mol", DIM_S, 8, "end"))
    els.append("</svg>")
    return "\n".join(els)


def svg_stereo_map():
    """
    A radial stereocentre map — all 22 centres shown in a clock-like diagram.
    """
    W, H = 560, 380
    cx, cy = W//2, H//2
    r_inner, r_outer = 65, 140

    els = [f"<svg viewBox='0 0 {W} {H}' xmlns='http://www.w3.org/2000/svg' "
           f"style='width:100%;background:{BG_SVG};border-radius:4px;border:1px solid {BORD_S};'>"]

    # Inner ring label
    els.append(f"<circle cx='{cx}' cy='{cy}' r='{r_inner}' fill='none' "
               f"stroke='{BORD_S}' stroke-width='1' stroke-dasharray='4 3'/>")
    els.append(f"<circle cx='{cx}' cy='{cy}' r='{r_outer}' fill='none' "
               f"stroke='{BORD_S}' stroke-width='1' stroke-dasharray='2 4'/>")
    els.append(f"<text x='{cx}' y='{cy-8}' text-anchor='middle' font-size='11' "
               f"fill='{FG_SVG}' font-family='JetBrains Mono,monospace'>22</text>")
    els.append(f"<text x='{cx}' y='{cy+8}' text-anchor='middle' font-size='8' "
               f"fill='{DIM_S}' font-family='JetBrains Mono,monospace'>stereocentres</text>")
    els.append(f"<text x='{cx}' y='{cy+22}' text-anchor='middle' font-size='7' "
               f"fill='{DIM_S}' font-family='JetBrains Mono,monospace'>tylosin A</text>")

    n = len(STEREOCENTRES)
    for i, (lbl, config, region) in enumerate(STEREOCENTRES):
        ang = (2 * math.pi * i / n) - math.pi / 2
        # spoke
        ix = cx + r_inner * math.cos(ang)
        iy = cy + r_inner * math.sin(ang)
        ox2 = cx + r_outer * math.cos(ang)
        oy2 = cy + r_outer * math.sin(ang)
        col = GREEN if config == "R" else CYAN
        els.append(f"<line x1='{ix:.1f}' y1='{iy:.1f}' x2='{ox2:.1f}' y2='{oy2:.1f}' "
                   f"stroke='{col}' stroke-width='1.3' opacity='.4'/>")
        # node
        els.append(f"<circle cx='{ox2:.1f}' cy='{oy2:.1f}' r='13' "
                   f"fill='{col}' opacity='.12' stroke='{col}' stroke-width='1.2'/>")
        els.append(f"<text x='{ox2:.1f}' y='{oy2-3:.1f}' text-anchor='middle' "
                   f"font-size='7' fill='{col}' font-weight='bold' "
                   f"font-family='JetBrains Mono,monospace'>{lbl}</text>")
        els.append(f"<text x='{ox2:.1f}' y='{oy2+7:.1f}' text-anchor='middle' "
                   f"font-size='7.5' fill='{col}' font-weight='bold' "
                   f"font-family='JetBrains Mono,monospace'>({config})</text>")

    # Legend
    for xx, col2, lbl2 in [(10,GREEN,f"R × {R_count}"),(90,CYAN,f"S × {S_count}")]:
        els.append(f"<circle cx='{xx+5}' cy='{H-14}' r='5' fill='{col2}' opacity='.5'/>")
        els.append(f"<text x='{xx+14}' y='{H-10}' font-size='9' fill='{col2}' "
                   f"font-family='JetBrains Mono,monospace'>{lbl2}</text>")

    els.append(f"<text x='{W-8}' y='{H-6}' text-anchor='end' font-size='8' "
               f"fill='{DIM_S}' font-family='JetBrains Mono,monospace'>all defined · single natural enantiomer</text>")
    els.append("</svg>")
    return "\n".join(els)


def svg_sugar_detail(sugar_name):
    """Draw a simple hexose pyranose ring for each sugar with labels."""
    W, H = 380, 220
    col_map = {"Mycaminose": GREEN, "Mycarose": CYAN, "Mycinose": PURPLE}
    col = col_map.get(sugar_name, GREEN)

    details = {
        "Mycaminose": {
            "full": "β-D-Mycaminose",
            "formula": "3-(dimethylamino)-3,6-dideoxy-D-mannose",
            "attach": "C5-OH of aglycone",
            "role": "Essential for ribosome binding",
            "subs": {0: "NMe₂", 1: "OH", 2: "H", 3: "CH₃", 4: "O", 5: ""},
        },
        "Mycarose": {
            "full": "L-Mycarose",
            "formula": "2,3,6-trideoxy-3-C-methyl-L-ribo-hexose",
            "attach": "C4′ of mycaminose",
            "role": "Stabilises PTC interaction",
            "subs": {0: "OH", 1: "CMe", 2: "H", 3: "CH₃", 4: "O", 5: ""},
        },
        "Mycinose": {
            "full": "D-Mycinose (bis-OMe)",
            "formula": "2,3-di-O-methyl-6-deoxy-D-allose",
            "attach": "C14-OH of aglycone",
            "role": "Unique to tylosin — domain II rRNA contact",
            "subs": {0: "OMe", 1: "OMe", 2: "H", 3: "CH₃", 4: "O", 5: ""},
        },
    }
    d = details[sugar_name]

    els = [f"<svg viewBox='0 0 {W} {H}' xmlns='http://www.w3.org/2000/svg' "
           f"style='width:100%;background:{BG_SVG};border-radius:4px;border:1px solid {BORD_S};'>"]

    # pyranose ring (chair-like flat hexagon)
    rx, ry = 160, 115
    rr = 52
    verts2 = [(rx + rr*math.cos(math.pi/3*i - math.pi/6),
               ry + rr*math.sin(math.pi/3*i - math.pi/6)) for i in range(6)]
    pts2 = " ".join(f"{x:.1f},{y:.1f}" for x,y in verts2)
    els.append(f"<polygon points='{pts2}' fill='{col}' opacity='.06' "
               f"stroke='{col}' stroke-width='1.6'/>")

    subs = d["subs"]
    for i2, (x2,y2) in enumerate(verts2):
        ang2 = math.pi/3*i2 - math.pi/6
        sx = x2 + 20*math.cos(ang2)
        sy = y2 + 20*math.sin(ang2)
        lbl2 = subs.get(i2,"")
        if lbl2:
            els.append(f"<line x1='{x2:.1f}' y1='{y2:.1f}' x2='{sx:.1f}' y2='{sy:.1f}' "
                       f"stroke='{col}' stroke-width='1.2' opacity='.5'/>")
            els.append(f"<text x='{sx:.1f}' y='{sy+4:.1f}' text-anchor='middle' "
                       f"font-size='9' fill='{col}' font-family='JetBrains Mono,monospace'>{lbl2}</text>")
        # numbering
        nx = x2 - 8*math.cos(ang2)
        ny = y2 - 8*math.sin(ang2)
        els.append(f"<text x='{nx:.1f}' y='{ny+3:.1f}' text-anchor='middle' "
                   f"font-size='7' fill='{DIM_S}' font-family='JetBrains Mono,monospace'>{i2+1}</text>")

    # Text info panel
    tx = 250
    els.append(f"<text x='{tx}' y='30' text-anchor='middle' font-size='13' fill='{col}' "
               f"font-weight='bold' font-family='JetBrains Mono,monospace'>{sugar_name}</text>")
    els.append(f"<text x='{tx}' y='48' text-anchor='middle' font-size='8' fill='{FG_SVG}' "
               f"font-family='JetBrains Mono,monospace'>{d['full']}</text>")

    for j2, (k2, v2) in enumerate([("Formula", d["formula"]),
                                    ("Attached", d["attach"]),
                                    ("Role", d["role"])]):
        yy = 80 + j2*36
        els.append(f"<text x='{tx}' y='{yy}' text-anchor='middle' font-size='7' fill='{DIM_S}' "
                   f"font-family='JetBrains Mono,monospace'>{k2.upper()}</text>")
        # Wrap long text
        words = v2.split()
        line2 = ""
        ly_offset = yy+12
        for w2 in words:
            test = (line2+" "+w2).strip()
            if len(test)*5.2 > 150:
                els.append(f"<text x='{tx}' y='{ly_offset}' text-anchor='middle' font-size='8.5' "
                           f"fill='{BRIGHT}' font-family='JetBrains Mono,monospace'>{line2}</text>")
                line2 = w2; ly_offset += 12
            else:
                line2 = test
        if line2:
            els.append(f"<text x='{tx}' y='{ly_offset}' text-anchor='middle' font-size='8.5' "
                       f"fill='{BRIGHT}' font-family='JetBrains Mono,monospace'>{line2}</text>")

    els.append(f"<text x='8' y='{H-6}' font-size='8' fill='{DIM_S}' "
               f"font-family='JetBrains Mono,monospace'>deoxy hexose moiety · pyranose form</text>")
    els.append("</svg>")
    return "\n".join(els)


# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.6rem 0 1rem">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.62rem;
                  color:#2a4535;letter-spacing:.18em;margin-bottom:.5rem">
        MACROLIDE LAB · v1.0
      </div>
      <div style="font-family:'DM Serif Display',serif;font-size:1.6rem;
                  color:#c8d9c2;line-height:1.1">
        Tylosin A
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.68rem;
                  color:#5a7560;margin-top:.3rem">
        C46H77NO17 · MW 916.1
      </div>
    </div>
    <hr style="border-color:#1e3322;margin:.5rem 0 1rem">
    """, unsafe_allow_html=True)

    page = st.radio("Navigate", [
        "⬡  Overview",
        "⬢  2D Structure",
        "◉  Stereocentre Map",
        "⬟  Sugar Moieties",
        "≡  SMILES & Data",
    ], label_visibility="collapsed")

    st.markdown("""
    <hr style="border-color:#1e3322;margin:1rem 0">
    <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#2a4535;line-height:1.8">
      <div style="color:#4caf7d">SOURCE</div>
      Streptomyces fradiae<br>
      <div style="color:#4caf7d;margin-top:.5rem">CLASS</div>
      16-membered macrolide<br>
      <div style="color:#4caf7d;margin-top:.5rem">TARGET</div>
      50S ribosomal subunit<br>
      <div style="color:#4caf7d;margin-top:.5rem">USE</div>
      Veterinary antibiotic<br>
      <div style="color:#4caf7d;margin-top:.5rem">CAS</div>
      1401-69-0
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  PAGES
# ══════════════════════════════════════════════

if page == "⬡  Overview":
    st.markdown('<div class="fadein">', unsafe_allow_html=True)

    # Top banner
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0a120c 0%,#0e1d10 60%,#080c0a 100%);
                border:1px solid #1e3322;border-radius:4px;
                padding:1.6rem 2rem;margin-bottom:1.2rem;position:relative;overflow:hidden">
      <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;
                  border-radius:50%;background:#4caf7d;opacity:.04;pointer-events:none"></div>
      <div class="terminal-header">TYLOSIN A · STEREOCHEMISTRY PROFILE</div>
      <div style="font-family:'DM Serif Display',serif;font-size:2.4rem;
                  color:#e8f5e0;line-height:1.1;margin:.3rem 0">
        Macrolide Antibiotic
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#5a7560;margin-top:.4rem">
        (4R,5S,6R,7S,8R,9R,10S,11S,13S,15R,16R) · natural product · single enantiomer
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4, c5 = st.columns(5)
    stats = [
        ("22", "Stereocentres"),
        (f"2²²", "Max Isomers"),
        ("4.2M", "Theoretical stereoisomers"),
        ("3", "Sugar moieties"),
        ("916.1", "MW g/mol"),
    ]
    for col, (num, label) in zip([c1,c2,c3,c4,c5], stats):
        with col:
            st.markdown(f"""<div style="background:#0e1510;border:1px solid #1e3322;
                border-radius:4px;padding:1rem;text-align:center">
              <div class="big-number" style="font-size:1.9rem">{num}</div>
              <div class="big-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div class="section-title">What is Tylosin?</div>', unsafe_allow_html=True)
        st.markdown("""<div class="card">
          <div class="card-title">Origin &amp; Structure</div>
          <p style="font-size:.86rem;color:#c8d9c2;line-height:1.7">
          Tylosin A is a <b>16-membered macrolide antibiotic</b> produced naturally by 
          <i>Streptomyces fradiae</i> via a type-I polyketide synthase (PKS). 
          The core structure is the <b>tylonolide aglycone</b> — a 16-membered lactone ring 
          bearing a characteristic <b>aldehyde at C6</b> and a conjugated diene (C11=C12–C13=C14).
          </p>
          <p style="font-size:.86rem;color:#c8d9c2;line-height:1.7;margin-top:.6rem">
          Three deoxyhexose sugars are appended: <b>D-mycaminose</b> at C5 
          (with a disaccharide partner <b>L-mycarose</b>), and <b>mycinose</b> at C14. 
          This sugar decoration is key to ribosomal binding and potency.
          </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
          <div class="card-title">Mode of Action</div>
          <p style="font-size:.86rem;color:#c8d9c2;line-height:1.7">
          Tylosin binds in the <b>polypeptide exit tunnel</b> of the 50S ribosomal subunit, 
          blocking nascent peptide egress. The C6-aldehyde forms a <b>reversible covalent imine bond</b> 
          with A2062 of 23S rRNA — unique among macrolides. The mycarose moiety 
          hydrogen-bonds with G2540, and the mycaminose dimethylamino group makes 
          electrostatic contacts at the tunnel wall.
          </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
          <div class="card-title">Stereoisomer Count</div>
          <div style="display:flex;gap:1.5rem;align-items:flex-end;margin-bottom:.6rem">
            <div>
              <div class="big-number">2²²</div>
              <div class="big-label">theoretical max</div>
            </div>
            <div style="font-size:.9rem;color:#5a7560;padding-bottom:.3rem">= 4,194,304 possible stereoisomers</div>
          </div>
          <p style="font-size:.82rem;color:#5a7560;line-height:1.6">
          In reality, only <b>one stereoisomer</b> exists in nature — the biosynthetic machinery 
          of the PKS enforces absolute stereocontrol at all 22 centres. No synthetic 
          racemic mixture is possible in practice; total synthesis would require explicit 
          stereocontrol at each centre.
          </p>
          <div style="margin-top:.8rem;display:flex;flex-wrap:wrap;gap:.3rem">
        """ + "".join(
            f'<span class="stereo-badge {"sb-R" if c=="R" else "sb-S"}">{l} ({c})</span>'
            for l, c, _ in STEREOCENTRES
        ) + """</div></div>""", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">Key Properties</div>', unsafe_allow_html=True)
        st.markdown("""<div class="kv-grid">
          <div class="kv-item"><div class="kv-label">Formula</div><div class="kv-value">C₄₆H₇₇NO₁₇</div></div>
          <div class="kv-item"><div class="kv-label">MW</div><div class="kv-value">916.10 g/mol</div></div>
          <div class="kv-item"><div class="kv-label">CAS</div><div class="kv-value">1401-69-0</div></div>
          <div class="kv-item"><div class="kv-label">Ring size</div><div class="kv-value">16-membered</div></div>
          <div class="kv-item"><div class="kv-label">Stereocentres</div><div class="kv-value">22 (all defined)</div></div>
          <div class="kv-item"><div class="kv-label">R centres</div><div class="kv-value" style="color:#4caf7d">"""+str(R_count)+"""</div></div>
          <div class="kv-item"><div class="kv-label">S centres</div><div class="kv-value" style="color:#26c6da">"""+str(S_count)+"""</div></div>
          <div class="kv-item"><div class="kv-label">Sugars</div><div class="kv-value">3</div></div>
          <div class="kv-item"><div class="kv-label">pKa (amine)</div><div class="kv-value">~7.7</div></div>
          <div class="kv-item"><div class="kv-label">logP</div><div class="kv-value">1.63</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-title" style="font-size:1.1rem">R vs S Distribution</p>', unsafe_allow_html=True)

        # Bar chart in SVG
        total = R_count + S_count
        r_pct = R_count / total
        bw = 180
        st.markdown(f"""
        <div style="background:#0e1510;border:1px solid #1e3322;border-radius:4px;padding:1rem">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a7560;margin-bottom:.6rem">
            CONFIG DISTRIBUTION
          </div>
          <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:.5rem">
            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#4caf7d;min-width:24px">R</div>
            <div style="flex:1;background:#1e3322;border-radius:2px;height:16px;position:relative">
              <div style="width:{r_pct*100:.1f}%;background:#4caf7d;height:100%;border-radius:2px;opacity:.7"></div>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#4caf7d">{R_count} ({r_pct*100:.0f}%)</div>
          </div>
          <div style="display:flex;align-items:center;gap:.8rem">
            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#26c6da;min-width:24px">S</div>
            <div style="flex:1;background:#1e3322;border-radius:2px;height:16px;position:relative">
              <div style="width:{(1-r_pct)*100:.1f}%;background:#26c6da;height:100%;border-radius:2px;opacity:.7"></div>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#26c6da">{S_count} ({(1-r_pct)*100:.0f}%)</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="card">
          <div class="card-title">Variants</div>
          <table class="rtable">
            <tr><th>Name</th><th>Difference</th><th>MW</th></tr>
            <tr><td style="color:#a3e635">Tylosin A</td><td>parent</td><td>916.1</td></tr>
            <tr><td>Tylosin B</td><td>−mycarose</td><td>772.0</td></tr>
            <tr><td>Tylosin C</td><td>−OMe on mycinose</td><td>902.1</td></tr>
            <tr><td>Tylosin D</td><td>C20 reduced</td><td>918.1</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "⬢  2D Structure":
    st.markdown('<div class="fadein">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">2D Structural Schematic</div>', unsafe_allow_html=True)

    col_svg, col_info = st.columns([3, 2], gap="large")

    with col_svg:
        st.markdown(svg_macrolide_2d(), unsafe_allow_html=True)
        st.markdown('<p class="note" style="text-align:center">Schematic — ring proportions stylised for clarity. '
                    'Stereocentres shown as R (green) / S (cyan) nodes.</p>', unsafe_allow_html=True)

    with col_info:
        st.markdown("""<div class="card">
          <div class="card-title">Reading the Structure</div>
          <div class="step-item">
            <span class="step-num">01</span>
            <span>The 16-membered <b>lactone ring</b> (tylonolide) is the macrolide backbone. 
            The ester C=O closes the ring between C1 and C16.</span>
          </div>
          <div class="step-item">
            <span class="step-num">02</span>
            <span>The <b>conjugated diene</b> C11=C12–C13=C14 (shown in lime) is a 
            pharmacophoric feature not found in 14-membered macrolides.</span>
          </div>
          <div class="step-item">
            <span class="step-num">03</span>
            <span>The <b>C6-aldehyde</b> (CHO, amber) forms a reversible Schiff base 
            with A2062 of 23S rRNA — unique binding mechanism.</span>
          </div>
          <div class="step-item">
            <span class="step-num">04</span>
            <span>Three <b>deoxyhexose sugars</b> (dashed lines) contribute additional 
            stereocentres and ribosomal contacts.</span>
          </div>
          <div class="step-item">
            <span class="step-num">05</span>
            <span>Wedge / dash bonds are not shown at scale — see the Stereocentre Map 
            for all 22 configurations.</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
          <div class="card-title">Functional Groups</div>
          <table class="rtable">
            <tr><th>Group</th><th>Position</th><th>Role</th></tr>
            <tr><td style="color:#f59e0b">–CHO</td><td>C6</td><td>Covalent rRNA bond</td></tr>
            <tr><td style="color:#f59e0b">–C=O</td><td>C9</td><td>Ketone</td></tr>
            <tr><td style="color:#a3e635">C=C–C=C</td><td>C11–C14</td><td>Diene, conj.</td></tr>
            <tr><td style="color:#c8d9c2">–OH ×3</td><td>C4,C10,C15</td><td>H-bonding</td></tr>
            <tr><td style="color:#c8d9c2">–OC=O</td><td>C1–C16</td><td>Lactone ester</td></tr>
            <tr><td style="color:#ce93d8">–OMe ×2</td><td>mycinose</td><td>Unique to tylosin</td></tr>
            <tr><td style="color:#4caf7d">–NMe₂</td><td>mycaminose</td><td>Ribosome anchor</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "◉  Stereocentre Map":
    st.markdown('<div class="fadein">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Stereocentre Map</div>', unsafe_allow_html=True)

    col_map, col_table = st.columns([5, 4], gap="large")

    with col_map:
        st.markdown(svg_stereo_map(), unsafe_allow_html=True)

        # CIP explanation
        st.markdown("""<div class="card" style="margin-top:.8rem">
          <div class="card-title">CIP Priority Rules</div>
          <div class="step-item"><span class="step-num">1</span>
            <span>Assign priorities by atomic number at each substituent (O &gt; N &gt; C &gt; H)</span></div>
          <div class="step-item"><span class="step-num">2</span>
            <span>For ties, proceed outward along substituent chains (phantom atoms for double bonds)</span></div>
          <div class="step-item"><span class="step-num">3</span>
            <span>Orient lowest priority group away from viewer</span></div>
          <div class="step-item"><span class="step-num">4</span>
            <span>Trace 1→2→3: <b style="color:#4caf7d">clockwise = R</b>, 
            <b style="color:#26c6da">anticlockwise = S</b></span></div>
        </div>""", unsafe_allow_html=True)

    with col_table:
        st.markdown("""<div class="card">
          <div class="card-title">All 22 Defined Stereocentres</div>
          <table class="rtable">
            <tr><th>#</th><th>Centre</th><th>Config</th><th>Region</th></tr>""" +
            "".join(
                f"<tr><td style='color:#2a4535'>{i+1}</td>"
                f"<td style='font-weight:bold'>{l}</td>"
                f"<td><span class='stereo-badge {'sb-R' if c=='R' else 'sb-S'}' style='padding:.1rem .4rem;font-size:.65rem'>({c})</span></td>"
                f"<td style='color:#5a7560;font-size:.72rem'>{r}</td></tr>"
                for i,(l,c,r) in enumerate(STEREOCENTRES)
            ) +
            "</table></div>", unsafe_allow_html=True)

        st.markdown(f"""<div class="card">
          <div class="card-title">Stereoisomer Arithmetic</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.78rem;
                      color:#5a7560;line-height:2">
            n (chiral centres) = <span style="color:#a3e635">22</span><br>
            Max stereoisomers  = 2ⁿ = <span style="color:#a3e635">4,194,304</span><br>
            Diastereomers possible = 2ⁿ⁻¹ = <span style="color:#26c6da">2,097,152</span><br>
            Enantiomers of tylosin = <span style="color:#4caf7d">1 pair</span><br>
            <br>
            <span style="color:#2a4535">// In nature: only 1 stereoisomer<br>
            // PKS enforces absolute stereocontrol<br>
            // No meso forms (no internal symmetry)</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "⬟  Sugar Moieties":
    st.markdown('<div class="fadein">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Deoxyhexose Sugar Moieties</div>', unsafe_allow_html=True)

    sugar_sel = st.selectbox("Select sugar", ["Mycaminose", "Mycarose", "Mycinose"])

    col_draw, col_info = st.columns([3, 2], gap="large")

    with col_draw:
        st.markdown(svg_sugar_detail(sugar_sel), unsafe_allow_html=True)

    with col_info:
        sugar_data = {
            "Mycaminose": {
                "colour": GREEN,
                "class": "3,6-Dideoxyhexose",
                "config": "D-series · β-glycosidic",
                "stereos": 5,
                "attach_pos": "C5-OH of tylonolide",
                "partner": "L-mycarose at C4′",
                "unique": "NMe₂ at C3 — key contact with A2058/A2059 of 23S rRNA",
                "centres": [("C1′","S"),("C2′","R"),("C3′","S"),("C4′","R"),("C5′","S")],
            },
            "Mycarose": {
                "colour": CYAN,
                "class": "2,3,6-Trideoxyhexose",
                "config": "L-series · α-glycosidic",
                "stereos": 4,
                "attach_pos": "C4′ of mycaminose",
                "partner": "Disaccharide partner",
                "unique": "C3-methyl branch; no O2/O3 — unusually lipophilic, enhances PTC contact",
                "centres": [("C1″","S"),("C2″","—"),("C3″","—"),("C4″","R")],
            },
            "Mycinose": {
                "colour": PURPLE,
                "class": "Bis-O-methyl-6-deoxyhexose",
                "config": "D-series · β-glycosidic",
                "stereos": 5,
                "attach_pos": "C14-OH of tylonolide",
                "partner": "No partner (monosaccharide)",
                "unique": "Two OMe groups (C2,C3) — unique to tylosin; contacts domain II of 23S rRNA",
                "centres": [("C1‴","S"),("C2‴","S"),("C3‴","S"),("C4‴","S"),("C5‴","R")],
            },
        }
        sd = sugar_data[sugar_sel]
        col = sd["colour"]

        st.markdown(f"""<div class="card" style="border-left-color:{col}">
          <div class="card-title" style="color:{col}">{sugar_sel.upper()}</div>
          <div class="kv-grid">
            <div class="kv-item"><div class="kv-label">Class</div><div class="kv-value" style="font-size:.78rem">{sd['class']}</div></div>
            <div class="kv-item"><div class="kv-label">Config</div><div class="kv-value" style="font-size:.78rem">{sd['config']}</div></div>
            <div class="kv-item"><div class="kv-label">Stereocentres</div><div class="kv-value" style="color:{col}">{sd['stereos']}</div></div>
            <div class="kv-item"><div class="kv-label">Attached at</div><div class="kv-value" style="font-size:.75rem">{sd['attach_pos']}</div></div>
          </div>
          <div style="margin-top:.8rem;font-size:.82rem;color:#c8d9c2;line-height:1.6">
            <b style="color:{col}">Pharmacological role:</b><br>{sd['unique']}
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="card" style="border-left-color:{col}">
          <div class="card-title" style="color:{col}">STEREOCENTRES IN {sugar_sel.upper()}</div>
          <table class="rtable">
            <tr><th>Centre</th><th>Config</th></tr>
            {"".join(
              f"<tr><td>{l}</td><td><span class='stereo-badge {'sb-R' if c=='R' else 'sb-S'}' style='padding:.1rem .4rem;font-size:.65rem'>({c})</span></td></tr>"
              if c in ("R","S") else f"<tr><td>{l}</td><td style='color:#2a4535'>—</td></tr>"
              for l,c in sd['centres']
            )}
          </table>
        </div>""", unsafe_allow_html=True)

        # All 3 sugars summary
        st.markdown("""<div class="card">
          <div class="card-title">SUGAR SUMMARY</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#5a7560;line-height:2">
            <span style="color:#4caf7d">Mycaminose</span> → 5 stereocentres<br>
            <span style="color:#26c6da">Mycarose</span>   → 4 stereocentres<br>
            <span style="color:#ce93d8">Mycinose</span>   → 5 stereocentres<br>
            <br>
            Sugars subtotal: <span style="color:#a3e635">14</span> of 22 centres<br>
            Aglycone ring:   <span style="color:#a3e635">8</span> of 22 centres
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "≡  SMILES & Data":
    st.markdown('<div class="fadein">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">SMILES, InChI &amp; Raw Data</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("""<div class="card">
          <div class="card-title">CANONICAL SMILES (Tylosin A)</div>""",
          unsafe_allow_html=True)
        st.markdown(f"""<div class="smiles-terminal">
          <span style="color:#4caf7d">CC</span>[C@H]1OC(=O)C<span style="color:#26c6da">[C@@H]</span>(O)
          <span style="color:#26c6da">[C@H]</span>(C)<span style="color:#26c6da">[C@@H]</span>
          (O<span style="color:#4caf7d">[C@@H]2O[C@H](C)</span>
          <span style="color:#26c6da">[C@@H]</span>(O<span style="color:#ce93d8">[C@H]3C
          [C@@](C)(O)[C@@H](O)[C@H](C)O3</span>)
          <span style="color:#26c6da">[C@@H]</span>([C@H]2O)N(C)C)
          <span style="color:#26c6da">[C@@H]</span>(CC=O)C
          <span style="color:#26c6da">[C@@H]</span>(C)C(=O)
          <span style="color:#a3e635">/C=C/C(C)=C/</span>
          <span style="color:#26c6da">[C@@H]</span>1CO
          <span style="color:#ce93d8">[C@@H]4O[C@H](C)[C@@H](O)[C@@H](OC)[C@H]4OC</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div class="card">
          <div class="card-title">SMILES LEGEND</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;line-height:2">
            <span style="color:#26c6da">[C@@H] / [C@H]</span> — stereospecified carbon<br>
            <span style="color:#a3e635">/C=C/</span> — E (trans) double bond<br>
            <span style="color:#4caf7d">O[C@@H]...O</span> — mycaminose sugar ring<br>
            <span style="color:#ce93d8">[C@H]3...O3</span> — mycinose sugar ring<br>
            <span style="color:#c8d9c2">N(C)C</span> — dimethylamino group<br>
            <span style="color:#f59e0b">CC=O</span> — pendant aldehyde (C6)
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
          <div class="card-title">DOUBLE BOND GEOMETRY</div>
          <table class="rtable">
            <tr><th>Bond</th><th>Geometry</th><th>Notation</th></tr>
            <tr><td>C11=C12</td><td style="color:#a3e635">E (trans)</td><td>/C=C/</td></tr>
            <tr><td>C13=C14</td><td style="color:#a3e635">E (trans)</td><td>C(C)=C/</td></tr>
          </table>
          <p class="note" style="margin-top:.6rem">Conjugated E,E-diene — rigid planar system in the macrolide scaffold</p>
        </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown("""<div class="card">
          <div class="card-title">InChI KEY</div>
          <div style="background:#050805;border:1px solid #1e3322;border-radius:3px;
                      padding:.7rem 1rem;font-family:'JetBrains Mono',monospace;
                      font-size:.72rem;color:#4a6650;word-break:break-all">
            WBPYTXDJUQJLPQ-VMXQISHHSA-N
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
          <div class="card-title">PHYSICOCHEMICAL DATA</div>
          <table class="rtable">
            <tr><th>Property</th><th>Value</th></tr>
            <tr><td>Molecular formula</td><td>C₄₆H₇₇NO₁₇</td></tr>
            <tr><td>Exact mass</td><td>915.513 Da</td></tr>
            <tr><td>MW</td><td>916.10 g/mol</td></tr>
            <tr><td>H-bond donors</td><td>6</td></tr>
            <tr><td>H-bond acceptors</td><td>18</td></tr>
            <tr><td>Rotatable bonds</td><td>10</td></tr>
            <tr><td>logP (XLogP)</td><td>1.63</td></tr>
            <tr><td>pKa (NMe₂)</td><td>~7.7</td></tr>
            <tr><td>TPSA</td><td>267 Å²</td></tr>
            <tr><td>Stereocentres</td><td>22 (all defined)</td></tr>
            <tr><td>R centres</td><td style="color:#4caf7d">"""+str(R_count)+"""</td></tr>
            <tr><td>S centres</td><td style="color:#26c6da">"""+str(S_count)+"""</td></tr>
            <tr><td>E double bonds</td><td>2</td></tr>
            <tr><td>PubChem CID</td><td>5280440</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="card">
          <div class="card-title">STEREOCENTRE SEQUENCE (InChI /t notation)</div>
          <div style="background:#050805;border:1px solid #1e3322;border-radius:3px;
                      padding:.7rem 1rem;font-family:'JetBrains Mono',monospace;
                      font-size:.65rem;color:#4a6650;line-height:1.8;word-break:break-all">
            <span style="color:#2a4535">// /t notation from InChI</span><br>
            t24<span style="color:#ef5350">-</span>,25<span style="color:#4caf7d">+</span>,
            26<span style="color:#ef5350">-</span>,27<span style="color:#ef5350">-</span>,
            28<span style="color:#4caf7d">+</span>,29<span style="color:#4caf7d">+</span>,
            30<span style="color:#ef5350">-</span>,32<span style="color:#ef5350">-</span>,
            33<span style="color:#ef5350">-</span>,35<span style="color:#4caf7d">+</span>,
            36<span style="color:#ef5350">-</span>,37<span style="color:#ef5350">-</span>,
            38<span style="color:#ef5350">-</span>,39<span style="color:#ef5350">-</span>,
            40<span style="color:#ef5350">-</span>,41<span style="color:#ef5350">-</span>,
            42<span style="color:#ef5350">-</span>,43<span style="color:#4caf7d">+</span>,
            44<span style="color:#4caf7d">+</span>,45<span style="color:#ef5350">-</span>,
            46<span style="color:#ef5350">-</span><br><br>
            <span style="color:#4caf7d">+ = R</span> &nbsp; <span style="color:#ef5350">- = S</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="border-top:1px solid #1e3322;margin-top:2rem;padding-top:.8rem;
            font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#2a4535;
            display:flex;justify-content:space-between;flex-wrap:wrap;gap:.4rem">
  <span>TYLOSIN A STEREOCHEMISTRY EXPLORER · Pure SVG · No RDKit · No external APIs</span>
  <span>C46H77NO17 · CID 5280440 · CAS 1401-69-0</span>
</div>
""", unsafe_allow_html=True)
