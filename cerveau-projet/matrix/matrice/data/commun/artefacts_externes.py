"""artefacts_externes -- le DOMICILE des ARTEFACTS EXTERIEURS declares (EO-408).

POURQUOI CE FICHIER EXISTE. Le garde du perimetre d'ecriture
(`_operateur/optimus-prime/super-combos/combos/outils/garde-perimetre-write.py`) juge
les fichiers MODIFIES HORS de `matrix/` : c'est la regle WRITE=matrix/ (M-098).
Mesure du 2026-09-24 : il rendait code 1 pour 4550 fichiers hors de la Matrice, TOUS
sous `.kilo/worktrees/lemon-aardwolf` -- un WORKTREE d'un outil ETRANGER, ne deux
minutes avant le demarrage de la session. AUCUNE ecriture de la v3 n'avait eu lieu :
le rouge venait d'un artefact exterieur, et il repartait tout seul a la disparition
du worktree (meme classe que l'incident MO-187). Un rouge qui depend d'un artefact
exterieur ne garde pas la regle, il la brouille.

CE QUE CE FICHIER DECLARE : les ARBRES d'un outil etranger a la v3, qui vivent dans
le workspace mais que la v3 n'ecrit JAMAIS. La declaration est ETROITE (une racine
nommee, relative a la RACINE DU WORKSPACE) et VISIBLE : le garde DIT ce qu'il met de
cote, COMBIEN de fichiers, et de QUAND date l'artefact. Une exemption muette serait
un angle mort (doctrine des exemptions visibles, MO-075) -- et une exemption large
(< tout ce qui est cache >) rendrait le garde aveugle a ce qu'il doit garder.

CE QU'IL NE FAIT PAS : il ne juge pas -- il NOMME. Le verdict reste au garde.
"""

import sys
from datetime import datetime
from pathlib import Path

# `racine.py` est un VOISIN de ce module (data/commun) : le chemin est pose pour que
# l import marche meme quand le module est charge seul, et non seulement par un
# consommateur qui a deja insere data/commun dans son sys.path.
_DOSSIER_COMMUN = Path(__file__).resolve().parent
if str(_DOSSIER_COMMUN) not in sys.path:
    sys.path.insert(0, str(_DOSSIER_COMMUN))

from racine import detecter_racine  # noqa: E402

# Le dossier de l'outil EXTERIEUR, a la racine du workspace (celle qui porte AGENTS.md).
DOSSIER_OUTILS_EXTERNES = ".kilo"

# NOM et MOTIF de la zone, demandes par les gardes qui la consomment (MO-497) : la
# declaration d une zone est son nom + son motif + son predicat, et les TROIS
# appartiennent a ce fichier -- un garde qui reecrirait le motif ici ferait dire autre
# chose a deux instruments (MO-492, M-076).
NOM_ARTEFACTS_EXTERNES = "artefacts-externes"
MOTIF_ARTEFACTS_EXTERNES = (
    "arbres d'un outil ETRANGER a la v3 (worktrees du harnais) : hors de la Matrice, "
    "hors de tout ecriture de la v3 -- comptes A PART et NOMMES avec leur date de "
    "naissance (EO-408), jamais modifies"
)

# Les RACINES declarees, sous ce dossier : ce sont des arbres d'un outil etranger,
# pas ceux de la v3. Ajouter une racine = une DECISION, tracee ici -- jamais un nom
# invente au fil d'un incident.
#
# MO-487 (EO-462) : la racine VIDE `()` declare le DOSSIER `.kilo` LUI-MEME -- donc
# tout ce que l'outil etranger ecrit dans son propre dossier, son `.gitignore`
# compris. Mesure du 2026-09-28 : `.kilo/.gitignore` (ecrit par l'outil, HORS de
# `.kilo/worktrees`) faisait allumer le declencheur defcon `perimetre-write`
# (niveau 5) alors que le worktree voisin, lui, etait deja mis de cote : un artefact
# declare A MOITIE laisse un rouge qu'on doit se rappeler normal -- le defaut exact
# que le createur a demande d'inverser. La v3 n'ecrit JAMAIS dans `.kilo` : la
# declaration reste NOMMEE (une racine precise), elle n'est pas un < tout ce qui est
# cache >. L'ORDRE compte : `worktrees` AVANT, pour que le worktree reste NOMME avec
# sa date de naissance (EO-408), au lieu d'etre noye dans `.kilo`.
RACINES_ARTEFACTS = (("worktrees",), ())


def chemins_artefacts(racine):
    """Les chemins des racines d'artefacts DECLAREES, sous la racine du workspace."""
    return [
        Path(racine).joinpath(DOSSIER_OUTILS_EXTERNES, *morceaux)
        for morceaux in RACINES_ARTEFACTS
    ]


def artefact_de(chemin_resolu, racine):
    """L'ARTEFACT qui contient <chemin_resolu>, ou None. Un artefact est NOMMABLE.

    Rend le chemin du SOUS-ARBRE precis quand il y en a un (le worktree, qui porte sa
    date de naissance) : un simple < c'est un artefact > ne suffit pas a un rapport --
    le garde doit pouvoir dire QUEL artefact, COMBIEN de fichiers, et NE QUAND.
    """
    resolu = Path(chemin_resolu)
    for candidat in chemins_artefacts(racine):
        try:
            relatif = resolu.resolve().relative_to(candidat.resolve())
        except (ValueError, OSError):
            continue
        if relatif.parts:
            return candidat.joinpath(relatif.parts[0])
        return candidat
    return None


def est_artefact_externe(chemin):
    """True si <chemin> est dans un artefact EXTERNE DECLARE (M-497, MO-497).

    Le PREDICAT que les gardes consomment : il ne demande PAS la racine du workspace a
    l appelant, il la DETECTE (racine.py) -- sinon chaque consommateur devrait
    redemander la racine et le criteria vivrait a plusieurs endroits (M-076). Un
    appelant qui n arrive pas a detecter la racine n accorde AUCUNE exemption :
    mieux vaut un garde qui accuse trop qu une exemption muette (MO-075).
    """
    try:
        resolu = Path(chemin).resolve()
    except (OSError, RuntimeError):
        return False
    # `detecter_racine` ne rend PAS None hors workspace : il LEVE. Mesure du jour --
    # suppose non, ce predicat non protege faisait tomber le garde EN FIN DE COURSE
    # sur tout fichier pose hors du workspace, et le garde rendait alors 1 (le bon
    # code) SANS nommer la violation : le contre-temoin du maillon 67 s en apercut
    # sans qu'aucun message ne dise pourquoi. Une exception non nommee est un garde
    # muet qui pretend travailler.
    try:
        racine = detecter_racine(resolu)
    except (OSError, RuntimeError, ValueError):
        return False
    return artefact_de(resolu, racine) is not None


def date_de_naissance(chemin):
    """La date de naissance d'un artefact (`%Y-%m-%d %H:%M:%S`), ou None si illisible.

    Windows et POSIX ne datent pas la creation de la meme facon : `st_birthtime`
    d'abord (le vrai instant de naissance), puis `st_ctime`. Rendre None vaut
    < je ne sais pas date cet artefact > -- jamais une date inventee : l'appelant le
    DIT a l'affichage.
    """
    try:
        stat = Path(chemin).stat()
    except OSError:
        return None
    for champ in ("st_birthtime", "st_ctime"):
        valeur = getattr(stat, champ, None)
        if valeur:
            try:
                return datetime.fromtimestamp(valeur).strftime("%Y-%m-%d %H:%M:%S")
            except (OSError, OverflowError, ValueError):
                return None
    return None
