#!/usr/bin/env python3
# -*- coding: ascii -*-
# [nom-outil].py
# [Description courte de ce que fait l'outil]
# Version : 0.3.0-beta
# Statut : ebauche

# ============================================================
# OUTIL-TEMPLATE PYTHON - MODELE DE SCRIPT
# ============================================================
# Instructions d'utilisation de ce template :
#   1. Copier ce fichier vers agents/tools/[categorie]/[nom-outil]/[nom-outil].py
#      (categorie = dossier d'ACTION : ajouter, analyser, corriger, lister, ...)
#   2. Remplacer [nom-outil] par le nom reel de l'outil
#   3. Remplacer [Description courte] par la vraie description
#   4. Completer les fonctions selon le besoin
#   5. Remplir le modele de documentation [nom-outil].md (outil-template-python.md)
#   6. Ajouter l'outil dans index-tools.md
#   7. Assigner l'outil a l'agent concerne (protocole-outils Regle 6)
#   8. Tester en --dry-run avant toute utilisation
#   9. Valider la conformite ASCII avec valider-conformite-ascii
# ============================================================
# REGLE IMMUABLE DE NOMMAGE :
#   Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie.
#   Exemples : dossier 'rechercher/' -> outil 'rechercher-xxx'
#             dossier 'lire/'       -> outil 'lire-xxx'
#   La fonction verifier_nommage ci-dessous controle cela au demarrage.
#   (Ne pas supprimer ce bloc lors de la creation de l'outil)
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python
#   Aucune dependance externe (pip install) n'est autorisee.
#   Utiliser uniquement la bibliotheque standard : sys, os, pathlib,
#   argparse, re, io, json, subprocess, ...
# ============================================================
# REGLE IMMUABLE : ASCII strict
#   Aucun accent, emoji ou caractere Unicode dans le code ni les
#   commentaires. Utiliser uniquement des caracteres ASCII (0-127).
# ============================================================
# REGLE IMMUABLE : PROTECTIONS + OPTIONS ON/OFF + CHRONO
#   TOUT outil doit embarquer le triplet (protocole-outils Regle 9) :
#   1. PROTECTIONS : verifier_nommage, validation, --dry-run
#   2. OPTIONS on/off : --activer/--desactiver, --isoler N (isoler ou
#      desactiver une fonction / un workflow complet sans toucher au code)
#   3. CHRONO : option standard --chrono (mesure de duree, bilan en fin)
#   Les durees alimenteront les futurs outils de suivi.
# ============================================================
# REGLE IMMUABLE : MESSAGES INFORMATIONNELS (v0.3.0, demande utilisateur)
#   Les outils passent des MESSAGES contextuels aux agents dans leur sortie,
#   aux endroits importants : 'si vous avez modifie X, n oubliez pas Y'.
#   - afficher_messages_info(messages) affiche la section
#     '=== MESSAGES POUR L AGENT ===' avec une ligne ' > ' par message.
#   - L APPEL est OBLIGATOIRE en fin de main() (apres l action reussie) pour
#     TOUT outil qui ecrit/modifie dans le projet. Les messages sont TOUJOURS
#     affiches (pas une option) : c est le contrat informationnel.
#   - Chaque outil fournit SES messages statiques contextuels (fichiers
#     compagnons a mettre a jour, regles a respecter, etapes suivantes).
#   Exemple :
#     if not args.dry_run:
#         afficher_messages_info([
#             "fichier modifie : indexer dans index-tools.md",
#             "fichier modifie : adapter les tests (Morpheus)",
#         ])
#   NE PAS SUPPRIMER ce bloc ni la fonction afficher_messages_info lors de
#   la creation de l outil.
# ============================================================
# REGLE IMMUABLE : DOCUMENTATION OBLIGATOIRE (v0.2.0, demande utilisateur)
#   L agent doit LIRE le .md de l outil avant de l utiliser : le mode reel
#   (sans --dry-run) est BLOQUE tant que l agent n a pas passe --confirme-doc
#   (confirmation explicite de lecture de la documentation). La protection
#   verifie aussi que le .md du MEME dossier existe (un outil sans doc =
#   usage a risque, le contrat d utilisation n existe pas).
#   - --doc            : affiche le .md complet et sort (lecture directe)
#   - --confirme-doc   : confirme la lecture de la doc (requis en mode reel)
#   - sans --confirme-doc en mode reel : affiche la section Utilisation du
#     .md + message de refus, puis sort en erreur (code 2)
#   NE PAS SUPPRIMER ce bloc ni les fonctions verifier_doc_presente /
#   exiger_confirmation_doc lors de la creation de l outil.
# ============================================================

import argparse
import os
import sys
from pathlib import Path

VERSION = "0.3.0-beta"
STATUT = "ebauche"

# Couleurs ANSI (optionnel, activees uniquement si le terminal les supporte)
_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Retourne le texte colore si le terminal le supporte, sinon le texte brut."""
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def _doc_chemin(script_path):
    """Chemin du .md de documentation situe a cote du script (meme nom)."""
    p = Path(script_path)
    return p.with_suffix(".md")


def verifier_doc_presente(script_path):
    """PROTECTION DOC : verifie que le .md de documentation existe a cote du
    script. Un outil sans documentation = usage a risque (le contrat
    d utilisation n existe pas) : refus de fonctionner."""
    doc = _doc_chemin(script_path)
    if not doc.is_file():
        print(
            _couleur(
                "ERREUR: Documentation manquante : %s" % doc,
                "rouge",
            ),
            file=sys.stderr,
        )
        print("  Le .md de l outil est OBLIGATOIRE (regle immuable, protocole-outils).",
              file=sys.stderr)
        sys.exit(2)


def afficher_section_utilisation(doc):
    """Affiche la section Utilisation du .md (auto-affichage en cas de refus)."""
    try:
        texte = doc.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("[INFO] Impossible de lire le .md pour afficher la section Utilisation")
        return
    lignes = texte.splitlines()
    dans_usage = False
    for ligne in lignes:
        if ligne.strip().startswith("## "):
            dans_usage = ligne.strip().lower().startswith("## utilisation")
            continue
        if dans_usage and ligne.strip():
            print("  " + ligne.rstrip())


def exiger_confirmation_doc(script_path, dry_run, confirme_doc):
    """PROTECTION DOC : en mode reel (sans --dry-run), la lecture du .md doit
    etre confirmee par --confirme-doc. Sans confirmation : affiche la section
    Utilisation du .md + message de refus, puis sort en erreur (code 2).

    L agent lit TOUJOURS la sortie de la commande : l auto-affichage de la
    doc au refus garantit qu il voit le contrat avant de relancer."""
    if dry_run:
        return  # le dry-run est le mode de decouverte, libre
    if confirme_doc:
        return  # l agent a confirme la lecture de la documentation
    doc = _doc_chemin(script_path)
    verifier_doc_presente(script_path)
    print(_couleur("=== DOCUMENTATION OBLIGATOIRE ===", "jaune"))
    print("  Cet outil exige la lecture de sa documentation avant usage reel.")
    print("  Section Utilisation de %s :" % doc.name)
    print("")
    afficher_section_utilisation(doc)
    print("")
    print(_couleur("REFUS: relancez avec --confirme-doc apres lecture de la doc.", "rouge"),
          file=sys.stderr)
    sys.exit(2)


def afficher_messages_info(messages):
    """MESSAGES INFORMATIONNELS (regle immuable v0.3.0) : affiche une section
    '=== MESSAGES POUR L AGENT ===' avec une ligne ' > ' par message.

    A appeler en fin de main() apres une action reussie (et non dry-run)
    pour tout outil qui ecrit/modifie dans le projet. Les messages sont
    TOUJOURS affiches : l agent voit les consequences de son action
    (fichiers compagnons, regles, etapes suivantes) sans avoir a les
    deviner."""
    if not messages:
        return
    print("")
    print(_couleur("=== MESSAGES POUR L AGENT ===", "jaune"))
    for message in messages:
        print("  > %s" % message)


def verifier_nommage(script_path):
    """VERIFIE que le nom du fichier commence par le prefixe du dossier de categorie.

    Exemple : agents/tools/rechercher/rechercher-texte/rechercher-texte.py
    -> dossier parent = 'rechercher-texte', prefixe attendu = 'rechercher-'

    Exception : le template lui-meme (outil-template) vit a la racine de tools/
    et n'a pas de prefixe de categorie -- la verification est sautee.
    """
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


def afficher_aide(parser):
    """Affiche l'aide de l'outil."""
    print("=== [nom-outil] v%s ===" % VERSION)
    print("")
    parser.print_help()


def construire_parser():
    """Construit le parseur d'arguments avec les options standard de l'outil."""
    parser = argparse.ArgumentParser(
        prog="[nom-outil]",
        description="[Description courte de ce que fait l'outil]",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="[nom-outil] v%s" % VERSION)
    parser.add_argument("--chrono", action="store_true", help="Mesurer la duree d execution (bilan en fin)")
    parser.add_argument("--doc", action="store_true",
                        help="Afficher le .md de documentation complet et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation (requis en mode reel)")
    # --- Options specifiques de l'outil : ajouter ici ---
    # parser.add_argument("--option", type=str, help="Description de l'option")
    # --- Arguments positionnels de l'outil : ajouter ici ---
    # parser.add_argument("cible", type=str, help="Description de l'argument")
    return parser


def main():
    """Point d'entree principal de l'outil."""
    # Verifier la regle immuable de nommage
    verifier_nommage(sys.argv[0])

    # PROTECTION DOC (regle immuable) : le .md doit exister
    verifier_doc_presente(sys.argv[0])

    parser = construire_parser()
    args = parser.parse_args()

    # --doc : afficher la documentation complete et sortir
    if getattr(args, "doc", False):
        doc = _doc_chemin(sys.argv[0])
        print(doc.read_text(encoding="utf-8"))
        return 0

    # PROTECTION DOC : le mode reel exige --confirme-doc (lecture du .md)
    exiger_confirmation_doc(sys.argv[0], getattr(args, "dry_run", False),
                            getattr(args, "confirme_doc", False))

    # --- LOGIQUE DE L'OUTIL : implementer ici ---
    # if args.dry_run:
    #     print("[DRY-RUN] Aucune modification reelle")
    #     return 0
    #
    # resultat = faire_quelque_chose(args)
    # if resultat:
    #     print(_couleur("OK", "vert"))
    #     return 0
    # else:
    #     print(_couleur("ERREUR", "rouge"), file=sys.stderr)
    #     return 1

    # Placeholder : afficher l'aide si rien n'est implemente
    afficher_aide(parser)
    return 0


if __name__ == "__main__":
    sys.exit(main())
