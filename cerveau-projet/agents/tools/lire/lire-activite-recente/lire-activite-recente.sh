#!/bin/bash
# lire-activite-recente.sh
# Lire les N dernieres interventions des agents depuis l'historique
# (AGENTS-historique.md) au format condense : date | session | agent | action.
# Version : 0.1.1
# Statut : prepare
# Parite avec lire-activite-recente.py (meme comportement, memes resultats).

# Verifier le nommage (prefixe du dossier de categorie)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NOM_SCRIPT="$(basename "$0" .sh)"
DOSSIER="$(basename "$SCRIPT_DIR")"
PREFIXE="${DOSSIER%%-*}-"
if [[ "$NOM_SCRIPT" != "$PREFIXE"* ]]; then
    echo "ERREUR: Le nom '$NOM_SCRIPT' ne commence pas par le prefixe du dossier '$PREFIXE'" >&2
    exit 1
fi

# Transmettre tous les arguments au code python embarque
# NOTE : PAS de shebang ni de coding cookie en tete du heredoc python --
# ils cassent l'execution en mode stdin (python3 -). Meme pattern que
# guider-parcours.sh (production) : le heredoc commence par les imports.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NOM_PY="lire-activite-recente.py" python3 - "$@" <<'PYEOF'
import argparse
import os
import re
import sys

# NOTE : le nommage est deja verifie par le .sh (bash) avant le heredoc.
VERSION = "0.1.1"
STATUT = "prepare"
FICHIER_DEFAUT = "AGENTS-historique.md"

RE_BALISES = re.compile(r"<[^>]+>")


def nettoyer_balises(texte):
    """Retire les balises HTML (spans de couleur) d une cellule."""
    return RE_BALISES.sub("", texte).strip()

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-activite-recente.py",
        description="Lire les N dernieres interventions des agents (format condense).",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier historique (defaut: env AGENTS_HISTORIQUE ou AGENTS-historique.md)")
    parser.add_argument("--nombre", default=None,
                        help="Nombre d'entrees a afficher (defaut: 15)")
    parser.add_argument("--longueur", default=None,
                        help="Longueur max de l'action en caracteres (defaut: 100)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def extraire_entrees(fichier, nombre, longueur):
    """Extraire les N dernieres interventions (les plus recentes en premier).
    Format v0.1.1 : | agent | heure | date | session | raison | (la 1re
    cellule est un span colore ; la raison peut continuer en lignes '###>').
    Retourne la liste de tuples (date, session, agent, action) avec
    date = 'AAAA-MM-JJ HH:MM' (reconstituee) et action = raison complete."""
    entrees = []
    try:
        with open(fichier, encoding="utf-8", errors="replace") as f:
            lignes = [ligne.strip() for ligne in f]
        i = 0
        while i < len(lignes) and len(entrees) < nombre:
            l = lignes[i]
            if not l.startswith("| <span"):
                i += 1
                continue
            parties = l.split("|")
            if len(parties) < 6:
                i += 1
                continue
            agent = nettoyer_balises(parties[1])
            heure = parties[2].strip()
            date = parties[3].strip()
            session = parties[4].strip()
            raison = "|".join(parties[5:-1]).strip()
            # continuations '###>' : suite de la raison (meme entree)
            i += 1
            while i < len(lignes) and lignes[i].startswith("###>"):
                suite = lignes[i][4:].strip()
                if suite:
                    raison += " " + suite
                i += 1
            date_heure = (date + " " + heure).strip()
            action = raison if len(raison) <= longueur else raison[:longueur] + "..."
            entrees.append((date_heure, session, agent, action))
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return None
    return entrees


def main(argv=None):
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("lire-activite-recente.py v" + VERSION + " (" + STATUT + ")")
        return 0

    nombre = 15
    if args.nombre is not None:
        if not args.nombre.isdigit() or int(args.nombre) < 1:
            print(RED + "[ERREUR] --nombre doit etre un entier >= 1: " + args.nombre + NC)
            return 1
        nombre = int(args.nombre)

    longueur = 100
    if args.longueur is not None:
        if not args.longueur.isdigit() or int(args.longueur) < 1:
            print(RED + "[ERREUR] --longueur doit etre un entier >= 1: " + args.longueur + NC)
            return 1
        longueur = int(args.longueur)

    fichier = args.fichier or os.environ.get("AGENTS_HISTORIQUE") or FICHIER_DEFAUT
    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier historique non trouve: " + fichier + NC)
        print(YELLOW + "  Defaut: env AGENTS_HISTORIQUE ou " + FICHIER_DEFAUT + NC)
        return 1

    if args.verbose:
        print(BLUE + "[INFO] Fichier: " + fichier + NC)
        print(BLUE + "[INFO] " + str(nombre) + " entrees (action max " + str(longueur) + " caracteres)" + NC)
        print("---")

    entrees = extraire_entrees(fichier, nombre, longueur)
    if entrees is None:
        return 1

    if not entrees:
        print(YELLOW + "[INFO] Aucune intervention trouvee dans " + fichier + NC)
        return 0

    for date, session, agent, action in entrees:
        print("%s | %s | %s | %s" % (date, session, agent, action))

    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF
