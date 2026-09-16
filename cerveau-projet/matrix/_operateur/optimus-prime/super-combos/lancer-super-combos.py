#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lancer-super-combos.py -- Lanceur de super-combos par numero

Permet de lancer un super-combos par son numero numerote (sc-001, sc-002,
contrat de nommage CV-008 -- BDD conventions-matrice). Les anciennes formes
"#1" et "1" restent
acceptees et sont normalisees vers sc-001. La casse est libre (SC-001 ou
sc-001) : la forme canonique est en MINUSCULES (le `C-` majuscule est reserve
au champ `constat` fige, regle CV-009).

LE VERBE VIENT DU REGISTRE (correction MO-071, EO-114). Le lanceur n'ecrit plus
"executer" en dur : chaque entree de `registry.json` declare son CONTRAT DE
LANCEMENT, et c'est lui qui est lu.

    "verbe"  : le verbe par DEFAUT de l'objet (peut etre VIDE : un objet sans
               entree unique, comme un cycle a phases, n'en a pas)
    "verbes" : la liste des verbes ACCEPTES (la seule source de verite)

Un objet sans contrat, un contrat incoherent, ou un verbe demande hors contrat
est REFUSE NOMMEMENT (code 2) : jamais un verbe invente, jamais un echec muet.
C'est ce qui empeche un super-combo de naitre inlancable par construction (le
registre est verifie par `creer-combo.py verifier`, qui exige ce contrat).

Usage:
  python lancer-super-combos.py --numero <SC-NNN> [--verbe <verbe>] [--fichier <fichier>] [--mission <id>] [args du super-combo...]
  python lancer-super-combos.py --lister

Les arguments NON reconnus par le lanceur sont transmis TELS QUELS au
super-combo : c'est ainsi qu'on lui donne ses propres options (ex : les phases
de sc-002 exigent une phrase et --type/--gravite/--frequence).
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path


REGISTRY_PATH = Path(__file__).parent / "registry.json"

# Contrat de nommage CV-008 : les super-combos sont numerotes sc-001, sc-002...
# MINUSCULES (regle CV-009) : `C-` majuscule = champ constat fige, jamais un id.
PREFIXE_SUPER_COMBO = "sc-"
LARGEUR_NUMERO = 3

# Contrat de LANCEMENT (MO-071) : les deux champs lus dans le registre.
CLE_CONTRAT_VERBE = "verbe"
CLE_CONTRAT_VERBES = "verbes"

CODE_INCONNU = 1
CODE_REFUS = 2


def charger_registry() -> dict:
    """Charger le registre des super-combos."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"super-combos": []}


def normaliser_numero(numero):
    """Normalise vers sc-<NNN> : accepte sc-001, SC-001, 1 et l'ancien #1."""
    brut = str(numero).strip().lstrip("#").lower()
    if brut.startswith(PREFIXE_SUPER_COMBO):
        return brut
    if brut.isdigit():
        return PREFIXE_SUPER_COMBO + brut.zfill(LARGEUR_NUMERO)
    return brut


def resoudre_lancement(combo, verbe_demande=""):
    """Retourne (code, verbe, message) : le verbe a lancer, ou un refus NOMME.

    Fonction PURE (aucun disque, aucun sous-processus) : elle se prouve sur des
    entrees piegees sans rien lancer. Trois refus, tous NOMMES :
      - l'entree ne declare aucun contrat (champs "verbe"/"verbes") ;
      - le "verbe" par defaut est absent de sa propre liste "verbes" ;
      - le verbe demande n'est pas dans la liste (ou il n'y a pas de defaut).
    """
    identifiant = combo.get("id", "?")
    verbes = [verbe for verbe in (combo.get(CLE_CONTRAT_VERBES) or []) if verbe]
    if not verbes:
        return (
            CODE_REFUS, "",
            "le super-combo " + identifiant + " ne declare AUCUN contrat de lancement "
            "dans registry.json (champs \"" + CLE_CONTRAT_VERBE + "\"/\"" + CLE_CONTRAT_VERBES
            + "\") : le poser par la porte (creer-combo.py verifier le refuse desormais)",
        )
    if verbe_demande:
        if verbe_demande not in verbes:
            return (
                CODE_REFUS, "",
                "verbe \"" + verbe_demande + "\" hors contrat de " + identifiant
                + " -- verbes acceptes : " + ", ".join(verbes),
            )
        return 0, verbe_demande, ""
    defaut = combo.get(CLE_CONTRAT_VERBE, "")
    if not defaut:
        return (
            CODE_REFUS, "",
            "le super-combo " + identifiant + " n'a pas d'entree unique : choisir un verbe "
            "avec --verbe <" + "|".join(verbes) + ">",
        )
    if defaut not in verbes:
        return (
            CODE_REFUS, "",
            "contrat incoherent pour " + identifiant + " : \"" + CLE_CONTRAT_VERBE + "\" = "
            + defaut + " est absent de \"" + CLE_CONTRAT_VERBES + "\" (" + ", ".join(verbes) + ")",
        )
    return 0, defaut, ""


def lister_super_combos():
    """Lister tous les super-combos disponibles (numerotes + contrat de lancement)."""
    registry = charger_registry()

    print("=" * 60)
    print("SUPER-COMBOS DISPONIBLES (numerotes, CV-008)")
    print("=" * 60)
    print()

    for combo in registry.get("super-combos", []):
        # Lecture defensive : un champ manquant est SIGNALE, il ne fait jamais
        # planter le lanceur (trou attrape le 2026-09-13 : sc-002 n'avait
        # jamais ete enregistre, seuls id/nom/fichier existaient).
        manquants = [c for c in ("description", "phases") if not combo.get(c)]
        if not combo.get(CLE_CONTRAT_VERBES):
            manquants.append(CLE_CONTRAT_VERBES)
        print("  " + str(combo.get("id", "?")).ljust(7) + " : " + str(combo.get("nom", "?")))
        print("          " + str(combo.get("description", "(description manquante)")))
        print("          Phases: " + (", ".join(combo.get("phases", [])) or "(non declarees)"))
        defaut = combo.get(CLE_CONTRAT_VERBE, "")
        verbes = combo.get(CLE_CONTRAT_VERBES) or []
        print("          Lancement: " + ("defaut " + defaut if defaut else "aucune entree unique")
              + (" -- verbes : " + ", ".join(verbes) if verbes else ""))
        if manquants:
            print("          ECART registre : champ(s) manquant(s) : " + ", ".join(manquants))
        print()

    print("Utilisation : python lancer-super-combos.py --numero <sc-NNN> [--verbe <verbe>]")
    print("Exemple : python lancer-super-combos.py --numero sc-001 --fichier mon_fichier.py")
    print("Exemple : python lancer-super-combos.py --numero sc-002 --verbe detecter \"Quand X, Y, car Z\" --type outil --gravite mineure --frequence ponctuelle")


def lancer_super_combos(numero, verbe_demande="", fichier=None, mission=None, extras=None):
    """Lancer un super-combos par son numero (sc-001, sc-002...)."""
    extras = list(extras or [])
    registry = charger_registry()
    numero = normaliser_numero(numero)

    combo = None
    for candidat in registry.get("super-combos", []):
        if candidat.get("id") == numero:
            combo = candidat
            break

    if not combo:
        print("ERREUR : Super-combos " + numero + " introuvable")
        return CODE_INCONNU

    print("Lancement du super-combos " + combo["id"] + " : " + str(combo.get("nom", "")))
    print()

    code, verbe, message = resoudre_lancement(combo, verbe_demande)
    if code != 0:
        print("REFUS : " + message)
        return code

    script_path = Path(__file__).parent / combo["fichier"]
    cmd = [sys.executable, str(script_path), verbe]

    if fichier:
        cmd.extend(["--fichier", fichier])

    if mission:
        cmd.extend(["--mission", mission])

    cmd.extend(extras)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
    else:
        # Un echec doit DIRE pourquoi. Le diagnostic d'un super-combo peut
        # partir sur STDOUT (sc-002 repond "Phase inconnue: executer" sur
        # stdout) : afficher stderr seul perdait le message et laissait un
        # "ERREUR :" vide devant l'agent (trou mesure le 2026-09-13, MO-067).
        print("ERREUR (code " + str(result.returncode) + ") :")
        for nom_flux, texte in (("stdout", result.stdout), ("stderr", result.stderr)):
            if texte and texte.strip():
                print("  [" + nom_flux + "] " + texte.strip())
        if not (result.stdout and result.stdout.strip()) and not (result.stderr and result.stderr.strip()):
            print("  (aucun message : le script n'a rien dit -- verifier " + str(script_path) + ")")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Lanceur de super-combos")
    parser.add_argument("--numero", help="Numero du super-combos (sc-001, sc-002, etc.)")
    parser.add_argument("--verbe", default="", help="Verbe a lancer (defaut : celui du registre)")
    parser.add_argument("--fichier", help="Fichier a traiter")
    parser.add_argument("--mission", help="ID de la mission")
    parser.add_argument("--lister", action="store_true", help="Lister les super-combos disponibles")
    # Les arguments NON reconnus sont TRANSMIS au super-combo : c'est ainsi qu'on
    # lui donne ses propres options (les phases de sc-002 en exigent).
    args, extras = parser.parse_known_args()

    if args.lister or not args.numero:
        lister_super_combos()
        return 0

    return lancer_super_combos(args.numero, args.verbe, args.fichier, args.mission, extras)


if __name__ == "__main__":
    sys.exit(main())
