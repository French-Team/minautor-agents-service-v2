#!/usr/bin/env python3
# -*- coding: ascii -*-
# mettre-a-jour-versions.py
#
# LE BUMPER SYSTEMATIQUE : met a jour la version d une cible sur TOUS ses
# fichiers porteurs de version, en un seul passage, avec detection auto de la
# version actuelle, dry-run par defaut et verification de coherence post-bump.
#
# Lecons prises en compte :
#   - chrono-haut (2026-08-13) : un bump doit couvrir py + sh + md + SPEC
#     (la spec avait ete oubliee -> test-028 KO)
#   - les tests de version (004/005/007/016) cassent a chaque bump manuel
#   - la coherence catalogue (154 commandes) doit rester exacte
#
# Formats de version supportes (verifies sur le projet) :
#   1. Outil .py  : ligne en-tete '# Version : X.Y.Z' + constante VERSION = "X.Y.Z"
#   2. Outil .sh  : ligne '# Version : X.Y.Z' + VERSION="X.Y.Z"
#   3. Outil .md  : '**Version :** X.Y.Z'
#   4. Spec .md   : '**Version :** X.Y.Z' (dossier spec/ de certains outils)
#   5. Parcours JSON : champ 'version' de l objet parcours (sans v)
#   6. Fiche agent .md : 'PARCOURS (vX.Y.Z)' (avec v)
#   7. Protocole .md : frontmatter 'version: "X.Y.Z"'
#   8. version-readme.txt : fichier contenant 'X.Y.Z'
#   9. Catalogue JSON : champ 'version' du catalogue (sans v)
#
# Cibles :
#   <dossier-outil>       : bump py + sh + md + spec (si presentes) d un coup
#   --parcours <agent>    : bump parcours JSON + fiche (PARCOURS (vX.Y.Z))
#   --protocole <chemin>  : bump frontmatter version d un protocole
#   --version-readme      : bump version-readme.txt
#   --catalogue           : bump version du catalogue-commandes.json
#   <fichier>             : cible generique, format detecte automatiquement
#
# Nouvelles versions :
#   (defaut)              : bump PATCH (X.Y.Z -> X.Y.(Z+1))
#   --nouvelle X.Y.Z      : version explicite
#   --mineure             : X.(Y+1).0
#   --majeure             : (X+1).0.0
#
# Dry-run PAR DEFAUT : affiche 'ancienne -> nouvelle' par fichier, ne modifie
# rien. --wet applique reellement. Apres application, relecture de tous les
# fichiers pour verifier que tous portent la nouvelle version (verdict OK/KO).
#
# Options :
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail les motifs remplaces par fichier
#   --version
#
# Usage:
#   python3 mettre-a-jour-versions.py cerveau-projet/agents/tools/editer/editer-fichier/
#   python3 mettre-a-jour-versions.py --parcours cerberus --wet
#   python3 mettre-a-jour-versions.py --catalogue --nouvelle 0.3.0
#   python3 mettre-a-jour-versions.py --protocole <chemin> --mineure
#
# Version : 0.1.4
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (mettre-a-jour-).
# =============================================================================
import argparse
import io
import json
import os
import re
import sys
from datetime import datetime

VERSION = "0.1.4"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


# ---------------------------------------------------------------------------
# Motifs de version par format
# ---------------------------------------------------------------------------
# Chaque motif : (regex, groupe, description)
# Groupe 1 = version pure (X.Y.Z). Suffixe optionnel (-py, -sh, -beta...) :
# capture pour l affichage, conserve par remplacer_version (groupe 0 entier).
_RE_SUFFIXE = r"(?:-[A-Za-z0-9.]+)?"
_RE_EN_TETE = re.compile(r"(?m)^\s*#?\s*Version : (\d+\.\d+\.\d+)" + _RE_SUFFIXE)
_RE_CONSTANTE = re.compile(r"VERSION = \"(\d+\.\d+\.\d+)" + _RE_SUFFIXE + r"\"")
_RE_VARIABLE = re.compile(r"VERSION=\"(\d+\.\d+\.\d+)" + _RE_SUFFIXE + r"\"")
# Round bumper (2026-08-16) : 24 docs utilisent '**Version** :' (espace
# avant le deux-points) vs 92 '**Version :**' - le motif couvre les 2 formats.
# Round bumper v0.1.4 (2026-08-17, demande utilisateur audit croise) : le
# motif ne couvrait QUE le champ standard en debut de ligne -> les .md en
# format TABLEAU ('| **Version** |'), BLOCKQUOTE ('> **Version** :'), LISTE
# ('- Version :' / '- **X.Y.Z**') ou section '## Version' etaient INVISIBLES
# et declares 'coherent' sans verification (2 vrais ecarts caches :
# generateurs-carte/generateurs-ligne). Le motif couvre desormais les 4
# formats, avec priorite au champ standard (toujours en tete de fichier).
_RE_MD_VERSION = re.compile(
    r"(?m)^\s*(?:"
    r"\*\*Version(?:\*\* :|\*? :\*\*|\*\*:| :\*\*)\s*"      # standard
    r"|>\s*\*\*Version(?:\*\* :|\*? :\*\*|\*\*:| :\*\*)\s*"  # blockquote
    r"|\|\s*\*\*Version\*\*\s*\|\s*"                         # tableau
    r"|-\s*Version\s*:\s*"                                      # liste '- Version :'
    r"|-\s*\*\*?v?)(\d+\.\d+\.\d+)" + _RE_SUFFIXE)
_RE_JSON_VERSION = re.compile(r"\"version\"\s*:\s*\"(\d+\.\d+\.\d+)\"")
_RE_FICHE_PARCOURS = re.compile(r"PARCOURS \(v(\d+\.\d+\.\d+)\)")
_RE_PROTOCOLE_FRONT = re.compile(r"(?m)^\s*version:\s*\"(\d+\.\d+\.\d+)\"")
_RE_FICHIER_ISO = re.compile(r"(?m)^(\d+\.\d+\.\d+)\s*$")

# nom -> (regex, description)
MOTIFS = {
    "py_en_tete": (_RE_EN_TETE, "en-tete '# Version : X.Y.Z'"),
    "py_constante": (_RE_CONSTANTE, "constante VERSION = \"X.Y.Z\""),
    "sh_en_tete": (_RE_EN_TETE, "en-tete '# Version : X.Y.Z'"),
    "sh_variable": (_RE_VARIABLE, "variable VERSION=\"X.Y.Z\""),
    "md_version": (_RE_MD_VERSION, "champ '**Version :**'"),
    "json_version": (_RE_JSON_VERSION, "champ JSON 'version'"),
    "fiche_parcours": (_RE_FICHE_PARCOURS, "mention 'PARCOURS (vX.Y.Z)'"),
    "protocole_front": (_RE_PROTOCOLE_FRONT, "frontmatter 'version:'"),
    "fichier_iso": (_RE_FICHIER_ISO, "fichier version isole"),
}


def motifs_pour_chemin(chemin):
    """Retourne la liste des (nom, regex) applicables a un fichier, dans
    l ordre de remplacement."""
    base = os.path.basename(chemin)
    if base.endswith(".py"):
        return [("py_en_tete", _RE_EN_TETE), ("py_constante", _RE_CONSTANTE)]
    if base.endswith(".sh"):
        return [("sh_en_tete", _RE_EN_TETE), ("sh_variable", _RE_VARIABLE)]
    if base.endswith(".md"):
        return [("md_version", _RE_MD_VERSION)]
    if base.endswith(".json"):
        return [("json_version", _RE_JSON_VERSION)]
    if base == "version-readme.txt":
        return [("fichier_iso", _RE_FICHIER_ISO)]
    return []


def rel(chemin, racine):
    """Chemin relatif affichable (forward slashes, lisible sur tout OS)."""
    return os.path.relpath(chemin, racine).replace(os.sep, "/")


def lire_fichier(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def ecrire_fichier(chemin, texte):
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texte)


def remplacer_version(texte, motif, ancienne, nouvelle):
    """Remplace UNIQUEMENT la version == ancienne dans le texte pour ce motif.
    Retourne (nouveau_texte, nb_remplacements)."""
    pattern = motif.pattern

    def _sub(m):
        if m.group(1) == ancienne:
            return m.group(0).replace(ancienne, nouvelle)
        return m.group(0)

    nouveau = motif.sub(_sub, texte)
    # comptage : difference du nombre d occurrences de la chaine exacte
    nb = texte.count(ancienne) - nouveau.count(ancienne)
    return nouveau, nb


def detecter_versions(chemin):
    """Retourne {motif_nom: version} pour un fichier (premiere occurrence
    par motif). Le type de fichier est distingue pour ne pas confondre les
    versions : une fiche d agent (PARCOURS (vX.Y.Z)) porte sa propre version
    de fiche en frontmatter (champ version:), distincte de celle du parcours
    -> seule la mention PARCOURS compte. Un protocole porte la sienne en
    frontmatter -> seul protocole_front compte."""
    texte = lire_fichier(chemin)
    trouvees = {}
    for nom, (motif, _desc) in MOTIFS.items():
        m = motif.search(texte)
        if m:
            trouvees[nom] = m.group(1)
    if _RE_FICHE_PARCOURS.search(texte):
        # fiche d agent : la version du PARCOURS est la seule cible
        trouvees.pop("protocole_front", None)
        trouvees.pop("md_version", None)
    elif _RE_PROTOCOLE_FRONT.search(texte):
        # protocole : la version frontmatter est la seule cible
        trouvees.pop("fiche_parcours", None)
    return trouvees, texte


def detecter_versions_type(chemin):
    """Comme detecter_versions mais ne considere QUE les motifs propres au
    type du fichier (via motifs_pour_chemin). Evite les faux positifs : un
    .md documentaire contient des exemples de code avec '# Version :' ou
    '"version": ...' qui ne sont PAS la version de l outil."""
    texte = lire_fichier(chemin)
    trouvees = {}
    for nom, motif in motifs_pour_chemin(chemin):
        m = motif.search(texte)
        if m:
            trouvees[nom] = m.group(1)
    return trouvees, texte


def est_parcours_fichier(chemin):
    """Fichier .md qui mentionne PARCOURS (vX.Y.Z) -> fiche d agent."""
    try:
        texte = lire_fichier(chemin)
    except Exception:
        return False
    return bool(_RE_FICHE_PARCOURS.search(texte))


def collecter_outils_tous(racine):
    """Scanne TOUS les dossiers outils (action/outil) du projet.

    Ne retient que les fichiers PRINCIPAUX d un outil : basename == nom du
    dossier (outil.py / outil.sh / outil.md). Les fichiers auxiliaires
    (tester-*.sh, *-test.md, spec/, exemples) portent leurs propres versions
    documentaires et seraient des faux positifs.
    Retourne : {chemin_outil: [fichiers]}.
    """
    base = os.path.join(racine, "cerveau-projet", "agents", "tools")
    resultat = {}
    if not os.path.isdir(base):
        return resultat
    for action in sorted(os.listdir(base)):
        chemin_action = os.path.join(base, action)
        if not os.path.isdir(chemin_action):
            continue
        for outil in sorted(os.listdir(chemin_action)):
            chemin_outil = os.path.join(chemin_action, outil)
            if not os.path.isdir(chemin_outil):
                continue
            fichiers = []
            for nom in sorted(os.listdir(chemin_outil)):
                base_nom = nom.rsplit(".", 1)[0]
                if base_nom != outil:
                    continue
                if nom.endswith(".py") or nom.endswith(".sh") or nom.endswith(".md"):
                    fichiers.append(os.path.join(chemin_outil, nom))
            if fichiers:
                resultat[chemin_outil] = fichiers
    return resultat


def version_reference_outil(versions_par_fichier, fichiers):
    """Version de reference d un outil : constante VERSION du .py (source de
    verite a jour), sinon en-tete du .py, sinon la plus haute detectee."""
    for chemin in fichiers:
        if chemin.endswith(".py"):
            v = versions_par_fichier.get(chemin, {})
            if "py_constante" in v:
                return v["py_constante"]
    for chemin in fichiers:
        if chemin.endswith(".py"):
            v = versions_par_fichier.get(chemin, {})
            if "py_en_tete" in v:
                return v["py_en_tete"]
    toutes = set()
    for chemin in fichiers:
        for ver in versions_par_fichier.get(chemin, {}).values():
            toutes.add(ver)
    return max(toutes) if toutes else None


def detecter_compagnons(racine, nom_outil, ancienne, fichiers_deja_traites):
    """Detecte les FICHIERS COMPAGNONS : fichiers du projet qui referencent
    le nom de l outil bumpe ET l ancienne version (avec ou sans prefixe v).

    Round bumper (2026-08-16, demande utilisateur) : quand on bump un outil,
    les tests/docs/corrections qui pincent son ancienne version doivent etre
    mis a jour aussi - sinon KO en cascade a la non-regression (8 tests
    casses a chaque bump du lanceur). Le bumper les SIGNALE (ne les modifie
    pas : chaque type a son format d adaptation) avec verdict KO.

    Retourne : liste triee de (chemin_relatif, nb_occurrences)."""
    base = os.path.join(racine, "cerveau-projet")
    if not os.path.isdir(base):
        return []
    deja = set(os.path.abspath(c) for c in fichiers_deja_traites)
    cibles_v = [ancienne, "v" + ancienne, "V" + ancienne]
    compagnons = []
    for action, _sous, fichiers in os.walk(base):
        if "__pycache__" in action or ".git" in action:
            continue
        for nom in fichiers:
            chemin = os.path.join(action, nom)
            # EXCLUSION des corrections.md (lecons des agents) : ce sont des
            # MENTIONS HISTORIQUES (lecons passees qui documentent les versions
            # d epoque), jamais des pins a adapter - exclues pour ne pas
            # polluer la liste des compagnons (faux positifs, round 0.5.2).
            if nom == "corrections.md":
                continue
            if os.path.abspath(chemin) in deja:
                continue
            try:
                texte = lire_fichier(chemin)
            except Exception:
                continue
            if nom_outil not in texte:
                continue
            nb = sum(texte.count(c) for c in cibles_v)
            if nb:
                compagnons.append((rel(chemin, racine), nb))
    return sorted(compagnons)


def traiter_tous(args, racine):
    """Mode --tous : audit de TOUS les outils (dry-run) ou correction des
    incoherences (--wet). L outil qui porte la version de reference est la
    constante VERSION du .py (source de verite a jour)."""
    outils = collecter_outils_tous(racine)
    print(_couleur("=== Audit des versions de TOUS les outils (bumper --tous) ===", "bleu"))
    print("  %d outil(s) scanne(s) | Mode : %s" % (
        len(outils),
        "APPLICATION (--wet)" if args.wet else "DRY-RUN (audit, aucune modification)"))
    print("")

    total_ecarts = 0
    total_corriges = 0
    rapport_lignes = []

    for dossier in sorted(outils.keys()):
        fichiers = outils[dossier]
        relpath = rel(dossier, racine)
        versions_par_fichier = {}
        for chemin in fichiers:
            v, _t = detecter_versions_type(chemin)
            versions_par_fichier[chemin] = v

        reference = version_reference_outil(versions_par_fichier, fichiers)
        if reference is None:
            continue

        # ecarts : fichiers dont une version != reference
        ecarts = []
        for chemin in fichiers:
            v = versions_par_fichier.get(chemin, {})
            mauvais = [(m, ver) for m, ver in v.items() if ver != reference]
            if mauvais:
                ecarts.append((chemin, mauvais))

        if not ecarts:
            print("  %s %s : coherent (%s)" % (_couleur("[OK]", "vert"), relpath, reference))
            continue

        total_ecarts += 1
        print("  %s %s : INCOHERENT (reference %s)" % (
            _couleur("[KO]", "rouge"), relpath, reference))
        for chemin, mauvais in ecarts:
            detail = ", ".join("%s=%s" % (m, ver) for m, ver in mauvais)
            print("     - %s : %s" % (rel(chemin, racine), detail))
            if args.wet:
                texte = lire_fichier(chemin)
                nouveau = texte
                nb_fichier = 0
                for motif_nom, ver in mauvais:
                    motif = MOTIFS.get(motif_nom, (None, None))[0]
                    if motif is None:
                        continue
                    nouveau, nb = remplacer_version(nouveau, motif, ver, reference)
                    nb_fichier += nb
                if nb_fichier and nouveau != texte:
                    ecrire_fichier(chemin, nouveau)
                    total_corriges += nb_fichier
                    print("         -> corrige vers %s (%d remplacement(s))" % (
                        reference, nb_fichier))

    print("")

    # --- verification post-correction (si --wet)
    if args.wet and total_ecarts:
        restants = 0
        for dossier in outils:
            versions_par_fichier = {}
            for chemin in outils[dossier]:
                versions_par_fichier[chemin] = detecter_versions_type(chemin)[0]
            ref = version_reference_outil(versions_par_fichier, outils[dossier])
            if ref is None:
                continue
            for ver in versions_par_fichier.values():
                for v in ver.values():
                    if v != ref:
                        restants += 1
        if restants == 0:
            print(_couleur("  Verification post-correction : 0 incoherence restante [OK]", "vert"))
        else:
            print(_couleur("  Verification post-correction : %d incoherence(s) restante(s) [KO]"
                           % restants, "rouge"))
            sys.exit(1)

    verdict = "OK" if total_ecarts == 0 else "KO"
    couleur = "vert" if total_ecarts == 0 else "rouge"
    print(_couleur(
        "  Verdict : %s -- %d outil(s) incoherent(s), %d remplacement(s) corriges (mode %s)"
        % (verdict, total_ecarts, total_corriges,
           "wet" if args.wet else "dry-run"), couleur))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : mettre-a-jour-versions --tous\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("- Outils scanne(s) : %d\n" % len(outils))
            fh.write("- Mode : %s\n" % ("wet" if args.wet else "dry-run"))
            fh.write("- Verdict : %s\n\n" % verdict)
            fh.write("## Outils incoherents\n\n")
            for dossier in sorted(outils.keys()):
                fichiers = outils[dossier]
                versions_par_fichier = {}
                for chemin in fichiers:
                    versions_par_fichier[chemin] = detecter_versions_type(chemin)[0]
                reference = version_reference_outil(versions_par_fichier, fichiers)
                if reference is None:
                    continue
                ecarts = []
                for chemin in fichiers:
                    v = versions_par_fichier.get(chemin, {})
                    mauvais = [(m, ver) for m, ver in v.items() if ver != reference]
                    if mauvais:
                        ecarts.append((rel(chemin, racine), mauvais))
                if ecarts:
                    fh.write("- %s (reference %s)\n" % (rel(dossier, racine), reference))
                    for rp, mauvais in ecarts:
                        detail = ", ".join("%s=%s" % (m, ver) for m, ver in mauvais)
                        fh.write("  - %s : %s\n" % (rp, detail))
            fh.write("\n")
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    return 1 if total_ecarts else 0


def collecter_fichiers_cible(args, racine):
    """Retourne la liste des fichiers a traiter pour la cible choisie."""
    fichiers = []
    detail_cible = ""

    if args.parcours:
        agent = args.parcours
        base = os.path.join(racine, "cerveau-projet", "agents", agent)
        parcours_json = os.path.join(base, "parcours", "parcours-%s.json" % agent)
        fiche_md = os.path.join(base, "%s.md" % agent)
        if not os.path.isfile(parcours_json):
            print(_couleur("[KO] Parcours introuvable : %s" % parcours_json, "rouge"))
            sys.exit(1)
        fichiers.append(parcours_json)
        if os.path.isfile(fiche_md):
            fichiers.append(fiche_md)
        detail_cible = "parcours agent '%s' (%d fichier(s))" % (agent, len(fichiers))
        return fichiers, detail_cible

    if args.protocole:
        chemin = os.path.abspath(args.protocole)
        if not os.path.isfile(chemin):
            print(_couleur("[KO] Protocole introuvable : %s" % chemin, "rouge"))
            sys.exit(1)
        fichiers.append(chemin)
        detail_cible = "protocole '%s'" % os.path.basename(chemin)
        return fichiers, detail_cible

    if args.version_readme:
        chemin = os.path.join(racine, "cerveau-projet", "agents", "clio", "version-readme.txt")
        if not os.path.isfile(chemin):
            print(_couleur("[KO] version-readme.txt introuvable : %s" % chemin, "rouge"))
            sys.exit(1)
        fichiers.append(chemin)
        detail_cible = "version-readme.txt"
        return fichiers, detail_cible

    if args.catalogue:
        chemin = os.path.join(racine, "cerveau-projet", "agents", "tools",
                              "generateurs", "generateurs-commande", "catalogue-commandes.json")
        if not os.path.isfile(chemin):
            print(_couleur("[KO] catalogue-commandes.json introuvable : %s" % chemin, "rouge"))
            sys.exit(1)
        fichiers.append(chemin)
        detail_cible = "catalogue-commandes.json"
        return fichiers, detail_cible

    # cible par defaut : chemin (dossier outil ou fichier)
    cible = args.cible
    if not cible:
        parser.error("cible manquante : fournir un chemin, ou --parcours/--protocole/"
                     "--version-readme/--catalogue")
    chemin = os.path.abspath(cible)
    if os.path.isdir(chemin):
        # dossier outil : py + sh + md + spec/*.md
        for nom in sorted(os.listdir(chemin)):
            if nom.endswith(".py") or nom.endswith(".sh") or nom.endswith(".md"):
                fichiers.append(os.path.join(chemin, nom))
        spec_dir = os.path.join(chemin, "spec")
        if os.path.isdir(spec_dir):
            for nom in sorted(os.listdir(spec_dir)):
                if nom.endswith(".md"):
                    fichiers.append(os.path.join(spec_dir, nom))
        detail_cible = "dossier outil '%s' (%d fichier(s))" % (os.path.basename(chemin), len(fichiers))
    elif os.path.isfile(chemin):
        fichiers.append(chemin)
        detail_cible = "fichier '%s'" % os.path.basename(chemin)
    else:
        print(_couleur("[KO] Cible introuvable : %s" % cible, "rouge"))
        sys.exit(1)

    # garde-fou : un .md peut etre une fiche d agent (PARCOURS (vX.Y.Z))
    # -> on conserve le motif fiche_parcours en plus
    return fichiers, detail_cible


def calculer_nouvelle(ancienne, args):
    try:
        maj, mineur, patch = (int(p) for p in ancienne.split("."))
    except ValueError:
        return None
    if args.nouvelle:
        return args.nouvelle
    if args.majeure:
        return "%d.0.0" % (maj + 1)
    if args.mineure:
        return "%d.%d.0" % (maj, mineur + 1)
    return "%d.%d.%d" % (maj, mineur, patch + 1)


def main():
    parser = argparse.ArgumentParser(
        description="Bump systematique et coherent des versions (le bumper des agents)")
    parser.add_argument("cible", nargs="?", default="",
                        help="Chemin d un dossier outil ou d un fichier (optionnel si une option cible est donnee)")
    parser.add_argument("--parcours", type=str, default="",
                        help="Agent dont on bump le parcours JSON + la fiche (ex: cerberus)")
    parser.add_argument("--protocole", type=str, default="",
                        help="Chemin d un protocole (frontmatter version)")
    parser.add_argument("--version-readme", action="store_true",
                        help="Bump cerveau-projet/agents/clio/version-readme.txt")
    parser.add_argument("--catalogue", action="store_true",
                        help="Bump la version du catalogue-commandes.json")
    parser.add_argument("--tous", action="store_true",
                        help="Audit de TOUS les outils (dry-run) ou correction des incoherences (avec --wet) : en-tete vs constante vs doc")
    parser.add_argument("--nouvelle", type=str, default="",
                        help="Nouvelle version explicite (ex: 0.4.6)")
    parser.add_argument("--mineure", action="store_true",
                        help="Bump mineur : X.(Y+1).0")
    parser.add_argument("--majeure", action="store_true",
                        help="Bump majeur : (X+1).0.0")
    parser.add_argument("--wet", action="store_true",
                        help="Applique reellement les modifications (defaut : dry-run)")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail des motifs remplaces")
    parser.add_argument("--version", action="version",
                        version="mettre-a-jour-versions v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()

    # mode --tous : audit/correction de TOUS les outils (independant des autres cibles)
    if args.tous:
        return traiter_tous(args, racine)

    fichiers, detail_cible = collecter_fichiers_cible(args, racine)

    print(_couleur("=== Mettre a jour les versions (bumper) ===", "bleu"))
    print("  Cible : %s" % detail_cible)
    print("  Mode  : %s" % ("APPLICATION (--wet)" if args.wet else "DRY-RUN (aucune modification)"))
    print("")

    # --- 1. detecter les versions par fichier
    versions_par_fichier = {}   # chemin -> {motif: version}
    toutes_versions = set()
    for chemin in fichiers:
        v, _t = detecter_versions(chemin)
        versions_par_fichier[chemin] = v
        for motif_nom, ver in v.items():
            toutes_versions.add(ver)

    # --- 2. verifier la coherence des fichiers de la cible
    if not toutes_versions:
        print(_couleur("[KO] Aucune version detectee dans la cible (%d fichier(s) scanne(s))"
                       % len(fichiers), "rouge"))
        for chemin in fichiers:
            print("     - %s" % rel(chemin, racine))
        sys.exit(1)

    versions_multiples = sorted(toutes_versions)
    if len(versions_multiples) > 1:
        print(_couleur("[KO] INCOHERENCE DE VERSION dans la cible :", "rouge"))
        for chemin in fichiers:
            v = versions_par_fichier.get(chemin, {})
            for motif_nom, ver in sorted(v.items()):
                print("     - %s : %s (%s)" % (rel(chemin, racine), ver, motif_nom))
        print(_couleur("     -> versions trouvees : %s. Corriger d abord, puis relancer."
                       % ", ".join(versions_multiples), "rouge"))
        sys.exit(1)

    ancienne = versions_multiples[0]
    nouvelle = calculer_nouvelle(ancienne, args)
    if not nouvelle or not re.match(r"^\d+\.\d+\.\d+$", nouvelle):
        print(_couleur("[KO] Nouvelle version invalide : '%s'" % (nouvelle or ""), "rouge"))
        sys.exit(1)

    print("  Version : %s -> %s" % (_couleur(ancienne, "jaune"), _couleur(nouvelle, "vert")))
    print("")

    # --- 3. appliquer ou simuler
    total_remplacements = 0
    fichiers_modifies = []
    incoherents = []
    for chemin in fichiers:
        relpath = rel(chemin, racine)
        v = versions_par_fichier.get(chemin, {})
        texte = lire_fichier(chemin)
        nouveau_texte = texte
        nb_fichier = 0
        motifs_touches = []

        # motifs specifiques du fichier
        for motif_nom, motif in motifs_pour_chemin(chemin):
            if motif_nom in v:
                nouveau_texte, nb = remplacer_version(nouveau_texte, motif, ancienne, nouvelle)
                nb_fichier += nb
                if nb:
                    motifs_touches.append(motif_nom)

        # cas particulier : fiche d agent (PARCOURS (vX.Y.Z)) et protocole
        # (frontmatter) - le motif md_version ne couvre pas ces cas
        est_fiche = est_parcours_fichier(chemin) or "PARCOURS (v" in texte
        if est_fiche:
            nouveau_texte, nb = remplacer_version(nouveau_texte, _RE_FICHE_PARCOURS, ancienne, nouvelle)
            nb_fichier += nb
            if nb:
                motifs_touches.append("fiche_parcours")
        elif _RE_PROTOCOLE_FRONT.search(texte):
            nouveau_texte, nb = remplacer_version(nouveau_texte, _RE_PROTOCOLE_FRONT, ancienne, nouvelle)
            nb_fichier += nb
            if nb:
                motifs_touches.append("protocole_front")

        if nb_fichier == 0:
            incoherents.append(relpath)
            print("  %s %s : %s (%s)" % (
                _couleur("[KO]", "rouge"), relpath, ancienne,
                "aucun motif de version trouve"))
            continue

        total_remplacements += nb_fichier
        fichiers_modifies.append(relpath)
        print("  %s %s : %s -> %s (%d remplacement(s)%s)" % (
            _couleur("[OK]", "vert"), relpath, ancienne, nouvelle,
            nb_fichier,
            (" : " + ", ".join(motifs_touches)) if args.verbose else ""))

        if args.wet and nouveau_texte != texte:
            ecrire_fichier(chemin, nouveau_texte)

    print("")

    # --- 4. verification post-bump (si application)
    if args.wet:
        ecarts = 0
        for chemin in fichiers:
            relpath = rel(chemin, racine)
            verifs, _t = detecter_versions(chemin)
            restants = [ver for ver in verifs.values() if ver == ancienne]
            if restants:
                ecarts += len(restants)
                print("  %s %s : il reste %d occurrence(s) de %s" % (
                    _couleur("[KO]", "rouge"), relpath, len(restants), ancienne))
        if ecarts == 0:
            print(_couleur("  Verification post-bump : TOUS les fichiers portent %s [OK]"
                           % nouvelle, "vert"))
        else:
            print(_couleur("  Verification post-bump : %d ecart(s) restant(s) [KO]"
                           % ecarts, "rouge"))
            sys.exit(1)

    # --- 4b. FICHIERS COMPAGNONS (round bumper, demande utilisateur 2026-08-16) :
    # apres un bump, signaler les fichiers du projet qui referencent encore
    # l ANCIENNE version de l outil (tests, docs, corrections) pour ne plus
    # oublier de les adapter. Verdict KO si des compagnons existent.
    nom_outil = ""
    if args.parcours:
        nom_outil = args.parcours
    elif args.catalogue:
        nom_outil = "catalogue-commandes"
    elif args.version_readme:
        nom_outil = "version-readme"
    elif args.protocole:
        nom_outil = os.path.basename(os.path.dirname(os.path.abspath(args.protocole)))
    elif fichiers:
        premier = os.path.abspath(fichiers[0])
        if os.path.isdir(premier):
            nom_outil = os.path.basename(premier)
        elif args.cible and os.path.isdir(os.path.abspath(args.cible)):
            nom_outil = os.path.basename(os.path.abspath(args.cible))
        else:
            nom_outil = os.path.basename(premier).rsplit(".", 1)[0]

    compagnons = []
    if nom_outil:
        compagnons = detecter_compagnons(racine, nom_outil, ancienne, fichiers)
        if compagnons:
            print(_couleur("\n=== FICHIERS COMPAGNONS A METTRE A JOUR (ancienne version %s) ==="
                           % ancienne, "jaune"))
            print(_couleur("  %d fichier(s) referencent encore '%s' (nom de l outil + ancienne version) :"
                           % (len(compagnons), nom_outil), "jaune"))
            for rp, nb in compagnons:
                print("     - %s (%d occurrence(s))" % (rp, nb))
            print(_couleur("  -> Les adapter (tests : Morpheus ; docs/fiches : agent concerne) "
                           "avant de relancer la non-regression.", "jaune"))
            print(_couleur("  RAPPEL OBLIGATOIRE : lancer ce bumper sur CHAQUE outil bumpe AVANT "
                           "la non-regression pour adapter les compagnons (sinon KO en "
                           "cascade a la suite - lecon 2026-08-16, 5 KO).", "rouge"))

    # --- 5. verdict global
    nb_ko = len(incoherents)
    if nb_ko == 0 and not compagnons:
        verdict = "OK"
        couleur = "vert"
    else:
        verdict = "KO"
        couleur = "rouge"
    print(_couleur("  Verdict : %s -- %d fichier(s) mis a jour, %d remplacement(s), %d fichier(s) sans version%s"
                   % (verdict, len(fichiers_modifies), total_remplacements, nb_ko,
                      ", %d compagnon(s) a adapter" % len(compagnons) if compagnons else ""),
                   couleur))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : mettre-a-jour-versions\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("- Cible : %s\n" % detail_cible)
            fh.write("- Version : %s -> %s\n" % (ancienne, nouvelle))
            fh.write("- Mode : %s\n" % ("wet" if args.wet else "dry-run"))
            fh.write("- Verdict : %s\n\n" % verdict)
            fh.write("## Fichiers\n\n")
            for rp in fichiers_modifies:
                fh.write("- %s : %s -> %s\n" % (rp, ancienne, nouvelle))
            if incoherents:
                fh.write("\n## Fichiers sans version\n\n")
                for rp in incoherents:
                    fh.write("- %s\n" % rp)
            if compagnons:
                fh.write("\n## Fichiers compagnons a mettre a jour\n\n")
                for rp, nb in compagnons:
                    fh.write("- %s (%d occurrence(s))\n" % (rp, nb))
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    return 1 if nb_ko else 0


if __name__ == "__main__":
    sys.exit(main())
