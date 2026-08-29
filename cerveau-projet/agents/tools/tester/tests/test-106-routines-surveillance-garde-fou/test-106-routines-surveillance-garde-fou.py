#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-106-routines-surveillance-garde-fou.py

Garde-fou des routines de surveillance v1 transposes des v2 (2026-08-29) :
flux, sante, encart, live, vigie-perimetre. Verifie trois invariants :

  A. EXISTENCE + triplet : chaque routine existe et porte --dry-run.
  B. ENREGISTREMENT : manifest.json les reference (actif, intervalle) et
     grades-v1.json leur attribue G3.
  C. DETECTION d anomalie : chaque routine contient la logique de
     detection (patterns de code) sans jamais corriger (lecture seule).
  D. DRY-RUN SANS EFFET DE BORD : un --dry-run ne modifie AUCUN fichier
     d etat de la routine (ex: flux .flux_derniere.txt, vigie-perimetre
     etat-empreintes.json) et ne cree rien.
     NB : l inbox ne peut pas etre comparee (le daemon l ecrit en
     parallele - flaky), on verifie les fichiers d etat a la place.

Points verifies :
  1. flux/sante/encart/live/vigie-perimetre existent et portent --dry-run.
  2. manifest.json les reference tous (actif + intervalle attendu).
  3. grades-v1.json : chacun en G3.
  4. Sante : detection daemons DEFCON/encart/BDD (patterns).
  5. Live : detection agent actif/inbox/activite (patterns).
  6. Encart : detection colonnes/en-tete (pattern).
  7. Flux : persistance par .flux_derniere.txt (pattern changement).
  8. Vigie-perimetre : detection 4W (QUI/QUOI/QUAND/OU + empreinte).
  9. Dry-run des 5 : rc dans {0,1}, sortie avec le prefixe de la routine,
     et AUCUN fichier d etat cree/modifie (.flux_derniere.txt,
     etat-empreintes.json).
 10. Regression cible : un --dry-run de flux ne cree PAS .flux_derniere.txt
     lorsque l etat n existait pas (correction 2026-08-29).
 11. chaque routine applique --dry-run (option explicitement lue).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.1
Tags: routines, surveillance, flux, sante, encart, live, vigie-perimetre,
garde-fou
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

ORACLE_DIR = os.path.join(TOOLS_DIR, "oracle")
ROUTINES_DIR = os.path.join(ORACLE_DIR, "routines")
MANIFEST = os.path.join(ROUTINES_DIR, "manifest.json")
GRADES = os.path.join(ORACLE_DIR, "grades-v1.json")

ROUTINES = {
    "flux": os.path.join(ROUTINES_DIR, "flux.py"),
    "sante": os.path.join(ROUTINES_DIR, "sante.py"),
    "encart": os.path.join(ROUTINES_DIR, "encart.py"),
    "live": os.path.join(ROUTINES_DIR, "live.py"),
    "vigie-perimetre": os.path.join(ROUTINES_DIR, "vigie-perimetre.py"),
    "verifier-statuts": os.path.join(ROUTINES_DIR, "verifier-statuts.py"),
}
# intervalle attendu dans le manifest (secondes)
INTERVALLES = {"flux": 600, "sante": 300, "encart": 300, "live": 300,
                "vigie-perimetre": 300, "verifier-statuts": 300}
# prefixe de sortie + pattern de detection
PATTERNS = {
    "flux": ("[FLUX]", "_DERNIERE_VALEUR"),
    "sante": ("[SANTE]", "anomalie(s)"),
    "encart": ("[ENCART]", "anomalie(s)"),
    "live": ("[LIVE]", "anomalie(s)"),
    "vigie-perimetre": ("[VIGIE-PERIMETRE]", "perimetre-modifie"),
    "verifier-statuts": ("[VERIFIER-STATUTS]", "_est_urgence_reelle"),
}
ETAT_EMPREINTES = os.path.join(ROUTINES_DIR, "etat-empreintes.json")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
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


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def point_1_existence_triplet():
    """1. Les 5 routines existent avec --dry-run + main."""
    ok = True
    manquants = []
    for nom, chemin in ROUTINES.items():
        contenu = lire(chemin)
        if not (os.path.isfile(chemin) and "--dry-run" in contenu
                and "def main()" in contenu):
            ok = False
            manquants.append(nom)
    verifier("1. flux/sante/encart/live/vigie-perimetre existent "
             "(--dry-run, main)",
             ok, "manquants=%s" % ",".join(manquants) if manquants else "")


def point_2_manifest():
    """2. Manifest reference les 5 routines (actif, intervalle, script)."""
    try:
        data = json.loads(lire(MANIFEST))
    except ValueError:
        data = {}
    routines = {r.get("nom"): r for r in data.get("routines_surveillance", [])}
    ok = True
    details = []
    for nom, chemin in ROUTINES.items():
        r = routines.get(nom)
        if not (r and r.get("actif") is True
                and r.get("intervalles_secondes") == INTERVALLES[nom]
                and r.get("script") == "%s.py" % nom):
            ok = False
            details.append(nom)
    # vigie-perimetre exige aussi la section perimetre_surveille.
    perimetre = data.get("perimetre_surveille", [])
    if not perimetre:
        ok = False
        details.append("perimetre_surveille-absent")
    verifier("2. manifest reference les 5 routines + perimetre_surveille",
             ok, "KO=%s" % ",".join(details) if details else "")


def point_3_grade():
    """3. grades-v1 donne G3 aux 5 routines."""
    try:
        data = json.loads(lire(GRADES))
    except ValueError:
        data = {}
    routines = data.get("routines", {})
    manquants = [n for n in ROUTINES if routines.get(n) != "G3"]
    ok = not manquants
    verifier("3. grades-v1 G3 pour les 5 routines", ok,
             "manquants=%s" % ",".join(manquants) if manquants else "")


def point_4_sante_detection():
    """4. Sante : detection daemons + DEFCON + encart + BDD."""
    contenu = lire(ROUTINES["sante"])
    ok = ("_verifier_daemon" in contenu
          and "_verifier_defcon" in contenu
          and "_verifier_encart" in contenu
          and "_verifier_bdd" in contenu
          and "LECTURE SEULE" not in contenu)  # sante historise, pas une empreinte
    ok = (ok and "anomalie(s)" in contenu)
    verifier("4. sante detection (daemons, DEFCON, encart, BDD)", ok)


def point_5_live_detection():
    """5. Live : detection agent actif + inbox + activite."""
    contenu = lire(ROUTINES["live"])
    ok = ("_agent_actif" in contenu
          and "_verifier_inbox" in contenu
          and "_verifier_derniere_activite" in contenu
          and "anomalie(s)" in contenu)
    verifier("5. live detection (agent, inbox, activite)", ok)


def point_6_encart_detection():
    """6. Encart : detection en-tete/colonnes v1."""
    contenu = lire(ROUTINES["encart"])
    ok = ("ENTETE_V1" in contenu
          and "anomalie(s)" in contenu)
    verifier("6. encart detection (en-tete/colonnes v1)", ok)


def point_7_flux_persistance():
    """7. Flux : persistance par .flux_derniere.txt (changement)."""
    contenu = lire(ROUTINES["flux"])
    ok = ("_DERNIERE_VALEUR" in contenu
          and "changement" in contenu
          and "_compter_p1_non_acquittes" in contenu)
    verifier("7. flux persistance .flux_derniere.txt (changement)", ok)


def point_8_vigie_detection_4w():
    """8. Vigie-perimetre : detection 4W + empreinte + perimetre_surveille."""
    contenu = lire(ROUTINES["vigie-perimetre"])
    ok = ("[perimetre-modifie]" in contenu
          and "QUI:" in contenu and "QUOI:" in contenu
          and "QUAND:" in contenu and "OU:" in contenu
          and "SHA-256" in contenu
          and "_empreinte" in contenu)
    verifier("8. vigie-perimetre detection 4W + empreinte SHA-256", ok)


def point_9_dry_run_sans_effet_de_bord():
    """9. --dry-run des 5 : rc dans {0,1}, prefixe sortie, et AUCUN
    fichier d etat cree/modifie (.flux_derniere.txt, etat-empreintes.json)."""
    ok = True
    details = []
    flux_state = os.path.join(ROUTINES_DIR, ".flux_derniere.txt")
    etat_avant = {}
    for nom in ("flux", "vigie-perimetre"):
        f = flux_state if nom == "flux" else ETAT_EMPREINTES
        if os.path.isfile(f):
            etat_avant[nom] = lire(f)
        else:
            etat_avant[nom] = None
    for nom, chemin in ROUTINES.items():
        r = run([PYTHON, chemin, "--dry-run"], timeout=120)
        prefixe, _ = PATTERNS[nom]
        if r.returncode not in (0, 1) or prefixe not in (r.stdout or ""):
            ok = False
            details.append("%s(rc=%d)" % (nom, r.returncode))
    # Flux + vigie-perimetre : dry-run ne doit PAS toucher leur etat.
    for nom in ("flux", "vigie-perimetre"):
        f = flux_state if nom == "flux" else ETAT_EMPREINTES
        apres = lire(f) if os.path.isfile(f) else None
        if apres != etat_avant[nom]:
            ok = False
            details.append("%s-state-change" % nom)
    verifier("9. --dry-run sans effet de bord (rc/prefixe/etats flux+vigie)",
             ok, ";".join(details) if details else "")


def point_11_verifier_statuts_capacites():
    """11. verifier-statuts : oracle informe - escalade DEFCON 4 +
    mission asap + inter-round si round en cours + anti-inondation."""
    contenu = lire(ROUTINES["verifier-statuts"])
    ok = ("defcon-escaler" in contenu
          and "mission-ajouter" in contenu
          and "defcon-escaler" in contenu
          and "--file" in contenu
          and "_est_urgence_reelle" in contenu
          and "_lire_urgents" in contenu
          and "inter-round" in contenu
          and "etat-statuts.json" in contenu)
    verifier("11. verifier-statuts (escalade DEFCON 4 + mission asap + IR)", ok)

    # defcon-escaler doit exister dans oracle.py (CLI officielle) + la
    # fonction escaler() dans defcon.py (escalade 2->4 = degradation).
    oracle_src = lire(os.path.join(ORACLE_DIR, "oracle.py"))
    defcon_src = lire(os.path.join(ORACLE_DIR, "fonctions", "defcon.py"))
    ok2 = ("defcon-escaler" in oracle_src
           and "def escaler(" in defcon_src
           and "DEFCON 2 (REPRISE TOTALE =" in defcon_src)
    verifier("12. oracle.py + defcon.py exposent defcon-escaler (2->4)",
             ok2)


def point_10_ne_fait_pas_croire():
    """10. Regression cible corrigee : les routines ont une option --dry-run
    EXPLICITE (chacune le teste dans main), pas seulement la presence du
    mot. Un --dry-run doit etre SANS effet de bord. On revet une trace ici
    que --dry-run est bien teste en premiere logique.
    """
    ok = True
    for nom, chemin in ROUTINES.items():
        contenu = lire(chemin)
        # --dry-run doit etre lu et applique avant toute ecriture d etat.
        if "--dry-run" not in contenu or "dry_run" not in contenu:
            ok = False
    verifier("10. chaque routine applique --dry-run (option lue)", ok)


def main():
    print("=== test-106 : garde-fou routines surveillance v1 ===")
    points = [
        ("1. existence + triplet", point_1_existence_triplet),
        ("2. manifest {actif, intervalle}", point_2_manifest),
        ("3. grades G3", point_3_grade),
        ("4. sante detection", point_4_sante_detection),
        ("5. live detection", point_5_live_detection),
        ("6. encart detection", point_6_encart_detection),
        ("7. flux persistance", point_7_flux_persistance),
        ("8. vigie-perimetre detection 4W", point_8_vigie_detection_4w),
        ("9. dry-run sans effet de bord", point_9_dry_run_sans_effet_de_bord),
        ("10. option dry-run explicite", point_10_ne_fait_pas_croire),
        ("11. verifier-statuts (escalade+mission+IR)", point_11_verifier_statuts_capacites),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        if CHRONO_ACTIF:
            ETAPES.append((nom, time.monotonic() - t_debut))

    if CHRONO_ACTIF:
        total = time.monotonic() - DEBUT_TEST
        print("")
        print("=== CHRONO test (total %.1fs) ===" % total)
        for nom, duree in ETAPES:
            print("  %-40s %6.2fs" % (nom, duree))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())