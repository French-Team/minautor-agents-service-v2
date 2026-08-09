#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-nommage.py

Verifie que le nommage est correct selon les conventions :
protocole (nom.XX.XX.statut.md), agent (nom-agent.md),
outil (nom-outil.sh/py/md avec prefixe du dossier),
convention (convention-nom.md). Mode recursif pour valider
tous les outils d'un dossier.

Mode --mots-seuls : applique la REGLE FONDAMENTALE "aucun mot seul"
(convention-renommage.md) : tout identifiant (cle YAML ou JSON) doit etre
compose d'au moins 2 mots (nom-agent, role-agent, statut-cerberus...).
Detecte les cles d'identification a un seul mot (nom, role, statut, id...)
dans les blocs YAML des fiches/frontmatter et les blocs identite/agent/profil
des fichiers JSON. Exceptions structurelles : type, commun, tags.

Utilisation:
  valider-nommage.py [OPTIONS] CHEMIN

Options:
  --aide, -h          Afficher l'aide
  --verbose, -v       Afficher les details
  --version           Afficher la version
  --type TYPE         Type de fichier (protocole, convention, agent, outil)
  --recursive, -r     Valider tous les outils d'un dossier
  --mots-seuls        Verifier la regle fondamentale 'aucun mot seul'

Proprietaire : Vulcain (outil partage)
Version : 0.3.1-py
Statut : prepare
"""

import io
import json
import os
import re
import sys

VERSION = "0.3.2-py"
STATUT = "prepare"

STATUTS_VALIDES = ("ebauche", "prepare", "dev", "test", "valide")

PATTERN_PROTOCOLE = re.compile(r"^([a-zA-Z0-9_-]+)\.(\d+)\.(\d+)\.([a-zA-Z]+)\.md$")
PATTERN_AGENT = re.compile(r"^[a-z]+\.md$")
PATTERN_OUTIL = re.compile(r"^[a-z-]+\.(sh|py|md)$")
PATTERN_CONVENTION = re.compile(r"^convention-[a-z-]+\.md$")

# Cles structurelles du format d'identite : autorisees a un seul mot
# (definies par le schema, pas des identifiants nommes).
EXCEPTIONS_STRUCTURELLES = ("type", "commun", "tags", "appartient_a")

# Cles de structure du schema de fiche : autorisees a un seul mot car
# definies par le template (version, cree, specialites, forces, faiblesses...).
CLES_SCHEMA_AUTORISEES = (
    "version", "cree", "specialites", "forces", "faiblesses", "config",
    "commandes", "outils", "parcours", "corrections", "fiche", "profil",
    "identite", "session", "agent", "raison", "mission",
)

# Identifiants generiques INTERDITS a un seul mot (le coeur de la regle) :
# nom, role, statut, id, date, cible, titre... -> doivent etre composes
# (nom-agent, role-agent, statut-cerberus, id-llm, date-mise-a-jour...).
MOTS_SEULS_INTERDITS = (
    "nom", "role", "statut", "id", "date", "cible", "titre", "description",
    "theme", "type_controle", "derniere", "mise",
)

# Regex d'une cle "mot seul" : uniquement des lettres minuscules, sans - ni _
PATTERN_CLE_MOT_SEUL = re.compile(r"^[a-z]+$")

# Blocs d'identification a verifier (racines YAML indentees ou objets JSON)
BLOCS_IDENTIFICATION = ("identite", "agent", "profil", "session")

# Dossiers de TRACES HISTORISEES ignores en mode recursif (documents figes
# qui documentent d'anciennes conventions -- comme corrections.md).
DOSSIERS_TRACES = ("controles", "rapports", "retro-actions", "historique", "exemples")

# Sous-dossiers COMPOSANTS d'un outil (pas des outils eux-memes) : ignores par
# le scan recursif de nommage. Ce sont des dossiers structurels de l'outil
# (tests/, spec/, caches) dont les fichiers ont leur propre convention de
# nommage (test-NNN-*, spec-*.XX.XX.ebauche.md) et ne doivent pas etre valides
# avec le prefixe de la categorie parente.
SOUS_DOSSERS_COMPOSANTS = ("tests", "spec", "protections", "__pycache__")

# Fichiers de TRACES DOCUMENTAIRES assumees (notes d'exemple YAML historiques,
# hors perimetre de la convention -- decision actee en mission precedente).
FICHIERS_TRACES = ("mission-condenseur.md",)


def afficher_aide():
    print("==========================================")
    print("  valider-nommage v%s" % VERSION)
    print("  Verifier le nommage selon les conventions")
    print("==========================================")
    print("")
    print("Usage: valider-nommage.py [OPTIONS] CHEMIN")
    print("")
    print("Options:")
    print("  --aide, -h          Afficher cette aide")
    print("  --verbose, -v       Afficher les details")
    print("  --version           Afficher la version")
    print("  --type TYPE         Type de fichier (protocole, convention, agent, outil)")
    print("  --recursive, -r     Valider tous les outils d'un dossier (ignore --type)")
    print("  --mots-seuls        Regle fondamentale 'aucun mot seul' (YAML/JSON)")
    print("")
    print("Types de fichiers:")
    print("  protocole     nom-protocole.XX.XX.statut.md")
    print("  agent         nom-agent.md")
    print("  outil         nom-outil.sh, nom-outil.py ou nom-outil.md")
    print("  convention    convention-nom.md")
    print("")
    print("Statuts valides (protocoles):")
    print("  ebauche, prepare, dev, test, valide")
    print("")
    print("Mode --mots-seuls:")
    print("  Applique la REGLE FONDAMENTALE : tout identifiant = 2+ mots.")
    print("  Detecte les IDENTIFIANTS generiques a un seul mot (nom, role, statut,")
    print("  id, date, cible...) dans les blocs YAML (agent:, profil:, identite:) et")
    print("  les objets JSON identite/agent/profil.")
    print("  Autorises : exceptions structurelles (type, commun, tags, appartient_a)")
    print("  et cles de schema de fiche (version, cree, specialites, forces...).")
    print("  En recursif : dossiers de traces ignores (controles, rapports,")
    print("  retro-actions, historique, exemples).")
    print("  Usage: valider-nommage.py --mots-seuls <fichier.md|.json|dossier>")
    print("")
    print("Exemples:")
    print("  valider-nommage.py --type protocole chemin/vers/protocole.md")
    print("  valider-nommage.py --type agent chemin/vers/agent.md")
    print("  valider-nommage.py --recursive cerveau-projet/agents/tools/")
    print("  valider-nommage.py --mots-seuls cerveau-projet/agents/cerberus/cerberus.md")
    print("  valider-nommage.py --mots-seuls --recursive cerveau-projet/agents/")


def valider_protocole(fichier, verbose):
    basename = os.path.basename(fichier)
    erreurs = 0

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    m = PATTERN_PROTOCOLE.match(basename)
    if not m:
        print("  [ERREUR] Format invalide : %s" % basename)
        print("    Attendu : nom-protocole.XX.XX.statut.md")
        return 1

    nom_part, major_part, minor_part, statut_part = m.groups()

    statut = statut_part
    if statut not in STATUTS_VALIDES:
        print("  [ERREUR] Statut invalide : %s" % statut)
        print("    Statuts valides : ebauche, prepare, dev, test, valide")
        return 1

    print("  [OK] Format valide : %s" % basename)
    if verbose:
        print("    Nom : %s" % nom_part)
        print("    Version : %s.%s" % (major_part, minor_part))
        print("    Statut : %s" % statut)
    return 0


def valider_agent(fichier, verbose):
    basename = os.path.basename(fichier)

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    if PATTERN_AGENT.match(basename):
        print("  [OK] Format valide : %s" % basename)
        return 0
    print("  [ERREUR] Format invalide : %s" % basename)
    print("    Attendu : nom-agent.md")
    return 1


def valider_convention(fichier, verbose):
    basename = os.path.basename(fichier)

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    if PATTERN_CONVENTION.match(basename):
        print("  [OK] Format valide : %s" % basename)
        return 0
    print("  [ERREUR] Format invalide : %s" % basename)
    print("    Attendu : convention-nom.md")
    return 1


def valider_outil(fichier, verbose, categorie=None):
    basename = os.path.basename(fichier)
    erreurs = 0

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    # Formats speciaux LEGITIMES (conventions dediees, hors nom-outil.sh/py/md) :
    #   - definition-combo.json : fichier canonique d'un combo (dossier combos/combo-*/)
    #   - test-XXX-nom-outil.(py|sh|md) : fichier de test formel (dossier tests/test-XXX-*/)
    dossier_parent = os.path.basename(os.path.dirname(os.path.abspath(fichier)))
    format_special_combo = (basename == "definition-combo.json" and dossier_parent.startswith("combo-"))
    format_special_test = (re.match(r"^test-\d+-[a-z0-9-]+\.(py|sh|md)$", basename)
                           and dossier_parent.startswith("test-"))

    if format_special_combo or format_special_test:
        print("  [OK] Format special reconnu : %s (convention %s)" % (
            basename, "definition-combo.json" if format_special_combo else "test-XXX-nom-outil"))
        if verbose:
            print("  [OK] Prefixe dossier respecte : %s/" % dossier_parent)
        return erreurs

    if not PATTERN_OUTIL.match(basename):
        print("  [ERREUR] Format invalide : %s" % basename)
        print("    Attendu : nom-outil.sh, nom-outil.py ou nom-outil.md")
        erreurs += 1

    nom = re.sub(r"\.(sh|py|md)$", "", basename)

    if not categorie:
        dossier_outil = os.path.dirname(os.path.abspath(fichier))
        categorie = os.path.basename(os.path.dirname(dossier_outil))

    if categorie and (nom == categorie or nom.startswith(categorie + "-")):
        if verbose:
            print("  [OK] Prefixe dossier respecte : %s/" % categorie)
    else:
        print("  [ERREUR] Prefixe dossier manquant : %s" % basename)
        print("    Le nom doit commencer par '%s-' (dossier: %s/)" % (categorie, categorie))
        erreurs += 1

    return erreurs



def valider_recursif(dossier, verbose):
    total = 0
    ok = 0
    ko = 0

    print("=== Validation recursive des outils dans : %s ===" % dossier)
    print("")

    # Structure: tools/categorie/outil/
    if not os.path.isdir(dossier):
        print("Erreur: '%s' n'est pas un dossier" % dossier)
        return 1

    try:
        entrees = sorted(os.listdir(dossier))
    except OSError:
        print("Erreur: Impossible de lire le dossier '%s'" % dossier)
        return 1

    for categorie_nom in entrees:
        if categorie_nom in SOUS_DOSSERS_COMPOSANTS:
            continue
        chemin_cat = os.path.join(dossier, categorie_nom)
        if not os.path.isdir(chemin_cat):
            continue
        try:
            sous = sorted(os.listdir(chemin_cat))
        except OSError:
            continue
        for outil_nom in sous:
            if outil_nom in SOUS_DOSSERS_COMPOSANTS:
                continue
            chemin_outil = os.path.join(chemin_cat, outil_nom)
            if not os.path.isdir(chemin_outil):
                continue
            for f in sorted(os.listdir(chemin_outil)):
                if f.endswith((".sh", ".py", ".md")):
                    total += 1
                    code = valider_outil(os.path.join(chemin_outil, f), verbose, categorie_nom)
                    if code == 0:
                        ok += 1
                    else:
                        ko += 1
                    print("")

    print("=== Resume ===")
    print("  Total : %d" % total)
    print("  OK : %d" % ok)
    if ko > 0:
        print("  Erreurs : %d" % ko)
    else:
        print("  Erreurs : 0")
    return ko


def cle_est_mot_seul_interdit(cle):
    """Retourne True si la cle est un identifiant generique a un seul mot
    (interdit par la regle fondamentale). Les cles de schema et les
    exceptions structurelles sont autorisees."""
    if not PATTERN_CLE_MOT_SEUL.match(cle):
        return False
    if cle in EXCEPTIONS_STRUCTURELLES:
        return False
    if cle in CLES_SCHEMA_AUTORISEES:
        return False
    return cle in MOTS_SEULS_INTERDITS


def verifier_cle_mot_seul(cle, contexte, rapport):
    """Ajoute la cle a rapport si c'est un identifiant generique interdit."""
    if cle_est_mot_seul_interdit(cle):
        rapport.append("%s : cle '%s' = IDENTIFIANT MOT SEUL (regle fondamentale : 2+ mots)" % (contexte, cle))


def verifier_yaml_md(contenu, fichier, rapport):
    """Analyse les blocs YAML indentees (agent:, profil:, identite:, session:)
    et le frontmatter d'un fichier .md/.py/.sh. Signale les cles a un seul mot.
    Le bloc courant est suivi : une cle racine (agent:) active la surveillance,
    une cle de sous-bloc (  nom:) est verifiee si le bloc courant est
    un bloc d'identification."""
    lignes = contenu.split("\n")
    dans_frontmatter = False
    bloc_courant = ""
    for num, ligne in enumerate(lignes, start=1):
        # Frontmatter : bloc entre deux lignes '---'
        if ligne.strip() == "---":
            if not dans_frontmatter and num == 1:
                dans_frontmatter = True
                continue
            if dans_frontmatter:
                dans_frontmatter = False
                continue
        # Frontmatter commente (.py/.sh) : '# identite:' (racine, 1 espace)
        #                         et '#   cle:' (sous-cle, 3 espaces)
        mh = re.match(r"^# [a-zA-Z0-9_-]+:", ligne)
        if mh:
            racine = mh.group(0)[2:-1].strip()
            bloc_courant = racine if racine in BLOCS_IDENTIFICATION else ""
            continue
        mh2 = re.match(r"^#   ([a-zA-Z0-9_-]+):", ligne)
        if mh2:
            cle = mh2.group(1)
            if bloc_courant in BLOCS_IDENTIFICATION:
                verifier_cle_mot_seul(cle, "%s:%d" % (fichier, num), rapport)
            continue
        # Bloc YAML indentee de 2 espaces : '  cle: valeur'
        m = re.match(r"^  ([a-zA-Z0-9_-]+):", ligne)
        if m:
            cle = m.group(1)
            if bloc_courant in BLOCS_IDENTIFICATION:
                verifier_cle_mot_seul(cle, "%s:%d" % (fichier, num), rapport)
            continue
        # Ligne racine YAML non indentee : 'agent:', 'profil:', ...
        pm = re.match(r"^([a-zA-Z0-9_-]+):", ligne)
        if pm:
            racine = pm.group(1)
            bloc_courant = racine if racine in BLOCS_IDENTIFICATION else ""
            continue
        # Ligne racine dans le frontmatter YAML : identite:, agent:, ...
        if dans_frontmatter:
            fm = re.match(r"^([a-zA-Z0-9_-]+):", ligne)
            if fm:
                bloc_courant = fm.group(1) if fm.group(1) in BLOCS_IDENTIFICATION else ""
                continue


def verifier_json(contenu, fichier, rapport):
    """Analyse un fichier JSON : cles des objets identite/agent/profil."""
    try:
        data = json.loads(contenu)
    except ValueError as e:
        rapport.append("%s : JSON invalide (%s)" % (fichier, e))
        return

    def parcourir(obj, chemin):
        if isinstance(obj, dict):
            for cle, valeur in obj.items():
                if cle in BLOCS_IDENTIFICATION and isinstance(valeur, dict):
                    for scle in valeur.keys():
                        verifier_cle_mot_seul(scle, "%s:%s" % (fichier, chemin + cle), rapport)
                else:
                    parcourir(valeur, chemin + cle + "/")

    parcourir(data, "")


def verifier_mots_seuls_fichier(fichier):
    """Applique la regle fondamentale 'aucun mot seul' a un fichier."""
    basename = os.path.basename(fichier)
    print("[CHECKLIST] Regle fondamentale 'aucun mot seul' : %s" % basename)
    print("")

    if not os.path.isfile(fichier):
        print("  [ERREUR] Le fichier '%s' n'existe pas" % fichier)
        return 1

    try:
        with io.open(fichier, encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
    except OSError as e:
        print("  [ERREUR] Lecture impossible : %s" % e)
        return 1

    rapport = []
    if fichier.endswith(".md"):
        verifier_yaml_md(contenu, fichier, rapport)
    elif fichier.endswith(".json"):
        verifier_json(contenu, fichier, rapport)
    elif fichier.endswith((".py", ".sh")):
        verifier_yaml_md(contenu, fichier, rapport)
    else:
        print("  [ERREUR] Extension non analysee (md, json, py ou sh requis)")
        return 1

    if rapport:
        for r in rapport:
            print("  [ERREUR] %s" % r)
        print("")
        print("  Total : %d mot(s) seul(s) detecte(s)" % len(rapport))
        return len(rapport)
    print("  [OK] Aucun mot seul detecte")
    return 0


def verifier_mots_seuls_recursif(dossier):
    """Applique la regle a tous les .md et .json d'un dossier (recursif)."""
    if not os.path.isdir(dossier):
        print("Erreur: '%s' n'est pas un dossier" % dossier)
        return 1

    total = 0
    ko = 0
    print("=== Regle fondamentale 'aucun mot seul' (recursif) : %s ===" % dossier)
    print("")
    for racine, sous_dossiers, fichiers in os.walk(dossier):
        # Ignorer les caches, dossiers masques et dossiers de traces historisees
        sous_dossiers[:] = [d for d in sous_dossiers if not d.startswith("__") and d not in DOSSIERS_TRACES]
        for f in sorted(fichiers):
            if f.endswith((".md", ".json")) and f not in FICHIERS_TRACES:
                chemin = os.path.join(racine, f)
                total += 1
                code = verifier_mots_seuls_fichier(chemin)
                if code != 0:
                    ko += 1
                print("")

    print("=== Resume ===")
    print("  Fichiers analyses : %d" % total)
    if ko > 0:
        print("  Fichiers avec mots seuls : %d" % ko)
    else:
        print("  Fichiers avec mots seuls : 0")
    return ko


def main(argv):
    verbose = False
    type_fichier = ""
    fichier = ""
    recursif = False
    mots_seuls = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "-h"):
            afficher_aide()
            return 0
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg == "--version":
            print("valider-nommage v%s" % VERSION)
            return 0
        elif arg == "--type":
            if i + 1 < len(argv):
                type_fichier = argv[i + 1]
                i += 1
        elif arg in ("--recursive", "-r"):
            recursif = True
        elif arg == "--mots-seuls":
            mots_seuls = True
        elif arg.startswith("-"):
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        else:
            fichier = arg
        i += 1

    if mots_seuls:
        if not fichier:
            print("Erreur: Aucun fichier ou dossier specifie pour --mots-seuls")
            return 1
        if recursif:
            return verifier_mots_seuls_recursif(fichier)
        return verifier_mots_seuls_fichier(fichier)

    if recursif:
        if not fichier:
            print("Erreur: Aucun dossier specifie pour --recursive")
            return 1
        return valider_recursif(fichier, verbose)

    if not fichier:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    if not os.path.isfile(fichier):
        print("Erreur: Le fichier '%s' n'existe pas" % fichier)
        return 1

    if not type_fichier:
        print("Erreur: Type non specifie")
        print("Utilisez --type pour specifier le type")
        return 1

    if type_fichier == "protocole":
        return valider_protocole(fichier, verbose)
    if type_fichier == "agent":
        return valider_agent(fichier, verbose)
    if type_fichier == "outil":
        return valider_outil(fichier, verbose)
    if type_fichier == "convention":
        return valider_convention(fichier, verbose)

    print("Erreur: Type inconnu '%s'" % type_fichier)
    print("Types disponibles : protocole, agent, outil, convention")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
