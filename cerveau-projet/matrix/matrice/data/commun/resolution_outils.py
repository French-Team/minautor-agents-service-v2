"""Resolution d'une BRIQUE du workspace par son NOM (source UNIQUE, EO-287 / MO-295).

Pourquoi ce module existe : les appelants INTERNES recopiaient chacun le chemin de la
brique qu'ils appelaient (`data/outils/<nom>/main.py`). Le jour ou l'outil est renomme ou
deplace, l'appel echouait SANS DIRE POURQUOI -- un traceback opaque au lieu d'un refus
nomme. Ici la resolution ET le refus vivent UNE fois (M-076, zero duplication) ; la facade
CLI `matrix/lancer.py` les reutilise, et les documents (le demarrage) n'ecrivent plus de
chemin de brique a la main.

QUATRE FAMILLES, dans l'ORDRE de priorite :
  1. `outil`     : `matrice/data/outils/<nom>/main.py`      (enfant DIRECT) ;
  2. `routine`   : `matrice/routines/<nom>/main.py`         (enfant DIRECT) ;
  3. `operateur` : `_operateur/optimus-prime/**/main.py`,   profondeur BORNEE (<= 2) ;
  4. `combo`     : les DOSSIERS-briques du parc des combos (`c-00X-<nom>`,
                 et les outils transverses sous `combos/outils/`) ;
  5. `script`    : les .py des domiciles DECLARES de l'operateur (`<nom>.py`).
  6. derniere regle : un chemin `.py` EXISTANT (un script qui n'est pas une brique).

Pourquoi l'operateur (MO-295) : le pilote et l'entonnoir d'Optimus n'ont pas de main.py
sous `data/outils` -- ils n'etaient donc PAS nommables, et le demarrage les ecrivait en
chemin ancre recopie. La profondeur est BORNEE parce qu'une fouille large ramasserait les
entrailles des combos et de la zone jetable, qui ne sont pas des briques de commande.

Contrat :
    chemin_outil(nom) -> Path du main.py, ou leve OutilIntrouvable (refus nomme).
    resoudre(nom)     -> (chemin, None) ou (None, message) : la facade CLI.

Le refus NOMME dit le nom fautif, les noms proches et le remede -- il ne devine jamais,
et il ne rend JAMAIS None en silence.
"""
from pathlib import Path

# LA REGLE DES NOMS PROCHES VIT A UN SEUL DOMICILE (M-076 / MO-468) : elle est
# CONSOMMEE ici, jamais recopiee. Les DEUX noms du domicile sont importes -- la
# constante du seuil est un RE-EXPORT (les lecteurs d avant la trouvent au meme
# endroit), la borne des proches est utilisee par le refus de ce module.
from noms_proches import NOMBRE_PROCHES, SEUIL_PROXIMITE, proches  # noqa: F401


# La racine se DETECTE par le motif partage (L-013 / MO-088) : jamais `parents[N]`
# nus, qui cassent a la premiere profondeur qui change. `cible` porte le motif.
from cible import racine_matrice

RACINE_MATRIX = racine_matrice(__file__)
RACINE_MATRICE = RACINE_MATRIX / "matrice"
DOSSIER_OUTILS = RACINE_MATRICE / "data" / "outils"
DOSSIER_ROUTINES = RACINE_MATRICE / "routines"

# L'ordre fait la PRIORITE : un outil avant une routine homonyme (meme regle
# que la facade matrix/lancer.py, qui lit ce module).
FAMILLES = (("outil", DOSSIER_OUTILS), ("routine", DOSSIER_ROUTINES))

# --- L'OPERATEUR : ses briques vivent HORS de la Matrice --------------------
# Le domicile est DECLARE (meme motif que `zone_tmp.DOMICILE_ZONE_OPTIMUS`), jamais
# un chemin invente au fil de l'eau.
DOMICILE_OPERATEUR = ("_operateur", "optimus-prime")
DOSSIER_OPERATEUR = RACINE_MATRIX.joinpath(*DOMICILE_OPERATEUR)
FAMILLE_OPERATEUR = "operateur"
FAMILLE_SCRIPT = "script"
# LA FAMILLE EN COMBO (MO-575) : les outils transverses sont des DOSSIERS, pas
# des .py a plat. Leur domicile est DECLARE comme les autres -- jamais un chemin
# invente au fil de l'eau (M-076).
FAMILLE_COMBO = "combo"
DOMICILE_COMBOS = ("super-combos", "combos")
DOMICILE_OUTILS_TRANSVERSES = ("super-combos", "combos", "outils")
# Les COMBOS sont des dossiers-briques directs ; les outils transverses sont
# des dossiers-briques un cran plus bas (ils vivent DANS le parc des combos).
# DEUX MOTIFS, UNE SEULE FAMILLE : un motif elargi ramasserait les entrailles.
MOTIFS_COMBO = ("*/main.py", "outils/*/main.py")
# Un dossier-cache de Python n est pas une brique : le motif des .bak ecarte les
# copies, celui-ci ecarte le cache.
NOMS_ECARTES = ("__pycache__",)
# BORNEE : l'entonnoir range un cran sous le pilote, les combos un cran sous
# `super-combos`. Aller plus bas ramasserait un cobaye, pas une brique.
PROFONDEUR_OPERATEUR = 2
# La ZONE JETABLE n'est pas un domicile : un cobaye ne doit pas devenir une brique.
ZONES_EXCLUES = ("tmp-optimus",)
# Les domiciles ou un `.py` EST une commande (brique) de l'operateur.
DOMICILES_SCRIPTS = ("super-combos/combos/outils", "super-combos", "cockpit",
                     "espions", "remorque")
MOTIF_BRIQUE = "*/main.py"

_CACHE = None


class OutilIntrouvable(RuntimeError):
    """Le nom ne resout aucune brique : le message EST le refus nomme."""


def briques_operateur(profondeur=PROFONDEUR_OPERATEUR):
    """Les briques de l'operateur (`main.py`) a une profondeur BORNEE.

    Le cran 1 porte le pilote, le cran 2 l'entonnoir et les entrees des super-combos.
    La zone jetable est ECARTEE : un cobaye n'est pas une brique.
    """
    if not DOSSIER_OPERATEUR.is_dir():
        return []
    trouves = []
    for cran in range(1, profondeur + 1):
        motif = "/".join(["*"] * cran) + "/main.py"
        trouves.extend(p for p in DOSSIER_OPERATEUR.glob(motif)
                       if not any(zone in p.parts for zone in ZONES_EXCLUES))
    return sorted(trouves)


def briques_combos(domiciles=None):
    """Les briques EN COMBO : des DOSSIERS-briques, la ou le parc attendait des .py.

    MESURE (MO-575, 2026-10-04) : la profondeur BORNEE de l operateur s arrete au
    cran 2, et `scripts_operateur` ne glob que les `.py` du dossier LUI-MEME. Les
    briques du parc des combos sont des DOSSIERS plus bas que ca : onze d entre
    elles portaient au registre des outils `servi_a_l_injection` VRAI et etaient
    REFUSEES par le lanceur sous le nom qu elles portent -- une porte qui parle
    sans agir. Les trois premieres mesurees sont les BDD sous `combos/outils/`, les
    huit autres les COMBOS `c-00X` ; meme cause, meme remede.

    LA FAMILLE EST DECLAREE, la profondeur n est pas elargie : elargir ramasserait
    les entrailles de tous les dossiers du parc. Ici un dossier n est une brique que
    s il porte un `main.py` -- le meme contrat que les autres familles -- et la zone
    jetable reste ecustee comme partout ailleurs.

    `domiciles` est la liste des DOMICILES qui CONTIENNENT les briques (le meme sens
    que le glob `*/main.py` applique), pas la brique elle-meme. Par defaut c est le
    parc des combos et le dossier des outils qui sont une entree du meme.
    """
    if domiciles is None:
        domiciles = [DOSSIER_OPERATEUR.joinpath(*DOMICILE_COMBOS),
                     DOSSIER_OPERATEUR.joinpath(*DOMICILE_OUTILS_TRANSVERSES)]
    trouves = []
    for domicile in domiciles:
        domicile = Path(domicile)
        if not domicile.is_dir():
            continue
        for motif in MOTIFS_COMBO:
            for principal in domicile.glob(motif):
                if any(zone in principal.parts for zone in ZONES_EXCLUES):
                    continue
                nom = principal.parent.name
                if nom.startswith(".") or nom in NOMS_ECARTES:
                    continue
                trouves.append(principal)
    return sorted(set(trouves))


def scripts_operateur():
    """Les `.py` des domiciles DECLARES -- un script nomme y est une commande."""
    trouves = []
    for chemin in DOMICILES_SCRIPTS:
        dossier = DOSSIER_OPERATEUR / chemin
        if not dossier.is_dir():
            continue
        trouves.extend(p for p in dossier.glob("*.py") if ".bak" not in p.name)
    return sorted(trouves)


def entrer_outils():
    """(famille, nom, main.py) pour chaque brique resolvable par son NOM."""
    briques = []
    for famille, dossier in FAMILLES:
        if not dossier.is_dir():
            continue
        for principal in sorted(dossier.glob(MOTIF_BRIQUE)):
            briques.append((famille, principal.parent.name, principal))
    for principal in briques_operateur():
        briques.append((FAMILLE_OPERATEUR, principal.parent.name, principal))
    for principal in briques_combos():
        briques.append((FAMILLE_COMBO, principal.parent.name, principal))
    for principal in scripts_operateur():
        briques.append((FAMILLE_SCRIPT, principal.stem, principal))
    return briques


def par_nom():
    """Le nom -> sa brique, dans l'ORDRE de priorite des familles (jamais devine)."""
    global _CACHE
    if _CACHE is None:
        _CACHE = {}
        for _, nom, principal in entrer_outils():
            _CACHE.setdefault(nom, principal)
    return _CACHE


def noms_connus():
    """Les noms resolvables, tries -- sert au refus (noms proches) et au --lister."""
    return sorted(par_nom())


# --- LA REGLE DES NOMS PROCHES : CONSOMMEE, jamais recopiee (M-076 / MO-468) -----
# Elle vit a UN SEUL domicile (data/commun/noms_proches.py) depuis que le refus du
# PILOTE la consomme aussi : deux copies d une meme regle divergent en silence, et
# celles-ci avaient DEJA diverge -- celle du pilote ne cherchait que la SOUS-CHAINE,
# donc un nom fautif d UNE LETTRE n y proposait rien. Le seuil et la borne des
# proches sont importes en tete de module avec la regle, et RE-EXPORTES ici : la
# facade `lancer.py` et les lecteurs d avant les trouvent au meme endroit.


def noms_proches(nom, noms=None):
    """Les noms PROCHES d un nom fautif, parmi les briques resolvables (ou `noms`).

    LA REGLE N EST PAS ICI (M-076) : cette fonction lui DONNE le parc -- les noms
    connus de la facade, ou la liste recue -- et rend sa reponse telle quelle. Un
    nom vide et un nom sans sosie restent donc traites par le domicile, une seule
    fois pour les DEUX consommateurs.
    """
    parc = noms_connus() if noms is None else list(noms)
    return proches(nom, parc)


def refus_nom(nom):
    """Le refus NOMME : le nom fautif, les noms proches, le remede."""
    trouves = noms_proches(nom)
    message = "nom inconnu : " + nom
    if trouves:
        message += " -- proches : " + ", ".join(trouves[:NOMBRE_PROCHES])
    message += " -- remede : --lister, ou un .py existant (chemin ancre)"
    return message


def resoudre(nom):
    """Rend (main.py, None) ou (None, refus nomme).

    Un chemin .py EXISTANT reste accepte (derniere regle) : la facade CLI sert
    aussi a lancer un script qui n'est pas une brique nommee.
    """
    connu = par_nom().get(nom)
    if connu is not None:
        return connu, None
    direct = Path(nom)
    if nom.endswith(".py") and direct.is_file():
        return direct.resolve(), None
    return None, refus_nom(nom)


def chemin_outil(nom):
    """Rend le main.py de la brique <nom> -- ou REFUSE en la nommant.

    Aucun appelant ne fabrique ce chemin lui-meme : un chemin recopie ne se
    plaint jamais quand l'outil disparait, il rend un traceback opaque.
    """
    chemin, refus = resoudre(nom)
    if refus is not None:
        raise OutilIntrouvable(refus)
    return chemin
