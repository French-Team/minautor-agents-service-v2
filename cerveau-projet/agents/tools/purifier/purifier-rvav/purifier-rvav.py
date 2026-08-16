#!/usr/bin/env python3
# -*- coding: ascii -*-
# purifier-rvav.py
#
# Purification RVAV (etape 5 du workflow) : reduire les fichiers surcharges
# SANS JAMAIS SUPPRIMER D INFORMATION. Les lecons/entrees les plus anciennes
# sont DEPLACEES vers un fichier d archive cote a cote.
#
# Principe (decision utilisateur 2026-08-15) : le protocole rvav-workflow etait
# abandone et perime. Besoins listes par Buffy (spec-purification-rvav.md) :
#   - corrections.md d agent (lecons ## [LECON]) : quota 1000 lignes, archive
#     dans <agent>-historique.md
#   - AGENTS-historique.md (entrees | 2026-) : quota 800 lignes, archive dans
#     AGENTS-historique-archive.md
#   - fiches agents (template) et protocoles : signaler seulement
#
# Options :
#   --tous                  Purifier tous les fichiers en surcharge (scan
#                           fichier courant + AGENTS-historique.md)
#   --agent <nom>           Purifier les corrections.md d un agent
#   --fichier <chemin>      Purifier un fichier precis
#   --seuil <n>             Seuil de lignes (defaut 1000 corrections / 800 hist)
#   --dry-run               Mode par defaut : afficher le plan sans rien modifier
#   --executer              Appliquer reellement (TOUJOURS apres un dry-run valide)
#   --rapport <fichier>     Ecrire le plan de purification en markdown
#   --verbose               Detail par fichier
#   --version               Afficher la version
#   --aide, -h              Afficher cette aide
#
# Usage:
#   python3 purifier-rvav.py --tous --dry-run --rapport plan.md
#   python3 purifier-rvav.py --agent janus --dry-run
#   python3 purifier-rvav.py --agent janus --executer
#   python3 purifier-rvav.py --fichier AGENTS-historique.md --executer
#
# Retour: 0 si tout va bien (ou dry-run sans probleme), 1 si des fichiers
# restent en surcharge ou erreur, 2 usage invalide.
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (purifier-).
# =============================================================================
import argparse
import io
import os
import sys

VERSION = "0.1.0"
STATUT = "ebauche"

SEUIL_CORRECTIONS = 1000
SEUIL_HISTORIQUE = 800

# Couleurs ANSI (desactivees si la sortie n est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""


def trouver_racine():
    """Trouve la racine du projet (la ou AGENTS.md existe)."""
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            sys.stderr.write("ERREUR : racine du projet introuvable (AGENTS.md absent).\n")
            sys.exit(2)
        courant = parent


def compter_lignes(chemin):
    """Compte le nombre de lignes d un fichier."""
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def lire(chemin):
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def ecrire(chemin, contenu):
    """Ecrit en LF pur + ASCII strict (garantie projet)."""
    contenu = contenu.replace("\r\n", "\n").replace("\r", "\n")
    with io.open(chemin, "w", encoding="ascii", errors="strict", newline="\n") as f:
        f.write(contenu)


def decouper_frontmatter(lignes):
    """Separe le frontmatter YAML (--- ... ---) du corps. Retourne (frontmatter, corps)."""
    if not lignes or lignes[0].strip() != "---":
        return [], lignes
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            return lignes[: i + 1], lignes[i + 1 :]
    return [], lignes


def decouper_lecons(corps):
    """Decoupe le corps en blocs de lecons (## [LECON] ... jusqu a la suivante)."""
    lecons = []
    courant = None
    reste = []
    for ligne in corps:
        if ligne.startswith("## [LECON]"):
            if courant is not None:
                lecons.append(courant)
            courant = [ligne]
        elif courant is not None:
            courant.append(ligne)
        else:
            reste.append(ligne)
    if courant is not None:
        lecons.append(courant)
    return lecons, reste


def decouper_entrees_historique(corps):
    """Decoupe AGENTS-historique en blocs d entrees (| 2026- ... jusqu a la suivante)."""
    entrees = []
    courant = None
    reste = []
    for ligne in corps:
        if ligne.startswith("| 2026-"):
            if courant is not None:
                entrees.append(courant)
            courant = [ligne]
        elif courant is not None:
            courant.append(ligne)
        else:
            reste.append(ligne)
    if courant is not None:
        entrees.append(courant)
    return entrees, reste


def calculer_archivage(blocs, lignes_avant, seuil):
    """Calcule combien de blocs (du plus ancien, index 0) archiver pour que le
    fichier passe sous le seuil. Retourne (nb_a_archiver, lignes_apres_estimees).
    On archive TANT QUE le fichier reste au-dessus du seuil (et on garde
    toujours au moins un bloc)."""
    taille_blocs = [len(b) for b in blocs]
    total = lignes_avant
    nb = 0
    while nb < len(taille_blocs) - 1 and total > seuil:
        total -= taille_blocs[nb]
        nb += 1
    return nb, total


def cible_purification(racine, args):
    """Retourne la liste des fichiers a purifier : (chemin, type, seuil)."""
    cibles = []
    if args.agent:
        chemin = os.path.join(racine, "cerveau-projet", "agents", args.agent,
                              "corrections.md")
        if not os.path.isfile(chemin):
            print(RED + "[ERREUR] corrections.md introuvable pour l agent %s : %s"
                  % (args.agent, chemin) + NC)
            sys.exit(2)
        cibles.append((chemin, "corrections", args.seuil or SEUIL_CORRECTIONS))
    if args.fichier:
        chemin = args.fichier
        if not os.path.isabs(chemin):
            chemin = os.path.join(racine, chemin)
        if not os.path.isfile(chemin):
            print(RED + "[ERREUR] fichier introuvable : %s" % chemin + NC)
            sys.exit(2)
        if os.path.basename(chemin) == "AGENTS-historique.md":
            cibles.append((chemin, "historique", args.seuil or SEUIL_HISTORIQUE))
        else:
            cibles.append((chemin, "corrections", args.seuil or SEUIL_CORRECTIONS))
    if args.tous:
        agents_dir = os.path.join(racine, "cerveau-projet", "agents")
        for nom in sorted(os.listdir(agents_dir)):
            chemin = os.path.join(agents_dir, nom, "corrections.md")
            if os.path.isfile(chemin):
                cibles.append((chemin, "corrections", SEUIL_CORRECTIONS))
        hist = os.path.join(racine, "AGENTS-historique.md")
        if os.path.isfile(hist):
            cibles.append((hist, "historique", SEUIL_HISTORIQUE))
    vus = set()
    uniques = []
    for c in cibles:
        if c[0] not in vus:
            vus.add(c[0])
            uniques.append(c)
    return uniques


def nom_archive(chemin, type_fichier):
    """Nom du fichier d archive cote a cote."""
    dossier = os.path.dirname(chemin)
    base = os.path.basename(chemin)
    if type_fichier == "historique":
        return os.path.join(dossier, "AGENTS-historique-archive.md")
    if base == "corrections.md":
        agent = os.path.basename(os.path.dirname(chemin))
        return os.path.join(dossier, agent + "-historique.md")
    return chemin + ".archive.md"


def en_tete_archive(chemin, type_fichier):
    """En-tete du fichier d archive."""
    base = os.path.basename(chemin)
    if type_fichier == "historique":
        titre = "Archive des entrees historiques -- AGENTS-historique"
    else:
        agent = os.path.basename(os.path.dirname(chemin))
        titre = "Archive des lecons -- %s" % agent
    return [
        "---",
        "identite:",
        "  type: archive",
        "  appartient_a: commun",
        "  commun: true",
        "---",
        "# %s" % titre,
        "",
        "> Archive creee par purifier-rvav : les blocs les plus anciens de",
        "> %s y sont deplaces (principe anti-perte : rien n est supprime)." % base,
        "",
        "---",
        "",
    ]


def nettoyer_lignes_vides(lignes):
    """Supprime les lignes vides consecutives (max 1)."""
    resultat = []
    precedent_vide = False
    for l in lignes:
        vide = (l.strip() == "")
        if vide and precedent_vide:
            continue
        resultat.append(l)
        precedent_vide = vide
    return resultat


def purifier_fichier(chemin, type_fichier, seuil, dry_run, verbose, rapport_lignes):
    """Analyse un fichier et retourne le plan (ou l applique si not dry_run)."""
    lignes_avant = compter_lignes(chemin)
    if lignes_avant <= seuil:
        if verbose:
            print(GREEN + "[OK] %s : %d lignes (sous le seuil %d)"
                  % (os.path.basename(chemin), lignes_avant, seuil) + NC)
        return 0, lignes_avant, lignes_avant, 0

    lignes = lire(chemin).split("\n")
    frontmatter, corps = decouper_frontmatter(lignes)

    if type_fichier == "historique":
        blocs, reste = decouper_entrees_historique(corps)
    else:
        blocs, reste = decouper_lecons(corps)

    if not blocs:
        print(YELLOW + "[ATTENTION] %s : %d lignes mais aucun bloc structurable a archiver"
              % (os.path.basename(chemin), lignes_avant) + NC)
        return 1, lignes_avant, lignes_avant, 0

    nb, lignes_apres = calculer_archivage(blocs, lignes_avant, seuil)
    if nb == 0:
        print(YELLOW + "[ATTENTION] %s : %d lignes, aucun bloc archivable"
              % (os.path.basename(chemin), lignes_avant) + NC)
        return 1, lignes_avant, lignes_avant, 0

    archives = blocs[:nb]
    gardes = blocs[nb:]

    archive_chemin = nom_archive(chemin, type_fichier)
    nb_lignes_archive = sum(len(b) for b in archives)

    print("")
    print(BLUE + "=== %s (%s) : %d lignes > seuil %d ==="
          % (os.path.basename(chemin), type_fichier, lignes_avant, seuil) + NC)
    print("  a archiver : %d blocs (%d lignes) -> %s"
          % (nb, nb_lignes_archive, os.path.basename(archive_chemin)))
    print("  apres purification : ~%d lignes" % lignes_apres)

    if not dry_run:
        # Construire les 2 contenus EN MEMOIRE d abord
        lignes_gardees = [l for bloc in gardes for l in bloc]
        corps_garde = lignes_gardees[:]
        if reste:
            corps_garde = reste + corps_garde
        nouveau = frontmatter + corps_garde
        nouveau = nettoyer_lignes_vides(nouveau)
        contenu_principal = "\n".join(nouveau).rstrip("\n") + "\n"

        en_tete = en_tete_archive(chemin, type_fichier)
        lignes_archive = [l for bloc in archives for l in bloc]

        # ACCUMULATION ANTI-PERTE : si l archive existe deja, les nouveaux
        # blocs (plus anciens) sont PREFIXES devant le contenu existant
        # (lecon Vulcain 2026-08-15 : une 2e purification avait ECRASE
        # l archive et perdu 5 lecons).
        if os.path.isfile(archive_chemin):
            ancien = lire(archive_chemin).rstrip("\n").split("\n")
            en_tete_ancien, corps_ancien = decouper_frontmatter(ancien)
            if en_tete_ancien:
                contenu_archive = "\n".join(en_tete_ancien + lignes_archive + corps_ancien).rstrip("\n") + "\n"
            else:
                contenu_archive = "\n".join(en_tete + lignes_archive + corps_ancien).rstrip("\n") + "\n"
        else:
            contenu_archive = "\n".join(en_tete + lignes_archive).rstrip("\n") + "\n"

        # GARANTIE ANTI-PERTE : ecrire l ARCHIVE EN PREMIER (si l archive
        # echoue, le fichier principal reste intact - lecon Vulcain 2026-08-15
        # : un plantage entre les 2 ecritures avait perdu 5 lecons).
        ecrire(archive_chemin, contenu_archive)
        ecrire(chemin, contenu_principal)

        apres = compter_lignes(chemin)
        print(GREEN + "  [EXECUTE] %d lignes -> %d lignes (archive : %s)"
              % (lignes_avant, apres, os.path.basename(archive_chemin)) + NC)
        if apres > seuil:
            print(RED + "  [KO] fichier encore au-dessus du seuil (%d > %d)"
                  % (apres, seuil) + NC)
            return 1, lignes_avant, apres, nb
        return 0, lignes_avant, apres, nb

    if rapport_lignes is not None:
        rapport_lignes.append(
            "- %s : %d lignes -> ~%d lignes (%d blocs archives vers %s)"
            % (os.path.basename(chemin), lignes_avant, lignes_apres, nb,
               os.path.basename(archive_chemin)))
    return 0, lignes_avant, lignes_apres, nb


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="purifier-rvav.py",
        description="Purification RVAV : reduire les fichiers surcharges sans perte (deplacement vers archive).",
        add_help=False,
    )
    parser.add_argument("--tous", action="store_true",
                        help="Purifier tous les fichiers en surcharge")
    parser.add_argument("--agent", metavar="NOM",
                        help="Purifier les corrections.md d un agent")
    parser.add_argument("--fichier", metavar="CHEMIN",
                        help="Purifier un fichier precis")
    parser.add_argument("--seuil", type=int, default=None,
                        help="Seuil de lignes (defaut 1000 corrections / 800 historique)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Mode par defaut : afficher le plan sans modifier")
    parser.add_argument("--executer", action="store_true",
                        help="Appliquer reellement (apres un dry-run valide)")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="Ecrire le plan de purification en markdown")
    parser.add_argument("--verbose", action="store_true", help="Detail")
    parser.add_argument("--version", action="store_true", help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true", help="Afficher cette aide")
    return parser


def main():
    parser = construire_parser()
    args = parser.parse_args()

    if args.version:
        print("purifier-rvav %s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        parser.print_help()
        return 0
    if not (args.tous or args.agent or args.fichier):
        parser.print_help()
        return 2

    racine = trouver_racine()
    cibles = cible_purification(racine, args)
    if not cibles:
        print(YELLOW + "Aucun fichier a purifier." + NC)
        return 0

    dry_run = not args.executer
    if dry_run:
        print(YELLOW + "[DRY-RUN] Aucun changement applique (utilisez --executer)." + NC)

    rapport_lignes = []
    nb_problemes = 0
    for chemin, type_fichier, seuil in cibles:
        p, avant, apres, nba = purifier_fichier(chemin, type_fichier, seuil,
                                                dry_run, args.verbose, rapport_lignes)
        nb_problemes += p

    if args.rapport and rapport_lignes:
        with io.open(args.rapport, "w", encoding="ascii", newline="\n") as f:
            f.write("# Rapport de purification RVAV\n\n")
            f.write("Date : 2026-08-15\n")
            f.write("Mode : %s\n" % ("dry-run" if dry_run else "execute"))
            f.write("\n## Plan\n\n")
            f.write("\n".join(rapport_lignes) + "\n")
        print(GREEN + "Rapport ecrit : %s" % args.rapport + NC)

    print("")
    if nb_problemes == 0:
        print(GREEN + "=== VERDICT : OK (%d fichier(s) traite(s), %s) ==="
              % (len(cibles), "plan dry-run" if dry_run else "execute") + NC)
        return 0
    print(RED + "=== VERDICT : %d fichier(s) avec probleme ===" % nb_problemes + NC)
    return 1


if __name__ == "__main__":
    sys.exit(main())
