#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-sans-attendre.py -- Garde : la verification ne se PAYE PAS en attendant

Pourquoi (2026-09-13, parole du createur) : < attendre une action qui va prendre
900 s n'est pas du tout un bon moyen de savoir si ca fonctionne ; si ca ne
fonctionne pas, on a attendu 900 s pour rien >. La reponse n'est pas d'attendre
mieux : c'est de rendre la chose LISIBLE.

  1. l'attente est DECOUPEE (`matrice/data/commun/attente.py`) : un arret demande
     est vu en quelques secondes, quelle que soit la cadence ;
  2. la cadence se LIT : chaque routine publie la sienne a l'allumage, et
     `vie etat` affiche celle qu'elle DECLARE.

Depuis le 2026-09-14 (GO createur), le garde surveille AUSSI la REGLE que l'agent
relit : < l'attente ne prouve rien > (regle immuable dediee). MO-062/MO-064
n'avaient cable que les BOUCLES des routines ; la regle n'etait ecrite nulle part
ou l'agent la relit, et deux attentes de ~10 min ont eu lieu le meme jour < pour
voir > un anneau s'emplir alors que la preuve se LISAIT en une commande. Le
controle `regle-lue-a-l-allumage` exige la doctrine aux QUATRE emplacements que
l'agent relit, et se PIEGE lui-meme (regle absente, emplacement muet).

Depuis MO-077 (2026-09-13), la lecture est BORNEE et la cadence de l'espion vit
dans son ETAT COURT (espion-etat.json) : son journal est rotationne, donc un
`demarrage` peut un jour partir dans l'archive -- un controle qui chercherait la
cadence dans le journal serait AVEUGLE apres une rotation, c'est-a-dire
neutralise par le nettoyage qu'il surveille (lecon L-040). Le controle d'accord
affiche la duree de lecture MESUREE a chaque execution : la borne est une
propriete constatee, jamais une intention.

Ce garde verifie ces proprietes a CHAQUE execution de la non-regression, pour
qu'elles ne puissent pas se perdre en silence.

CE QU'IL NE FAIT PAS (volontairement) :
  - il ne touche AUCUNE routine en service (lecon L-053 : un cobaye ne se pose
    jamais sur une entite en service -- mon premier essai a efface le PID de
    l'espion vivant) ;
  - il ne relance rien, il ne supprime aucun PID, il n'ecrit aucun drapeau.
  La republication d'un PID file perdu est prouvee en mission (MO-062) et
  surveillee en aval par le maillon 3 de la non-regression du flux (une routine
  vivante sans PID file y rompt la chaine).

Usage: python verifier-sans-attendre.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

# --- SEUILS (aucune valeur en dur dans la logique) --------------------------
# Une attente de 900 s dont le drapeau est vu en <= 5 s : la marge est large
# (mesure reelle : 2,0 s) et elle ne depend PAS de la cadence eprouvee.
CADENCE_EPREUVE_SECONDES = 900
MARGE_UNITE_SECONDES = 5
DELAI_DRAPEAU_SECONDES = 1.0
# Un `time.sleep` de CADENCE : soit son argument parle d'un INTERVALLE (le nom
# reel de la panne : `intervalle_secondes`, `INTERVALLE_SECONDS`,
# `INTERVALLE_SUPERVISION_SECONDES`), soit c'est un litteral >= 10 s.
#
# Motif volontairement ETROIT : on n'accuse pas tout ce qui finit par
# `_SECONDES`. Une pause courte et nommee (`PAUSE_REPRISE_SECONDES`, 5 s, qui
# vit dans une passe et non dans une boucle) n'est PAS la panne qu'on traque, et
# un garde qui crie sur du legitime finit ignore (lecon L-054).
MOTIF_INTERVALLE = ("interval", "INTERVAL")
LITTERAL_MINIMUM_SECONDES = 10

# OU chercher l'attente d'une boucle. `*/boucle/fonctions.py` est la convention
# des routines ; les trois autres fichiers sont des boucles ecrites a la main
# (suivi-sync, routeur de maintenance) ou le superviseur lui-meme.
FICHIERS_BOUCLE = (
    "suivi-sync/main.py",
    "routeur-maintenance/routeur.py",
    "vie/server_matrice.py",
)

# Fichier qui PUBLIE la cadence effective de chaque routine : source
# INDEPENDANTE de `vie etat` (qui lit, lui, la valeur DECLAREE).
#
# Ce n'est PLUS le journal : les journaux de routines sont ROTATIONNES (MO-077,
# puis MO-078 qui a etendu la borne aux quatre, puis MO-079 au routeur) -- un
# `demarrage` finit un jour dans l'archive, et un controle qui chercherait la
# cadence dans le journal deviendrait AVEUGLE, c'est-a-dire neutralise par le
# nettoyage qu'il surveille (lecon L-040). La cadence se lit donc dans l'ETAT
# COURT de chaque routine, qui n'est jamais deplace.
#
# AUCUN des cinq journaux rotationnes n'est lu ici : le routeur de maintenance
# publie desormais SA cadence dans routeur-cadence.json (MO-079) au lieu de la
# laisser dans routeur-historique.jsonl -- sinon la premiere rotation aurait
# emporte le `demarrage` que ce controle cherchait.
JOURNAL_PAR_ROUTINE = {
    "veille-flux": ("veille-cadence.json", "intervalle"),
    "espion-integrite": ("espion-etat.json", "intervalle"),
    "vigie-profil": ("vigie-profil-cadence.json", "intervalle"),
    "vigie-portes": ("vigie-portes-cadence.json", "intervalle"),
    "suivi-sync": (None, None),
    "routeur-maintenance": ("routeur-cadence.json", "intervalle"),
}

# Lecture BORNEE (MO-077) : on lit la QUEUE des journaux, jamais tout l'historique.
# Mesure avant/apres : la cadence de l'espion etait cherchee dans 87,7 Mo / 540 608
# lignes ; elle est desormais lue dans la QUEUE BORNEE (et, pour l'espion, dans
# un fichier d'etat d'une ligne). MO-099 : la FENETRE ne se declare plus ici --
# elle vient du moteur PARTAGE (data/commun/rotation_journal.py), deduite de la
# borne declaree du journal lu.

# --- LA REGLE QUE L'AGENT RELIT (2026-09-14) --------------------------------
# < L'attente ne prouve rien > : une preuve se LIT, elle ne s'ATTEND pas. La regle
# doit vivre aux QUATRE emplacements que l'agent relit a l'allumage ; si l'un la
# perd, elle peut disparaitre en silence et l'agent redevient libre de dormir
# < pour voir > (incident du 2026-09-14).
#   - le fichier de la regle porte la DOCTRINE (marqueur ci-dessous) ;
#   - l'index, la fiche et le protocole injecte la NOMMENT.
CHEMIN_REGLE_ATTENTE = (
    Path("_operateur") / "optimus-prime" / "regles-immuables" / "attente-ne-prouve-rien.md"
)
REGLE_ATTENTE_FICHIER = "attente-ne-prouve-rien.md"
REGLE_ATTENTE_DOCTRINE = "Une preuve se LIT, elle ne s'ATTEND pas"
REGLE_ATTENTE_EMPLACEMENTS = (
    (Path("_operateur") / "optimus-prime" / "regles-immuables" / "regles-immuables-readme.md",
     "l'index des regles immuables"),
    (Path("_operateur") / "optimus-prime" / "optimus-prime.md",
     "la fiche (REGLES ABSOLUES)"),
    (Path("_operateur") / "optimus-prime" / "protocoles" / "proto-1-reprise-mission.md",
     "le protocole injecte au demarrage"),
)


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def lire_texte(chemin):
    """Lit un fichier sans jamais lever (garde L-026 : un controle ne tue rien)."""
    try:
        return chemin.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


# --------------------------------------------------------------------------- 1
def controler_unite(matrix):
    """L'attente DECOUPEE rend la main des que le drapeau apparait.

    On eprouve une attente de 900 s avec un drapeau pose au bout de 1 s : si le
    mecanisme est casse, ce garde prend 15 minutes -- et il n'attend PAS une
    cadence reelle, il eprouve le mecanisme.
    """
    chemin = matrix / "matrice" / "data" / "commun" / "attente.py"
    if not chemin.is_file():
        return ("unite", False, "attente.py introuvable : " + str(chemin))
    try:
        specification = importlib.util.spec_from_file_location("attente_epreuve", str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        attendre = module.attendre
    except Exception as erreur:  # noqa: BLE001 -- on AVOUE l'echec, on ne plante pas
        return ("unite", False, "attente.py illisible : " + str(erreur))

    # Le drapeau d'epreuve vit dans le dossier TEMPORAIRE DU SYSTEME : jamais sur
    # une routine en service, et jamais dans la zone (un garde qui laisse un
    # residu dans la zone fait crier le garde des residus).
    drapeau = Path(tempfile.gettempdir()) / "matrice-attente-epreuve.tmp"
    if drapeau.exists():
        drapeau.unlink()

    def poser():
        time.sleep(DELAI_DRAPEAU_SECONDES)
        drapeau.write_text("arret\n", encoding="utf-8")

    debut = time.time()
    fil = threading.Thread(target=poser, daemon=True)
    fil.start()
    vu = attendre(CADENCE_EPREUVE_SECONDES, drapeau)
    duree = time.time() - debut
    fil.join(timeout=DELAI_DRAPEAU_SECONDES + 5)
    if drapeau.exists():
        drapeau.unlink()

    detail = (
        "drapeau vu=" + str(vu) + " en " + str(round(duree, 2)) + "s "
        "(cadence eprouvee " + str(CADENCE_EPREUVE_SECONDES) + "s)"
    )
    return ("unite", bool(vu) and duree <= MARGE_UNITE_SECONDES, detail)


# --------------------------------------------------------------------------- 2
def controler_fabrique(routines):
    """Aucune boucle ne dort en UN BLOC : elles passent par l'attente partagee.

    C'est le controle de la FABRIQUE, pas de l'effet (meme doctrine que le
    controle des prefixes) : un `time.sleep(intervalle)` dans une boucle, c'est
    la panne qui revient -- l'arret se paie a la cadence.

    Retourne (nom, ok, detail) et la liste des ecarts nommes fichier:ligne.
    """
    fichiers = []
    for chemin in sorted(routines.glob("*/boucle/fonctions.py")):
        fichiers.append(chemin)
    for relatif in FICHIERS_BOUCLE:
        chemin = routines / relatif
        if chemin.is_file():
            fichiers.append(chemin)

    if not fichiers:
        return ("fabrique", False, "aucune boucle trouvee sous " + str(routines)), []

    ecarts = []
    inspectees = 0
    for chemin in fichiers:
        inspectees += 1
        for numero, ligne in enumerate(lire_texte(chemin).splitlines(), 1):
            if "time.sleep(" not in ligne:
                continue
            if ligne.strip().startswith("#"):
                continue
            argument = ligne.split("time.sleep(", 1)[1].split(")", 1)[0].strip()
            fautif = any(motif in argument for motif in MOTIF_INTERVALLE)
            if not fautif:
                # Un litteral : fautif seulement s'il s'agit d'une cadence.
                chiffres = "".join(caractere for caractere in argument if caractere.isdigit())
                fautif = bool(chiffres) and int(chiffres) >= LITTERAL_MINIMUM_SECONDES
            if fautif:
                ecarts.append(
                    str(chemin.relative_to(routines.parent.parent)) + ":" + str(numero)
                    + " dort en UN BLOC (time.sleep(" + argument + ")) : passer par l'attente partagee"
                )

    detail = (
        str(len(fichiers)) + " boucle(s) inspectee(s), aucun sommeil en un bloc"
        if not ecarts
        else str(len(ecarts)) + " sommeil(s) en un bloc"
    )
    return ("fabrique", not ecarts, detail), ecarts


# --------------------------------------------------------------------------- 3
def lire_etat(matrix):
    """Passe la porte `vie etat` et rend (texte, cadences, serveur_actif)."""
    from lancement import delai_sous_processus  # data/commun installe par main()
    porte = matrix / "matrice" / "routines" / "vie" / "main.py"
    if not porte.is_file():
        return None, {}, None
    try:
        resultat = subprocess.run(
            [sys.executable, str(porte), "etat"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=delai_sous_processus(),
        )
    except (OSError, subprocess.SubprocessError):
        return None, {}, None
    texte = resultat.stdout
    cadences = {}
    serveur_actif = None
    for ligne in texte.splitlines():
        if "| cadence declaree :" in ligne:
            nom = ligne.strip().split(" :")[0]
            valeur = ligne.split("cadence declaree :")[1].strip().rstrip("s")
            cadences[nom] = int(valeur) if valeur.isdigit() else None
        elif "cadence : ILLISIBLE" in ligne:
            cadences[ligne.strip().split(" :")[0]] = None
        if "serveur matrice :" in ligne:
            serveur_actif = "ACTIVE" in ligne
    return texte, cadences, serveur_actif


def controler_lecture(cadences):
    """La cadence de chaque routine doit etre LISIBLE (aucun aveugle)."""
    if not cadences:
        return ("lecture", False, "`vie etat` ne rend aucune cadence (porte muette ?)")
    illisibles = [nom for nom, valeur in cadences.items() if not isinstance(valeur, int)]
    detail = (
        str(len(cadences)) + " cadence(s) lue(s) : "
        + ", ".join(str(nom) + "=" + str(valeur) + "s" for nom, valeur in sorted(cadences.items()))
        if not illisibles
        else "ILLISIBLE : " + ", ".join(sorted(illisibles))
    )
    return ("lecture", not illisibles, detail)


# --------------------------------------------------------------------------- 4
def queue_journal(chemin, octets):
    """Retourne les DERNIERES lignes d'un fichier, sans balayer l'historique.

    La premiere ligne lue peut etre TRONQUEE (on a coupe au milieu) : elle n'est
    gardee que si la lecture a commence au debut du fichier.
    """
    try:
        taille = chemin.stat().st_size
        debut = max(0, taille - octets)
        with open(str(chemin), "rb") as flux:
            flux.seek(debut)
            bloc = flux.read()
    except OSError:
        return []
    lignes = bloc.decode("utf-8", errors="replace").splitlines()
    if debut > 0 and lignes:
        lignes = lignes[1:]
    return [ligne for ligne in lignes if ligne.strip()]


def cadence_publiee(routines, nom):
    """Derniere cadence EFFECTIVE publiee par la routine : (valeur, presente, duree).

    La duree de lecture est RENDUE et affichee par le controle d'accord : la
    lecture bornee est une propriete MESUREE a chaque execution, pas une intention.
    """
    fichier, cle = JOURNAL_PAR_ROUTINE.get(nom, (None, None))
    if fichier is None:
        return None, False, 0.0
    chemin = routines / nom / fichier
    if not chemin.is_file():
        return None, False, 0.0
    debut = time.time()
    from rotation_journal import octets_queue_du_journal  # data/commun installe par main()
    lignes = queue_journal(chemin, octets_queue_du_journal(chemin))
    duree = time.time() - debut
    for ligne in reversed(lignes):
        try:
            evenement = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if "demarrage" in evenement or evenement.get("type") == "demarrage":
            valeur = evenement.get(cle)
            if isinstance(valeur, int):
                return valeur, True, duree
    # Repli : un etat COURT peut etre un JSON INDENTE (plusieurs lignes). On relit
    # alors le fichier entier -- il est minuscule par construction -- plutot que
    # de retomber en silence sur < sans trace > (un controle qui s'eteint sans le
    # dire est pire qu'un controle absent).
    try:
        evenement = json.loads(chemin.read_text(encoding="utf-8", errors="replace"))
        if "demarrage" in evenement or evenement.get("type") == "demarrage":
            valeur = evenement.get(cle)
            if isinstance(valeur, int):
                return valeur, True, duree
    except (OSError, ValueError):
        pass
    return None, True, duree


def controler_accord(routines, cadences):
    """La cadence LUE par la porte doit dire la meme chose que le journal.

    Deux sources independantes : la porte lit la valeur DECLAREE (constantes de
    la routine), le journal publie la valeur EFFECTIVE (celle du lancement). Un
    desaccord n'est jamais anodin : c'est ainsi que les routines ont tourne a
    60 s alors qu'elles declaraient 300/900 (MO-061).
    """
    desaccords = []
    sans_trace = []
    duree_max = 0.0
    for nom, cadence_porte in sorted(cadences.items()):
        if not isinstance(cadence_porte, int):
            continue
        publiee, trace_presente, duree = cadence_publiee(routines, nom)
        duree_max = max(duree_max, duree)
        if not trace_presente:
            if nom in JOURNAL_PAR_ROUTINE:
                sans_trace.append(nom)
            continue
        if publiee is None:
            sans_trace.append(nom)
        elif publiee != cadence_porte:
            desaccords.append(
                nom + " : la porte LIT " + str(cadence_porte) + "s mais la routine PUBLIE "
                + str(publiee) + "s (override explicite ? ou la porte ment)"
            )
    detail = (
        "porte et journaux d'accord"
        if not desaccords
        else " ; ".join(desaccords)
    )
    detail += " (lecture la plus lente : " + str(round(duree_max * 1000, 2)) + " ms)"
    if not desaccords and sans_trace:
        detail += " (sans trace publiee : " + ", ".join(sorted(sans_trace)) + ")"
    return ("accord", not desaccords, detail)


# --------------------------------------------------------------------------- 5
def controler_garde_serveur(texte, serveur_actif):
    """Un serveur arrete doit faire CRIER l'etat, jamais dire que tout va bien.

    Motif MO-062 : le serveur etait mort, 4 routines sur 6 arretees, et la porte
    annoncait < La Matrice vit (toutes les routines actives) >. Le garde muet du
    selecteur avait deja coute une journee ; on ne le rejoue pas.
    """
    if texte is None or serveur_actif is None:
        return ("garde-serveur", False, "etat du serveur illisible (la porte n'a pas repondu)")
    if serveur_actif:
        return ("garde-serveur", True, "serveur ACTIF")
    crie = "ATTENTION" in texte or "dort" in texte
    return (
        "garde-serveur",
        crie,
        "serveur ARRET et la porte le DIT" if crie else "serveur ARRET mais la porte ne crie PAS",
    )


# --------------------------------------------------------------------------- 6
# Les trois sommeils du cobaye : la panne nommee, le litteral de cadence, et la
# pause courte qu'il ne faut PAS accuser.
SOMMEIL_INTERVALLE = "            time.sleep(intervalle_secondes)\n"
SOMMEIL_LITTERAL = "            time.sleep(30)\n"
SOMMEIL_PAUSE_COURTE = "            time.sleep(PAUSE_REPRISE_SECONDES)\n"
SOMMEIL_CONFORME = "            attendre(intervalle_secondes, DRAPEAU)\n"


def controler_autotest():
    """Le garde se PIEGE lui-meme : un detecteur jamais vu se declencher ne prouve rien.

    On plante quatre boucles dans le dossier TEMPORAIRE DU SYSTEME (jamais dans
    la zone : un harnais qui laisse un residu fait crier le garde des residus) et
    on exige que le controle de fabrique ACCUSE les deux vraies pannes et
    EPARGNE la pause courte et l'attente partagee.
    """
    import shutil

    racine = Path(tempfile.mkdtemp(prefix="verifier-sans-attendre-autotest-"))
    cobayes = racine / "matrice" / "routines"
    epreuves = []

    def poser(nom, contenu):
        dossier = cobayes / nom / "boucle"
        dossier.mkdir(parents=True, exist_ok=True)
        (dossier / "fonctions.py").write_text(contenu, encoding="utf-8")

    def accuses():
        _, ecarts = controler_fabrique(cobayes)
        return ecarts

    try:
        poser("cobaye-intervalle", "def demarrer(i):\n" + SOMMEIL_INTERVALLE)
        ecarts = accuses()
        epreuves.append(("sommeil d'INTERVALLE accuse", len(ecarts) == 1 and ":2" in ecarts[0]))

        shutil.rmtree(cobayes)
        poser("cobaye-litteral", "def boucle():\n" + SOMMEIL_LITTERAL)
        epreuves.append(("litteral de cadence accuse", len(accuses()) == 1))

        shutil.rmtree(cobayes)
        poser("cobaye-pause-courte", "def passe():\n" + SOMMEIL_PAUSE_COURTE)
        epreuves.append(("pause courte EPARGNEE", not accuses()))

        shutil.rmtree(cobayes)
        poser("cobaye-conforme", "def boucle():\n" + SOMMEIL_CONFORME)
        epreuves.append(("attente partagee acceptee", not accuses()))
    finally:
        shutil.rmtree(racine, ignore_errors=True)

    reussies = sum(1 for _, ok in epreuves if ok)
    detail = (
        "detecte et epargne (" + str(reussies) + "/4)"
        if reussies == len(epreuves)
        else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok)
    )
    return ("autotest", reussies == len(epreuves), detail)


# --------------------------------------------------------------------------- 7
def controler_regle_lue(matrix):
    """La regle < l'attente ne prouve rien > doit etre LUE a l'allumage (2026-09-14).

    Quatre emplacements : la regle elle-meme (elle porte la doctrine), l'index des
    regles immuables, la fiche (REGLES ABSOLUES) et le protocole de reprise (celui
    que l'agent relit au demarrage). Si l'un la perd, une regle que personne ne
    relit ne protege rien -- c'est exactement le trou que MO-062/MO-064 avaient
    laisse : le garde protegeait les BOUCLES, pas la CONDUITE de l'agent.
    """
    ecarts = []
    regle = matrix / CHEMIN_REGLE_ATTENTE
    if not regle.is_file():
        ecarts.append("regle ABSENTE : " + str(CHEMIN_REGLE_ATTENTE))
    elif REGLE_ATTENTE_DOCTRINE not in lire_texte(regle):
        ecarts.append("regle SANS sa doctrine : " + str(CHEMIN_REGLE_ATTENTE))
    for relatif, description in REGLE_ATTENTE_EMPLACEMENTS:
        if REGLE_ATTENTE_FICHIER not in lire_texte(matrix / relatif):
            ecarts.append(str(relatif) + " (" + description + ") ne nomme plus la regle")
    detail = (
        "regle relue a l'allumage (" + str(1 + len(REGLE_ATTENTE_EMPLACEMENTS))
        + " emplacement(s))"
        if not ecarts
        else " ; ".join(ecarts)
    )
    return ("regle-lue-a-l-allumage", not ecarts, detail), ecarts


def controler_autotest_regle():
    """Le controle de la regle se PIEGE (lecon L-032) : un detecteur jamais vu crier
    ne prouve rien. On monte trois cobayes dans le dossier TEMPORAIRE DU SYSTEME :
    un complet (accepte), un sans la regle (accuse), un avec un emplacement muet
    (accuse -- nomme).
    """
    import shutil

    racine = Path(tempfile.mkdtemp(prefix="verifier-regle-attente-autotest-"))

    def poser(relatif, contenu):
        chemin = racine / relatif
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(contenu, encoding="utf-8")

    epreuves = []
    try:
        poser(CHEMIN_REGLE_ATTENTE, "# CONTROLE\n" + REGLE_ATTENTE_DOCTRINE + "\n")
        for relatif, _ in REGLE_ATTENTE_EMPLACEMENTS:
            poser(relatif, "voir " + REGLE_ATTENTE_FICHIER + "\n")
        _, ecarts = controler_regle_lue(racine)
        epreuves.append(("cobaye complet ACCEPTE", not ecarts))

        (racine / CHEMIN_REGLE_ATTENTE).unlink()
        _, ecarts = controler_regle_lue(racine)
        epreuves.append(("regle ABSENTE ACCUSEE", len(ecarts) == 1))

        poser(CHEMIN_REGLE_ATTENTE, "# CONTROLE\n" + REGLE_ATTENTE_DOCTRINE + "\n")
        poser(REGLE_ATTENTE_EMPLACEMENTS[0][0], "index muet\n")
        _, ecarts = controler_regle_lue(racine)
        epreuves.append(("emplacement MUET ACCUSE", len(ecarts) == 1))
    finally:
        shutil.rmtree(racine, ignore_errors=True)

    reussies = sum(1 for _, ok in epreuves if ok)
    detail = (
        "piege (" + str(reussies) + "/3)"
        if reussies == len(epreuves)
        else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok)
    )
    return ("autotest-regle-lue", reussies == len(epreuves), detail)


def main():
    parser = argparse.ArgumentParser(description="Garde : la verification ne se paie pas en attendant")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    args = parser.parse_args()

    matrix = trouver_matrix(Path(args.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(args.racine))
        return 2
    routines = matrix / "matrice" / "routines"
    # MO-099 : le moteur PARTAGE entre dans sys.path -- il porte la FENETRE de
    # lecture des queues (deduite de la borne declaree du journal lu).
    sys.path.insert(0, str(matrix / "matrice" / "data" / "commun"))

    resultats = []
    ecarts_nommes = []

    resultats.append(controler_unite(matrix))

    resultat_regle, ecarts_regle = controler_regle_lue(matrix)
    resultats.append(resultat_regle)
    ecarts_nommes.extend(ecarts_regle)

    resultat_fabrique, ecarts_fabrique = controler_fabrique(routines)
    resultats.append(resultat_fabrique)
    ecarts_nommes.extend(ecarts_fabrique)

    texte_etat, cadences, serveur_actif = lire_etat(matrix)
    resultats.append(controler_lecture(cadences))
    resultats.append(controler_accord(routines, cadences))
    resultats.append(controler_garde_serveur(texte_etat, serveur_actif))
    resultats.append(controler_autotest())
    resultats.append(controler_autotest_regle())

    print("VERIFIER SANS ATTENDRE -- cadence lue, jamais attendue")
    for nom, ok, detail in resultats:
        print("[" + ("OK  " if ok else "KO  ]") + "] " + nom + " : " + detail)
    for ecart in ecarts_nommes:
        print("       -> " + ecart)

    if any(not ok for _, ok, _ in resultats) or ecarts_nommes:
        print("\nVERDICT KO : la verification repasse par l'attente (ou la regle n'est plus relue).")
        return 1
    print("\nVERDICT OK : on lit la cadence, on n'attend pas la cadence ; la regle est relue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
