#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
presenter-agent.py
Presentateur COMMUN des possibilites d un agent - version PRESENTATION HUMAINE.

Outil generique reutilisable : il lit la FICHE de l agent (frontmatter YAML :
role, specialites, forces, style) ET son ARBRE v2 (branches) et produit une
PRESENTATION en langage naturel, comme un humain se presenterait :
  - Qui je suis / mon role
  - Ce que je peux faire pour toi
  - Comment ca se passe (deroule)
  - Mes points forts
  - Mes possibilites (branches de mon arbre)

Fiabilite : tout est genere DYNAMIQUEMENT depuis la fiche + l arbre. Aucun
texte fige. Si la fiche ou l arbre est illisible/incomplet, l outil REFUSE
d afficher une presentation mensongere (code 1).

Usage:
  presenter-agent.py <agent> [--detail]
  presenter-agent.py --lister-agents          # lister les agents a arbre v2

Proprietaire : Buffy (developpeur principal, outils communs)
Version : 0.2.0
Statut : ebauche
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

VERSION = "0.2.0"
STATUT = "ebauche"

# Racine du projet : presenter-agent -> presenter -> tools -> agents -> cerveau-projet -> racine
RACINE = Path(__file__).resolve().parents[5]

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "cyan": "\033[0;36m",
    "magenta": "\033[0;35m",
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
    print(_couleur("REFUS: relancez avec --confirme-doc apres lecture de la doc.", "rouge"),
          file=sys.stderr)
    sys.exit(2)


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(_couleur("ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                       % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


def afficher_messages_info(messages):
    if not messages:
        return
    print("")
    print(_couleur("=== MESSAGES POUR L AGENT ===", "jaune"))
    for message in messages:
        print("  > %s" % message)


# ------------------------------------------------------------------
# Chargement de l arbre d un agent
# ------------------------------------------------------------------

def _charger_json(chemin, obligatoire=True):
    p = Path(chemin)
    if not p.is_file():
        p = RACINE / chemin
    if not p.is_file():
        if obligatoire:
            print(_couleur("ERREUR: Fichier introuvable: %s" % chemin, "rouge"), file=sys.stderr)
            sys.exit(1)
        return None
    try:
        with p.open(encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        print(_couleur("ERREUR: JSON invalide dans %s: %s" % (chemin, exc), "rouge"), file=sys.stderr)
        sys.exit(1)


def trouver_arbre(agent):
    """Trouve et charge l arbre v2 d un agent (arbre-<agent>.json).

    Renvoie (donnees, dossier_base) ou dossier_base est le dossier contenant
    l arbre (parcours/) pour resoudre les themes."""
    candidates = [
        RACINE / "cerveau-projet" / "agents" / agent / "parcours" / ("arbre-" + agent + ".json"),
        RACINE / "cerveau-projet" / "agents" / agent / ("arbre-" + agent + ".json"),
    ]
    for p in candidates:
        if p.is_file():
            return _charger_json(str(p), obligatoire=True), p.parent
    print(_couleur("ERREUR: Aucun arbre v2 trouve pour l agent '%s'." % agent, "rouge"),
          file=sys.stderr)
    print("  Cherche : %s" % candidates[0], file=sys.stderr)
    sys.exit(1)


def trouver_fiche(agent):
    """Trouve la fiche de l agent (cerveau-projet/agents/<agent>/<agent>.md)."""
    p = RACINE / "cerveau-projet" / "agents" / agent / (agent + ".md")
    if not p.is_file():
        return None
    return p


# ------------------------------------------------------------------
# Mini-parseur YAML du frontmatter de fiche (stdlib pure)
# ------------------------------------------------------------------

def _nettoyer_valeur(texte):
    """Nettoie une valeur YAML : guillemets, espaces, commentaires."""
    t = texte.strip()
    if t.startswith('"') and t.endswith('"'):
        t = t[1:-1]
    elif t.startswith("'") and t.endswith("'"):
        t = t[1:-1]
    # retirer un commentaire en fin de ligne (mais pas un # dans une chaine)
    if " #" in t:
        t = t.split(" #")[0].rstrip()
    return t


def lire_frontmatter(chemin_fiche):
    """Parse le frontmatter YAML d une fiche (structure plate : sections,
    sous-cles, listes a tirets). Renvoie un dict, vide si absent."""
    try:
        lignes = chemin_fiche.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return {}
    if not lignes or lignes[0].strip() != "---":
        return {}
    # trouver la fin du frontmatter
    fin = None
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            fin = i
            break
    if fin is None:
        return {}
    corps = lignes[1:fin]

    data = {}
    section = None
    cle = None
    for ligne in corps:
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        indent = len(ligne) - len(ligne.lstrip())
        texte = ligne.strip()
        if indent == 0 and texte and ":" in texte and not texte.startswith("- "):
            # nouvelle section
            nom = texte.split(":", 1)[0].strip()
            section = nom
            cle = None
            data[section] = {}
            continue
        if indent >= 2 and texte.startswith("- "):
            # element de liste
            item = _nettoyer_valeur(texte[2:])
            if section is not None and cle is not None:
                if not isinstance(data[section].get(cle), list):
                    data[section][cle] = []
                data[section][cle].append(item)
            continue
        if indent >= 2 and ":" in texte and not texte.startswith("- "):
            nom = texte.split(":", 1)[0].strip()
            valeur = texte.split(":", 1)[1].strip()
            if valeur == "":
                cle = nom
                if section is not None:
                    data[section][nom] = []  # liste en attente
                continue
            valeur = _nettoyer_valeur(valeur)
            if section is not None:
                data[section][nom] = valeur
            continue
    return data


# ------------------------------------------------------------------
# Construction de la presentation humaine
# ------------------------------------------------------------------

def extraire_profil(frontmatter):
    """Extrait le profil humain depuis le frontmatter de la fiche."""
    agent = frontmatter.get("agent", {})
    profil = frontmatter.get("profil", {})
    config = frontmatter.get("config", {})

    role = (profil.get("role-agent") or agent.get("role_specifique") or "").strip()
    specialites = [s for s in profil.get("specialites", []) if s]
    forces = [f for f in profil.get("forces", []) if f]
    style = (config.get("style") or "").strip()
    ton = (config.get("communication", {}).get("ton") or "").strip() \
        if isinstance(config.get("communication"), dict) else ""
    nom = (agent.get("nom-agent") or "").strip()

    return {
        "nom": nom,
        "role": role,
        "specialites": specialites,
        "forces": forces,
        "style": style,
        "ton": ton,
    }


def preparer_presentation(donnees, dossier_base, frontmatter):
    """Construit la structure de la presentation humaine.

    Tout est lu dans la fiche + l arbre : aucun texte fige sur l agent.
    """
    arbre = donnees.get("arbre", {})
    racine = donnees.get("racine", {})
    profil = extraire_profil(frontmatter)

    branches = []
    for b in racine.get("branches", []):
        branches.append({
            "reponse": b.get("reponse", "?"),
            "description": (b.get("description") or "").strip(),
            "vers": b.get("vers", ""),
        })

    return {
        "agent": arbre.get("agent", "?"),
        "nom_arbre": arbre.get("nom", "?"),
        "version": arbre.get("version", "?"),
        "racine_titre": racine.get("titre", "Quel theme ?"),
        "racine_question": (racine.get("question") or "").strip(),
        "dossier_base": dossier_base,
        "branches": branches,
        "profil": profil,
    }


def charger_besoins_themes(pres, branche):
    """Charge les besoins (redirects) d un theme de branche, si lisible."""
    vers = branche.get("vers", "")
    if not vers:
        return []
    p = Path(pres["dossier_base"]) / vers
    if not p.is_file():
        return []
    try:
        data_theme = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return []
    theme = data_theme.get("theme", {})
    besoins = [r.get("besoin", "?") for r in theme.get("redirects", [])]
    return besoins


def _couper_lignes(texte, largeur=88):
    """Coupe un texte long en lignes de la largeur donnee (sans casser de mot)."""
    lignes = []
    for paragraphe in texte.split("\n"):
        mots = paragraphe.split()
        courante = ""
        for mot in mots:
            if len(courante) + len(mot) + 1 > largeur:
                if courante:
                    lignes.append(courante)
                courante = mot
            else:
                courante = (courante + " " + mot).strip()
        if courante:
            lignes.append(courante)
    return lignes


def afficher_presentation(pres, avec_besoins=False):
    """Affiche la presentation HUMAINE generee depuis la fiche + l arbre."""
    profil = pres.get("profil", {})
    nom = profil.get("nom") or pres["agent"]
    print("")
    print(_couleur("Bonjour ! Je suis %s." % nom.upper(), "vert"))
    if profil.get("role"):
        print("")
        for ligne in _couper_lignes(profil["role"]):
            print(ligne)

    # --- Ce que je peux faire pour toi (specialites) ---
    if profil.get("specialites"):
        print("")
        print("Ce que je peux faire pour toi :")
        for s in profil["specialites"]:
            print(_couleur("  - ", "cyan") + s)
        print("")

    # --- Comment ca se passe (branches en langage naturel) ---
    print("Comment je travaille, concretement :")
    for i, b in enumerate(pres["branches"], 1):
        print(_couleur("  %d) %s" % (i, b["reponse"]), "cyan"))
        if b.get("description"):
            for ligne in _couper_lignes("     " + b["description"]):
                print(ligne)
        if avec_besoins:
            besoins = charger_besoins_themes(pres, b)
            if besoins:
                print("     -> %s" % " / ".join(besoins))
    print("")

    # --- Mes points forts (forces) ---
    if profil.get("forces"):
        print("Mes points forts :")
        for f in profil["forces"]:
            print("  * " + f)
        print("")

    # --- Style et ton ---
    traits = []
    if profil.get("style"):
        traits.append(profil["style"])
    if profil.get("ton"):
        traits.append(profil["ton"])
    if traits:
        print("Mon style : %s." % " ; ".join(traits))
    print("")
    print(_couleur("Je t'ecoute : dis-moi ce qui t'amene.", "vert"))
    print(_couleur("=== FIN DE LA PRESENTATION ===", "vert"))


def meilleur_agentocher(prefixe):
    """Trouve les agents dont le nom commence par le prefixe (aide)."""
    base = RACINE / "cerveau-projet" / "agents"
    resultats = []
    if not base.is_dir():
        return resultats
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        arbre = d / "parcours" / ("arbre-" + d.name + ".json")
        if arbre.is_file():
            resultats.append(d.name)
    if prefixe:
        resultats = [a for a in resultats if a.startswith(prefixe.lower())]
    return resultats


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="presenter-agent",
        description="Presentateur COMMUN d un agent (presentation humaine generee depuis sa fiche + son arbre v2)",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("agent", type=str, help="Nom de l agent (ex: socrate)")
    parser.add_argument("--detail", action="store_true",
                        help="Ajouter les buts (besoins) de chaque branche")
    parser.add_argument("--lister-agents", action="store_true",
                        help="Lister tous les agents disposant d un arbre v2")
    parser.add_argument("--version", action="version", version="presenter-agent v%s" % VERSION)
    parser.add_argument("--dry-run", action="store_true", help="Verifier sans rien afficher")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--chrono", action="store_true", help="Mesurer la duree d execution")
    parser.add_argument("--doc", action="store_true",
                        help="Afficher le .md de documentation complet et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation (requis en mode reel)")
    return parser


def main():
    import time
    debut = time.time()

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

    if args.lister_agents:
        liste = meilleur_agentocher("")
        if not liste:
            print(_couleur("Aucun agent avec arbre v2 trouve.", "rouge"), file=sys.stderr)
            return 1
        print("Agents disposant d'un arbre v2 :")
        for a in liste:
            print("  - %s" % a)
        return 0

    if args.dry_run:
        trouver_arbre(args.agent)
        print(_couleur("[DRY-RUN] L arbre de '%s' existe et est lisible." % args.agent, "vert"))
        return 0

    # Charger l arbre + la fiche
    donnees, dossier_base = trouver_arbre(args.agent)
    fiche = trouver_fiche(args.agent)
    frontmatter = lire_frontmatter(fiche) if fiche else {}
    pres = preparer_presentation(donnees, dossier_base, frontmatter)

    # Garde-fou de coherence : ni arbre vide ni fiche absente ne permettent
    # une presentation mensongere.
    if not pres["branches"]:
        print(_couleur("ERREUR: L arbre de '%s' n a aucune branche : presentation refusee "
                       "(fiable avant tout)." % args.agent, "rouge"), file=sys.stderr)
        return 1
    if not pres["profil"].get("role") and not pres["profil"].get("specialites"):
        print(_couleur("ERREUR: Fiche de '%s' sans role ni specialites : presentation "
                       "refusee (fiable avant tout)." % args.agent, "rouge"), file=sys.stderr)
        return 1

    afficher_presentation(pres, avec_besoins=args.detail)

    if args.chrono:
        print("Duree : %.2fs" % (time.time() - debut))

    afficher_messages_info([
        "presentation generee DYNAMIQUEMENT depuis la fiche + l arbre v2 de l agent - toujours synchronisee",
        "REGLE : l agent doit AFFICHER la sortie COMPLETE de cette presentation a l utilisateur",
        "si vous ecrivez/modifiez la fiche ou l arbre, relancez la sequence : presenter-agent <agent> --confirme-doc",
    ])
    return 0


if __name__ == "__main__":
    sys.exit(main())