"""O espectro do ano: as contribuições dos últimos 12 meses como um espectro de emissão.

Cada risco é um dia. Dia sem commit não emite nada; quanto mais commit, mais
claro e mais grosso o risco. Roda todo dia pela Action (.github/workflows/espectro.yml).

Com GITHUB_TOKEN no ambiente, busca os dados na API do GitHub e guarda em
dados/contribuicoes.json. Sem token, desenha a partir desse arquivo.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import urllib.request

from arte import PALETAS, RAIZ, fontes_css, salvar, txt

USUARIO = os.environ.get("USUARIO", "AugustoDonateli")
DADOS = RAIZ / "dados" / "contribuicoes.json"
MESES = "jan fev mar abr mai jun jul ago set out nov dez".split()

CONSULTA = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def buscar() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return json.loads(DADOS.read_text())
    corpo = json.dumps({"query": CONSULTA, "variables": {"login": USUARIO}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=corpo,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except Exception as erro:  # API fora do ar: redesenha com os últimos dados salvos
        print(f"aviso: não deu para buscar as contribuições ({erro}); usando {DADOS.name}")
        return json.loads(DADOS.read_text())
    dias = [
        {"date": d["date"], "count": d["contributionCount"]}
        for semana in cal["weeks"]
        for d in semana["contributionDays"]
    ]
    dados = {"total": cal["totalContributions"], "dias": dias}
    DADOS.parent.mkdir(exist_ok=True)
    DADOS.write_text(json.dumps(dados, indent=0))
    return dados


def _mistura(t: float) -> str:
    """Âmbar escuro → ouro → branco quente, como metal esquentando."""
    paradas = [(0.0, (140, 74, 18)), (0.55, (240, 169, 58)), (1.0, (255, 243, 209))]
    for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
        if t <= t1:
            k = (t - t0) / (t1 - t0)
            return "#%02x%02x%02x" % tuple(round(a + (b - a) * k) for a, b in zip(c0, c1))
    return "#fff3d1"


def _data_br(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]}"


def desenhar(tema: str, dados: dict) -> str:
    p = PALETAS[tema]
    dias = dados["dias"]
    W, H = 1150, 262
    faixa_y, faixa_h = 6, 150
    margem = 14
    n = len(dias)
    passo = (W - 2 * margem) / max(n - 1, 1)
    maximo = max((d["count"] for d in dias), default=0) or 1

    riscos, brilhos = [], []
    for i, d in enumerate(dias):
        c = d["count"]
        if not c:
            continue
        t = math.log1p(c) / math.log1p(maximo)
        x = margem + i * passo
        cor = _mistura(t)
        riscos.append(
            f'<rect x="{x - (1 + 1.4 * t):.1f}" y="{faixa_y}" width="{2 + 2.8 * t:.1f}" height="{faixa_h}" fill="{cor}" opacity="{0.6 + 0.4 * t:.2f}"/>'
        )
        if t > 0.25:
            brilhos.append(
                f'<rect x="{x - (3 + 5 * t):.1f}" y="{faixa_y}" width="{6 + 10 * t:.1f}" height="{faixa_h}" fill="{cor}" opacity="{0.5 * t:.2f}"/>'
            )

    # Régua: um traço por semana, traço longo e nome no começo de cada mês
    regua = [f'<line x1="0" x2="{W}" y1="{faixa_y + faixa_h + 12}" y2="{faixa_y + faixa_h + 12}"/>']
    rotulos = []
    base = faixa_y + faixa_h + 12
    for i, d in enumerate(dias):
        data = dt.date.fromisoformat(d["date"])
        x = margem + i * passo
        if data.day == 1:
            virada = data.month == 1
            regua.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{base}" y2="{base + (16 if virada else 11)}"/>')
            fim = x + 40 > W  # o último mês não pode sair da imagem
            ancora = f' text-anchor="end" x="{x - 4:.1f}"' if fim else f' x="{x + 4:.1f}"'
            rotulos.append(f'<text{ancora} y="{base + 30}">{MESES[data.month - 1]}</text>')
            if virada:
                rotulos.append(f'<text class="ano" x="{x + 4:.1f}" y="{base + 50}">{data.year}</text>')
        elif data.weekday() == 0:
            regua.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{base}" y2="{base + 5}"/>')

    total = dados["total"]
    forte = max(dias, key=lambda d: d["count"]) if dias else None
    resumo = f"{total} contribuições nos últimos 12 meses"
    destaque = f"dia mais forte: {_data_br(forte['date'])}, {forte['count']}" if forte and forte["count"] else ""
    texto = resumo + destaque + "".join(MESES) + "0123456789"

    borda = f' stroke="{p["regua"]}" stroke-opacity=".5" stroke-width="1.5"' if tema == "escuro" else ""
    css = f"""{fontes_css(texto)}
text{{font-family:'Bricolage',system-ui,sans-serif;font-size:17px;font-weight:500;fill:{p['apoio']}}}
.ano{{font-size:14px;font-weight:600}}
.resumo{{font-size:21px;font-weight:700;fill:{p['tinta']}}}
.regua line{{stroke:{p['regua']};stroke-width:1.5}}
.varre{{transform:scaleX(0);transform-origin:0 0;transform-box:fill-box;animation:varre 2.6s cubic-bezier(.45,0,.25,1) .3s forwards}}
.cursor{{opacity:0;transform:translateX(0);animation:cursor 2.6s cubic-bezier(.45,0,.25,1) .3s both}}
@keyframes varre{{to{{transform:scaleX(1)}}}}
@keyframes cursor{{0%{{opacity:0;transform:translateX(0)}}6%{{opacity:1}}92%{{opacity:1}}100%{{opacity:0;transform:translateX({W}px)}}}}
@media (prefers-reduced-motion:reduce){{.varre{{animation:none;transform:none}}.cursor{{display:none}}}}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{txt(resumo)}. Cada risco do espectro é um dia.">
<style>{css}</style>
<defs>
  <filter id="halo" x="-50%" y="0" width="200%" height="100%"><feGaussianBlur stdDeviation="5"/></filter>
  <clipPath id="faixa"><rect x="0" y="{faixa_y}" width="{W}" height="{faixa_h}" rx="6"/></clipPath>
  <mask id="leitura"><rect class="varre" x="0" y="0" width="{W}" height="{faixa_y + faixa_h}" fill="#fff"/></mask>
</defs>
<rect x="0" y="{faixa_y}" width="{W}" height="{faixa_h}" rx="6" fill="#0F0D0A"{borda}/>
<g clip-path="url(#faixa)">
  <g mask="url(#leitura)">
    <g filter="url(#halo)">{''.join(brilhos)}</g>
    {''.join(riscos)}
  </g>
  <rect class="cursor" x="-1" y="{faixa_y}" width="2" height="{faixa_h}" fill="#FFF3D1"/>
</g>
<g class="regua">{''.join(regua)}</g>
{''.join(rotulos)}
<text class="resumo" x="0" y="{H - 6}">{txt(resumo)}</text>
<text x="{W}" y="{H - 6}" text-anchor="end">{txt(destaque)}</text>
</svg>"""


if __name__ == "__main__":
    dados = buscar()
    for tema in PALETAS:
        print(salvar(f"espectro-{tema}.svg", desenhar(tema, dados)))
