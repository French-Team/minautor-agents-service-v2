#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-118-file-relais-ordonee-garde-fou.py
GARDE-FOU : la file de relais est ORDONNEE par importance puis CLASSIFIEE
par type (decision utilisateur [attention] 2026-09-02, oracle v0.5.8,
mission 52ceaea1 - fonctions/files.py).

Contexte (oracle v0.5.8, 2026-09-02) :
  - La file asap n est PLUS consommee en FIFO strict. Le relais prend la
    mission EN_ATTENTE la PLUS IMPORTANTE : priorite la plus basse d abord
    (1 avant 2), puis a priorite egale la DATE la plus RECENTE d abord
    (un message recent peut etre plus important qu un ancien).
  - classifier(mission) deduit (priorite, type) par mots-cles a l ajout :
    priorite 1 si [urgent]/[attention]/etat urgent/p1 non-acquitte/purge
    p1/anomalie/serveur mort/processus fantome/defcon/alerte/urgent, sinon 2 ;
    type = urgent/purge/revision/test/creation/coordination.
  - prendre() enrichit les anciennes entrees sans champ (retro-compat) et
    pose statut PRISE + prise_date (atomique).
  - relais() porte la classification (mission-relais).

Invariants verifies (sur FILES_DIR TEMPORAIRE, jamais les vraies files) :
  1. classifier() : mots-cles -> priorite/type corrects (8 cas)
  2. ajouter() stocke priorite + type ; lister() affiche Px/type
  3. prendre() : ordre = priorite basse d abord puis date recente d abord
     a priorite egale (4 missions, ordre attendu P1 recentes puis P2
     recentes) ; entree sans date en fin de classement
  4. prendre() atomique : EN_ATTENTE -> PRISE + prise_date posee
  5. Retro-compatibilite : ancienne entree sans champs -> enrichie a la
     prise (priorite/type deduits)
  6. mission-relais end-to-end sur FILES_DIR temporaire : la mission la
     plus importante est relayee
  7. Normes : ASCII strict + LF pur (files.py + test) + purge

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: file, relais, classification, ordre-importance, garde-fou
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

FILES_PY = os.path.join(TOOLS_DIR, "oracle", "fonctions", "files.py")
ORACLE_PY = os.path.join(TOOLS_DIR, "oracle", "oracle.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            pass
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        for p in sys.argv[i + 1].split(","):
            try:
                DESACTIVES.append(int(p))
            except ValueError:
                pass

T_START = time.monotonic()
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-118 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s" % nom)
        if detail:
            print("       %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def ascii_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def charger_files(tmp_dir):
    """Charger fonctions/files.py avec FILES_DIR redirige vers tmp_dir.

    _file_path ne cree pas le dossier parent : on le cree ici pour que
    l ajout de mission fonctionne sur la file temporaire."""
    os.makedirs(tmp_dir, exist_ok=True)
    spec = importlib.util.spec_from_file_location("files_mod", FILES_PY)
    f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f)
    ancien = f.FILES_DIR
    f.FILES_DIR = type(ancien)(tmp_dir)
    return f, ancien


# ------------------------------------------------------------------
# Points
# ------------------------------------------------------------------
def sous_tmp(tmp_dir, nom):
    """Sous-repertoire dedie a un point (isolation des files entre points)."""
    p = os.path.join(tmp_dir, nom)
    os.makedirs(p, exist_ok=True)
    return p


def point_1_classifier(tmp_dir):
    f, _ = charger_files(sous_tmp(tmp_dir, "p1"))
    cas = [
        ("[urgent] serveur mort", (1, "urgent")),
        ("[attention] decision utilisateur perimetre", (1, "urgent")),
        ("ETAT URGENT x1: 4 anomalies", (1, "urgent")),
        ("PURGE P1 : lire puis acquitter", (1, "purge")),
        ("REVISION strategique : questionner l utilisateur", (2, "revision")),
        ("TEST MORPHEUS non-regression", (2, "test")),
        ("CREER un OUTIL lister-flags", (2, "creation")),
        ("MISSION simple sans mot-cle", (2, "coordination")),
    ]
    ko = []
    for mission, attendu in cas:
        got = f.classifier(mission)
        if got != attendu:
            ko.append("%s->%s attendu %s" % (mission[:25], got, attendu))
    verifier("1. classifier() : mots-cles -> priorite/type (8 cas)",
             not ko, "; ".join(ko[:3]))


def point_2_ajouter_lister(tmp_dir):
    f, _ = charger_files(sous_tmp(tmp_dir, "p2"))
    e, err = f.ajouter("P2/coordination : mission sans urgence", file="asap",
                       agent="x")
    ok_stock = (err is None and e.get("priorite") == 2
                and e.get("type") == "coordination")
    # lister affiche Px/type : verifier que l entree porte la classification
    liste = f.lister("asap")
    entree = [m for m in liste if m.get("id") == e["id"]]
    ok_lister = len(entree) == 1 and entree[0].get("priorite") == 2
    verifier("2. ajouter() stocke priorite/type + lister() expose la classification",
             ok_stock and ok_lister, "err=%s" % err)


def point_3_tri_importance(tmp_dir):
    f, _ = charger_files(sous_tmp(tmp_dir, "p3"))
    m1, _ = f.ajouter("P2/travail : invention d un module d archivage avance",
                      file="asap", agent="x")
    time.sleep(1.05)
    m2, _ = f.ajouter("P1/travail : [urgent] serveur indisponible",
                      file="asap", agent="x")
    time.sleep(1.05)
    m3, _ = f.ajouter("P2/travail : mise a jour du catalogue de references",
                      file="asap", agent="x")
    time.sleep(1.05)
    m4, _ = f.ajouter("P1/travail : [attention] decision perimetre",
                      file="asap", agent="x")
    ordre = []
    for _ in range(4):
        e, err = f.prendre(file="asap")
        ordre.append(e["id"])
        f.terminer(e["id"], file="asap")
    attendu = [m4["id"], m2["id"], m3["id"], m1["id"]]
    verifier("3. prendre() : P1 recentes puis P2 recentes (priorite ASC, date DESC)",
             ordre == attendu, "ordre=%s attendu=%s" % (ordre, attendu))


def point_4_atomique(tmp_dir):
    f, _ = charger_files(sous_tmp(tmp_dir, "p4"))
    e, _ = f.ajouter("P2/coordination : mission atomique", file="asap",
                     agent="x")
    pris, err = f.prendre(file="asap")
    ok_statut = pris.get("statut") == "PRISE" and pris.get("prise_date")
    # Le fichier sur disque porte bien le statut PRISE
    chemin = f._file_path("asap")
    ligne = [l for l in chemin.read_text(encoding="utf-8").splitlines()
             if json.loads(l).get("id") == e["id"]][0]
    sur_disque = json.loads(ligne).get("statut") == "PRISE"
    verifier("4. prendre() atomique : EN_ATTENTE -> PRISE + prise_date (disque)",
             ok_statut and sur_disque, "statut=%s" % pris.get("statut"))


def point_5_retro(tmp_dir):
    f, _ = charger_files(sous_tmp(tmp_dir, "p5"))
    chemin = f._file_path("asap")
    vieille = {"id": "zzzz9999", "date": "2026-09-01T00:00:00",
               "mission": "P2/x : [urgent] ancienne entree sans champs",
               "statut": "EN_ATTENTE", "agent": "y"}
    with open(chemin, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(vieille) + "\n")
    e, err = f.prendre(file="asap")
    ok = (e.get("priorite") == 1 and e.get("type") == "urgent"
          and e.get("statut") == "PRISE" and e.get("prise_date"))
    verifier("5. retro-compatibilite : ancienne entree sans champs enrichie a la prise",
             ok, "err=%s e=%s" % (err, {k: e.get(k) for k in ("priorite", "type", "statut")}))


def point_6_relais(tmp_dir):
    f, _ = charger_files(sous_tmp(tmp_dir, "p6"))
    # Une P2 ancienne puis une P1 recente : le relais doit porter la P1
    f.ajouter("P2/travail : ancienne mission sans urgence", file="asap", agent="x")
    time.sleep(1.05)
    p1, _ = f.ajouter("P1/travail : [urgent] processus fantome detecte",
                      file="asap", agent="x")
    e, err = f.relais("asap")
    ok = e is not None and e.get("id") == p1["id"] and e.get("priorite") == 1
    verifier("6. relais() porte la mission la plus importante (P1 recente)",
             ok, "err=%s relayee=%s" % (err, e.get("id") if e else None))


def point_7_normes():
    fichiers = [os.path.abspath(__file__), FILES_PY]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("7. ASCII strict : 0 non-ASCII (files.py + test)",
             total_na == 0, "nb=%d" % total_na)
    verifier("8. LF pur : 0 CRLF (files.py + test)",
             total_crlf == 0, "nb=%d" % total_crlf)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-118 : file de relais ordonnee + classifiee ===")
    tmp_dir = os.path.join(PROJECT_ROOT, "tmp-test118")
    try:
        if point_actif(1):
            t0 = time.monotonic()
            point_1_classifier(tmp_dir)
            chrono_etape("1. classifier", t0)
        if point_actif(2):
            t0 = time.monotonic()
            point_2_ajouter_lister(tmp_dir)
            chrono_etape("2. ajouter/lister", t0)
        if point_actif(3):
            t0 = time.monotonic()
            point_3_tri_importance(tmp_dir)
            chrono_etape("3. tri importance", t0)
        if point_actif(4):
            t0 = time.monotonic()
            point_4_atomique(tmp_dir)
            chrono_etape("4. atomique", t0)
        if point_actif(5):
            t0 = time.monotonic()
            point_5_retro(tmp_dir)
            chrono_etape("5. retro", t0)
        if point_actif(6):
            t0 = time.monotonic()
            point_6_relais(tmp_dir)
            chrono_etape("6. relais", t0)
        if point_actif(7):
            t0 = time.monotonic()
            point_7_normes()
            chrono_etape("7. normes", t0)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
    except Exception as e:
        print("  [KO] EXCEPTION : %s" % e)
        NB_KO += 1
    finally:
        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (file ordonnee + classee)"
                                    if NB_KO == 0 else "KO (file incoherente)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())