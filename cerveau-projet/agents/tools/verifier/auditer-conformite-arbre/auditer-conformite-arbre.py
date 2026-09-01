#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
auditer-conformite-arbre.py
auditer-conformite-arbre

Usage:
  auditer-conformite-arbre.py --agent <nom>
  auditer-conformite-arbre.py --agent <nom> --rapport <fichier.md>
  auditer-conformite-arbre.py --liste
  auditer-conformite-arbre.py --version
  auditer-conformite-arbre.py --aide

Auditeur de conformite de l ARBRE d un agent v1 par rapport aux BESOINS v2
(liste de reference besoins-v2.json, derivee du contrat pilote.py + templates
v2 freelance).

Principe : chaque besoin de besoins-v2.json est une verification exploitable.
L outil charge l arbre d un agent (arbre-<agent>.json dans
cerveau-projet/agents/<agent>/parcours/), les themes et fins qu il reference,
puis execute chaque verification du besoin. Il produit un verdict par besoin
(OK / KO bloquant / KO avertissement / ~ information) + un rapport global.

Le but : identifier les problemes ET incoherences structurelles de l arbre
avant de le corriger - un agent a la fois. L outil ne modifie RIEN (audit seul).

Verdict :
  - OK  : le besoin est satisfait.
  - BLOQUANT : le besoin n est pas satisfait (casse le pilotage ou la chaine).
  - AVERTISSEMENT : le besoin n est pas satisfait (risque, non structurant).
  - INFO : details a verifier (non bloquant).
"""

import argparse
import io
import json
import os
import sys

VERSION = "0.1.0"

RACINE = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(RACINE, "cerveau-projet")):
    RACINE = os.path.dirname(RACINE)

CHEMIN_LISTE = os.path.join(RACINE, "cerveau-projet", "agents", "tools",
                            "verifier", "auditer-conformite-arbre", "besoins-v2.json")


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------

def lire_json(chemin):
    """Lit un JSON en UTF-8, renvoie None si absent ou invalide."""
    if not os.path.isfile(chemin):
        return None
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            return json.load(fh)
    except ValueError:
        return None


def dossier_arbre(agent):
    """Dossier parcours d un agent v1."""
    return os.path.join(RACINE, "cerveau-projet", "agents", agent, "parcours")


def charge_element(dossier, nom_fichier):
    """Charge un element JSON (theme/fins) depuis le dossier parcours."""
    if not nom_fichier:
        return None
    chemin = os.path.join(dossier, nom_fichier)
    return lire_json(chemin)


# ---------------------------------------------------------------------------
# Verifications (une fonction par besoin). Chacune retourne
# (statut, detail) avec statut dans {OK, BLOQUANT, AVERTISSEMENT, INFO}.
# ---------------------------------------------------------------------------

# Couverture de types deduits (besoin C3) : on reprend ici le vocabulaire que
# le pilote cherche (mapping _resoudre_racine + _type_mission_auto). C est une
# liste partielle, representative, que l agent audite peut etendre.
TYPES_DEDUITS = (
    "CONSTRUIRE", "CREER", "COMPLETER", "MODIFIER", "MAJ", "CONTROLE",
    "NON-REGRESSION", "DETECTER", "EXPLORER", "RECHERCHER", "CORRIGER",
    "NETTOYER", "VERIFIER", "PROPOSER", "SIGNALER", "EDUCER", "AUTO-CORRECTION",
    "REVISION", "SYNTHESE", "AUDIT", "VERACITE", "AUTRE", "INTER-ROUND", "LIRE",
    "ACTIVATION", "AGENT", "AMELIORER", "CARTOGRAPHIER", "DOCUMENTER",
    "HONNETETE", "OUTILS", "PROTOCOLE", "PURIFIER", "TESTER", "SAUVEGARDER",
    "RESTAURER", "FICHE-AGENT", "ARBRE-DECISION", "JARVIS", "OUTILS-COMBOS",
    "ROUTINES", "PROTOCOLES", "REGLES", "VEILLE", "ACCUEIL",
)


import re


def _champ_depuis(verification):
    """Extrait le chemin d acces depuis une verification 'champ[:a.b.c] == v'
    ou 'liste[:a.b.c] non vide'. Retourne (path, reste) ; path=None si absent."""
    m = re.search(r"\[:([a-zA-Z0-9_.\[\]/ -]+)\]", verification)
    if not m:
        return None, verification
    return m.group(1).strip(), verification[m.end():].strip()


def _extraire(objet, path_str):
    """Naviguer dans un dict selon 'a.b.c' (les segments ; dans "["x"]"
    sont ignores). Utilise pour les verifications de champ/dict/lire."""
    cur = objet
    for seg in path_str.split("."):
        seg = seg.strip().strip('"').strip("'")
        if seg.startswith("[") and seg.endswith("]"):
            # route vers une cle nom de fichier : a ignorer pour l extraction
            cur = cur.copy() if isinstance(cur, dict) else cur
            continue
        if isinstance(cur, dict) and seg in cur:
            cur = cur[seg]
        else:
            return None
    return cur


def verif_champ(fichier, chemin_champ, attendu, agent):
    """Verification 'champ[:a.b.c] == attendu'. Le placeholder 'agent' compare
    au nom de l agent audite."""
    path_str, reste = _champ_depuis(chemin_champ)
    if path_str is None:
        return "BLOQUANT", "champ illisible: %s" % chemin_champ
    if "==" in reste:
        attendu = reste.split("==", 1)[1].strip().strip("'").strip('"')
    valeur = _extraire(fichier, path_str)
    if valeur is None:
        return "BLOQUANT", "champ introuvable: %s" % chemin_champ
    attendu_resolu = agent if attendu in ("agent", "<agent>") else attendu
    if str(valeur).strip() == str(attendu_resolu).strip():
        return "OK", "valeur '%s' conforme" % valeur
    return "BLOQUANT", "valeur '%s' != attendu '%s'" % (valeur, attendu_resolu)


def verif_liste_non_vide(fichier, chemin, agent):
    """Verification 'liste[:a.b.c] non vide'."""
    path_str, reste = _champ_depuis(chemin)
    if path_str is None:
        return "BLOQUANT", "chemin illisible: %s" % chemin
    cur = _extraire(fichier, path_str)
    if cur is None:
        return "BLOQUANT", "liste introuvable: %s" % chemin
    if isinstance(cur, (list, dict)) and len(cur) > 0:
        return "OK", "%d element(s)" % len(cur)
    return "BLOQUANT", "liste/dict vide"


def auditer_arbre(agent):
    """Audite l arbre de l agent contre chaque besoin de besoins-v2.json."""
    dossier = dossier_arbre(agent)
    if not os.path.isdir(dossier):
        return [(None, "BLOQUANT",
                 "dossier parcours introuvable: %s" % dossier)]

    arbre = lire_json(os.path.join(dossier, "arbre-%s.json" % agent))
    if arbre is None:
        return [(None, "BLOQUANT",
                 "arbre-arbre-%s.json introuvable ou JSON invalide" % agent)]

    liste = lire_json(CHEMIN_LISTE)
    if liste is None:
        return [(None, "BLOQUANT",
                 "besoins-v2.json introuvable ou invalide: %s" % CHEMIN_LISTE)]

    # Precharger les themes et fins references par la racine
    racine = arbre.get("racine", {})
    branches = racine.get("branches", [])
    fins_fichier = arbre.get("fins", {}).get("fichier", "fins.json")
    fins = charge_element(dossier, fins_fichier)
    themes = {}
    for br in branches:
        vers = br.get("vers", "")
        themes[vers] = charge_element(dossier, vers)

    resultats = []
    for besoin in liste.get("besoins", []):
        bid = besoin.get("id")
        verification = besoin.get("verification", "")
        categorie = besoin.get("categorie", "")
        cible = besoin.get("cible", "")

        if bid == "C1":
            statut, detail = _c1(branches, themes, dossier)
        elif bid == "C3":
            statut, detail = _c3(branches)
        elif bid == "A6":
            statut, detail = _a6(arbre, dossier)
        elif bid == "F1":
            if fins is None:
                statut, detail = "BLOQUANT", "fins.json introuvable"
            elif isinstance(fins.get("fins"), dict) and len(fins.get("fins")) > 0:
                statut, detail = "OK", "%d fin(s)" % len(fins.get("fins"))
            else:
                statut, detail = "BLOQUANT", "fins.fins vide ou absent"
        elif bid == "T1":
            statut, detail = _t1(themes)
        elif bid == "T2":
            statut, detail = _t2(themes)
        elif bid == "T3":
            statut, detail = _t3(themes)
        elif bid == "T5":
            statut, detail = _t5(themes, fins)
        elif bid == "T6":
            statut, detail = _t6(themes)
        elif bid == "F2":
            statut, detail = _f2(themes, fins)
        elif bid == "F3":
            statut, detail = _f3(fins)
        elif bid == "F4":
            statut, detail = _f4(fins)
        elif bid == "F5":
            statut, detail = _f5(fins)
        elif bid == "C4":
            statut, detail = _c4(themes)
        elif bid == "C2":
            statut, detail = _c2(themes, fins)
        elif bid == "T4":
            statut, detail = _t4(themes)
        else:
            # Besoins ge neAir et liste / champ
            if verification.startswith("champ["):
                statut, detail = verif_champ(arbre, verification, None, agent)
            elif verification.startswith("liste[") and "non vide" in verification:
                statut, detail = verif_liste_non_vide(arbre, verification, agent)
            elif verification.startswith("chaque branche"):
                statut, detail = _a5(branches)
            elif verification.startswith("chaque vers"):
                statut, detail = _c1(branches, themes, dossier)
            elif verification.startswith("fin.type"):
                statut, detail = _t5(themes, fins)
            else:
                statut, detail = "INFO", "verification non implementee: %s" % verification

        # Le seuil du verdict depend du niveau du besoin
        if bid == "C3":
            niveau_reel = "BLOQUANT" if statut in ("BLOQUANT", "AVERTISSEMENT", "INFO") else "OK"
        elif bid in ("T4",):
            # T4 est information : on remonte en averissement si pas OK
            statut = statut if statut == "OK" else "AVERTISSEMENT"
        else:
            niveau_reel = statut

        resultats.append((bid, statut, detail, besoin))

    return resultats


# --- checks cibles (fonctions dediees) ---

def _a6(arbre, dossier):
    """checer le: fins.fichier pointe un fichier existant dans le dossier."""
    fins_fichier = arbre.get("fins", {}).get("fichier", "fins.json")
    if not fins_fichier:
        return "BLOQUANT", "fins.fichier vide"
    chemin = os.path.join(dossier, fins_fichier)
    if os.path.isfile(chemin):
        return "OK", "fichier fins present: %s" % fins_fichier
    return "BLOQUANT", "fins.fichier '%s' introuvable dans '%s'" % (fins_fichier, dossier)


def _a5(branches):
    ko = []
    for br in branches:
        if not br.get("reponse"):
            ko.append("branche sans 'reponse'")
        if not br.get("vers"):
            ko.append("branche '%s' sans 'vers'" % br.get("reponse"))
    if ko:
        return "BLOQUANT", "; ".join(ko)
    return "OK", "%d branches avec reponse+vers" % len(branches)


def _c1(branches, themes, dossier):
    KO = []
    for br in branches:
        vers = br.get("vers", "")
        if not vers:
            continue
        if vers not in themes:
            KO.append("theme pointe introuvable: %s" % vers)
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "tous les themes pointees existent"


def _c3(branches):
    """Couverture des types deduits par le pilote (besoin C3)."""
    reponses = [str(br.get("reponse", "")).upper() for br in branches]
    descriptions = " ".join(str(br.get("description", "")) for br in branches)
    manquants = []
    for typ in TYPES_DEDUITS:
        if typ in reponses:
            continue
        if typ.lower() in descriptions.lower():
            continue
        manquants.append(typ)
    # Ne signaler que les types pertinents pour un "agent d action" generique :
    # on garde l ensemble, mais en avertissement si beaucoup de types absents
    # (une racine ne couvre pas TOUT le vocabulaire ; les gestions speciales
    # INTER-ROUND etc. sont dans les fins/themes).
    if not manquants:
        return "OK", "couverture complete"
    # Types qui, pour un agent simple, devraient etre geres explicitement.
    # LIRE est exclu : la lecture (fiche, lecons, activite) se fait souvent a
    # l interieur des themes (ex: DETECTER d argus), une branche LIRE dediee
    # n est pas indispensable si la lecture est couverte par les themes.
    essentiels = [t for t in ("INTER-ROUND", "AUTRE") if t in manquants]
    if essentiels:
        return "AVERTISSEMENT", "types essentiels non couverts: %s" % ", ".join(essentiels)
    return "INFO", "types deduits absents (a evaluer selon le role): %s" % ", ".join(manquants[:12])


def _t1(themes):
    KO = []
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        if not red:
            KO.append("%s: sans redirects" % vers)
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "tous les themes ont des redirects"


def _t2(themes):
    KO = []
    total = 0
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        for r in red or []:
            total += 1
            if not r.get("besoin"):
                KO.append("%s: redirect sans besoin" % vers)
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "%d redirects tous avec besoin" % total


def _t3(themes):
    KO = []
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        for r in red or []:
            if r.get("action") == "procedure":
                etapes = r.get("etapes")
                if not isinstance(etapes, list) or len(etapes) == 0:
                    KO.append("%s: redirect procedure sans etapes (%s)"
                              % (vers, r.get("besoin", "?")))
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "toutes les procedures ont des etapes"


def _t4(themes):
    KO = []
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        for r in red or []:
            if r.get("action") == "redirection" and not r.get("vers"):
                KO.append("%s: redirection sans vers" % vers)
    if KO:
        return "AVERTISSEMENT", "; ".join(KO)
    return "OK", "redirections documentees"


def _t5(themes, fins):
    KO = []
    for vers, th in themes.items():
        if th is None:
            continue
        fin = th.get("fin")
        if not fin or fin.get("type") != "lien" or not fin.get("vers"):
            KO.append("%s: fin sans lien vers fins" % vers)
            continue
        case = fin.get("case")
        if fin.get("vers") != fins_fichier_attendu(fin) and case not in (fins or {}).get("fins", {}):
            pass
        if not case or case not in (fins or {}).get("fins", {}):
            KO.append("%s: fin.case '%s' absente de fins.json" % (vers, case))
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "toutes les fins pointent une case existante"


def _t6(themes):
    KO = []
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        for r in red or []:
            etapes = r.get("etapes") or []
            if not etapes:
                if r.get("action") not in ("redirection", "activer", "reactiver"):
                    KO.append("%s: redirect sans aucune etape (%s)"
                              % (vers, r.get("besoin", "?")))
    if KO:
        return "AVERTISSEMENT", "; ".join(KO)
    return "OK", "aucun redirect vide"


def _f2(themes, fins):
    cases_fins = set((fins or {}).get("fins", {}).keys())
    KO = []
    for vers, th in themes.items():
        if th is None:
            continue
        fin = th.get("fin") or {}
        case = fin.get("case")
        if case and case not in cases_fins:
            KO.append("%s -> case '%s' absente" % (vers, case))
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "toutes les cases fins referencees existent"


def _f3(fins):
    KO = []
    for case, f in (fins or {}).get("fins", {}).items():
        if f.get("action") in ("reactiver", "activer"):
            cible = f.get("cible", "")
            if not cible:
                KO.append("%s: fin %s sans cible" % (case, f.get("action")))
            elif cible.startswith("<"):
                KO.append("%s: cible placeholder non resolue '%s'" % (case, cible))
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "aucune cible placeholder"


def _f4(fins):
    """Modele aero R1 : aucune fin ne cible cerberus."""
    KO = []
    for case, f in (fins or {}).get("fins", {}).items():
        if f.get("action") in ("reactiver", "activer"):
            cible = (f.get("cible", "") or "").lower()
            if cible == "cerberus":
                KO.append("%s: cible cerberus (vestige v1, doit aller vers oracle)" % case)
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "aucune fin vers cerberus (modele aero R1)"


def _f5(fins):
    """Modele aero R3 : aucune fin n active un autre agent (le pilote decide)."""
    AGENTS = (
        "argus", "athena", "atlas", "buffy", "cerberus", "chiron", "clio",
        "ferrari", "gardien", "hades", "hermes", "hygie", "janus",
        "morpheus", "oracle", "promethee", "redacteur-v2", "socrate",
        "themis", "vulcain",
    )
    KO = []
    for case, f in (fins or {}).get("fins", {}).items():
        if f.get("action") == "activer":
            cible = (f.get("cible", "") or "").lower().strip()
            if cible and not cible.startswith("<") and cible in AGENTS:
                KO.append("%s: active '%s' (vestige v1, le pilote decide du suivant)"
                          % (case, cible))
    if KO:
        return "BLOQUANT", "; ".join(KO)
    return "OK", "aucune fin n active un autre agent (modele aero R3)"


def _c4(themes):
    """Modele aero R4 : separation montant/descendant - pas de melange
    procedure + activation dans le meme redirect d un theme."""
    AV = []
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        for r in red or []:
            action = r.get("action", "procedure")
            if action == "procedure":
                texte = " ".join(r.get("etapes", []))
                if ("activer-agent-principal" in texte
                        or " reactiver " in texte
                        or " oracle.py reactiver-fin" in texte):
                    AV.append("%s: redirect procedure contient une activation "
                              "(flux descendant) dans un theme de travail" % vers)
    if AV:
        return "AVERTISSEMENT", "; ".join(AV)
    return "OK", "aucun melange montant/descendant (modele aero R4)"


def _c2(themes, fins):
    """Case morte : une fin declaree jamais referencee par un theme.
    On tolere 'fin-theme' : fin conventionnelle de retour a la racine."""
    cases_fins = set((fins or {}).get("fins", {}).keys())
    referencees = set()
    for vers, th in themes.items():
        if th is None:
            continue
        c = th.get("fin", {}).get("case")
        if c:
            referencees.add(c)
    mortes = cases_fins - referencees - {"fin-theme"}
    if mortes:
        return "AVERTISSEMENT", "fins mortes (jamais referencees): %s" % ", ".join(sorted(mortes))
    return "OK", "aucune fin morte (fin-theme conventionnelle ignorer)"


def fins_fichier_attendu(fin):
    """Resout le nom de fichier fins depuis fin.vers (nom du fichier)."""
    vers = fin.get("vers", "")
    return os.path.basename(vers)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Auditer la conformite de l arbre d un agent v1 aux besoins v2")
    parser.add_argument("--agent", metavar="NOM",
                        help="Auditer l arbre d UN agent (ex: argus)")
    parser.add_argument("--liste", action="store_true",
                        help="Afficher la liste des besoins v2")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="Ecrire le rapport dans ce fichier")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias -h)")
    args = parser.parse_args()

    if args.version:
        print("auditer-conformite-arbre v%s" % VERSION)
        return 0

    if args.liste:
        liste = lire_json(CHEMIN_LISTE)
        print("=== Besoins v2 (%s) ===" % CHEMIN_LISTE)
        for b in (liste or {}).get("besoins", []):
            print("[%s/%s/%s] %s" % (b["id"], b["categorie"], b["niveau"], b["titre"]))
            print("    %s" % b["detail"])
        return 0

    if not args.agent:
        print("[ERREUR] Choisir --agent <nom> ou --liste")
        return 1

    print("=== auditer-conformite-arbre v%s ===" % VERSION)
    print("Agent : %s" % args.agent)
    print("")

    resultats = auditer_arbre(args.agent)
    # Reporter en tete la premiere erreur bloquante (dossier/arbre/liste)
    lignes_rapport = [
        "# Audit conformite de l arbre - %s" % args.agent,
        "",
        "Outil    : auditer-conformite-arbre v%s" % VERSION,
        "Reference: besoins-v2.json",
        "",
        "| Besoin | Categorie | Verdict | Detail |",
        "|---|---|---|---|",
    ]
    nb_ok = 0
    nb_bloquant = 0
    nb_avert = 0
    nb_info = 0
    for bid, statut, detail, besoin in resultats:
        categorie = besoin.get("categorie", "?") if besoin else "?"
        titre = besoin.get("titre", "?") if besoin else "?"
        ligne = "[%s] %s : %s -- %s" % (categorie, bid, statut, detail)
        print("  " + ligne)
        lignes_rapport.append("| %s | %s | %s | %s |"
                              % (bid, categorie, statut, detail))
        if statut == "OK":
            nb_ok += 1
        elif statut in ("BLOQUANT", "KO"):
            nb_bloquant += 1
        elif statut == "AVERTISSEMENT":
            nb_avert += 1
        else:
            nb_info += 1

    print("")
    print("=== RESULTAT : %d OK / %d bloquant / %d avertissement / %d info ==="
          % (nb_ok, nb_bloquant, nb_avert, nb_info))

    if args.rapport:
        contenu = "\n".join(lignes_rapport) + "\n"
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(contenu)
        print("[RAPPORT] ecrit dans %s" % args.rapport)

    return 1 if nb_bloquant else 0


if __name__ == "__main__":
    sys.exit(main())