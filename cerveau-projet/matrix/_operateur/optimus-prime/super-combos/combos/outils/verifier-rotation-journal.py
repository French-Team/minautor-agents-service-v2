#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-rotation-journal.py -- Garde : borner un journal de la Matrice ne perd RIEN

Pourquoi (2026-09-13, MO-077 puis MO-078) : les journaux des routines de la
Matrice sont en AJOUT SEUL et rien ne les bornait. Mesures : espion-log.jsonl
87,7 Mo / 540 608 lignes ; journal-veille.txt 3,85 Mo / 44 050 lignes ;
vigie-profil-log.jsonl 76 Ko ; vigie-portes-log.jsonl 32 Ko. Trois lecteurs les
lisaient EN ENTIER (flux, attente, encart routines) et un journal de 540 000
lignes n'a pas le droit d'en perdre une seule en silence.Depuis MO-078 le moteur est PARTAGE (`matrice/data/commun/rotation_journal.py`,
motif unique M-076) : les cinq routines le consomment avec LEURS constantes.
Ce garde exige donc les DEUX proprietes :

  1. LE MOTEUR : rien ne se perd et rien ne se duplique (le contenu d'origine se
     retrouve A L'IDENTIQUE dans archive + journal actif), l'archive fait partie
     du "deja connu" (lecon L-040 : sinon la rotation se reecrit des jumeaux au
     passage suivant) et une course pendant la rotation est REFUSEE, jamais
     ecrasee.
  2. LES CINQ PORTES : chacune repond, sur SON journal, sans jamais ecrire
     dans le service (le controle borne le seuil a l'infini : un garde ne
     rotationne pas le journal qu'il surveille, lecon L-053).

CE QU'IL NE FAIT PAS : il ne touche JAMAIS un journal de service. Ses cobayes
vivent dans le dossier temporaire du systeme ; il s'AUTOTESTE en rejouant deux
rotations NAIVES (sans archive, sans dedup) que le controle doit ACCUSER
(lecon L-032 : un controle qu'on ne peut pas pieger ne prouve rien).

Usage: python verifier-rotation-journal.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import collections
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) ----------------------
# Le moteur PARTAGE : une seule source pour les cinq journaux.
MODULE_PARTAGE = Path("matrice") / "data" / "commun" / "rotation_journal.py"
# La FABRIQUE DE FIXTURES JETABLES (meme dossier partage) : ce garde ne
# recopie plus `mkdtemp`/`rmtree`, il DEMANDE ses fixtures au domicile commun.
MODULE_FABRIQUE = Path("matrice") / "data" / "commun" / "cobayes_jetables.py"
PREFIXE_COBAYE = "garde-rotation-"
NOM_MAIN = "main.py"
# Fenetre d'EPREUVE (MO-099) : ce nombre n'est PAS la fenetre reelle de lecture des
# journaux (chaque domaine la deduit de SA borne declaree, voir le moteur partage
# data/commun/rotation_journal.py). C'est un PARAMETRE D'EPREUVE : il doit rester
# PETIT et CONNU pour que le cobaye de lecture bornee le depasse.
OCTETS_QUEUE_EPREUVE = 256 * 1024
# Cobaye de lecture bornee : il doit etre PLUS GROS que la fenetre (sinon il ne
# prouve rien) -- 20 000 lignes font environ 900 Ko contre 256 Ko lus.
LIGNES_QUEUE_EPREUVE = 20000

# TABLE des journaux bornes : (routine, chemin relatif a matrix/, prefixe
# d'archive, script de la routine, fichier ou vivent ses constantes). Chaque
# PORTE est interrogee sur SON journal (subprocess : les modules `constants` des
# routines portent le meme nom, L-029). Le SCRIPT compte : le routeur de
# maintenance n'a pas de `main.py` (c'est `routeur.py`), et ses constantes vivent
# dans ce meme fichier -- l'exclure aurait laisse le dernier journal sans borne.
NOM_CONSTANTES = "constants.py"
JOURNAUX = (
    ("espion-integrite", Path("matrice") / "routines" / "espion-integrite" / "espion-log.jsonl",
     "espion-log-archive", NOM_MAIN, NOM_CONSTANTES),
    ("veille-flux", Path("matrice") / "routines" / "veille-flux" / "journal-veille.txt",
     "journal-veille-archive", NOM_MAIN, NOM_CONSTANTES),
    ("vigie-profil", Path("matrice") / "routines" / "vigie-profil" / "vigie-profil-log.jsonl",
     "vigie-profil-archive", NOM_MAIN, NOM_CONSTANTES),
    ("vigie-portes", Path("matrice") / "routines" / "vigie-portes" / "vigie-portes-log.jsonl",
     "vigie-portes-archive", NOM_MAIN, NOM_CONSTANTES),
    ("routeur-maintenance", Path("matrice") / "routines" / "routeur-maintenance" / "routeur-historique.jsonl",
     "routeur-archive", "routeur.py", "routeur.py"),
)

# Le controle des portes n'ecrit JAMAIS dans le service : un seuil hors
# d'atteinte garantit que la porte repond < rien a faire > sur le vrai journal.
SEUIL_INFINI = 10 ** 12

# Cobaye du moteur : un journal assez long pour etre coupe, avec ses pieges
# (deux lignes IDENTIQUES a l'octet pres, une ligne cassee).
LIGNES_COBAYE = 400
GARDES_COBAYE = 40
SEUIL_COBAYE = 1
GARDES_COURSE = 5

RESULTATS = []


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def multiset(lignes):
    """Compteur des lignes (signature exacte : la date COMPTE, c'est un fait)."""
    compteur = collections.Counter()
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            compteur[json.dumps(json.loads(ligne), ensure_ascii=True, sort_keys=True)] += 1
        except ValueError:
            compteur["CASSEE:" + ligne] += 1
    return compteur


def controler_transfert(avant, archive_apres, actif_apres):
    """Compare le CONTENU d'origine a (archive + actif). Rend (perdus, ajoutes).

    UNE comparaison, deux pannes : ce qui manque est une PERTE, ce qu'on a en
    plus est un JUMEAU. Les deux sont fatales pour un journal en ajout seul.
    """
    obtenus = multiset(archive_apres) + multiset(actif_apres)
    attendus = multiset(avant)
    perdus = {sig: n for sig, n in (attendus - obtenus).items() if n}
    ajoutes = {sig: n for sig, n in (obtenus - attendus).items() if n}
    return perdus, ajoutes


def lire(chemin):
    """Lignes non vides d'un fichier (vide si absent)."""
    if chemin is None or not Path(chemin).is_file():
        return []
    with open(str(chemin), "r", encoding="utf-8", errors="replace") as flux:
        return [ligne.rstrip("\r\n") for ligne in flux if ligne.strip()]


def ecrire_journal_cobaye(chemin):
    """Ecrit un journal de test avec ses pieges. Rend la liste des lignes."""
    lignes = []
    for index in range(LIGNES_COBAYE):
        evenement = {
            "type": "observation",
            "chapitre": 1,
            "bdd": "bdd-" + str(index % 7) + ".json",
            "etat": "ok",
            "detail": "integrite verifiee",
            "date": "2026-09-06 09:00:" + str(index % 60).zfill(2),
        }
        lignes.append(json.dumps(evenement, ensure_ascii=True))
    double = json.dumps({"type": "passe", "chapitres": [1], "bdds_surveillees": 14,
                         "ecarts": [], "date": "2026-09-06 10:00:00"}, ensure_ascii=True)
    lignes.append(double)
    lignes.append(double)
    lignes.append('{"type": "passe", "chapitres": [1]')
    lignes.append('{"type": "demarrage", "intervalle": 300, "date": "2026-09-06 09:00:00"}')
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(str(chemin), "w", encoding="utf-8", newline="\n") as flux:
        flux.write("\n".join(lignes) + "\n")
    return lignes


def charger_moteur(matrix):
    """Charge le moteur PARTAGE par son chemin (jamais un import devine)."""
    chemin = matrix / MODULE_PARTAGE
    if not chemin.is_file():
        return None
    import importlib.util

    specification = importlib.util.spec_from_file_location("moteur_rotation_epreuve", str(chemin))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def charger_fabrique(matrix):
    """Charge la FABRIQUE DE FIXTURES JETABLES par son chemin (moteur partage).

    Meme domicile que le moteur de rotation, et meme chargement que lui : les
    outils portent des tirets, un import par nom serait devine. Ce garde ne
    recopie donc plus `mkdtemp`/`rmtree` : le retrait des fixtures et la
    mutation d une copie vivent a UN seul domicile (L-029/L-102).
    """
    chemin = matrix / MODULE_FABRIQUE
    if not chemin.is_file():
        return None
    import importlib.util

    specification = importlib.util.spec_from_file_location("cobayes_jetables_epreuve",
                                                          str(chemin))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def archives(dossier, prefixe):
    return sorted(Path(dossier).glob(prefixe + "-*.jsonl"))


# --------------------------------------------------------------------------- 1
def controler_moteur(moteur, dossier, erreurs):
    """Le moteur partage : rien perdu, rien duplique, actif borne, trace rendue."""
    journal = dossier / "cobaye-espion.jsonl"
    lignes_avant = ecrire_journal_cobaye(journal)
    traces = []
    rapport = moteur.tourner(journal, SEUIL_COBAYE, GARDES_COBAYE, 3, "cobaye-log-archive")
    controler("moteur-repond", bool(rapport.get("rotation")), rapport.get("motif", "")[:110])
    if not rapport.get("rotation"):
        erreurs.append("le moteur n'a pas rotationne le cobaye : " + str(rapport.get("motif")))
        return
    fichiers_archive = archives(dossier, "cobaye-log-archive")
    contenu_archive = []
    for chemin in fichiers_archive:
        contenu_archive += lire(chemin)
    actif = lire(journal)
    controler("archive-dattee", bool(fichiers_archive) and fichiers_archive[0].name.startswith("cobaye-log-archive-"),
              fichiers_archive[0].name if fichiers_archive else "aucune archive")
    perdus, ajoutes = controler_transfert(lignes_avant, contenu_archive, actif)
    controler("rien-perdu", not perdus,
              str(len(lignes_avant)) + " ligne(s) d'origine, 0 perdue"
              if not perdus else str(sum(perdus.values())) + " ligne(s) PERDUE(S)")
    controler("rien-duplique", not ajoutes,
              "0 jumeau" if not ajoutes else str(sum(ajoutes.values())) + " jumeau(x)")
    if perdus:
        erreurs.append("le moteur a perdu " + str(sum(perdus.values())) + " ligne(s)")
    if ajoutes:
        erreurs.append("le moteur a duplique " + str(sum(ajoutes.values())) + " ligne(s)")
    controler("actif-borne", len(actif) == GARDES_COBAYE,
              str(len(actif)) + " evenement(s) actif(s) (attendu " + str(GARDES_COBAYE) + ")")
    cassees = [l for l in (contenu_archive + actif) if not _est_json(l)]
    controler("ligne-cassee-conservee", len(cassees) >= 1,
              str(len(cassees)) + " ligne(s) illisible(s) conservee(s) telles quelles")
    # La TRACE : le moteur rend l'evenement, la routine le journalise (L-020).
    code, _ = moteur.tourner_et_journaliser(
        journal, SEUIL_COBAYE, GARDES_COBAYE, 3, "cobaye-log-archive",
        traces.append, verbeux=False, forcer=True,
    )
    controler("trace-rendue", bool(traces) and traces[-1].get("type") == "rotation",
              "evenement de trace : " + str(sorted(traces[-1].keys())[:4]) if traces else "AUCUNE trace")
    return rapport


def _est_json(ligne):
    try:
        json.loads(ligne)
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------- 2
def controler_reprise(moteur, dossier, prefixe, erreurs):
    """REPRISE APRES ARRET (L-040) : le deja connu inclut-il l'archive ?

    Piege monte exactement comme l'incident que la lecon decrit : une ligne a
    DEJA ete deplacee dans l'archive, ET elle est encore dans le journal actif
    (arret entre l'archivage et la reecriture, ou rotation relancee). Si le
    moteur ne consulte pas l'archive comme "deja connu", il ecrira un JUMEAU et
    doublera l'archive en silence.
    """
    journal = dossier / "cobaye-reprise.jsonl"
    lignes = ecrire_journal_cobaye(journal)
    moteur.tourner(journal, SEUIL_COBAYE, GARDES_COBAYE, 3, prefixe)
    contenu_archive = []
    for chemin in archives(dossier, prefixe):
        contenu_archive += lire(chemin)
    actif_avant = lire(journal)
    jumeau = contenu_archive[0]
    signatures_avant = set(multiset(contenu_archive + actif_avant))
    with open(str(journal), "w", encoding="utf-8", newline="\n") as flux:
        flux.write(jumeau + "\n")
        flux.write("\n".join(actif_avant) + "\n")
    rapport = moteur.tourner(journal, SEUIL_COBAYE, len(actif_avant), 3, prefixe, forcer=True)
    contenu_apres = []
    for chemin in archives(dossier, prefixe):
        contenu_apres += lire(chemin)
    actif_apres = lire(journal)
    signatures_apres = set(multiset(contenu_apres + actif_apres))
    controler(
        "reprise-sans-jumeau",
        len(contenu_apres) == len(contenu_archive) and rapport.get("jumeaux", 0) >= 1,
        str(len(contenu_archive)) + " -> " + str(len(contenu_apres)) + " ligne(s) d'archive, "
        + str(rapport.get("jumeaux", 0)) + " jumeau(x) ignore(s)",
    )
    if len(contenu_apres) != len(contenu_archive):
        erreurs.append("l'archive a double au 2e passage : le deja connu n'inclut pas l'archive (L-040)")
    controler("reprise-sans-perte", signatures_avant.issubset(signatures_apres),
              "aucune signature n'a disparu du systeme (archive + actif)")
    if not signatures_avant.issubset(signatures_apres):
        erreurs.append("la reprise a fait disparaitre des signatures")
    _ = lignes


# --------------------------------------------------------------------------- 3
def controler_course(moteur, dossier, erreurs):
    """Course simulee : un ecrivain ajoute une ligne pendant l'archivage.

    Le moteur doit RECOMMENCER, puis REFUSER en le nommant -- et ne jamais
    ecraser ce qui a ete ecrit.
    """
    journal = dossier / "cobaye-course.jsonl"
    ecrire_journal_cobaye(journal)
    lignes_avant = lire(journal)
    vrai = moteur.ajouter_archive

    def ajouter_et_simuler_course(chemin, lot, connues):
        resultat = vrai(chemin, lot, connues)
        with open(str(journal), "a", encoding="utf-8", newline="\n") as flux:
            flux.write('{"type": "concurrent", "date": "2026-09-13 21:00:00"}\n')
        return resultat

    moteur.ajouter_archive = ajouter_et_simuler_course
    try:
        traces = []
        code, rapport = moteur.tourner_et_journaliser(
            journal, SEUIL_COBAYE, GARDES_COURSE, 3, "cobaye-log-archive", traces.append
        )
    finally:
        moteur.ajouter_archive = vrai
    perdus = set(multiset(lignes_avant)) - set(multiset(lire(journal)))
    controler(
        "course-refusee",
        code == 1 and "REFUS" in rapport["motif"] and not perdus,
        "code " + str(code) + ", " + rapport["motif"][:80]
        + ", lignes d'origine conservees : " + str(not perdus),
    )
    if code != 1 or "REFUS" not in rapport["motif"]:
        erreurs.append("une course pendant la rotation n'a pas ete refusee")
    if perdus:
        erreurs.append("une course a fait perdre des lignes")
    controler("course-tracee", any(t.get("type") == "rotation" for t in traces),
              "le refus est journalise (jamais un silence)")


# --------------------------------------------------------------------------- 4
def rotation_naive(avant, gardees, avec_archive, avec_dedup):
    """L'ANCIENNE regle, rejouee pour l'autotest (elle doit etre ACCUSEE).

    Deux pieges : (a) reecrire le journal SANS rien archiver (perte seche) ;
    (b) archiver SANS regarder ce que l'archive contient deja (jumeaux).
    """
    coupe = max(0, len(avant) - gardees)
    a_archiver, a_garder = avant[:coupe], avant[coupe:]
    archive = []
    if avec_archive:
        archive = list(a_archiver)
        if not avec_dedup:
            archive = archive + list(a_archiver)
    return archive, a_garder


def controler_autotest(dossier):
    """Le controle doit ACCUSER les deux rotations naives (lecon L-032)."""
    lignes = lire(dossier / "cobaye-espion.jsonl") or []
    if len(lignes) < GARDES_COBAYE * 2:
        lignes = [json.dumps({"n": i, "date": "2026-09-06 09:00:00"}) for i in range(200)]
    archive_naive, actif_naif = rotation_naive(lignes, GARDES_COBAYE, False, False)
    perdus, _ = controler_transfert(lignes, archive_naive, actif_naif)
    controler(
        "autotest-sans-archive", bool(perdus),
        "la rotation qui n'archive RIEN est accusee (" + str(sum(perdus.values())) + " perdue(s))"
        if perdus else "NON ACCUSEE : le controle ne saurait pas voir une perte",
    )
    archive_naive, actif_bis = rotation_naive(lignes, GARDES_COBAYE, True, False)
    _, ajoutes = controler_transfert(lignes, archive_naive, actif_bis)
    controler(
        "autotest-sans-dedup", bool(ajoutes),
        "la rotation qui ignore l'archive deja ecrite est accusee ("
        + str(sum(ajoutes.values())) + " jumeau(x))"
        if ajoutes else "NON ACCUSEE : le controle ne saurait pas voir un jumeau",
    )


# --------------------------------------------------------------------------- 5
def controler_decision(moteur, erreurs):
    """La decision est PURE : seuil, gardes, journal absent -- sans disque."""
    cas = [
        ("sous le seuil", moteur.decision_rotation(10, 10, 100, 5), (False, 10)),
        ("au-dessus", moteur.decision_rotation(101, 10, 100, 5), (True, 5)),
        ("journal plus court que la garde", moteur.decision_rotation(101, 3, 100, 5), (False, 3)),
        ("journal absent", moteur.decision_rotation(None, 0, 100, 5), (False, 0)),
    ]
    echecs = [nom for nom, obtenu, attendu in cas if (obtenu[0], obtenu[1]) != attendu]
    controler("decision-pure", not echecs,
              str(len(cas)) + " cas" + ("" if not echecs else " : " + str(echecs)))
    if echecs:
        erreurs.append("decision de rotation fausse : " + str(echecs))
    # Lecture BORNEE : elle doit rendre les memes dernieres lignes qu'une lecture
    # complete, sans balayer l'historique.
    # Le cobaye doit etre PLUS GROS que la fenetre de lecture, sinon il ne prouve
    # rien (un faux cobaye vert est un cobaye suspect, lecon L-032).
    journal = Path(tempfile.gettempdir()) / ("queue-epreuve-" + str(time.time_ns()) + ".jsonl")
    total = LIGNES_QUEUE_EPREUVE
    journal.write_text(
        "\n".join('{"n": ' + str(i) + ', "date": "2026-09-06 09:00:00"}' for i in range(total)) + "\n",
        encoding="utf-8", newline="\n",
    )
    bornees = moteur.lire_queue_journal(journal, OCTETS_QUEUE_EPREUVE)
    completes = lire(journal)[-len(bornees):]
    controler(
        "lecture-bornee",
        bornees == completes and 0 < len(bornees) < total,
        str(total) + " ligne(s) au cobaye -> " + str(len(bornees))
        + " lues dans la queue, les memes que la fin du journal",
    )
    if bornees != completes:
        erreurs.append("la lecture bornee ne rend pas les memes dernieres lignes")
    if len(bornees) >= total:
        erreurs.append("le cobaye de lecture bornee n'est pas plus gros que la fenetre : il ne prouve rien")
    try:
        journal.unlink()
    except OSError:
        pass


# --------------------------------------------------------------------------- 6
def controler_portes(matrix, erreurs):
    """Chaque PORTE repond sur SON journal, sans jamais ecrire dans le service."""
    from lancement import delai_sous_processus  # data/commun installe par main()
    for routine, relatif, prefixe, script, fichier_constantes in JOURNAUX:
        dossier = matrix / "matrice" / "routines" / routine
        porte = dossier / script
        if not porte.is_file():
            erreurs.append("porte de rotation absente : " + str(porte))
            controler("porte-" + routine, False, "main.py absent")
            continue
        try:
            resultat = subprocess.run(
                [sys.executable, str(porte), "rotation", "--seuil", str(SEUIL_INFINI)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=delai_sous_processus(), cwd=str(dossier),
            )
            sortie = (resultat.stdout or "") + (resultat.stderr or "")
            code = resultat.returncode
        except (OSError, subprocess.SubprocessError) as erreur:
            erreurs.append("porte de rotation illisible (" + routine + ") : " + str(erreur))
            controler("porte-" + routine, False, str(erreur)[:80])
            continue
        repond = code == 0 and "SANS ROTATION" in sortie and "absent" not in sortie
        detail = "code " + str(code) + " : " + (sortie.strip().splitlines()[0][:90] if sortie.strip() else "aucune sortie")
        controler("porte-" + routine, repond, detail)
        if not repond:
            erreurs.append("la porte de rotation de " + routine + " ne repond pas sur son journal")
        # Les constantes de la routine sont DECLAREES (lues dans la source : un
        # garde ne charge pas cinq modules `constants` homonymes, lecon L-029).
        source = dossier / fichier_constantes
        texte = source.read_text(encoding="utf-8", errors="replace") if source.is_file() else ""
        for nom in ("SEUIL_OCTETS_JOURNAL", "EVENEMENTS_GARDES_JOURNAL", "NOM_ARCHIVE_PREFIXE"):
            if nom not in texte:
                erreurs.append(routine + " : constante de rotation manquante (" + nom + ")")
        if prefixe not in texte:
            erreurs.append(routine + " : prefixe d'archive inattendu (" + prefixe + ")")


# --------------------------------------------------------------------------- 7
def controler_journaux_reels(matrix, erreurs):
    """Les journaux de service sont-ils bornes ET lisibles (archive + actif) ?"""
    for routine, relatif, prefixe, _, _ in JOURNAUX:
        journal = matrix / relatif
        if not journal.is_file():
            erreurs.append("journal de service introuvable : " + str(journal))
            controler("journal-" + routine, False, "absent : " + str(journal))
            continue
        lignes = lire(journal)
        illisibles = [ligne for ligne in lignes if not _est_json(ligne)]
        fichiers_archive = archives(journal.parent, prefixe)
        taille = journal.stat().st_size
        taille_archives = sum(chemin.stat().st_size for chemin in fichiers_archive)
        detail = (
            str(len(lignes)) + " evenement(s) actif(s) / " + str(round(taille / 1024)) + " Ko ; "
            + str(len(fichiers_archive)) + " archive(s) / " + str(round(taille_archives / 1024)) + " Ko"
        )
        controler("journal-" + routine, bool(lignes), detail)
        if not lignes:
            erreurs.append("le journal de " + routine + " est vide : la surveillance a disparu")
        if illisibles:
            # Un journal texte (veille) peut porter des lignes non-JSON : on le
            # SIGNALE sans bloquer, la conversion n'est pas le sujet de ce garde.
            print("       -> " + str(len(illisibles)) + " ligne(s) hors JSON (journal texte ?)")
        if fichiers_archive and taille > taille_archives:
            erreurs.append(
                routine + " : le journal actif pese plus lourd que ses archives (la rotation ne borne rien)"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Garde : borner un journal de la Matrice ne perd rien (moteur partage, cinq portes)"
    )
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    # data/commun sur sys.path (motif M-076) : le plafond d'un sous-processus a
    # son domicile unique (lancement.py), il n'est jamais recopie ici.
    sys.path.insert(0, str(matrix / "matrice" / "data" / "commun"))
    moteur = charger_moteur(matrix)
    if moteur is None:
        print("Moteur de rotation introuvable : " + str(matrix / MODULE_PARTAGE))
        return 2
    fabrique = charger_fabrique(matrix)
    if fabrique is None:
        print("Fabrique de fixtures introuvable : " + str(matrix / MODULE_FABRIQUE))
        return 2

    print("VERIFIER ROTATION JOURNAL -- moteur PARTAGE, cinq portes, rien ne se perd")

    erreurs = []
    with fabrique.fixtures(PREFIXE_COBAYE) as dossier:
        controler(
            "moteur-partage",
            callable(getattr(moteur, "decision_rotation", None)) and callable(getattr(moteur, "tourner", None)),
            "le moteur vit dans data/commun (une seule source pour les cinq journaux)",
        )
        controler_moteur(moteur, dossier, erreurs)
        controler_reprise(moteur, dossier, "cobaye-reprise-archive", erreurs)
        controler_course(moteur, dossier, erreurs)
        controler_autotest(dossier)
        controler_decision(moteur, erreurs)
        controler_portes(matrix, erreurs)
        controler_journaux_reels(matrix, erreurs)

    echecs = [nom for nom, ok, _ in RESULTATS if not ok]
    if erreurs or echecs:
        for ecart in erreurs:
            print("ECART : " + ecart)
        print("")
        print("VERDICT KO : la rotation des journaux n'est plus sure (voir les ecarts nommes).")
        return 1
    print("")
    print("VERDICT OK : le moteur deplace sans perdre ni dupliquer, et les cinq portes repondent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
