#!/usr/bin/env python3
# -*- coding: ascii -*-
# editer-fichier-agents.py
# Edite les fiches des agents (.md) : ligne ou bloc structure par titre markdown,
# avec suppression, remplacement, insertion et correcteur ASCII integre.
# Version : 0.1.0-beta
# Statut : beta

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom du fichier doit commencer
# par le prefixe du dossier de categorie (editer-).
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python, ASCII strict (0-127).
# ============================================================

import argparse
import io
import os
import re
import sys
from pathlib import Path

VERSION = "0.1.0-beta"
STATUT = "beta"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(
            _couleur(
                "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                % (nom_fichier, prefixe),
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)


# ------------------------------------------------------------------
# Lecture du fichier avec detection du saut de ligne (LF/CRLF)
# ------------------------------------------------------------------
def lire_fichier(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as fh:
        brut = fh.read()
    nl = "\r\n" if "\r\n" in brut else "\n"
    lignes = brut.split(nl)
    # si le fichier se termine par un saut de ligne, split produit une
    # ligne vide finale qu'il faut conserver pour la reecriture
    return brut, lignes, nl


def ecrire_fichier(chemin, lignes, nl, backup, dry_run):
    if dry_run:
        return
    if backup:
        Path(str(chemin) + ".bak").write_text(
            "\n".join(lignes) + (nl if lignes and lignes[-1] == "" else ""),
            encoding="utf-8", newline="",
        )
    contenu = "\n".join(lignes)
    if lignes and lignes[-1] == "":
        contenu += nl
    with io.open(chemin, "w", encoding="utf-8", newline="") as fh:
        fh.write(contenu)


# ------------------------------------------------------------------
# Localisation des blocs delimites par un titre markdown
# ------------------------------------------------------------------
RE_TITRE = re.compile(r"^(#{1,6})\s+(.*)$")


def localiser_titres(lignes):
    """Retourne [(n_ligne, niveau, texte_titre)] pour chaque titre markdown."""
    resultats = []
    for i, l in enumerate(lignes):
        m = RE_TITRE.match(l.rstrip("\r"))
        if m:
            resultats.append((i, len(m.group(1)), m.group(2).strip()))
    return resultats


def trouver_bloc(lignes, titre):
    """Trouve le bloc commence par le titre (niveau quelconque) et retourne
    (debut, fin_exclue, niveau, titre_exact). fin_exclue = prochain titre de
    niveau <= niveau, ou fin de fichier."""
    titres = localiser_titres(lignes)
    for idx, (n_ligne, niveau, texte) in enumerate(titres):
        if texte == titre or texte.lower() == titre.lower():
            fin = len(lignes)
            for n2, niv2, _ in titres[idx + 1:]:
                if niv2 <= niveau:
                    fin = n2
                    break
            return n_ligne, fin, niveau
    return None


def trouver_ligne(lignes, numero):
    """Retourne l index (0-base) de la ligne numero (1-base), ou None."""
    if numero < 1 or numero > len(lignes):
        return None
    return numero - 1


# ------------------------------------------------------------------
# Correcteur ASCII : reutilise le dictionnaire de corriger-accents
# ------------------------------------------------------------------
def lire_dictionnaire():
    dico = (
        Path(__file__).resolve().parent.parent.parent
        / "corriger" / "corriger-dictionnaire-accents" / "corriger-dictionnaire-accents.txt"
    )
    replacements = []
    try:
        with dico.open(encoding="utf-8") as df:
            for line in df:
                line = line.rstrip("\n").rstrip("\r")
                if not line or line.startswith("#"):
                    continue
                if "|" in line:
                    accent, repl = line.split("|", 1)
                    if accent:
                        replacements.append((accent, repl))
    except OSError:
        pass
    return replacements


def corriger_ascii(lignes):
    """Applique le dictionnaire sur chaque ligne (ASCII strict attendu)."""
    replacements = lire_dictionnaire()
    total = 0
    for i, l in enumerate(lignes):
        for accent, repl in replacements:
            count = l.count(accent)
            if count > 0:
                lignes[i] = lignes[i].replace(accent, repl)
                total += count
    return total


# ------------------------------------------------------------------
# Actions d edition
# ------------------------------------------------------------------
def action_supprimer(lignes, debut, fin_exclue):
    """Supprime [debut, fin_exclue). Retourne les lignes resultantes."""
    return lignes[:debut] + lignes[fin_exclue:]


def action_remplacer(lignes, debut, fin_exclue, nouveau):
    """Remplace [debut, fin_exclue) par les lignes de 'nouveau'."""
    nouvelles = nouveau.split("\n")
    return lignes[:debut] + nouvelles + lignes[fin_exclue:]


def action_ajouter(lignes, index, nouveau, apres):
    """Insere 'nouveau' avant ou apres l index."""
    nouvelles = nouveau.split("\n")
    pos = index + 1 if apres else index
    return lignes[:pos] + nouvelles + lignes[pos:]


def main():
    verifier_nommage(sys.argv[0])

    parser = argparse.ArgumentParser(
        prog="editer-fichier-agents",
        description="Edite les fiches des agents : ligne ou bloc (titre markdown), supprimer/remplacer/ajouter, correcteur ASCII integre.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("fichier", type=str, help="Fichier .md de la fiche agent a editer")
    parser.add_argument("--ligne", type=int, default=None, help="Numero de ligne cible (1-base)")
    parser.add_argument("--bloc", type=str, default=None, help="Titre du bloc cible (ex: Historique)")
    parser.add_argument("--supprimer", action="store_true", help="Supprimer la ligne ou le bloc cible")
    parser.add_argument("--remplacer", type=str, default=None, help="Texte de remplacement (ligne ou bloc)")
    parser.add_argument("--ajouter", type=str, default=None, help="Texte a ajouter")
    parser.add_argument("--apres", action="store_true", help="Ajouter APRES la cible (sinon avant)")
    parser.add_argument("--ascii", action="store_true", help="Corriger les caracteres non-ASCII apres l edition")
    parser.add_argument("--backup", action="store_true", help="Creer une sauvegarde .bak avant")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="editer-fichier-agents v%s" % VERSION)
    args = parser.parse_args()

    chemin = Path(args.fichier)
    if not chemin.is_file():
        print(_couleur("[ERREUR] Fichier non trouve: %s" % args.fichier, "rouge"), file=sys.stderr)
        return 1

    if args.ligne is None and args.bloc is None:
        print(_couleur("[ERREUR] Indiquer --ligne N ou --bloc \"Titre\"", "rouge"), file=sys.stderr)
        return 1
    if args.ligne is not None and args.bloc is not None:
        print(_couleur("[ERREUR] Choisir --ligne OU --bloc, pas les deux", "rouge"), file=sys.stderr)
        return 1
    if not args.supprimer and args.remplacer is None and args.ajouter is None:
        print(_couleur("[ERREUR] Indiquer --supprimer, --remplacer <texte> ou --ajouter <texte>", "rouge"), file=sys.stderr)
        return 1
    if args.remplacer is not None and args.ajouter is not None:
        print(_couleur("[ERREUR] Choisir --remplacer OU --ajouter", "rouge"), file=sys.stderr)
        return 1

    brut, lignes, nl = lire_fichier(chemin)

    if args.bloc is not None:
        res = trouver_bloc(lignes, args.bloc)
        if res is None:
            print(_couleur("[ERREUR] Bloc non trouve: %s" % args.bloc, "rouge"), file=sys.stderr)
            return 1
        debut, fin_exclue, niveau = res
        cible_desc = "bloc '%s' (lignes %d-%d)" % (args.bloc, debut + 1, fin_exclue)
        if args.supprimer:
            lignes = action_supprimer(lignes, debut, fin_exclue)
        elif args.remplacer is not None:
            lignes = action_remplacer(lignes, debut, fin_exclue, args.remplacer)
        elif args.ajouter is not None:
            lignes = action_ajouter(lignes, debut - 1, args.ajouter, args.apres)
    else:
        index = trouver_ligne(lignes, args.ligne)
        if index is None:
            print(_couleur("[ERREUR] Ligne hors bornes: %d (fichier: %d lignes)" % (args.ligne, len(lignes)), "rouge"), file=sys.stderr)
            return 1
        cible_desc = "ligne %d" % args.ligne
        if args.supprimer:
            lignes = action_supprimer(lignes, index, index + 1)
        elif args.remplacer is not None:
            lignes = action_remplacer(lignes, index, index + 1, args.remplacer)
        elif args.ajouter is not None:
            lignes = action_ajouter(lignes, index, args.ajouter, args.apres)

    nb_ascii = 0
    if args.ascii:
        nb_ascii = corriger_ascii(lignes)

    if args.dry_run:
        print(_couleur("[DRY-RUN] Cible: %s" % cible_desc, "jaune"))
        if nb_ascii:
            print("  [ASCII] %d corrections non-ASCII detectees" % nb_ascii)
        print("[DRY-RUN] Aucune modification reelle")
        return 0

    ecrire_fichier(chemin, lignes, nl, args.backup, args.dry_run)

    action = "supprime" if args.supprimer else ("remplace" if args.remplacer is not None else "ajoute")
    print(_couleur("[OK] %s %s" % (action.capitalize(), cible_desc), "vert"))
    if nb_ascii:
        print(_couleur("[OK] %d caracteres non-ASCII corriges" % nb_ascii, "vert"))
    if args.backup:
        print("[INFO] Sauvegarde: %s.bak" % chemin)
    return 0


if __name__ == "__main__":
    sys.exit(main())
