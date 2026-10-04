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
  --bloc-fiche NOM    Generer le bloc markdown Environnement de travail
                      (Systeme) a inserer dans la fiche de l agent NOM
  --version           Afficher la version

Proprietaire : Vulcain (outil partage)
Version : 0.2.3-py
Statut : prepare
"""

import datetime
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys

try:
    import psutil
    PSUTIL = True
except ImportError:
    psutil = None
    PSUTIL = False

VERSION = "0.2.3-py"
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
    print("  --bloc-fiche NOM    Generer le bloc markdown Environnement de travail")
    print("                      (Systeme) a inserer dans la fiche de l agent NOM")
    print("  --version           Afficher la version")
    print("")
    print("Exemples:")
    print("  verifier-systeme.py")
    print("  verifier-systeme.py --format json")
    print("  verifier-systeme.py --format resume --detail complet")
    print("  verifier-systeme.py --enregistrer")
    print("  verifier-systeme.py --bloc-fiche cerberus")


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


def informations_ressources():
    """Ressources materielles : RAM totale/disponible (Mo), disque libre (Go),
    charge CPU (%). psutil en dependance douce (fallback -1 si absent)."""
    ram_totale = -1
    ram_dispo = -1
    charge = -1.0
    if PSUTIL:
        try:
            vm = psutil.virtual_memory()
            ram_totale = int(vm.total // (1024 * 1024))
            ram_dispo = int(vm.available // (1024 * 1024))
            charge = round(float(psutil.cpu_percent(interval=None)), 1)
        except Exception:
            pass
    disque_libre = -1.0
    try:
        usage = shutil.disk_usage(".")
        disque_libre = round(usage.free / (1024 ** 3), 1)
    except Exception:
        pass
    return {
        "ram_totale_mo": ram_totale,
        "ram_disponible_mo": ram_dispo,
        "disque_libre_go": disque_libre,
        "charge_cpu": charge,
    }


def extraire_version(texte):
    """Extrait le premier numero de version (ex: 'Python 3.14.4' -> '3.14.4')."""
    m = re.search(r"(\d+(?:\.\d+)+)", texte or "")
    return m.group(1) if m else "-"


def _routine_classeur():
    """Charger la routine centrale du classeur v1."""
    chemin = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "oracle", "fonctions", "classeur.py"))
    try:
        spec = importlib.util.spec_from_file_location("classeur_v1", chemin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (OSError, ImportError, AttributeError):
        return None


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
    res = informations_ressources()
    print("| Systeme | OS | %s | %s | - |" % (os_nom, version_os))
    print("| Systeme | Architecture | %s | - | - |" % arch)
    if res["ram_totale_mo"] >= 0:
        print("| Ressources | RAM | %d Mo total / %d Mo dispo | - | - |" % (
            res["ram_totale_mo"], res["ram_disponible_mo"]))
    if res["disque_libre_go"] >= 0:
        print("| Ressources | Disque libre | %.1f Go | - | - |" % res["disque_libre_go"])
    if res["charge_cpu"] >= 0:
        print("| Ressources | Charge CPU | %.1f %% | - | - |" % res["charge_cpu"])

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

    res = informations_ressources()
    donnees = {
        "systeme": {
            "os": os_nom,
            "version": version_os,
            "arch": arch,
        },
        "ressources": res,
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

    res = informations_ressources()
    print("**Systeme** : %s %s (%s)" % (os_nom, version_os, arch))
    if res["ram_totale_mo"] >= 0:
        print("**Ressources** : RAM %d Mo total / %d Mo dispo, disque %.1f Go libre, charge CPU %.1f %%" % (
            res["ram_totale_mo"], res["ram_disponible_mo"], res["disque_libre_go"], res["charge_cpu"]))
    print("**Shells** : Bash %s" % bash["version"])
    print("**Langages** : %s, %s" % (python["version"], node["version"]))
    print("**Outils** : Git %s" % git["version"])


def bloc_fiche(agent):
    """Genere le bloc markdown Environnement de travail (Systeme) a inserer
    dans la fiche de l agent (demande utilisateur 2026-08-16 : chaque fiche
    doit contenir les infos de l environnement reel pour ne jamais oublier
    les differences Windows vs Linux). Sortie ASCII strict + LF."""
    os_nom, version_os, arch = informations_systeme()
    bash = verifier_outil("bash")
    python = verifier_outil("python3")
    node = verifier_outil("node")
    git = verifier_outil("git")
    # racine du projet (AGENTS.md)
    base = os.path.abspath(__file__)
    for _ in range(8):
        base = os.path.dirname(base)
        if os.path.isfile(os.path.join(base, "AGENTS.md")):
            break
    racine = os.path.normpath(base)
    est_windows = (os_nom == "Windows")

    lignes = []
    lignes.append("## Environnement de travail (Systeme)")
    lignes.append("")
    lignes.append("> Environnement REEL detecte par verifier-systeme (--bloc-fiche).")
    lignes.append("> Je le verifie avant toute commande systeme : je suis sur %s, PAS sur Linux." % os_nom)
    lignes.append("")
    lignes.append("| Element | Valeur |")
    lignes.append("|---|---|")
    lignes.append("| **OS** | %s %s (%s) |" % (os_nom, version_os, arch))
    lignes.append("| **Shell** | Bash %s |" % extraire_version(bash["version"]))
    lignes.append("| **Python** | %s |" % extraire_version(python["version"]))
    lignes.append("| **Node.js** | %s |" % extraire_version(node["version"]))
    lignes.append("| **Git** | %s |" % extraire_version(git["version"]))
    lignes.append("| **Racine projet** | %s |" % racine)
    lignes.append("")
    lignes.append("**Differences Windows vs Linux a ne jamais oublier** :")
    lignes.append("")
    if est_windows:
        lignes.append("- Ce systeme est WINDOWS avec bash MSYS/Git Bash : les commandes sont POSIX (ls, mv, rm, cp, grep), jamais cmd.exe ni PowerShell.")
        lignes.append("- Les chemins ont DEUX formes : POSIX /z/analyste-in-console (commandes bash) et natif Z:\\analyste-in-console (outils/scripts Windows).")
        lignes.append("- Fins de ligne : LF OBLIGATOIRE (jamais CRLF) - un append sans corriger-fins-de-ligne introduit du CRLF.")
        lignes.append("- python3 est disponible (Python %s) : les outils du cerveau s executent avec python3." % extraire_version(python["version"]))
        lignes.append("- Les fichiers s ecrivent en ASCII strict : tout script temp passe par l entonnoir (protection de sortie LF + ASCII).")
    else:
        lignes.append("- Ce systeme est LINUX : chemins POSIX uniquement, bash natif.")
        lignes.append("- Fins de ligne : LF OBLIGATOIRE (jamais CRLF).")
        lignes.append("- python3 est disponible (Python %s) : les outils du cerveau s executent avec python3." % extraire_version(python["version"]))
        lignes.append("- Les fichiers s ecrivent en ASCII strict : tout script temp passe par l entonnoir.")
    lignes.append("")
    lignes.append("> Source : verifier-systeme --bloc-fiche %s (v%s)" % (agent, VERSION))
    return "\n".join(lignes)


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
    fichier_stockage = chemin_classeur("cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md")
    fichier_hist = chemin_classeur("cerveau-projet/agents/classeur-variables/historique/historique-modifications.md")

    if not os.path.exists(fichier_stockage):
        print("ERREUR: classeur introuvable: %s" % fichier_stockage)
        return 1

    date_jour = datetime.date.today().isoformat()
    nouvelle_valeur = valeur_profil()
    nouvelle_ligne = "| `profil-systeme` | %s | verifier-systeme | %s | [OK] |" % (
        nouvelle_valeur, date_jour)

    # --- Lecture de l'ancienne valeur via la routine centrale ---
    classeur = _routine_classeur()
    if classeur is None:
        print("ERREUR: routine centrale du classeur introuvable")
        return 1
    lignes, _ = classeur.lire_fichier(
        fichier_stockage, "profil-systeme", "verifier-systeme", "oracle", "session-admin")
    if lignes is None:
        print("ERREUR: lecture du classeur impossible: %s" % fichier_stockage)
        return 1
    ancienne_valeur = "(aucune)"
    for ligne in lignes:
        if "`profil-systeme`" in ligne:
            debut = ligne.find("| `profil-systeme` | ")
            if debut >= 0:
                reste = ligne[debut + len("| `profil-systeme` | "):]
                ancienne_valeur = reste.split(" | verifier-systeme")[0].strip()
            break

    # --- Mise a jour du tableau de stockage via la routine centrale ---
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
    if not classeur.ecrire_lignes(
            fichier_stockage, resultat, "profil-systeme", "verifier-systeme",
            "oracle", "session-admin",
            ancienne_valeur=ancienne_valeur,
            nouvelle_valeur=nouvelle_valeur,
            raison="Mise a jour du profil systeme utilisateur"):
        print("ERREUR: ecriture du classeur refusee par la routine centrale")
        return 1

    print("[OK] Profil systeme enregistre dans le classeur-variables")
    print("Variable : profil-systeme")
    print("Valeur   : %s" % nouvelle_valeur)
    print("Source   : verifier-systeme")
    return 0


def main(argv):
    format_sortie = "table"
    detail = "standard"
    enregistrer = False
    agent_bloc = None

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
        elif arg == "--bloc-fiche":
            if i + 1 < len(argv):
                agent_bloc = argv[i + 1]
                i += 1
            else:
                print("Option --bloc-fiche requiert un nom d agent")
                return 1
        else:
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        i += 1

    if enregistrer:
        return enregistrer_profil()

    if agent_bloc:
        print(bloc_fiche(agent_bloc))
        return 0

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
