#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
editer-fichier.py

Remplace une chaine par une autre dans un fichier.
Premiere occurrence par defaut, toutes avec --global.

Utilisation:
  editer-fichier.py [OPTIONS] <fichier> <ancien> <nouveau>

Options :
  --global         Remplacer toutes les occurrences
  --backup         Creer une sauvegarde .bak avant
  --dry-run        Simuler sans modifier
  --verbose        Afficher les details
  --help           Afficher cette aide
  --version        Afficher la version

Retour : 0 si succes, 1 si erreur ou si AUCUNE occurrence trouvee
         (echec explicite : jamais 0 silencieux).

Proprietaire : Vulcain (outil partage)
Version : 0.4.1
Statut : prepare
"""

import io
import os
import shutil
import sys

VERSION = "0.4.1"
STATUT = "prepare"

NOM_ATTENDU = "editer-fichier.py"

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
    print("=== editer-fichier v%s ===" % VERSION)
    print("")
    print("Usage: editer-fichier.py [OPTIONS] <fichier> <ancien> <nouveau>")
    print("")
    print("Options :")
    print("  --global         Remplacer toutes les occurrences")
    print("  --backup         Creer une sauvegarde .bak avant")
    print("  --dry-run        Simuler sans modifier")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")
    print("  --version        Afficher la version")
    print("")
    print("Exemples :")
    print("  editer-fichier.py fichier.md \"ancien\" \"nouveau\"")
    print("  editer-fichier.py --global fichier.md \"texte\" \"remplacement\"")
    print("")
    print("Retour : 0 si succes, 1 si erreur ou si AUCUNE occurrence trouvee.")


def main(argv):
    verifier_nommage(os.path.basename(sys.argv[0]))

    fichier = ""
    ancien = ""
    nouveau = ""
    global_remplacement = False
    backup = False
    dry_run = False
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--global":
            global_remplacement = True
        elif arg == "--backup":
            backup = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--verbose":
            verbose = True
        elif arg in ("--help", "-h"):
            help_demande = True
        elif arg == "--version":
            print("editer-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            if not fichier:
                fichier = arg
            elif not ancien:
                ancien = arg
            elif not nouveau:
                nouveau = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not fichier or not ancien:
        print("[ERREUR] Arguments manquants")
        afficher_aide()
        return 1

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in fichier:
        print("[ERREUR] Chemin non sur (octet nul present)")
        return 1

    # Securite (round 3) : refus de modifier a travers un lien symbolique
    # (l'ecriture suivrait le lien vers la cible a l'insu de l'agent)
    if os.path.islink(fichier):
        print("[ERREUR] Chemin est un lien symbolique (refus securite): %s" % fichier)
        return 1

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve: %s" % fichier)
        return 1

    # Lecture robuste (round 3) : UTF-8 puis fallback latin-1, jamais de crash
    contenu = None
    try:
        with io.open(fichier, encoding="utf-8-sig") as fh:
            contenu = fh.read()
    except (UnicodeDecodeError, OSError):
        try:
            with io.open(fichier, encoding="latin-1") as fh:
                contenu = fh.read()
        except Exception:
            contenu = None
    if contenu is None:
        print("[ERREUR] Impossible de lire le fichier : %s" % fichier)
        return 1

    if ancien not in contenu:
        print("[ERREUR] Aucune occurrence de '%s' dans %s" % (ancien, fichier))
        print("  (verifiez l'indentation exacte et le contenu de la chaine)")
        return 1

    if global_remplacement:
        nb = contenu.count(ancien)
    else:
        nb = 1

    if dry_run:
        print("[DRY-RUN] %d occurrence(s) trouvee(s)" % nb)
        for num, ligne in enumerate(contenu.split("\n"), 1):
            if ancien in ligne:
                print("  %d: %s" % (num, ligne.strip()))
        return 0

    if backup:
        shutil.copy2(fichier, fichier + ".bak")
        if verbose:
            print("[INFO] Sauvegarde: %s.bak" % fichier)

    # UNE SEULE PASSE (performance round 2) : le test d'existence 'ancien in
    # contenu' est fait avant (aucun double scan complet du fichier). Pour un
    # remplacement simple, replace(..., 1) ne scanne que jusqu'a la premiere
    # occurrence ; count n'est calcule que pour --global.
    if global_remplacement:
        nouveau_contenu = contenu.replace(ancien, nouveau)
    else:
        nouveau_contenu = contenu.replace(ancien, nouveau, 1)

    with io.open(fichier, "w", encoding="utf-8", newline="") as fh:
        fh.write(nouveau_contenu)

    if verbose:
        print("[OK] %d occurrence(s) remplacee(s) dans %s" % (nb, fichier))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
