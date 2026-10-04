#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cockpit-matrice.py -- Cockpit prive d'Optimus (M-129)

La Matrice comme serveur distant. Routes privees verrouillees, lecture
seule, jamais d'ecriture. Domicile : _operateur/optimus-prime/cockpit/
(Flux 2, zone maintenance,_operateur => invisible cameleon, L-016).

Usage: python cockpit-matrice.py --route <etat|sante|flux1|flux2|chercher|metriques|remise|complet> [--json] [--racine .] [--requete <texte>]
  --route   : une ou plusieurs separees par virgule, defaut: complet
  --json    : sortie machine (JSON)
  --racine  : racine projet (defaut: cwd, detectee via data/commun/racine.py)
  --requete : route /chercher seulement -- texte a chercher dans toute la Matrice
              (sans lui, un temoin prouve que la porte unique repond)
"""
import argparse
import collections
import importlib.util
import json
import re
import statistics
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 4 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
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

import sys
from pathlib import Path

COCKPIT_DIR = Path(__file__).resolve().parent
# _operateur/optimus-prime/cockpit -> matrix -> cerveau-projet
REPERTOIRE_MATRIX = COCKPIT_DIR.parent.parent.parent  # matrix
if REPERTOIRE_MATRIX.name != "matrix":
    raise RuntimeError("Structure inattendue : cockpit n'est pas dans matrix/_operateur/optimus-prime/cockpit")
REPERTOIRE_MATRICE = REPERTOIRE_MATRIX / "matrice"
REPERTOIRE_DATA = REPERTOIRE_MATRICE / "data"
REPERTOIRE_OP = REPERTOIRE_MATRIX / "_operateur" / "optimus-prime"
# data/commun = motif unique racine (M-076) : detecter_racine
sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
from racine import detecter_racine  # noqa: E402
# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : --route est une LISTE
# ("sante,flux2") ; son caractere appartient a son domicile, jamais au cockpit.
from transport_listes import decouper_liste  # noqa: E402
# Le PLAFOND des boites intercom se LIT chez son domicile (lecteur PARTAGE, M-076) :
# le cockpit ne recopie aucune valeur, il mesure et il cite sa source.
from rotation_journal import lire_constante_declaree, lire_constante_texte  # noqa: E402

ENCODAGE = "utf-8"
ROUTES = ("etat", "sante", "flux1", "flux2", "chercher", "metriques", "remise", "complet")
ROUTES_EXPANDED = ("etat", "sante", "flux1", "flux2", "chercher", "metriques", "remise")

# --- ENCART /remise (MO-474) : LE POIDS DE REMISE PAR ROUND -------------------
# Demande createur (2026-09-26) : surveiller dans le TEMPS le poids de la fiche que
# l agent lit a chaque round (MO-471/472/473). La serie se DERIVE de l outbox des
# injections -- aucune ecriture, vue REGENERABLE. Le PLAFOND et les FONCTIONS de la
# fiche ne sont PAS recopies : ils sont CONSOMMES chez leur domicile
# (injection/fonctions.py), comme le cockpit consomme deja les autres (M-076).
CHEMIN_OUTBOX_FLUX = ("_operateur", "maintenance", "pilote", "outbox.jsonl")
LIGNES_REMISE_SERIE = 12
# --- TENDANCE (MO-476) : l evolution se LIT SUR LA SERIE ----------------------
# Demande createur (2026-09-26) : montrer AUSSI le poids de l injection ENTIERE et
# son evolution dans le TEMPS. Une tendance se juge sur ce que la serie FAIT (la
# moyenne d une moitie vs l autre), jamais sur deux points extremes : un pic isole
# ne fait pas une tendance. Ces deux valeurs sont une POLITIQUE D AFFICHAGE (comme
# les tailles de sortie), JAMAIS des seuils de mesure.
SEUIL_TENDANCE_POURCENT = 5
RAMPE_TENDANCE = ".:-=+*#%@"
# --- DERIVE (MO-477) : UNE HAUSSE PROLONGEE, PAS UN PIC ----------------------
# Demande createur (2026-09-26) : SIGNALER dans /remise une HAUSSE PROLONGEE du
# poids d injection. Une derive n est PAS n importe quelle hausse : c est une hausse
# de FOND (moyenne 2e moitie > 1re moitie) au-dela du seuil, CONFIRMEE par la FIN de
# la serie (les N derniers rounds tous AU-DESSUS de la moyenne de la 1re moitie).
# Un pic isole, ou une reprise qui retombe, ne fait donc pas une derive. Ces deux
# valeurs sont une POLITIQUE D AFFICHAGE, JAMAIS des seuils de mesure.
SEUIL_DERIVE_POURCENT = 10
ROUNDS_DERIVE_CONSECUTIFS = 3

# /chercher (EO-112) : la PORTE UNIQUE de recherche n'etait branchee que sur son
# temoin de veille. Le cockpit est l'endroit ou Optimus cherche a la main : il
# l'appelle donc pour de vrai. Sans --requete, un temoin prouve que la porte est
# VIVANTE (un moteur aveugle repond "0 resultat" : lecon MO-055).
REQUETE_TEMOIN = "moteur de recherche"
REQUETE_ROUTE = ""

# --- BOITES INTERCOM : MESUREES, ET JUGEES QUAND ELLES ONT UN CONTRAT (MO-322) --
# Demande createur (2026-09-20) : l outbox du flux pesait 17,5 Mo pour un plafond de
# 5 Mo et RIEN n en mesurait la TAILLE -- le cockpit n en comptait que les LIGNES,
# donc une boite qui quadruple restait invisible sous un /sante VERT. Ces listes
# disent QUI est JUGE (les boites que le pilote borne : il en repond) et QUI est
# seulement DECLARE (le heritage v2 et les boites d optimus-prime/intercom : la
# regle immuable perimetre-write interdit d y ecrire, donc on les mesure sans les
# juger -- un controle qui crie sur ce que personne ne repare ne garde plus rien).
# Le PLAFOND, lui, ne vit PAS ici : il est LU chez son domicile (les constantes du
# pilote) -- une seule source pour toute la Matrice.
CHEMIN_CONSTANTES_PILOTE = ("_operateur", "optimus-prime", "pilote", "constants.py")
NOM_CONSTANTE_SEUIL_BOITES = "SEUIL_OCTETS_BOITES_INTERCOM"
BOITES_INTERCOM_JUGEES = (
    ("pilote/outbox (flux)", ("_operateur", "maintenance", "pilote", "outbox.jsonl")),
    ("matrice/inbox (flux)", ("_operateur", "maintenance", "matrice", "inbox.jsonl")),
)
BOITES_INTERCOM_DECLAREES = (
    ("v2 pilote/outbox", ("matrice", "intercom", "pilote", "outbox.jsonl")),
    ("v2 matrice/inbox", ("matrice", "intercom", "matrice", "inbox.jsonl")),
    ("v2 cameleon/inbox", ("matrice", "intercom", "cameleon", "inbox.jsonl")),
    ("optimus-prime pilote/outbox", ("_operateur", "optimus-prime", "intercom", "pilote", "outbox.jsonl")),
    ("optimus-prime matrice/inbox", ("_operateur", "optimus-prime", "intercom", "matrice", "inbox.jsonl")),
)

# --- JOURNAUX DES ROUTINES : LE VIVANT SE JUGE, LES ARCHIVES SE DISENT (MO-324) --
# Demande createur (2026-09-20, suite de MO-322/323) : "etendre la porte de taille
# de /sante aux journaux des routines -- l espion-integrite a deja pese 87 Mo".
# Mesure du jour : l archive de l espion-integrite pese 90 580 798 o et RIEN ne la
# mesurait. Aucune liste n est ecrite ici : chaque routine DECLARE son journal
# (NOM_JOURNAL), sa borne (SEUIL_OCTETS_JOURNAL) et son prefixe d archive
# (NOM_ARCHIVE_PREFIXE) dans SON constants.py -- on LIT ces trois valeurs chez
# elle, par les lecteurs PARTAGES (entier et texte), jamais recopiees.
# Le PLANCHER de visibilite ne juge aucun journal (chacun a sa borne declaree) :
# il sert a ACCUSER un fichier du repertoire `routines/` qui grandit sans etre NI
# journal declare NI archive declaree -- c est ainsi qu une archive de 90 Mo a
# vecu sans que /sante la voie.
PLANCHER_VISIBILITE_JOURNAUX = 1024 * 1024
EXTENSIONS_JOURNAUX_SUIVIES = (".jsonl", ".txt", ".log")
# ATTENTION AUX DEUX NIVEAUX : la racine detectee est celle du WORKSPACE, et le
# dossier `matrix` contient lui-meme l arbre de la Matrice (`matrix/matrice/...`).
# C est le meme piege que REPERTOIRE_MATRICE = REPERTOIRE_MATRIX / "matrice" en
# tete de ce fichier -- et il s est paye UNE FOIS : la premiere version de cette
# porte cherchait `<matrix>/routines` et ne trouvait RIEN, donc elle rendait un
# VERT SILENCIEUX ("aucune routine ne declare de journal"). Un controle qui ne
# trouve rien doit se demander s il cherche au bon endroit : le chemin est donc
# declare ici, en morceaux, une seule fois.
REPERTOIRE_ROUTINES = ("matrice", "routines")

# --- POLITIQUE D'AFFICHAGE DU COCKPIT (jamais des mesures) -------------------
# P6 de la revue MO-098 : ces nombres ne MESURENT rien -- ils decident COMBIEN
# de texte l'operateur voit et combien de lignes une sortie garde. Ils sont
# NOMMES pour ne jamais etre pris pour un seuil de surveillance : aucun d'eux
# n'entre dans SEUILS_PERFS ; changer l'un d'eux change le confort de lecture,
# jamais la surveillance de la Matrice.
LIMITE_AFFICHAGE_CHERCHER = 10   # resultats montres par la porte de recherche
TAILLE_EXTRAIT_COURT = 300       # extrait d'une ligne ou d'un dictionnaire
TAILLE_SORTIE_STANDARD = 2000    # sortie d'un outil, format standard
TAILLE_SORTIE_LARGE = 3000       # sortie d'un outil, format large
TAILLE_SORTIE_TRES_LARGE = 4000  # sortie tres large (lecture d'une BDD)
TAILLE_SORTIE_MAXIMALE = 6000    # sortie maximale (bloc long)
LIGNES_SORTIE_COURTE = 20        # lignes gardees d'une sortie courte
LIGNES_VERDICT = 30              # lignes gardees autour d'un VERDICT
LIGNES_QUEUE_JOURNAL = 20        # queue lue dans un journal (lire tail 20)
LIGNES_ENTETE_JOURNAL = 1        # l'entete d'un journal est toujours gardee
HITS_MONTRES = 5                 # resultats detailles d'une recherche affiches


def _run(cmd, cwd=None):
    try:
        r = lancer_enfant(cmd, capture_output=True, text=True, timeout=20, cwd=cwd)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT (20s) : " + " ".join(cmd)
    except OSError as e:
        return 2, str(e)


def _read_text(path, limit=800):
    try:
        t = Path(path).read_text(encoding=ENCODAGE)
        lines = t.strip().splitlines()
        if len(lines) > limit:
            return "\n".join(lines[-limit:]) + f"\n[... {len(lines)} lignes, {limit} affichees]"
        return t.strip()
    except OSError as e:
        return f"(illisible : {e})"


def _tail_jsonl(path, n=5):
    try:
        lines = Path(path).read_text(encoding=ENCODAGE).strip().splitlines()
        tail = [l for l in lines if l.strip()][-n:]
        out = []
        for l in tail:
            try:
                j = json.loads(l)
                out.append(j)
            except ValueError:
                out.append({"brut": l[:TAILLE_EXTRAIT_COURT]})
        return out
    except OSError:
        return []


def _section(title):
    return f"\n=== /{title} ===\n"


def route_etat(racine):
    out = []
    out.append(_section("etat") + "Matrice comme serveur distant -- sante + session (lecture seule)")
    for cmd, label in [
        ([sys.executable, str(REPERTOIRE_MATRICE / "routines" / "vie" / "main.py"), "etat"], "vie etat (3 boucles)"),
        ([sys.executable, str(REPERTOIRE_MATRICE / "routines" / "vie" / "main.py"), "server", "etat"], "server etat"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "pause-session" / "main.py"), "etat"], "pause-session etat"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "pause-session" / "main.py"), "journal"], "pause-session journal (10 derniers)"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "machine-defcon" / "main.py"), "lire"], "machine-defcon lire"),
    ]:
        code, txt = _run(cmd)
        out.append(f"\n[{label}] code={code}\n" + txt.strip())
    for cle in ("defcon", "perimetre-cameleon"):
        code, txt = _run([sys.executable, str(REPERTOIRE_DATA / "outils" / "bdd-variables" / "main.py"), "lire", "--cle", cle])
        out.append(f"\n[classeur {cle}] code={code}\n" + txt.strip()[:TAILLE_SORTIE_STANDARD])
    for rel in ("matrice/inbox.jsonl", "pilote/outbox.jsonl", "cameleon/inbox.jsonl"):
        p = REPERTOIRE_MATRICE / "intercom" / rel
        try:
            n = sum(1 for _ in p.open(encoding=ENCODAGE)) if p.exists() else -1
            # MO-322 : la TAILLE accompagne les lignes -- une boite qui grandit se
            # voit ici comme dans la porte de /sante (un compte de lignes seul ne
            # dit rien du POIDS d une boite : 708 messages pesaient 17,5 Mo).
            o = p.stat().st_size if p.exists() else -1
            out.append(f"[intercom {rel}] lignes={n} octets={o}")
        except OSError as e:
            out.append(f"[intercom {rel}] {e}")
    return "\n".join(out)


def _racine_matrice(racine):
    """Le dossier matrix/ a partir de la racine passee (convention des gardes)."""
    depart = Path(racine).resolve()
    if depart.name == "matrix":
        return depart
    for candidat in (depart / "matrix", depart / "cerveau-projet" / "matrix"):
        if candidat.is_dir():
            return candidat
    return depart


def _octets_fichier(chemin):
    """Taille d un fichier en octets, ou None s il est absent ou illisible."""
    try:
        return chemin.stat().st_size
    except OSError:
        return None


def porte_boites_intercom(racine):
    """MESURE la TAILLE des boites intercom et JUGE celles qui ont un contrat.

    Mesure du defaut (2026-09-20, MO-322) : l outbox du flux portait 17 458 027
    octets, soit 3,5 fois le plafond de 5 Mo, et RIEN ne mesurait sa TAILLE -- les
    routes du cockpit n en comptaient que les LIGNES, donc une boite qui quadruple
    restait invisible sous un `/sante` VERT. Une surveillance qui ne mesure pas la
    grandeur qu elle surveille ne surveille rien.

    Le PLAFOND n est pas recopie : il est LU chez son domicile (le `constants.py`
    du PILOTE, la porte qui borne) par le lecteur PARTAGE `lire_constante_declaree`
    (M-076). Quand il est ILLISIBLE, il n est pas suppose : la porte ACCUSE en le
    nommant -- une valeur lue nulle part se lirait comme un fait (L-055).

    Les boites du HERITAGE v2 et celles d optimus-prime/intercom sont MESUREES et
    NOMMEES, jamais jugees : la regle immuable `perimetre-write` interdit d y
    ecrire, et un controle qui crie sur ce que personne ne repare ne garde plus
    rien (lecon EO-152, vraie ici une quatrieme fois).

    Rend (code, texte) : code 1 des qu une boite JUGEABLE depasse le plafond, ou
    quand le plafond lui-meme est illisible.
    """
    matrice = _racine_matrice(racine)
    lignes = ["  BOITES INTERCOM -- la taille se MESURE, le contrat se JUGE"]
    depassements = []
    seuil = lire_constante_declaree(matrice.joinpath(*CHEMIN_CONSTANTES_PILOTE),
                                    NOM_CONSTANTE_SEUIL_BOITES)
    if seuil is None:
        lignes.append("  plafond ILLISIBLE : " + NOM_CONSTANTE_SEUIL_BOITES + " absent de "
                      + str(Path(*CHEMIN_CONSTANTES_PILOTE))
                      + " -- la porte ne SUPPOSE pas un seuil, elle ne peut donc pas juger")
    else:
        lignes.append("  plafond LU chez son domicile : " + NOM_CONSTANTE_SEUIL_BOITES
                      + " = " + str(seuil) + " o")
    for nom, morceaux in BOITES_INTERCOM_JUGEES:
        octets = _octets_fichier(matrice.joinpath(*morceaux))
        if octets is None:
            lignes.append("  JUGEABLE " + nom + " : ABSENTE (" + "/".join(morceaux)
                          + ") -- une boite absente se DIT, elle ne se lit pas comme un zero")
            continue
        if seuil is not None and octets > seuil:
            depassements.append(nom + " = " + str(octets) + " o")
            lignes.append("  JUGEABLE " + nom + " : " + str(octets) + " o -- DEPASSE le plafond"
                          " (le pilote la borne a sa prochaine cloture)")
        else:
            lignes.append("  JUGEABLE " + nom + " : " + str(octets) + " o -- sous le plafond")
    for nom, morceaux in BOITES_INTERCOM_DECLAREES:
        octets = _octets_fichier(matrice.joinpath(*morceaux))
        if octets is None:
            continue
        lignes.append("  HORS CONTRAT (mesuree, non jugee) " + nom + " : " + str(octets) + " o")
    if depassements:
        return 1, "\n".join(lignes + ["  ACCUSE : " + " | ".join(depassements)])
    if seuil is None:
        return 1, "\n".join(lignes)
    return 0, "\n".join(lignes)


def _cle_chemin(chemin):
    """Cle de comparaison d un chemin (absolu si possible, en minuscules)."""
    try:
        return str(chemin.resolve()).lower()
    except OSError:
        return str(chemin).lower()


def _journaux_declares(matrice):
    """Les routines qui DECLARENT leur journal : (routine, nom, borne, prefixe).

    Aucune liste en dur : les trois valeurs sont LUES dans le `constants.py` de
    chaque routine, par les lecteurs PARTAGES (entier et texte). Une routine qui ne
    declare pas sa borne ne peut pas etre JUGEe -- elle sort de cette population,
    et ses fichiers ne tombent pas dans l oubli pour autant : les angles morts
    ci-dessous les rattrapent.
    """
    declarees = []
    repertoire = matrice.joinpath(*REPERTOIRE_ROUTINES)
    if not repertoire.is_dir():
        return declarees
    for constants in sorted(repertoire.glob("*/constants.py")):
        nom = lire_constante_texte(constants, "NOM_JOURNAL")
        borne = lire_constante_declaree(constants, "SEUIL_OCTETS_JOURNAL")
        if not nom or not borne:
            continue
        declarees.append((constants.parent.name, nom, borne,
                          lire_constante_texte(constants, "NOM_ARCHIVE_PREFIXE") or ""))
    return declarees


def porte_journaux_routines(racine):
    """MESURE la TAILLE des journaux des routines et JUGE ceux qui ont une borne.

    Demande createur (2026-09-20, suite de MO-322/MO-323) : "etendre la porte de
    taille de /sante aux journaux des routines -- l espion-integrite a deja pese
    87 Mo". Mesure du jour : l archive de l espion-integrite pese 90 580 798 o et
    RIEN ne la mesurait ; son journal VIVANT, lui, est borne par sa routine (8 Mo)
    et la rotation a joue.

    CE QUI EST JUGE : le JOURNAL VIVANT de chaque routine qui DECLARE une borne
    (`SEUIL_OCTETS_JOURNAL`, lue chez elle). Depasser sa propre borne veut dire que
    la rotation qui doit le borner n a pas tourne -- la routine est arretee ou
    cassee -- et c est exactement ce qu un cockpit doit dire.

    CE QUI EST DECLARE, JAMAIS JUGE : les ARCHIVES de ces memes routines. La
    rotation ne SUPPRIME rien (son contrat est de DEPLACER) : une archive ne peut
    donc grandir que par decision, et la borner serait une decision du createur.
    Elles sont MESUREES et NOMMEES avec leur prefixe de domicile -- une masse
    visible n est plus un angle mort.

    LES ANGLES MORTS sont ACCUSES : tout fichier du repertoire `routines/` au-dessus
    du plancher de visibilite qui n est NI un journal declare NI une archive
    declaree grandit sans que rien ne le mesure -- c est ainsi qu une archive de
    90 Mo a vecu sans que /sante la voie.

    Rend (code, texte) : code 1 des qu un journal depasse SA borne, ou qu un angle
    mort existe.
    """
    matrice = _racine_matrice(racine)
    lignes = ["  JOURNAUX DES ROUTINES -- le VIVANT se juge, les ARCHIVES se disent"]
    depassements = []
    mesures = set()
    declarees = _journaux_declares(matrice)
    if not declarees:
        lignes.append("  aucune routine ne declare de journal (NOM_JOURNAL + SEUIL_OCTETS_JOURNAL)")
    for routine, nom, borne, prefixe in declarees:
        dossier = matrice.joinpath(*REPERTOIRE_ROUTINES) / routine
        vivant = dossier / nom
        relatif = "routines/" + routine + "/" + nom
        mesures.add(_cle_chemin(vivant))
        octets = _octets_fichier(vivant)
        if octets is None:
            lignes.append("  JUGEABLE " + routine + " : journal ABSENT (" + relatif + ") -- une"
                          " absence se DIT, elle ne se lit pas comme un zero")
        elif octets > borne:
            depassements.append(relatif + " = " + str(octets) + " o")
            lignes.append("  JUGEABLE " + routine + " : " + str(octets) + " o -- DEPASSE sa borne de "
                          + str(borne) + " o : la rotation qui doit le borner n a pas tourne")
        else:
            lignes.append("  JUGEABLE " + routine + " : " + str(octets) + " o -- sous sa borne de "
                          + str(borne) + " o")
        if prefixe:
            lots = sorted(dossier.glob(prefixe + "-*"))
            total = 0
            for archive in lots:
                mesures.add(_cle_chemin(archive))
                poids = _octets_fichier(archive)
                if poids is not None:
                    total += poids
            if lots:
                lignes.append("  DECLAREE " + routine + " : " + str(len(lots))
                              + " archive(s) du prefixe `" + prefixe + "`, " + str(total)
                              + " o -- la rotation ne SUPPRIME rien : leur poids est une decision"
                              " du createur, il est MESURE et DIT")
            else:
                lignes.append("  DECLAREE " + routine + " : aucune archive du prefixe `" + prefixe + "`")
    angles = []
    repertoire = matrice.joinpath(*REPERTOIRE_ROUTINES)
    if repertoire.is_dir():
        for fichier in repertoire.rglob("*"):
            if not fichier.is_file() or fichier.suffix.lower() not in EXTENSIONS_JOURNAUX_SUIVIES:
                continue
            if _cle_chemin(fichier) in mesures:
                continue
            poids = _octets_fichier(fichier)
            if poids is None or poids < PLANCHER_VISIBILITE_JOURNAUX:
                continue
            angles.append((fichier, poids))
    if angles:
        for fichier, poids in angles:
            relatif = str(fichier.relative_to(matrice)).replace("\\", "/")
            lignes.append("  ANGLE MORT " + relatif + " : " + str(poids) + " o -- NI journal declare NI"
                          " archive declaree : rien ne le mesure (le declarer chez sa routine, ou le"
                          " faire tourner)")
            depassements.append("ANGLE MORT " + relatif + " = " + str(poids) + " o")
    else:
        lignes.append("  angle mort : AUCUN fichier au-dessus du plancher de "
                      + str(PLANCHER_VISIBILITE_JOURNAUX) + " o n echappe a la mesure")
    if depassements:
        return 1, "\n".join(lignes + ["  ACCUSE : " + " | ".join(depassements)])
    return 0, "\n".join(lignes)


# --- LE LOT ARME DU PILOTE : LA REPRISE SE LIT, ET SA MEMOIRE SE JUGE (MO-380) ---
# POURQUOI (demande du createur, 2026-09-21) : la REPRISE DU RETARD -- 37 missions
# versees d'un seul geste par `file verser` -- ne se lisait qu'en ouvrant le JSON a
# la main. Un lot qu'on ne voit pas est un lot qu'on ne suit pas.
# Le cockpit n'affiche RIEN lui-meme : il appelle le verbe du pilote (`lot etat`),
# qui est le domicile du lot. Son code entre dans le bilan comme celui des autres
# portes : un maillon qui a perdu sa memoire de naissance est ACCUSE (sans elle, son
# verdict d'origine n'est plus atteignable -- panne MO-339, mesuree), il ne se fond
# pas dans une liste de 37.
def porte_lot_arme(racine):
    cmd = [sys.executable, str(REPERTOIRE_OP / "pilote" / "main.py"), "lot", "etat"]
    code, txt = _run(cmd)
    return code, txt.strip()[:TAILLE_SORTIE_LARGE]


def route_sante(racine):
    out = []
    # Bilan des portes (label, code) : sert au VERDICT global en fin de route.
    bilan = []
    out.append(_section("sante") + "Integrite marbre + BDD (preuves SHA-256, lecture seule)")
    for cmd, label in [
        # `verifier` (et non `tour`) : cette route est en LECTURE SEULE (`ecriture: false`)
        # et un appel a la demande qui journalise 15 lignes fait grossir un journal en
        # ajout seul sans rien apporter a la surveillance (MO-077 : le journal de
        # l'espion pesait 87,7 Mo, en partie a cause des appels du cockpit).
        ([sys.executable, str(REPERTOIRE_MATRICE / "routines" / "espion-integrite" / "main.py"), "verifier"], "espion-integrite verifier"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "verifier-conventions" / "main.py"), "verifier"], "verifier-conventions"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "verifier-regles" / "main.py"), "verifier"], "verifier-regles"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "verifier-protocoles" / "main.py"), "verifier"], "verifier-protocoles"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "bdd-regles-matrice" / "main.py"), "verifier"], "bdd-regles-matrice verifier"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "bdd-conventions-matrice" / "main.py"), "verifier"], "bdd-conventions-matrice verifier"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "bdd-protocoles-matrice" / "main.py"), "verifier"], "bdd-protocoles-matrice verifier"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "bdd-modifications" / "main.py"), "verifier"], "bdd-modifications verifier"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "suivi-optimus" / "main.py"), "verifier"], "suivi-optimus verifier"),
        # MO-096 : le croisement FILE du pilote <-> JOURNAL (categorie `coherence`,
        # construite en MO-048) existait mais n'etait branche NULLE PART -- une
        # porte que personne ne franchit ne protege rien. C'est par ce trou que
        # MO-095 (2026-09-15) a ete menee de bout en bout SANS jamais entrer dans
        # le marbre, sous un `verifier` vert : lui ne juge que la coherence
        # INTERNE du journal (une mission jamais declaree y est invisible).
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "suivi-optimus" / "main.py"), "coherence"], "suivi-optimus coherence (file <-> journal)"),
    ]:
        code, txt = _run(cmd)
        bilan.append((label, code))
        short = txt.strip().splitlines()
        # keep first 20 lines max per check
        body = "\n".join(short[:LIGNES_SORTIE_COURTE])
        if len(short) > 20:
            body += f"\n[... {len(short)-20} lignes masquees]"
        out.append(f"\n[{label}] code={code}\n" + body)
    for cmd, label in [
        ([sys.executable, str(REPERTOIRE_OP / "super-combos" / "combos" / "outils" / "garde-ascii.py"), str(REPERTOIRE_MATRIX)], "garde-ascii matrix/ (matrice + _operateur + docs)"),
        ([sys.executable, str(REPERTOIRE_OP / "super-combos" / "combos" / "outils" / "garde-perimetre-write.py"), "--jours", "1", "--racine", str(racine)], "garde-perimetre WRITE (1j)"),
        ([sys.executable, str(REPERTOIRE_OP / "super-combos" / "combos" / "outils" / "garde-tmp.py"), "--racine", str(racine)], "garde-tmp"),
    ]:
        code, txt = _run(cmd)
        bilan.append((label, code))
        out.append(f"\n[{label}] code={code}\n" + txt.strip()[:TAILLE_SORTIE_STANDARD])
    # LES BOITES INTERCOM (MO-322) : leur TAILLE entre dans le bilan de /sante.
    # Elle n etait mesuree par AUCUNE porte -- le cockpit ne comptait que les
    # lignes -- donc une boite de 17,5 Mo pour un plafond de 5 Mo vivait sous un
    # /sante VERT. Une porte qui ne mesure pas la grandeur qu elle surveille ne
    # surveille rien.
    code_boites, texte_boites = porte_boites_intercom(racine)
    bilan.append(("boites intercom (taille)", code_boites))
    out.append("\n[boites intercom (taille)] code=" + str(code_boites) + "\n" + texte_boites)
    # LES JOURNAUX DES ROUTINES (MO-324) : meme doctrine, autre population. Le
    # VIVANT se juge contre la borne que SA routine declare ; les ARCHIVES sont
    # mesurees et DITES (la rotation ne supprime rien) ; les fichiers qui ne sont ni
    # l un ni l autre sont des ANGLES MORTS et ils sont ACCUSES -- c est ainsi
    # qu une archive de 90 Mo a vecu sans que /sante la voie.
    code_journaux, texte_journaux = porte_journaux_routines(racine)
    bilan.append(("journaux des routines (taille)", code_journaux))
    out.append("\n[journaux des routines (taille)] code=" + str(code_journaux) + "\n" + texte_journaux)
    # LE LOT ARME (MO-380) : la reprise du retard se lit ICI (rang k/n, item, type,
    # urgence, statut) et sa memoire entre dans le verdict. Un lot de 37 maillons
    # versees d'un seul geste etait invisible au cockpit ; une reprise qu'on ne voit
    # pas ne se reprend pas.
    code_lot, texte_lot = porte_lot_arme(racine)
    bilan.append(("lot arme (memoire des maillons)", code_lot))
    out.append("\n[lot arme (memoire des maillons)] code=" + str(code_lot) + "\n" + texte_lot)
    out.append(_verdict_sante(bilan))
    return "\n".join(out)


def _verdict_sante(bilan):
    """Rend le VERDICT de la route /sante a partir des codes des portes.

    Une porte rouge doit CRIER en fin de route : un `code=1` noye au milieu de
    vingt blocs ne se lit pas a la reprise -- c'est ainsi que le faux vert
    MO-095 (mission menee sans entrer dans le marbre) a survecu une session.
    """
    echecs = [(label, code) for label, code in bilan if code != 0]
    if echecs:
        return (
            "\nVERDICT /sante : " + str(len(echecs)) + " PORTE(S) EN ECHEC sur "
            + str(len(bilan)) + " -- "
            + ", ".join(label + " (code " + str(code) + ")" for label, code in echecs)
        )
    return "\nVERDICT /sante : OK (" + str(len(bilan)) + " porte(s) verte(s))"


def route_flux1(racine):
    out = []
    out.append(_section("flux1") + "Flux 1 CAMELEON : Matrice GUIDE (pilote/file, vrac/tresse, veille)")
    for cmd, label in [
        ([sys.executable, str(REPERTOIRE_MATRICE / "pilote" / "main.py"), "file"], "pilote file (89 missions)"),
        ([sys.executable, str(REPERTOIRE_MATRICE / "pilote" / "entonnoir" / "main.py"), "file"], "entonnoir file+vrac"),
        ([sys.executable, str(REPERTOIRE_MATRICE / "pilote" / "entonnoir" / "main.py"), "tresse", "brin"], "tresse brin"),
    ]:
        code, txt = _run(cmd)
        out.append(f"\n[{label}] code={code}\n" + txt.strip()[:TAILLE_SORTIE_LARGE])
    for rel in ("pilote/outbox.jsonl", "cameleon/inbox.jsonl"):
        p = REPERTOIRE_MATRICE / "intercom" / rel
        tail = _tail_jsonl(str(p), n=3)
        out.append(f"\n[intercom {rel} tail 3]")
        for j in tail:
            out.append("  " + json.dumps(j, ensure_ascii=False)[:TAILLE_EXTRAIT_COURT])
        if not tail:
            out.append("  (vide ou absent)")
    code, txt = _run([sys.executable, str(REPERTOIRE_OP / "super-combos" / "combos" / "outils" / "lanceur-non-regression.py"), "--racine", str(racine)])
    # keep verdict only
    short = [l for l in txt.splitlines() if "VERDICT" in l or l.startswith("  ")][:LIGNES_VERDICT]
    out.append(f"\n[lanceur-non-regression] code={code}\n" + ("\n".join(short) if short else txt.strip()[:TAILLE_SORTIE_LARGE]))
    return "\n".join(out)


def route_flux2(racine):
    out = []
    out.append(_section("flux2") + "Flux 2 MAINTENANCE : Matrice SURVEILLE Optimus (espions, remorque, suivi-optimus)")
    for cmd, label in [
        ([sys.executable, str(REPERTOIRE_OP / "espions" / "espion-integrite-optimus.py"), "verifier"], "espion-integrite-optimus verifier (71)"),
        ([sys.executable, str(REPERTOIRE_OP / "espions" / "espion-activite-optimus.py")], "espion-activite-optimus (file/frictions/verrous)"),
        ([sys.executable, str(REPERTOIRE_OP / "remorque" / "remorque-optimus.py"), "etat"], "remorque etat (45)"),
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "suivi-optimus" / "main.py"), "verifier"], "suivi-optimus verifier"),
    ]:
        code, txt = _run(cmd)
        out.append(f"\n[{label}] code={code}\n" + txt.strip()[:TAILLE_SORTIE_LARGE])
    code, txt = _run([sys.executable, str(REPERTOIRE_DATA / "outils" / "suivi-optimus" / "main.py"), "lire", "--n", "5"])
    out.append(f"\n[suivi-optimus lire --n 5] code={code}\n" + txt.strip()[:TAILLE_SORTIE_TRES_LARGE])
    return "\n".join(out)


# SEUILS DE POLITIQUE restants (MO-100) : ce qui reste ici est un CHOIX du
# cockpit, pas une mesure d'objet. Tout ce qui mesure un objet est parti chez
# l'objet : le budget de la veille (MO-097) et le budget du bilan-periode
# (MO-100) sont DECLARES par l'outil et PUBLIES, le cockpit se contente de LIRE.
# - `py_compile_ms` (400) : SUPPRIMEE en MO-100. Aucun code ne la lisait (grep :
#   sa seule declaration) ; elle donnait l'illusion que la compilation etait
#   surveillee a 400 ms alors que la compilation reelle mesuree etait de 1406 ms
#   puis 794 ms (MO-097). La brancher telle quelle aurait fait crier a tort.
# - `bilan_periode_ms` (500) : MIGREE en MO-100 vers
#   `bilan-periode/constants.py:BUDGET_PASSE_MS`, publiee dans la sortie de
#   l'outil puis lue ici.
# - `usages_lignes` (50000) : MIGREE en MO-101/P3 vers le PROPRIETAIRE du
#   journal (`bdd-usages/constants.py:SEUIL_OCTETS_JOURNAL`), qui le borne et le
#   PUBLIE dans sa porte `lire` ; le cockpit le LIT. Le dict reste VIDE : le
#   cockpit ne possede plus AUCUN seuil -- tout seuil de mesure est declare et
#   publie par l'objet mesure.
SEUILS_PERFS = {}

# Budget PUBLIE par un OUTIL dans sa propre sortie (MO-100), sur le motif de
# MO-097 applique aux outils : l'objet DECLARE, l'objet PUBLIE, le cockpit LIT.
# Sans publication, le cockpit le DIT ("BUDGET NON PUBLIE") au lieu de se
# rabattre sur un nombre ecrit ici -- que l'outil n'a jamais promis.
MOTIF_BUDGET_OUTIL = re.compile(r"Budget declare de l'outil : (\d+) ms")

# Capacite du journal des usages PUBLIEE par son proprietaire (MO-101/P3), lue
# par la porte `bdd-usages lire` : le cockpit compare la TAILLE REELLE du
# journal a cette capacite declaree. Depassee => la rotation n'a pas tourne
# (fait reel, pas un gout) ; absente => le cockpit le DIT, jamais de repli muet.
MOTIF_CAPACITE_JOURNAL = re.compile(r"Capacite declaree du journal usages : (\d+) octets")

# Budgets DECLARES par les routines (MO-097) : le seuil de la veille n'est plus
# une valeur en dur du cockpit. La routine DECLARE son budget (constants.py) et
# le PUBLIE dans son etat court ; le cockpit LIT la publication et, si elle
# manque, il le DIT -- au lieu de crier contre un seuil qu'aucune routine n'a
# jamais promis (ce seuil en dur faisait crier le cockpit chaque jour sur une
# passe stable a 1,7 s pour une cadence de 300 s, soit 0,6 % du temps).
ETATS_BUDGETS = {
    "veille-flux": ("routines", "veille-flux", "veille-cadence.json", "budget_passe_ms"),
}


def _budget_declare(nom_routine):
    """Budget de passe publie par la routine (ms), ou None si non publie."""
    rel = ETATS_BUDGETS.get(nom_routine)
    if not rel:
        return None
    try:
        with open(str(REPERTOIRE_MATRICE.joinpath(*rel[:-1])), "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
    except (OSError, ValueError):
        return None
    valeur = donnees.get(rel[-1])
    return valeur if isinstance(valeur, int) else None

def _budget_publie_par_outil(txt_metriques):
    """Budget declare publie par l'outil dans sa sortie (ms), ou None."""
    resultat = MOTIF_BUDGET_OUTIL.search(txt_metriques or "")
    return int(resultat.group(1)) if resultat else None


def _capacite_publiee(txt_metriques):
    """Capacite du journal usages publiee par son proprietaire (octets), ou None."""
    resultat = MOTIF_CAPACITE_JOURNAL.search(txt_metriques or "")
    return int(resultat.group(1)) if resultat else None


def _taille_journal_usages():
    """Taille reelle du journal des usages (octets), ou None s'il est illisible."""
    try:
        return (REPERTOIRE_DATA / "usages-outils-combos.jsonl").stat().st_size
    except OSError:
        return None


def _suggere_perfs(txt_metriques):
    """Analyse le texte des metriques et suggere 1 PERFORMANCE-* si seuil depasse."""
    suggestions = []
    # Parse duree moy depuis bilan-periode
    for outil in ("veille-flux", "bilan-periode"):
        m = re.search(re.escape(outil) + r".*duree moy (\d+) ms", txt_metriques)
        if m:
            moy = int(m.group(1))
            if "veille" in outil:
                seuil = _budget_declare(outil)
                if seuil is None:
                    suggestions.append(
                        outil + " moy " + str(moy) + "ms : BUDGET NON PUBLIE par la routine"
                        + " (a reparer -- aucune comparaison possible sans valeur declaree)"
                    )
                    continue
            else:
                seuil = _budget_publie_par_outil(txt_metriques)
                if seuil is None:
                    suggestions.append(
                        outil + " moy " + str(moy) + "ms : BUDGET NON PUBLIE par l'outil"
                        + " (a reparer -- aucune comparaison possible sans valeur declaree)"
                    )
                    continue
            if moy > seuil:
                cible = "PERFORMANCE-ROUTINES" if "veille" in outil else "PERFORMANCE-OUTILS"
                suggestions.append(f"{outil} moy {moy}ms > budget declare {seuil}ms -> suggere d'enchainer {cible}")
    # Capacite du journal usages (MO-101/P3) : la valeur est LUE chez son
    # proprietaire (publiee par `bdd-usages lire`), et comparee a la taille
    # REELLE du journal. Un depassement ne veut plus dire "le journal a grossi"
    # mais "la rotation liee a la capacite n'a pas tourne" -- un vrai signal.
    capacite = _capacite_publiee(txt_metriques)
    taille = _taille_journal_usages()
    if capacite is None:
        suggestions.append(
            "journal usages : CAPACITE NON PUBLIEE par son proprietaire (bdd-usages"
            " lire) -- a reparer, aucune comparaison possible sans capacite declaree"
        )
    elif taille is not None and taille > capacite:
        suggestions.append(
            f"journal usages {taille} octets > capacite declaree {capacite} octets"
            " -> la ROTATION n'a pas tourne (PERFORMANCE-OUTILS)"
        )
    if suggestions:
        return "\n[SUGGESTION AUTO (seuils proto-2 de SUGGESTION -- rien ne se pose ici, ce ne sont PAS des declencheurs)]\n" + "\n".join("  - " + s for s in suggestions)
    return "\n[SUGGESTION AUTO] aucun seuil depasse (proto-2 B : aucune suggestion d'enchainement)"


def _resumer_moteur(texte):
    """Resume lisible de la sortie --json du moteur (jamais un dump brut)."""
    try:
        donnees = json.loads(texte)
    except ValueError:
        return "  sortie illisible : " + texte.strip()[:TAILLE_EXTRAIT_COURT]
    lignes = [
        "  trouves : " + str(donnees.get("trouve", 0))
        + " | retournes : " + str(donnees.get("retourne", 0))
    ]
    if donnees.get("tronque"):
        lignes.append("  TRONQUE (limite de lecture) : " + ", ".join(donnees["tronque"]))
    if donnees.get("ecartes_sans_date"):
        lignes.append("  ecartes faute de date : " + str(donnees["ecartes_sans_date"]))
    for hit in donnees.get("hits", [])[:HITS_MONTRES]:
        # Un hit FICHIER ne porte pas de champ "source" (defaut : fichier).
        if hit.get("source", "fichier") == "fichier":
            lignes.append("  - " + str(hit.get("fichier")) + ":" + str(hit.get("ligne")))
        else:
            lignes.append("  - [" + str(hit.get("source")) + "] " + str(hit.get("cle")))
    if not donnees.get("hits"):
        lignes.append("  (aucun resultat)")
    return "\n".join(lignes)


def route_chercher(racine):
    """Branche la PORTE UNIQUE de recherche dans le cockpit (lecture seule).

    EO-112 : le moteur n'avait qu'un appelant (la vigie) ; ici il sert vraiment,
    au meme endroit ou Optimus cherchait a la main (une mission, une lecon, un
    fichier). Avec --requete la recherche est reelle, sans elle un temoin prouve
    que la porte repond et n'est pas aveugle.

    EO-126 : la porte est appelee avec --prive, parce que cette route annonce un
    perimetre (maintenance,_operateur) que le moteur exclut par defaut -- la
    promesse de routes-privees.json n'etait vraie que sur le papier.
    """
    out = []
    out.append(_section("chercher")
               + "Moteur de recherche (porte unique) -- branchee dans le cockpit (lecture seule)")
    moteur = REPERTOIRE_DATA / "outils" / "rechercher" / "main.py"
    requete = REQUETE_ROUTE or REQUETE_TEMOIN
    mode = "requete reelle" if REQUETE_ROUTE else "temoin (porte vivante ?)"
    # `--prive` (EO-126) : la route annonce `zone_perimetre = maintenance,_operateur`
    # dans routes-privees.json, mais le moteur EXCLUT ces zones par defaut -- la
    # promesse etait donc FAUSSE (mesure : POSTURE_PAR_TYPE = 0, meme par ici). Le
    # cockpit est la fenetre privee d'Optimus : il demande explicitement ce que le
    # perimetre annonce deja.
    code, texte = _run([
        sys.executable, str(moteur), "rechercher",
        "--requete", requete, "--dans", "tous", "--prive",
        "--json", "--limite", str(LIMITE_AFFICHAGE_CHERCHER),
    ])
    out.append("[" + mode + "] requete=" + repr(requete) + " code=" + str(code))
    out.append(_resumer_moteur(texte))
    return "\n".join(out)


def route_metriques(racine):
    out = []
    out.append(_section("metriques") + "Performances + activite (lecture seule) -- seuils proto-2 de SUGGESTION (rien ne se pose ici ; les VRAIS declencheurs sont LUS en bas)")
    out.append(
        "Seuils de MESURE du cockpit : "
        + (", ".join(f"{k}={v}" for k, v in SEUILS_PERFS.items()) or "aucun (tout seuil de mesure est declare par l'objet mesure)")
    )
    out.append(
        "Politique d'AFFICHAGE du cockpit (confort de lecture, JAMAIS une mesure) : "
        + "limite=" + str(LIMITE_AFFICHAGE_CHERCHER)
        + " extraits=" + str(TAILLE_EXTRAIT_COURT)
        + " sorties=" + "/".join(str(v) for v in (TAILLE_SORTIE_STANDARD, TAILLE_SORTIE_LARGE, TAILLE_SORTIE_TRES_LARGE, TAILLE_SORTIE_MAXIMALE))
        + " lignes=" + "/".join(str(v) for v in (LIGNES_SORTIE_COURTE, LIGNES_VERDICT, LIGNES_QUEUE_JOURNAL))
        + " hits=" + str(HITS_MONTRES)
    )
    metriques_txt = ""
    for cmd, label in [
        ([sys.executable, str(REPERTOIRE_DATA / "outils" / "bilan-periode" / "main.py"), "bilan", "--periode", "heures"], "bilan-periode heures (6h)"),
        ([sys.executable, str(REPERTOIRE_OP / "super-combos" / "combos" / "outils" / "bilan-matrice.py"), "--rapide", "--racine", str(racine)], "bilan-matrice --rapide"),
    ]:
        code, txt = _run(cmd)
        block = f"\n[{label}] code={code}\n" + txt.strip()[:TAILLE_SORTIE_MAXIMALE]
        out.append(block)
        metriques_txt += block + "\n"
    # Porte `bdd-usages lire` AVANT l'analyse : c'est son en-tete qui PUBLIE la
    # capacite du journal (MO-101/P3). Lue APRES l'analyse, la publication
    # n'arrivait jamais au controle -- le cockpit criait CAPACITE NON PUBLIEE
    # alors qu'elle etait publiee deux blocs plus bas (lecon L-028 : un controle
    # qui ne voit pas ce qu'il doit lire est un faux verdict).
    code_usages, txt_usages = _run(
        [sys.executable, str(REPERTOIRE_DATA / "outils" / "bdd-usages" / "main.py"), "lire"]
    )
    lignes_usages = txt_usages.strip().splitlines()
    # Le controle lit l'EN-TETE (capacite publiee + dernieres lignes), pas les
    # 1265 lignes du journal : la sortie complete noierait le rapport.
    entete_usages = "\n".join(lignes_usages[:LIGNES_ENTETE_JOURNAL] + lignes_usages[-LIGNES_QUEUE_JOURNAL:]) if lignes_usages else txt_usages.strip()
    out.append(f"\n[bdd-usages lire tail 20] code={code_usages}\n" + entete_usages[:TAILLE_SORTIE_TRES_LARGE])
    metriques_txt += entete_usages + "\n"
    # Budgets lus chez les objets, une fois leurs sorties disponibles : les
    # routines publient dans leur etat court, les outils dans leur sortie.
    budget_outil = _budget_publie_par_outil(metriques_txt)
    out.insert(
        2,
        "Budgets declares par les objets mesures : "
        + ", ".join(
            nom + "=" + (str(_budget_declare(nom)) if _budget_declare(nom) is not None else "NON PUBLIE")
            for nom in ETATS_BUDGETS
        )
        + " | bilan-periode="
        + (str(budget_outil) + " ms" if budget_outil is not None else "NON PUBLIE par l'outil"),
    )
    out.append(_suggere_perfs(metriques_txt))
    # --- LES VRAIS DECLENCHEURS (voie A, EO-181/MO-198) ----------------------
    # Le mot "declencheur" avait DEUX sens dans ce cockpit : ici, le FAUX (des
    # seuils de performance qui ne declenchent rien). Les VRAIS vivent ailleurs :
    # AUTOMATIQUES, POSES par la porte machine-defcon, branches sur la passe
    # VIGILE de la veille. Le cockpit les LIT en direct (`surveiller --evaluer`)
    # au lieu de les citer de memoire -- motif du projet : l'objet DECLARE,
    # l'objet PUBLIE, le cockpit LIT. `--evaluer` est LECTURE SEULE : il rapporte
    # et NE POSE RIEN (aucun niveau n'est monte par une lecture).
    code_decl, txt_decl = _run(
        [sys.executable,
         str(REPERTOIRE_DATA / "outils" / "machine-defcon" / "main.py"),
         "surveiller", "--evaluer"]
    )
    out.append(
        "DECLENCHEURS REELS (AUTOMATIQUES -- poses par machine-defcon/surveiller,"
        " branches sur la passe VIGILE de la veille) : code=" + str(code_decl)
    )
    out.append("  " + (txt_decl.strip() or "aucun rapport de la porte"))
    out.append(
        "  -> les seuils proto-2 ci-dessus NE SONT PAS ces declencheurs : ce sont des"
        " SUGGESTIONS faites a l'operateur (rien ne se pose tout seul)."
    )
    return "\n".join(out)


# --- LA PORTE /remise (MO-474) : LE POIDS DE REMISE PAR ROUND ------------------
# Demande createur (2026-09-26) : surveiller DANS LE TEMPS le poids de la fiche que
# l agent lit a chaque round (MO-471/472/473), pour voir le PLAFOND DE REMISE tenir
# ou glisser. La serie se DERIVE de l outbox des injections : vue REGENERABLE,
# aucune ecriture, rien a maintenir. Le PLAFOND et les PESEURS ne sont PAS recopies
# -- le module de la fiche est CONSOMME chez son domicile
# (pilote/injection/fonctions.py), comme le cockpit consomme deja les autres seuils
# (M-076) : recopier une formule de poids serait deux verites (L-029).
def _charger_fonctions_injection():
    """Charge injection/fonctions.py par son CHEMIN (domicile du pilote).

    Rend (module, motif_echec) : le module, ou (None, motif NOMME). Aucun repli muet
    (L-055) : un domicile illisible se DIT, il ne se lit pas comme un zero.
    """
    chemin = REPERTOIRE_OP / "pilote" / "injection" / "fonctions.py"
    if not chemin.is_file():
        return None, "domicile ABSENT : " + str(chemin)
    repertoire_pilote = str(REPERTOIRE_OP / "pilote")
    if repertoire_pilote not in sys.path:
        sys.path.insert(0, repertoire_pilote)
    try:
        specification = importlib.util.spec_from_file_location(
            "injection_fonctions_cockpit", str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError) as erreur:
        return None, ("domicile ILLISIBLE : " + str(chemin) + " ("
                      + type(erreur).__name__ + " : " + str(erreur) + ")")
    return module, ""


def _dernieres_injections(chemin, n):
    """Les n DERNIERES injections JSON d un journal jsonl (lecture SEQUENTIELLE).

    Chaque ligne non vide est lue UNE fois ; seules les n dernieres INJECTIONS sont
    retenues (l outbox d un flux porte aussi d autres messages : la fenetre ne peut
    donc pas compter les lignes, elle compte les injections). Une ligne illisible est
    comptee et ECARTEE, jamais devinee. Rend (injections, ligne(s) illisible(s),
    lignes lues) ; un journal absent rend (-1) en lignes lues (le DIT, jamais un faux
    zero).
    """
    injections = collections.deque(maxlen=n)
    illisibles = 0
    lues = 0
    try:
        with open(str(chemin), "r", encoding=ENCODAGE) as flux:
            for ligne in flux:
                if not ligne.strip():
                    continue
                lues += 1
                try:
                    entree = json.loads(ligne)
                except ValueError:
                    illisibles += 1
                    continue
                if entree.get("mission") and entree.get("objectif"):
                    injections.append(entree)
    except OSError:
        return [], 0, -1
    return list(injections), illisibles, lues


def _direction_tendance(valeurs):
    """Direction d une tendance : (mot, moyenne 1re moitie, moyenne 2e moitie, pourcent).

    Une TENDANCE se juge sur ce que la serie FAIT, pas sur deux points extremes : on
    compare donc la MOYENNE de la 1re moitie a celle de la 2e (un pic isole ne fait
    pas une tendance). Un mouvement sous SEUIL_TENDANCE_POURCENT se lit "stable".
    PURE : aucune ecriture, testable sur des valeurs fabriquees.
    """
    if not valeurs:
        return "stable", 0, 0, 0
    if len(valeurs) < 2:
        return "stable", valeurs[0], valeurs[0], 0
    milieu = len(valeurs) // 2
    gauche = valeurs[:milieu] or valeurs[:1]
    droite = valeurs[milieu:] or valeurs[-1:]
    moyenne_gauche = int(round(sum(gauche) / len(gauche)))
    moyenne_droite = int(round(sum(droite) / len(droite)))
    pourcent = (0 if not moyenne_gauche else
                int(round(100 * (moyenne_droite - moyenne_gauche) / moyenne_gauche)))
    if pourcent > SEUIL_TENDANCE_POURCENT:
        return "hausse", moyenne_gauche, moyenne_droite, pourcent
    if pourcent < -SEUIL_TENDANCE_POURCENT:
        return "baisse", moyenne_gauche, moyenne_droite, pourcent
    return "stable", moyenne_gauche, moyenne_droite, pourcent


def _etincelle(valeurs):
    """Etincelle ASCII (une colonne par round) -- politique d AFFICHAGE.

    Chaque valeur devient UN caractere de RAMPE_TENDANCE, proportionnel a sa place
    entre le min et le max de la SERIE. Une serie PLATE rend un caractere UNIQUE au
    milieu de la rampe : sans ce cas, un min egal au max ferait une division par zero
    (le DIT au lieu de planter). PURE : aucune ecriture.
    """
    if not valeurs:
        return ""
    mini, maxi = min(valeurs), max(valeurs)
    if maxi == mini:
        return RAMPE_TENDANCE[len(RAMPE_TENDANCE) // 2] * len(valeurs)
    dernier = len(RAMPE_TENDANCE) - 1
    return "".join(RAMPE_TENDANCE[int(round(dernier * (valeur - mini) / (maxi - mini)))]
                   for valeur in valeurs)


def _consecutifs_au_dessus(valeurs, reference):
    """Longueur de la serie FINALE de rounds STRICTEMENT au-dessus de la reference.

    On remonte depuis le DERNIER round : des qu un round n est plus au-dessus, la
    serie s arrete. C est ce qui distingue une hausse PROLONGEE (tenue jusqu au
    bout) d un pic isole suivi d une retombee. PURE (aucune ecriture).
    """
    consecutifs = 0
    for valeur in reversed(valeurs):
        if valeur > reference:
            consecutifs += 1
        else:
            break
    return consecutifs


def _deriver_tendance(valeurs):
    """Detecte une HAUSSE PROLONGEE (derive) : (derive, motif, pourcent, consecutifs).

    Une DERIVE, c est une hausse de FOND -- la moyenne de la 2e moitie depasse celle
    de la 1re moitie d au moins SEUIL_DERIVE_POURCENT -- CONFIRMEE par la FIN de la
    serie : les ROUNDS_DERIVE_CONSECUTIFS derniers rounds sont tous AU-DESSUS de la
    moyenne de la 1re moitie. Sans la confirmation, une hausse n est qu une
    ESTIMATION (motif dit). Un pic isole ne mord donc jamais. PURE (aucune ecriture).
    """
    if len(valeurs) < 2:
        return False, "serie trop courte pour une tendance", 0, 0
    mot, moyenne_gauche, _moyenne_droite, pourcent = _direction_tendance(valeurs)
    consecutifs = _consecutifs_au_dessus(valeurs, moyenne_gauche)
    if mot != "hausse":
        return False, "pas de hausse de fond", pourcent, consecutifs
    if pourcent < SEUIL_DERIVE_POURCENT:
        return False, ("hausse " + str(pourcent) + " pour cent sous le seuil de derive "
                       + str(SEUIL_DERIVE_POURCENT) + " pour cent"), pourcent, consecutifs
    if consecutifs < ROUNDS_DERIVE_CONSECUTIFS:
        return False, ("hausse " + str(pourcent) + " pour cent NON confirmee : "
                       + str(consecutifs) + " round(s) au-dessus de la 1re moitie"
                       " (il en faut " + str(ROUNDS_DERIVE_CONSECUTIFS) + ")"), \
            pourcent, consecutifs
    return True, ("hausse " + str(pourcent) + " pour cent confirmee par " + str(consecutifs)
                  + " round(s) consecutif(s) AU-DESSUS de la 1re moitie"), pourcent, consecutifs


def route_remise(racine):
    """LE POIDS DE REMISE PAR ROUND -- la fiche lue a chaque round (MO-474).

    Demande createur (2026-09-26) : un encart de suivi qui montre, dans le TEMPS, le
    poids de la fiche que l agent lit a chaque round et son etat contre le PLAFOND DE
    REMISE (MO-473). Lecture seule, vue REGENERABLE : rien n est ecrit.

    Ce que la porte NE fait PAS : recopier le plafond ni la formule de poids. Elle
    CHARGE le domicile du pilote (`injection/fonctions.py`) et l INTERROGE
    (`PLAFOND_REMISE_TOKENS`, `poids_fiche`, `poids_injection`) -- un seuil recopie
    est un seuil qui ment le jour ou sa source change (L-029).
    """
    matrice = _racine_matrice(racine)
    chemin_outbox = matrice.joinpath(*CHEMIN_OUTBOX_FLUX)
    lignes = [
        _section("remise")
        + "POIDS DE REMISE PAR ROUND -- la fiche lue a chaque round (fiche technique)",
        "  source : " + "/".join(CHEMIN_OUTBOX_FLUX) + " (dernieres "
        + str(LIGNES_REMISE_SERIE) + " injections reelles)",
    ]
    module, motif = _charger_fonctions_injection()
    if module is None:
        lignes.append("  PLAFOND DE REMISE et PESEURS NON LUS -- " + motif
                      + " (la porte ne SUPPOSE pas un plafond : elle ne peut pas juger)")
        return "\n".join(lignes) + "\nVERDICT /remise : INDETERMINE (domicile illisible)"
    plafond = module.PLAFOND_REMISE_TOKENS
    lignes.append("  plafond de remise LU chez son domicile : PLAFOND_REMISE_TOKENS = "
                  + str(plafond) + " tokens")
    injections, illisibles, lues = _dernieres_injections(chemin_outbox, LIGNES_REMISE_SERIE)
    if not injections:
        if lues < 0:
            detail = "outbox ABSENTE (" + str(chemin_outbox) + ")"
        else:
            detail = "aucune injection lisible dans les " + str(lues) + " dernieres lignes"
        lignes.append("  AUCUNE MESURE : " + detail + " -- le DIT, jamais le taire (L-055)")
        return "\n".join(lignes) + "\nVERDICT /remise : INDETERMINE (aucune injection)"
    if illisibles:
        lignes.append("  " + str(illisibles) + " ligne(s) d outbox ILLISIBLE(S) : ecartees de la serie")
    fiches = []
    entieres = []
    depassements = []
    depassements_injection = []
    plafond_injection = getattr(module, "PLAFOND_INJECTION_TOKENS", 0)
    lignes.append("")
    lignes.append("  date                 mission   fiche   injection   gain     plafond")
    for injection in injections:
        fiche = module.poids_fiche(injection)
        entiere = module.poids_injection(injection)
        fiches.append(fiche)
        entieres.append(entiere)
        gain = ("0 %" if not entiere else str(int(100 * (entiere - fiche) / entiere)) + " %")
        etat = "DEPASSE" if fiche > plafond else "tenu"
        if fiche > plafond:
            depassements.append(str(injection.get("mission", "?")) + " = " + str(fiche) + " t")
        if plafond_injection and entiere > plafond_injection:
            depassements_injection.append(str(injection.get("mission", "?")) + " = "
                                          + str(entiere) + " t")
        lignes.append("  " + str(injection.get("date", "?"))[:19].ljust(20)
                      + str(injection.get("mission", "?"))[:8].ljust(10)
                      + str(fiche).rjust(5) + str(entiere).rjust(12)
                      + str(gain).rjust(8) + "     " + etat)
    lignes.append("")
    lignes.append("  serie : " + str(len(fiches)) + " round(s) | fiche min "
                  + str(min(fiches)) + " / mediane " + str(int(statistics.median(fiches)))
                  + " / max " + str(max(fiches)) + " tokens"
                  + " | plafond tenu sur " + str(len(fiches) - len(depassements))
                  + "/" + str(len(fiches)))
    # --- POIDS D INJECTION TOTAL ET TENDANCE (MO-476) ------------------------
    # Demande createur (2026-09-26) : montrer AUSSI le poids de l injection ENTIERE
    # (le total remis, fiche comprise) et son EVOLUTION dans le TEMPS. Le total de la
    # serie est un CUMUL (somme + moyenne) ; la TENDANCE compare la moyenne de la 1re
    # moitie a celle de la 2e -- un pic isole ne fait pas une tendance.
    lignes.append("  total sur la serie : injection " + str(sum(entieres)) + " tokens"
                  + " (moyenne " + str(int(sum(entieres) / len(entieres))) + ")"
                  + " | fiche " + str(sum(fiches)) + " tokens"
                  + " (moyenne " + str(int(sum(fiches) / len(fiches))) + ")")
    lignes.append("")
    lignes.append("  TENDANCE (1 colonne par round, du PLUS ANCIEN au plus RECENT) :")
    for etiquette, serie in (("fiche    ", fiches), ("injection", entieres)):
        mot, moyenne_gauche, moyenne_droite, pourcent = _direction_tendance(serie)
        signe = "+" if pourcent >= 0 else ""
        lignes.append("    " + etiquette + " | " + _etincelle(serie) + " | "
                      + "1re moitie " + str(moyenne_gauche) + " -> 2e moitie "
                      + str(moyenne_droite) + " : " + mot.upper()
                      + " (" + signe + str(pourcent) + " pour cent)")
    if plafond_injection:
        etat_injection = "DEPASSE" if depassements_injection else "tenu"
        lignes.append("  plafond global d injection LU chez son domicile :"
                      " PLAFOND_INJECTION_TOKENS = " + str(plafond_injection) + " tokens"
                      + " -- " + etat_injection + " sur "
                      + str(len(entieres) - len(depassements_injection))
                      + "/" + str(len(entieres)) + " round(s)")
    # --- DERIVE DU POIDS D INJECTION (MO-477) --------------------------------
    # Demande createur (2026-09-26) : SIGNALER une HAUSSE PROLONGEE du poids
    # d injection. Le detecteur MORD sur une hausse de fond CONFIRMEE par la fin de
    # la serie ; un pic isole ne mord jamais (il retombe).
    derive, motif_derive, pourcent_derive, consecutifs_derive = _deriver_tendance(entieres)
    if derive:
        lignes.append("  DERIVE : " + motif_derive + " -- HAUSSE PROLONGEE du poids"
                      " d injection (seuils : SEUIL_DERIVE_POURCENT = "
                      + str(SEUIL_DERIVE_POURCENT) + ", ROUNDS_DERIVE_CONSECUTIFS = "
                      + str(ROUNDS_DERIVE_CONSECUTIFS) + ")")
    else:
        lignes.append("  derive du poids d injection : AUCUNE -- " + motif_derive)
    if depassements or depassements_injection:
        if depassements:
            lignes.append("  ACCUSE (remise) : " + " | ".join(depassements)
                          + " -- la remise DIT le depassement et nomme `pilote ordres --id"
                          " <id> --complet` (jamais de troncage muet)")
        if depassements_injection:
            lignes.append("  ACCUSE (injection) : " + " | ".join(depassements_injection)
                          + " -- l injection ENTIERE depasse le PLAFOND GLOBAL d injection")
        return "\n".join(lignes) + "\nVERDICT /remise : KO (" \
            + str(len(depassements)) + " remise(s) et " + str(len(depassements_injection)) \
            + " injection(s) AU-DESSUS DU PLAFOND)"
    if derive:
        return "\n".join(lignes) + "\nVERDICT /remise : ALERTE (HAUSSE PROLONGEE du poids"\
            " d injection : +" + str(pourcent_derive) + " pour cent, confirmee par "\
            + str(consecutifs_derive) + " round(s) -- a surveiller)"
    return "\n".join(lignes) + "\nVERDICT /remise : OK (" + str(len(fiches)) \
        + " round(s) sous le plafond de remise)"


ROUTERS = {
    "etat": route_etat,
    "sante": route_sante,
    "flux1": route_flux1,
    "flux2": route_flux2,
    "chercher": route_chercher,
    "metriques": route_metriques,
    "remise": route_remise,
}


def main():
    parser = argparse.ArgumentParser(description="Cockpit prive Optimus -- Matrice comme serveur distant (lecture seule)")
    parser.add_argument("--route", default="complet", help="Route(s) : etat|sante|flux1|flux2|chercher|metriques|remise|complet (virgule separee)")
    parser.add_argument("--json", action="store_true", help="Sortie JSON machine")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--requete", default="", help="Route /chercher : texte a rechercher (defaut : temoin)")
    args = parser.parse_args()

    # Option de la SEULE route /chercher : les routes ont une signature (racine),
    # cette option traverse donc par ce module (lecture seule, aucune ecriture).
    global REQUETE_ROUTE
    REQUETE_ROUTE = args.requete.strip()

    try:
        racine = detecter_racine(COCKPIT_DIR)
    except RuntimeError:
        racine = Path(args.racine).resolve()
    else:
        # l'utilisateur peut forcer une autre racine
        if args.racine != ".":
            racine = Path(args.racine).resolve()

    routes_demandees = [r.lower() for r in decouper_liste(args.route)]
    if not routes_demandees:
        routes_demandees = ["complet"]
    # complet = tout
    if "complet" in routes_demandees:
        routes_demandees = list(ROUTES_EXPANDED)
    else:
        for r in routes_demandees:
            if r not in ROUTERS:
                print(f"Route inconnue : {r} (choix : {', '.join(ROUTES)})")
                return 2

    result = {}
    textes = []
    for nom in routes_demandees:
        fn = ROUTERS[nom]
        txt = fn(racine)
        result[nom] = txt
        textes.append(txt)

    if args.json:
        print(json.dumps({"routes": routes_demandees, "racine": str(racine), "result": result}, ensure_ascii=False, indent=2))
    else:
        print("\n".join(textes))
        print("\n--- cockpit lecture seule (aucune ecriture, aucun drapeau pose) ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
