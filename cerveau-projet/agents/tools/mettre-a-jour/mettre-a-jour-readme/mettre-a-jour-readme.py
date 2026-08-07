#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
mettre-a-jour-readme.py

Outil pour corriger le README afin qu'il reflete l'etat reel du projet.
Le README est le livre du projet, jamais un carnet de suivi : l'outil
corrige le texte existant, il n'ajoute AUCUNE ligne d'historique.

Options:
  --verifier         Comparer l'etat reel au README, lister les ecarts (sans modifier)
  --maj              Corriger le texte du README (agents, outils, compteurs)
  --journal [N]      Consulter les N dernieres interventions (diagnostic, non inscrit au README)
  --logo CHEMIN      Inserer une image (logo) en tete du README, apres le titre H1
  --badges SPEC      Inserer des badges GitHub/Shields statiques (format label=message:couleur;...)
  --agents           Afficher le compte reel des agents
  --outils           Afficher le compte reel des outils par categorie
  --help             Afficher cette aide

Proprietaire : Clio (agent dedie au README)
Version : 0.4.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.4.0-py"
STATUT = "prepare"

README = "README.md"
HISTORIQUE = "AGENTS-historique.md"
AGENTS_DIR = "cerveau-projet/agents"
TOOLS_DIR = "cerveau-projet/agents/tools"

CATEGORIES_EXCLUES = {"combos"}


def compter_agents():
    """Compter les agents reels (dossiers dans agents/, hors tools)."""
    nb = 0
    if not os.path.isdir(AGENTS_DIR):
        return 0
    for nom in os.listdir(AGENTS_DIR):
        if os.path.isdir(os.path.join(AGENTS_DIR, nom)) and nom != "tools":
            nb += 1
    return nb


def lister_agents_reels():
    """Lister les agents reels (noms des dossiers)."""
    resultat = []
    if not os.path.isdir(AGENTS_DIR):
        return resultat
    for nom in os.listdir(AGENTS_DIR):
        if os.path.isdir(os.path.join(AGENTS_DIR, nom)) and nom != "tools":
            resultat.append(nom)
    return resultat


def lire_role_agent(agent):
    """Lire le role specifique d'un agent depuis sa fiche."""
    fiche = os.path.join(AGENTS_DIR, agent, agent + ".md")
    if not os.path.isfile(fiche):
        return ""
    try:
        with io.open(fiche, "r", encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                m = re.match(r"^\s*role_specifique:\s*(.*)$", ligne)
                if m:
                    return m.group(1).strip().strip('"').strip("'").replace("\r", "")
    except IOError:
        return ""
    return ""


def lister_categories():
    """Lister les categories d'outils (chaque sous-dossier, plus combos et templates)."""
    categories = []
    if os.path.isdir(TOOLS_DIR):
        for nom in sorted(os.listdir(TOOLS_DIR)):
            chemin = os.path.join(TOOLS_DIR, nom)
            if os.path.isdir(chemin) and nom not in CATEGORIES_EXCLUES:
                categories.append(nom)
    categories.append("combos")
    categories.append("templates")
    return categories


def compter_outils_categorie(categorie):
    """Compter les outils d'une categorie (chaque outil = un sous-dossier)."""
    dir_cat = os.path.join(TOOLS_DIR, categorie)

    # Cas special templates : outil-template (fichiers a la racine de tools/)
    if categorie == "templates":
        return 1 if os.path.isfile(os.path.join(TOOLS_DIR, "outil-template.md")) else 0

    if not os.path.isdir(dir_cat):
        return 0

    # Cas special tester : compter les protections (sous-dossiers de protections/)
    if categorie == "tester":
        protections = os.path.join(dir_cat, "protections")
        if not os.path.isdir(protections):
            return 0
        return len([d for d in os.listdir(protections) if os.path.isdir(os.path.join(protections, d))])

    # Cas special combos : compter les sous-dossiers
    if categorie == "combos":
        return len([d for d in os.listdir(dir_cat) if os.path.isdir(os.path.join(dir_cat, d))])

    return len([d for d in os.listdir(dir_cat) if os.path.isdir(os.path.join(dir_cat, d))])


def lister_outils_categorie(categorie):
    """Lister les outils reels d'une categorie (noms separes par ', ')."""
    dir_cat = os.path.join(TOOLS_DIR, categorie)

    if categorie == "templates":
        if os.path.isfile(os.path.join(TOOLS_DIR, "outil-template.md")):
            return "outil-template"
        return ""

    if not os.path.isdir(dir_cat):
        return ""

    if categorie == "tester":
        protections = os.path.join(dir_cat, "protections")
        if not os.path.isdir(protections):
            return ""
        noms = [f[:-3] for f in os.listdir(protections) if f.endswith(".md") and os.path.isfile(os.path.join(protections, f))]
        return ", ".join(sorted(noms))

    noms = [d for d in os.listdir(dir_cat) if os.path.isdir(os.path.join(dir_cat, d))]
    return ", ".join(sorted(noms))


def compter_total_outils():
    """Total des outils sur toutes les categories."""
    total = 0
    for cat in lister_categories():
        total += compter_outils_categorie(cat)
    return total


def lire_journal(n):
    """Lire les N dernieres interventions de l'historique (diagnostic uniquement)."""
    if not os.path.isfile(HISTORIQUE):
        return []
    lignes = []
    with io.open(HISTORIQUE, "r", encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            if ligne.startswith("| 20") or ligne.startswith("| 19"):
                lignes.append(ligne.rstrip("\n"))
    return lignes[:n]


def capitaliser(nom):
    """Capitaliser un nom (cerberus -> Cerberus)."""
    return nom[:1].upper() + nom[1:] if nom else nom


def nom_categorie_affichable(cle):
    """Nom de categorie affichable (capitalise + 'Mettre a jour')."""
    cat = capitaliser(cle)
    cat = cat.replace("Mettre-a-jour", "Mettre a jour")
    return cat


def lire_readme():
    """Lire le README complet."""
    with io.open(README, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def verifier():
    """Verifier l'etat reel et comparer avec le README."""
    total = compter_total_outils()
    print("=== ETAT REEL DU PROJET ===")
    print("")
    print("Agents reels : %d" % compter_agents())
    print("")
    print("Outils par categorie :")
    for cat in lister_categories():
        print("  %-14s : %d" % (cat, compter_outils_categorie(cat)))
    print("  TOTAL         : %d" % total)
    print("")
    print("=== ECARTS AVEC LE README ===")
    print("")

    contenu = lire_readme()

    # Agents manquants dans la table du README (casse insensible)
    ecart = 0
    for agent in lister_agents_reels():
        if not re.search(r"\*\*%s\*\*" % re.escape(agent), contenu, re.IGNORECASE):
            print("  [MANQUANT] Agent '%s' absent de la table 'Les agents'" % agent)
            ecart += 1
    if ecart == 0:
        print("  [OK] Tous les agents sont dans la table")

    # Titre boite a outils
    m = re.search(r"^## La boite a outils \(([0-9]*) outils\)", contenu, re.MULTILINE)
    if m:
        titre_actuel = int(m.group(1))
        if titre_actuel != total:
            print("  [OBSOLETE] Titre : 'La boite a outils (%d outils)' -> devrait etre %d" % (titre_actuel, total))
        else:
            print("  [OK] Titre 'La boite a outils (%d outils)'" % titre_actuel)
    else:
        print("  [MANQUANT] Titre 'La boite a outils' introuvable dans le README")

    # Compteurs et outils par categorie
    for cle in lister_categories():
        cat = nom_categorie_affichable(cle)
        nb = compter_outils_categorie(cle)
        m = re.search(r"\*\*%s \(([0-9]*)\)\*\*" % re.escape(cat), contenu)
        if m:
            lue = int(m.group(1))
            if lue != nb:
                print("  [OBSOLETE] %s : README dit %d, reel = %d" % (cat, lue, nb))
            else:
                print("  [OK] %s : %d" % (cat, nb))
        else:
            print("  [MANQUANT] %s : compteur introuvable (reel = %d)" % (cat, nb))

        # Outils manquants dans la liste de la categorie
        liste_reelle = lister_outils_categorie(cle)
        m2 = re.search(r"\*\*%s \([0-9]*\)\*\* \| ([^|]*)" % re.escape(cat), contenu)
        ligne_readme = m2.group(1) if m2 else ""
        for outil in [o.strip() for o in liste_reelle.split(",") if o.strip()]:
            nom = outil.split(": ")[-1]
            if nom and nom not in ligne_readme:
                print("  [MANQUANT] %s : outil '%s' absent de la liste" % (cat, nom))

    print("")
    print("Utilisez --maj pour corriger le texte du README.")


def mettre_a_jour():
    """Corriger le README pour qu'il reflete l'etat reel."""
    total = compter_total_outils()
    print("=== CORRECTION DU README ===")

    contenu = lire_readme()

    # 1. Titre boite a outils
    if re.search(r"^## La boite a outils \(([0-9]*) outils\)", contenu, re.MULTILINE):
        contenu = re.sub(r"^## La boite a outils \([0-9]* outils\)", "## La boite a outils (%d outils)" % total, contenu, count=1, flags=re.MULTILINE)
        print("  [CORRIGE] Titre : La boite a outils (%d outils)" % total)

    # 2. Compteurs par categorie
    for cle in lister_categories():
        cat = nom_categorie_affichable(cle)
        nb = compter_outils_categorie(cle)
        if re.search(r"\*\*%s \([0-9]*\)\*\*" % re.escape(cat), contenu):
            contenu = re.sub(r"\*\*%s \([0-9]*\)\*\*" % re.escape(cat), "**%s (%d)**" % (cat, nb), contenu)
            print("  [CORRIGE] %s : %d" % (cat, nb))

    # 3. Ajouter les agents manquants dans la table 'Les agents'
    agents_ajoutes = 0
    for agent in lister_agents_reels():
        if not re.search(r"\*\*%s\*\*" % re.escape(agent), contenu, re.IGNORECASE):
            role = lire_role_agent(agent)
            if not role:
                role = "Agent"
            nom_affichable = capitaliser(agent)
            ligne = "| **%s** | %s | Selon sa carte de decision |" % (nom_affichable, role)
            # Inserer la ligne avant '### Le cycle fondamental' (fin de la table des agents)
            if "### Le cycle fondamental" in contenu:
                contenu = contenu.replace("### Le cycle fondamental", ligne + "\n### Le cycle fondamental", 1)
            else:
                contenu += "\n" + ligne + "\n"
            print("  [AJOUTE] Agent '%s' ajoute dans la table" % nom_affichable)
            agents_ajoutes += 1
    if agents_ajoutes == 0:
        print("  [OK] Table des agents complete")

    # 4. Reconstruire la liste des outils de chaque categorie
    for cle in lister_categories():
        cat = nom_categorie_affichable(cle)
        nb = compter_outils_categorie(cle)
        liste_reelle = lister_outils_categorie(cle)
        # Format de ligne : | **Cat (N)** | liste outils | usage |
        # Decoupage par | : parties[0]="", parties[1]=" **Cat (N)** ", parties[2]="liste outils", parties[3]="usage"
        pattern = re.compile(r"^\| \*\*%s \(\d+\)\*\* \|[^|]*\|[^|]*\|" % re.escape(cat), re.MULTILINE)
        if pattern.search(contenu):
            def reconstruire(match):
                ligne_actuelle = match.group(0)
                # Conserver la colonne usage (4e partie apres decoupage par |)
                parties = ligne_actuelle.split("|")
                usage = parties[3].strip() if len(parties) >= 4 else ""
                return "| **%s (%d)** | %s | %s |" % (cat, nb, liste_reelle, usage)
            contenu = pattern.sub(reconstruire, contenu)
            print("  [RECONSTRUIT] %s : %d outils" % (cat, nb))

    with io.open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    print("")
    print("[OK] README corrige pour refleter l'etat reel.")


def encoder_badge(texte):
    """Encoder une portion de badge Shields (label ou message).

    Suit les conventions Shields : espace -> '_', tiret -> '--'.
    Tout caractere non-ASCII est rejete (regle immuable).
    """
    out = []
    for c in texte:
        if c == " ":
            out.append("_")
        elif c == "-":
            out.append("--")
        elif ord(c) > 127:
            raise ValueError("caractere non-ASCII dans un badge : %r" % c)
        else:
            out.append(c)
    return "".join(out)


def inserer_badges(spec):
    """Inserer des badges statiques Shields en tete du README.

    `spec` est une liste de badges separee par ';', chaque badge au format
    `label=message:couleur`. Chaque badge devient une image Markdown
    `[![label](url)](url)` pointee vers img.shields.io (badge statique).
    Idempotent : si une ligne de badges identique existe deja, n'insere rien.
    """
    badges = [b for b in spec.split(";") if b.strip()]
    if not badges:
        print("[ERREUR] Aucun badge fourni (spec vide).")
        return 1

    lignes = []
    for b in badges:
        b = b.strip()
        if "=" not in b or ":" not in b:
            print("[ERREUR] Badge invalide (attendu label=message:couleur) : %s" % b)
            return 1
        label, reste = b.split("=", 1)
        if ":" not in reste:
            print("[ERREUR] Badge invalide (couleur manquante) : %s" % b)
            return 1
        message, couleur = reste.rsplit(":", 1)
        label = label.strip()
        message = message.strip()
        couleur = couleur.strip()
        if not label or not message or not couleur:
            print("[ERREUR] Badge incomplet (label, message et couleur requis) : %s" % b)
            return 1
        try:
            # Encoder label et message + valider la couleur en ASCII
            label_enc = encoder_badge(label)
            message_enc = encoder_badge(message)
            if any(ord(c) > 127 for c in couleur):
                raise ValueError("caractere non-ASCII dans la couleur du badge : %r" % couleur)
            url = "https://img.shields.io/badge/%s-%s-%s?style=flat" % (
                label_enc, message_enc, couleur)
        except ValueError as e:
            print("[ERREUR] %s" % e)
            return 1
        lignes.append("[![%s](%s)](%s)" % (label, url, url))

    ligne_badges = " ".join(lignes)

    with io.open(README, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()

    if ligne_badges in contenu:
        print("[OK] Ces badges sont deja presents dans le README (aucun doublon).")
        return 0

    m = re.search(r"^# ", contenu, re.MULTILINE)
    if not m:
        print("[ERREUR] Aucun titre H1 (# ...) trouve : rien n'a ete insere.")
        return 1

    # Position apres la fin de la ligne H1 (include le saut de ligne si present)
    pos = m.end()
    nl = contenu.find("\n", pos)
    if nl != -1:
        pos = nl + 1

    contenu = contenu[:pos] + "\n" + ligne_badges + "\n\n" + contenu[pos:]

    with io.open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    print("[OK] %d badge(s) insere(s) en tete du README, apres le titre H1." % len(lignes))
    return 0


def inserer_logo(chemin_image):
    """Inserer une image (logo) en tete du README, juste apres le titre H1.

    Idempotent : si le chemin est deja present dans le README, n'insere rien.
    Le chemin (et l'alt) doivent etre en ASCII (regle immuable).
    """
    with io.open(README, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()

    if chemin_image in contenu:
        print("[OK] Le logo '%s' est deja present dans le README (aucun doublon)." % chemin_image)
        return 0

    m = re.search(r"^# ", contenu, re.MULTILINE)
    if not m:
        print("[ERREUR] Aucun titre H1 (# ...) trouve : rien n'a ete insere.")
        return 1

    # Position apres la fin de la ligne H1 (include le saut de ligne si present)
    pos = m.end()
    nl = contenu.find("\n", pos)
    if nl != -1:
        pos = nl + 1

    logo_md = "\n![Logo](%s)\n\n" % chemin_image
    contenu = contenu[:pos] + logo_md + contenu[pos:]

    with io.open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    print("[OK] Logo '%s' insere en tete du README, apres le titre H1." % chemin_image)
    return 0


def afficher_journal(n):
    """Afficher le journal (diagnostic, non inscrit au README)."""
    print("=== Dernieres interventions (%d) -- diagnostic ===" % n)
    for ligne in lire_journal(n):
        print(ligne)
    print("")
    print("Note : ces interventions servent a savoir CE QUI A CHANGE.")
    print("Le README est corrige (--maj), jamais rempli de lignes.")


def afficher_aide():
    print("=== mettre-a-jour-readme v%s ===" % VERSION)
    print("")
    print("Usage: mettre-a-jour-readme.py [OPTIONS]")
    print("")
    print("Options :")
    print("  --verifier         Comparer l'etat reel au README, lister les ecarts (sans modifier)")
    print("  --maj              Corriger le texte du README (agents, outils, compteurs)")
    print("  --journal [N]      Consulter les N dernieres interventions (diagnostic, non inscrit au README)")
    print("  --logo CHEMIN      Inserer une image (logo) en tete du README, apres le titre H1")
    print("  --badges SPEC      Inserer des badges statiques Shields (label=message:couleur;...), apres le titre H1")
    print("  --agents           Afficher le compte reel des agents")
    print("  --outils           Afficher le compte reel des outils par categorie")
    print("  --help             Afficher cette aide")
    print("")
    print("Exemples :")
    print("  mettre-a-jour-readme.py --verifier")
    print("  mettre-a-jour-readme.py --maj")
    print("  mettre-a-jour-readme.py --journal 5")
    print("  mettre-a-jour-readme.py --logo cerveau-projet/assets/images/logo.jpg")
    print("  mettre-a-jour-readme.py --badges \"Plateforme=Windows:blue;Statut=stable:brightgreen\"")


def main(argv):
    if "--help" in argv or "-h" in argv or not argv:
        afficher_aide()
        return 0

    if "--version" in argv:
        print("mettre-a-jour-readme v%s (%s)" % (VERSION, STATUT))
        return 0

    if not os.path.isfile(README):
        print("[ERREUR] Fichier README introuvable : %s" % README)
        return 1

    if "--verifier" in argv:
        verifier()
        return 0

    if "--maj" in argv:
        mettre_a_jour()
        return 0

    if "--journal" in argv:
        n = 10
        try:
            idx = argv.index("--journal")
            if idx + 1 < len(argv) and argv[idx + 1].isdigit():
                n = int(argv[idx + 1])
        except ValueError:
            pass
        afficher_journal(n)
        return 0

    if "--logo" in argv:
        idx = argv.index("--logo")
        if idx + 1 >= len(argv):
            print("[ERREUR] Option --logo necessite un chemin d'image.")
            return 1
        chemin_image = argv[idx + 1]
        if not os.path.isfile(chemin_image):
            print("[ERREUR] Fichier image introuvable : %s" % chemin_image)
            return 1
        return inserer_logo(chemin_image)

    if "--badges" in argv:
        idx = argv.index("--badges")
        if idx + 1 >= len(argv):
            print("[ERREUR] Option --badges necessite une specification (label=message:couleur;...).")
            return 1
        return inserer_badges(argv[idx + 1])

    if "--agents" in argv:
        print("Agents reels : %d" % compter_agents())
        return 0

    if "--outils" in argv:
        print("=== Outils par categorie ===")
        total = 0
        for cat in lister_categories():
            nb = compter_outils_categorie(cat)
            print("  %s : %d" % (cat, nb))
            total += nb
        print("  TOTAL : %d" % total)
        return 0

    verifier()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
