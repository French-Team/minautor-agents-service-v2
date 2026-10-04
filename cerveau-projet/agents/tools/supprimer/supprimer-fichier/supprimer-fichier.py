#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
supprimer-fichier.py

Supprimer un fichier avec verification.

Options:
  --backup         Creer une sauvegarde .bak avant suppression
  --forcer         Supprimer sans confirmer
  --dry-run        Simuler sans supprimer
  --verbose        Afficher les details
  --help           Afficher cette aide
  --version        Afficher la version

Retour : 0 si succes, 1 si erreur ou si le fichier n'existe pas
         (echec explicite : jamais 0 silencieux).

Proprietaire : Buffy (outil partage)
Version : 0.3.2
Statut : prepare
"""

import os
import shutil
import sys

VERSION = "0.3.2"
STATUT = "prepare"

NOM_ATTENDU = "supprimer-fichier.py"

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    if nom_script != NOM_ATTENDU:
        print("[ERREUR] Nom de fichier invalide : %s" % nom_script)
        print("  Attendu : %s" % NOM_ATTENDU)
        sys.exit(2)


def afficher_aide():
    print("=== supprimer-fichier v%s ===" % VERSION)
    print("")
    print("Usage: supprimer-fichier.py [OPTIONS] <fichier>")
    print("")
    print("Options :")
    print("  --backup         Creer une sauvegarde .bak avant suppression")
    print("  --forcer         Supprimer sans confirmer")
    print("  --dry-run        Simuler sans supprimer")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")
    print("  --version        Afficher la version")
    print("")
    print("Retour : 0 si succes, 1 si erreur ou si le fichier n'existe pas.")


def verrouiller_habilitation(agent, outil, audit=False):
    """Appelle proteger-verrou-habilitation et retourne (code, message).
    Source de verite : les cartes de decision (aucune liste en dur).
    audit=True (v0.2.0) : mode tests - pas de verification d identite reelle."""
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            break
        parent = os.path.dirname(courant)
        if parent == courant:
            return (2, "[ERREUR] Racine du projet introuvable (AGENTS.md absent)")
        courant = parent
    verrou = os.path.join(
        courant, "cerveau-projet", "agents", "tools", "proteger",
        "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    import subprocess
    cmd = [sys.executable, verrou, "--agent", agent, "--outil", outil]
    if audit:
        cmd.append("--audit")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    message = (r.stdout + r.stderr).strip()
    return (r.returncode, message)


def main(argv):
    verifier_nommage(os.path.basename(sys.argv[0]))

    fichier = ""
    agent = ""
    backup = False
    forcer = False
    dry_run = False
    verbose = False
    help_demande = False
    audit = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--forcer":
            forcer = True
        elif arg == "--backup":
            backup = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--audit":
            audit = True
        elif arg == "--agent":
            if i + 1 >= len(argv):
                print("[ERREUR] --agent requiert un nom d agent")
                return 2
            agent = argv[i + 1]
            i += 1
        elif arg == "--version":
            print("supprimer-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            fichier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not fichier:
        print("[ERREUR] Aucun fichier specifie")
        afficher_aide()
        return 1

    # VERROU D HABILITATION (regle immuable : seul hygie supprime). --agent
    # est OBLIGATOIRE et le verrou est appele AVANT toute action : si l agent
    # n est pas habilite, la suppression est refusee et le message indique
    # QUI est habilite (cycle Cerberus -> agent).
    if not agent:
        print("[ERREUR] --agent est OBLIGATOIRE : l outil doit connaitre "
              "l agent appelant (verrou d habilitation).")
        return 2
    code, message = verrouiller_habilitation(agent, "supprimer-fichier", audit=audit)
    if code != 0:
        print(message)
        return 1 if code == 1 else 2

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in fichier:
        print("[ERREUR] Chemin non sur (octet nul present)")
        return 1

    # Note securite : os.remove() sur un lien symbolique supprime LE LIEN
    # lui-meme, jamais la cible - la suppression est donc sure (aucune
    # traversee). Les liens de dossier (NTFS junction) ne sont pas touches.

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier inexistant: %s" % fichier)
        return 1

    if dry_run:
        print("[DRY-RUN] Suppression: %s" % fichier)
        return 0

    if backup:
        shutil.copy2(fichier, fichier + ".bak")
        if verbose:
            print("[INFO] Sauvegarde: %s.bak" % fichier)

    os.remove(fichier)

    if verbose:
        print("[OK] Supprime: %s" % fichier)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
