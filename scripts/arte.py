"""Peças comuns das artes do perfil: paleta, fontes embutidas e medida de texto.

As imagens do README são SVGs que o GitHub mostra como <img>. Imagem não carrega
nada de fora, então cada SVG leva dentro só os caracteres que usa das fontes
(subset). Assim a tipografia é a de verdade, e o arquivo continua leve.
"""
from __future__ import annotations

import base64
import io
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "scripts" / "fontes"
ASSETS = RAIZ / "assets"

BRICOLAGE = FONTES / "bricolage.woff2"  # variável: wght 400–800, opsz 12–96
CAVEAT = FONTES / "caveat.woff2"  # caligrafia, peso 600

# Duas paletas. "tinta" é o texto; "latao" é o ouro do Au; "caneta" é a Bic azul
# das anotações. As famílias pintam as fichas dos projetos.
PALETAS = {
    "claro": {
        "tinta": "#1B1814",
        "apoio": "#5B544A",
        "latao": "#E4B04C",
        "latao_tinta": "#1B1814",
        "sombra": "#1B1814",
        "brilho": "#FFFFFF",
        "caneta": "#1F47C2",
        "regua": "#8A8274",
        "familias": {
            "estudo": ("#D3E3F6", "#1B1814"),
            "ciencia": ("#D2EDDB", "#1B1814"),
            "design": ("#F6DCC8", "#1B1814"),
        },
    },
    "escuro": {
        "tinta": "#EDE7DB",
        "apoio": "#A79F92",
        "latao": "#E0A34A",
        "latao_tinta": "#17140F",
        "sombra": "#7C5726",
        "brilho": "#FFF4D6",
        "caneta": "#9DB7FF",
        "regua": "#7D766B",
        "familias": {
            "estudo": ("#1D3150", "#EDE7DB"),
            "ciencia": ("#173B28", "#EDE7DB"),
            "design": ("#4A2C19", "#EDE7DB"),
        },
    },
}


def _subset_woff2(caminho: Path, texto: str) -> str:
    """Corta a fonte para os caracteres de `texto` e devolve em base64."""
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "tnum"]
    opts.notdef_outline = True
    fonte = subset.load_font(str(caminho), opts)
    sub = subset.Subsetter(opts)
    sub.populate(text=texto + " ")
    sub.subset(fonte)
    buf = io.BytesIO()
    subset.save_font(fonte, buf, opts)
    return base64.b64encode(buf.getvalue()).decode()


def fontes_css(texto_bricolage: str, texto_caveat: str = "") -> str:
    css = (
        "@font-face{font-family:'Bricolage';font-weight:400 800;"
        f"src:url(data:font/woff2;base64,{_subset_woff2(BRICOLAGE, texto_bricolage)}) format('woff2')}}"
    )
    if texto_caveat:
        css += (
            "@font-face{font-family:'Caveat';font-weight:600;"
            f"src:url(data:font/woff2;base64,{_subset_woff2(CAVEAT, texto_caveat)}) format('woff2')}}"
        )
    return css


@lru_cache(maxsize=None)
def _instancia(peso: int, opsz: int) -> TTFont:
    fonte = TTFont(str(BRICOLAGE))
    return instancer.instantiateVariableFont(fonte, {"wght": peso, "opsz": opsz})


def largura(texto: str, tamanho: float, peso: int = 800, opsz: int = 96, espacamento: float = 0) -> float:
    """Largura aproximada do texto em px (sem kerning), para posicionar palavras."""
    fonte = _instancia(peso, opsz)
    cmap = fonte.getBestCmap()
    hmtx = fonte["hmtx"]
    upm = fonte["head"].unitsPerEm
    total = 0
    for ch in texto:
        glifo = cmap.get(ord(ch))
        if glifo:
            total += hmtx[glifo][0]
    return total * tamanho / upm + espacamento * max(len(texto) - 1, 0)


@lru_cache(maxsize=None)
def _caveat() -> TTFont:
    return TTFont(str(CAVEAT))


def largura_caveat(texto: str, tamanho: float) -> float:
    fonte = _caveat()
    cmap, hmtx, upm = fonte.getBestCmap(), fonte["hmtx"], fonte["head"].unitsPerEm
    return sum(hmtx[cmap[ord(c)]][0] for c in texto if ord(c) in cmap) * tamanho / upm


def txt(s: str) -> str:
    return escape(s)


def salvar(nome: str, svg: str) -> Path:
    ASSETS.mkdir(exist_ok=True)
    destino = ASSETS / nome
    destino.write_text(svg, encoding="utf-8")
    return destino
