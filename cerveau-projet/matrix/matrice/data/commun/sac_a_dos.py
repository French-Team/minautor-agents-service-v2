"""Sac a dos embarque : chaque outil note LUI-MEME ses usages en BDD (M-076).

Porte unique respectee : la note part par l'outil bdd-usages (subprocess),
jamais d'ecriture directe du journal (proto-7). Un echec de notation
n'arrete JAMAIS l'outil (best-effort, comme la veille-flux).
bdd-usages ne se note pas lui-meme : le garde OUTIL_EXCLU interdit la recursion.

Amelioration (audit protections 2026-09-09, decision createur) : quand l'outil
REFUSE (code != 0), le message de protection (lignes REFUS) est note en DETAIL
dans la BDD -- le sac a dos devient le journal des protections declenchees
(raison tracee, pas seulement le code). La sortie console reste inchangee.

Espion tokens (E-097, imperatif 56) : chaque appel note aussi le POIDS du
contexte -- tokens AVANT (l'ordre donne a l'outil : sa commande et ses
arguments) et tokens APRES (la sortie que le LLM devra lire). Estimation
DETERMINISTE (1 token ~ 4 caracteres) via data/commun/tokens.py : la Matrice ne
voit pas la tokenisation du LLM, elle mesure un POIDS. L'ecart avant/apres
designe les outils bavards, exactement ce qu'un centre de controle veut voir.
"""


import os
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

import contextlib
import io
import subprocess
import sys
import time
from pathlib import Path

try:
    from tokens import estimer_tokens, peser_tokens
except ImportError:  # importe comme paquet (chemin complet)
    from commun.tokens import estimer_tokens, peser_tokens

# T1 de la chaine PB-002 : le refus de l OPTION EN TETE vit au DOMICILE
# (options.py) -- le sac a dos le CONSOMME, il ne le recopie jamais (M-076).
try:
    from options import nom_de_l_outil, refuser_option_en_tete
except ImportError:  # importe comme paquet (chemin complet)
    from commun.options import nom_de_l_outil, refuser_option_en_tete

REPERTOIRE_COMMUN = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_COMMUN.parent
OUTIL_EXCLU = "bdd-usages"
TAGS_SAC_A_DOS = "sac-a-dos"

# LE CANAL DE DECLARATION D UNE SONDE (MO-555).
#
# POURQUOI IL EXISTE. Un harnais appelle une porte FAUX VOLONTAIREMENT pour
# verifier que son refus fonctionne : sc-004 pose une option bidon, la suite de
# non-regression appelle un segment inexistant. Ces appels sortent en code 2,
# exactement comme ceux d un appelant qui se trompe. Sans distinction, la metrique
# < porte mal utilisee > compte une sonde comme une faute et noie les vraies
# alertes sous des centaines de harnais (mesure : 34 alertes, dont 274/274 sur
# plusieurs portes).
#
# POURQUOI UNE VARIABLE D ENVIRONNEMENT. L usage est ecrit ici et ICI SEUL :
# noter_usage impose `--tags sac-a-dos` en dur, donc le harnais ne peut pas
# passer un tag par la ligne de commande, et le journal ne porte aucun champ
# appelant (mesure sur 44 597 evenements : 4 valeurs de tags, aucune declarative).
# L environnement est donc le SEUL canal qui existe sans rien inventer d autre.
# Le harnais la pose autour de son appel et la retire apres : la declaration vaut
# pour CE coup-la, pas pour la suite.
#
# CE QUE LA DECLARATION NE FAIT PAS. Elle ne supprime rien, elle ne corrige
# rien, elle ne rend pas un refus muet : l usage reste note, le refus reste
# visible, et le tag se lit. C est une DECLARATION, pas un privilege -- un
# appelant qui se trompe n a aucune raison de la poser, et si un jour il la pose,
# la ligne qu il produit le dit.
VARIABLE_SONDE = "MATRICE_SONDE"
TAG_SONDE = "sonde"


def tags_de_notation():
    """Les tags de l usage note, sac-a-dos TOUJOURS, sonde SI elle est declaree.

    Fonction PURE : elle ne lit que l environnement, elle n ecrit rien et ne
    lance rien. Le sac-a-dos reste donc best-effort : une declaration illisible
    (pas une chaine) ne fait pas echouer la notation.
    """
    tags = [TAGS_SAC_A_DOS]
    if os.environ.get(VARIABLE_SONDE):
        tags.append(TAG_SONDE)
    return tags
CHEMIN_BDD_USAGES = REPERTOIRE_DATA / "outils" / OUTIL_EXCLU
TIMEOUT_NOTATION = 30
LONGUEUR_MAX_DETAIL = 300


def extraire_protection(sortie):
    """Retourne le message de protection declenchee (lignes REFUS), tronque.

    Priorite aux lignes portant le marqueur REFUS (protection explicite) ;
    a defaut, la derniere ligne non vide (message d'erreur). Vide si aucune.
    """
    lignes = [ligne.strip() for ligne in sortie.splitlines() if ligne.strip()]
    refus = [ligne for ligne in lignes if "REFUS" in ligne]
    if refus:
        return (" | ".join(refus))[:LONGUEUR_MAX_DETAIL]
    if lignes:
        return lignes[-1][:LONGUEUR_MAX_DETAIL]
    return ""


def noter_usage(arguments, code, duree_ms, detail="", tokens_avant=0, tokens_apres=0):
    """Note UN usage via bdd-usages (porte unique). Echec jamais bloquant.

    Porte aussi le poids du contexte (espion E-097) : tokens avant (l'ordre)
    et tokens apres (la sortie).
    """
    nom_outil = nom_de_l_outil()
    if nom_outil == OUTIL_EXCLU:
        return
    commande = arguments[0] if arguments else "-"
    contenu = [
        sys.executable, "main.py", "noter",
        "--outil", nom_outil, "--commande", commande,
        "--code", str(code), "--duree", str(duree_ms),
        "--tokens-avant", str(tokens_avant), "--tokens-apres", str(tokens_apres),
        "--tags", ",".join(tags_de_notation()),
    ]
    if detail:
        contenu += ["--detail", detail]
    try:
        termine = lancer_enfant(
            contenu,
            cwd=str(CHEMIN_BDD_USAGES),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_NOTATION,
        )
    except (OSError, subprocess.TimeoutExpired) as erreur:
        print("sac-a-dos : notation impossible (" + type(erreur).__name__ + ")", file=sys.stderr)
        return
    if termine.returncode != 0:
        print("sac-a-dos : notation refusee (code " + str(termine.returncode) + ")", file=sys.stderr)


def noms_declares(declaration):
    """Les NOMS de verbes d une DECLARATION, ou None si elle n en declare aucun.

    LA FORME NE DECIDE PAS, LA DECLARATION DECIDE (T4 de PB-002, 2026-09-20) :
    l outil peut declarer ses verbes par la TABLE DE ROUTAGE `COMMANDES =
    {verbe: handler}` (l usage majoritaire) OU par une SUITE DE NOMS
    (`COMMANDES = ("a", "b")`, ou `VERBES = [...]`). Les deux formes expriment
    exactement la meme intention -- "cet outil attend un VERBE en tete" -- et
    seule la seconde etait ignoree. Mesure : deux outils neufs declaraient leurs
    verbes en TUPLE ; ils ECHAPPAIENT donc au refus nomme, une option en tete
    rendait leur doc sans jamais la nommer (sonde sc-004 : 2 ecarts).
    Seules les CLES d un dict sont des noms (jamais les handlers).
    """
    if isinstance(declaration, dict):
        noms = [cle for cle in declaration if isinstance(cle, str)]
        return noms or None
    if isinstance(declaration, (list, tuple, set, frozenset)):
        noms = [element for element in declaration if isinstance(element, str)]
        return noms or None
    return None


def commandes_de(principal):
    """Les VERBES declares par le module de l'outil, ou None s il n en declare pas.

    Convention d architecture : un outil qui declare un VERBE attend un VERBE en
    tete ; une option a cette place est une FAUTE, qui se DIT (T1). Un outil qui ne
    declare pas de verbes accepte une option en tete (mesure 2026-09-20 : 6 outils)
    et n est JAMAIS accuse a tort : chez lui, le refus appartient au parseur
    d options. La declaration de l OUTIL decide, jamais une liste tenue ici.

    La declaration est lue dans TOUTES ses formes legitimes -- `COMMANDES` (table
    de routage OU suite de noms), puis `VERBES` en secours (noms_declares) : une
    forme non reconnue faisait ECHAPPER l outil au refus nomme en silence (T4).
    """
    globales = getattr(principal, "__globals__", None) or {}
    for nom in ("COMMANDES", "VERBES"):
        verbes = noms_declares(globales.get(nom))
        if verbes:
            return verbes
    return None


def envelopper(principal, arguments):
    """Execute principal(arguments), chronometre, note l'usage, retourne le code.

    La sortie console est capturee puis reaffichee a l'identique (rien ne
    change pour l'appelant) ; en cas de refus (code != 0), le message de
    protection est note en detail dans la BDD usages.

    T1 de la chaine PB-002 (2026-09-20) : deux garde-fous, poses ICI parce que ce
    point est commun a TOUS les outils.
      1. L OPTION EN TETE : une option la ou un VERBE est attendu est REFUSEE et
         NOMMEE, par le message du domicile (options.py). Sans cela, 28 outils
         imprimaient leur doc sans jamais nommer l option fautive (sonde sc-004 :
         32 ecarts mesures le 2026-09-20).
      2. L ARRET FORCE COMPRIS : un `SystemExit` leve par le refus par defaut du
         domicile sortait du `with` sans reafficher la sortie capturee -- le refus
         devenait MUET pour l appelant. Le code est desormais rendu comme les
         autres et l usage est note (un refus est un usage).
    """
    nom_outil = nom_de_l_outil()
    debut = time.monotonic()
    # Espion tokens (E-097) : AVANT = l'ordre donne (la commande et ses arguments).
    tokens_avant = peser_tokens(" ".join(str(morceau) for morceau in arguments))
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        code_tete = refuser_option_en_tete(arguments, nom_outil,
                                           commandes=commandes_de(principal))
        if code_tete:
            code = code_tete
        else:
            try:
                code = principal(arguments)
            except SystemExit as arret:
                # sys.exit(2) -> 2 ; sys.exit("message") -> 1 ; sys.exit() -> 0.
                if isinstance(arret.code, int):
                    code = arret.code
                elif arret.code is None:
                    code = 0
                else:
                    print(str(arret.code))
                    code = 1
    duree_ms = int((time.monotonic() - debut) * 1000)
    sortie = tampon.getvalue()
    if sortie:
        sys.stdout.write(sortie)
    # APRES = la sortie produite (ce que le LLM devra lire).
    tokens_apres = estimer_tokens(sortie)
    detail = extraire_protection(sortie) if code != 0 else ""
    noter_usage(arguments, code, duree_ms, detail, tokens_avant, tokens_apres)
    return code
