# Gera o cabeçalho e os cards do README do perfil (versões clara e escura).
from pathlib import Path
A = Path("assets")
SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
  "dark":  dict(bg1="#070b16", bg2="#0d1426", fg="#f1f5f9", sub="#94a3b8", line="#1e293b",
               b1="#14b8a6", b2="#8b5cf6", b3="#22d3ee", bop="0.55", panel="#0f172a", pill="#1e293b", pilltx="#cbd5e1"),
  "light": dict(bg1="#f8fafc", bg2="#eef2ff", fg="#0f172a", sub="#475569", line="#e2e8f0",
               b1="#5eead4", b2="#c4b5fd", b3="#a5f3fc", bop="0.75", panel="#ffffff", pill="#f1f5f9", pilltx="#334155"),
}

def header(t, name):
    c = THEMES[t]
    lines = ["desenvolvedor web &amp; automação", "construindo a Aurora, IA no WhatsApp", "estudante de informática no Ifes"]
    rot = "".join(
        f'<text class="rot r{i}" x="80" y="232">{s}<tspan class="cur">_</tspan></text>' for i, s in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Augusto Donateli, desenvolvedor web">
<style>
  .name {{ font: 800 72px {SANS}; fill: {c["fg"]}; letter-spacing: -2px; }}
  .hi   {{ font: 600 22px {MONO}; fill: {c["sub"]}; }}
  .prompt {{ font: 600 26px {MONO}; fill: {c["b1"]}; }}
  .rot  {{ font: 500 26px {MONO}; fill: {c["fg"]}; opacity: 0; animation: rot 12s infinite; }}
  .r1 {{ animation-delay: 4s; }} .r2 {{ animation-delay: 8s; }}
  @keyframes rot {{ 0%{{opacity:0; transform:translateY(8px)}} 4%,30%{{opacity:1; transform:translateY(0)}} 34%,100%{{opacity:0; transform:translateY(-8px)}} }}
  .cur  {{ fill: {c["b1"]}; animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .loc  {{ font: 500 18px {MONO}; fill: {c["sub"]}; }}
  .blob {{ opacity: {c["bop"]}; }}
  .a1 {{ animation: d1 16s ease-in-out infinite alternate; }}
  .a2 {{ animation: d2 20s ease-in-out infinite alternate; }}
  .a3 {{ animation: d3 18s ease-in-out infinite alternate; }}
  @keyframes d1 {{ to {{ transform: translate(-140px, 40px) scale(1.15); }} }}
  @keyframes d2 {{ to {{ transform: translate(120px, -30px) scale(0.9); }} }}
  @keyframes d3 {{ to {{ transform: translate(-80px, -50px) scale(1.2); }} }}
  @media (prefers-reduced-motion: reduce) {{ .a1,.a2,.a3,.cur {{ animation: none; }} .rot {{ animation: none; }} .r0 {{ opacity: 1; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c["line"]}" stroke-width="1" opacity="0.6"/></pattern>
  <clipPath id="clip"><rect width="1200" height="320" rx="24"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect width="1200" height="320" fill="url(#bg)"/>
  <g filter="url(#blur)">
    <ellipse class="blob a1" cx="980" cy="90"  rx="260" ry="110" fill="{c["b1"]}"/>
    <ellipse class="blob a2" cx="820" cy="250" rx="220" ry="90"  fill="{c["b2"]}"/>
    <ellipse class="blob a3" cx="1120" cy="260" rx="180" ry="80" fill="{c["b3"]}"/>
  </g>
  <rect width="1200" height="320" fill="url(#grid)" opacity="0.35"/>
  <text class="hi" x="80" y="82">// oi, eu sou o Guto 👋</text>
  <text class="name" x="76" y="164">Augusto Donateli</text>
  <text class="prompt" x="80" y="232">&gt;</text>
  <g transform="translate(26 0)">{rot}</g>
  <text class="loc" x="80" y="286">📍 Cachoeiro de Itapemirim · ES · Brasil</text>
</g>
<rect x="0.5" y="0.5" width="1199" height="319" rx="24" fill="none" stroke="{c["line"]}"/>
</svg>'''
    (A / f"header-{t}.svg").write_text(svg, encoding="utf-8")

def card(t, slug, title, kicker, desc, tags, accent, live):
    c = THEMES[t]
    W, H = 600, 230
    x = 32; pills = []
    for tag in tags:
        w = int(len(tag) * 7.9) + 24
        pills.append(f'<rect x="{x}" y="176" width="{w}" height="28" rx="14" fill="{c["pill"]}"/>'
                     f'<text class="tag" x="{x + w/2}" y="195" text-anchor="middle">{tag}</text>')
        x += w + 8
    d = "".join(f'<text class="desc" x="32" y="{120 + i*24}">{s}</text>' for i, s in enumerate(desc))
    status = (f'<circle class="pulse" cx="{W-118}" cy="44" r="5" fill="#22c55e"/><text class="live" x="{W-104}" y="49">no ar</text>'
              if live else "")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<style>
  .title {{ font: 750 30px {SANS}; fill: {c["fg"]}; letter-spacing: -0.6px; }}
  .kick  {{ font: 600 13px {MONO}; fill: {accent}; letter-spacing: 1.5px; text-transform: uppercase; }}
  .desc  {{ font: 400 16px {SANS}; fill: {c["sub"]}; }}
  .tag   {{ font: 600 12.5px {MONO}; fill: {c["pilltx"]}; }}
  .live  {{ font: 600 13px {MONO}; fill: {c["sub"]}; }}
  .arrow {{ font: 600 24px {SANS}; fill: {c["sub"]}; }}
  .pulse {{ animation: p 2s ease-in-out infinite; }}
  @keyframes p {{ 50% {{ opacity: .35; }} }}
  .glow {{ animation: g 6s ease-in-out infinite alternate; }}
  @keyframes g {{ to {{ transform: translate(-40px, 20px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .pulse, .glow {{ animation: none; }} }}
</style>
<defs>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{c["panel"]}"/>
  <ellipse class="glow" cx="{W-40}" cy="10" rx="170" ry="90" fill="{accent}" opacity="{0.28 if t=="dark" else 0.22}" filter="url(#b)"/>
  <rect x="0" y="0" width="6" height="{H}" fill="{accent}"/>
  <text class="kick" x="32" y="48">{kicker}</text>
  <text class="title" x="30" y="88">{title}</text>
  {d}
  {"".join(pills)}
  {status}
  <text class="arrow" x="{W-48}" y="52">↗</text>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{c["line"]}"/>
</svg>'''
    (A / f"card-{slug}-{t}.svg").write_text(svg, encoding="utf-8")

CARDS = [
  ("compasso", "Compasso", "música · web audio",
   ["Teoria musical que vira som e vira gesto: trilha", "de lições, braço, groove, ouvido e afinador."],
   ["React", "TypeScript", "Tone.js", "GSAP", "Supabase"], "#f59e0b", True),
  ("enem", "Estudos ENEM", "educação · planejamento",
   ["Decide o que estudar hoje, lembra dos seus erros", "e encaixa as revisões até a data da prova."],
   ["React", "TypeScript", "Vite", "Playwright"], "#3b82f6", True),
  ("escape", "Escape Químico", "feira de ciências · tempo real",
   ["Sala de fuga de química: fila do dia, sessões,", "perguntas por QR code e placar ao vivo."],
   ["Next.js", "TypeScript", "Supabase", "Zod"], "#10b981", True),
  ("ifesciencia", "Ifesciência", "divulgação científica",
   ["Site do @ifesciencia: catálogo de experimentos", "para professores e painel da equipe."],
   ["Next.js", "Supabase", "GSAP", "pdf-lib"], "#a855f7", True),
]
for t in THEMES:
    header(t, "Augusto Donateli")
    for cd in CARDS:
        card(t, *cd)
print(sorted(p.name for p in A.iterdir()))
