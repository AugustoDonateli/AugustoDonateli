# Como as artes do perfil são feitas

Tudo aqui é SVG desenhado em Python. As fontes (Bricolage Grotesque e Caveat) vão
embutidas em cada arquivo, cortadas só nos caracteres que ele usa.

- `gerar_arte.py` desenha o cabeçalho e as fichas dos projetos. Rode à mão quando
  mudar algum projeto: `python scripts/gerar_arte.py`
- `espectro.py` desenha o espectro de contribuições. A Action
  `.github/workflows/espectro.yml` roda ele todo dia.
- `arte.py` tem a paleta, as fontes e a medida de texto que os dois usam.

Precisa de `pip install fonttools brotli`.
