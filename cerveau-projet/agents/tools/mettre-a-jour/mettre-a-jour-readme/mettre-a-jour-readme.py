#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
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
Version : 0.4.8-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.4.8-py"
STATUT = "prepare"

README = "README.md"
README_DEV = "cerveau-projet/readme-dev.md"
HISTORIQUE = "AGENTS-historique.md"
AGENTS_DIR = "cerveau-projet/agents"
TOOLS_DIR = "cerveau-projet/agents/tools"

CATEGORIES_EXCLUES = {"combos"}


def _est_outil(nom):
    """Un outil est un sous-dossier reel (jamais un dossier technique)."""
    return nom != "" and not nom.startswith("__")


def compter_agents():
    """Compter les agents d action (dossier avec parcours JSON)."""
    nb = 0
    if not os.path.isdir(AGENTS_DIR):
        return 0
    for nom in os.listdir(AGENTS_DIR):
        dossier = os.path.join(AGENTS_DIR, nom)
        if not (os.path.isdir(dossier) and nom != "tools"):
            continue
        # Un agent d action a un arbre v2 : agents/<nom>/parcours/arbre-<nom>.json
        # (migration v1->v2 : les parcours v1 sont retires)
        if os.path.isfile(os.path.join(dossier, "parcours", "arbre-" + nom + ".json")):
            nb += 1
    return nb


def lister_agents_reels():
    """Lister les agents reels (noms des dossiers)."""
    resultat = []
    if not os.path.isdir(AGENTS_DIR):
        return resultat
    for nom in os.listdir(AGENTS_DIR):
        dossier = os.path.join(AGENTS_DIR, nom)
        if not (os.path.isdir(dossier) and nom != "tools"):
            continue
        # Un agent d action a un arbre v2 : agents/<nom>/parcours/arbre-<nom>.json
        # (migration v1->v2 : les parcours v1 sont retires)
        parcours_dir = os.path.join(dossier, "parcours")
        if os.path.isdir(parcours_dir) and os.path.isfile(os.path.join(parcours_dir, "arbre-" + nom + ".json")):
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
    """Lister les categories d'outils (chaque sous-dossier, plus combos et templates).

    v0.4.7 : les dossiers techniques (__pycache__, __MACOSX...) ne sont pas
    des categories.
    """
    categories = []
    if os.path.isdir(TOOLS_DIR):
        for nom in sorted(os.listdir(TOOLS_DIR)):
            chemin = os.path.join(TOOLS_DIR, nom)
            if os.path.isdir(chemin) and nom not in CATEGORIES_EXCLUES and _est_outil(nom):
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
        return len([d for d in os.listdir(protections) if _est_outil(d) and os.path.isdir(os.path.join(protections, d))])

    # v0.4.7 : un dossier technique (__pycache__) n'est pas un outil
    return len([d for d in os.listdir(dir_cat) if _est_outil(d) and os.path.isdir(os.path.join(dir_cat, d))])


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

    noms = [d for d in os.listdir(dir_cat) if _est_outil(d) and os.path.isdir(os.path.join(dir_cat, d))]
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
            # v0.4.3 : les entrees commencent par '| <span' (agent colore en
            # 1re colonne, format v0.5.15 de l historique)
            if ligne.startswith("| <span"):
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


def extraire_table_agents(contenu):
    """Region de la table 'Mes agents' du README public : du titre
    '## Mes agents' jusqu'au titre suivant (### ou ##).

    v0.4.8 : la presence des agents est verifiee DANS CETTE TABLE
    uniquement. Avant, la recherche se faisait dans tout le fichier : une
    mention narrative ('**Oracle**' dans 'Mon pilote : Oracle') ou des
    lignes orphelines en fin de fichier masquaient des agents absents de
    la table.

    Retourne (region, pos_insertion) :
      - region : texte depuis le titre jusqu'au titre suivant (exclu)
      - pos_insertion : index ou inserer de nouvelles lignes (juste avant
        le titre suivant), None si aucun titre suivant.
    """
    marque = "## Mes agents"
    pos = contenu.find(marque)
    if pos == -1:
        return contenu, None
    pos += len(marque)
    m = re.search(r"^### |^## ", contenu[pos:], re.MULTILINE)
    if not m:
        return contenu[pos:], None
    return contenu[pos:pos + m.start()], pos + m.start()


def verifier_somme_comptes():
    """Verifier que la SOMME des compteurs du tableau readme-dev (section 6)
    = le total reel calcule. Anti-recurrence du bug Clio (compteurs 132 vs
    134 : une categorie manquante + une sur-comptee passaient inapercues
    car chaque ligne etait verifiee separement).

    Retourne le nombre d'ecarts (0 = coherent).
    """
    ecarts = 0
    if not os.path.isfile(README_DEV):
        print("  [MANQUANT] readme-dev introuvable : %s" % README_DEV)
        return 1
    with io.open(README_DEV, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    total = compter_total_outils()
    somme = 0
    nb_lignes = 0
    for ligne in contenu.split("\n"):
        m = re.match(r"^\| ([A-Z][^|]*?) \| (\d+) \|", ligne)
        if not m:
            continue
        nom = m.group(1).strip()
        if nom == "Categorie":
            continue
        nb = int(m.group(2))
        somme += nb
        nb_lignes += 1
        # Comparer le compte du tableau au compte reel (meme logique que
        # compter_outils_categorie, par dossier de categorie).
        cle = nom.lower().replace(" ", "-")
        reel = compter_outils_categorie(cle)
        if reel != nb:
            print("  [ECART] %s : tableau dit %d, reel = %d" % (nom, nb, reel))
            ecarts += 1
    if somme != total:
        print("  [ECART SOMME] readme-dev tableau : somme = %d, total reel = %d" % (somme, total))
        ecarts += 1
    if ecarts == 0:
        print("  [OK] readme-dev tableau : %d categories, somme %d = total reel %d" % (nb_lignes, somme, total))
    return ecarts


def aligner_badges_header():
    """Aligner les badges du header du README public sur les comptes reels :
    les 2 occurrences (affichage img + href) de 'Outils-N' et 'Agents-N'.

    v0.4.6 (lecon Clio/Janus) : --maj corrigeait les tables mais pas les
    badges en dur du header.
    """
    if not os.path.isfile(README):
        return
    with io.open(README, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    modifie = False
    for nom, reel in (("Outils", compter_total_outils()), ("Agents", compter_agents())):
        pattern = re.compile(r"badge/%s-\d+-" % nom)
        if pattern.search(contenu):
            nouveau = pattern.sub("badge/%s-%d-" % (nom, reel), contenu)
            if nouveau != contenu:
                contenu = nouveau
                modifie = True
                print("  [CORRIGE] Badge %s aligne : %d (affichage + href)." % (nom, reel))
    if modifie:
        with io.open(README, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(contenu)
    else:
        print("  [OK] Badges du header deja a jour.")


def corriger_readme_dev():
    """Corriger readme-dev : tableau section 6 (comptes reels par categorie,
    categories obsoletes retirees, manquantes ajoutees) + ligne d'intro +
    lignes de synthese (section 1 : Agents, Outils).

    v0.4.6 (anti-recurrence bug Clio 132 vs 134) : verifier SANS corriger ne
    suffisait pas -- on reconstruit le tableau lui-meme.
    v0.4.7 : la ligne de separation |---|---| est conservee, les exemples
    deja curates sont conserves (sauf si '__pycache__' s y est glisse), et
    les lignes de synthese de la section 1 sont corrigees aussi.
    """
    if not os.path.isfile(README_DEV):
        print("  [MANQUANT] readme-dev introuvable : %s" % README_DEV)
        return
    with io.open(README_DEV, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    modifie = False

    categories = [c for c in lister_categories() if compter_outils_categorie(c) > 0]
    total = compter_total_outils()

    # 1. Ligne d'intro '**N outils dans M categories** :'
    m_intro = re.search(r"^\*\*[0-9]+ outils dans [0-9]+ categories\*\* :", contenu, re.MULTILINE)
    if m_intro:
        nouveau = "**%d outils dans %d categories** :" % (total, len(categories))
        if m_intro.group(0) != nouveau:
            contenu = contenu.replace(m_intro.group(0), nouveau, 1)
            modifie = True
            print("  [CORRIGE] readme-dev intro : %d outils / %d categories" % (total, len(categories)))

    # 2. Tableau section 6 : reperer l'entete puis les lignes de donnees
    lignes = contenu.split("\n")
    idx_entete = None
    for i, ligne in enumerate(lignes):
        if re.match(r"^\| Categorie \| Nb \| Exemples \|$", ligne.strip()):
            idx_entete = i
            break
    if idx_entete is None:
        # Structure absente : rien a corriger (l outil ne cree pas la section)
        return
    fin = idx_entete + 2
    exemples = {}
    while fin < len(lignes):
        m = re.match(r"^\| ([A-Za-z][^|]*?) \| (\d+) \| (.*?) \|\s*$", lignes[fin])
        if not m:
            break
        exemples[m.group(1).strip()] = m.group(3).strip()
        fin += 1

    nouvelles = []
    for cle in categories:
        cat = nom_categorie_affichable(cle)
        nb = compter_outils_categorie(cle)
        ex = exemples.get(cat, "")
        if not ex or "__pycache__" in ex:
            ex = lister_outils_categorie(cle)
        nouvelles.append("| %s | %d | %s |" % (cat, nb, ex))

    ancien_bloc = "\n".join(lignes[idx_entete + 2:fin])
    nouveau_bloc = "\n".join(nouvelles)
    if ancien_bloc != nouveau_bloc:
        lignes[idx_entete + 2:fin] = nouvelles
        contenu = "\n".join(lignes)
        modifie = True
        print("  [CORRIGE] Tableau readme-dev section 6 : %d categories (%d outils)." % (len(nouvelles), total))
    else:
        print("  [OK] Tableau readme-dev section 6 deja a jour (%d categories)." % len(nouvelles))

    # 3. Lignes de synthese de la section 1 (Agents / Outils)
    syntheses = (
        ("Agents", "%d agents + classeur-variables (voir section 4)" % compter_agents()),
        ("Outils", "%d outils dans %d categories (voir section 6)" % (total, len(categories))),
    )
    for nom, valeur in syntheses:
        m = re.search(r"^\| \*\*%s\*\* \| [^|]* \|\s*$" % nom, contenu, re.MULTILINE)
        if m:
            nouveau = "| **%s** | %s |" % (nom, valeur)
            if m.group(0).strip() != nouveau:
                contenu = contenu.replace(m.group(0), nouveau, 1)
                modifie = True
                print("  [CORRIGE] readme-dev synthese %s : %s" % (nom, valeur))

    if modifie:
        with io.open(README_DEV, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(contenu)


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

    # Agents manquants dans la table 'Mes agents' du README public.
    # v0.4.8 : presence verifiee DANS LA TABLE uniquement (lignes
    # '| **Agent** |'), pas dans tout le fichier.
    region, _pos = extraire_table_agents(contenu)
    ecart = 0
    for agent in lister_agents_reels():
        if not re.search(r"^\| \*\*%s\*\* \|" % re.escape(agent), region, re.MULTILINE | re.IGNORECASE):
            print("  [MANQUANT] Agent '%s' absent de la table 'Mes agents'" % agent)
            ecart += 1
    if ecart == 0:
        print("  [OK] Tous les agents sont dans la table 'Mes agents'")

    # Badge Outils du README public (nouvelle norme 1ere personne 20/08) :
    # la liste technique exhaustive vit dans readme-dev (section 6), pas dans
    # le README public. Le verifier tolere l absence de la section 'La boite
    # a outils' (ancien format) et s appuie sur readme-dev pour les compteurs.
    badge = re.search(r"Outils-(\d+)", contenu)
    if badge:
        lue = int(badge.group(1))
        if lue != total:
            print("  [OBSOLETE] Badge Outils-%d -> devrait etre %d" % (lue, total))
        else:
            print("  [OK] Badge Outils-%d (README public)" % lue)

    # Badge Agents du README public (v0.4.6)
    badge_agents = re.search(r"Agents-(\d+)", contenu)
    if badge_agents:
        lue = int(badge_agents.group(1))
        reel = compter_agents()
        if lue != reel:
            print("  [OBSOLETE] Badge Agents-%d -> devrait etre %d" % (lue, reel))
        else:
            print("  [OK] Badge Agents-%d (README public)" % lue)
    if re.search(r"^## La boite a outils \(([0-9]*) outils\)", contenu, re.MULTILINE):
        print("  [INFO] Section 'La boite a outils' encore presente (ancien format) : compteurs verifies ci-dessous")
    else:
        print("  [INFO] README public sans section 'La boite a outils' (nouvelle norme) : compteurs verifies dans readme-dev (section 6)")

    # Compteurs et outils par categorie : uniquement si l ancienne section
    # 'La boite a outils' existe encore dans le README public
    # (retro-compatibilite). Nouvelle norme : les compteurs par categorie et
    # les listes d outils vivent dans readme-dev (section 6), verifies par
    # verifier_somme_comptes() ci-dessous.
    ancienne_section = re.search(r"^## La boite a outils \(([0-9]*) outils\)", contenu, re.MULTILINE)
    if ancienne_section:
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

            # Outils manquants dans la liste de la categorie
            liste_reelle = lister_outils_categorie(cle)
            m2 = re.search(r"\*\*%s \([0-9]*\)\*\* \| ([^|]*)" % re.escape(cat), contenu)
            ligne_readme = m2.group(1) if m2 else ""
            for outil in [o.strip() for o in liste_reelle.split(",") if o.strip()]:
                nom = outil.split(": ")[-1]
                if nom and nom not in ligne_readme:
                    print("  [MANQUANT] %s : outil '%s' absent de la liste" % (cat, nom))

    # Somme des compteurs du readme-dev (anti-recurrence bug Clio 132 vs 134)
    print("")
    print("=== README-DEV (tableau des categories, section 6) ===")
    verifier_somme_comptes()

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

    # 3. Ajouter les agents manquants dans la table 'Mes agents' du README
    # public. v0.4.8 : la presence est verifiee dans la table uniquement
    # (region entre '## Mes agents' et le titre suivant), et l'insertion se
    # fait en fin de table au format 2 colonnes de cette table. Avant :
    # recherche globale + ancre obsolete ('### Le cycle fondamental') +
    # format 3 colonnes creaient des lignes orphelines en fin de fichier.
    region, pos_insertion = extraire_table_agents(contenu)
    manquants = []
    for agent in lister_agents_reels():
        if not re.search(r"^\| \*\*%s\*\* \|" % re.escape(agent), region, re.MULTILINE | re.IGNORECASE):
            manquants.append(agent)
    if manquants:
        lignes = []
        for agent in manquants:
            role = lire_role_agent(agent)
            if not role:
                role = "Agent"
            lignes.append("| **%s** | %s |" % (capitaliser(agent), role))
        bloc = "".join(l + "\n" for l in lignes)
        if pos_insertion is not None:
            # Coller le bloc a la derniere ligne de la table : la ligne
            # blanche qui precedait le titre suivant passe apres le bloc.
            debut = contenu[:pos_insertion]
            if debut.endswith("\n\n"):
                debut = debut[:-1]
            contenu = debut + bloc + "\n" + contenu[pos_insertion:]
        else:
            contenu += "\n" + bloc + "\n"
        for agent in manquants:
            print("  [AJOUTE] Agent '%s' ajoute dans la table 'Mes agents'" % capitaliser(agent))
    else:
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

    # 5. Aligner les badges du header (Outils-N, Agents-N) : affichage + href
    # (lecon Clio/Janus : --maj corrigeait les tables mais pas les badges)
    aligner_badges_header()

    # 6. Corriger le tableau readme-dev (section 6) : comptes reels par
    # categorie, categories obsoletes retirees, manquantes ajoutees
    # (anti-recurrence bug Clio 132 vs 134 : verifier SANS corriger ne
    # suffisait pas - v0.4.6 corrige le tableau lui-meme)
    corriger_readme_dev()

    print("")
    print("[OK] README corrige pour refleter l'etat reel.")
    print("")
    print("=== CONTROLE FINAL : somme des compteurs readme-dev ===")
    if verifier_somme_comptes() == 0:
        print("[OK] somme des compteurs = total reel (readme-dev coherent).")
    else:
        print("[ECART] readme-dev incoherent - corriger le tableau (section 6) avant de conclure.")


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
    print("  --dry-run          Preview AVANT/APRES sans ecrire (obligatoire avant --maj)")
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
    print("  mettre-a-jour-readme.py --dry-run")
    print("  mettre-a-jour-readme.py --maj")
    print("  mettre-a-jour-readme.py --journal 5")
    print("  mettre-a-jour-readme.py --logo cerveau-projet/assets/images/logo.jpg")
    print("  mettre-a-jour-readme.py --badges \"Plateforme=Windows:blue;Statut=stable:brightgreen\"")


def dry_run():
    """Mode dry-run : montrer le AVANT/APRES sans ecrire.
    Affiche les changements qui seraient faits par --maj.
    Regle Clio : dry-run OBLIGATOIRE avant toute modification."""
    total = compter_total_outils()
    print("=== DRY-RUN (preview AVANT/APRES) ===")
    print("")
    print("Ce qui changerait avec --maj :")
    print("")

    contenu = lire_readme()
    changements = []

    # 1. Titre boite a outils
    m = re.search(r"^## La boite a outils \(([0-9]*) outils\)", contenu, re.MULTILINE)
    if m:
        titre_actuel = int(m.group(1))
        if titre_actuel != total:
            changements.append("Titre : '%d outils' -> '%d outils'" % (titre_actuel, total))

    # 2. Compteurs par categorie
    for cle in lister_categories():
        cat = nom_categorie_affichable(cle)
        nb = compter_outils_categorie(cle)
        m = re.search(r"\*\*%s \(([0-9]*)\)\*\*" % re.escape(cat), contenu)
        if m:
            lue = int(m.group(1))
            if lue != nb:
                changements.append("%s : %d -> %d" % (cat, lue, nb))

    # 3. Agents manquants (v0.4.8 : dans la table 'Mes agents' uniquement,
    # pas dans tout le fichier -- une mention narrative ou une ligne
    # orpheline masquait les absents de la table)
    region, _pos = extraire_table_agents(contenu)
    agents_manquants = []
    for agent in lister_agents_reels():
        if not re.search(r"^\| \*\*%s\*\* \|" % re.escape(agent), region, re.MULTILINE | re.IGNORECASE):
            agents_manquants.append(capitaliser(agent))
    if agents_manquants:
        changements.append("Agents a ajouter : %s" % ", ".join(agents_manquants))

    # 4. Badges du header (Outils-N, Agents-N) : affichage + href
    for nom, reel in (("Outils", total), ("Agents", compter_agents())):
        mb = re.search(r"badge/%s-(\d+)-" % nom, contenu)
        if mb and int(mb.group(1)) != reel:
            changements.append("Badge %s : %d -> %d (affichage + href)" % (nom, int(mb.group(1)), reel))

    # 5. readme-dev : intro, categories obsoletes/manquantes, synthese
    if os.path.isfile(README_DEV):
        with io.open(README_DEV, "r", encoding="utf-8", errors="replace") as fh:
            contenu_dev = fh.read()
        categories_actives = [c for c in lister_categories() if compter_outils_categorie(c) > 0]
        m_intro = re.search(r"^\*\*([0-9]+) outils dans ([0-9]+) categories\*\* :", contenu_dev, re.MULTILINE)
        if m_intro and (int(m_intro.group(1)), int(m_intro.group(2))) != (total, len(categories_actives)):
            changements.append("readme-dev intro : '%s outils dans %s categories' -> '%d outils dans %d categories'"
                               % (m_intro.group(1), m_intro.group(2), total, len(categories_actives)))
        noms_tableau = set()
        for ligne in contenu_dev.split("\n"):
            m_row = re.match(r"^\| ([A-Z][^|]*?) \| (\d+) \| .* \|\s*$", ligne)
            if m_row and m_row.group(1).strip() != "Categorie":
                noms_tableau.add(m_row.group(1).strip())
        obsoletes = [n for n in sorted(noms_tableau) if n.lower().replace(" ", "-") not in [c.lower() for c in categories_actives]]
        if obsoletes:
            changements.append("readme-dev categories obsoletes a retirer : %s" % ", ".join(obsoletes))
        manquantes = [nom_categorie_affichable(c) for c in categories_actives
                      if nom_categorie_affichable(c) not in noms_tableau]
        if manquantes:
            changements.append("readme-dev categories manquantes a ajouter : %s" % ", ".join(manquantes))
        for nom, valeur in (("Agents", "%d agents + classeur-variables (voir section 4)" % compter_agents()),
                            ("Outils", "%d outils dans %d categories (voir section 6)" % (total, len(categories_actives)))):
            m_syn = re.search(r"^\| \*\*%s\*\* \| [^|]* \|\s*$" % nom, contenu_dev, re.MULTILINE)
            if m_syn and m_syn.group(0).strip() != "| **%s** | %s |" % (nom, valeur):
                changements.append("readme-dev synthese %s a corriger" % nom)

    # 6. Outils manquants par categorie : uniquement si l ancienne section
    # 'La boite a outils' existe dans le README public (retro-compatibilite).
    # Nouvelle norme : les listes d outils vivent dans readme-dev (section 6).
    if re.search(r"^## La boite a outils \(([0-9]*) outils\)", contenu, re.MULTILINE):
        for cle in lister_categories():
            cat = nom_categorie_affichable(cle)
            liste_reelle = lister_outils_categorie(cle)
            m2 = re.search(r"\*\*%s \([0-9]*\)\*\* \| ([^|]*)" % re.escape(cat), contenu)
            ligne_readme = m2.group(1) if m2 else ""
            outils_manquants = []
            for outil in [o.strip() for o in liste_reelle.split(",") if o.strip()]:
                nom = outil.split(": ")[-1]
                if nom and nom not in ligne_readme:
                    outils_manquants.append(nom)
            if outils_manquants:
                changements.append("%s : outils a ajouter : %s" % (cat, ", ".join(outils_manquants)))

    if not changements:
        print("  [AUCUN CHANGEMENT] Le README est deja a jour.")
    else:
        for i, chgt in enumerate(changements, 1):
            print("  %d. %s" % (i, chgt))

    print("")
    print("=== FIN DRY-RUN ===")
    print("Pour appliquer ces changements, utilisez --maj.")
    return 0


def main(argv):
    if "--help" in argv or "-h" in argv or "--aide" in argv or not argv:
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

    if "--dry-run" in argv:
        return dry_run()

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
