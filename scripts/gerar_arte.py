"""Gera o cabeçalho e as fichas dos projetos do README (versões clara e escura).

Rodar da raiz do repositório:  python scripts/gerar_arte.py
O espectro de contribuições é outro script (espectro.py), que roda todo dia.
"""
from __future__ import annotations

import math

from arte import PALETAS, fontes_css, largura, salvar, txt

EASE = "cubic-bezier(.22,1,.36,1)"  # o mesmo EASE da Aurora


# ---------------------------------------------------------------- cabeçalho
def cabecalho(tema: str) -> str:
    p = PALETAS[tema]
    W, H = 1150, 400
    lado = 270
    cx, cy = 222, 200  # centro da ficha do Au

    # Manchete, palavra por palavra (para entrarem em sequência)
    manchete = "Oi, eu sou o Guto."
    tam, peso, ls = 68, 800, -1.8
    x0, base = 446, 196
    palavras, x = [], x0
    espaco = largura(" ", tam, peso, 72)
    for i, w in enumerate(manchete.split(" ")):
        palavras.append(
            f'<text class="pal" style="animation-delay:{0.38 + i * 0.09:.2f}s" x="{x:.1f}" y="{base}">{txt(w)}</text>'
        )
        x += largura(w, tam, peso, 72, ls) + espaco

    linha = "Desenvolvedor web em Cachoeiro de Itapemirim, ES."
    nota = "Au de Augusto. E de ouro, claro."

    # Seta à mão: da anotação até a borda da ficha
    p0, c1, c2, p3 = (472, 300), (430, 316), (392, 292), (370, 248)
    pts = [
        tuple(
            (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t**2 * c + t**3 * d
            for a, b, c, d in zip(p0, c1, c2, p3)
        )
        for t in [i / 60 for i in range(61)]
    ]
    comp = sum(math.dist(pts[i], pts[i + 1]) for i in range(60))
    dx, dy = p3[0] - c2[0], p3[1] - c2[1]
    n = math.hypot(dx, dy)
    ux, uy = -dx / n, -dy / n
    pontas = []
    for ang in (0.5, -0.5):
        rx = ux * math.cos(ang) - uy * math.sin(ang)
        ry = ux * math.sin(ang) + uy * math.cos(ang)
        pontas.append(f"M{p3[0]} {p3[1]} l{rx * 15:.1f} {ry * 15:.1f}")

    texto_bricolage = manchete + linha + "79196,97AuAugusto[Xe] 4f14 5d10 6s1"
    css = f"""
{fontes_css(texto_bricolage, nota)}
.b{{font-family:'Bricolage',system-ui,sans-serif}}
.pal{{font:800 {tam}px 'Bricolage',system-ui,sans-serif;letter-spacing:{ls}px;fill:{p['tinta']};
  animation:sobe .7s {EASE} both}}
.linha{{font:440 27px 'Bricolage',system-ui,sans-serif;fill:{p['apoio']};animation:aparece .8s ease-out .95s both}}
.nota{{font:600 40px 'Caveat',cursive;fill:{p['caneta']}}}
.cai{{transform:rotate(-3deg);animation:cai 1s {EASE} both}}
.sombra{{transform:translate(12px,12px);animation:pousa .45s ease-out .55s both}}
.brilho{{transform:translateX(-420px);animation:brilho 1.2s cubic-bezier(.45,0,.2,1) 2.7s both}}
.seta{{stroke-dasharray:{comp:.1f};stroke-dashoffset:{comp:.1f};animation:risca .6s ease-in-out 1.55s forwards}}
.ponta{{opacity:0;animation:aparece .12s linear 2.12s forwards}}
.escreve{{transform:scaleX(0);transform-origin:0 0;transform-box:fill-box;animation:escreve 1.15s steps(28,end) 1.8s forwards}}
@keyframes sobe{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes aparece{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes cai{{0%{{opacity:0;transform:translateY(-46px) rotate(-11deg)}}55%{{opacity:1;transform:translateY(5px) rotate(-1.6deg)}}78%{{transform:translateY(-2px) rotate(-3.4deg)}}100%{{transform:rotate(-3deg)}}}}
@keyframes pousa{{from{{transform:translate(0,0);opacity:0}}to{{transform:translate(12px,12px);opacity:1}}}}
@keyframes brilho{{to{{transform:translateX(420px)}}}}
@keyframes risca{{to{{stroke-dashoffset:0}}}}
@keyframes escreve{{to{{transform:scaleX(1)}}}}
@media (prefers-reduced-motion:reduce){{
  .pal,.linha,.cai,.sombra,.brilho,.ponta,.seta,.escreve{{animation:none}}
  .seta{{stroke-dashoffset:0}} .ponta{{opacity:1}} .escreve{{transform:none}} .brilho{{display:none}}
}}"""

    m = lado / 2
    ficha = f"""
<g transform="translate({cx} {cy})">
  <g class="cai">
    <rect class="sombra" x="{-m}" y="{-m}" width="{lado}" height="{lado}" rx="7" fill="{p['sombra']}"/>
    <rect x="{-m}" y="{-m}" width="{lado}" height="{lado}" rx="7" fill="{p['latao']}" stroke="{p['latao_tinta']}" stroke-width="3"/>
    <g clip-path="url(#recorte)">
      <g transform="rotate(20)"><rect class="brilho" x="-45" y="-240" width="90" height="480" fill="url(#reflexo)"/></g>
    </g>
    <g class="b" fill="{p['latao_tinta']}">
      <text x="{-m + 20}" y="{-m + 44}" font-size="30" font-weight="700">79</text>
      <text x="{m - 20}" y="{-m + 40}" font-size="18" font-weight="500" text-anchor="end">196,97</text>
      <text x="0" y="40" font-size="142" font-weight="800" text-anchor="middle" letter-spacing="-5">Au</text>
      <text x="0" y="86" font-size="26" font-weight="650" text-anchor="middle">Augusto</text>
      <text x="0" y="{m - 18}" font-size="15" font-weight="500" text-anchor="middle">[Xe] 4f<tspan dy="-7" font-size="10">14</tspan><tspan dy="7"> 5d</tspan><tspan dy="-7" font-size="10">10</tspan><tspan dy="7"> 6s</tspan><tspan dy="-7" font-size="10">1</tspan></text>
    </g>
  </g>
</g>"""

    anotacao = f"""
<path class="seta" d="M{p0[0]} {p0[1]} C{c1[0]} {c1[1]} {c2[0]} {c2[1]} {p3[0]} {p3[1]}" fill="none" stroke="{p['caneta']}" stroke-width="2.8" stroke-linecap="round"/>
<path class="ponta" d="{' '.join(pontas)}" fill="none" stroke="{p['caneta']}" stroke-width="2.8" stroke-linecap="round"/>
<g transform="rotate(-2.5 486 318)">
  <mask id="escrita"><rect class="escreve" x="482" y="282" width="560" height="60" fill="#fff"/></mask>
  <text class="nota" x="486" y="318" mask="url(#escrita)">{txt(nota)}</text>
</g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Oi, eu sou o Guto. Augusto Donateli, desenvolvedor web em Cachoeiro de Itapemirim.">
<style>{css}</style>
<defs><linearGradient id="reflexo"><stop offset="0" stop-color="{p['brilho']}" stop-opacity="0"/><stop offset=".5" stop-color="{p['brilho']}" stop-opacity=".75"/><stop offset="1" stop-color="{p['brilho']}" stop-opacity="0"/></linearGradient><clipPath id="recorte"><rect x="{-m}" y="{-m}" width="{lado}" height="{lado}" rx="7"/></clipPath></defs>
{ficha}
{''.join(palavras)}
<text class="linha" x="449" y="248">{txt(linha)}</text>
{anotacao}
</svg>"""


# ------------------------------------------------------------------- fichas
# O número é a ordem em que o repositório nasceu na conta (o 1 é o primeiro).
PROJETOS = [
    # arquivo, número, símbolo, nome, mês, família
    ("compasso", 14, "Cp", "Compasso", "ago 2026", "estudo"),
    ("enem", 21, "En", "Estudos ENEM", "set 2026", "estudo"),
    ("escape", 19, "Eq", "Escape Químico", "set 2026", "ciencia"),
    ("ifesciencia", 16, "If", "Ifesciência", "ago 2026", "ciencia"),
    ("nba", 15, "Nb", "NBA do zero", "ago 2026", "estudo"),
    ("teclado", 6, "Tc", "Teclado K950", "mai 2026", "design"),
]
NOME_FAMILIA = {"estudo": "estudo", "ciencia": "ciência", "design": "design", "produto": "produto"}


def ficha(tema: str, numero: int, simbolo: str, nome: str, mes: str, familia: str) -> str:
    p = PALETAS[tema]
    em_obra = familia == "produto"
    if em_obra:
        fundo, letra = ("none", p["tinta"])
    else:
        fundo, letra = p["familias"][familia]
    borda = p["tinta"]
    rotulo = "em construção" if em_obra else NOME_FAMILIA[familia]
    texto = f"{numero}{simbolo}{nome}{mes}{rotulo}"
    L = 300

    faixa = ""
    if em_obra:
        # fita de risco: só para o que ainda não está pronto, e ela anda devagar
        listras = "".join(
            f'<path d="M{x} 0 l26 0 l-34 34 l-26 0z" fill="{p["latao"]}"/>' for x in range(-40, L + 80, 52)
        )
        faixa = f"""
<clipPath id="fita"><rect x="3" y="{L - 40}" width="{L - 6}" height="37" rx="3"/></clipPath>
<g clip-path="url(#fita)">
  <rect x="0" y="{L - 40}" width="{L}" height="40" fill="{p['tinta']}"/>
  <g class="anda">{listras}</g>
</g>"""

    rodape_y = L - 54 if em_obra else L - 22
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{L}" viewBox="0 0 {L} {L}" role="img" aria-label="{txt(nome)}">
<style>{fontes_css(texto)}
text{{font-family:'Bricolage',system-ui,sans-serif;fill:{letra}}}
.anda{{transform:translate(0,{L - 37}px);animation:anda 3.2s linear infinite}}
@keyframes anda{{from{{transform:translate(0,{L - 37}px)}}to{{transform:translate(52px,{L - 37}px)}}}}
@media (prefers-reduced-motion:reduce){{.anda{{animation:none}}}}
</style>
<rect x="1.5" y="1.5" width="{L - 3}" height="{L - 3}" rx="6" fill="{fundo}" stroke="{borda}" stroke-width="3" {'stroke-dasharray="10 7"' if em_obra else ''}/>
{faixa}
<text x="20" y="46" font-size="30" font-weight="700">{numero}</text>
<text x="{L - 20}" y="42" font-size="17" font-weight="500" text-anchor="end">{txt(mes)}</text>
<text x="{L / 2}" y="{166 if not em_obra else 156}" font-size="118" font-weight="800" text-anchor="middle" letter-spacing="-3">{txt(simbolo)}</text>
<text x="{L / 2}" y="{214 if not em_obra else 200}" font-size="25" font-weight="650" text-anchor="middle">{txt(nome)}</text>
<text x="{L / 2}" y="{rodape_y}" font-size="16" font-weight="500" text-anchor="middle" opacity=".8">{txt(rotulo)}</text>
</svg>"""


if __name__ == "__main__":
    for tema in PALETAS:
        print(salvar(f"cabecalho-{tema}.svg", cabecalho(tema)))
        for arquivo, *dados in PROJETOS:
            salvar(f"ficha-{arquivo}-{tema}.svg", ficha(tema, *dados))
        salvar(f"ficha-aurora-{tema}.svg", ficha(tema, 13, "Ar", "Aurora", "jul 2026", "produto"))
