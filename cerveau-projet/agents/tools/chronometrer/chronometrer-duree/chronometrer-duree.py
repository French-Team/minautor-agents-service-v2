#!/usr/bin/env python3
# -*- coding: ascii -*-
# chronometrer-duree.py
# Mesure la duree d une intervention d agent : demarrer au lancement de la
# mission, arreter au passage du relais (activation de l agent suivant ou
# reactivation de Cerberus). L etat est un journal JSONL
# (traces/chronos.jsonl) : une entree ouverte (sans date_fin) = chrono actif.
# Version : 0.1.2
# Statut : ebauche

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
# ============================================================
# REGLE IMMUABLE : DOCUMENTATION OBLIGATOIRE (v0.2.0, demande utilisateur)
#   L agent doit LIRE le .md de l outil avant de l utiliser : le mode reel
#   (sans --dry-run) est BLOQUE tant que l agent n a pas passe --confirme-doc
#   (confirmation explicite de lecture de la documentation).
#   - --doc            : affiche le .md complet et sort (lecture directe)
#   - --confirme-doc   : confirme la lecture de la doc (requis en mode reel)
# ============================================================

import argparse
import io
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

VERSION = "0.1.2"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def _doc_chemin(script_path):
    p = Path(script_path)
    return p.with_suffix(".md")


def verifier_doc_presente(script_path):
    doc = _doc_chemin(script_path)
    if not doc.is_file():
        print(_couleur("ERREUR: Documentation manquante : %s" % doc, "rouge"),
              file=sys.stderr)
        print("  Le .md de l outil est OBLIGATOIRE (regle immuable, protocole-outils).",
              file=sys.stderr)
        sys.exit(2)


def afficher_section_utilisation(doc):
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
    if dry_run:
        return
    if confirme_doc:
        return
    doc = _doc_chemin(script_path)
    verifier_doc_presente(script_path)
    print(_couleur("=== DOCUMENTATION OBLIGATOIRE ===", "jaune"))
    print("  Cet outil exige la lecture de sa documentation avant usage reel.")
    print("  Section Utilisation de %s :" % doc.name)
    print("")
    afficher_section_utilisation(doc)
    print("")
    print(_couleur("REFUS: relancez avec --confirme-doc apres lecture de la doc.",
                   "rouge"), file=sys.stderr)
    sys.exit(2)


def afficher_messages_info(messages):
    if not messages:
        return
    print("")
    print(_couleur("=== MESSAGES POUR L AGENT ===", "jaune"))
    for message in messages:
        print("  > %s" % message)


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(_couleur(
            "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
            % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


def afficher_aide(parser):
    print("=== chronometrer-duree v%s ===" % VERSION)
    print("")
    parser.print_help()


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="chronometrer-duree",
        description="Mesure la duree d une intervention d agent "
                    "(journal traces/chronos.jsonl).",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--tokens", type=str, default="",
                        help="JSON du snapshot tokens au demarrage "
                             "(ex: '{\"envoyes\":100,\"recus\":50}')")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans rien modifier")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="version",
                        version="chronometrer-duree v%s" % VERSION)
    parser.add_argument("--chrono", action="store_true",
                        help="Mesurer la duree d execution (bilan en fin)")
    parser.add_argument("--doc", action="store_true",
                        help="Afficher le .md de documentation complet et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation "
                             "(requis en mode reel)")
    parser.add_argument("action", nargs="?", default=None,
                        help="demarrer <session> <agent> | arreter <session> | etat")
    parser.add_argument("session", nargs="?", default=None,
                        help="session (ex: session-llm-1)")
    parser.add_argument("agent", nargs="?", default=None,
                        help="agent a chronometrer (demarrer)")
    return parser


# ---------------------------------------------------------------------------
# Logique du chronometre
# ---------------------------------------------------------------------------

def chemin_chronos():
    env = os.environ.get("CHRONOS_FICHIER")
    if env:
        return env
    script = Path(__file__).resolve()
    # remonter de chronometrer/chronometrer-duree/ vers la racine projet
    # parents : [0]=chronometrer-duree [1]=chronometrer [2]=tools
    #           [3]=agents [4]=cerveau-projet
    racine = script.parents[4]  # .../cerveau-projet
    return os.path.join(str(racine), "agents", "traces", "chronos.jsonl")


def lire_chronos():
    if not os.path.isfile(chemin_chronos()):
        return []
    entrees = []
    with io.open(chemin_chronos(), encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                entrees.append(json.loads(ligne))
            except ValueError:
                continue
    return entrees


def ecrire_chronos(entrees):
    dossier = os.path.dirname(chemin_chronos())
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(chemin_chronos(), "w", encoding="utf-8", newline="\n") as fh:
        for e in entrees:
            fh.write(json.dumps(e, ensure_ascii=True) + "\n")


def chrono_actif(entrees, session=None):
    for e in reversed(entrees):
        if not e.get("date_fin"):
            if session is None or e.get("session") == session:
                return e
    return None


def chronos_actifs(entrees, session=None):
    """Tous les chronos ouverts (sans date_fin), filtres par session si
    fournie. Permet la coexistence de plusieurs sessions LLM : sans session,
    retourne UN chrono actif par session (le plus recent de chacune)."""
    actifs = {}
    for e in entrees:
        if e.get("date_fin"):
            continue
        if session is not None and e.get("session") != session:
            continue
        # garder le plus recent de chaque session (ordre croissant du fichier)
        actifs[e.get("session")] = e
    return list(actifs.values())


def formater_duree(secondes):
    secondes = int(round(secondes or 0))
    if secondes < 60:
        return "%ds" % secondes
    return "%dmin %ds" % (secondes // 60, secondes % 60)


def calculer_duree(entree):
    try:
        debut = datetime.strptime(entree["date_debut"], "%Y-%m-%d %H:%M:%S")
        fin = datetime.strptime(entree["date_fin"], "%Y-%m-%d %H:%M:%S")
    except (KeyError, ValueError):
        return 0
    return max(0, int((fin - debut).total_seconds()))


def main():
    verifier_nommage(sys.argv[0])
    verifier_doc_presente(sys.argv[0])

    parser = construire_parser()
    args = parser.parse_args()

    if getattr(args, "doc", False):
        doc = _doc_chemin(sys.argv[0])
        print(doc.read_text(encoding="utf-8"))
        return 0

    exiger_confirmation_doc(sys.argv[0], getattr(args, "dry_run", False),
                            getattr(args, "confirme_doc", False))

    t0 = time.monotonic()
    if not args.action:
        afficher_aide(parser)
        return 0

    messages = []
    if args.action == "demarrer":
        if not args.session or not args.agent:
            print(_couleur("ERREUR: demarrer <session> <agent> requis", "rouge"),
                  file=sys.stderr)
            return 1
        if args.dry_run:
            print("[DRY-RUN] demarrer %s %s (aucun changement)" % (args.session,
                                                                   args.agent))
            return 0
        entrees = lire_chronos()
        actif = chrono_actif(entrees, args.session)
        if actif is not None:
            actif["date_fin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            actif["duree_secondes"] = calculer_duree(actif)
            print("AVERTISSEMENT: chrono deja ouvert pour %s (%s) - ferme "
                  "(%s)" % (actif.get("agent"), actif.get("session"),
                            formater_duree(actif["duree_secondes"])))
        tokens_debut = {}
        if args.tokens:
            try:
                tokens_debut = json.loads(args.tokens)
                if not isinstance(tokens_debut, dict):
                    tokens_debut = {}
            except ValueError:
                tokens_debut = {}
        entrees.append({
            "date_debut": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "session": args.session,
            "agent": args.agent,
            "date_fin": None,
            "duree_secondes": None,
            "tokens_debut": tokens_debut or None,
        })
        ecrire_chronos(entrees)
        print("Chrono demarre : %s / %s" % (args.session, args.agent))
        messages.append("le chrono de %s tourne : arreter a la fin de la "
                        "mission (activer l agent suivant)" % args.agent)
        messages.append("duree affichee dans AGENTS-historique au passage du "
                        "relais (repere ###)")

    elif args.action == "arreter":
        if not args.session:
            print(_couleur("ERREUR: arreter <session> requis", "rouge"),
                  file=sys.stderr)
            return 1
        if args.dry_run:
            actif = chrono_actif(lire_chronos(), args.session)
            if actif is None:
                print("[DRY-RUN] AUCUN_CHRONO")
            else:
                print("[DRY-RUN] arreter %s : chrono de %s (aucun changement)"
                      % (args.session, actif.get("agent")))
            return 0
        entrees = lire_chronos()
        actif = chrono_actif(entrees, args.session)
        if actif is None:
            print("AUCUN_CHRONO")
            return 0
        actif["date_fin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        actif["duree_secondes"] = calculer_duree(actif)
        ecrire_chronos(entrees)
        duree = formater_duree(actif["duree_secondes"])
        # 3e champ : snapshot tokens de debut (utilise par activer-agent-
        # principal pour calculer la conso de l intervention par difference)
        tokens_debut = actif.get("tokens_debut") or {}
        if tokens_debut:
            print("%s | %s | %s" % (actif.get("agent", ""), duree,
                                     json.dumps(tokens_debut, ensure_ascii=True)))
        else:
            print("%s | %s" % (actif.get("agent", ""), duree))
        messages.append("duree de %s : %s (journal traces/chronos.jsonl)"
                        % (actif.get("agent"), duree))
        messages.append("activer-agent-principal ajoute la duree au repere "
                        "### de l entree de l agent dans AGENTS-historique")

    elif args.action == "etat":
        # COEXISTENCE MULTI-SESSIONS (2026-08-19) : etat <session> affiche
        # le chrono de CETTE session ; etat (sans session) affiche TOUS les
        # chronos actifs, une ligne par session (les sessions LLM peuvent
        # tourner en parallele).
        actifs = chronos_actifs(lire_chronos(), args.session)
        if not actifs:
            if args.session:
                print("Aucun chrono actif pour %s" % args.session)
            else:
                print("Aucun chrono actif")
        else:
            for e in actifs:
                print("Chrono actif : %s / %s (demarre %s)"
                      % (e.get("session"), e.get("agent"),
                         e.get("date_debut")))
        return 0

    else:
        print(_couleur("ERREUR: action inconnue '%s'" % args.action, "rouge"),
              file=sys.stderr)
        return 1

    if args.chrono:
        print("")
        print("[chrono] chronometrer-duree : %.2fs" % (time.monotonic() - t0))
    if messages:
        afficher_messages_info(messages)
    return 0


if __name__ == "__main__":
    sys.exit(main())
