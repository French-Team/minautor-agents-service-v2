#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
rechercher-accents-sensibles.py

Recherche les caracteres non-ASCII dans les ZONES SENSIBLES uniquement :
  - frontmatter YAML (blocs --- en tete des .md)
  - noms de fichiers et dossiers
  - blocs de code (``` ... ``` dans les .md)
  - fichiers de code (.sh, .py, .js, etc. - fichier entier)
  - liens relatifs [texte](chemin) dans les .md

Mode : RECHERCHE ET RAPPORT UNIQUEMENT (jamais de correction).

Options:
  --zones <liste>      Zones a rechercher (frontmatter,noms,blocs,code,liens)
  --extensions <liste> Extensions des fichiers de code (defaut: sh,py,js,json,yaml,yml,txt)
  --exclure <liste>    Motifs de chemins a exclure
  --verbose            Afficher le detail ligne par ligne
  --help               Afficher cette aide

Proprietaire : Themis (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

EXCLUSIONS_DEFAUT = "node_modules,.git,.agents,.backup,.tmp,dictionnaire-,exemples"
EXTENSIONS_DEFAUT = "sh,py,js,json,yaml,yml,txt"

ZONES_DISPONIBLES = ("frontmatter", "noms", "blocs", "code", "liens")


def afficher_aide():
    print("=== rechercher-accents-sensibles v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-accents-sensibles.py [OPTIONS] [DOSSIER]")
    print("")
    print("Options :")
    print("  --zones <liste>      Zones a rechercher (separees par des virgules)")
    print("                       Disponibles : frontmatter, noms, blocs, code, liens")
    print("  --extensions <liste> Extensions des fichiers de code (ex: sh,py,js)")
    print("  --exclure <liste>    Motifs de chemins a exclure")
    print("  --verbose            Afficher le detail ligne par ligne")
    print("  --help               Afficher cette aide")
    print("")
    print("NOTE : Cet outil ne modifie JAMAIS les fichiers. Il recherche et rapporte.")


def est_non_ascii(ligne):
    """Retourner True si la ligne contient un caractere hors [ -~]."""
    for ch in ligne:
        if ord(ch) > 127:
            return True
    return False


def est_md(fichier):
    return fichier.endswith(".md")


def est_code(fichier, extensions):
    return any(fichier.endswith("." + ext) for ext in extensions)


def analyser_fichier(fichier, zones, extensions, verbose):
    """Analyser un fichier et retourner la liste des detections (zone, ligne, detail)."""
    detections = []
    nom = os.path.basename(fichier)

    # ZONE NOMS : verifie le nom du fichier une fois
    if "noms" in zones and est_non_ascii(nom):
        detections.append(("noms", 0, nom))

    if not (est_md(fichier) or est_code(fichier, extensions)):
        return detections

    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            lignes = fh.readlines()
    except IOError:
        return detections

    in_fm = False
    in_bloc = False

    for i, ligne in enumerate(lignes, 1):
        contenu = ligne.rstrip("\r\n")

        # ZONE CODE : fichier de code entier
        if est_code(fichier, extensions):
            if "code" in zones and est_non_ascii(contenu):
                detections.append(("code", i, contenu))
            continue

        # --- mode md ---
        # FRONTMATTER : bloc --- ... --- en tete
        if "frontmatter" in zones:
            if i == 1 and contenu.strip() == "---":
                in_fm = True
                continue
            if in_fm and contenu.strip() == "---":
                in_fm = False
                continue
            if in_fm and est_non_ascii(contenu):
                detections.append(("frontmatter", i, contenu))

        # BLOCS DE CODE : lignes entre ``` et ```
        if "blocs" in zones:
            if contenu.strip().startswith("```"):
                in_bloc = not in_bloc
                continue
            if in_bloc and est_non_ascii(contenu):
                detections.append(("blocs", i, contenu))

        # LIENS RELATIFS : extraire les chemins ](...)
        if "liens" in zones:
            for m in re.finditer(r"\]\(([^)]*)\)", contenu):
                chemin = m.group(1)
                if est_non_ascii(chemin):
                    detections.append(("liens", i, chemin))

    return detections


def main(argv):
    dossier = "."
    zones = "frontmatter,noms,blocs,code,liens"
    extensions = EXTENSIONS_DEFAUT
    exclusions = EXCLUSIONS_DEFAUT
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--zones" and i + 1 < len(argv):
            zones = argv[i + 1]
            i += 2
            continue
        if arg == "--extensions" and i + 1 < len(argv):
            extensions = argv[i + 1]
            i += 2
            continue
        if arg == "--exclure" and i + 1 < len(argv):
            exclusions = argv[i + 1]
            i += 2
            continue
        if arg == "--verbose":
            verbose = True
            i += 1
            continue
        if arg in ("--help", "--aide", "-h"):
            help_demande = True
            i += 1
            continue
        if arg == "--version":
            print("rechercher-accents-sensibles v%s (%s)" % (VERSION, STATUT))
            return 0
        dossier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    print("=== Rechercher accents dans les zones sensibles ===")
    print("Version : %s" % VERSION)
    print("Dossier : %s" % dossier)
    print("Zones : %s" % zones)
    print("Fichiers EXCEPTION VOLONTAIRE (dictionnaire-*) exclus automatiquement")
    print("")

    if not os.path.isdir(dossier):
        print("[ERREUR] Le dossier n'existe pas : %s" % dossier)
        return 1

    zone_liste = [z.strip() for z in zones.split(",") if z.strip()]
    ext_liste = [e.strip() for e in extensions.split(",") if e.strip()]
    excl_liste = [m for m in exclusions.split(",") if m]

    nb_fichiers = 0
    nb_fichiers_problemes = 0
    nb_detections = {z: 0 for z in ZONES_DISPONIBLES}

    for racine, dossiers, fichiers in os.walk(dossier):
        dossiers[:] = [d for d in dossiers if d != ".git" and not d.startswith(".")]
        for nom in fichiers:
            chemin = os.path.join(racine, nom)
            if any(m in chemin for m in excl_liste):
                continue
            nb_fichiers += 1
            detections = analyser_fichier(chemin, zone_liste, ext_liste, verbose)
            if detections:
                nb_fichiers_problemes += 1
                zones_touchees = ", ".join(sorted(set(z for z, _, _ in detections)))
                if verbose:
                    for zone, num, detail in detections:
                        prefixe = "noms" if zone == "noms" and num == 0 else "ligne %d" % num
                        print("  [%s] %s (%s) : %s" % (zone, chemin, prefixe, detail))
                else:
                    print("  [%s] %s" % (zones_touchees, chemin))
            for zone, _, _ in detections:
                nb_detections[zone] += 1

    total = sum(nb_detections.values())
    print("")
    print("=== Resume ===")
    print("Total fichiers examines : %d" % nb_fichiers)
    print("Fichiers avec accent en zone sensible : %d" % nb_fichiers_problemes)
    print("Detections par zone :")
    print("  frontmatter YAML : %d" % nb_detections["frontmatter"])
    print("  noms de fichiers : %d" % nb_detections["noms"])
    print("  blocs de code    : %d" % nb_detections["blocs"])
    print("  fichiers de code : %d" % nb_detections["code"])
    print("  liens relatifs   : %d" % nb_detections["liens"])
    print("  TOTAL            : %d" % total)
    print("")
    print("[INFO] Recherche seule : aucun fichier n a ete modifie.")
    print("[INFO] Pour corriger : utiliser corriger-accents-zones-sensibles ou corriger-emojis, puis relancer.")

    return 1 if nb_fichiers_problemes > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
