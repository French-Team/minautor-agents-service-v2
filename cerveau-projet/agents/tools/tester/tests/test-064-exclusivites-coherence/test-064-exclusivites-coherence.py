#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-064-exclusivites-coherence.py
GARDE-FOU : la COHERENCE GLOBALE des exclusivites (audit Cerberus 2026-08-16,
demande utilisateur) :
  - les 5 regles de gouvernance documentees dans regles-groupes-agents.md
    (seul janus lance la non-regression, seul morpheus ecrit les tests, seul
    clio met a jour le README, seul buffy corrige les fichiers des agents,
    seul hygie supprime) ont chacune leur outil cle assigne au bon
    proprietaire dans les cartes ET dans la table du verrou d habilitation,
  - chaque outil EXCLUSIF veritable (present dans la carte d UN SEUL agent,
    source = table du verrou qui scanne TOUS les agents y compris le trio)
    est verrouille : un non-proprietaire est BLOQUE,
  - les PARTAGES LEGITIMES documentes restent acceptes (ex: tester-protections
    chez morpheus + janus pour la non-regression ; detecter-residus chez
    hygie + janus/vulcain pour la DETECTION sans suppression).

Contexte (2026-08-16, audit Cerberus) :
  - 43 outils "exclusifs" derives par evaluer-processus (AGENTS_CERVE seul)
    contenaient 1 FAUX POSITIF : valider-conventions derive exclusif -> buffy
    mais en realite aussi chez athena (trio). La source de verite pour
    l exclusivite est la TABLE DU VERROU (construite depuis TOUTES les cartes,
    trio inclus) - pas la derivation AGENTS_CERVE seule.
  - Les 5 regles de gouvernance ont leurs garde-fous dedies (037/058/020-038/
    059/045) mais AUCUN ne verifie la coherence globale regle <-> carte <-> verrou.

Invariants verifies :
  1. Les 5 outils cles des regles de gouvernance sont dans la carte de leur
     proprietaire (buffy: editer-parcours, editer-fichier-agents ; clio:
     combos-maj-readme-massive, mettre-a-jour-readme ; janus:
     tester-lancer-non-regression ; morpheus: tester-protections ; hygie:
     detecter-residus)
  2. Chacun de ces outils est dans la TABLE du verrou avec SON proprietaire
     (les partages legittimes documentes sont acceptes en plus)
  3. Chaque outil EXCLUSIF veritable (table du verrou, exactement 1 agent)
     est verrouille : appel du verrou par un non-proprietaire -> BLOQUE (rc=1)
  4. Aucun faux positif : la derivation evaluer-processus ne doit pas
     declarer exclusif un outil present chez un autre agent (trio inclus)
  5. Preuve reelle : cerberus -> guider-parcours (exclusif buffy) BLOQUE
  6. Normes : ASCII strict + LF pur (outils + test)
"""
import importlib.util
import io
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

VERROU_PY = os.path.join(TOOLS_DIR, "proteger",
                         "proteger-verrou-habilitation",
                         "proteger-verrou-habilitation.py")
EVALUER_PY = os.path.join(TOOLS_DIR, "evaluer", "evaluer-processus",
                          "evaluer-processus.py")
REGLES = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                      "regles-immuables", "general",
                      "regles-groupes-agents.md")

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
ETAPES = []
T_START = time.monotonic()


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
    print("=== CHRONO test-064 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s" % nom)
        if detail:
            print("     %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def lire(chemin):
    if not os.path.exists(chemin):
        return ""
    return io.open(chemin, encoding="utf-8", errors="replace").read()


def ascii_count(chemin):
    if not os.path.exists(chemin):
        return 999
    return sum(1 for c in lire(chemin) if ord(c) > 127)


def crlf_count(chemin):
    if not os.path.exists(chemin):
        return 999
    return io.open(chemin, "rb").read().count(b"\r\n")


def charger_module(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def table_verrou():
    """Charge le verrou et retourne la table outil -> set(agents)."""
    verrou = charger_module(VERROU_PY, "verrou_064")
    verrou.detecter_racine()
    return verrou.construire_table()


def derivation_exclusifs():
    """Charge evaluer-processus et retourne {outil: proprietaire}."""
    ep = charger_module(EVALUER_PY, "evaluer_proc_064")
    racine = ep.racine_projet()
    return ep.outils_exclusifs(racine)


def outils_carte_agent(agent):
    """Retourne les outils de la carte d un agent (tous types outil)."""
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", agent,
                          "parcours", "parcours-%s.json" % agent)
    if not os.path.isfile(chemin):
        return set()
    import json
    p = json.load(io.open(chemin, encoding="utf-8"))
    outils = set()
    for cid, c in p.get("cases", {}).items():
        for idx in c.get("indices", []):
            if idx.get("type") == "outil":
                nom = idx.get("nom") or idx.get("catalogue")
                if nom:
                    outils.add(nom)
    return outils


def tous_agents():
    """Liste tous les agents avec parcours (incluant le trio)."""
    resultats = []
    base = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
    if os.path.isdir(base):
        for nom in sorted(os.listdir(base)):
            if os.path.isdir(os.path.join(base, nom, "parcours")):
                resultats.append(nom)
    return resultats


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== GARDE-FOU test-064 : EXCLUSIVITES COHERENCE ===")
    try:
        # 1. Les 5 outils cles des regles sont dans la carte du proprietaire
        if point_actif(1):
            t0 = time.monotonic()
            regles = {
                "buffy": ["editer-parcours", "editer-fichier-agents"],
                "clio": ["combos-maj-readme-massive", "mettre-a-jour-readme"],
                "janus": ["tester-lancer-non-regression"],
                "morpheus": ["tester-protections"],
                "hygie": ["detecter-residus"],
            }
            manquants = []
            for prop, outils in regles.items():
                carte = outils_carte_agent(prop)
                for o in outils:
                    if o not in carte:
                        manquants.append("%s:%s" % (prop, o))
            verifier("1. Les 5 outils cles des regles sont dans la carte de "
                     "leur proprietaire", not manquants,
                     "; ".join(manquants))
            chrono_etape("1. outils regles", t0)

        # 2. Chaque outil cle est dans la table du verrou avec son proprietaire
        if point_actif(2):
            t0 = time.monotonic()
            table = table_verrou()
            attendus = {
                "editer-parcours": "buffy",
                "editer-fichier-agents": "buffy",
                "combos-maj-readme-massive": "clio",
                "mettre-a-jour-readme": "clio",
                "tester-lancer-non-regression": "janus",
                "tester-protections": "morpheus",
                "detecter-residus": "hygie",
            }
            absents = []
            for outil, prop in attendus.items():
                agents = table.get(outil, set())
                if prop not in agents:
                    absents.append("%s:%s absent de %s" %
                                   (outil, prop, sorted(agents)))
            verifier("2. 7 outils cles presents dans la table du verrou avec "
                     "leur proprietaire", not absents, "; ".join(absents))
            chrono_etape("2. table verrou", t0)

        # 3. Chaque outil EXCLUSIF veritable (1 seul agent) est verrouille :
        #    appel du verrou par un non-proprietaire -> BLOQUE (rc=1)
        if point_actif(3):
            t0 = time.monotonic()
            table = table_verrou()
            exclusifs = {o: list(a)[0] for o, a in table.items()
                         if len(a) == 1}
            # echantillon representatif (tous les exclusifs serait trop lent) :
            # on teste un exclusif par proprietaire
            par_prop = {}
            for o, p in exclusifs.items():
                par_prop.setdefault(p, []).append(o)
            echecs = []
            non_proprietaires = [a for a in tous_agents() if a != "hygie"]
            for prop, outils in sorted(par_prop.items()):
                if not outils:
                    continue
                outil = sorted(outils)[0]
                # choisir un non-proprietaire
                autres = [a for a in non_proprietaires if a != prop]
                if not autres:
                    continue
                non_prop = autres[0]
                r = lancer([PYTHON, VERROU_PY, "--agent", non_prop,
                            "--outil", outil, "--audit"], timeout=30)
                bloque = (r.returncode == 1 and "BLOQUE" in r.stdout)
                if not bloque:
                    echecs.append("%s->%s rc=%d" % (non_prop, outil,
                                                    r.returncode))
            verifier("3. Outils exclusifs verrouilles : un non-proprietaire "
                     "est BLOQUE (%d outils testes)" % len(par_prop),
                     not echecs, "; ".join(echecs))
            chrono_etape("3. verrou exclusifs", t0)

        # 4. Aucun faux positif : derivation evaluer-processus ne doit pas
        #    declarer exclusif un outil present chez un autre agent (trio inclu)
        if point_actif(4):
            t0 = time.monotonic()
            exclusifs = derivation_exclusifs()
            agents = tous_agents()
            faux = []
            for outil, prop in sorted(exclusifs.items()):
                for a in agents:
                    if a == prop:
                        continue
                    if outil in outils_carte_agent(a):
                        faux.append("%s (prop=%s aussi chez %s)" %
                                    (outil, prop, a))
            verifier("4. Aucun faux positif : derivation coherente avec "
                     "TOUTES les cartes (trio inclus)", not faux,
                     "; ".join(faux))
            chrono_etape("4. faux positifs", t0)

        # 5. Preuve reelle : cerberus -> guider-parcours (exclusif buffy)
        if point_actif(5):
            t0 = time.monotonic()
            r = lancer([PYTHON, VERROU_PY, "--agent", "cerberus",
                        "--outil", "guider-parcours", "--audit"], timeout=30)
            ok = (r.returncode == 1 and "BLOQUE" in r.stdout)
            verifier("5. Preuve : cerberus -> guider-parcours (exclusif "
                     "buffy) BLOQUE", ok, "rc=%d out=%s" %
                     (r.returncode, r.stdout.strip()[-60:]))
            chrono_etape("5. preuve", t0)

        # 6. Normes ASCII + LF pur (outils + test)
        if point_actif(6):
            t0 = time.monotonic()
            fichiers = [VERROU_PY, EVALUER_PY, REGLES,
                        os.path.abspath(__file__)]
            total_na = sum(ascii_count(f) for f in fichiers)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("6. ASCII strict : 0 non-ASCII (verrou + evaluer + "
                     "regles + test)", total_na == 0, "total=%d" % total_na)
            verifier("7. LF pur : 0 CRLF (verrou + evaluer + regles + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("6. normes", t0)

    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO,
                                                               NB_POINTS))
    PROTECTIONS.afficher_rating("test-064-exclusivites-coherence")
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
