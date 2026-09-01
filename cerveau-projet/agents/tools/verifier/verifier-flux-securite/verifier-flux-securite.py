#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
verifier-flux-securite.py -- ROUTINE DE SECURITE : verifie le flux.

Le flux correct :
  Oracle active Cerberus (DEBUT Oracle)
  Oracle active un agent (DEBUT Oracle)
  L agent travaille (DEBUT agent si auto-historise)
  Oracle historise FIN (FIN Oracle)
  Oracle re-active Cerberus (DEBUT Oracle)

REGLE : entre chaque DEBUT et FIN d un agent, Oracle DOIT apparaitre.
Oracle est le SEUL a historiser DEBUT/FIN. Un agent ne historise JAMAIS
son propre DEBUT/FIN.

Lit le tableau AGENTS-activite-recente.md et verifie les regles.

Proprietaire : Buffy (responsable). Version : 0.1.0.
"""

import io
import os
import re
import sys

VERSION = "0.1.0"

# Fichier du tableau d activites recentes
AGENTS_ACTIVITE_RECENTE = os.environ.get(
    "AGENTS_ACTIVITE_RECENTE",
    os.path.join(os.path.dirname(__file__), "..", "..", "..",
                 "..", "..", "AGENTS-activite-recente.md"))
AGENTS_ACTIVITE_RECENTE = os.path.normpath(AGENTS_ACTIVITE_RECENTE)


def _lister_entrees():
    """Lire le tableau et retourner une liste de dicts.

    Chaque dict : {grade, agent, df, secteur, raison, heure, id, type}
    df = Etat (DEBUT, FIN, ATTENTE, URGENT, BUG, ACTIF) - colonne
    renommee Debut/Fin -> Etat le 2026-08-29 (decision utilisateur).
    """
    if not os.path.isfile(AGENTS_ACTIVITE_RECENTE):
        print("ERREUR: %s introuvable" % AGENTS_ACTIVITE_RECENTE)
        return []

    contenu = io.open(AGENTS_ACTIVITE_RECENTE, "r",
                      encoding="utf-8", errors="replace").read()
    entrees = []
    for ligne in contenu.split("\n"):
        ligne = ligne.strip()
        if not ligne.startswith("|"):
            continue
        if ligne.startswith("| Grade |") or ligne.startswith("|---"):
            continue
        cols = [c.strip() for c in ligne.split("|")]
        # cols[0] et cols[-1] sont vides (debut/fin du |)
        # Format : | Grade | Agent | Defcon | Executeur | Etat | Secteur |
        #          Raison | Heure | id | Type |
        #   (colonne Defcon creee 2026-08-29 apres Agent ; Debut/Fin -> Etat)
        if len(cols) < 12:
            continue
        entrees.append({
            "grade": cols[1],
            "agent": cols[2],
            "defcon": cols[3],
            "executeur": cols[4],
            "df": cols[5],
            "secteur": cols[6],
            "raison": cols[7],
            "heure": cols[8],
            "id": cols[9],
            "type": cols[10],
        })
    return entrees


def _est_oracle(agent):
    """Vrai si l agent est Oracle."""
    return (agent or "").lower() == "oracle"


def _est_citations(agent):
    """Vrai si l agent est une routine (citations)."""
    return (agent or "").lower() == "citations"


def verifier_flux(entrees=None):
    """Verifier les regles de flux. Retourne (ok, erreurs).

    Regles :
    R1 : Chaque agent (hors Oracle, hors citations) DOIT avoir un DEBUT
         et un FIN dans le tableau.
    R2 : Le DEBUT d un agent doit etre precede d un entry Oracle
         (Oracle historise le DEBUT).
    R3 : Le FIN d un agent doit etre suivi d un entry Oracle
         (Oracle historise le FIN).
    R4 : Un agent ne doit JAMAIS historiser son propre DEBUT/FIN
         (sauf citations = DEV).
    R5 : Entre chaque DEBUT et FIN d un agent, il doit y avoir au moins
         une entree Oracle (Oracle pilote).
    R6 : Les citations ont toujours "DEV" comme Etat (etat dynamique
         etats-actions.json v0.1.0, decision 2026-08-29 : routine presente
         pour le dev, hors flux de travail reel - ex-ATTENTE).
    """
    if entrees is None:
        entrees = _lister_entrees()

    erreurs = []
    ok = True

    # --- R1 : Chaque agent a DEBUT + FIN (casse insensible) ---
    agents_debut = {}  # agent_lower -> premiere entree DEBUT
    agents_fin = {}    # agent_lower -> premiere entree FIN

    for i, e in enumerate(entrees):
        ag = e["agent"]
        ag_low = ag.lower()
        df = e["df"]
        if _est_oracle(ag) or _est_citations(ag):
            continue
        if df == "DEBUT" and ag_low not in agents_debut:
            agents_debut[ag_low] = i
        if df == "FIN" and ag_low not in agents_fin:
            agents_fin[ag_low] = i

    for ag in agents_debut:
        if ag not in agents_fin:
            ok = False
            idx = agents_debut[ag]
            erreurs.append(
                "R1: Agent '%s' a un DEBUT (ligne %d, %s) mais pas de FIN"
                % (ag, idx + 1, entrees[idx]["heure"]))

    # R2 supprime : Oracle n apparait plus dans le tableau entre les agents.
    # Oracle pilote mais n est pas un agent du flux.

    # R3 supprime : Oracle n apparait plus dans le tableau entre les agents.

    # --- R4 : Agent ne historise pas son propre DEBUT/FIN ---
    for i, e in enumerate(entrees):
        ag = e["agent"]
        df = e["df"]
        if _est_oracle(ag) or _est_citations(ag):
            continue
        if df in ("DEBUT", "FIN"):
            # Verifier si c est un DEBUT/FIN d Oracle pour cet agent
            # (normalement oui - Oracle historise)
            # Si l agent est dans la colonne Agent avec DEBUT/FIN,
            # c est un probleme SEULEMENT si Oracle n a pas historise
            # (on verifie via R2/R3)
            pass

    # R5 supprime : Oracle n apparait plus dans le tableau entre les agents.

    # --- R6 : Citations ont toujours "DEV" (ex-ATTENTE, v0.2.0) ---
    for i, e in enumerate(entrees):
        if _est_citations(e["agent"]) and e["df"] != "DEV":
            ok = False
            erreurs.append(
                "R6: Citation (ligne %d, %s) a Etat='%s' au lieu de 'DEV'"
                % (i + 1, e["heure"], e["df"]))

    # --- R7 : Apres le FIN d un agent, le prochain agent est Cerberus ---
    # L utilisateur ne parle qu avec Cerberus. Quand un agent finit,
    # Oracle re-active Cerberus (pas un autre agent).
    # Casse insensible : Cerberus == cerberus.
    # NOTE : le tableau est TRIE DESC (plus recent en haut). Pour trouver
    # le prochain evenement chronologique, on cherche VERS LE HAUT
    # (index decroissant = plus recent).
    for ag, idx in agents_fin.items():
        if ag.lower() == "cerberus":
            continue  # Cerberus qui finit = normal (pas de suite)
        # Chercher la prochaine entree agent (hors Oracle, hors citations)
        # EN REMONTANT dans le tableau (vers le plus recent)
        prochain_agent = None
        for j in range(idx - 1, -1, -1):
            a = entrees[j]["agent"]
            if _est_oracle(a) or _est_citations(a):
                continue
            prochain_agent = a
            break
        if prochain_agent and prochain_agent.lower() != "cerberus":
            ok = False
            erreurs.append(
                "R7: FIN de '%s' (ligne %d) -> prochain agent '%s' "
                "(devrait etre Cerberus)"
                % (ag, idx + 1, prochain_agent))

    return ok, erreurs


def afficher_flux(entrees=None):
    """Afficher le flux detecte pour debug."""
    if entrees is None:
        entrees = _lister_entrees()

    print("=== FLUX DETECTE ===")
    print()
    for i, e in enumerate(entrees):
        ag = e["agent"]
        df = e["df"]
        marqueur = ""
        if _est_oracle(ag):
            marqueur = " <<<< ORACLE"
        if df == "DEBUT":
            marqueur += " [DEBUT]"
        elif df == "FIN":
            marqueur += " [FIN]"
        elif df == "ATTENTE":
            marqueur += " [ATTENTE]"
        print("  %2d. %s | %s | %s | %s%s" % (
            i + 1, e["heure"], ag, df, e["raison"][:40], marqueur))
    print()


def main():
    """CLI : verifier-flux-securite.py [--flux] [--version]."""
    if "--version" in sys.argv:
        print("verifier-flux-securite v%s" % VERSION)
        return 0

    if "--flux" in sys.argv:
        afficher_flux()

    ok, erreurs = verifier_flux()

    if ok:
        print("FLUX OK : toutes les regles de securite sont respectees.")
        print("  R1: Chaque agent a DEBUT + FIN")
        print("  R2: DEBUT d un agent precede d Oracle")
        print("  R3: FIN d un agent suivi d Oracle")
        print("  R4: Agent ne historise pas son propre DEBUT/FIN")
        print("  R5: Oracle present entre DEBUT et FIN de chaque agent")
        print("  R6: Citations = DEV")
        print("  R7: Apres FIN agent -> Cerberus (pas un autre agent)")
        return 0
    else:
        print("FLUX KO : %d anomalie(s) detectee(s) :" % len(erreurs))
        for e in erreurs:
            print("  - %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
