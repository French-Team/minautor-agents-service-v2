#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
verifier-systeme.py

Verifie le systeme de l'utilisateur et retourne les informations :
OS, architecture, shells, langages et outils disponibles (bash,
python3, node, git, npm) avec leurs versions et chemins.

Utilisation:
  verifier-systeme.py [OPTIONS]

Options:
  --aide, -h          Afficher cette aide
  --format FORMAT     Format de sortie: table, json, resume (defaut: table)
  --detail DETAIL     Niveau de detail: standard, complet (defaut: standard)
  --version           Afficher la version

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import json
import os
import platform
import shutil
import subprocess
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("==========================================")
    print("  verifier-systeme v%s" % VERSION)
    print("  Verifie le systeme de l'utilisateur")
    print("==========================================")
    print("")
    print("Usage: verifier-systeme.py [OPTIONS]")
    print("")
    print("Options:")
    print("  --aide, -h          Afficher cette aide")
    print("  --format FORMAT     Format de sortie: table, json, resume (defaut: table)")
    print("  --detail DETAIL     Niveau de detail: standard, complet (defaut: standard)")
    print("  --version           Afficher la version")
    print("")
    print("Exemples:")
    print("  verifier-systeme.py")
    print("  verifier-systeme.py --format json")
    print("  verifier-systeme.py --format resume --detail complet")


def detecter_os():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    if system == "Linux":
        return "Linux"
    if system == "Darwin":
        return "Mac"
    return "Inconnu (%s)" % system


def obtenir_version(outil):
    try:
        resultat = subprocess.run(
            [outil, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        premiere = (resultat.stdout or resultat.stderr).split("\n")[0]
        return premiere.strip() if premiere.strip() else "Version inconnue"
    except Exception:
        return "Version inconnue"


def verifier_outil(outil):
    chemin = shutil.which(outil)
    if chemin:
        return {"disponible": True, "version": obtenir_version(outil), "chemin": chemin}
    return {"disponible": False, "version": "-", "chemin": "-"}


def informations_systeme():
    os_nom = detecter_os()
    arch = platform.machine() or "Inconnu"
    if os_nom == "Windows":
        version_os = platform.version() or "Inconnu"
    else:
        version_os = platform.release() or "Inconnu"
    return os_nom, version_os, arch


def afficher_table():
    print("| Categorie | Element | Disponible | Version | Chemin |")
    print("|---|---|---|---|---|")

    os_nom, version_os, arch = informations_systeme()
    print("| Systeme | OS | %s | %s | - |" % (os_nom, version_os))
    print("| Systeme | Architecture | %s | - | - |" % arch)

    bash = verifier_outil("bash")
    print("| Shell | Bash | %s | %s | %s |" % (
        "Oui" if bash["disponible"] else "Non", bash["version"], bash["chemin"]))

    python = verifier_outil("python3")
    print("| Langage | Python | %s | %s | %s |" % (
        "Oui" if python["disponible"] else "Non", python["version"], python["chemin"]))

    node = verifier_outil("node")
    print("| Langage | Node.js | %s | %s | %s |" % (
        "Oui" if node["disponible"] else "Non", node["version"], node["chemin"]))

    git = verifier_outil("git")
    print("| Outil | Git | %s | %s | %s |" % (
        "Oui" if git["disponible"] else "Non", git["version"], git["chemin"]))

    npm = verifier_outil("npm")
    print("| Outil | npm | %s | %s | %s |" % (
        "Oui" if npm["disponible"] else "Non", npm["version"], npm["chemin"]))


def afficher_json():
    os_nom, version_os, arch = informations_systeme()
    bash = verifier_outil("bash")
    python = verifier_outil("python3")
    node = verifier_outil("node")
    git = verifier_outil("git")
    npm = verifier_outil("npm")

    donnees = {
        "systeme": {
            "os": os_nom,
            "version": version_os,
            "arch": arch,
        },
        "shells": [
            {"nom": "Bash", "disponible": bash["disponible"], "version": bash["version"]},
        ],
        "langages": [
            {"nom": "Python", "disponible": python["disponible"], "version": python["version"]},
            {"nom": "Node.js", "disponible": node["disponible"], "version": node["version"]},
        ],
        "outils": [
            {"nom": "Git", "disponible": git["disponible"], "version": git["version"]},
            {"nom": "npm", "disponible": npm["disponible"], "version": npm["version"]},
        ],
    }
    print(json.dumps(donnees, indent=2, ensure_ascii=True))


def afficher_resume():
    os_nom, version_os, arch = informations_systeme()
    bash = verifier_outil("bash")
    python = verifier_outil("python3")
    node = verifier_outil("node")
    git = verifier_outil("git")

    print("**Systeme** : %s %s (%s)" % (os_nom, version_os, arch))
    print("**Shells** : Bash %s" % bash["version"])
    print("**Langages** : %s, %s" % (python["version"], node["version"]))
    print("**Outils** : Git %s" % git["version"])


def main(argv):
    format_sortie = "table"
    detail = "standard"

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "-h"):
            afficher_aide()
            return 0
        elif arg == "--version":
            print("verifier-systeme v%s" % VERSION)
            return 0
        elif arg == "--format":
            if i + 1 < len(argv):
                format_sortie = argv[i + 1]
                i += 1
        elif arg == "--detail":
            if i + 1 < len(argv):
                detail = argv[i + 1]
                i += 1
        else:
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        i += 1

    if format_sortie not in ("table", "json", "resume"):
        print("Format inconnu: %s" % format_sortie)
        print("Formats disponibles: table, json, resume")
        return 1

    if format_sortie == "table":
        afficher_table()
    elif format_sortie == "json":
        afficher_json()
    else:
        afficher_resume()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
