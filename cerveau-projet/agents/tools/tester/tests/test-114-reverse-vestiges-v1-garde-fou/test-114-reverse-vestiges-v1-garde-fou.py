#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-114-reverse-vestiges-v1-garde-fou.py

REVERSE DE LA NON-REGRESSION (decision utilisateur 2026-09-02) : la suite
ne verifie plus seulement qu une modification n a rien casse : elle devient
un MOYEN DE RETROUVER LES VESTIGES DE LA V1 encore presents dans les
structures v2. La v2 (arbres, themes, fins, guider-arbre, pilote) est la
reference depuis 2026-08-29 ; les parcours-*.json v1 sont des ARCHIVES
protegees par le marbre (hors perimetre de ce scan).

Ce test remplace le role actif v2 des gardes-fous v1 suivants :
  - test-018 (fins REACTIVER-CERBERUS dans les 15 parcours v1) : en v2,
    les fins vivent dans fins.json de chaque agent et suivent le modele
    aero (action=reactiver + cible=oracle + reactiver-fin <agent>
    --cible oracle). Les redirections (fin-theme, action=redirection)
    ramenent a la racine de l arbre et ne sont PAS des fins.
  - test-072 (relecture c0/c0b en cases de parcours v1) : en v2, la
    relecture obligatoire est gravee dans la regle D7 de chaque arbre
    (arbre.regles : RELIRE OBLIGATOIRE, corrections puis fiche). Seule
    exception documentee : un agent declare dans ses regles un mode
    Round SOLO / MODE CONVERSATION (reactivation Cerberus en fin de
    cycle), comme redacteur-v2 (D5).

Le REVERSE en action : tout token v1 de GUIDAGE (guider-parcours,
parcours-demarrage) trouve dans une structure v2 (theme-*.json,
arbre-*.json, fins.json - hors archives parcours-*.json et hors .bak)
fait ECHOUER ce test : c est un vestige a purger, pas une regle a garder.

Points verifies :
  1. Agents v2 detectes (arbre-<agent>.json) : >= 20.
  2. Chaque agent v2 possede son fins.json.
  3. Toute fin RELLE (action=reactiver) porte cible=oracle + la commande
     reactiver-fin (modele aero R1/R3 : jamais cerberus) - EXCEPTION
     DOCUMENTEE (decision utilisateur 2026-09-02) : la fin
     fin-coordination de l aeroport ORACLE atterrit sur CERBERUS avec le
     bilan consolide (fin de round). fin-signal/fin-inter-round d oracle
     restent cible=oracle.
  4. Toute redirection (action=redirection) pointe vers arbre-<agent>.json.
  5. Relecture v2 : chaque arbre declare la regle D7 (RELIRE OBLIGATOIRE
     avec corrections ET fiche) OU l exception Round SOLO /
     MODE CONVERSATION (cas redacteur-v2 documente).
  6. REVERSE : zero token v1 de guidage (guider-parcours,
     parcours-demarrage) dans les structures v2.
  7. Normes : ASCII strict + LF pur sur les structures v2 scannees.
  8. Preuve negative : un agent factice (zz-vestige, != oracle) avec une
     fin vers cerberus et un arbre sans D7 ni exception est DETECTE (le
     scan marche vraiment - l exception oracle reste etroite).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.1
Tags: reverse, vestiges-v1, arbres-v2, modele-aero, relecture, garde-fou
"""
import glob
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
AGENTS_BASE = os.path.join(CERVEau, "agents")
TOOLS_DIR = os.path.join(AGENTS_BASE, "tools")

TOKENS_V1 = ["guider-parcours", "parcours-demarrage"]

TMP_BASE = os.path.join(tempfile.gettempdir(), "tmp-rev-v1-test-114")

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


def agents_v2(base):
    """Agents porteurs d un arbre v2 (arbre-<agent>.json).
    Le chemin est base/<agent>/parcours/arbre-*.json : l agent est le
    nom du dossier PARENT du dossier parcours."""
    return sorted(set(os.path.basename(os.path.dirname(os.path.dirname(p)))
                      for p in glob.glob(os.path.join(base, "*", "parcours",
                                                      "arbre-*.json"))))


def structures_v2(agent, base):
    """Fichiers de decision v2 d un agent (hors archives parcours-*.json
    et hors .bak)."""
    dossier = os.path.join(base, agent, "parcours")
    result = []
    for nom in sorted(os.listdir(dossier)):
        if not nom.endswith(".json"):
            continue
        if nom.startswith("parcours-") or nom.endswith(".bak"):
            continue
        result.append(os.path.join(dossier, nom))
    return result


def erreurs_fins(agent, base):
    """Fins reelles non-oracle OU redirections sans cible d arbre.

    EXCEPTION DOCUMENTEE (decision utilisateur 2026-09-02) : la fin
    fin-coordination de l aeroport ORACLE atterrit sur CERBERUS avec le
    bilan consolide (fin de round - Cerberus est le point de
    Depart/arrivee des demandes utilisateur). Toute AUTRE fin reactiver
    (tout autre agent, ou oracle fin-signal/fin-inter-round) doit viser
    oracle. La preuve negative (point 8) utilise un agent factice
    zz-vestige -> il reste detecte."""
    erreurs = []
    chemin = os.path.join(base, agent, "parcours", "fins.json")
    try:
        data = json.loads(lire(chemin))
    except (OSError, ValueError):
        return ["fins.json illisible"]
    for fid, fin in (data.get("fins") or {}).items():
        action = fin.get("action", "")
        if action == "reactiver":
            cible = fin.get("cible")
            if cible != "oracle":
                # EXCEPTION fin de round : oracle/fin-coordination -> cerberus
                if not (agent.lower() == "oracle" and fid == "fin-coordination"
                        and cible == "cerberus"):
                    erreurs.append("%s cible=%s" % (fid, cible))
            if "reactiver-fin" not in fin.get("commande", ""):
                erreurs.append("%s commande sans reactiver-fin" % fid)
        elif action == "redirection":
            vers = fin.get("vers", "")
            if not vers.endswith("arbre-%s.json" % agent):
                erreurs.append("%s vers=%s" % (fid, vers))
    return erreurs


def a_relecture_v2(agent, base):
    """La relecture v2 est gravee dans l arbre (regle D7) OU l agent
    declare l exception Round SOLO / MODE CONVERSATION."""
    candidats = glob.glob(os.path.join(base, agent, "parcours",
                                       "arbre-*.json"))
    if not candidats:
        return False, "pas d arbre"
    arbre = json.loads(lire(candidats[0]))
    regles = json.dumps((arbre.get("arbre") or {}).get("regles") or {},
                        ensure_ascii=False)
    if "RELIRE" in regles:
        if "corrections" not in regles or "fiche" not in regles:
            return False, "D7 partiel (corrections/fiche absent)"
        return True, ""
    if "Round SOLO" in regles or "MODE CONVERSATION" in regles:
        return True, "exception Round SOLO / MODE CONVERSATION"
    return False, "ni D7 RELIRE ni exception declaree"


def erreurs_tokens_v1(agent, base):
    """Tokens v1 de guidage presents dans les structures v2 (REVERSE)."""
    trouves = []
    for chemin in structures_v2(agent, base):
        texte = lire(chemin)
        for token in TOKENS_V1:
            if token in texte:
                trouves.append("%s:%s" % (os.path.basename(chemin), token))
    return trouves


def erreurs_ascii_lf(agent, base):
    erreurs = []
    for chemin in structures_v2(agent, base):
        try:
            data = open(chemin, "rb").read()
        except OSError:
            continue
        crlf = data.count(b"\r\n")
        non_ascii = len([c for c in data if c > 127])
        if crlf or non_ascii:
            erreurs.append("%s: CRLF=%d >127=%d" % (os.path.basename(chemin),
                                                    crlf, non_ascii))
    return erreurs


def _ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)


def _agent_factice(nom):
    """Agent factice : fin vers cerberus + arbre sans D7 ni exception."""
    base = os.path.join(TMP_BASE, "agents", nom)
    _ecrire(os.path.join(base, "parcours", "arbre-%s.json" % nom),
            json.dumps({"arbre": {"regles": {"D1": "aucune relecture"}}},
                       ensure_ascii=True, indent=1))
    _ecrire(os.path.join(base, "parcours", "fins.json"),
            json.dumps({"fins": {"fin-x": {
                "action": "reactiver", "cible": "cerberus",
                "commande": "python3 oracle.py reactiver-fin %s" % nom}}},
                ensure_ascii=True, indent=1))
    return base


def _nettoyer():
    shutil.rmtree(TMP_BASE, ignore_errors=True)


def point_1_decouverte():
    agents = agents_v2(AGENTS_BASE)
    verifier("1. agents v2 detectes (>= 20, trouve: %d)" % len(agents),
             len(agents) >= 20, "agents=%s" % ", ".join(agents[:5]))


def point_2_fins_presentes():
    manquants = []
    for agent in agents_v2(AGENTS_BASE):
        chemin = os.path.join(AGENTS_BASE, agent, "parcours", "fins.json")
        if not os.path.isfile(chemin):
            manquants.append(agent)
    verifier("2. fins.json present pour chaque agent v2", not manquants,
             "manquants: %s" % ", ".join(manquants))


def point_3_fins_oracle():
    details = []
    for agent in agents_v2(AGENTS_BASE):
        for err in erreurs_fins(agent, AGENTS_BASE):
            if "cible" in err or "reactiver-fin" in err:
                details.append("%s: %s" % (agent, err))
    verifier("3. fins reelles -> oracle + reactiver-fin (modele aero)",
             not details, "; ".join(details))


def point_4_redirections():
    details = []
    for agent in agents_v2(AGENTS_BASE):
        for err in erreurs_fins(agent, AGENTS_BASE):
            if err.startswith("vers="):
                details.append("%s: %s" % (agent, err))
    verifier("4. redirections -> arbre-<agent>.json", not details,
             "; ".join(details))


def point_5_relecture_v2():
    details = []
    for agent in agents_v2(AGENTS_BASE):
        ok, raison = a_relecture_v2(agent, AGENTS_BASE)
        if not ok:
            details.append("%s: %s" % (agent, raison))
    verifier("5. relecture v2 (D7 RELIRE ou exception documentee)",
             not details, "; ".join(details))


def point_6_reverse_tokens():
    details = []
    for agent in agents_v2(AGENTS_BASE):
        for err in erreurs_tokens_v1(agent, AGENTS_BASE):
            details.append("%s: %s" % (agent, err))
    verifier("6. REVERSE : 0 token v1 (guider-parcours, parcours-demarrage)"
             " dans les structures v2", not details, "; ".join(details))


def point_7_ascii_lf():
    details = []
    for agent in agents_v2(AGENTS_BASE):
        for err in erreurs_ascii_lf(agent, AGENTS_BASE):
            details.append("%s: %s" % (agent, err))
    verifier("7. ASCII strict + LF pur sur les structures v2", not details,
             "; ".join(details))


def point_8_preuve_negative():
    _nettoyer()
    base = _agent_factice("zz-vestige")
    nom = "zz-vestige"
    erreurs_fin = erreurs_fins(nom, os.path.join(base, ".."))
    ok_relecture, raison = a_relecture_v2(nom, os.path.join(base, ".."))
    detecte = any("cible=cerberus" in e or "reactiver-fin" in e
                  for e in erreurs_fin)
    detecte = detecte and not ok_relecture
    _ecrire(os.path.join(base, "parcours", "theme-x.json"),
            json.dumps({"themes": [{"etapes": ["relancer guider-parcours"]}]},
                       ensure_ascii=True, indent=1))
    tokens = erreurs_tokens_v1(nom, os.path.join(base, ".."))
    detecte = detecte and any("guider-parcours" in t for t in tokens)
    verifier("8. preuve negative : fin cerberus + arbre sans D7 + token v1"
             " -> detectes (%s)" % raison, detecte,
             "fin=%s relecture=%s tokens=%s" % (erreurs_fin, raison, tokens))
    _nettoyer()


def main():
    print("=== test-114 : reverse - les structures v2 ne doivent plus"
          " porter de vestiges v1 ===")
    points = [
        ("1. agents v2 detectes", point_1_decouverte),
        ("2. fins.json presents", point_2_fins_presentes),
        ("3. fins -> oracle (aero)", point_3_fins_oracle),
        ("4. redirections -> arbre", point_4_redirections),
        ("5. relecture v2 (D7)", point_5_relecture_v2),
        ("6. 0 token v1 (reverse)", point_6_reverse_tokens),
        ("7. ASCII + LF", point_7_ascii_lf),
        ("8. preuve negative", point_8_preuve_negative),
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
        print("=== CHRONO test (total %.1fs) === " % total)
        for nom, duree in ETAPES:
            print("  %-34s %6.2fs" % (nom, duree))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
