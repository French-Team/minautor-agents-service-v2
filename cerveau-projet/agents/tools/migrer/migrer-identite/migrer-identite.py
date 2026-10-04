#!/usr/bin/env python3
# -*- coding: ascii -*-
# migrer-identite.py
# Migrer les fichiers vers le schema hybride v0.2.0 de detecter-impacts
# (bloc identite: type/appartient_a/commun dans chaque fichier du cerveau).
# Version : 0.2.3
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# MIGRER-IDENTITE - MIGRATION VERS LE SCHEMA HYBRIDE v0.2.0
# ============================================================
# Objectif : ajouter le bloc identite a tous les fichiers d'un dossier
# (par defaut agents/tools/), selon le format adapte au type :
#   .md  -> frontmatter YAML en tete (--- / identite: / ---)
#   .py/.sh -> bloc de commentaires dans les 12 premieres lignes
#   .json -> cle top-level "identite"
# Idempotent : si le bloc est deja present, le fichier est saute (skip).
# Options : --dry-run (afficher sans ecrire), --liste (lister les cibles),
#           --racine (dossier source, defaut agents/tools/),
#           --appartient-a (defaut commun), --commun (defaut true),
#           --force (reinserer meme si present).
# Exclusions par defaut : outil-template.* et les tests/*.sh (perimetre
# decision utilisateur), __pycache__.
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom de l'outil doit commencer par le
# prefixe du dossier de categorie (migrer/ -> migrer-identite).
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python (aucune dependance externe).
# REGLE IMMUABLE : ASCII strict (aucun accent ni caractere Unicode).
# ============================================================

"""
migrer-identite.py
migrer-identite

Usage:
  migrer-identite.py [OPTIONS]
"""

import argparse
import json
import os
import sys
from pathlib import Path

VERSION = "0.2.3"
STATUT = "ebauche"

# Chemin racine par defaut : le dossier agents/tools/ du cerveau-projet.
_RACINE_DEFAUT = Path(__file__).resolve().parent.parent.parent.parent

_TYPES_PAR_DOSSIER = {
    "spec": "spec",
    "combos": "combo",
    "tester": "outil",
}

_NOMS_SPECIAUX = {
    "catalogue-commandes.json": "outil",
    "exemple-combo.json": "combo",
}


def _type_pour(chemin: Path, racine: Path) -> str:
    """Determine le type identite d'un fichier selon son role (v0.2.0 :
    extension a tout le cerveau - racine, classeur, pense-bete, template, note)."""
    nom = chemin.name
    # Templates : priorite sur tout (fiche-agent-template, spec-template, etc.)
    if nom.startswith("outil-template") or nom == "template-test.md":
        return "outil"
    if "-template" in nom:
        return "template"
    # Racine du projet / journal des activations
    if nom == "AGENTS.md":
        return "racine"
    if nom == "AGENTS-historique.md":
        return "historique"
    # Specs dans un sous-dossier spec/
    if "spec" in chemin.parts:
        return "spec"
    # Tests d'outils (decision utilisateur 2026-08-08) : les fichiers
    # tester-* sont des tests, type dedie 'test' (priorite sur tout :
    # un tester- dans combos/ est un test, pas un combo).
    if nom.startswith("tester-"):
        return "test"
    # Combos : UNIQUEMENT les definitions (definition-combo.json) dans un
    # dossier combos/. Les outils du dossier combos/ (combos-moteur,
    # combos-audit-general, combos-corriger-non-ascii, combos-valider-cerveau)
    # sont des OUTILS, pas des combos (correction v0.2.2 : la regle v0.2.1
    # 'combos in chemin.parts' etait trop large).
    if nom == "definition-combo.json":
        return "combo"
    if nom.startswith("combos-"):
        return "outil"
    if nom in _NOMS_SPECIAUX:
        return _NOMS_SPECIAUX[nom]
    # Classeur de variables
    if "classeur-variables" in chemin.parts:
        return "classeur"
    # Pense-betes (regles, conventions, specs, templates)
    if "pense-betes" in chemin.parts:
        return "pense-bete"
    # Document de note (missions, resumes, priorites) -> appartient au dossier
    if chemin.suffix == ".md" and not _dans_outils(chemin, racine):
        return "note"
    return "outil"


def _dans_outils(chemin: Path, racine: Path) -> bool:
    """Vrai si le fichier vit dans un dossier agents/tools/ (perimetre outil)."""
    rel = chemin.relative_to(racine).as_posix() if _dans_racine(chemin, racine) else chemin.as_posix()
    return "/agents/tools/" in rel or rel.startswith("agents/tools/")


def _dans_racine(chemin: Path, racine: Path) -> bool:
    try:
        chemin.relative_to(racine)
        return True
    except ValueError:
        return False


def _bloc_identite_py_sh(type_id: str, appartient_a: str, commun: bool) -> str:
    """Construit le bloc commentaires # identite: pour .py/.sh."""
    lignes = [
        "# identite:",
        "#   type: " + type_id,
        "#   appartient_a: " + appartient_a,
        "#   commun: " + ("true" if commun else "false"),
    ]
    return "\n".join(lignes) + "\n"


def _bloc_identite_md(type_id: str, appartient_a: str, commun: bool) -> str:
    """Construit le frontmatter YAML pour .md."""
    return (
        "---\n"
        "identite:\n"
        "  type: " + type_id + "\n"
        "  appartient_a: " + appartient_a + "\n"
        "  commun: " + ("true" if commun else "false") + "\n"
        "---\n"
    )


def _bloc_identite_json(type_id: str, appartient_a: str, commun: bool) -> dict:
    """Construit le dict identite pour .json."""
    return {
        "identite": {
            "type": type_id,
            "appartient_a": appartient_a,
            "commun": commun,
        }
    }


def _position_identite_py_sh(lignes: list):
    """Retourne l indice du bloc '# identite:' (ou -1) dans les 30 premieres lignes."""
    for i, l in enumerate(lignes[:30]):
        if l.strip().startswith("# identite:"):
            return i
    return -1


def _a_identite_py_sh(lignes: list) -> bool:
    """Vrai si un bloc '# identite:' est present dans les 12 premieres lignes."""
    return 0 <= _position_identite_py_sh(lignes) < 12


def _a_identite_md(lignes: list) -> bool:
    """Vrai si un frontmatter avec 'identite:' est present en tete."""
    if not lignes or lignes[0].strip() != "---":
        return False
    for l in lignes[1:15]:
        if l.strip().startswith("identite:"):
            return True
    return False


def _a_frontmatter_md(lignes: list) -> bool:
    """Vrai si un frontmatter '---' est present en tete (avec ou sans identite).

    Un frontmatter existant SANS identite est un fichier special (test,
    template, doc de test) : on ne colle JAMAIS un 2e frontmatter par-dessus.
    """
    return bool(lignes) and lignes[0].strip() == "---"


def _exclu(chemin: Path, racine: Path) -> bool:
    """Vrai si le fichier doit etre exclu du perimetre (decisions utilisateur)."""
    nom = chemin.name
    rel = chemin.relative_to(racine).as_posix() if _dans_racine(chemin, racine) else chemin.as_posix()
    if "__pycache__" in rel:
        return True
    # Traces historisees (decision utilisateur) : rapports dates figes
    # (controles de Janus, rapports de Themis, retro-actions de Vulcain)
    # qui ne seront jamais a jour -> on ne leur ajoute pas d'identite.
    for trace in ("controles/", "rapports/", "retro-actions/"):
        if trace in "/" + rel:
            return True
    # Dossiers hors perimetre (decision utilisateur, v0.2.1) :
    # - exemples/ : fichiers de test volontairement pollues (accents,
    #   emojis) - jamais a migrer
    # - recherches-web/ : resultats de recherches, pas des fichiers du cerveau
    # - sauvegardes/ : artefacts de sauvegarde (test_mission_*.json)
    for hors in ("exemples/", "recherches-web/", "sauvegardes/"):
        if hors in "/" + rel:
            return True
    # Templates exclus (decision utilisateur)
    if nom == "outil-template.py" or nom == "outil-template.sh" or nom == "outil-template.md":
        return True
    # Template de test exclu
    if nom == "template-test.md":
        return True
    # Tests exclus (decision utilisateur) : fichiers .sh ET .md dans un
    # dossier tests/ (le frontmatter custom des docs de test est preserve).
    if "/tests/" in "/" + rel:
        return True
    return False


def _migrer_py_sh(contenu: str, type_id: str, appartient_a: str, commun: bool) -> str:
    """Insere (ou replace) le bloc identite dans un .py/.sh.

    - Retire un bloc '# identite:' existant, ou qu'il soit (evite le doublon).
    - Insere apres l'en-tete court (shebang, coding, nom, version, statut),
      en s'arretant a la 1re ligne vide OU au 1er non-# : le bloc doit etre
      dans les 12 premieres lignes (convention detecter-impacts).
    """
    lignes = contenu.split("\n")
    # 1. Retirer un bloc existant (4 lignes) ou qu'il soit.
    gardees = []
    i = 0
    while i < len(lignes):
        if lignes[i].strip().startswith("# identite:"):
            i += 4  # sauter le bloc identite (identite + 3 champs)
            continue
        gardees.append(lignes[i])
        i += 1
    lignes = gardees
    # 2. Trouver la position d'insertion : apres l'en-tete court.
    #    Rechercher d'abord la ligne '# Statut' (ou '# Version' sinon)
    #    dans les 12 premieres lignes : c'est la fin de l'en-tete de
    #    nommage. Fallback : 1re ligne vide ou 1er non-#.
    pos = -1
    for i in range(min(12, len(lignes))):
        l = lignes[i].strip()
        if l.startswith("# Statut") or l.startswith("# statut"):
            pos = i + 1
            break
    if pos < 0:
        for i in range(min(12, len(lignes))):
            l = lignes[i].strip()
            if l.startswith("# Version") or l.startswith("# version"):
                pos = i + 1
                break
    if pos < 0:
        pos = 0
        while pos < min(12, len(lignes)):
            l = lignes[pos]
            if l.strip() == "" or not l.startswith("#"):
                break
            pos += 1
    # Si le fichier commence directement par du code, inserer en tete.
    bloc = _bloc_identite_py_sh(type_id, appartient_a, commun)
    nouvelles = lignes[:pos] + [bloc.rstrip("\n")] + lignes[pos:]
    return "\n".join(nouvelles)


def _migrer_md(contenu: str, type_id: str, appartient_a: str, commun: bool) -> str:
    """Insere le frontmatter YAML en tete d'un .md."""
    bloc = _bloc_identite_md(type_id, appartient_a, commun)
    return bloc + contenu


def _migrer_json(contenu: str, type_id: str, appartient_a: str, commun: bool) -> str:
    """Ajoute la cle top-level identite a un .json."""
    try:
        data = json.loads(contenu)
    except json.JSONDecodeError as e:
        raise ValueError("JSON invalide: %s" % e)
    data["identite"] = {
        "type": type_id,
        "appartient_a": appartient_a,
        "commun": commun,
    }
    return json.dumps(data, ensure_ascii=True, indent=2) + "\n"


def _appartient_a_effectif(type_id: str, chemin: Path, defaut: str) -> str:
    """Calcule l'appartient_a reel selon le type (v0.2.0) :
    - note -> dossier parent (ex: agents/vulcain/mission-x.md -> vulcain)
    - racine/classeur/pense-bete/template -> commun
    - defaut (outil, spec, combo, ...) -> valeur passee (defaut commun)"""
    if type_id == "note":
        return chemin.parent.name
    if type_id in ("racine", "classeur", "pense-bete", "template", "historique"):
        return "commun"
    return defaut


def _migrer_fichier(chemin: Path, racine: Path, appartient_a: str,
                    commun: bool, dry_run: bool, force: bool) -> str:
    """Migre un fichier. Retourne: 'migre' | 'skip' | 'deja' | 'erreur'."""
    type_id = _type_pour(chemin, racine)
    appartient_a = _appartient_a_effectif(type_id, chemin, appartient_a)
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        return "erreur:lecture:%s" % e

    # Verifier presence selon le format
    lignes = contenu.split("\n")
    if chemin.suffix in (".py", ".sh"):
        pos_bloc = _position_identite_py_sh(lignes)
        if pos_bloc >= 0 and pos_bloc < 12 and not force:
            return "deja"
        if pos_bloc >= 12 and not force:
            # Bloc present mais HORS fenetre 12 lignes : a reparer
            # (deplacer sans doublon) pour rester lisible par
            # detecter-impacts.
            if dry_run:
                return "reparer(dry-run)"
            try:
                nouveau = _migrer_py_sh(contenu, type_id, appartient_a, commun)
            except Exception as e:
                return "erreur:insertion:%s" % e
            try:
                nouveau.encode("ascii")
            except UnicodeEncodeError:
                return "erreur:non-ascii"
            if nouveau == contenu:
                return "inchange"
            chemin.write_text(nouveau, encoding="utf-8", newline="")
            return "reparer"
        if dry_run:
            return "migre(dry-run)"
        try:
            nouveau = _migrer_py_sh(contenu, type_id, appartient_a, commun)
        except Exception as e:
            return "erreur:insertion:%s" % e
    elif chemin.suffix == ".md":
        deja = _a_identite_md(lignes)
        if deja and not force:
            return "deja"
        # Frontmatter existant sans identite : fichier special (test,
        # template, doc de test) -> ne jamais coller un 2e frontmatter.
        if not force and _a_frontmatter_md(lignes):
            return "ignore:frontmatter-sans-identite"
        if dry_run:
            return "migre(dry-run)"
        try:
            nouveau = _migrer_md(contenu, type_id, appartient_a, commun)
        except Exception as e:
            return "erreur:insertion:%s" % e
    elif chemin.suffix == ".json":
        deja = "identite" in json.loads(contenu) if _json_valide(contenu) else False
        if deja and not force:
            return "deja"
        if dry_run:
            return "migre(dry-run)"
        try:
            nouveau = _migrer_json(contenu, type_id, appartient_a, commun)
        except Exception as e:
            return "erreur:insertion:%s" % e
    else:
        return "ignore"

    # Verification ASCII strict avant ecriture
    try:
        nouveau.encode("ascii")
    except UnicodeEncodeError:
        return "erreur:non-ascii"
    if chemin.read_text(encoding="utf-8") == nouveau:
        return "inchange"
    chemin.write_text(nouveau, encoding="utf-8", newline="")
    return "migre"


def _json_valide(contenu: str) -> bool:
    try:
        json.loads(contenu)
        return True
    except json.JSONDecodeError:
        return False


def _collecter(racine: Path) -> list:
    """Collectionne les fichiers .py/.sh/.md/.json (hors exclusions)."""
    fichiers = []
    for ext in (".py", ".sh", ".md", ".json"):
        for f in racine.rglob("*" + ext):
            if f.is_file() and not _exclu(f, racine):
                fichiers.append(f)
    return sorted(fichiers)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrer les fichiers vers le schema hybride v0.2.0 "
                    "(bloc identite dans chaque fichier).")
    parser.add_argument("--racine", default=str(_RACINE_DEFAUT),
                        help="dossier a migrer (defaut: agents/tools/)")
    parser.add_argument("--dry-run", action="store_true",
                        help="afficher sans ecrire")
    parser.add_argument("--liste", action="store_true",
                        help="lister les fichiers a migrer sans rien faire")
    parser.add_argument("--appartient-a", default="commun",
                        help="valeur appartient_a (defaut: commun)")
    parser.add_argument("--commun", default="true",
                        choices=["true", "false"],
                        help="valeur commun (defaut: true)")
    parser.add_argument("--force", action="store_true",
                        help="reinserer meme si le bloc est deja present")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = Path(args.racine)
    if not racine.is_dir():
        print("ERREUR: dossier introuvable: %s" % racine)
        return 1

    commun = args.commun == "true"
    fichiers = _collecter(racine)

    if args.liste:
        print("=== FICHIERS A MIGRER (%d) ===\n" % len(fichiers))
        for f in fichiers:
            rel = f.relative_to(racine).as_posix()
            print("  %s -> %s" % (rel, _type_pour(f, racine)))
        print("\nTotal: %d fichiers" % len(fichiers))
        return 0

    nb_migre = nb_deja = nb_ignore = nb_erreur = 0
    for f in fichiers:
        res = _migrer_fichier(f, racine, args.appartient_a, commun,
                              args.dry_run, args.force)
        rel = f.relative_to(racine).as_posix()
        if res == "migre":
            nb_migre += 1
            print("  [MIGRE] %s" % rel)
        elif res == "migre(dry-run)":
            nb_migre += 1
            print("  [DRY-RUN] %s -> serait migre (type: %s)" % (rel, _type_pour(f, racine)))
        elif res == "deja":
            nb_deja += 1
            print("  [DEJA]  %s" % rel)
        elif res == "reparer":
            nb_migre += 1
            print("  [REPARE] %s" % rel)
        elif res == "reparer(dry-run)":
            nb_migre += 1
            print("  [REPARE-DRY] %s -> bloc deplace dans les 12 premieres lignes" % rel)
        elif res == "inchange":
            nb_deja += 1
            print("  [INCHANGE] %s" % rel)
        elif res.startswith("ignore"):
            nb_ignore += 1
            if res != "ignore":
                print("  [IGNORE] %s (%s)" % (rel, res))
        else:
            nb_erreur += 1
            print("  [ERREUR] %s (%s)" % (rel, res))

    mode = "DRY-RUN" if args.dry_run else "REEL"
    print("\n=== RAPPORT (%s) ===" % mode)
    print("  Migres:       %d" % nb_migre)
    print("  Deja presents:%d" % nb_deja)
    print("  Ignores:      %d" % nb_ignore)
    print("  Erreurs:      %d" % nb_erreur)
    print("  Total:        %d" % len(fichiers))
    return 1 if nb_erreur else 0


if __name__ == "__main__":
    sys.exit(main())
