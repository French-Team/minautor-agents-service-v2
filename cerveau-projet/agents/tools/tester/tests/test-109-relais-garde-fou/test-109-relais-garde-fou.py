#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-109-relais-garde-fou.py

Garde-fou du relais Oracle v1 (oracle/fonctions/relais.py), le module
qui pousse les messages du hub (inbox/cerberus.jsonl) vers leurs
destinataires.

Contexte (2026-08-29) : BUG CRITIQUE CORRIGE - corruption en cascade du
hub. _ecrire_jsonl appliquait json.dumps() sur des lignes BRUTES deja
serialisees : a chaque tic du daemon, le relais re-echappait le JSON
d'une couche -> croissance exponentielle (le hub a atteint 1 Go de
guillemets imbriques). Fix : un str est ecrit TEL QUEL, un dict est
serialise une seule fois.

Points verifies :
  1. Le module existe, compile et est importable.
  2. FIX verrouille : _ecrire_jsonl ecrit un str tel quel (pas de
     json.dumps sur un brut deja serialise).
  3. Stabilite taille : une ligne deja serialisee (simple ou double-
     echappee) ne GROSSIT PAS apres relayer_hub.
  4. Pas de re-echappement en cascade : apres 5 tics successifs, la
     taille totale reste stable (<= taille initiale).
  5. Un message non-lu double-echappe est marque lu et normalise
     (devient un JSON simple, taille reduite ou stable).
  6. Les messages deja lus sont conserves tels quels.
  7. relayer_hub retourne le bon nombre de messages relayes.
  8. Script ASCII (convention v1).
  AUDIT DU HUB REEL (anti-recurrence 2026-08-29, apres incident 1 Go) :
  9. Taille du hub raisonnable (< 1 Mo, pas de retour a la croissance
     exponentielle).
 10. Chaque ligne du hub est un dict JSON valide (aucun double-
     echappement, aucune ligne illisible).
 11. Aucune signature de la cascade (guillemets imbriques anormaux).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.1
Tags: relais, hub, corruption, jsonl, oracle, garde-fou, anti-recurrence
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

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

ORACLE_DIR = os.path.join(TOOLS_DIR, "oracle")
RELAIS = os.path.join(ORACLE_DIR, "fonctions", "relais.py")
HUB = os.path.join(ORACLE_DIR, "inbox", "cerberus.jsonl")
# Seuil de taille du hub : au-dela, signe de re-croissance (l incident
# avait atteint 1 Go ; un hub sain fait quelques Ko).
SEUIL_HUB_OCTETS = 1024 * 1024

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


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def charger_relais():
    """Charger relais.py en module."""
    spec = importlib.util.spec_from_file_location("relais_test", RELAIS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _message(lu=True, de="agent-x", vers="cerberus", double=False):
    """Construire un message de hub. double=True = double-echappe (le
    format corrompu produit par l ancien bug)."""
    base = {
        "id": "msg-1",
        "de": de,
        "vers": vers,
        "priorite": 2,
        "date": "2026-08-29T09:00:00",
        "objet": "Test",
        "corps": "corps",
        "lu": lu,
        "accuse": lu,
        "type": "test",
    }
    if double:
        # json.dumps une fois de plus : la ligne est une CHAINE JSON
        return json.dumps(json.dumps(base, ensure_ascii=False),
                          ensure_ascii=False)
    return json.dumps(base, ensure_ascii=False)


def point_1_module_existe():
    ok = (os.path.isfile(RELAIS)
          and "def relayer_hub()" in lire(RELAIS)
          and "def _ecrire_jsonl" in lire(RELAIS))
    verifier("1. relais.py existe (relayer_hub, _ecrire_jsonl)", ok)


def point_2_fix_anti_reechappement():
    """2. FIX verrouille : _ecrire_jsonl ecrit un str tel quel.
    Le code du fix : 'if isinstance(msg, str): f.write(msg + chr(10))'."""
    contenu = lire(RELAIS)
    ok = ("isinstance(msg, str)" in contenu
          and "f.write(msg" in contenu)
    verifier("2. FIX: _ecrire_jsonl ecrit un str tel quel", ok)


def point_3_stabilite_ligne_deja_serialisee():
    """3. Stabilite : une ligne deja serialisee ne GROSSIT PAS.
    Simule le hub dans un dossier temporaire (remplacement INBOX_DIR),
    sans toucher au vrai hub."""
    try:
        mod = charger_relais()
        tmp = tempfile.mkdtemp(prefix="relais-test-")
        try:
            hub = os.path.join(tmp, "cerberus.jsonl")
            # Ligne simple lue + ligne double-echappee lue : ni l'une ni
            # l'autre ne doit grossir (fix : str ecrit tel quel).
            lignes = [_message(lu=True, double=False),
                      _message(lu=True, double=True)]
            with io.open(hub, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lignes) + "\n")
            avant = os.path.getsize(hub)
            # Detourner les chemins du module vers le temp.
            old_inbox = mod.INBOX_DIR
            mod.INBOX_DIR = tmp
            old_outbox = mod.OUTBOX_DIR
            mod.OUTBOX_DIR = tmp
            try:
                mod.relayer_hub()
            finally:
                mod.INBOX_DIR = old_inbox
                mod.OUTBOX_DIR = old_outbox
            apres = os.path.getsize(hub)
            ok = apres <= avant
            verifier("3. stabilite taille (lignes lues conservees)", ok,
                     "avant=%d apres=%d (croissance %+d)"
                     % (avant, apres, apres - avant))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:
        verifier("3. stabilite taille (lignes lues conservees)", False,
                 str(exc)[:120])


def point_4_pas_de_cascade_5_tics():
    """4. Pas de cascade : 5 tics successifs, taille stable (<= initial)."""
    try:
        mod = charger_relais()
        tmp = tempfile.mkdtemp(prefix="relais-test-")
        try:
            hub = os.path.join(tmp, "cerberus.jsonl")
            lignes = [_message(lu=True, double=True),
                      _message(lu=False, de="agent-y", double=True)]
            with io.open(hub, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lignes) + "\n")
            taille_apres = []
            old_inbox, old_outbox = mod.INBOX_DIR, mod.OUTBOX_DIR
            mod.INBOX_DIR, mod.OUTBOX_DIR = tmp, tmp
            try:
                for _ in range(5):
                    mod.relayer_hub()
                    taille_apres.append(os.path.getsize(hub))
            finally:
                mod.INBOX_DIR, mod.OUTBOX_DIR = old_inbox, old_outbox
            # Aucun tic ne doit faire grossir le fichier.
            ok = all(t <= taille_apres[0] for t in taille_apres)
            verifier("4. pas de cascade sur 5 tics (taille stable)", ok,
                     "tailles=%s" % taille_apres)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:
        verifier("4. pas de cascade sur 5 tics (taille stable)", False,
                 str(exc)[:120])


def point_5_normalisation_non_lu():
    """5. Un message non-lu double-echappe est marque lu et normalise
    (taille reduite ou stable, plus jamais double-echappe)."""
    try:
        mod = charger_relais()
        tmp = tempfile.mkdtemp(prefix="relais-test-")
        try:
            hub = os.path.join(tmp, "cerberus.jsonl")
            ligne = _message(lu=False, de="agent-y", double=True)
            with io.open(hub, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(ligne + "\n")
            old_inbox, old_outbox = mod.INBOX_DIR, mod.OUTBOX_DIR
            mod.INBOX_DIR, mod.OUTBOX_DIR = tmp, tmp
            try:
                nb, _ = mod.relayer_hub()
            finally:
                mod.INBOX_DIR, mod.OUTBOX_DIR = old_inbox, old_outbox
            apres = lire(hub).strip()
            # Marque lu, un seul niveau de serialisation (JSON simple).
            ok = (nb == 1
                  and apres.startswith("{")
                  and "\"lu\": true" in apres)
            verifier("5. non-lu double-echappe marque lu + normalise", ok,
                     "nb=%d extrait=%s" % (nb, apres[:80]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:
        verifier("5. non-lu double-echappe marque lu + normalise", False,
                 str(exc)[:120])


def point_6_lus_conserves():
    """6. Les messages deja lus sont conserves tels quels."""
    try:
        mod = charger_relais()
        tmp = tempfile.mkdtemp(prefix="relais-test-")
        try:
            hub = os.path.join(tmp, "cerberus.jsonl")
            ligne = _message(lu=True, double=True)
            with io.open(hub, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(ligne + "\n")
            old_inbox, old_outbox = mod.INBOX_DIR, mod.OUTBOX_DIR
            mod.INBOX_DIR, mod.OUTBOX_DIR = tmp, tmp
            try:
                nb, _ = mod.relayer_hub()
            finally:
                mod.INBOX_DIR, mod.OUTBOX_DIR = old_inbox, old_outbox
            apres = lire(hub).strip()
            ok = (nb == 0 and apres == ligne)
            verifier("6. messages lus conserves tels quels", ok,
                     "nb=%d modifie=%s" % (nb, apres != ligne))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:
        verifier("6. messages lus conserves tels quels", False,
                 str(exc)[:120])


def point_7_nb_relayes():
    """7. relayer_hub retourne le nombre correct de relayes."""
    try:
        mod = charger_relais()
        tmp = tempfile.mkdtemp(prefix="relais-test-")
        try:
            hub = os.path.join(tmp, "cerberus.jsonl")
            lignes = [_message(lu=False, de="agent-a", double=False),
                      _message(lu=False, de="agent-b", double=False),
                      _message(lu=True, double=False)]
            with io.open(hub, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lignes) + "\n")
            old_inbox, old_outbox = mod.INBOX_DIR, mod.OUTBOX_DIR
            mod.INBOX_DIR, mod.OUTBOX_DIR = tmp, tmp
            try:
                nb, details = mod.relayer_hub()
            finally:
                mod.INBOX_DIR, mod.OUTBOX_DIR = old_inbox, old_outbox
            ok = (nb == 2 and len(details) == 2)
            verifier("7. relayer_hub retourne le bon nb de relayes", ok,
                     "nb=%d details=%d" % (nb, len(details)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:
        verifier("7. relayer_hub retourne le bon nb de relayes", False,
                 str(exc)[:120])


def point_8_ascii():
    contenu = lire(RELAIS)
    ok = not any(ord(c) > 127 for c in contenu)
    verifier("8. script ASCII (convention v1)", ok)


def _audit_hub():
    """Audit du hub reel : retourne (taille, nb_lignes, illisibles,
    str2x, cascade). cascade = plus de 50% de lignes avec des
    guillemets imbriques anormaux (signature de la corruption)."""
    if not os.path.isfile(HUB):
        return 0, 0, 0, 0, False
    taille = os.path.getsize(HUB)
    illisibles = 0
    str2x = 0
    nb = 0
    cascade = False
    with io.open(HUB, "r", encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            l = ligne.strip()
            if not l:
                continue
            nb += 1
            try:
                dec = json.loads(l)
                if isinstance(dec, str):
                    str2x += 1
                    # double-echappe : doit redevenir un dict au niveau 2
                    try:
                        dec2 = json.loads(dec)
                        if not isinstance(dec2, dict):
                            illisibles += 1
                    except ValueError:
                        illisibles += 1
                elif not isinstance(dec, dict):
                    illisibles += 1
            except ValueError:
                illisibles += 1
    if nb and (illisibles + str2x) > nb // 2:
        cascade = True
    return taille, nb, illisibles, str2x, cascade


def point_9_hub_taille():
    """9. Taille du hub raisonnable (< 1 Mo). L incident avait atteint
    1 Go : toute re-croissance exponentielle doit etre detectee."""
    taille, nb, _, _, _ = _audit_hub()
    ok = taille <= SEUIL_HUB_OCTETS
    verifier("9. taille hub raisonnable (< 1 Mo)", ok,
             "taille=%d octets (%d lignes)" % (taille, nb))


def point_10_hub_lignes_valides():
    """10. Chaque ligne du hub est un dict JSON valide (aucun double-
    echappement, aucune ligne illisible)."""
    taille, nb, illisibles, str2x, _ = _audit_hub()
    ok = (illisibles == 0 and str2x == 0)
    verifier("10. hub: lignes dict valides (0 illisible, 0 double-echappe)",
             ok, "illisibles=%d str2x=%d sur %d lignes"
             % (illisibles, str2x, nb))


def point_11_hub_pas_cascade():
    """11. Aucune signature de la cascade (guillemets imbriques)."""
    taille, nb, illisibles, str2x, cascade = _audit_hub()
    ok = not cascade
    verifier("11. hub: aucune signature de cascade", ok,
             "cascade=%s (illisibles=%d str2x=%d)"
             % (cascade, illisibles, str2x))


def main():
    print("=== test-109 : garde-fou relais Oracle v1 ===")
    points = [
        ("1. module existe", point_1_module_existe),
        ("2. FIX anti-reechappement", point_2_fix_anti_reechappement),
        ("3. stabilite lignes serialisees", point_3_stabilite_ligne_deja_serialisee),
        ("4. pas de cascade 5 tics", point_4_pas_de_cascade_5_tics),
        ("5. normalisation non-lu", point_5_normalisation_non_lu),
        ("6. lus conserves tels quels", point_6_lus_conserves),
        ("7. nb relayes correct", point_7_nb_relayes),
        ("8. ASCII", point_8_ascii),
        ("9. audit hub: taille", point_9_hub_taille),
        ("10. audit hub: lignes valides", point_10_hub_lignes_valides),
        ("11. audit hub: pas de cascade", point_11_hub_pas_cascade),
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