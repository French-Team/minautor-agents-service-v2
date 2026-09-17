#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-evolution -- Super-combo auto-evolution (Optimus Prime)

Orchestre le cycle complet : detecter -> qualifier -> cibler -> modifier -> valider
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path


OUTILS_DIR = Path(__file__).parent.parent / "combos" / "outils"

# Le vocabulaire du PROCESSUS (types, gravites, frequences, demandes
# d'archivage) a UN domicile : l'outil bdd-frictions. L'orchestrateur le
# CONSOMME au lieu de recopier les valeurs admises (friction 50, MO-129).
BORNES_REMONTEE = 30


def charger_vocabulaire(nom_outil, nom_module):
    """Le vocabulaire d'un outil, charge par son chemin, ou None.

    MEME MOTIF que l'espion d'activite et revert-periode : ce chargement est
    aujourd'hui RECOPIE trois fois (friction 54, a porter dans un moteur
    partage). Retourner None vaut refus de deviner.
    """
    chemin = OUTILS_DIR / nom_outil / "fonctions" / nom_module
    if not chemin.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location(
            nom_outil.replace("-", "_") + "_domicile", str(chemin))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None
    return module


VOCABULAIRE_FRICTIONS = charger_vocabulaire("bdd-frictions", "bdd_frictions.py")


def run_outil(nom, args):
    """Executer un outil et retourner (code, stdout, stderr)"""
    outil_path = OUTILS_DIR / nom
    if nom.endswith(".py"):
        cmd = [sys.executable, str(outil_path)] + args
    else:
        cmd = [sys.executable, str(outil_path / "main.py")] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nPhases:")
        print("  detecter    -- Noter une friction (etape 1)")
        print("  qualifier   -- Lister/analyser frictions mission (etape 2)")
        print("  cibler      -- Verrouiller fichier cible (etape 3)")
        print("  modifier-avant -- Lecture + hash avant (etape 4a, non-bloquant)")
        print("  modifier-apres -- Hash apres + tests + BDD (etape 4b, non-bloquant)")
        print("  valider     -- Auto-valider (faible/moyen) ou createur (critique) (etape 5)")
        print("  stats       -- Statistiques auto-evolution")
        return 1

    phase = sys.argv[1]
    args = sys.argv[2:]

    if VOCABULAIRE_FRICTIONS is None:
        print("Vocabulaire des statuts introuvable (domicile bdd-frictions) : refus de deviner")
        print("les valeurs admises par la porte (friction 50, balayage MO-129).")
        return 2

    if phase == "detecter":
        return cmd_detecter(args)
    elif phase == "qualifier":
        return cmd_qualifier(args)
    elif phase == "cibler":
        return cmd_cibler(args)
    elif phase == "modifier-avant":
        return cmd_modifier_avant(args)
    elif phase == "modifier-apres":
        return cmd_modifier_apres(args)
    elif phase == "valider":
        return cmd_valider(args)
    elif phase == "stats":
        return cmd_stats(args)
    else:
        print(f"Phase inconnue: {phase}")
        return 1


def cmd_detecter(args):
    """Phase 1: Detecter une friction"""
    import argparse
    parser = argparse.ArgumentParser(description="Noter une friction")
    parser.add_argument("phrase", help="Quand <situation>, <probleme>, car <cause>")
    parser.add_argument("--type", required=True, choices=list(VOCABULAIRE_FRICTIONS.TYPES))
    parser.add_argument("--gravite", required=True, choices=list(VOCABULAIRE_FRICTIONS.GRAVITES))
    parser.add_argument("--frequence", required=True, choices=list(VOCABULAIRE_FRICTIONS.FREQUENCES))
    parser.add_argument("--mission-id", help="ID mission (optionnel)")
    parsed = parser.parse_args(args)

    code, out, err = run_outil("bdd-frictions", ["ajouter", parsed.phrase, "--type", parsed.type, "--gravite", parsed.gravite, "--frequence", parsed.frequence] + (["--mission-id", parsed.mission_id] if parsed.mission_id else []))
    print(out)
    if err:
        print(err, file=sys.stderr)
    return code


def cmd_qualifier(args):
    """Phase 2: Qualifier les frictions d'une mission"""
    import argparse
    parser = argparse.ArgumentParser(description="Lister frictions pour qualification")
    parser.add_argument("--mission-id", required=True)
    parsed = parser.parse_args(args)

    code, out, err = run_outil("bdd-frictions", ["lister", "--mission-id", parsed.mission_id, "--n", "50"])
    print(out)
    if err:
        print(err, file=sys.stderr)

    print("\n=== GRILLE QUALIFICATION (3 criteres) ===")
    print("Pour chaque friction :")
    print("  1. Reutilisable dans >1 contexte ? (OUI/NON)")
    print("  2. Cause racine identifable ? (OUI/NON)")
    print("  3. Solution reversible ? (OUI/NON)")
    print("\n3/3 = VRAIE REGLE GENERALE -> phase cibler")
    print("<3 = CAS PARTICULIER -> bdd-frictions archiver --id <id> --statut "
          + "|".join(VOCABULAIRE_FRICTIONS.DEMANDES_ARCHIVAGE) + " --raison cas-particulier")
    return code


def cmd_cibler(args):
    """Phase 3: Choisir et verrouiller la cible"""
    import argparse
    parser = argparse.ArgumentParser(description="Verrouiller fichier cible")
    parser.add_argument("--fichier", required=True, help="Chemin relatif depuis racine projet")
    parsed = parser.parse_args(args)

    code, out, err = run_outil("bdd-modifs", ["verrouiller", "--fichier", parsed.fichier])
    print(out)
    if err:
        print(err, file=sys.stderr)
    return code


def cmd_modifier_avant(args):
    """Phase 4a: Lecture + hash avant (non-bloquant). L agent modifie ENSUITE, puis appelle modifier-apres."""
    import argparse
    parser = argparse.ArgumentParser(description="Pre-modification : lecture + hash avant")
    parser.add_argument("--fichier", required=True)
    parsed = parser.parse_args(args)

    fichier_path = Path(parsed.fichier)
    if not fichier_path.exists():
        print(f"Fichier introuvable: {fichier_path}")
        return 1

    print(f"=== MODIFICATION-AVANT: {fichier_path} ===")

    print("\n1. Lecture complete...")
    code, out, err = run_outil("lire-fichier-complet.py", [str(fichier_path)])
    print(out)
    if code != 0:
        return code

    print("\n2. Hash AVANT...")
    code, out, err = run_outil("calculer-hash.py", [str(fichier_path)])
    hash_avant = out.strip().split()[0] if out.strip() else ""
    print(out)
    if code != 0:
        return code

    print(f"\nHASH_AVANT={hash_avant}")
    print("Modifiez le fichier (edit ou ajouter-case/redirect-theme.py), puis appelez :")
    print(f"  modifier-apres --fichier {fichier_path} --hash-avant {hash_avant} --friction-id <id> --raison \"<txt>\" --type <type>")
    return 0


def cmd_modifier_apres(args):
    """Phase 4b: Hash apres + tests + BDD (non-bloquant)."""
    import argparse
    parser = argparse.ArgumentParser(description="Post-modification : hash apres + tests + BDD")
    parser.add_argument("--fichier", required=True)
    parser.add_argument("--hash-avant", required=True)
    parser.add_argument("--friction-id", type=int, required=True)
    parser.add_argument("--raison", required=True)
    parser.add_argument("--type", choices=["theme", "protocole", "fiche", "combo", "outil", "convention", "regle"], default="theme")
    parsed = parser.parse_args(args)

    fichier_path = Path(parsed.fichier)
    if not fichier_path.exists():
        print(f"Fichier introuvable: {fichier_path}")
        return 1

    print(f"=== MODIFICATION-APRES: {fichier_path} ===")

    print("\n1. Hash APRES...")
    code, out, err = run_outil("calculer-hash.py", [str(fichier_path)])
    hash_apres = out.strip().split()[0] if out.strip() else ""
    print(out)
    if code != 0:
        return code

    if hash_apres == parsed.hash_avant:
        print("ATTENTION: hash inchange (aucune modification detectee).")
        return 1

    print("\n2. Tests validation...")
    if parsed.type == "theme":
        code, out, err = run_outil("tester-theme.py", [str(fichier_path)])
        print(out)
        if err:
            print(err, file=sys.stderr)
        if code != 0:
            print("ATTENTION: Theme invalide !")
            return code
    else:
        if str(fichier_path).endswith(".json"):
            try:
                import json
                with open(fichier_path, "r", encoding="utf-8") as f:
                    json.load(f)
                print("  JSON valide: OK")
            except Exception as e:
                print(f"  JSON INVALIDE: {e}")
                return 1

    print("\n3. Enregistrement BDD modifications...")
    diff = f"Hash avant: {parsed.hash_avant}\nHash apres: {hash_apres}\nFichier: {fichier_path}\nType: {parsed.type}\nRaison: {parsed.raison}"
    code, out, err = run_outil("bdd-modifs", ["ajouter", "--fichier", str(fichier_path), "--hash-avant", parsed.hash_avant, "--hash-apres", hash_apres, "--diff", diff, "--raison", parsed.raison, "--friction-id", str(parsed.friction_id)])
    print(out)
    if err:
        print(err, file=sys.stderr)

    return code


def cmd_valider(args):
    """Phase 5: auto-valider (faible/moyen) ou valider createur (critique)"""
    import argparse
    parser = argparse.ArgumentParser(description="Valider evolution")
    parser.add_argument("--fichier", required=True)
    parser.add_argument("--friction-id", type=int, required=True)
    parser.add_argument("--statut", required=True,
                        choices=list(VOCABULAIRE_FRICTIONS.DEMANDES_ARCHIVAGE))
    parser.add_argument("--raison", default="")
    parser.add_argument("--risque", default="faible", choices=["faible", "moyen", "critique"])
    parsed = parser.parse_args(args)

    mode = "AUTO" if parsed.risque in ("faible", "moyen") else "CREATEUR"
    print(f"=== VALIDATION {mode}: {parsed.fichier} (risque={parsed.risque}) ===")
    print(f"Statut: {parsed.statut.upper()}")

    if parsed.statut == VOCABULAIRE_FRICTIONS.DEMANDE_VALIDE:
        code, out, err = run_outil("bdd-modifs", ["deverrouiller", "--fichier", parsed.fichier])
        print(out)
        code, out, err = run_outil("bdd-frictions", ["archiver", "--id", str(parsed.friction_id), "--statut", "valide"])
        print(out)
        print("\n-> Lecon a enregistrer via: bdd-lecons ajouter \"<regle>\" --agent optimus-prime --categorie auto-evolution --mots-cles auto-valide,friction:<id>")
        if parsed.risque == "moyen":
            print("-> NOTIFIER createur a posteriori (resume + diff + preuves, sans blocage).")
    else:
        auteur = "auto (tests KO)" if parsed.risque in ("faible", "moyen") else "createur"
        code, out, err = run_outil("revert-fichier.py", ["--fichier", parsed.fichier, "--depuis-bak"])
        print(out)
        code, out, err = run_outil("bdd-modifs", ["annuler", "--fichier", parsed.fichier, "--raison", parsed.raison or f"Annule ({auteur})"])
        print(out)
        code, out, err = run_outil("bdd-frictions", ["archiver", "--id", str(parsed.friction_id), "--statut", "annule", "--raison", parsed.raison or f"Annule ({auteur})"])
        print(out)

    return 0


def cmd_stats(args):
    """Statistiques globales"""
    print("=== STATS FRICTIONS ===")
    code, out, err = run_outil("bdd-frictions", ["stats"])
    print(out)

    print("\n=== STATS MODIFICATIONS ===")
    code, out, err = run_outil("bdd-modifs", ["lister", "--n", "10"])
    print(out)

    return 0


if __name__ == "__main__":
    sys.exit(main())