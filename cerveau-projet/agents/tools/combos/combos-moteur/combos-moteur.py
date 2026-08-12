#!/usr/bin/env python3
# -*- coding: ascii -*-
# combos-moteur.py
# Moteur generique de combos declaratifs : execute une definition-combo.json
# case par case, avec passage de variables et interpolation {var}.
# Version : 0.1.0-beta
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# COMBO-ORCHESTRATEUR (spec-combos-moteur v0.1.0)
# ============================================================
# L'agent lance UN combo (definition-combo.json) au lieu d'une suite
# d'outils. Le moteur lit la definition et execute les cases dans
# l'ordre, en stockant chaque sortie dans une variable interne.
#
# 5 types de cases :
#   - generateur : appelle generateurs-commande --commande <catalogue>
#                  --reponses "<entrees interpolees>" -> sortie = commande
#   - outil      : execute la commande (subprocess) -> sortie = resultat
#   - controle   : question + branches (reponse -> vers)
#   - critere    : evalue une condition AUTOMATIQUEMENT (fichier-existe,
#                  sortie-contient, egalite, non-vide, fichier-contient)
#                  puis suit vers-vrai ou vers-faux SANS question humaine
#   - fin        : message de fin, retourne le resultat final
#
# Variables : memoire interne (dict), interpolation {var} dans les
# commandes et entrees. Option persistant: true sur une case -> la
# sortie est ecrite dans classeur-variables/stockage/variables-actuelles.md.
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : dossier 'combos/' -> prefixe 'combos-'
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python
# ============================================================
# REGLE IMMUABLE : ASCII strict (aucun accent, emoji, caractere Unicode)
# ============================================================

import argparse
import datetime
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

VERSION = "0.3.2"
STATUT = "ebauche"

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "cyan": "\033[0;36m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Retourne le texte colore si le terminal le supporte, sinon le texte brut."""
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


class ErreurCombo(Exception):
    """Erreur de definition ou d'execution d'un combo."""


def verifier_nommage(script_path):
    """REGLE IMMUABLE : le nom du fichier commence par le prefixe du dossier de categorie."""
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


# ------------------------------------------------------------------
# Chemins (le moteur vit dans agents/tools/combos/combos-moteur/)
# ------------------------------------------------------------------

def chemin_racine():
    """Racine du cerveau-projet : remonte de combos-moteur -> combos -> tools -> agents -> cerveau-projet."""
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def chemin_generateur():
    """Chemin du script generateurs-commande (source de verite des commandes)."""
    return (
        chemin_racine()
        / "agents"
        / "tools"
        / "generateurs"
        / "generateurs-commande"
        / "generateurs-commande.py"
    )


def chemin_catalogue():
    """Chemin du catalogue de commandes (source de verite des cles)."""
    return chemin_racine() / "agents" / "tools" / "generateurs" / "generateurs-commande" / "catalogue-commandes.json"


def chemin_classeur():
    """Chemin du stockage du classeur-variables (persistance optionnelle)."""
    return (
        chemin_racine()
        / "classeur-variables"
        / "stockage"
        / "variables-actuelles.md"
    )


# ------------------------------------------------------------------
# Lecture et validation de la definition
# ------------------------------------------------------------------

def charger_definition(chemin):
    """Charge la definition-combo.json et verifie sa structure de base."""
    p = Path(chemin)
    if not p.is_file():
        raise ErreurCombo("Fichier de definition introuvable: %s" % chemin)
    try:
        with p.open(encoding="utf-8") as fh:
            donnees = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ErreurCombo("JSON invalide dans %s: %s" % (chemin, exc))
    if "combo" not in donnees or "cases" not in donnees:
        raise ErreurCombo("La definition doit contenir 'combo' et 'cases'")
    return donnees


def valider_definition(donnees):
    """Valide la structure complete : case_depart, branches et suivant existants."""
    meta = donnees.get("combo", {})
    cases = donnees.get("cases", {})
    depart = meta.get("case_depart")
    erreurs = []
    if not depart:
        erreurs.append("case_depart manquant dans combo")
    elif depart not in cases:
        erreurs.append("case_depart '%s' introuvable dans cases" % depart)
    for cid, case in cases.items():
        typ = case.get("type")
        if typ not in ("generateur", "outil", "controle", "critere", "fin"):
            erreurs.append("case '%s': type inconnu '%s'" % (cid, typ))
            continue
        suivant = case.get("suivant")
        branches = case.get("branches")
        vers_vrai = case.get("vers-vrai")
        vers_faux = case.get("vers-faux")
        if suivant and suivant not in cases:
            erreurs.append("case '%s': suivant '%s' introuvable" % (cid, suivant))
        if vers_vrai and vers_vrai not in cases:
            erreurs.append("case '%s': vers-vrai '%s' introuvable" % (cid, vers_vrai))
        if vers_faux and vers_faux not in cases:
            erreurs.append("case '%s': vers-faux '%s' introuvable" % (cid, vers_faux))
        for b in branches or []:
            vers = b.get("vers")
            if vers and vers not in cases:
                erreurs.append("case '%s': branche vers '%s' introuvable" % (cid, vers))
        if typ == "critere":
            if not vers_vrai or not vers_faux:
                erreurs.append("case '%s': critere sans 'vers-vrai' ou 'vers-faux'" % cid)
            if "condition" not in case or "type" not in (case.get("condition") or {}):
                erreurs.append("case '%s': critere sans 'condition.type'" % cid)
    if erreurs:
        for e in erreurs:
            print(_couleur("ERREUR: " + e, "rouge"), file=sys.stderr)
        sys.exit(1)
    return True


def valider_cles_generateurs(donnees):
    """GARDE-FOU v0.3.0 : verifie que les cles des entrees des cases generateur
    correspondent EXACTEMENT aux parametres du catalogue de commandes.

    Regle (spec-combos-moteur v0.2.1, lecon du KO test-003) : une definition-combo
    ne doit JAMAIS inventer une cle. Chaque cle des `entrees` doit etre un
    `parametre.cle` de la commande ciblee dans catalogue-commandes.json (source
    de verite), et chaque parametre obligatoire du catalogue doit etre fourni.

    Retourne la liste des erreurs (vide si tout est conforme).
    """
    erreurs = []
    chemin = chemin_catalogue()
    if not chemin.is_file():
        erreurs.append("Catalogue introuvable pour la validation des cles: %s" % chemin)
        return erreurs
    try:
        with chemin.open(encoding="utf-8") as fh:
            catalogue = json.load(fh)
    except (OSError, ValueError) as exc:
        erreurs.append("Catalogue illisible pour la validation des cles: %s" % exc)
        return erreurs
    commandes = {c.get("nom"): c for c in catalogue.get("commandes", [])}
    meta = donnees.get("combo", {})
    nom_combo = meta.get("nom", "?")
    for cid, case in donnees.get("cases", {}).items():
        if case.get("type") != "generateur":
            continue
        catalogue_cible = case.get("catalogue")
        if catalogue_cible not in commandes:
            erreurs.append(
                "combo '%s' case '%s': catalogue '%s' introuvable dans le catalogue de commandes"
                % (nom_combo, cid, catalogue_cible)
            )
            continue
        parametres = commandes[catalogue_cible].get("parametres", [])
        cles_catalogue = [p.get("cle") for p in parametres]
        entrees = case.get("entrees") or {}
        inconnues = sorted(set(entrees.keys()) - set(cles_catalogue))
        for cle in inconnues:
            erreurs.append(
                "combo '%s' case '%s': cle '%s' hors catalogue (la commande '%s' attend: %s)"
                % (nom_combo, cid, cle, catalogue_cible, ", ".join(cles_catalogue))
            )
        obligatoires = [p.get("cle") for p in parametres if p.get("obligatoire")]
        manquantes = sorted(set(obligatoires) - set(entrees.keys()))
        for cle in manquantes:
            erreurs.append(
                "combo '%s' case '%s': parametre obligatoire '%s' manquant (commande '%s')"
                % (nom_combo, cid, cle, catalogue_cible)
            )
    return erreurs


# ------------------------------------------------------------------
# Variables et interpolation
# ------------------------------------------------------------------

def interpoler(texte, variables, contexte):
    """Remplace {var} par la valeur de la variable. Variable inconnue -> erreur."""
    if texte is None:
        return ""
    def remplacer(m):
        nom = m.group(1)
        if nom not in variables:
            raise ErreurCombo(
                "Variable non trouvee: {%s} (%s)" % (nom, contexte)
            )
        return str(variables[nom])
    # Accepte lettres, chiffres, tirets et underscores (kebab-case et snake_case)
    return re.sub(r"\{([A-Za-z0-9_-]+)\}", remplacer, str(texte))


# ------------------------------------------------------------------
# Persistance dans le classeur-variables
# ------------------------------------------------------------------

def persister_variable(nom, valeur):
    """Ecrit (ou met a jour) la ligne de la variable dans variables-actuelles.md."""
    chemin = chemin_classeur()
    if not chemin.is_file():
        raise ErreurCombo(
            "Classeur introuvable pour la persistance: %s" % chemin
        )
    valeur_plate = str(valeur).replace("|", "/").replace("\n", " ").strip()
    date = datetime.date.today().strftime("%Y-%m-%d")
    ligne = "| `%s` | %s | combos-moteur | %s | [OK] |" % (nom, valeur_plate, date)

    try:
        texte = chemin.read_text(encoding="utf-8")
    except OSError as exc:
        raise ErreurCombo("Impossible de lire le classeur: %s" % exc)

    pattern = re.compile(
        r"^\| `%s` \|.*\| \[OK\] \|$" % re.escape(nom), re.MULTILINE
    )
    if pattern.search(texte):
        texte = pattern.sub(ligne, texte, count=1)
    else:
        # Inserer la ligne avant le separateur '---' qui suit le tableau
        marqueur = "\n---\n"
        index = texte.find(marqueur)
        if index == -1:
            texte = texte.rstrip("\n") + "\n" + ligne + "\n"
        else:
            texte = texte[:index] + "\n" + ligne + "\n" + texte[index:]

    try:
        chemin.write_text(texte, encoding="utf-8")
    except OSError as exc:
        raise ErreurCombo("Impossible d'ecrire le classeur: %s" % exc)
    print(_couleur("[PERSISTANT] %s = %s" % (nom, valeur_plate), "jaune"))


# ------------------------------------------------------------------
# Execution des cases
# ------------------------------------------------------------------

def extraire_commande_generateur(sortie, catalogue):
    """Extrait la commande generee : la premiere ligne non vide APRES le marqueur."""
    lignes = sortie.splitlines()
    for i, ligne in enumerate(lignes):
        if "COMMANDE A LANCER" in ligne:
            for suivante in lignes[i + 1:]:
                if suivante.strip():
                    return suivante.strip()
            break
    # Secours : derniere ligne non vide (sortie stable du generateur)
    lignes_nb = [l.strip() for l in lignes if l.strip()]
    if lignes_nb:
        return lignes_nb[-1]
    raise ErreurCombo(
        "Impossible d'extraire la commande generee pour '%s'" % catalogue
    )


def executer_case_generateur(case, cid, variables, dry_run, verbose, no_journal=False):
    """Case generateur : compose la commande via generateurs-commande --reponses."""
    catalogue = case.get("catalogue")
    if not catalogue:
        raise ErreurCombo("Case generateur '%s' sans 'catalogue'" % cid)
    entrees = case.get("entrees") or {}
    if verbose:
        print("  [%s] generateur %s" % (cid, catalogue))

    morceaux = []
    for cle, valeur in entrees.items():
        v = interpoler(valeur, variables, "entrees de la case " + cid)
        morceaux.append("%s=%s" % (cle, v))
    reponses = ";".join(morceaux)

    generateur = chemin_generateur()
    if not generateur.is_file():
        raise ErreurCombo("Generateur introuvable: %s" % generateur)

    cmd = [
        sys.executable or "python3",
        str(generateur),
        "--commande",
        catalogue,
        "--reponses",
        reponses,
    ]
    if no_journal:
        cmd.append("--no-journal")
    if dry_run:
        print(_couleur("[DRY-RUN] ", "cyan") + " ".join(cmd))
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ErreurCombo(
            "Echec de l'appel au generateur (case %s): %s" % (cid, exc)
        )

    if proc.returncode != 0:
        raise ErreurCombo(
            "Generateur en erreur (case %s, %s):\n%s"
            % (cid, catalogue, (proc.stderr or proc.stdout))
        )

    commande = extraire_commande_generateur(proc.stdout, catalogue)
    variables[case["sortie"]] = commande
    if verbose:
        print("  -> commande generee: %s" % commande)
    return


def executer_case_outil(case, cid, variables, dry_run, verbose):
    """Case outil : execute la commande (interpolee) en subprocess.

    ROBUSTESSE (round 5) : le code retour est verifie. Un echec (exit != 0)
    ARRETE le combo avec un message explicite (case, commande, code, sortie) :
    un agent ne doit jamais croire qu'un combo a reussi alors qu'une etape a
    echoue. Exception : la case peut declarer `"echec_ok": true` quand le code
    non nul est un RESULTAT legitime (outil de controle/detection qui signale
    un ecart par exit 1) - le resultat est alors stocke normalement et le
    combo continue.
    """
    commande_brute = case.get("commande")
    if not commande_brute:
        raise ErreurCombo("Case outil '%s' sans 'commande'" % cid)
    commande = interpoler(commande_brute, variables, "commande de la case " + cid)
    if verbose:
        print("  [%s] outil : %s" % (cid, commande))

    if dry_run:
        print(_couleur("[DRY-RUN] ", "cyan") + commande)
        return

    try:
        args_list = shlex.split(commande)
    except ValueError as exc:
        raise ErreurCombo("Commande invalide (case %s): %s" % (cid, exc))

    try:
        proc = subprocess.run(
            args_list,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ErreurCombo("Echec d'execution (case %s): %s" % (cid, exc))

    resultat = (proc.stdout or "") + (proc.stderr or "")
    # ROBUSTESSE (round 5) : echec = arret, sauf echec_ok declare
    if proc.returncode != 0 and not case.get("echec_ok"):
        raise ErreurCombo(
            "La commande de la case '%s' a echoue (code %d):\n  %s\n%s"
            % (cid, proc.returncode, commande, resultat.strip()[:500])
        )
    if proc.returncode != 0 and case.get("echec_ok") and verbose:
        print(_couleur(
            "  -> code %d (echec_ok: resultat conserve)" % proc.returncode,
            "jaune",
        ))
    variables[case["sortie"]] = resultat.strip()
    if verbose:
        print("  -> sortie: %s" % resultat.strip()[:200])
    if case.get("persistant"):
        persister_variable(case["sortie"], resultat.strip())
    return


def trouver_branche(branches, reponse):
    """Trouve la branche correspondant a la reponse (numero ou texte)."""
    rep = reponse.strip()
    if rep.isdigit():
        idx = int(rep) - 1
        if 0 <= idx < len(branches):
            return branches[idx]
        return None
    for b in branches:
        if b.get("reponse", "").strip().lower() == rep.lower():
            return b
    return None


def evaluer_critere(case, cid, variables, verbose):
    """Case critere : evalue une condition AUTOMATIQUEMENT et retourne
    la prochaine case (vers-vrai ou vers-faux). Aucune question humaine.

    Conditions supportees :
      - fichier-existe : {chemin} existe sur le disque
      - fichier-contient : le fichier {chemin} contient le texte {texte}
      - sortie-contient : la valeur de {source} (variable ou texte) contient {texte}
      - egalite : la variable {variable} vaut exactement {valeur}
      - non-vide : la variable {variable} existe et n'est pas vide
    """
    condition = case.get("condition") or {}
    type_condition = condition.get("type")
    if verbose:
        print("  [%s] critere : %s" % (cid, type_condition))

    vrai = False

    if type_condition == "fichier-existe":
        chemin = interpoler(condition.get("chemin", ""), variables, "critere " + cid)
        vrai = Path(chemin).is_file()
        if verbose:
            print("  -> fichier-existe %s : %s" % (chemin, "VRAI" if vrai else "FAUX"))

    elif type_condition == "fichier-contient":
        chemin = interpoler(condition.get("chemin", ""), variables, "critere " + cid)
        texte = interpoler(condition.get("texte", ""), variables, "critere " + cid)
        if Path(chemin).is_file():
            try:
                contenu = Path(chemin).read_text(encoding="utf-8", errors="replace")
                vrai = texte in contenu
            except OSError:
                vrai = False
        else:
            vrai = False
        if verbose:
            print("  -> fichier-contient %s : %s" % (chemin, "VRAI" if vrai else "FAUX"))

    elif type_condition == "sortie-contient":
        source = interpoler(condition.get("source", ""), variables, "critere " + cid)
        texte = interpoler(condition.get("texte", ""), variables, "critere " + cid)
        vrai = texte in (source or "")
        if verbose:
            print("  -> sortie-contient : %s" % ("VRAI" if vrai else "FAUX"))

    elif type_condition == "egalite":
        variable = condition.get("variable")
        valeur = interpoler(condition.get("valeur", ""), variables, "critere " + cid)
        actuel = str(variables.get(variable, ""))
        vrai = actuel == valeur
        if verbose:
            print("  -> egalite %s=%s : %s" % (variable, valeur, "VRAI" if vrai else "FAUX"))

    elif type_condition == "non-vide":
        variable = condition.get("variable")
        actuel = variables.get(variable)
        vrai = actuel is not None and str(actuel).strip() != ""
        if verbose:
            print("  -> non-vide %s : %s" % (variable, "VRAI" if vrai else "FAUX"))

    else:
        raise ErreurCombo(
            "Critere '%s': type de condition inconnu '%s'" % (cid, type_condition)
        )

    return case.get("vers-vrai") if vrai else case.get("vers-faux")


def resoudre_controle(case, cid, variables, reponses_predefinies, verbose):
    """Case controle : pose la question et retourne la prochaine case."""
    question = case.get("question", "Quelle reponse ?")
    branches = case.get("branches") or []
    if verbose:
        print("  [%s] controle : %s" % (cid, question))
    print(_couleur("QUESTION : %s" % question, "cyan"))
    for i, b in enumerate(branches, 1):
        print("  [%d] %s" % (i, b.get("reponse", "?")))

    rep = None
    if reponses_predefinies is not None:
        if cid in reponses_predefinies:
            rep = reponses_predefinies[cid].strip()
        else:
            raise ErreurCombo(
                "Controle '%s': reponse manquante dans --reponses" % cid
            )
    else:
        try:
            rep = input("> ").strip()
        except EOFError:
            raise ErreurCombo(
                "Controle '%s': aucune reponse fournie (fin d'entree)" % cid
            )

    b = trouver_branche(branches, rep)
    if b is None:
        raise ErreurCombo(
            "Controle '%s': reponse inconnue '%s' (possibles: %s)"
            % (cid, rep, " / ".join(br.get("reponse", "?") for br in branches))
        )
    return b.get("vers")


def lister_cases(donnees):
    """Mode --liste : affiche les cases sans executer."""
    meta = donnees.get("combo", {})
    cases = donnees.get("cases", {})
    print("=== Combo %s v%s ===" % (meta.get("nom", "?"), meta.get("version", "?")))
    if meta.get("description"):
        print(meta.get("description"))
    print("Depart : %s" % meta.get("case_depart", "?"))
    print("")
    for cid, case in cases.items():
        print("  [%s] %-10s %s" % (cid, case.get("type", "?"), case.get("titre", "")))
    return 0


def executer(donnees, reponses_predefinies, dry_run, verbose, variables_initiales=None, no_journal=False):
    """Parcourt la definition case par case jusqu'a une case fin."""
    meta = donnees.get("combo", {})
    cases = donnees.get("cases", {})
    variables = dict(variables_initiales or {})
    cid = meta.get("case_depart")

    print("=== Combo %s v%s ===" % (_couleur(meta.get("nom", "?"), "bleu"), meta.get("version", "?")))
    if meta.get("description"):
        print(meta.get("description"))
    print("")

    while True:
        if cid not in cases:
            raise ErreurCombo("Case suivante introuvable: '%s'" % cid)
        case = cases[cid]
        typ = case.get("type")
        titre = case.get("titre", cid)

        if typ == "fin":
            print(_couleur("=== COMBO TERMINE ===", "vert"))
            print("Fin de combo atteinte : case '%s' (%s)" % (cid, titre))
            if case.get("message"):
                print(case.get("message"))
            print("")
            if verbose:
                print("Variables finales :")
                for k, v in sorted(variables.items()):
                    print("  %s = %s" % (k, str(v)[:120]))
            return 0

        if verbose:
            print("")
            print(_couleur("--- [%s] %s ---" % (cid, titre), "bleu"))

        if typ == "generateur":
            executer_case_generateur(case, cid, variables, dry_run, verbose, no_journal)
        elif typ == "outil":
            executer_case_outil(case, cid, variables, dry_run, verbose)
        elif typ == "controle":
            suivant = resoudre_controle(case, cid, variables, reponses_predefinies, verbose)
            cid = suivant
            continue
        elif typ == "critere":
            suivant = evaluer_critere(case, cid, variables, verbose)
            cid = suivant
            continue
        else:
            raise ErreurCombo("Case '%s': type inconnu '%s'" % (cid, typ))

        cid = case.get("suivant")
        if not cid:
            print(_couleur("=== COMBO TERMINE ===", "vert"))
            return 0


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="combos-moteur",
        description="Moteur generique de combos declaratifs (definition-combo.json)",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("definition", type=str, help="Chemin du fichier definition-combo.json")
    parser.add_argument("--liste", action="store_true", help="Lister les cases sans executer")
    parser.add_argument("--reponses", type=str, default=None, help="Reponses des controles : case=reponse;case2=reponse2")
    parser.add_argument("--var", type=str, default=None, action="append", help="Variable initiale : cle=valeur (repetable)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les commandes sans les executer")
    parser.add_argument("--no-journal", action="store_true", help="Desactiver la journalisation d usage (generateur)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details de chaque case")
    parser.add_argument("--version", action="version", version="combos-moteur v%s" % VERSION)
    return parser


def parser_reponses_controles(chaine):
    """Parse --reponses 'c1=OUI;c3=NON' -> dict {case: reponse}."""
    reponses = {}
    if not chaine:
        return reponses
    for morceau in chaine.split(";"):
        morceau = morceau.strip()
        if not morceau:
            continue
        if "=" not in morceau:
            raise ErreurCombo("Reponse mal formee (case=reponse) : %s" % morceau)
        cle, valeur = morceau.split("=", 1)
        reponses[cle.strip()] = valeur.strip()
    return reponses


def parser_variables(chaine):
    """Parse --var 'cle=valeur' -> dict {cle: valeur} (valeurs avec = conservees)."""
    variables = {}
    if not chaine:
        return variables
    for morceau in chaine:
        morceau = morceau.strip()
        if not morceau:
            continue
        if "=" not in morceau:
            raise ErreurCombo("Variable mal formee (cle=valeur) : %s" % morceau)
        cle, valeur = morceau.split("=", 1)
        variables[cle.strip()] = valeur.strip()
    return variables


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()

    try:
        donnees = charger_definition(args.definition)
        valider_definition(donnees)
        # GARDE-FOU v0.3.0 : cles des entrees des cases generateur vs catalogue
        erreurs_cles = valider_cles_generateurs(donnees)
        if erreurs_cles:
            for e in erreurs_cles:
                print(_couleur("[ERREUR] %s" % e, "rouge"), file=sys.stderr)
            return 1

        if args.liste:
            return lister_cases(donnees)

        reponses = None
        if args.reponses is not None:
            reponses = parser_reponses_controles(args.reponses)

        variables_initiales = None
        if args.var is not None:
            variables_initiales = parser_variables(args.var)

        return executer(donnees, reponses, args.dry_run, args.verbose, variables_initiales, args.no_journal)
    except ErreurCombo as exc:
        print(_couleur("[ERREUR] %s" % exc, "rouge"), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
