"""vivacite -- la sonde UNIQUE qui dit si un PID designe un processus VIVANT.

POURQUOI CE DOMICILE (M-076, L-029) : `processus_vivant` vivait en DEUX copies --
`matrice/routines/vie/fonctions.py` (la vie des routines) et le maillon 7 du flux
(`lanceur-non-regression-flux.py`) -- et une TROISIEME copie allait naitre pour la
garde de double lancement du routeur (EO-404). Trois copies de la meme sonde, ce
sont trois verites : une routine declaree morte par l'une et vivante par l'autre,
et une relance refusee sur un PID fantome que personne ne verifiait.

LA SONDE, dans l'ordre :
  - Windows natif : Win32 (OpenProcess) est PRIORITAIRE. `os.kill` et `ps` peuvent
    voir une couche Git/WSL differente du processus reel et rendre un faux negatif
    -- un faux "mort" relance une routine qui vit, un faux "vivant" laisse morte
    une routine que plus personne ne relance.
  - POSIX : `os.kill(pid, 0)` d'abord, `ps -p` en secours.

Un PID absent, nul, negatif ou illisible rend False : la question posee est
"y a-t-il un processus derriere ce numero ?", pas "ce numero est-il bien forme ?".
"""


import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, lot -- fin du residu) -----------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Bloc AUTOSUFFISANT : il ne depend ni de l ordre des imports du fichier, ni de la
# presence d un `import subprocess` de module (mesure du 2026-09-25 : deux fichiers
# casses par ces deux pieges, invisibles au py_compile).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())


import os
import sys

# Droit d'ouverture minimal qui suffit a CONSTATER la presence d'un processus :
# SYNCHRONIZE. On n'interroge rien, on ne lit rien, on ne modifie rien.
DROIT_SYNCHRONIZE = 0x00100000


def processus_vivant(pid):
    """True si un processus porte ce PID -- False sinon (absent, mort, illisible)."""
    try:
        numero = int(pid)
    except (TypeError, ValueError):
        return False
    if numero <= 0:
        return False

    if sys.platform == "win32" or os.name == "nt":
        try:
            import ctypes
            noyau = ctypes.windll.kernel32
            poignee = noyau.OpenProcess(DROIT_SYNCHRONIZE, False, numero)
            if poignee:
                noyau.CloseHandle(poignee)
                return True
        except Exception:
            pass
        return False

    try:
        os.kill(numero, 0)
        return True
    except OSError:
        pass
    try:
        import subprocess
        resultat = lancer_enfant(
            ["ps", "-p", str(numero)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
        return resultat.returncode == 0
    except Exception:
        return False
