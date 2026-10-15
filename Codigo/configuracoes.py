"""Constantes e caminhos usados pelo jogo todo."""
from pathlib import Path

TITULO = "OUTREM"
FPS = 60

# Tela lógica (16:9). Tudo é desenhado nela e o pygame amplia para a janela real.
# 640x360 amplia certinho (sem pixel torto) em 1280x720, 1920x1080, 2560x1440 e 4K.
LARGURA = 640
ALTURA = 360

# Tamanho extra dos sprites dos personagens (os PNGs são 128x128; 1 = tamanho original)
ESCALA_SPRITE = 1

# Caminhos: tudo é calculado a partir deste arquivo, então não depende de
# "de onde" o jogo é executado.
PASTA_CODIGO = Path(__file__).resolve().parent


def _achar_raiz():
    """Procura a pasta que tem Personagens/ e Ambientes/ (a raiz do repositório).

    Sobe pelas pastas a partir do código e também olha dentro de uma pasta
    chamada OUTREM, caso o código tenha sido copiado para fora do repositório.
    """
    for pasta in [PASTA_CODIGO, *PASTA_CODIGO.parents]:
        for candidata in (pasta, pasta / "OUTREM"):
            if (candidata / "Personagens").is_dir() and (candidata / "Ambientes").is_dir():
                return candidata
    raise FileNotFoundError(
        "Não achei as pastas 'Personagens' e 'Ambientes'. "
        "Coloque esta pasta de código dentro do repositório OUTREM "
        f"(procurei a partir de: {PASTA_CODIGO})."
    )


RAIZ = _achar_raiz()
PASTA_PERSONAGENS = RAIZ / "Personagens"
PASTA_AMBIENTES = RAIZ / "Ambientes"
