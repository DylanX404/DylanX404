"""Generates the animated profile SVGs in assets/. Pure SVG + SMIL (no JS, no external fonts or
images), so GitHub renders them reliably. Run: python3 .github/gen/gen.py"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[2] / "assets"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
BG, PANEL, LINE, TEXT, DIM = "#0b0f17", "#0f1520", "#1d2633", "#e6edf3", "#7d8b9c"
C1, C2, C3 = "#00e5ff", "#8b5cf6", "#22c55e"
CW = 0.602  # monospace advance per font-size


def esc(s: str) -> str:
    return escape(s)


# ----------------------------------------------------------------------------------------- hero
def hero() -> str:
    roles = ["autonomous systems", "applied ai", "infrastructure at scale", "security engineering", "building in private"]
    n, per = len(roles), 3.2
    total = n * per
    role_svg = []
    for i, r in enumerate(roles):
        a, b = i / n, (i + 1) / n
        eps = 0.06 / n
        kt = f"0;{a:.4f};{a + eps:.4f};{b - eps:.4f};{b:.4f};1"
        role_svg.append(
            f'<text x="80" y="214" font-family="{MONO}" font-size="22" fill="{C1}" opacity="0">{esc(r)}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/></text>'
        )
    rings = "".join(
        f'<circle cx="1010" cy="160" r="{r}" fill="none" stroke="{C1}" stroke-opacity="{0.10 + k * 0.05:.2f}" stroke-width="1"/>'
        for k, r in enumerate((110, 80, 50))
    )
    dots = "".join(
        f'<circle r="{s}" fill="{c}"><animateMotion dur="{d}s" repeatCount="indefinite" rotate="auto" '
        f'path="M {1010 + r} 160 A {r} {r} 0 1 1 {1010 - r} 160 A {r} {r} 0 1 1 {1010 + r} 160"/></circle>'
        for r, s, c, d in ((110, 3.5, C1, 14), (80, 3, C2, 9), (50, 2.5, C3, 6))
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="100%" role="img" aria-label="Dylan Bezuidenhout — systems engineer">
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-width="1"/></pattern>
  <radialGradient id="glow" cx="0.2" cy="0.1" r="0.7"><stop offset="0" stop-color="{C2}" stop-opacity="0.35"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/>
    <animate attributeName="cx" values="0.15;0.45;0.15" dur="18s" repeatCount="indefinite"/></radialGradient>
  <radialGradient id="glow2" cx="0.85" cy="0.5" r="0.35"><stop offset="0" stop-color="{C1}" stop-opacity="0.10"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{TEXT}"/><stop offset="0.45" stop-color="{TEXT}"/><stop offset="0.5" stop-color="{C1}"/><stop offset="0.55" stop-color="{TEXT}"/><stop offset="1" stop-color="{TEXT}"/>
    <animate attributeName="x1" values="-1;1" dur="5s" repeatCount="indefinite"/><animate attributeName="x2" values="0;2" dur="5s" repeatCount="indefinite"/></linearGradient>
  <linearGradient id="scan" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{C1}" stop-opacity="0"/><stop offset="1" stop-color="{C1}" stop-opacity="0.08"/></linearGradient>
  <clipPath id="card"><rect width="1200" height="320" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="1200" height="320" fill="{BG}"/>
  <rect width="1200" height="320" fill="url(#grid)" opacity="0.55"/>
  <rect width="1200" height="320" fill="url(#glow)"/>
  <rect width="1200" height="320" fill="url(#glow2)"/>
  <rect y="-80" width="1200" height="80" fill="url(#scan)"><animate attributeName="y" values="-80;320" dur="6s" repeatCount="indefinite"/></rect>
  <circle cx="40" cy="36" r="6" fill="#ff5f57"/><circle cx="60" cy="36" r="6" fill="#febc2e"/><circle cx="80" cy="36" r="6" fill="#28c840"/>
  <text x="80" y="122" font-family="{SANS}" font-size="56" font-weight="800" letter-spacing="2" fill="url(#name)">DYLAN BEZUIDENHOUT</text>
  <text x="80" y="164" font-family="{MONO}" font-size="20" fill="{DIM}">systems engineer</text>
  <text x="56" y="214" font-family="{MONO}" font-size="22" fill="{C2}">&gt;</text>
  {"".join(role_svg)}
  <circle cx="86" cy="268" r="5" fill="{C3}"><animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="100" y="273" font-family="{MONO}" font-size="14" fill="{DIM}">online · shipping quietly · always learning</text>
  {rings}{dots}
  <circle cx="1010" cy="160" r="9" fill="{C1}"><animate attributeName="r" values="7;11;7" dur="3s" repeatCount="indefinite"/></circle>
  <circle cx="1010" cy="160" r="9" fill="none" stroke="{C1}" stroke-width="2"><animate attributeName="r" values="9;130" dur="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0" dur="3s" repeatCount="indefinite"/></circle>
  <rect x="0.5" y="0.5" width="1199" height="319" rx="18" fill="none" stroke="{LINE}"/>
</g>
</svg>'''


# ----------------------------------------------------------------------------------------- terminal
def terminal() -> str:
    fs, lh, x0, y0 = 17, 30, 40, 92
    cw = fs * CW
    lines: list[tuple[str, str, float]] = []  # (kind, text, start time)
    t = 0.4

    def cmd(s: str) -> None:
        nonlocal t
        lines.append(("cmd", s, t))
        t += len(s) * 0.045 + 0.5

    def out(s: str, kind: str = "out") -> None:
        nonlocal t
        lines.append((kind, s, t))
        t += 0.22

    cmd("whoami")
    out("dylan  ·  systems engineer")
    t += 0.3
    cmd("cat ./focus")
    for row in ("autonomous systems   ▸  agents that plan, act and verify their own work",
                "applied ai           ▸  local models · evaluation · computer vision",
                "infrastructure       ▸  networks · fleets · observability · zero trust",
                "security             ▸  detection · hardening · least privilege"):
        out(row, "focus")
    t += 0.3
    cmd("ls ./projects")
    out("", "redact")
    out("[ 7 active · all private ]", "note")
    end = t + 0.3
    parts = []
    for i, (kind, s, start) in enumerate(lines):
        y = y0 + i * lh
        if kind == "cmd":
            w = (len(s) + 2) * cw
            parts.append(
                f'<clipPath id="c{i}"><rect x="{x0}" y="{y - fs}" height="{lh}" width="0">'
                f'<animate attributeName="width" begin="{start:.2f}s" dur="{len(s) * 0.045:.2f}s" fill="freeze" calcMode="discrete" values="{";".join(f"{(k + 2) * cw:.1f}" for k in range(len(s) + 1))}"/></rect></clipPath>'
                f'<g clip-path="url(#c{i})"><text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{C3}">$ <tspan fill="{TEXT}">{esc(s)}</tspan></text></g>'
            )
        elif kind == "redact":
            bars, bx = [11, 14, 8, 15, 6, 10, 9], x0
            for k, b in enumerate(bars):
                bw = b * cw
                parts.append(
                    f'<rect x="{bx:.1f}" y="{y - fs + 3}" width="{bw:.1f}" height="{fs}" rx="2" fill="{C1}" opacity="0">'
                    f'<animate attributeName="opacity" to="0.85" begin="{start + k * 0.08:.2f}s" dur="0.15s" fill="freeze"/>'
                    f'<animate attributeName="fill" values="{C1};{C2};{C1}" dur="{2.5 + k * 0.4:.1f}s" begin="{start:.2f}s" repeatCount="indefinite"/></rect>'
                )
                bx += bw + 2.5 * cw
        else:
            color = {"out": TEXT, "focus": DIM, "note": C1}[kind]
            body = esc(s)
            if kind == "focus":
                a, b = s.split("▸")
                body = f'<tspan fill="{TEXT}">{esc(a)}</tspan><tspan fill="{C2}">▸</tspan>{esc(b)}'
            parts.append(
                f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{color}" opacity="0" xml:space="preserve">{body}'
                f'<animate attributeName="opacity" to="1" begin="{start:.2f}s" dur="0.2s" fill="freeze"/></text>'
            )
    yc = y0 + len(lines) * lh
    parts.append(
        f'<text x="{x0}" y="{yc}" font-family="{MONO}" font-size="{fs}" fill="{C3}" opacity="0">$ '
        f'<animate attributeName="opacity" to="1" begin="{end:.2f}s" dur="0.1s" fill="freeze"/></text>'
        f'<rect x="{x0 + 2 * cw:.1f}" y="{yc - fs + 3}" width="{cw:.1f}" height="{fs}" fill="{TEXT}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1.1s" begin="{end:.2f}s" repeatCount="indefinite"/></rect>'
    )
    h = yc + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {h}" width="100%" role="img" aria-label="terminal: whoami, focus, projects">
<defs><clipPath id="win"><rect width="1000" height="{h}" rx="14"/></clipPath>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{C2}" stop-opacity="0.25"/><stop offset="1" stop-color="{C1}" stop-opacity="0.08"/></linearGradient></defs>
<g clip-path="url(#win)">
  <rect width="1000" height="{h}" fill="{PANEL}"/>
  <rect width="1000" height="44" fill="url(#bar)"/>
  <circle cx="26" cy="22" r="6" fill="#ff5f57"/><circle cx="46" cy="22" r="6" fill="#febc2e"/><circle cx="66" cy="22" r="6" fill="#28c840"/>
  <text x="500" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{DIM}">dylan@lab: ~</text>
  {"".join(parts)}
  <rect x="0.5" y="0.5" width="999" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>
</g></svg>'''


# ----------------------------------------------------------------------------------------- stack
LANG = [("Python", "#3572A5"), ("TypeScript", "#3178c6"), ("JavaScript", "#f1e05a"), ("SQL", "#e38c00"),
        ("Bash", "#89e051"), ("HTML", "#e34c26"), ("CSS", "#663399"), ("YAML", "#cb171e")]
TOOLS = [("React", "#61dafb"), ("FastAPI", "#009688"), ("Django", "#0c4b33"), ("Node.js", "#5fa04e"),
         ("PostgreSQL", "#336791"), ("Docker", "#2496ed"), ("Linux", "#fcc624"), ("Cloudflare", "#f38020"),
         ("GitHub Actions", "#2088ff"), ("Tailwind", "#38bdf8"), ("Vite", "#a855f7")]
DOMAINS = [("LLM agents", C1), ("local models", C2), ("computer vision", "#f472b6"), ("zero trust", C3),
           ("observability", "#fbbf24"), ("automation", "#60a5fa"), ("networking", "#34d399"), ("APIs", "#f87171")]


def chip_row(items: list[tuple[str, str]], y: int, speed: float, reverse: bool, fs: int = 16) -> str:
    cw, pad, gap = fs * CW, 18, 14
    xs, x = [], 0.0
    for name, _ in items:
        w = len(name) * cw + pad * 2 + 16
        xs.append((x, w))
        x += w + gap
    span = x
    chips = []
    for copy in range(3):
        for (name, col), (cx, w) in zip(items, xs, strict=True):
            X = cx + copy * span
            chips.append(
                f'<g transform="translate({X:.1f},{y})"><rect width="{w:.1f}" height="40" rx="20" fill="{PANEL}" stroke="{LINE}"/>'
                f'<circle cx="{pad + 4}" cy="20" r="5" fill="{col}"/>'
                f'<text x="{pad + 16}" y="25.5" font-family="{MONO}" font-size="{fs}" fill="{TEXT}">{esc(name)}</text></g>'
            )
    a, b = (-span, 0) if reverse else (0, -span)
    return (f'<g><animateTransform attributeName="transform" type="translate" from="{a:.1f} 0" to="{b:.1f} 0" '
            f'dur="{speed}s" repeatCount="indefinite"/>{"".join(chips)}</g>')


def stack() -> str:
    W, H = 1000, 300
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="languages and tools">
<defs>
  <clipPath id="box"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
  <linearGradient id="fadeR" x1="1" x2="0"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
  <linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{C2}" stop-opacity="0"/><stop offset="0.5" stop-color="{C1}"/><stop offset="1" stop-color="{C2}" stop-opacity="0"/>
    <animate attributeName="x1" values="-1;1" dur="4s" repeatCount="indefinite"/><animate attributeName="x2" values="0;2" dur="4s" repeatCount="indefinite"/></linearGradient>
</defs>
<g clip-path="url(#box)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <text x="32" y="44" font-family="{MONO}" font-size="15" fill="{DIM}"><tspan fill="{C2}">//</tspan> stack <tspan fill="{LINE}">·</tspan> <tspan fill="{C3}">languages</tspan> · <tspan fill="{C1}">tools</tspan> · <tspan fill="#f472b6">domains</tspan></text>
  <rect x="32" y="60" width="{W - 64}" height="1.5" fill="url(#line)"/>
  {chip_row(LANG, 84, 34, False)}
  {chip_row(TOOLS, 148, 46, True)}
  {chip_row(DOMAINS, 212, 40, False)}
  <rect y="76" width="110" height="184" fill="url(#fadeL)"/><rect x="{W - 110}" y="76" width="110" height="184" fill="url(#fadeR)"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE}"/>
</g></svg>'''


# ----------------------------------------------------------------------------------------- now
def now() -> str:
    W, H, cw_, gap = 1000, 250, 312, 32
    cards = [
        ("AGENTS", "systems that research, decide", "and check their own work", C1),
        ("VISION", "models that see — tuned to", "run fast at the edge", "#f472b6"),
        ("INFRA", "networks, fleets and", "zero-trust plumbing", C3),
    ]
    out = []
    for i, (title, l1, l2, col) in enumerate(cards):
        x = i * (cw_ + gap / 2) + 4
        g = [f'<rect x="{x}" y="4" width="{cw_}" height="{H - 8}" rx="14" fill="{PANEL}" stroke="{LINE}"/>',
             f'<rect x="{x}" y="4" width="{cw_}" height="3" rx="1.5" fill="{col}" opacity="0.8"><animate attributeName="opacity" values="0.3;1;0.3" dur="{3 + i}s" repeatCount="indefinite"/></rect>']
        cx, cy = x + cw_ / 2, 92
        if title == "AGENTS":
            pts = [(cx - 70, cy - 30), (cx, cy - 50), (cx + 70, cy - 25), (cx - 45, cy + 35), (cx + 50, cy + 38), (cx, cy)]
            for a in range(len(pts)):
                for b in range(a + 1, len(pts)):
                    if (a + b) % 2 == 0 or 5 in (a, b):
                        (x1, y1), (x2, y2) = pts[a], pts[b]
                        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-opacity="0.25"/>')
            for k, (px, py) in enumerate(pts):
                r = 7 if k == 5 else 4.5
                g.append(f'<circle cx="{px}" cy="{py}" r="{r}" fill="{col}"><animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" begin="{k * 0.4:.1f}s" repeatCount="indefinite"/></circle>')
            g.append(f'<circle r="3" fill="{TEXT}"><animateMotion dur="3s" repeatCount="indefinite" path="M{pts[0][0]},{pts[0][1]} L{pts[5][0]},{pts[5][1]} L{pts[2][0]},{pts[2][1]} L{pts[4][0]},{pts[4][1]} L{pts[5][0]},{pts[5][1]} L{pts[3][0]},{pts[3][1]} Z"/></circle>')
        elif title == "VISION":
            g.append(f'<rect x="{cx - 80}" y="{cy - 55}" width="160" height="110" rx="6" fill="none" stroke="{LINE}"/>')
            for dx, dy in ((-80, -55), (80, -55), (-80, 55), (80, 55)):
                sx, sy = (1 if dx < 0 else -1), (1 if dy < 0 else -1)
                g.append(f'<path d="M{cx + dx} {cy + dy + sy * 16} V{cy + dy} H{cx + dx + sx * 16}" fill="none" stroke="{col}" stroke-width="2.5"/>')
            g.append(f'<rect x="{cx - 34}" y="{cy - 22}" width="68" height="44" rx="3" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-dasharray="4 3">'
                     f'<animate attributeName="x" values="{cx - 60};{cx - 10};{cx - 44};{cx - 60}" dur="5s" repeatCount="indefinite"/>'
                     f'<animate attributeName="y" values="{cy - 40};{cy - 10};{cy - 30};{cy - 40}" dur="5s" repeatCount="indefinite"/></rect>')
            g.append(f'<rect x="{cx - 78}" y="{cy - 53}" width="156" height="2" fill="{col}" opacity="0.7"><animate attributeName="y" values="{cy - 53};{cy + 51};{cy - 53}" dur="2.8s" repeatCount="indefinite"/></rect>')
            g.append(f'<text x="{cx - 76}" y="{cy + 72}" font-family="{MONO}" font-size="11" fill="{col}">conf 0.<tspan>9<animate attributeName="opacity" values="1;0.4;1" dur="1s" repeatCount="indefinite"/></tspan>7</text>')
        else:
            nodes = [(cx - 100, cy), (cx - 35, cy - 40), (cx - 35, cy + 40), (cx + 35, cy - 40), (cx + 35, cy + 40), (cx + 100, cy)]
            edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 4), (2, 3)]
            for a, b in edges:
                (x1, y1), (x2, y2) = nodes[a], nodes[b]
                g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-opacity="0.3"/>')
            for k, (px, py) in enumerate(nodes):
                g.append(f'<rect x="{px - 8}" y="{py - 8}" width="16" height="16" rx="4" fill="{PANEL}" stroke="{col}"/>')
            for k, path in enumerate(((0, 1, 3, 5), (0, 2, 4, 5), (0, 1, 4, 5), (0, 2, 3, 5))):
                d = "M" + " L".join(f"{nodes[n][0]},{nodes[n][1]}" for n in path)
                g.append(f'<circle r="3" fill="{TEXT}"><animateMotion dur="2.6s" begin="{k * 0.65:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
            g.append(f'<path d="M{cx + 92} {cy - 26} l8 -6 l8 6 v8 c0 8 -8 12 -8 12 c0 0 -8 -4 -8 -12z" fill="none" stroke="{col}" stroke-width="1.5" transform="translate(-8,-2)"/>')
        g.append(f'<text x="{x + 24}" y="{H - 66}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3" fill="{col}">{title}</text>')
        g.append(f'<text x="{x + 24}" y="{H - 42}" font-family="{SANS}" font-size="15" fill="{TEXT}">{esc(l1)}</text>')
        g.append(f'<text x="{x + 24}" y="{H - 22}" font-family="{SANS}" font-size="15" fill="{DIM}">{esc(l2)}</text>')
        out.append("".join(g))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="now building: agents, vision, infrastructure">{"".join(out)}</svg>'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in (("hero", hero), ("terminal", terminal), ("now", now), ("stack", stack)):
        (OUT / f"{name}.svg").write_text(fn())
        print("wrote", OUT / f"{name}.svg")
