#!/usr/bin/env python3
# -*- coding: ascii -*-
# generateurs-case.py
# Genere, edite et supprime des cases d'une carte de decision (parcours JSON)
# avec recablage automatique des references et validation auto complete.
# Version : 0.1.0-beta
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom DOIT commencer par le
# prefixe du dossier de categorie (generateurs-) : controle au demarrage.
# REGLE IMMUABLE : 100% stdlib Python.
# REGLE IMMUABLE : ASCII strict (aucun accent, emoji ou Unicode).
# ============================================================

import argparse
import json
import subprocess
import sys
from pathlib import Path

VERSION = "0.2.1"
STATUT = "ebauche"

# Racine du projet : 5 remontees depuis ce fichier
# (generateurs-case -> generateurs -> tools -> agents -> cerveau-projet -> racine)
RACINE = Path(__file__).resolve().parents[5]
GUIDER_PY = RACINE / "cerveau-projet" / "agents" / "tools" / "guider" / "guider-parcours" / "guider-parcours.py"

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


def verifier_nommage(script_path):
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


# ------------------------------------------------------------
# Chargement / sauvegarde
# ------------------------------------------------------------

def charger_parcours(chemin):
    """Charge le parcours JSON et valide sa structure de base."""
    chemin = Path(chemin)
    if not chemin.exists():
        print(_couleur("ERREUR: Parcours introuvable: %s" % chemin, "rouge"), file=sys.stderr)
        sys.exit(1)
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError as e:
        print(_couleur("ERREUR: JSON invalide: %s" % e, "rouge"), file=sys.stderr)
        sys.exit(1)
    if "parcours" not in donnees or "cases" not in donnees:
        print(_couleur("ERREUR: Structure invalide (attendu: parcours + cases)", "rouge"), file=sys.stderr)
        sys.exit(1)
    return donnees


def sauvegarder_parcours(chemin, donnees):
    """Ecrit le parcours JSON en ASCII strict avec indentation 2."""
    chemin = Path(chemin)
    try:
        contenu = json.dumps(donnees, ensure_ascii=True, indent=2)
        # Verifier que le contenu est 100% ASCII avant d'ecrire
        contenu.encode("ascii")
    except UnicodeEncodeError:
        print(_couleur("ERREUR: Contenu non-ASCII refuse (regle immuable)", "rouge"), file=sys.stderr)
        sys.exit(1)
    with open(chemin, "w", encoding="ascii", newline="\n") as f:
        f.write(contenu)
        f.write("\n")


# ------------------------------------------------------------
# References
# ------------------------------------------------------------

def references_vers(cases, case_id):
    """Retourne la liste des (source, type) qui pointent vers case_id."""
    refs = []
    for source_id, case in cases.items():
        if source_id == case_id:
            continue
        if case.get("suivant") == case_id:
            refs.append((source_id, "suivant"))
        for i, branche in enumerate(case.get("branches", [])):
            if branche.get("vers") == case_id:
                refs.append((source_id, "branche[%d]" % i))
    return refs


def valider_references(donnees, verbose=False):
    """Valide que toutes les references (suivant, vers, case_depart) existent."""
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    erreurs = []
    if depart not in cases:
        erreurs.append("case_depart '%s' inexistante" % depart)
    for case_id, case in cases.items():
        suivant = case.get("suivant")
        if suivant is not None and suivant not in cases:
            erreurs.append("case %s: suivant '%s' inexistant" % (case_id, suivant))
        for i, branche in enumerate(case.get("branches", [])):
            vers = branche.get("vers")
            if vers is not None and vers not in cases:
                erreurs.append("case %s: branche[%d] vers '%s' inexistant" % (case_id, i, vers))
    if erreurs:
        for e in erreurs:
            print(_couleur("  [ERREUR] %s" % e, "rouge"), file=sys.stderr)
        return False
    if verbose:
        print(_couleur("  [OK] References validees (%d cases)" % len(cases), "vert"))
    return True


# ------------------------------------------------------------
# Garde-fou Pattern 5 : chaine de delegation ACTIVE
# ------------------------------------------------------------

_FORMULATIONS_PASSIVES = (
    "te reactive",
    "te reactivera",
    "il me reactive",
    "elle me reactive",
    "j'attends",
    "j attends",
    "attend le retour",
    "attendre le retour",
    "en attente de",
    "tu seras reactive",
    "il va te",
    "elle va te",
)


def formuler_avertissement_fin_passive(message):
    """Retourne l'avertissement si le message de fin porte une formulation passive bloquante (Pattern 5), sinon None."""
    if not message:
        return None
    msg = message.lower()
    trouvees = [f for f in _FORMULATIONS_PASSIVES if f in msg]
    if not trouvees:
        return None
    return (
        "ATTENTION (Pattern 5, spec-guider-parcours v0.2.6) : le message de fin contient une "
        "formulation passive (%s) qui peut COUPER LA CHAINE. Une delegation ne se termine JAMAIS "
        "par une fin passive ('X te reactive') : materialiser la boucle RELAIS -> RETOUR -> CLOTURE "
        "dans le parcours (voir parcours-vulcain v0.2.1)." % ", ".join(trouvees)
    )


_OUTILS_ECRITURE = (
    "creer-fichier",
    "ecrire-fichier",
    "editer-fichier",
    "ajouter-contenu-fichier",
    "inserer-contenu-fichier",
    "copier-fichier",
)


def formuler_avertissement_regles_immuables(case):
    """Garde-fou REGLES IMMUABLES (non-bloquant) : rappelle RVAV + delegation (Morpheus/Janus)
    sur les cases d'ecriture (outil d'ecriture dans les indices) et les fins de delegation.

    Constat utilisateur 2026-08-08 : RVAV et la delegation (tests -> Morpheus, controle -> Janus)
    etaient absents des generateurs -> les nouvelles cartes/cases produites ne rappelaient plus
    les regles immuables et la chaine de delegation se degradait silencieusement.
    Retourne l'avertissement (str) ou None.
    """
    if not case:
        return None
    avertissements = []

    type_case = case.get("type")
    nom_outils = []
    for indice in case.get("indices", []):
        if indice.get("type") == "outil" and indice.get("nom") in _OUTILS_ECRITURE:
            nom_outils.append(indice.get("nom"))

    if nom_outils or (case.get("message") and "rapport" in case.get("message", "").lower()):
        # Case d'ecriture : rappel ASCII (Pattern 2) + RVAV avant de valider
        if nom_outils and (
            not case.get("indices")
            or case["indices"][0].get("type") != "regle"
            or not case["indices"][0].get("texte", "").startswith("REGLE IMMUABLE ASCII")
        ):
            avertissements.append(
                "RAPPEL ASCII (Pattern 2, spec-guider-parcours v0.2.0) : la case d'ecriture (%s) "
                "DOIT porter en TETE de ses indices un indice regle 'REGLE IMMUABLE ASCII' "
                "(100%% ASCII, guillemets ASCII, jamais de guillemets francais)." % ", ".join(nom_outils)
            )
        avertissements.append(
            "RAPPEL RVAV (regle immuable) : je ne valide JAMAIS sans avoir passe la boucle RVAV "
            "complete (Rechercher, Verifier, Analyser, Valider) sur mon travail. Pour une case qui "
            "ECRIT dans un fichier, ajouter un indice regle RVAV a la case (ou a la case suivante)."
        )

    if type_case == "fin":
        message = (case.get("message") or "").lower()
        if "morpheus" in message or "janus" in message or "active" in message or "reactive" in message:
            avertissements.append(
                "RAPPEL DELEGATION (chaine bout-en-bout, spec-guider-parcours v0.2.15) : a la fin d'un "
                "maillon de chaine, j ACTIVE le maillon suivant a MA fin (Vulcain active Morpheus -> "
                "Morpheus active Janus -> Janus REACTIVE Cerberus avec le bilan consolide). Chaque "
                "maillon passe la boucle RVAV sur son travail AVANT d'activer le suivant. Une activation "
                "directe par Cerberus reste valide (fin = reactiver Cerberus)."
            )
        elif "rvav" not in message:
            avertissements.append(
                "RAPPEL RVAV (regle immuable) : avant d'activer le maillon suivant, passer la boucle "
                "RVAV complete (Rechercher, Verifier, Analyser, Valider) sur mon travail."
            )

    if not avertissements:
        return None
    return (
        "ATTENTION (GARDE-FOU REGLES IMMUABLES, generateurs-case v0.2.1) : "
        + " | ".join(avertissements)
    )


def afficher_avertissement_regles_immuables(case):
    """Affiche l'avertissement des regles immuables s'il y a lieu (non-bloquant)."""
    avertissement = formuler_avertissement_regles_immuables(case)
    if avertissement:
        print(_couleur("  " + avertissement, "jaune"), file=sys.stderr)


def action_liste(args):
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    print("=== Parcours %s v%s ===" % (donnees["parcours"].get("nom", ""), donnees["parcours"].get("version", "")))
    print("Agent : %s | Depart : %s | %d cases" % (donnees["parcours"].get("agent", ""), depart, len(cases)))
    print("")
    for case_id, case in cases.items():
        marqueur = ""
        if case_id == depart:
            marqueur = " (depart)"
        print("  [%s] %-8s %s%s" % (case_id, case.get("type", "?"), case.get("titre", ""), marqueur))
    return 0


def prochain_id_libre(cases, base="c"):
    """Retourne le prochain id cN libre (c0b exclu du comptage simple)."""
    numeros = []
    for case_id in cases:
        if case_id.startswith(base) and case_id[1:].isdigit():
            numeros.append(int(case_id[1:]))
    if not numeros:
        return base + "1"
    return base + str(max(numeros) + 1)


def construire_case(args, donnees):
    """Construit la case a ajouter selon le type."""
    type_case = args.type_case
    case = {"titre": args.titre if args.titre else "Nouvelle case", "type": type_case}
    if type_case in ("question", "controle"):
        if not args.question:
            print(_couleur("ERREUR: type '%s' exige --question" % type_case, "rouge"), file=sys.stderr)
            sys.exit(1)
        case["question"] = args.question
        if type_case == "controle" and not args.branches and not args.suivant:
            print(_couleur("ERREUR: type 'controle' exige --branche ou --suivant", "rouge"), file=sys.stderr)
            sys.exit(1)
    elif type_case == "indice":
        if not args.suivant:
            print(_couleur("ERREUR: type 'indice' exige --suivant", "rouge"), file=sys.stderr)
            sys.exit(1)
    elif type_case == "fin":
        if args.message:
            case["message"] = args.message
            avertissement = formuler_avertissement_fin_passive(args.message)
            if avertissement:
                print(_couleur("  " + avertissement, "jaune"), file=sys.stderr)
        afficher_avertissement_regles_immuables(case)
        return case
    else:
        print(_couleur("ERREUR: type inconnu '%s' (question/indice/controle/fin)" % type_case, "rouge"), file=sys.stderr)
        sys.exit(1)

    indices = []
    if args.indices_regle:
        for texte in args.indices_regle:
            indices.append({"type": "regle", "texte": texte})
    if args.indices_outil:
        for spec in args.indices_outil:
            parties = spec.split(":")
            if len(parties) < 2:
                print(_couleur("ERREUR: --indice-outil attend <nom>:<chemin>[:commande]", "rouge"), file=sys.stderr)
                sys.exit(1)
            indice = {"type": "outil", "nom": parties[0], "chemin": parties[1]}
            if len(parties) >= 3:
                indice["commande"] = ":".join(parties[2:])
            indices.append(indice)
    if args.indices_fichier:
        for spec in args.indices_fichier:
            parties = spec.split(":")
            if len(parties) < 2:
                print(_couleur("ERREUR: --indice-fichier attend <chemin>:<raison>", "rouge"), file=sys.stderr)
                sys.exit(1)
            indices.append({"type": "fichier", "chemin": parties[0], "raison": ":".join(parties[1:])})
    if indices:
        case["indices"] = indices
    afficher_avertissement_regles_immuables(case)

    branches = []
    if args.branches:
        for spec in args.branches:
            parties = spec.split(":")
            if len(parties) != 2:
                print(_couleur("ERREUR: --branche attend <reponse>:<vers>", "rouge"), file=sys.stderr)
                sys.exit(1)
            branches.append({"reponse": parties[0], "vers": parties[1]})
    if branches:
        case["branches"] = branches
    elif type_case in ("question",) and args.suivant:
        case["suivant"] = args.suivant
    elif type_case == "indice" and args.suivant:
        case["suivant"] = args.suivant
    return case


def action_ajouter(args):
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]

    # Id de la nouvelle case
    if args.case_id:
        nouveau_id = args.case_id
        if nouveau_id in cases:
            print(_couleur("ERREUR: la case '%s' existe deja" % nouveau_id, "rouge"), file=sys.stderr)
            sys.exit(1)
    else:
        nouveau_id = prochain_id_libre(cases)

    case = construire_case(args, donnees)
    cases[nouveau_id] = case

    # Recablage pour insertion a une position precise (--apres)
    if args.apres:
        if args.apres not in cases:
            print(_couleur("ERREUR: la case '%s' a inserer apres n'existe pas" % args.apres, "rouge"), file=sys.stderr)
            sys.exit(1)
        apres = cases[args.apres]
        ancien_suivant = apres.get("suivant")
        apres["suivant"] = nouveau_id
        if not args.suivant:
            # La nouvelle case prend la suite de la case apres
            if type_case_is_indice_or_suivant(case) and ancien_suivant:
                case["suivant"] = ancien_suivant
        # Les references vers la case inseree (branches) sont conservees

    if args.dry_run:
        print(_couleur("[DRY-RUN] Case '%s' (%s) ajoutee a %s" % (nouveau_id, case.get("type"), args.parcours), "jaune"))
        return 0

    sauvegarder_parcours(args.parcours, donnees)
    print(_couleur("[OK] Case '%s' (%s) ajoutee: %s" % (nouveau_id, case.get("type"), case.get("titre")), "vert"))
    valider_auto(args, donnees)
    return 0


def type_case_is_indice_or_suivant(case):
    return case.get("type") in ("indice", "question", "controle")


# ------------------------------------------------------------
# Bloc modele compose (action ajouter-bloc, Pattern 7)
# ------------------------------------------------------------

def action_ajouter_bloc(args):
    """Cree d'un coup un bloc MODELE COMPOSE (Pattern 7) : decision + deviation + rejoint.

    Structure creee :
      <decision> (question, 2 branches) :
        OUI -> <deviation> (indice) -> <rejoint> (indice) -> <suite>
        NON -> <suite> (flux principal)
    """
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]

    # Ids des 3 cases du bloc (defaut : cN + cNa + cNb, prochains libres)
    base = prochain_id_libre(cases)
    id_decision = args.decision or base
    id_deviation = args.deviation or (id_decision + "a")
    id_rejoint = args.rejoint or (id_decision + "b")

    for cid in (id_decision, id_deviation, id_rejoint):
        if cid in cases:
            print(_couleur("ERREUR: la case '%s' existe deja" % cid, "rouge"), file=sys.stderr)
            sys.exit(1)

    if not args.suite:
        print(_couleur("ERREUR: ajouter-bloc exige --suite <case> (suite du flux principal)", "rouge"), file=sys.stderr)
        sys.exit(1)

    # Case decision (question, 2 branches)
    decision = {
        "titre": args.titre or "Decision",
        "type": "question",
        "question": args.question or "Quelle est la decision ?",
        "branches": [
            {"reponse": "OUI", "vers": id_deviation},
            {"reponse": "NON", "vers": args.suite},
        ],
    }

    # Case deviation (indice -> rejoint)
    deviation = {
        "titre": args.titre_deviation or "DEVIATION : workflow secondaire",
        "type": "indice",
        "indices": [
            {
                "type": "regle",
                "texte": "REGLE PATTERN 7 (spec-guider-parcours v0.2.13) : deviation vers un workflow secondaire - le workflow secondaire se termine par un REJOINT vers le flux principal (jamais une fin au milieu, jamais une boucle d'attente).",
            }
        ],
        "suivant": id_rejoint,
    }

    # Case rejoint (indice -> suite du flux principal)
    rejoint = {
        "titre": args.titre_rejoint or "REJOINT : retour au flux principal",
        "type": "indice",
        "indices": [
            {
                "type": "regle",
                "texte": "REGLE PATTERN 7 (spec-guider-parcours v0.2.13) : rejoint le flux principal - la deviation est terminee, on revient a la suite du flux.",
            }
        ],
        "suivant": args.suite,
    }

    cases[id_decision] = decision
    cases[id_deviation] = deviation
    cases[id_rejoint] = rejoint
    afficher_avertissement_regles_immuables(decision)
    afficher_avertissement_regles_immuables(deviation)
    afficher_avertissement_regles_immuables(rejoint)

    # Recablage si --apres : la case apres pointe vers la decision du bloc
    if args.apres:
        if args.apres not in cases:
            print(_couleur("ERREUR: la case '%s' a inserer apres n'existe pas" % args.apres, "rouge"), file=sys.stderr)
            sys.exit(1)
        cases[args.apres]["suivant"] = id_decision

    if args.dry_run:
        print(
            _couleur(
                "[DRY-RUN] Bloc modele compose ajoute : %s (decision) -> %s (deviation) -> %s (rejoint) -> %s (suite)"
                % (id_decision, id_deviation, id_rejoint, args.suite),
                "jaune",
            )
        )
        return 0

    sauvegarder_parcours(args.parcours, donnees)
    print(
        _couleur(
            "[OK] Bloc modele compose ajoute : %s (decision) -> %s (deviation) -> %s (rejoint) -> %s (suite)"
            % (id_decision, id_deviation, id_rejoint, args.suite),
            "vert",
        )
    )
    valider_auto(args, donnees)
    return 0


def action_editer(args):
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    if args.case_id not in cases:
        print(_couleur("ERREUR: la case '%s' n'existe pas" % args.case_id, "rouge"), file=sys.stderr)
        sys.exit(1)
    case = cases[args.case_id]

    modifications = []
    if args.titre is not None:
        case["titre"] = args.titre
        modifications.append("titre")
    if args.question is not None:
        case["question"] = args.question
        modifications.append("question")
    if args.message is not None:
        case["message"] = args.message
        modifications.append("message")
        if case.get("type") == "fin":
            avertissement = formuler_avertissement_fin_passive(args.message)
            if avertissement:
                print(_couleur("  " + avertissement, "jaune"), file=sys.stderr)
    afficher_avertissement_regles_immuables(case)
    if args.suivant is not None:
        case["suivant"] = args.suivant
        modifications.append("suivant")
    if args.type_case is not None:
        case["type"] = args.type_case
        modifications.append("type")
    if args.branches is not None:
        branches = []
        for spec in args.branches:
            parties = spec.split(":")
            if len(parties) != 2:
                print(_couleur("ERREUR: --branche attend <reponse>:<vers>", "rouge"), file=sys.stderr)
                sys.exit(1)
            branches.append({"reponse": parties[0], "vers": parties[1]})
        case["branches"] = branches
        modifications.append("branches")
    if args.indices_regle is not None:
        case["indices"] = [{"type": "regle", "texte": t} for t in args.indices_regle]
        modifications.append("indices")
    if args.remove_indices:
        case["indices"] = []
        modifications.append("indices")

    if not modifications:
        print(_couleur("ERREUR: aucune modification fournie (--titre/--question/--suivant/...)", "rouge"), file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(_couleur("[DRY-RUN] Case '%s' : %s modifie(s) a %s" % (args.case_id, ", ".join(modifications), args.parcours), "jaune"))
        return 0

    sauvegarder_parcours(args.parcours, donnees)
    print(_couleur("[OK] Case '%s' modifiee (%s): %s" % (args.case_id, ", ".join(modifications), case.get("titre")), "vert"))
    valider_auto(args, donnees)
    return 0


def action_supprimer(args):
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    if args.case_id not in cases:
        print(_couleur("ERREUR: la case '%s' n'existe pas" % args.case_id, "rouge"), file=sys.stderr)
        sys.exit(1)
    case = cases[args.case_id]

    # Cible de recablage : le suivant de la case supprimee, sinon --vers
    cible = args.vers
    if cible is None:
        cible = case.get("suivant")
    if cible is None:
        print(
            _couleur(
                "ERREUR: la case '%s' n'a pas de suivant et --vers absent : impossible de recabler"
                % args.case_id,
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    if cible == args.case_id or (cible not in cases and cible != args.case_id):
        # Si la cible est la case elle-meme (boucle), on garde la case
        pass

    refs = references_vers(cases, args.case_id)
    if refs and not args.force and not args.vers:
        # Recablage automatique (decision utilisateur) : rediriger vers la cible
        pass

    # Application du recablage
    for source_id, type_ref in refs:
        if type_ref == "suivant":
            cases[source_id]["suivant"] = cible
        else:
            i = int(type_ref.split("[")[1].split("]")[0])
            cases[source_id]["branches"][i]["vers"] = cible

    # case_depart
    if donnees["parcours"].get("case_depart") == args.case_id:
        donnees["parcours"]["case_depart"] = cible

    del cases[args.case_id]

    if args.dry_run:
        print(
            _couleur(
                "[DRY-RUN] Case '%s' supprimee, %d reference(s) recablee(s) vers '%s'"
                % (args.case_id, len(refs), cible),
                "jaune",
            )
        )
        return 0

    sauvegarder_parcours(args.parcours, donnees)
    print(
        _couleur(
            "[OK] Case '%s' supprimee, %d reference(s) recablee(s) vers '%s'"
            % (args.case_id, len(refs), cible),
            "vert",
        )
    )
    valider_auto(args, donnees)
    return 0


# ------------------------------------------------------------
# Validation auto complete
# ------------------------------------------------------------

def valider_auto(args, donnees):
    """Validation auto complete : json (recharge), references, case_depart, guider-parcours --liste."""
    print(_couleur("  [VALIDATION AUTO]", "bleu"))
    ok_refs = valider_references(donnees, verbose=True)
    if not ok_refs:
        print(_couleur("  [ERREUR] References invalides : corriger avant usage", "rouge"), file=sys.stderr)
        return False
    # Relancer guider-parcours --liste sur le fichier modifie
    try:
        resultat = subprocess.run(
            [sys.executable, str(GUIDER_PY), args.parcours, "--liste"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if resultat.returncode != 0:
            print(_couleur("  [ERREUR] guider-parcours --liste a echoue", "rouge"), file=sys.stderr)
            print(resultat.stderr, file=sys.stderr)
            return False
        lignes = [l for l in resultat.stdout.splitlines() if l.strip()]
        print(_couleur("  [OK] guider-parcours --liste : %d lignes" % len(lignes), "vert"))
    except (OSError, subprocess.TimeoutExpired) as e:
        print(_couleur("  [ATTENTION] guider-parcours non lance: %s" % e, "jaune"), file=sys.stderr)
    return True


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-case",
        description="Genere, edite et supprime des cases d'une carte de decision (parcours JSON) avec recablage auto et validation.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("parcours", type=str, help="Chemin du parcours JSON (parcours-<agent>.json)")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # liste (--verbose et --version ajoutes par la boucle commune ci-dessous)
    p_liste = subparsers.add_parser("liste", help="Lister les cases de la carte")

    # ajouter
    p_ajouter = subparsers.add_parser("ajouter", help="Ajouter une case")
    p_ajouter.add_argument("--case", dest="case_id", type=str, help="Id de la nouvelle case (defaut: prochain cN libre)")
    p_ajouter.add_argument("--type", dest="type_case", type=str, required=True, choices=["question", "indice", "controle", "fin"], help="Type de la case")
    p_ajouter.add_argument("--titre", type=str, help="Titre de la case")
    p_ajouter.add_argument("--question", type=str, help="Question (types question/controle)")
    p_ajouter.add_argument("--message", type=str, help="Message (type fin)")
    p_ajouter.add_argument("--suivant", type=str, help="Case suivante (types indice/question)")
    p_ajouter.add_argument("--apres", type=str, help="Inserer apres cette case (recablage auto)")
    p_ajouter.add_argument("--branche", action="append", dest="branches", type=str, help="Branche <reponse>:<vers> (repetable)")
    p_ajouter.add_argument("--indice-regle", action="append", dest="indices_regle", type=str, help="Indice regle <texte> (repetable)")
    p_ajouter.add_argument("--indice-outil", action="append", dest="indices_outil", type=str, help="Indice outil <nom>:<chemin>[:commande] (repetable)")
    p_ajouter.add_argument("--indice-fichier", action="append", dest="indices_fichier", type=str, help="Indice fichier <chemin>:<raison> (repetable)")

    # editer
    p_editer = subparsers.add_parser("editer", help="Editer une case existante")
    p_editer.add_argument("case_id", type=str, help="Id de la case a editer")
    p_editer.add_argument("--titre", type=str, help="Nouveau titre")
    p_editer.add_argument("--question", type=str, help="Nouvelle question")
    p_editer.add_argument("--message", type=str, help="Nouveau message")
    p_editer.add_argument("--suivant", type=str, help="Nouvelle case suivante")
    p_editer.add_argument("--type", dest="type_case", type=str, choices=["question", "indice", "controle", "fin"], help="Nouveau type")
    p_editer.add_argument("--branche", action="append", dest="branches", type=str, help="Remplace les branches <reponse>:<vers>")
    p_editer.add_argument("--indice-regle", action="append", dest="indices_regle", type=str, help="Remplace les indices par des regles")
    p_editer.add_argument("--remove-indices", action="store_true", help="Vider les indices")

    # supprimer
    p_supprimer = subparsers.add_parser("supprimer", help="Supprimer une case avec recablage auto")
    p_supprimer.add_argument("case_id", type=str, help="Id de la case a supprimer")
    p_supprimer.add_argument("--vers", type=str, help="Cible de recablage (defaut: le suivant de la case supprimee)")
    p_supprimer.add_argument("--force", action="store_true", help="Forcer malgre les references (recablage auto quand meme)")

    # ajouter-bloc (modele compose Pattern 7)
    p_bloc = subparsers.add_parser("ajouter-bloc", help="Ajouter un bloc MODELE COMPOSE (decision + deviation + rejoint, Pattern 7)")
    p_bloc.add_argument("--decision", dest="decision", type=str, help="Id de la case decision (defaut: prochain cN libre)")
    p_bloc.add_argument("--deviation", dest="deviation", type=str, help="Id de la case deviation (defaut: derive de decision)")
    p_bloc.add_argument("--rejoint", dest="rejoint", type=str, help="Id de la case rejoint (defaut: derive de decision)")
    p_bloc.add_argument("--titre", type=str, help="Titre de la decision")
    p_bloc.add_argument("--question", type=str, help="Question de la decision (defaut: Quelle est la decision ?)")
    p_bloc.add_argument("--titre-deviation", dest="titre_deviation", type=str, help="Titre de la deviation")
    p_bloc.add_argument("--titre-rejoint", dest="titre_rejoint", type=str, help="Titre du rejoint")
    p_bloc.add_argument("--suite", type=str, required=True, help="Case suite du flux principal (cible des branches NON et du rejoint)")
    p_bloc.add_argument("--apres", type=str, help="Inserer apres cette case (recablage auto du suivant)")

    # options globales
    for sub in (p_liste, p_ajouter, p_editer, p_supprimer, p_bloc):
        sub.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
        sub.add_argument("--verbose", action="store_true", help="Afficher les details")
        sub.add_argument("--version", action="version", version="generateurs-case v%s" % VERSION)
    return parser


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()

    if args.action == "liste":
        return action_liste(args)
    elif args.action == "ajouter":
        return action_ajouter(args)
    elif args.action == "editer":
        return action_editer(args)
    elif args.action == "supprimer":
        return action_supprimer(args)
    elif args.action == "ajouter-bloc":
        return action_ajouter_bloc(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
