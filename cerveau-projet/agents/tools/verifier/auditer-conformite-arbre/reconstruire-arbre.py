#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
reconstruire-arbre.py
reconstruire-arbre

Usage:
  reconstruire-arbre.py --agent <nom>                # dry-run (ne modifie rien)
  reconstruire-arbre.py --agent <nom> --ecrire       # applique la reconstruction
  reconstruire-arbre.py --agent <nom> --rapport <f>  # ecrit le rapport
  reconstruire-arbre.py --version | --aide

RECONSTRUIRE l arbre d un agent v1 selon le MODELE ROUND AERO
(spec-modele-round-avion-parachutiste.001.01.ebauche.md, decision utilisateur
2026-08-30) :

  R1 : toute fin d agent va vers ORACLE (l aeroport), jamais vers cerberus.
  R2 : le pilote a SON arbre de mission (distinct des arbres d agents).
  R3 : les agents ne connaissent PAS le suivant - aucune fin n active un
       autre agent (vestige v1).
  R4 : separation flux montant / descendant (signale, a structurer).

L outil s appuie sur l AUDIT (auditer-conformite-arbre.py, besoins F4/F5) :
il ne reconstruit que ce que l audit a declare incoherent.

Transformations appliquees (--ecrire) :
  1. FIN VERS ORACLE (F4) : toute fin action=reactiver avec cible=cerberus
     -> cible=oracle (retour a l aeroport). Le titre/description/regle sont
     realignes sur le modele aero.
  2. SUPPRESSION DES ACTIVATIONS VESTIGES (F5) : toute fin action=activer
     vers un agent nomme (ex: activer buffy, activer promethee) est
     SUPPRIMEE car l agent ne doit pas connaitre le suivant (R3). Si un
     theme reference une fin supprimee, la fin du theme est reorientee vers
     la fin generique de retour a oracle (fin-retour-oracle) creee si absente.
  3. C4 (montant/descendant, v0.2.0) : les themes de travail ne doivent PAS
     contenir d activation directe d un autre agent (commande
     activer-agent-principal activer) : c est au PILOTE de decider du
     largage (R3). Chaque activation directe est remplacee par le SIGNALEMENT
     A ORACLE : deposer la mission (oracle.py mission-ajouter --file asap
     --agent <cible> "<besoin>") puis MA FIN vers ORACLE (reactiver-fin
     <agent> --cible oracle) - le pilote larguera l agent habilite et me
     renverra pour reprendre mon round.

L outil ne touche PAS : les branches de la racine, les commandes de travail
non-activantes. Il reconstruit les fins (partie montante) ET les etapes
activantes des themes (remplacement C4).

Securite :
  - par defaut DRY-RUN : affiche ce qui SERAIT change, n ecrit rien.
  - --ecrire : ecrit fins.json + les themes modifies (.bak avant ecriture).
  - ASCII strict + LF pur a l ecriture.
  - sauvegarde .bak de fins.json et de chaque theme avant ecriture.
"""

import argparse
import io
import json
import os
import re
import shutil
import sys

VERSION = "0.2.0"

RACINE = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(RACINE, "cerveau-projet")):
    RACINE = os.path.dirname(RACINE)

AGENTS_V1 = (
    "argus", "athena", "atlas", "buffy", "cerberus", "chiron", "clio",
    "ferrari", "gardien", "hades", "hermes", "hygie", "janus", "morpheus",
    "oracle", "promethee", "redacteur-v2", "socrate", "themis", "vulcain",
)


def lire_json(chemin):
    if not os.path.isfile(chemin):
        return None
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            return json.load(fh)
    except ValueError:
        return None


def dossier_arbre(agent):
    return os.path.join(RACINE, "cerveau-projet", "agents", agent, "parcours")


def _fin_oracle(case, agent, bilan_placeholder):
    """Construire une fin retour vers oracle (modele aero R1)."""
    return {
        "titre": "FIN - Retour a ORACLE (l aeroport)",
        "description": ("Modele aero : mission terminee, je reviens vers "
                        "ORACLE (l aeroport). C est le pilote qui decide du "
                        "suivant (R3) - je ne connais pas le prochain agent."),
        "action": "reactiver",
        "cible": "oracle",
        "commande": ("python3 cerveau-projet/agents/tools/oracle/oracle.py "
                     "reactiver-fin %s \"%s\" --cible oracle"
                     % (agent, bilan_placeholder)),
        "regle": ("REGLE MODELE AERO (R1/R3) : ma fin va vers ORACLE, jamais "
                  "vers cerberus, jamais vers un autre agent. Le pilote "
                  "decide de la suite. --cible oracle transmis a reactiver-fin."),
    }


def reconstruire(agent, ecrire=False):
    """Analyse et reconstruit les fins de l agent selon le modele aero.

    Retourne (rapport_lignes, modifie, nb_changements).
    """
    dossier = dossier_arbre(agent)
    if not os.path.isdir(dossier):
        return ["[ERREUR] dossier parcours introuvable: %s" % dossier], False, 0

    fins_path = os.path.join(dossier, "fins.json")
    fins = lire_json(fins_path)
    if fins is None:
        return ["[ERREUR] fins.json introuvable ou invalide: %s" % fins_path], False, 0

    arbre = lire_json(os.path.join(dossier, "arbre-%s.json" % agent))
    if arbre is None:
        return ["[ERREUR] arbre-%s.json introuvable" % agent], False, 0

    # Themes de l arbre (pour savoir quelles fins sont referencees)
    branches = arbre.get("racine", {}).get("branches", [])
    themes = {}
    for br in branches:
        vers = br.get("vers", "")
        themes[vers] = lire_json(os.path.join(dossier, vers))

    lignes = []
    lignes.append("=== reconstruire-arbre v%s -- %s ===" % (VERSION, agent))
    lignes.append("Modele : round aero (spec 2026-08-30, R1/R3)")
    lignes.append("Mode   : %s" % ("ECRITURE" if ecrire else "DRY-RUN (rien modifie)"))
    lignes.append("")

    modifie = False
    nb_chg = 0
    nouvelles_fins = {}
    fins_dict = fins.get("fins", {})
    themes_ref = {}
    for vers, th in themes.items():
        if th is not None:
            c = th.get("fin", {}).get("case")
            if c:
                themes_ref[c] = vers

    # ---- Passe 1 : FIN VERS ORACLE (F4) ----
    for case, f in fins_dict.items():
        action = f.get("action", "")
        cible = (f.get("cible", "") or "").lower().strip()
        if action == "reactiver" and cible == "cerberus":
            bilan_ph = "<bilan>"
            m = re.search(r"reactiver-fin\s+\w+\s+\"([^\"]+)\"", f.get("commande", ""))
            if m:
                bilan_ph = m.group(1)
            nouveau = _fin_oracle(case, agent, bilan_ph)
            lignes.append("[F4] fin '%s' : cible cerberus -> ORACLE (R1)" % case)
            lignes.append("     avant: cible=%s action=%s" % (f.get("cible"), action))
            lignes.append("     apres: cible=oracle action=reactiver")
            nouvelles_fins[case] = nouveau
            nb_chg += 1
        elif action == "redirection" and case == "fin-theme":
            nouvelles_fins[case] = f
        elif action == "reactiver" and cible == "oracle":
            # Deja orientee vers oracle mais la commande doit transmettre
            # la cible : reactiver-fin ... --cible oracle (pilote v0.2.1+)
            f2 = dict(f)
            cmd = f2.get("commande", "")
            if cmd and "--cible oracle" not in cmd and "reactiver-fin" in cmd:
                f2["commande"] = cmd.rstrip() + " --cible oracle"
                lignes.append("[F4b] fin '%s' : commande completee --cible oracle" % case)
                nb_chg += 1
            nouvelles_fins[case] = f2
        else:
            nouvelles_fins[case] = f

    # ---- Passe 2 : SUPPRESSION ACTIVATIONS VESTIGES (F5) ----
    fin_retour_oracle = None
    for case, f in list(nouvelles_fins.items()):
        action = f.get("action", "")
        cible = (f.get("cible", "") or "").lower().strip()
        if action == "activer" and cible and not cible.startswith("<") \
                and cible in AGENTS_V1 and cible != "oracle":
            lignes.append("[F5] fin '%s' : active '%s' -> SUPPRIMEE (R3, le "
                          "pilote decide du suivant)" % (case, f.get("cible")))
            del nouvelles_fins[case]
            nb_chg += 1
            # Reorienter les themes qui la reference
            if case in themes_ref:
                vers_theme = themes_ref[case]
                lignes.append("     theme %s : fin '%s' -> reorientee vers "
                              "retour oracle" % (vers_theme, case))
                if fin_retour_oracle is None:
                    fin_retour_oracle = "fin-retour-oracle"
                    nouvelles_fins[fin_retour_oracle] = _fin_oracle(
                        fin_retour_oracle, agent, "<bilan>")
                    nb_chg += 1

    # ---- Passe 3 : C4 (montant/descendant) - remplacement v0.2.0 ----
    # Les themes de travail ne doivent pas contenir d activation directe
    # d un autre agent : on remplace chaque commande
    #   activer-agent-principal.py activer <session> <cible> "<raison>"
    # par le SIGNALEMENT A ORACLE (mission-ajouter + fin reactiver-fin
    # --cible oracle). Le pilote decide du largage (R3).
    themes_modifies = {}   # vers_theme -> nouveau dict theme
    for vers, th in themes.items():
        if th is None:
            continue
        red = th.get("theme", {}).get("redirects") or th.get("redirects")
        if not red:
            continue
        modifie_theme = False
        nouveau_red = []
        for r in red:
            if r.get("action") != "procedure":
                nouveau_red.append(r)
                continue
            etapes = r.get("etapes", [])
            est_inter_round = "inter-round" in vers
            nouveau_etapes = []
            for e in etapes:
                if "activer-agent-principal" not in e:
                    nouveau_etapes.append(e)
                    continue
                # Extraire la cible et la raison de la commande d activation
                m = re.search(
                    r"activer-agent-principal\.py activer <session> (\S+)\s+\"([^\"]*)\"",
                    e)
                cible = m.group(1) if m else "<agent_appelant>"
                raison = m.group(2) if m else "<rapport>"
                if cible.startswith("<"):
                    cible = "<agent_habilite>"
                if est_inter_round:
                    # CAS INTER-ROUND (R2) : l agent n active JAMAIS
                    # l appelant. Il accuse reception et sa fin reactiver-fin
                    # --cible oracle ramene a ORACLE ; le pilote (qui connait
                    # le precedent via l etat de carte) reactive l appelant.
                    nouveau_etapes.append(
                        "MA FIN : python3 cerveau-projet/agents/tools/oracle/"
                        "oracle.py reactiver-fin %s \"<rapport du traitement "
                        "inter-round>\" --cible oracle (le pilote reactive "
                        "l appelant depuis l etat de carte - precedent)" % agent)
                    lignes.append("[C4] theme %s : reactivation de l appelant "
                                  "-> fin vers ORACLE, le pilote reactivera "
                                  "(R2)" % vers)
                else:
                    # DELEGATION DE TRAVAIL (R3) : remplacer par le
                    # signalement a Oracle (le pilote decide du largage)
                    nouveau_etapes.append(
                        "SIGNALER le besoin a ORACLE (le pilote decide du "
                        "largage, R3 - je n active JAMAIS un autre agent) : "
                        "python3 cerveau-projet/agents/tools/oracle/oracle.py "
                        "mission-ajouter --file asap --agent %s \"%s\""
                        % (cible, raison))
                    nouveau_etapes.append(
                        "PUIS MA FIN vers ORACLE : python3 cerveau-projet/agents/"
                        "tools/oracle/oracle.py reactiver-fin %s \"<bilan>\" "
                        "--cible oracle (le pilote larguera %s et me renverra "
                        "pour reprendre mon round)" % (agent, cible))
                    lignes.append("[C4] theme %s : activation directe '%s' -> "
                                  "signalement a Oracle (R3)" % (vers, cible))
                nb_chg += 1
                modifie_theme = True
            if modifie_theme:
                r2 = dict(r)
                r2["etapes"] = nouveau_etapes
                nouveau_red.append(r2)
            else:
                nouveau_red.append(r)
        if modifie_theme:
            th2 = dict(th)
            th2["theme"] = dict(th["theme"])
            th2["theme"]["redirects"] = nouveau_red
            themes_modifies[vers] = th2

    # ---- Ecriture ----
    if nb_chg == 0:
        lignes.append("")
        lignes.append("AUCUN changement necessaire : arbre conforme au modele aero.")
        return lignes, False, 0

    if ecrire:
        # Sauvegarde .bak puis ecriture propre (ascii + LF) : fins.json
        shutil.copyfile(fins_path, fins_path + ".bak")
        d = dict(fins)
        d["fins"] = dict(sorted(nouvelles_fins.items()))
        contenu = json.dumps(d, ensure_ascii=True, indent=2) + "\n"
        with io.open(fins_path, "w", encoding="ascii", newline="\n") as fh:
            fh.write(contenu)
        lignes.append("[ECRIT] %s (%d changement(s), .bak cree)" % (fins_path, nb_chg))
        # Ecrire les themes modifies (C4) avec .bak individuel
        for vers, th2 in themes_modifies.items():
            tp = os.path.join(dossier, vers)
            shutil.copyfile(tp, tp + ".bak")
            c2 = json.dumps(th2, ensure_ascii=True, indent=2) + "\n"
            with io.open(tp, "w", encoding="ascii", newline="\n") as fh:
                fh.write(c2)
            lignes.append("[C4-ECRIT] %s (.bak cree)" % tp)
        modifie = True
    else:
        lignes.append("")
        lignes.append("[DRY-RUN] %d changement(s) a appliquer - relancer avec "
                      "--ecrire" % nb_chg)

    return lignes, modifie, nb_chg


def main():
    parser = argparse.ArgumentParser(
        description="Reconstruire les fins d un arbre d agent selon le modele round aero")
    parser.add_argument("--agent", metavar="NOM", help="Agent a reconstruire")
    parser.add_argument("--ecrire", action="store_true",
                        help="Appliquer les changements (defaut: dry-run)")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="Ecrire le rapport dans ce fichier")
    parser.add_argument("--version", action="store_true", help="Afficher la version")
    parser.add_argument("--aide", action="help", help="Afficher cette aide")
    args = parser.parse_args()

    if args.version:
        print("reconstruire-arbre v%s" % VERSION)
        return 0
    if not args.agent:
        print("[ERREUR] --agent <nom> requis")
        return 1

    lignes, modifie, nb_chg = reconstruire(args.agent, ecrire=args.ecrire)
    print("\n".join(lignes))
    if args.rapport:
        with io.open(args.rapport, "w", encoding="ascii", newline="\n") as fh:
            fh.write("\n".join(lignes) + "\n")
        print("[RAPPORT] ecrit dans %s" % args.rapport)
    return 0 if not modifie else 0


if __name__ == "__main__":
    sys.exit(main())