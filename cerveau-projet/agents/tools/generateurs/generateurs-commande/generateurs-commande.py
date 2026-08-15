#!/usr/bin/env python3
# -*- coding: ascii -*-
# generateurs-commande.py
# Genere une commande complexe a lancer, en posant une question par parametre.
# Version : 0.2.5
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# BUT
# ============================================================
# L agent ne compose plus lui-meme les commandes complexes avec
# parametres. Ce generateur pose une question par parametre,
# valide chaque reponse, puis compose la commande exacte a lancer,
# basee sur un catalogue de commandes deja ecrites, corrigees et
# validees (catalogue-commandes.json).
#
# Deux modes :
#   1. Interactif (defaut) : menu de choix de la commande, puis une
#      question par parametre, reponses lues sur l entree standard.
#   2. Non-interactif (--commande + --reponses) : reponses fournies
#      en une fois, utile pour les tests automatises.
#
# Usage :
#   python3 generateurs-commande.py --liste
#   python3 generateurs-commande.py
#   python3 generateurs-commande.py --commande activer-activer
#   python3 generateurs-commande.py --commande remplir-pense-bete --reponses "fichier=...;section=idee;contenu=Mon idee"
# ============================================================

import argparse
import json
import os
import re
import sys
from pathlib import Path

VERSION = "0.2.5"
STATUT = "ebauche"

# Couleurs ANSI (desactivees si la sortie n est pas un terminal)
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def _couleur(texte, nom="neutre"):
    couleurs = {
        "rouge": RED,
        "vert": GREEN,
        "jaune": YELLOW,
        "bleu": BLUE,
        "neutre": NC,
    }
    if not sys.stdout.isatty():
        return texte
    return couleurs.get(nom, NC) + texte + NC


def verifier_nommage(script_path):
    """VERIFIE que le nom du fichier commence par le prefixe du dossier."""
    chemin = Path(os.path.abspath(script_path))
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


def charger_catalogue(chemin_catalogue):
    """Charge le catalogue des commandes depuis le JSON."""
    if not os.path.isfile(chemin_catalogue):
        print(
            _couleur(
                "ERREUR: Catalogue introuvable : %s" % chemin_catalogue,
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        with open(chemin_catalogue, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        print(
            _couleur("ERREUR: Catalogue invalide : %s" % str(e), "rouge"),
            file=sys.stderr,
        )
        sys.exit(1)


def trouver_commande(catalogue, nom):
    """Retrouve une commande du catalogue par son nom."""
    for commande in catalogue.get("commandes", []):
        if commande.get("nom") == nom:
            return commande
    return None


def lister_commandes(catalogue):
    """Affiche la liste des commandes du catalogue."""
    print(_couleur("=== Commande %s ===" % "generateurs-commande", "bleu"))
    print(_couleur("Version : %s (Statut : %s)" % (VERSION, STATUT), "bleu"))
    print("")
    commandes = catalogue.get("commandes", [])
    if not commandes:
        print("Aucune commande dans le catalogue.")
        return
    print(_couleur("Commandes disponibles :", "jaune"))
    for i, commande in enumerate(commandes, 1):
        nom = commande.get("nom", "?")
        description = commande.get("description", "")
        print("  %2d. %s : %s" % (i, nom, description))


def poser_question(parametre, numero, total):
    """Affiche la question et retourne la reponse saisie (brute)."""
    question = parametre.get("question", "Valeur pour %s ?" % parametre.get("cle", "?"))
    type_param = parametre.get("type", "texte")
    defaut = parametre.get("defaut", "")

    suffixe = ""
    if type_param == "choix":
        suffixe = " [choix : %s]" % ", ".join(parametre.get("choix", []))
    if defaut != "":
        suffixe += " [defaut : %s]" % defaut

    print(_couleur("[Question %d/%d] %s%s" % (numero, total, question, suffixe), "jaune"))
    try:
        reponse = input("> ").strip()
    except EOFError:
        return None
    return reponse


def valider_reponse(parametre, reponse):
    """Valide une reponse brute pour un parametre. Retourne (valeur, erreur)."""
    cle = parametre.get("cle", "?")
    type_param = parametre.get("type", "texte")
    obligatoire = parametre.get("obligatoire", False)
    defaut = parametre.get("defaut", "")

    if reponse == "" and defaut != "":
        reponse = defaut

    if type_param == "flag":
        reponse = reponse.strip().lower()
        if reponse in ("", "non", "false", "faux", "n"):
            return "", None
        if reponse in ("oui", "true", "vrai", "o", "y", "yes"):
            return parametre.get("flag", cle), None
        return None, "Reponse invalide pour %s (oui ou non attendu)" % cle

    if reponse == "":
        if obligatoire:
            return None, "Le parametre %s est obligatoire" % cle
        return "", None

    if type_param == "choix":
        choix = parametre.get("choix", [])
        if reponse not in choix:
            return None, "Valeur invalide pour %s (attendu : %s)" % (
                cle,
                ", ".join(choix),
            )
        return reponse, None

    return reponse, None


def composer_valeur(parametre, valeur):
    """Encapsule la valeur pour la commande (guillemets si besoin)."""
    if valeur == "":
        return ""
    quoter = parametre.get("quoter", False)
    contient_espace = re.search(r"[\s]", valeur) is not None
    if quoter or contient_espace:
        valeur_echappee = valeur.replace("\\", "\\\\").replace('"', '\\"')
        return '"%s"' % valeur_echappee
    return valeur


def composer_commande(commandes, reponses):
    """Compose la ligne de commande complete a partir des reponses."""
    commande = commandes
    modele = commande.get("modele", "")
    lignes = []
    for parametre in commande.get("parametres", []):
        cle = parametre.get("cle", "?")
        valeur = reponses.get(cle, "")
        lignes.append((cle, valeur))

    resultat = modele
    for cle, valeur in lignes:
        parametre = None
        for p in commande.get("parametres", []):
            if p.get("cle") == cle:
                parametre = p
                break
        if valeur == "":
            # Flag a valeur en dur dans le modele (--cle {cle}) : retirer le flag ET le placeholder si la valeur est vide
            # (corrige 2026-08-09 : la condition etait inversee -> les flags optionnels non renseignes
            #  restaient vides dans la commande (--nombre sans valeur) et argparse les rejetait en erreur)
            # (corrige 2026-08-12 round 6 : le flag du MODELE sans champ flag declare restait orphelin
            #  (--commande seul) et absorbait l option suivante -- 95 entrees du catalogue concernees)
            flag_param = parametre.get("flag", "") if parametre else ""
            if flag_param:
                # Retirer le flag DECLARE suivi du placeholder (--refs {refs} -> rien si vide)
                resultat = re.sub(r"%s\s+\{%s\}" % (re.escape(flag_param), re.escape(cle)), "", resultat)
            else:
                # Retirer le flag du MODELE suivi du placeholder (--commande {commande} -> rien si vide)
                resultat = re.sub(r"--[a-z0-9-]+\s+\{%s\}" % re.escape(cle), "", resultat)
            # Retirer le placeholder seul ({dry_run} -> rien si vide)
            resultat = re.sub(r"\s+\{%s\}" % re.escape(cle), "", resultat)
        resultat = resultat.replace("{%s}" % cle, composer_valeur(parametre, valeur))

    resultat = re.sub(r"\s+", " ", resultat).strip()

    base = [commande.get("interpreteur", "python3")]
    script = commande.get("script", "")
    if script:
        base.append(script)
    if resultat:
        base.append(resultat)
    return " ".join(base)


def interroger_interactif(commandes, reponses_forcees=None):
    """Pose les questions une par une et retourne les reponses.

    Si des reponses sont forcees (--reponses), les parametres fournis sont
    valides sans question ; un parametre obligatoire manquant devient une
    erreur immediate (mode non-interactif).
    """
    reponses = {}
    parametres = commandes.get("parametres", [])
    total = len(parametres)
    for numero, parametre in enumerate(parametres, 1):
        cle = parametre.get("cle", "?")
        if reponses_forcees is not None:
            if cle in reponses_forcees:
                valeur, erreur = valider_reponse(parametre, reponses_forcees[cle])
                if erreur:
                    print(_couleur("  [ERREUR] %s" % erreur, "rouge"))
                    return None
                reponses[cle] = valeur
                continue
            if parametre.get("obligatoire", False):
                print(
                    _couleur(
                        "  [ERREUR] Parametre obligatoire manquant : %s (utiliser --reponses)"
                        % cle,
                        "rouge",
                    )
                )
                return None
            valeur, erreur = valider_reponse(parametre, parametre.get("defaut", ""))
            if erreur:
                print(_couleur("  [ERREUR] %s" % erreur, "rouge"))
                return None
            reponses[cle] = valeur
            continue
        while True:
            reponse = poser_question(parametre, numero, total)
            if reponse is None:
                print(_couleur("  [ABANDON] Entree standard epuisee (EOF)", "rouge"))
                return None
            valeur, erreur = valider_reponse(parametre, reponse)
            if erreur:
                print(_couleur("  [ERREUR] %s" % erreur, "rouge"))
                continue
            reponses[cle] = valeur
            break
    return reponses


def parser_reponses_forcees(chaine):
    """Parse la chaine --reponses 'cle=valeur;cle2=valeur2'."""
    reponses = {}
    if not chaine:
        return reponses
    for morceau in chaine.split(";"):
        morceau = morceau.strip()
        if not morceau:
            continue
        if "=" not in morceau:
            print(_couleur("ERREUR: Reponse mal formee (cle=valeur) : %s" % morceau, "rouge"), file=sys.stderr)
            sys.exit(1)
        cle, valeur = morceau.split("=", 1)
        reponses[cle.strip()] = valeur.strip()
    return reponses


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-commande",
        description="Genere une commande complexe en posant une question par parametre.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--liste", action="store_true", help="Lister les commandes du catalogue")
    parser.add_argument("--commande", type=str, help="Nom de la commande a generer (ex: activer-activer)")
    parser.add_argument("--reponses", type=str, help="Reponses fournies en une fois : cle=valeur;cle2=valeur2")
    parser.add_argument("--catalogue", type=str, help="Chemin du catalogue (defaut : a cote du script)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher la commande sans l executer")
    parser.add_argument("--agent", type=str, default="", help="Agent a journaliser (defaut : agent actif de AGENTS.md)")
    parser.add_argument("--no-journal", action="store_true", help="Desactiver la journalisation d usage")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="generateurs-commande v%s" % VERSION)
    return parser


def _lire_agent_actif():
    """Lit l agent actif de la session session-llm-1 dans AGENTS.md.
    Retourne 'inconnu' si introuvable (jamais d erreur bloquante)."""
    try:
        racine = os.path.dirname(os.path.abspath(sys.argv[0]))
        while not os.path.isfile(os.path.join(racine, "AGENTS.md")):
            parent = os.path.dirname(racine)
            if parent == racine:
                return "inconnu"
            racine = parent
        with open(os.path.join(racine, "AGENTS.md"), encoding="utf-8") as fh:
            txt = fh.read()
        bloc = txt.split("### Session : session-llm-1", 1)
        if len(bloc) < 2:
            return "inconnu"
        # couper sur la ligne de fin de bloc (--- seul en debut de ligne)
        segment = bloc[1].split("\n---", 1)[0]
        for ligne in segment.splitlines():
            if "Nom Agent" in ligne and "|" in ligne:
                return ligne.split("|")[2].strip().lower() or "inconnu"
        return "inconnu"
    except Exception:
        return "inconnu"


def _journaliser_usage(agent, outil, commande_finale):
    """Appelle enregistrer-usage-outil en mode generateur (discret : stderr).
    Ne doit JAMAIS bloquer la generation (erreurs silencieuses)."""
    try:
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                              "enregistrer", "enregistrer-usage-outil",
                              "enregistrer-usage-outil.py")
        if not os.path.isfile(script):
            return
        import subprocess
        subprocess.run(
            [sys.executable, script, "--agent", agent, "--outil", outil,
             "--mode", "generateur", "--commande", commande_finale],
            capture_output=True, timeout=10,
        )
    except Exception:
        pass


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()

    dossier_script = os.path.dirname(os.path.abspath(sys.argv[0]))
    chemin_catalogue = args.catalogue
    if not chemin_catalogue:
        chemin_catalogue = os.path.join(dossier_script, "catalogue-commandes.json")

    catalogue = charger_catalogue(chemin_catalogue)

    if args.liste:
        lister_commandes(catalogue)
        return 0

    commandes = None
    if args.commande:
        commandes = trouver_commande(catalogue, args.commande)
        if commandes is None:
            print(
                _couleur(
                    "ERREUR: Commande inconnue : %s (utiliser --liste)" % args.commande,
                    "rouge",
                ),
                file=sys.stderr,
            )
            return 1
    else:
        # Mode interactif : menu de choix
        lister_commandes(catalogue)
        print("")
        print(_couleur("Quelle commande generer ? (numero ou nom)", "jaune"))
        try:
            choix = input("> ").strip()
        except EOFError:
            choix = ""
        if choix.isdigit():
            index = int(choix) - 1
            toutes = catalogue.get("commandes", [])
            if 0 <= index < len(toutes):
                commandes = toutes[index]
        else:
            commandes = trouver_commande(catalogue, choix)
        if commandes is None:
            print(_couleur("ERREUR: Choix invalide", "rouge"), file=sys.stderr)
            return 1

    reponses_forcees = parser_reponses_forcees(args.reponses)

    print(_couleur("=== %s ===" % commandes.get("nom", "?"), "bleu"))
    print("%s" % commandes.get("description", ""))
    print("")

    reponses = interroger_interactif(commandes, reponses_forcees)
    if reponses is None:
        return 1

    commande_finale = composer_commande(commandes, reponses)

    print("")
    print(_couleur("=== COMMANDE A LANCER ===", "vert"))
    print(commande_finale)
    print("")

    # Journalisation d usage (registre JSONL) : automatique sauf --no-journal.
    # FIX v0.2.5 (2026-08-15, lecon Janus, 4 occurrences) : journaliser SON PROPRE NOM
    # (generateurs-commande) au lieu du nom de COMMANDE du catalogue (ex activer-activer)
    # - une entree 'activer-activer' cree un OUTIL_HORS_CARTE artificiel (test-035 KO) que
    #   Janus devait corriger manuellement a chaque activation. La commande generee complete
    #   reste dans le champ 'commande' du registre (veracite preservee).
    if not args.no_journal:
        agent = args.agent or _lire_agent_actif()
        _journaliser_usage(agent, "generateurs-commande", commande_finale)

    if args.verbose:
        print(_couleur("[DETAIL] Reponses recues :", "bleu"))
        for cle, valeur in sorted(reponses.items()):
            print("  %s = %s" % (cle, valeur))

    return 0


if __name__ == "__main__":
    sys.exit(main())
