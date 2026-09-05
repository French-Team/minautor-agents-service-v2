#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-116-retour-aeroport-avant-cerberus-garde-fou.py
GARDE-FOU : lors d une fin-coordination d Oracle (modele aero), la trace
pilote RETOUR AEROPORT doit PRECEDER l activation de Cerberus (decision
utilisateur 2026-09-02, fix pilote.py v0.2.3, mission a7a14712).

Contexte (fix v0.2.3, 2026-09-02) :
  - Dans _reactiver_maillon (fonctions/pilote.py), l ordre reel des
    operations etait : 1) _fin_auto pose FIN oracle ; 2)
    aap.activer_cerberus ACTIVE Cerberus (trace RETOUR ORACLE dans la
    section cerberus) ; 3) PUIS _historiser_pilote(RETOUR AEROPORT).
    Semantiquement inverse : on lisait l atterrissage avant le retour a
    l aeroport.
  - Fix : la trace RETOUR AEROPORT (via _historiser_pilote) est ecrite
    AVANT aap.activer_cerberus dans la branche cible=cerberus (avec
    anti-doublon deja_trace). Defaut secondaire corrige : _historiser /
    _activer_maillon ecrivent de vrais millisecondes (%H:%M:%S.%f
    tronque a 3) au lieu de .000 fixe - l ordre inter-ecrivains est
    lisible.

Invariants verifies :
  1. pilote.py : VERSION v0.2.3 ; dans _reactiver_maillon, la ligne
     _historiser_pilote(RETOUR AEROPORT) precede le premier appel a
     aap.activer_cerberus (branche cible=cerberus de fin de round)
  2. Flux REEL (AGENTS-historique.md) : pour le cycle de fin-coordination
     le plus recent, l horodatage de la trace pilote RETOUR AEROPORT est
     ANTERIEUR a l activation de Cerberus (RETOUR ORACLE dans la section
     cerberus)
  3. Les traces pilote recentes portent de vrais millisecondes (pas le
     .000 fixe de l ancien code)
  4. Preuve negative : un historique simule avec RETOUR AEROPORT APRES
     l activation Cerberus est DETECTE comme incoherent (le garde-fou
     ne dort pas)
  5. Normes : ASCII strict + LF pur (outil cible + test) + purge

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: traces, modele-aero, pilote, garde-fou, preuve-negative
"""
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

PILOTE_PY = os.path.join(TOOLS_DIR, "oracle", "fonctions", "pilote.py")
HISTORIQUE = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")

TMP = os.path.join(PROJECT_ROOT, "tmp-test116")

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
    print("=== CHRONO test-116 (total %.1fs) ===" % total)
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


# ------------------------------------------------------------------
# Analyse de l historique (format v1 : ## jour / ### agent / entree)
# ------------------------------------------------------------------
HORODATE = re.compile(
    r"^-\s+(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?\s+\|\s+[^|]+\s+\|\s+[^|]+\s+\|\s+(.*)$")


def analyser_flux(texte):
    """Extraire les entrees pilote RETOUR AEROPORT et les activations Cerberus.

    Retourne (retours, activations) : listes de tuples
    (heure_str, milli, jour) triees par chronologie croissante, ou
    heure_str = 'HH:MM:SS[.mmm]' triable, milli = int ms (0 si absent).
    """
    jour_courant = ""
    agent_courant = ""
    lignes = texte.split("\n")
    retours = []
    activations = []
    for l in lignes:
        ligne = l.strip()
        if ligne.startswith("## ") and len(ligne) >= 13 and ligne[3].isdigit():
            jour_courant = ligne[3:].strip()
            continue
        if ligne.startswith("### "):
            agent_courant = ligne[4:].strip().lower()
            continue
        m = HORODATE.match(ligne)
        if not m:
            continue
        h, mi, s, frac, raison = m.groups()
        milli = int((frac or "000")[:3].ljust(3, "0"))
        heure = "%s:%s:%s.%03d" % (h, mi, s, milli)
        r = raison.strip().upper()
        if agent_courant == "pilote" and r.startswith("RETOUR AEROPORT"):
            retours.append((heure, milli, jour_courant, ligne))
        if agent_courant == "cerberus" and r.startswith("RETOUR ORACLE"):
            activations.append((heure, milli, jour_courant, ligne))
    retours.sort(key=lambda t: (t[2], t[0]))
    activations.sort(key=lambda t: (t[2], t[0]))
    return retours, activations


def detecter_inversion(texte):
    """Verifier le cycle de fin-coordination LE PLUS RECENT.

    L historique conserve les anciennes traces (posees AVANT le fix
    v0.2.3, ex: 18:44:28.000 apres l activation 18:44:27.882) : elles
    refletent le bug corrige et ne doivent pas faire KO en permanence.
    Le garde-fou verifie donc le CYCLE LE PLUS RECENT (dernier retour
    pilote du jour le plus recent qui en porte, et l activation cerberus
    qui doit le suivre) : l heure du retour doit etre < l heure de
    l activation. Un retour non suivi d une activation du meme jour avec
    une activation qui le PRECEDE = inversion detectee.
    Retourne (ok, details).
    """
    retours, activations = analyser_flux(texte)
    if not retours:
        return True, []
    heure_r, milli_r, jour, ligne = retours[-1]
    c_apres = [a for a in activations
               if a[2] == jour and a[0] >= heure_r]
    if c_apres:
        # Cycle conforme : le retour est suivi d une activation.
        return True, []
    c_avant = [a for a in activations
               if a[2] == jour and a[0] < heure_r]
    if c_avant:
        return False, [
            "retour %s (jour %s) APRES l activation %s - inversion"
            % (heure_r, jour, max(c_avant)[0])]
    # Retour sans aucune activation du jour : cycle incomplet, non juge.
    return True, []


# ------------------------------------------------------------------
# Points
# ------------------------------------------------------------------
def point_1_code():
    """pilote.py v0.2.4 : RETOUR AEROPORT AVANT activer_cerberus."""
    ok_existe = os.path.isfile(PILOTE_PY)
    ok_version = False
    ok_ordre = False
    detail = ""
    if ok_existe:
        r = lancer([PYTHON, PILOTE_PY, "--version"], timeout=60)
        ok_version = (r.returncode == 0 and "0.2.4" in r.stdout)
        with io.open(PILOTE_PY, encoding="utf-8", errors="replace") as fh:
            lignes = fh.read().split("\n")
        # Numero de la ligne _historiser_pilote(RETOUR AEROPORT) et du
        # premier aap.activer_cerberus qui la suit.
        pos_retour = None
        pos_activer = None
        for i, l in enumerate(lignes):
            if ("_historiser_pilote" in l
                    and "RETOUR AEROPORT" in l and pos_retour is None):
                pos_retour = i
            if "aap.activer_cerberus(" in l and pos_activer is None:
                pos_activer = i
        if pos_retour is not None and pos_activer is not None:
            ok_ordre = pos_retour < pos_activer
            detail = "retour ligne %d, activer ligne %d" % (pos_retour + 1,
                                                           pos_activer + 1)
        else:
            detail = "pos_retour=%s pos_activer=%s" % (pos_retour, pos_activer)
    verifier("1. pilote.py v0.2.4 : RETOUR AEROPORT AVANT activer_cerberus",
             ok_existe and ok_version and ok_ordre,
             detail or "fichier/version/ordre KO")


def point_2_flux_reel():
    """Flux reel : RETOUR AEROPORT < activation Cerberus (cycle recent)."""
    if not os.path.isfile(HISTORIQUE):
        verifier("2. flux reel : historique present", False, "fichier absent")
        return
    with io.open(HISTORIQUE, encoding="utf-8", errors="replace") as fh:
        texte = fh.read()
    ok, details = detecter_inversion(texte)
    verifier("2. flux reel : aucun RETOUR AEROPORT apres activation Cerberus",
             ok, "; ".join(details[:3]) or "aucun cycle fin-coordination" )


def point_3_ms_reels():
    """Les traces pilote recentes portent de vrais millisecondes."""
    if not os.path.isfile(HISTORIQUE):
        verifier("3. ms reels : historique present", False, "fichier absent")
        return
    with io.open(HISTORIQUE, encoding="utf-8", errors="replace") as fh:
        texte = fh.read()
    retours, _ = analyser_flux(texte)
    if not retours:
        verifier("3. ms reels : au moins une trace RETOUR AEROPORT trouvee",
                 False, "aucune trace pilote")
        return
    # Prendre la trace la plus recente (derniere de la liste triee) :
    # les anciennes (avant v0.2.3) peuvent porter .000.
    heure_recente, milli_recent, jour, _ = retours[-1]
    ligne_recente = retours[-1][3]
    verifier("3. trace pilote recente porte de vrais ms (pas .000 fixe)",
             milli_recent != 0,
             "jour=%s heure=%s ligne=%s" % (jour, heure_recente, ligne_recente))


def point_4_preuve_negative():
    """Inversion simulee -> detectee par l analyseur."""
    modele = """## 2026-09-02

### cerberus
- 19:04:18.601 | glm5 | R | RETOUR ORACLE : FIN: COORDINATION TERMINEE - X

### pilote
- 19:04:20.371 | glm5 | R | RETOUR AEROPORT: oracle
"""
    ok, details = detecter_inversion(modele)
    verifier("4. preuve negative : RETOUR AEROPORT apres activation detecte",
             (not ok) and len(details) >= 1,
             "detail=%s" % "; ".join(details[:2]) if details else "non detecte")


def point_5_conforme():
    """Modele conforme : RETOUR AEROPORT avant activation -> aucun probleme."""
    modele = """## 2026-09-02

### cerberus
- 19:04:18.601 | glm5 | R | RETOUR ORACLE : FIN: COORDINATION TERMINEE - X

### pilote
- 19:04:18.371 | glm5 | R | RETOUR AEROPORT: oracle
"""
    ok, details = detecter_inversion(modele)
    verifier("5. modele conforme : aucun probleme signale",
             ok and not details, "; ".join(details[:2]) if details else "")


def point_6_normes():
    fichiers = [os.path.abspath(__file__), PILOTE_PY]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("6. ASCII strict : 0 non-ASCII (pilote.py + test)",
             total_na == 0, "nb=%d" % total_na)
    verifier("7. LF pur : 0 CRLF (pilote.py + test)",
             total_crlf == 0, "nb=%d" % total_crlf)


def nettoyer_test():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP, ignore_errors=True)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-116 : RETOUR AEROPORT PRECEDE l activation Cerberus ===")
    try:
        if point_actif(1):
            t0 = time.monotonic()
            point_1_code()
            chrono_etape("1. code", t0)
        if point_actif(2):
            t0 = time.monotonic()
            point_2_flux_reel()
            chrono_etape("2. flux reel", t0)
        if point_actif(3):
            t0 = time.monotonic()
            point_3_ms_reels()
            chrono_etape("3. ms reels", t0)
        if point_actif(4):
            t0 = time.monotonic()
            point_4_preuve_negative()
            chrono_etape("4. preuve negative", t0)
        if point_actif(5):
            t0 = time.monotonic()
            point_5_conforme()
            chrono_etape("5. modele conforme", t0)
        if point_actif(6):
            t0 = time.monotonic()
            point_6_normes()
            chrono_etape("6. normes", t0)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
    except Exception as e:
        print("  [KO] EXCEPTION : %s" % e)
        NB_KO += 1
    finally:
        nettoyer_test()

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (retour aeroport avant cerberus)"
                                    if NB_KO == 0 else "KO (flux incoherent)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())