#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
verifier-systeme.py

Verifie le systeme de l'utilisateur et retourne les informations :
OS, architecture, shells, langages et outils disponibles (bash,
python3, node, git, npm) avec leurs versions et chemins.

Option --enregistrer : ecrit / met a jour la variable profil-systeme
dans le classeur-variables (stockage + historique).

Utilisation:
  verifier-systeme.py [OPTIONS]

Options:
  --aide, -h          Afficher cette aide
  --format FORMAT     Format de sortie: table, json, resume (defaut: table)
  --detail DETAIL     Niveau de detail: standard, complet (defaut: standard)
  --enregistrer       Ecrire le profil systeme dans le classeur-variables
  --version           Afficher la version

Proprietaire : Vulcain (outil partage)
Version : 0.2.1-py
Statut : prepare
"""

import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys

VERSION = "0.2.1-py"
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
    print("  --enregistrer       Ecrire le profil systeme dans le classeur-variables")
    print("  --version           Afficher la version")
    print("")
    print("Exemples:")
    print("  verifier-systeme.py")
    print("  verifier-systeme.py --format json")
    print("  verifier-systeme.py --format resume --detail complet")
    print("  verifier-systeme.py --enregistrer")


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


def extraire_version(texte):
    """Extrait le premier numero de version (ex: 'Python 3.14.4' -> '3.14.4')."""
    m = re.search(r"(\d+(?:\.\d+)+)", texte or "")
    return m.group(1) if m else "-"


def chemin_classeur(relatif):
    """Chemin absolu vers un fichier du classeur (CWD ou racine du projet)."""
    depuis_cwd = os.path.abspath(relatif)
    if os.path.exists(depuis_cwd):
        return depuis_cwd
    base = os.path.abspath(__file__)
    for _ in range(6):
        base = os.path.dirname(base)
    return os.path.join(base, relatif)


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


def valeur_profil():
    """Construit la valeur compacte de la variable profil-systeme."""
    os_nom, version_os, arch = informations_systeme()
    bash = verifier_outil("bash")
    python = verifier_outil("python3")
    node = verifier_outil("node")
    git = verifier_outil("git")
    return "OS: %s / Bash: %s / Python: %s / Git: %s / Node: %s" % (
        os_nom,
        extraire_version(bash["version"]),
        extraire_version(python["version"]),
        extraire_version(git["version"]),
        extraire_version(node["version"]),
    )


def enregistrer_profil():
    """Ecrit ou met a jour la variable profil-systeme dans le classeur."""
    fichier_stockage = chemin_classeur("cerveau-projet/classeur-variables/stockage/variables-actuelles.md")
    fichier_hist = chemin_classeur("cerveau-projet/classeur-variables/historique/historique-modifications.md")

    if not os.path.exists(fichier_stockage):
        print("ERREUR: classeur introuvable: %s" % fichier_stockage)
        return 1

    date_jour = datetime.date.today().isoformat()
    nouvelle_valeur = valeur_profil()
    nouvelle_ligne = "| `profil-systeme` | %s | verifier-systeme | %s | [OK] |" % (
        nouvelle_valeur, date_jour)

    # --- Lecture de l'ancienne valeur (pour l'historique) ---
    ancienne_valeur = "(aucune)"
    with open(fichier_stockage, encoding="utf-8") as fh:
        lignes = fh.read().split("\n")
    for ligne in lignes:
        if "`profil-systeme`" in ligne:
            debut = ligne.find("| `profil-systeme` | ")
            if debut >= 0:
                reste = ligne[debut + len("| `profil-systeme` | "):]
                ancienne_valeur = reste.split(" | verifier-systeme")[0].strip()
            break

    # --- Mise a jour du tableau de stockage (une seule ligne profil-systeme) ---
    existe = any("`profil-systeme`" in ligne for ligne in lignes)
    resultat = []
    vu = False
    if existe:
        # Remplacer la ligne existante et supprimer les doublons
        for ligne in lignes:
            if "`profil-systeme`" in ligne and not vu:
                resultat.append(nouvelle_ligne)
                vu = True
            elif "`profil-systeme`" in ligne and vu:
                continue
            else:
                resultat.append(ligne)
    else:
        # Inserer apres la ligne fichier-final
        insere = False
        for ligne in lignes:
            resultat.append(ligne)
            if "fichier-final" in ligne and not insere:
                resultat.append(nouvelle_ligne)
                insere = True
        if not insere:
            resultat.append(nouvelle_ligne)
    with open(fichier_stockage, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(resultat))

    # --- Ajout de l'entree dans l'historique (recentes en premier) ---
    if os.path.exists(fichier_hist):
        with open(fichier_hist, encoding="utf-8") as fh:
            lignes_hist = fh.read().split("\n")
        entree = [
            "## %s -- Ecriture" % date_jour,
            "",
            "- **Variable** : profil-systeme",
            "- **Ancienne valeur** : %s" % ancienne_valeur,
            "- **Nouvelle valeur** : %s" % nouvelle_valeur,
            "- **Source** : verifier-systeme",
            "- **Raison** : Mise a jour du profil systeme utilisateur",
            "",
        ]
        resultat_hist = []
        insere_hist = False
        for ligne in lignes_hist:
            resultat_hist.append(ligne)
            if ligne.startswith("## Entrees recentes") and not insere_hist:
                resultat_hist.extend(entree)
                insere_hist = True
        if not insere_hist:
            resultat_hist.extend(entree)
        with open(fichier_hist, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(resultat_hist))

    print("[OK] Profil systeme enregistre dans le classeur-variables")
    print("Variable : profil-systeme")
    print("Valeur   : %s" % nouvelle_valeur)
    print("Source   : verifier-systeme")
    return 0


def main(argv):
    format_sortie = "table"
    detail = "standard"
    enregistrer = False

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
        elif arg == "--enregistrer":
            enregistrer = True
        else:
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        i += 1

    if enregistrer:
        return enregistrer_profil()

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
