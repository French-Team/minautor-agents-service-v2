#!/bin/bash
# migrer-identite.sh
# Migrer les fichiers vers le schema hybride v0.2.0 de detecter-impacts
# (bloc identite: type/appartient_a/commun dans chaque fichier du cerveau).
# Version : 0.2.3
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# Portage bash : ce script verifie le nommage puis execute le
# code Python embarque ci-dessous (heredoc). Le code est
# IDENTIQUE a migrer-identite.py (parite stricte py/sh).
# La racine par defaut est transmise via l'environnement.
# ============================================================

# Verifier le nommage de ce script avant toute chose
NOM_SCRIPT="$(basename "$0")"
DOSSIER="$(basename "$(dirname "$0")")"
if [[ "$NOM_SCRIPT" != "$DOSSIER"* ]]; then
    echo "ERREUR: nommage invalide - $NOM_SCRIPT ne commence pas par $DOSSIER-" >&2
    exit 1
fi

# Racine par defaut : dossier agents/tools/ du cerveau-projet
export MIGRER_IDENTITE_RACINE_DEFAUT="$(cd "$(dirname "$0")/../../../.." && pwd)"

# Embarquer le code Python (parite stricte avec le .py)
python3 - "$@" <<'PYEOF'
import json
import os
import sys
from pathlib import Path

VERSION = "0.2.3"
STATUT = "ebauche"

_RACINE_DEFAUT = Path(os.environ.get(
    "MIGRER_IDENTITE_RACINE_DEFAUT",
    str(Path(__file__).resolve().parent.parent.parent.parent) if "__file__" in dir() else "."
))

_NOMS_SPECIAUX = {
    "catalogue-commandes.json": "outil",
    "exemple-combo.json": "combo",
}


def _dans_racine(chemin, racine):
    try:
        chemin.relative_to(racine)
        return True
    except ValueError:
        return False


def _dans_outils(chemin, racine):
    rel = chemin.relative_to(racine).as_posix() if _dans_racine(chemin, racine) else chemin.as_posix()
    return "/agents/tools/" in rel or rel.startswith("agents/tools/")


def _type_pour(chemin, racine):
    nom = chemin.name
    if nom.startswith("outil-template") or nom == "template-test.md":
        return "outil"
    if "-template" in nom:
        return "template"
    if nom == "AGENTS.md":
        return "racine"
    if nom == "AGENTS-historique.md":
        return "historique"
    if "spec" in chemin.parts:
        return "spec"
    if nom.startswith("tester-"):
        return "test"
    if nom == "definition-combo.json":
        return "combo"
    if nom.startswith("combos-"):
        return "outil"
    if nom in _NOMS_SPECIAUX:
        return _NOMS_SPECIAUX[nom]
    if "classeur-variables" in chemin.parts:
        return "classeur"
    if "pense-betes" in chemin.parts:
        return "pense-bete"
    if chemin.suffix == ".md" and not _dans_outils(chemin, racine):
        return "note"
    return "outil"


def _bloc_identite_py_sh(type_id, appartient_a, commun):
    lignes = [
        "# identite:",
        "#   type: " + type_id,
        "#   appartient_a: " + appartient_a,
        "#   commun: " + ("true" if commun else "false"),
    ]
    return "\n".join(lignes) + "\n"


def _bloc_identite_md(type_id, appartient_a, commun):
    return (
        "---\n"
        "identite:\n"
        "  type: " + type_id + "\n"
        "  appartient_a: " + appartient_a + "\n"
        "  commun: " + ("true" if commun else "false") + "\n"
        "---\n"
    )


def _bloc_identite_json(type_id, appartient_a, commun):
    return {
        "identite": {
            "type": type_id,
            "appartient_a": appartient_a,
            "commun": commun,
        }
    }


def _position_identite_py_sh(lignes):
    for i, l in enumerate(lignes[:30]):
        if l.strip().startswith("# identite:"):
            return i
    return -1


def _a_identite_py_sh(lignes):
    return 0 <= _position_identite_py_sh(lignes) < 12


def _a_identite_md(lignes):
    if not lignes or lignes[0].strip() != "---":
        return False
    for l in lignes[1:15]:
        if l.strip().startswith("identite:"):
            return True
    return False


def _a_frontmatter_md(lignes):
    """Vrai si un frontmatter '---' est present en tete (avec ou sans identite)."""
    return bool(lignes) and lignes[0].strip() == "---"


def _json_valide(contenu):
    try:
        json.loads(contenu)
        return True
    except json.JSONDecodeError:
        return False


def _exclu(chemin, racine):
    nom = chemin.name
    rel = chemin.relative_to(racine).as_posix() if _dans_racine(chemin, racine) else chemin.as_posix()
    if "__pycache__" in rel:
        return True
    for trace in ("controles/", "rapports/", "retro-actions/"):
        if trace in "/" + rel:
            return True
    for hors in ("exemples/", "recherches-web/", "sauvegardes/"):
        if hors in "/" + rel:
            return True
    if nom == "outil-template.py" or nom == "outil-template.sh" or nom == "outil-template.md":
        return True
    if nom == "template-test.md":
        return True
    if "/tests/" in "/" + rel:
        return True
    return False


def _migrer_py_sh(contenu, type_id, appartient_a, commun):
    lignes = contenu.split("\n")
    gardees = []
    i = 0
    while i < len(lignes):
        if lignes[i].strip().startswith("# identite:"):
            i += 4
            continue
        gardees.append(lignes[i])
        i += 1
    lignes = gardees
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
    bloc = _bloc_identite_py_sh(type_id, appartient_a, commun)
    nouvelles = lignes[:pos] + [bloc.rstrip("\n")] + lignes[pos:]
    return "\n".join(nouvelles)


def _migrer_md(contenu, type_id, appartient_a, commun):
    bloc = _bloc_identite_md(type_id, appartient_a, commun)
    return bloc + contenu


def _migrer_json(contenu, type_id, appartient_a, commun):
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


def _appartient_a_effectif(type_id, chemin, defaut):
    if type_id == "note":
        return chemin.parent.name
    if type_id in ("racine", "classeur", "pense-bete", "template", "historique"):
        return "commun"
    return defaut


def _migrer_fichier(chemin, racine, appartient_a, commun, dry_run, force):
    type_id = _type_pour(chemin, racine)
    appartient_a = _appartient_a_effectif(type_id, chemin, appartient_a)
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        return "erreur:lecture:%s" % e

    lignes = contenu.split("\n")
    if chemin.suffix in (".py", ".sh"):
        pos_bloc = _position_identite_py_sh(lignes)
        if pos_bloc >= 0 and pos_bloc < 12 and not force:
            return "deja"
        if pos_bloc >= 12 and not force:
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

    try:
        nouveau.encode("ascii")
    except UnicodeEncodeError:
        return "erreur:non-ascii"
    if chemin.read_text(encoding="utf-8") == nouveau:
        return "inchange"
    chemin.write_text(nouveau, encoding="utf-8", newline="")
    return "migre"


def _collecter(racine):
    fichiers = []
    for ext in (".py", ".sh", ".md", ".json"):
        for f in racine.rglob("*" + ext):
            if f.is_file() and not _exclu(f, racine):
                fichiers.append(f)
    return sorted(fichiers)


def main():
    import argparse
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
PYEOF
