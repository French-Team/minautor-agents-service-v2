#!/usr/bin/env python3
# -*- coding: ascii -*-
# verifier-coherence-agents.py
# Verifie la coherence des blocs session d AGENTS.md contre les fichiers reels
# (arbres de decision v2, fiches, corrections, jarvis-data.json, table Sessions).
# Version : 0.1.0
# Statut : prepare

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path

VERSION = "0.1.0"
STATUT = "prepare"

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


def _doc_chemin(script_path):
    p = Path(script_path)
    return p.with_suffix(".md")


def verifier_doc_presente(script_path):
    doc = _doc_chemin(script_path)
    if not doc.is_file():
        print(_couleur("ERREUR: Documentation manquante : %s" % doc, "rouge"),
              file=sys.stderr)
        sys.exit(2)


def afficher_section_utilisation(doc):
    try:
        texte = doc.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
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
    print(_couleur("REFUS: relancez avec --confirme-doc apres lecture de la doc.", "rouge"),
          file=sys.stderr)
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


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="verifier-coherence-agents",
        description="Verifie la coherence des blocs session d AGENTS.md vs fichiers reels",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="verifier-coherence-agents v%s" % VERSION)
    parser.add_argument("--chrono", action="store_true", help="Mesurer la duree d execution")
    parser.add_argument("--doc", action="store_true", help="Afficher le .md de documentation complet et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation (requis en mode reel)")
    parser.add_argument("--agents-md", type=str, default=None,
                        help="Chemin vers AGENTS.md (defaut : racine du projet)")
    parser.add_argument("--seuil", type=int, default=0,
                        help="Code de sortie si des incoherences sont trouvees (defaut 0 = avertis seulement)")
    return parser


def trouver_racine():
    """Remonter jusqu'au dossier contenant cerveau-projet/ + AGENTS.md."""
    d = Path.cwd()
    while not (d / "AGENTS.md").is_file():
        if d == d.parent:
            return None
        d = d.parent
    return d


def extraire_blocs_agents(contenu, debut_marqueur="### Session :"):
    """Extraire les blocs session de la forme '### Session : <nom>' de AGENTS.md.

    Retourne {nom_session: {champs, texte}} avec :
    - champs : les valeurs du tableau du bloc (| **X** | valeur |)
    - texte  : TOUT le texte du bloc (tableau + bloc DEMARRAGE V2 qui suit),
      scanne jusqu au prochain '### Session' / '## ' (car les lignes hors
      tableau, comme '(themes : ...)', ne sont PAS dans le tableau).
    """
    blocs = {}
    lignes = contenu.splitlines()
    i = 0
    while i < len(lignes):
        ligne = lignes[i].strip()
        if ligne.startswith(debut_marqueur):
            nom = ligne[len(debut_marqueur):].strip()
            champ = {}
            texte_lignes = []
            i += 1
            while i < len(lignes):
                l = lignes[i].rstrip()
                if l.strip().startswith("### Session") or l.strip().startswith("## "):
                    break
                m = re.match(r"\| \*\*([^*]+)\*\* \|\s*(.*?)\s*\|$", l.strip())
                if m:
                    champ[m.group(1).strip()] = m.group(2).strip()
                texte_lignes.append(l)
                i += 1
            blocs[nom] = {"champs": champ, "texte": "\n".join(texte_lignes)}
            continue
        i += 1
    return blocs


def obtenir_agent_actif(fichier_md, nom_session):
    """Sous --agents-md, l entree 'Fiche' du bloc donne le chemin de la fiche."""
    return None  # interprete par la valeur du bloc


def verifier_fichier_existe(chemin, racine, incoherences, ligne, contexte):
    p = Path(racine) / chemin
    if not p.is_file():
        incoherences.append((ligne, contexte, "fichier introuvable : %s" % chemin))


def verifier_arbres_v2(racine, agents_md, incoherences, lignes_rapport, verbose):
    """Verifier que chaque bloc freelance a une ligne themes coherente avec son arbre.

    L arbre-<agent>.json (racine.suivant) doit etre reference. Le bloc DEMARRAGE
    V2 ne doit jamais lister plus de themes que l arbre n en reference.
    """
    freelance_agents = {}
    for nom, valeur in agents_md.items():
        fiche = valeur.get("champs", {}).get("Fiche", "")
        if "freelance" in fiche and "parcours" not in fiche:
            freelance_agents[nom] = valeur

    for nom, valeur in freelance_agents.items():
        champ = valeur.get("champs", {})
        fiche = champ.get("Fiche", "")
        # fiche = [cerveau-projet/freelance/stark/stark.md](...)
        m = re.search(r"freelance/([^/]+)/[^/]+\.md", fiche)
        if not m:
            continue
        agent = m.group(1)
        arbre = Path(racine) / "cerveau-projet/freelance" / agent / "parcours" / ("arbre-%s.json" % agent)
        if not arbre.is_file():
            incoherences.append((None, "bloc %s" % nom,
                                 "arbre introuvable : %s" % arbre))
            continue
        try:
            data = json.loads(arbre.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            incoherences.append((None, "bloc %s" % nom,
                                 "arbre illisible : %s" % arbre))
            continue
        suivant = data.get("racine", {}).get("suivant")
        themes_reels = set()
        if suivant:
            themes_reels.add(suivant)
        # le bloc DEMARRAGE V2 contient la ligne '(themes : ...)' dans le TEXTE
        # du bloc (hors tableau). On analyse tout le texte du bloc.
        texte_bloc = valeur.get("texte", "")
        # ligne '(themes : ...)' : tenter de capturer la ligne entiere, puis
        # extraire de celle-ci tous les themes theme-*.json listes.
        contenu_themes = None
        for ligne in texte_bloc.splitlines():
            l = ligne.strip()
            if re.search(r"themes\s*:", l):
                contenu_themes = re.sub(r"^[^(]*\(?\s*|themes\s*:\s*", "", l)
                break
        if contenu_themes:
            noms_themes = re.findall(r"theme-[A-Za-z0-9_-]+(?:\.json)?", contenu_themes)
            bases_reelles = set(os.path.splitext(t)[0] for t in themes_reels)
            orphelins = []
            for t in noms_themes:
                base = os.path.splitext(t)[0] if t.endswith(".json") else t
                if base not in bases_reelles:
                    orphelins.append(t)
            if orphelins:
                incoherences.append(
                    (None, "bloc %s DEMARRAGE V2" % nom,
                     "themes listes non references par l arbre : %s (arbre ne reference que %s)"
                     % (sorted(set(orphelins)), sorted(themes_reels))))
        if verbose:
            lignes_rapport.append("  [verbose] %s : arbre=%s themes_reels=%s" % (nom, arbre.name, sorted(themes_reels)))


def verifier_rsaisons_tronquees(agents_md, incoherences, verbose):
    """Detecter les raisons de bloc manifestement tronquees (fin de mot coupee)."""
    for nom, valeur in agents_md.items():
        raison = valeur.get("champs", {}).get("Raison", "")
        if not raison:
            continue
        # une raison ne finit normalement pas par un mot inacheve sans ponctuation
        if re.search(r"[A-Za-z]{2,}$", raison) and not re.search(r"[.\])!?:;]$", raison):
            incoherences.append((None, "bloc %s Raison" % nom,
                                 "raison potentiellement tronquee : '...%s'" % raison[-40:]))


def verifier_jarvis_data(racine, incoherences, verbose):
    """Verifier que chaque agent de jarvis-data.json a fiche + corrections non vides
    et existantes sur disque."""
    jd = Path(racine) / "cerveau-projet/freelance/tools-commun/jarvis/jarvis-data.json"
    if not jd.is_file():
        incoherences.append((None, "jarvis-data.json", "fichier introuvable"))
        return
    try:
        data = json.loads(jd.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        incoherences.append((None, "jarvis-data.json", "JSON illisible"))
        return
    for agent in data.get("agents", []):
        nom = agent.get("nom")
        for champ in ("fiche", "corrections"):
            val = agent.get(champ, "")
            if not val:
                incoherences.append((None, "jarvis-data.json agent %s" % nom,
                                     "%s vide" % champ))
                continue
            p = Path(racine) / val
            if not p.is_file():
                incoherences.append((None, "jarvis-data.json agent %s" % nom,
                                     "%s introuvable : %s" % (champ, val)))


def verifier_sessions_connues(contenu, agents_md, racine, incoherences, verbose):
    """Verifier la coherence de la table 'Sessions connues' avec les blocs.

    Chaque session du tableau doit avoir un bloc correspondant ET une derniere
    activite non vide. Des dates anciennes (plusieurs jours) avec un bloc recent
    signalent une desynchronisation entre ecrivains.
    """
    m = re.search(r"## Sessions connues\s*\n(.*?)(?=\n##|\Z)", contenu, re.DOTALL)
    if not m:
        return
    table = m.group(1)
    for ligne in table.splitlines():
        parts = [p.strip() for p in ligne.split("|") if p.strip()]
        if len(parts) >= 4 and parts[0].startswith("session-"):
            nom_session = parts[0]
            actif = parts[2]
            d_activite = parts[3]
            if nom_session not in agents_md:
                incoherences.append((None, "Session connue %s" % nom_session,
                                     "aucun bloc session correspondant"))
            if not d_activite or d_activite == "-":
                incoherences.append((None, "Session connue %s" % nom_session,
                                     "derniere activite vide"))
            elif verbose:
                pass  # les dates anciennes ne sont pas bloqueantes, simple signal


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

    racine = trouver_racine()
    if racine is None:
        print(_couleur("ERREUR: AGENTS.md introuvable depuis le repertoire courant.", "rouge"),
              file=sys.stderr)
        return 2

    agents_md_path = Path(args.agents_md) if args.agents_md else racine / "AGENTS.md"
    try:
        contenu = agents_md_path.read_text(encoding="utf-8")
    except OSError:
        print(_couleur("ERREUR: impossible de lire %s" % agents_md_path, "rouge"),
              file=sys.stderr)
        return 2

    incoherences = []
    lignes_rapport = []

    # 1. fiches + corrections des blocs existent
    blocs = extraire_blocs_agents(contenu)
    for nom, valeur in blocs.items():
        champ = valeur.get("champs", {})
        for cle in ("Fiche", "Corrections"):
            val = champ.get(cle, "")
            if val:
                m = re.search(r"\]\((.*?)\)", val)
                chemin = m.group(1) if m else val
                verifier_fichier_existe(chemin, racine, incoherences, None,
                                        "bloc %s %s" % (nom, cle))

    # 2. coherence arbres v2 vs blocs freelance
    verifier_arbres_v2(racine, blocs, incoherences, lignes_rapport, args.verbose)

    # 3. raisons potentiellement tronquees
    verifier_rsaisons_tronquees(blocs, incoherences, args.verbose)

    # 4. jarvis-data.json coherent
    verifier_jarvis_data(racine, incoherences, args.verbose)

    # 5. table Sessions connues vs blocs
    verifier_sessions_connues(contenu, blocs, racine, incoherences, args.verbose)

    # ---- sortie ----
    print(_couleur("=== verifier-coherence-agents v%s ===" % VERSION, "bleu"))
    print("Racine projet : %s" % racine)
    print("AGENTS.md     : %s" % agents_md_path)
    print("Blocs session : %d" % len(blocs))
    print("")
    for ligne in lignes_rapport:
        print(ligne)

    if incoherences:
        print(_couleur("=== INCOHERENCES (%d) ===" % len(incoherences), "rouge"))
        for i, (ligne, contexte, detail) in enumerate(incoherences, 1):
            pos = "l.%s" % ligne if ligne is not None else "-"
            print("  %d. [%s pos=%s] %s" % (i, contexte, pos, detail))
        print("")
        return args.seuil if args.seuil else 1
    else:
        print(_couleur("=== RESULTAT : 0 incoherence -- AGENTS.md COHERENT ===", "vert"))
        if not args.dry_run:
            afficher_messages_info([
                "verification realisee en lecture seule : aucune modification",
                "pour brancher au demarrage : ajouter cet outil a la case c0c (Cerberus) ou demarrer.md",
            ])
        return 0


if __name__ == "__main__":
    sys.exit(main())