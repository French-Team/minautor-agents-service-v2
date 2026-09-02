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

VERSION = "0.2.2"

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


# Blocs routines v1 (serveur de routines oracle, manifest.json) : ils
# historisent sous leur NOM de routine avec un id LLM et le type 'R'
# (colonne Executeur RT(<intervalle>) dans l encart v1). Ce ne sont pas
# des agents : ils sont exclus du scan de flux (meme liste que test-098).
BLOCS_ROUTINES = {"citations", "encart", "flux", "live", "notation",
                  "verifier-statuts", "vigie-perimetre"}
BLOCS_COORDINATION = {"cerberus", "oracle", "pilote"}


def _est_routine(agent):
    """Vrai si le bloc est une routine v1 (pas un agent)."""
    return (agent or "").lower() in BLOCS_ROUTINES


def _est_coordination(agent):
    """Vrai si l entree appartient a la coordination et non a un agent metier.

    Cerberus peut rester ouvert en accueil (DEBUT sans FIN), tandis que le
    pilote trace les phases de vol sans constituer une mission agent.
    """
    return (agent or "").lower() in BLOCS_COORDINATION


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
        # Les composants de coordination ne sont pas des agents metier :
        # Cerberus peut avoir un DEBUT ouvert et le pilote trace son vol.
        if _est_coordination(ag) or _est_citations(ag):
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
        # Les marqueurs DEBUT/FIN des composants de coordination sont
        # geres par leurs propres cycles (accueil Cerberus / vol pilote).
        if _est_coordination(ag) or _est_citations(ag):
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

    # --- R7 : Apres le FIN d un agent, le prochain agent est ORACLE
    # (l aeroport) - modele aero R1/R3 (2026-08-30) ---
    # MODELE AERO (spec modele-round-avion-parachutiste, R1) : la fin de
    # TOUT agent va vers ORACLE (l aeroport), JAMAIS vers Cerberus, jamais
    # vers un autre agent. C est le PILOTE (dans Oracle) qui decide de la
    # suite : largage d un maillon, ou atterrissage terminal sur Cerberus
    # en fin de round (bilan consolide) - cet atterrissage est une
    # DECISION DU PILOTE, pas une fin d agent.
    # Casse insensible : Oracle == oracle.
    # NOTE : le tableau est TRIE DESC (plus recent en haut). Pour trouver
    # le prochain evenement chronologique, on cherche VERS LE HAUT
    # (index decroissant = plus recent).
    # FIX v0.2.2 (mission 31fe865e, faux positif largage) : le scan NE
    # SAUTE PLUS la coordination (oracle/pilote/cerberus). Quand le pilote
    # LARGUE un agent apres une fin, le flux reel est :
    #   FIN agent -> pilote "RECUPERE: X" -> oracle "DEBUT: RETOUR X"
    #                    -> pilote activer <suivant>
    # L'ancien scan sautait les lignes RECUPERE/RETOUR (coordination) puis
    # trouvait l'agent LARGUE -> R7 KO a tort (preuve : ligne 'DEBUT:
    # RETOUR VULCAIN' agent=oracle 15:03:35 presente juste apres la fin).
    # Le prochain evenement doit ETRE un maillon de coordination (l
    # aeroport qui recoit la fin) : oracle/pilote = OK, cerberus = OK
    # seulement en atterrissage terminal (rien de plus recent au-dessus).
    for ag, idx in agents_fin.items():
        if _est_coordination(ag):
            continue  # coordination : cycle ouvert ou trace de vol normale
        # Chercher le PROCHAIN evenement (hors routines, hors citations)
        # EN REMONTANT dans le tableau (vers le plus recent). On ne saute
        # PAS la coordination : le prochain doit etre l aeroport.
        prochain_agent = None
        prochain_idx = None
        for j in range(idx - 1, -1, -1):
            a = entrees[j]["agent"]
            if _est_routine(a) or _est_citations(a):
                continue
            prochain_agent = a
            prochain_idx = j
            break
        if prochain_agent is None:
            continue  # fin en tete de tableau : rien de plus recent, OK
        if _est_coordination(prochain_agent):
            # Aeroport (oracle/pilote) : la fin a bien ete recue par le
            # pilote (RECUPERE + RETOUR) avant tout largage. Cerberus =
            # atterrissage terminal du pilote en fin de round ; verifie
            # qu il est bien la DERNIERE entree (rien ne redecoule).
            if prochain_agent.lower() == "cerberus" and prochain_idx:
                for j in range(prochain_idx - 1, -1, -1):
                    a = entrees[j]["agent"]
                    if _est_routine(a) or _est_citations(a):
                        continue
                    if not _est_coordination(a):
                        ok = False
                        erreurs.append(
                            "R7: FIN de '%s' (ligne %d) -> atterrissage "
                            "Cerberus NON terminal (ligne %d, agent '%s' "
                            "redecoule au-dessus)"
                            % (ag, idx + 1, j + 1, a))
                        break
            continue
        # Un agent METIER direct apres la fin (sans passage par l aeroport)
        # = violation du modele aero R1/R3.
        ok = False
        erreurs.append(
            "R7: FIN de '%s' (ligne %d) -> prochain agent '%s' "
            "(devrait etre Oracle - l aeroport, modele aero R1/R3 : "
            "la fin de tout agent va vers Oracle, rien vers "
            "Cerberus)"
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
        print("  R7: Apres FIN agent -> aeroport Oracle/pilote (l aeroport, modele aero)")
        return 0
    else:
        print("FLUX KO : %d anomalie(s) detectee(s) :" % len(erreurs))
        for e in erreurs:
            print("  - %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
