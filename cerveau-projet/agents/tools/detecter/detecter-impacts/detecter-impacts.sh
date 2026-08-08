#!/bin/bash
# detecter-impacts.sh
# Detecte les fichiers impliques par la modification d'un fichier du cerveau.
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# DETECTER-IMPACTS (parite avec detecter-impacts.py)
# ============================================================
# Le bash pose la variable DETECTER_IMPACTS_RACINE (le code python
# embarque ne doit PAS utiliser __file__ en mode stdin - lecon
# guider-parcours/generateurs-case) puis transmet les arguments
# par python3 - "$@".
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : dossier 'detecter/' -> prefixe 'detecter-'
# ============================================================

VERSION="0.2.1"
STATUT="ebauche"

# Racine du projet : remonte de detecter-impacts -> detecter -> tools
# -> agents -> cerveau-projet -> racine (5 niveaux depuis le DOSSIER)
export DETECTER_IMPACTS_RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

executer_python() {
    python3 - "$@" << 'PYEOF'
import argparse
import os
import sys
from pathlib import Path

VERSION = "0.2.1"
STATUT = "ebauche"

_IGNORES = {".git", "__pycache__", "node_modules", ".venv", "venv"}
_EXTENSIONS = {".md", ".py", ".sh", ".json", ".txt"}

# TRACES HISTORISEES (decision utilisateur) : les fichiers des dossiers
# controles/, rapports/ et retro-actions/ sont des traces datees figees
# (rapports de controle, comptes rendus, bilans). Elles ne seront JAMAIS
# 'a jour' : elles sont listees dans le rapport mais exclues du verdict
# (marqueur [HISTORISE], pas de comptage dans 'potentiellement non a
# jour'). Distinction reference vivante vs trace historisee.
_TRACES_HISTORISEES = {"controles", "rapports", "retro-actions"}


def chemin_racine():
    env = os.environ.get("DETECTER_IMPACTS_RACINE")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[4]


def lire_identite(chemin):
    """Lit l identite dans les 3 formats : .md frontmatter YAML, .py/.sh commentaires, .json cle top-level."""
    try:
        texte = chemin.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    suffixe = chemin.suffix.lower()

    if suffixe == ".json":
        try:
            import json
            donnees = json.loads(texte)
        except (ValueError, TypeError):
            return None
        if not isinstance(donnees, dict):
            return None
        identite = donnees.get("identite")
        if not isinstance(identite, dict):
            return None
        return {str(k).strip(): str(v).strip().strip('"').strip("'") for k, v in identite.items()}

    lignes = texte.splitlines()
    if suffixe in (".py", ".sh"):
        # identite en commentaires : une ligne contenant identite: puis lignes # type:/appartient_a:/commun:
        # CONTRAINTE DE CONVENTION : le bloc identite doit etre dans les 12 premieres lignes
        # (en tete du fichier, juste apres l en-tete de nommage) - evite les faux positifs
        # quand un en-tete documentaire plus bas mentionne identite: (exemple : ce fichier).
        identite = {}
        dans_identite = False
        for ligne in lignes[:12]:
            s = ligne.strip()
            if not s:
                continue
            if not s.startswith("#"):
                if dans_identite:
                    break
                continue
            contenu = s.lstrip("#").strip()
            if contenu == "identite:" or contenu.startswith("identite:"):
                dans_identite = True
                continue
            if dans_identite and contenu.startswith(("type:", "appartient_a:", "commun:")):
                cle, _, val = contenu.partition(":")
                identite[cle.strip()] = val.strip().strip('"').strip("'")
        return identite if identite else None

    # .md : frontmatter YAML entre --- et ---
    if not lignes or lignes[0].strip() != "---":
        return None
    fin = None
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            fin = i
            break
    if fin is None:
        return None
    bloc = lignes[1:fin]
    identite = {}
    dans_identite = False
    for ligne in bloc:
        s = ligne.strip()
        if not s or s.startswith("#"):
            continue
        if s == "identite:":
            dans_identite = True
            continue
        if dans_identite and s.startswith(("type:", "appartient_a:", "commun:")):
            cle, _, val = s.partition(":")
            identite[cle.strip()] = val.strip().strip('"').strip("'")
    if not identite:
        return None
    return identite


def scanner(racine):
    resultats = []
    for chemin in racine.rglob("*"):
        if not chemin.is_file():
            continue
        if any(part in _IGNORES for part in chemin.parts):
            continue
        if chemin.suffix.lower() in _EXTENSIONS:
            resultats.append(chemin)
    return sorted(resultats)


def reference_le_fichier(contenu, cible):
    base = cible.name
    sans_ext = cible.stem
    return (base in contenu) or (sans_ext in contenu)


def est_trace_historisee(chemin):
    """Vrai si le fichier vit dans un dossier de traces historisees
    (controles/, rapports/, retro-actions/) : traces datees figees qui
    ne seront jamais mises a jour."""
    return any(part in _TRACES_HISTORISEES for part in chemin.parts)


def statut_implique(implique, modifie):
    try:
        if implique.stat().st_mtime >= modifie.stat().st_mtime:
            return "A JOUR"
        return "NON MIS A JOUR"
    except OSError:
        return "INDISPONIBLE"


def trouver_impliques(modifie, identite, racine):
    commun = str(identite.get("commun", "false")).strip().lower() in ("true", "oui", "1", "yes")
    appartient = identite.get("appartient_a", "").strip().lower()

    # Resolution des chemins des 2 cotes (relatif vs absolu) avant comparaison
    modifie_abs = modifie.resolve()
    impliques = []
    for fichier in scanner(racine):
        if fichier.resolve() == modifie_abs:
            continue
        if commun:
            try:
                contenu = fichier.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if reference_le_fichier(contenu, modifie):
                if est_trace_historisee(fichier):
                    impliques.append((fichier, "reference", "HISTORISE"))
                else:
                    statut = statut_implique(fichier, modifie)
                    impliques.append((fichier, "reference", statut))
        else:
            ident = lire_identite(fichier)
            if ident and str(ident.get("appartient_a", "")).strip().lower() == appartient:
                if est_trace_historisee(fichier):
                    impliques.append((fichier, "identification", "HISTORISE"))
                else:
                    statut = statut_implique(fichier, modifie)
                    impliques.append((fichier, "identification", statut))
    return impliques


def afficher_rapport(modifie, identite, impliques, verbose):
    print("=== Detecter-impacts v%s === (Statut : %s)" % (VERSION, STATUT))
    print("Fichier modifie : %s" % modifie)
    if identite:
        print("Identite lue    : type=%s, appartient_a=%s, commun=%s"
              % (identite.get("type", "?"), identite.get("appartient_a", "?"),
                 identite.get("commun", "false")))
    print("")

    if not impliques:
        print("[OK] Aucun fichier implique trouve.")
        return 0

    print("=== Fichiers impliques (%d) ===" % len(impliques))
    non_a_jour = 0
    traces = 0
    for fichier, mode, statut in impliques:
        if statut == "HISTORISE":
            marqueur = "[HISTORISE]"
            traces += 1
        else:
            marqueur = "[NON MIS A JOUR]" if statut == "NON MIS A JOUR" else "[%s]" % statut
        print("  %s %s (%s)" % (marqueur, fichier, mode))
        if statut == "NON MIS A JOUR":
            non_a_jour += 1
    print("")
    print("=== Synthese ===")
    print("Impliques trouves : %d" % len(impliques))
    print("  dont traces historisees (exclues du verdict) : %d" % traces)
    print("Potentiellement non mis a jour : %d" % non_a_jour)
    if non_a_jour:
        print("VERDICT : des fichiers impliques sont plus anciens que la modification.")
        print("  -> verifier chacun et justifier (ou mettre a jour) avant de conclure.")
        return 1
    print("VERDICT : tous les fichiers impliques sont a jour (ou plus recents).")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="detecter-impacts",
        description="Detecte les fichiers impliques par la modification d'un fichier du cerveau.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("fichier", type=str,
                        help="Chemin du fichier modifie (il doit porter un frontmatter identite:)")
    parser.add_argument("--racine", type=str, default=None,
                        help="Racine du scan (defaut : cerveau-projet du projet)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="detecter-impacts v%s" % VERSION)
    args = parser.parse_args()

    modifie = Path(args.fichier)
    if not modifie.is_file():
        print("ERREUR: fichier introuvable : %s" % modifie, file=sys.stderr)
        return 2
    modifie = modifie.resolve()

    identite = lire_identite(modifie)
    if not identite:
        print("ERREUR: aucune identite ('identite:') dans %s" % modifie, file=sys.stderr)
        print("  -> ce fichier n'est pas encore migre vers le schema d'identification.", file=sys.stderr)
        print("  -> ajouter le bloc identite: (voir detecter-impacts.md section Schema).", file=sys.stderr)
        return 2

    racine = Path(args.racine) if args.racine else chemin_racine()
    if not racine.is_dir():
        print("ERREUR: racine de scan introuvable : %s" % racine, file=sys.stderr)
        return 2

    if args.verbose:
        print("[verbose] racine de scan : %s" % racine)
    impliques = trouver_impliques(modifie, identite, racine)
    return afficher_rapport(modifie, identite, impliques, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
PYEOF
}

# Main
main() {
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[ERREUR] python3 est requis pour detecter-impacts.sh (parite avec le .py)"
        exit 1
    fi
    executer_python "$@"
}

main "$@"
