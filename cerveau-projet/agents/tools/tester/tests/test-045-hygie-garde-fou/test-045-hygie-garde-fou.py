#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-045-hygie-garde-fou.py
GARDE-FOU : l agent Hygie (nettoyage du workspace) reste conforme et son
chariot de nettoyage reste present.

Contexte (mission utilisateur 2026-08-13) :
  - Creation de Hygie, agent de nettoyage de bout en bout : fiche (template
    noyau v0.3.0 + variante cerveau-projet), corrections, parcours v0.1.0,
    dossier snapshots/ (rotation 7 jours).
  - Chariot de nettoyage : detecter-residus (scan par zone),
    snapshot-nettoyage (creer/consulter/rotation/liste),
    combo-nettoyage-hygie (Pattern 3).
  - Anti-recurrence : toute regression (fiche non conforme, parcours casse,
    outil disparu du catalogue) fait KO.

Cas couverts:
  1. La fiche hygie.md est CONFORME (verifier-conformite-fiche)
  2. Le parcours hygie est valide (valider-case : 0 erreur)
  3. Le parcours hygie est CONFORME (valider-cartes-decision)
  4. Le parcours hygie a 0 probleme de cablage (detecter-cablages-manquants)
  5. Le chariot existe sur disque (detecter-residus, snapshot-nettoyage,
     combo-nettoyage-hygie)
  6. Le chariot est au catalogue generateurs-commande
  7. Le chariot est dans index-tools.md
  8. Le dossier snapshots/ existe
  9. ASCII strict : 0 non-ASCII (test + fiche + parcours)
  10. LF pur : 0 CRLF (test + fiche + parcours)
"""
import importlib.util
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

AGENT_DIR_ROOT = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
AGENT_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "hygie")
FICHE = os.path.join(AGENT_DIR, "hygie.md")
PARCOURS = os.path.join(AGENT_DIR, "parcours", "parcours-hygie.json")
SNAPSHOTS = os.path.join(AGENT_DIR, "snapshots")
PROTOCOLE_NETTOYAGE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                  "regles-immuables", "general",
                                  "protocole-nettoyage",
                                  "protocole-nettoyage.001.01.ebauche.md")
INDEX_REGLES = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                            "regles-immuables", "general",
                            "index-regles-general.md")
CATALOGUE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX_TOOLS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                           "index-tools.md")
REGISTRE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.jsonl")

# Tous les agents (glob des parcours) pour la regle de gouvernance
# "seul Hygie supprime" : aucun autre agent ne doit avoir les outils de
# suppression dans SA carte ni les declarer au registre.
AGENTS_GLOBAUX = []
for _nom in sorted(os.listdir(AGENT_DIR_ROOT)):
    if os.path.isdir(os.path.join(AGENT_DIR_ROOT, _nom)):
        AGENTS_GLOBAUX.append(_nom)

OUTILS_SUPPRESSION = ("supprimer-fichier", "supprimer-dossier")

CHARIOT = [
    ("detecter-residus", os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                      "tools", "detecter", "detecter-residus",
                                      "detecter-residus.py")),
    ("snapshot-nettoyage", os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                        "tools", "nettoyer", "snapshot-nettoyage",
                                        "snapshot-nettoyage.py")),
    ("combo-nettoyage-hygie", os.path.join(PROJECT_ROOT, "cerveau-projet",
                                           "agents", "tools", "combos",
                                           "combo-nettoyage-hygie",
                                           "definition-combo.json")),
]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lancer(script, *args):
    """Execution SOUS PROTECTION (timeout + tuer l arbre, erreurs silencieuses)."""
    try:
        r = PROTECTIONS.lancer_protege([sys.executable, script] + list(args),
                                       timeout=120)
        return r.returncode, (r.stdout + r.stderr)
    except Exception as e:
        return -1, str(e)


def main():
    print("=== test-045 : garde-fou Hygie (agent de nettoyage) ===")

    # 1. Fiche conforme
    rc, out = lancer(os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                  "tools", "verifier", "verifier-conformite-fiche",
                                  "verifier-conformite-fiche.py"), "--agent", "hygie")
    verifier("1. Fiche hygie CONFORME (verifier-conformite-fiche)",
             rc == 0 and "CONFORME" in out, "rc=%d" % rc)

    # 2. Parcours valide (valider-case : 0 erreur)
    rc, out = lancer(os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                  "tools", "valider", "valider-case",
                                  "valider-case.py"), PARCOURS)
    verifier("2. Parcours hygie valide (valider-case 0 erreur)",
             rc == 0 and "CONFORME" in out, "rc=%d" % rc)

    # 3. Parcours CONFORME (valider-cartes-decision)
    rc, out = lancer(os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                  "tools", "valider", "valider-cartes-decision",
                                  "valider-cartes-decision.py"), "--agent", "hygie")
    verifier("3. Parcours hygie CONFORME (valider-cartes-decision)",
             rc == 0 and "CONFORME" in out, "rc=%d" % rc)

    # 4. Cablages : 0 probleme
    rc, out = lancer(os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                  "tools", "detecter", "detecter-cablages-manquants",
                                  "detecter-cablages-manquants.py"), PARCOURS)
    verifier("4. Parcours hygie 0 probleme de cablage",
             "PROPRE" in out, "rc=%d" % rc)

    # 5. Chariot sur disque
    chariot_ok = all(os.path.isfile(chemin) for _, chemin in CHARIOT)
    verifier("5. Chariot present sur disque (3 outils)",
             chariot_ok, "; ".join(n for n, _ in CHARIOT))

    # 6. Chariot au catalogue
    noms_cat = []
    if os.path.isfile(CATALOGUE):
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat = json.load(fh)
        noms_cat = [e.get("nom", "") for e in cat.get("commandes", [])]
    verifier("6. Chariot au catalogue generateurs-commande",
             all(n in noms_cat for n, _ in CHARIOT),
             "manquants=%s" % [n for n, _ in CHARIOT if n not in noms_cat])

    # 7. Chariot dans index-tools.md
    if os.path.isfile(INDEX_TOOLS):
        idx = io.open(INDEX_TOOLS, encoding="utf-8").read()
        chariot_idx = all(n in idx for n, _ in CHARIOT)
    else:
        chariot_idx = False
    verifier("7. Chariot dans index-tools.md", chariot_idx)

    # 8. Dossier snapshots existe
    verifier("8. Dossier snapshots/ de Hygie existe", os.path.isdir(SNAPSHOTS))

    # 8b. REGLE DE GOUVERNANCE "SEUL HYGIE SUPPRIME" (cartes) : aucun autre
    # agent n a supprimer-fichier/supprimer-dossier dans SA carte
    derivees_cartes = []
    for agent in AGENTS_GLOBAUX:
        if agent == "hygie":
            continue
        chemin = os.path.join(AGENT_DIR_ROOT, agent, "parcours",
                              "parcours-%s.json" % agent)
        if not os.path.isfile(chemin):
            continue
        try:
            with io.open(chemin, encoding="utf-8") as fh:
                p = json.load(fh)
            contenu = json.dumps(p, ensure_ascii=True)
            if any(o in contenu for o in OUTILS_SUPPRESSION):
                derivees_cartes.append(agent)
        except Exception as e:
            derivees_cartes.append("%s(ERR %s)" % (agent, e))
    verifier("8b. Seul Hygie a supprimer-fichier/supprimer-dossier dans SA carte",
             len(derivees_cartes) == 0, "derivees=%s" % derivees_cartes)

    # 8c. REGLE DE GOUVERNANCE "SEUL HYGIE SUPPRIME" (registre) : aucune
    # declaration de supprimer-* par un agent autre que hygie
    derivees_registre = []
    if os.path.isfile(REGISTRE):
        try:
            with io.open(REGISTRE, encoding="utf-8") as fh:
                for ligne in fh:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    try:
                        entree = json.loads(ligne)
                    except Exception:
                        continue
                    outil = entree.get("outil", "")
                    if not any(o in outil for o in OUTILS_SUPPRESSION):
                        continue
                    agent = entree.get("agent", "?")
                    if agent != "hygie":
                        derivees_registre.append("%s -> %s (%s)" % (
                            agent, outil, entree.get("date", "?")))
        except Exception as e:
            derivees_registre.append("ERR %s" % e)
    verifier("8c. Registre : seul hygie declare supprimer-fichier/supprimer-dossier",
             len(derivees_registre) == 0, "derivees=%s" % derivees_registre)

    # 8d. PROTOCOLE DE NETTOYAGE : la chaine snapshot -> detection ->
    # suppression doit etre documentee dans protocole-nettoyage (cree
    # 2026-08-14, demande utilisateur : detecter-residus exclusif et
    # documente dans le protocole de nettoyage)
    try:
        proto_ok = os.path.isfile(PROTOCOLE_NETTOYAGE)
        if proto_ok:
            contenu = io.open(PROTOCOLE_NETTOYAGE, encoding="utf-8").read()
            proto_ok = ("detecter-residus" in contenu
                        and "snapshot-nettoyage" in contenu
                        and "SEUL HYGIE SUPPRIME" in contenu)
        idx_ok = os.path.isfile(INDEX_REGLES)
        if idx_ok:
            idx = io.open(INDEX_REGLES, encoding="utf-8").read()
            idx_ok = "protocole-nettoyage" in idx
        verifier("8d. protocole-nettoyage : chaine documentee (snapshot + detecter-residus + SEUL HYGIE) + index",
                 proto_ok and idx_ok,
                 "proto=%s idx=%s" % (proto_ok, idx_ok))
    except Exception as e:
        verifier("8d. protocole-nettoyage : chaine documentee + index", False, str(e))

    # 8e. REGLE IMMUABLE : "SEUL HYGIE SUPPRIME" doit etre documentee au
    # niveau regle immuable (regles-groupes-agents.md), pas seulement dans la
    # fiche ou le protocole (demande utilisateur 2026-08-14)
    try:
        chemin_regle = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                    "regles-immuables", "general",
                                    "regles-groupes-agents.md")
        if os.path.isfile(chemin_regle):
            contenu = io.open(chemin_regle, encoding="utf-8").read()
            ok_regle = ("SEUL HYGIE SUPPRIME" in contenu
                        and "supprimer-fichier" in contenu
                        and "test-045-hygie-garde-fou" in contenu)
        else:
            ok_regle = False
        # Lien croise : le protocole-nettoyage doit aussi referencer la regle
        # immuable (triple synchro fiche + protocole + regle, demande
        # utilisateur 2026-08-14)
        if os.path.isfile(PROTOCOLE_NETTOYAGE):
            proto = io.open(PROTOCOLE_NETTOYAGE, encoding="utf-8").read()
            ok_regle = ok_regle and "regles-groupes-agents.md" in proto
        # Lien croise retour : la FICHE hygie doit referencer les 2 autres
        # niveaux (protocole-nettoyage + regles-groupes-agents) - triple
        # synchro COMPLETE et bidirectionnelle (demande utilisateur 2026-08-14)
        if os.path.isfile(FICHE):
            fiche_contenu = io.open(FICHE, encoding="utf-8").read()
            ok_regle = (ok_regle
                        and "regles-groupes-agents" in fiche_contenu
                        and "protocole-nettoyage" in fiche_contenu)
        verifier("8e. triple synchro Hygie : regle immuable documentee + lien croise protocole + fiche",
                 ok_regle)
    except Exception as e:
        verifier("8e. triple synchro Hygie : regle immuable + liens croises", False, str(e))

    # 8f. ANTI-RECURRENCE : TOUTES les regles de gouvernance exclusives du
    # projet sont documentees au niveau regle immuable (regles-groupes-
    # agents.md). Une exclusivite qui vivrait uniquement dans une fiche ou
    # un protocole n est pas opposable a tous les agents.
    try:
        chemin_regle = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                    "regles-immuables", "general",
                                    "regles-groupes-agents.md")
        contenu = io.open(chemin_regle, encoding="utf-8").read()
        exclusivites = [
            ("SEUL HYGIE SUPPRIME", "hygie"),
            ("SEUL JANUS LANCE", "janus"),
            ("SEUL MORPHEUS ECRIT", "morpheus"),
            ("SEUL CLIO MET A JOUR", "clio"),
        ]
        manquantes = [nom for nom, _ in exclusivites if nom not in contenu]
        verifier("8f. toutes les regles exclusives (hygie/janus/morpheus/clio) au niveau regle immuable",
                 len(manquantes) == 0, "manquantes=%s" % manquantes)
    except Exception as e:
        verifier("8f. toutes les regles exclusives au niveau regle immuable", False, str(e))

    # 9-10. Normes
    fichiers_normes = [__file__, FICHE, PARCOURS]
    na_total = sum(ascii_count(f) for f in fichiers_normes)
    crlf_total = sum(crlf_count(f) for f in fichiers_normes)
    verifier("9. ASCII strict : 0 non-ASCII (test + fiche + parcours)",
             na_total == 0, "total=%d" % na_total)
    verifier("10. LF pur : 0 CRLF (test + fiche + parcours)",
             crlf_total == 0, "total=%d" % crlf_total)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
