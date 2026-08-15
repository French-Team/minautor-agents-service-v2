#!/usr/bin/env python3
# -*- coding: ascii -*-
# combos-maj-readme-massive.py
# Combo maj-readme-massive : GROSSE mise a jour conservative du README
# (analyse complete -> verifier -> maj -> correctifs de fond -> ASCII -> rapport)
# Proprietaire : Clio (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
combos-maj-readme-massive.py
combos-maj-readme-massive

Usage:
  combos-maj-readme-massive.py [OPTIONS]
"""

VERSION = "0.1.5"
STATUT = "prepare"

import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""

OUTILS = {
    "mettre-a-jour-readme": "cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-readme/mettre-a-jour-readme.py",
    "combos-analyse-projet": "cerveau-projet/agents/tools/combos/combos-analyse-projet/combos-analyse-projet.py",
    "valider-conformite-ascii": "cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py",
    "editer-fichier": "cerveau-projet/agents/tools/editer/editer-fichier/editer-fichier.py",
    "lire-fichier": "cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.py",
}


def verifier_nommage():
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        sys.exit(2)


def executer(racine, rel, args):
    p = Path(racine) / rel
    if not p.is_file():
        print(RED + "[ERREUR] Outil introuvable : " + str(p) + NC)
        return None
    try:
        proc = subprocess.run(
            [sys.executable, str(p)] + args,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except Exception as e:
        print(RED + "[ERREUR] Echec d'execution de " + str(p) + " : " + str(e) + NC)
        return None


def aligner_badges_header(racine):
    """Aligner tous les badges du header README (affichage + href) sur leurs
    sources de verite. Lecon Clio/Janus : le --maj corrige les tables mais
    pas les badges en dur du header, et le href pouvait rester obsolete
    (ex : affichage 128, lien 121).

    Badges dynamiques (sources de verite) :
      - Outils-N : compter_outils de combos-analyse-projet (compte reel)
      - Version-vX.Y.Z : fichier clio/version-readme.txt (maintenu par Clio)
      - Statut-X : fichier clio/statut-projet.txt (prepare/dev/stable)
    Badges statiques (Plateforme, Fait_avec, Langages) : le href est aligne
    sur l affichage si divergence (pas de source externe)."""
    readme = Path(racine) / "README.md"
    if not readme.is_file():
        print(YELLOW + "  [AVERT] README.md introuvable, badges header non corriges." + NC)
        return False
    texte = readme.read_text(encoding="utf-8", errors="replace")

    # --- sources de verite ---
    valeurs = {}

    # Outils : compter_outils (import dynamique, importlib requis : le nom
    # du module source contient des tirets - combos-analyse-projet.py)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "combos_analyse_projet",
            str(Path(racine) / "cerveau-projet" / "agents" / "tools" / "combos" / "combos-analyse-projet" / "combos-analyse-projet.py"),
        )
        analyse = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analyse)
        nb = sum(analyse.compter_outils(Path(racine)).values())
        valeurs["Outils"] = str(nb)
    except Exception as e:
        print(YELLOW + "  [AVERT] Source Outils indisponible : " + str(e) + NC)

    # Version : fichier clio/version-readme.txt (semver sans v, prefixe v)
    f_version = Path(racine) / "cerveau-projet" / "agents" / "clio" / "version-readme.txt"
    if f_version.is_file():
        v = f_version.read_text(encoding="utf-8", errors="replace").strip()
        if v:
            valeurs["Version"] = "v" + v
    else:
        print(YELLOW + "  [AVERT] Source Version introuvable : " + str(f_version) + NC)

    # Statut : fichier clio/statut-projet.txt
    f_statut = Path(racine) / "cerveau-projet" / "agents" / "clio" / "statut-projet.txt"
    if f_statut.is_file():
        s = f_statut.read_text(encoding="utf-8", errors="replace").strip()
        if s:
            valeurs["Statut"] = s
    else:
        print(YELLOW + "  [AVERT] Source Statut introuvable : " + str(f_statut) + NC)

    # --- aligner les badges dynamiques (affichage ET href) ---
    modifie = False
    for nom, valeur in valeurs.items():
        # motif : badge/Nom-<valeur>-<couleur>  (2 occurrences : affichage + href)
        motif = r"badge/" + re.escape(nom) + r"-([^?)]+)-([^?)]+)"
        def remplace(m, nom=nom, valeur=valeur):
            return "badge/" + nom + "-" + valeur + "-" + m.group(2)
        nouveau = re.sub(motif, remplace, texte)
        if nouveau != texte:
            modifie = True
            print(GREEN + "  [OK] Badge " + nom + " aligne : " + valeur + " (affichage + href)." + NC)
            texte = nouveau

    # --- badges statiques : aligner le href sur l affichage si divergence ---
    for nom in ["Plateforme", "Fait_avec", "Langages"]:
        occ = re.findall(r"badge/" + re.escape(nom) + r"-([^?)]+)-([^?)]+)", texte)
        if len(occ) == 2 and occ[0] != occ[1]:
            def remplace2(m, nom=nom, aff=occ[0]):
                return "badge/" + nom + "-" + aff[0] + "-" + m.group(2)
            nouveau = re.sub(r"badge/" + re.escape(nom) + r"-([^?)]+)-([^?)]+)", remplace2, texte)
            if nouveau != texte:
                modifie = True
                print(GREEN + "  [OK] Badge " + nom + " href aligne sur l affichage (" +
                      occ[0][0] + ")." + NC)
                texte = nouveau

    if modifie:
        readme.write_text(texte, encoding="utf-8", newline="")
        print(GREEN + "  [OK] Badges du header alignes (affichage + href)." + NC)
        return True
    print(GREEN + "  [OK] Badges du header deja a jour." + NC)
    return False



def bumper_version(racine):
    """Bumper la version mineure dans clio/version-readme.txt (Pattern version
    README, convention Clio) : semver X.Y.Z -> X.(Y+1).0 (jamais de patch pour
    une grosse MAJ). Retourne (ancienne, nouvelle) ou None si absent/invalide.
    Le README n est jamais touche ici : seule la SOURCE de verite est
    incrementee, le badge Version est aligne ensuite par aligner_badges_header."""
    f_version = Path(racine) / "cerveau-projet" / "agents" / "clio" / "version-readme.txt"
    if not f_version.is_file():
        print(YELLOW + "  [AVERT] Source Version introuvable, bump impossible : "
                       + str(f_version) + NC)
        return None
    v = f_version.read_text(encoding="utf-8", errors="replace").strip()
    parties = v.split(".")
    if len(parties) != 3 or not parties[1].isdigit():
        print(YELLOW + "  [AVERT] Version illisible (%r), bump annule." % v + NC)
        return None
    try:
        mineure = int(parties[1]) + 1
    except ValueError:
        print(YELLOW + "  [AVERT] Version illisible (%r), bump annule." % v + NC)
        return None
    nouvelle = "%s.%d.0" % (parties[0], mineure)
    f_version.write_text(nouvelle + "\n", encoding="utf-8", newline="")
    print(GREEN + "  [BUMP] Version README : " + v + " -> " + nouvelle
          + " (source version-readme.txt)." + NC)
    return (v, nouvelle)


def lire_version(racine):
    """Lire la version courante dans clio/version-readme.txt (ou None)."""
    f_version = Path(racine) / "cerveau-projet" / "agents" / "clio" / "version-readme.txt"
    if f_version.is_file():
        v = f_version.read_text(encoding="utf-8", errors="replace").strip()
        if v:
            return v
    return None

def verrouiller_habilitation(agent, outil, audit=False):
    """Verrou d habilitation : appelle proteger-verrou-habilitation et
    retourne (code, message). Le verrou lit les cartes de decision comme
    source de verite - aucune table en dur ici. audit=True (v0.2.0) : mode
    tests/preuves formelles - l identite reelle de la session n est pas
    verifiee (reserve aux tests ; en production jamais utilise)."""
    racine = Path.cwd()
    while not (racine / "AGENTS.md").is_file():
        if racine == racine.parent:
            return (2, "[ERREUR] Racine du projet introuvable (AGENTS.md absent)")
        racine = racine.parent
    verrou = racine / "cerveau-projet" / "agents" / "tools" / "proteger" / \
        "proteger-verrou-habilitation" / "proteger-verrou-habilitation.py"
    if not verrou.is_file():
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    cmd = [sys.executable, str(verrou), "--agent", agent, "--outil", outil]
    if audit:
        cmd.append("--audit")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    message = (r.stdout + r.stderr).strip()
    return (r.returncode, message)


def main():
    verifier_nommage()
    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-maj-readme-massive",
        description="Combo maj-readme-massive : grosse mise a jour conservative du README.",
    )
    parser.add_argument("racine", nargs="?", default=".", help="Racine du projet (defaut: .)")
    parser.add_argument("--agent", help="Nom de l agent appelant (OBLIGATOIRE, verrou d habilitation)")
    parser.add_argument("--audit", action="store_true",
                        help="Mode tests : verrou sans verification d identite reelle (reserve aux preuves formelles)")
    parser.add_argument("--rapport", action="store_true",
                        help="Sauvegarder le rapport dans clio/rapports/")
    parser.add_argument("--version", action="version",
                        version="combos-maj-readme-massive " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    # VERROU D HABILITATION (regle immuable : seul clio met a jour le README).
    # --agent est OBLIGATOIRE et le verrou est appele AVANT la moindre etape :
    # si l agent n est pas habilite, le combo refuse et le message indique QUI
    # est habilite (cycle Cerberus -> agent).
    if not args.agent:
        print("[ERREUR] --agent est OBLIGATOIRE : le combo doit connaitre "
              "l agent appelant (verrou d habilitation).")
        return 2
    code, message = verrouiller_habilitation(args.agent, "combos-maj-readme-massive",
                                             audit=args.audit)
    if code != 0:
        print(message)
        return 1 if code == 1 else 2

    racine = Path(args.racine)
    print(BLUE + "=== combos-maj-readme-massive v" + VERSION + " ===" + NC)
    print("Racine : " + str(racine.resolve()))
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    print(YELLOW + "MODE CONSERVATIF : la structure du README est conservee - on corrige "
                   "les compteurs, tables et badges, on ne refond pas les sections." + NC)
    print("")

    # Snapshot du README : detecter si le --maj a modifie le contenu (Pattern
    # version README : si le README change, la version est bumpee).
    chemin_readme = Path(racine) / "README.md"
    snapshot_readme = None
    if chemin_readme.is_file():
        snapshot_readme = chemin_readme.read_text(encoding="utf-8", errors="replace")

    etapes = []
    rapport = []
    bump_info = None
    version_avant = lire_version(racine)

    # Etape 1 : analyse complete
    print(BLUE + "--- Etape 1/5 : analyse complete (combos-analyse-projet) ---" + NC)
    r = executer(racine, OUTILS["combos-analyse-projet"], [])
    if r is None:
        return 1
    print(r)
    etapes.append("analyse")
    rapport.append("## Etape 1 - Analyse\n\n" + r + "\n")

    # Etape 2 : verifier
    print(BLUE + "--- Etape 2/5 : verifier (mettre-a-jour-readme --verifier) ---" + NC)
    r = executer(racine, OUTILS["mettre-a-jour-readme"], ["--verifier"])
    if r is None:
        return 1
    print(r)
    etapes.append("verifier")
    rapport.append("## Etape 2 - Verifier\n\n" + r + "\n")

    # Etape 3 : maj des compteurs
    print(BLUE + "--- Etape 3/5 : maj des compteurs (--maj) ---" + NC)
    r = executer(racine, OUTILS["mettre-a-jour-readme"], ["--maj"])
    if r is None:
        return 1
    print(r)
    etapes.append("maj")
    rapport.append("## Etape 3 - Maj compteurs\n\n" + r + "\n")

    # Etape 3b : bump de version si le README a change (Pattern version README).
    # Le README modifie par --maj (compteurs/agents/outils corriges) signifie une
    # nouvelle version : on incremente la source de verite AVANT aligner_badges_header
    # pour que le badge Version s aligne sur la NOUVELLE version.
    readme_actuel = None
    if chemin_readme.is_file():
        readme_actuel = chemin_readme.read_text(encoding="utf-8", errors="replace")
    if snapshot_readme is not None and readme_actuel != snapshot_readme:
        print(BLUE + "--- Etape 3b/5 : bump de version (README modifie) ---" + NC)
        bump_info = bumper_version(racine)
        if bump_info:
            etapes.append("bump")
            rapport.append("## Etape 3b - Bump version README\n\n"
                           "Version : " + bump_info[0] + " -> " + bump_info[1]
                           + " (bump auto car README modifie).\n")
        else:
            rapport.append("## Etape 3b - Bump version README\n\n"
                           "Aucun bump (source introuvable ou illisible).\n")
    else:
        print(GREEN + "  [OK] README inchange - pas de bump de version." + NC)

    # Etape 4 : correctifs de fond (tables, categories manquantes)
    print(BLUE + "--- Etape 4/5 : correctifs de fond (tables, categories, badge header) ---" + NC)
    print(YELLOW + "  Indice : verifier le resultat du --maj - si une NOUVELLE categorie est "
                   "absente de la table, inserer manuellement la ligne avec editer-fichier "
                   "(lecon Clio : --maj ne cree pas les nouvelles lignes de categories)." + NC)
    print(YELLOW + "  Le badge du header (Outils-N, affichage + href) est corrige "
                   "automatiquement ci-dessous." + NC)
    corrige_badge = aligner_badges_header(racine)
    etapes.append("correctifs")
    rapport.append("## Etape 4 - Correctifs de fond\n\n"
                   "Correctifs appliques manuellement (nouvelles categories, tables).\n"
                   "Badge header aligne automatiquement : " + str(corrige_badge) + "\n")

    # Etape 5 : ASCII
    print(BLUE + "--- Etape 5/5 : verification ASCII ---" + NC)
    r = executer(racine, OUTILS["valider-conformite-ascii"], ["README.md"])
    if r is None:
        return 1
    print(r)
    etapes.append("ascii")
    rapport.append("## Etape 5 - ASCII\n\n" + r + "\n")

    # Synthese
    print("")
    print(BLUE + "=== SYNTHESE ===" + NC)
    print("Etapes executees : " + ", ".join(etapes))
    if bump_info:
        print(GREEN + "Version README : " + bump_info[0] + " -> " + bump_info[1]
                      + " (bump auto, source version-readme.txt)." + NC)
    else:
        vv = version_avant or "inconnue"
        print("Version README : inchangee (" + vv + ").")
    print(GREEN + "Grosse MAJ conservative terminee. Verifier ensuite avec combos-analyse-projet "
                  "que le verdict passe a A JOUR." + NC)

    if args.rapport:
        rapport_dir = racine / "cerveau-projet" / "agents" / "clio" / "rapports"
        rapport_dir.mkdir(parents=True, exist_ok=True)
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        rapport_file = rapport_dir / ("maj-readme-massive-" + date + ".md")
        contenu = [
            "# Rapport de grosse MAJ du README -- " + date,
            "",
            "## Contexte",
            "- Combo utilise : combos-maj-readme-massive v" + VERSION,
            "- Mode : conservatif (structure conservee)",
            "- Version README : " + ((bump_info[0] + " -> " + bump_info[1]
                                      + " (bump auto)") if bump_info else
                                     ("inchangee (" + (version_avant or "inconnue") + ")")) ,
            "- Racine : " + str(racine.resolve()),
            "",
        ] + rapport
        rapport_file.write_text("\n".join(contenu) + "\n", encoding="utf-8", newline="")
        print("")
        print(GREEN + "Rapport sauvegarde : " + str(rapport_file) + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
