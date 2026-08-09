#!/usr/bin/env python3
# -*- coding: ascii -*-
# generateurs-ligne.py
# Ajoute une LIGNE (chemin de bout en bout) a une carte de decision via des
# gabarits (configs EXTERNALISEES dans gabarits-ligne.json, extensibles via
# ajouter-config sans toucher au code).
# Version : 0.3.0
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
import re
import subprocess
import sys
from pathlib import Path

VERSION = "0.3.0"
STATUT = "ebauche"

# Racine du projet : 5 remontees depuis ce fichier
# (generateurs-ligne -> generateurs -> tools -> agents -> cerveau-projet -> racine)
RACINE = Path(__file__).resolve().parents[5]
GUIDER_PY = RACINE / "cerveau-projet" / "agents" / "tools" / "guider" / "guider-parcours" / "guider-parcours.py"
VALIDER_CASE_PY = RACINE / "cerveau-projet" / "agents" / "tools" / "valider" / "valider-case" / "valider-case.py"

# Fichier des gabarits (configs) externalise : meme dossier que le script
GABARITS_JSON = Path(__file__).resolve().parent / "gabarits-ligne.json"

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
    """Ecrit le parcours JSON en ASCII strict avec indentation 2 et LF pur."""
    chemin = Path(chemin)
    try:
        contenu = json.dumps(donnees, ensure_ascii=True, indent=2)
        contenu.encode("ascii")
    except UnicodeEncodeError:
        print(_couleur("ERREUR: Contenu non-ASCII refuse (regle immuable)", "rouge"), file=sys.stderr)
        sys.exit(1)
    with open(chemin, "w", encoding="ascii", newline="\n") as f:
        f.write(contenu)
        f.write("\n")


# ------------------------------------------------------------
# Gabarits de lignes (configs = groupes de cases), externalises
# ------------------------------------------------------------
# Format interne d'une case (compatibilite numeroter_bloc / action_config) :
#   (suffixe, type, question, titre, branches, suivant)
#   branches : liste de (reponse, suffixe_destination)
#   suivant  : suffixe de destination ou "REJOINT" (case externe)
# Format JSON externe (gabarits-ligne.json) :
#   {"version": "...", "gabarits": {nom: {"description": ..., "cases": [
#       {"suffixe": ..., "type": ..., "titre": ..., "branches": [[r, d], ...],
#        "suivant": ...}, ...]}}}


def _case_json_en_tuple(c):
    """Convertit une case JSON en tuple interne."""
    branches = [[r, d] for r, d in (c.get("branches") or [])]
    return (c.get("suffixe", ""), c.get("type", ""), None,
            c.get("titre", ""), branches, c.get("suivant"))


def charger_gabarits():
    """Charge les gabarits depuis gabarits-ligne.json."""
    try:
        with open(GABARITS_JSON, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(_couleur("ERREUR: Impossible de charger %s : %s" % (GABARITS_JSON, e),
                       "rouge"), file=sys.stderr)
        sys.exit(1)
    gabarits = {}
    for nom, spec in donnees.get("gabarits", {}).items():
        gabarits[nom] = {
            "description": spec.get("description", ""),
            "cases": [_case_json_en_tuple(c) for c in spec.get("cases", [])],
        }
    return gabarits


def sauvegarder_gabarits(gabarits):
    """Ecrit gabarits-ligne.json (ASCII strict, indentation 2, LF pur, tries par nom)."""
    structure = {"version": VERSION, "gabarits": {}}
    for nom in sorted(gabarits):
        spec = gabarits[nom]
        cases = []
        for (suffixe, typ, _q, titre, branches, suivant) in spec["cases"]:
            cases.append({
                "suffixe": suffixe,
                "type": typ,
                "titre": titre,
                "branches": [[r, d] for r, d in branches],
                "suivant": suivant,
            })
        structure["gabarits"][nom] = {
            "description": spec["description"],
            "cases": cases,
        }
    contenu = json.dumps(structure, ensure_ascii=True, indent=2)
    contenu.encode("ascii")
    with open(GABARITS_JSON, "w", encoding="ascii", newline="\n") as f:
        f.write(contenu)
        f.write("\n")


GABARITS = charger_gabarits()


# ------------------------------------------------------------
# Verification de la carte cartographique d'Atlas
# ------------------------------------------------------------

def chemin_cartographie(chemin_parcours, agent):
    """Chemin de la carte Atlas : meme dossier que le parcours, cartographie-<agent>.md."""
    return Path(chemin_parcours).parent / ("cartographie-%s.md" % agent)


def etat_cartographie(chemin_parcours, agent):
    """Retourne (a_jour, raison). Carte a jour = fichier existe ET mtime > mtime parcours."""
    p_parcours = Path(chemin_parcours)
    p_carto = chemin_cartographie(chemin_parcours, agent)
    if not p_carto.exists():
        return False, "ABSENTE: cartographie-%s.md introuvable (%s)" % (agent, p_carto)
    m_parcours = p_parcours.stat().st_mtime
    m_carto = p_carto.stat().st_mtime
    if m_carto < m_parcours:
        return False, "PERIMEE: la carte (%s) est plus ancienne que le parcours (%s)" % (
            p_carto.name, p_parcours.name)
    return True, "A JOUR: %s (%s)" % (p_carto.name, p_carto)


def action_verifier(args):
    """Verdict CARTE A JOUR / A REGENERER."""
    donnees = charger_parcours(args.parcours)
    agent = donnees["parcours"].get("agent", "agent")
    a_jour, raison = etat_cartographie(args.parcours, agent)
    if a_jour:
        print(_couleur("[CARTE A JOUR] %s" % raison, "vert"))
        return 0
    print(_couleur("[CARTE A REGENERER] %s" % raison, "jaune"))
    print(_couleur("  -> Active Atlas via SA carte (case c31 Cartographier) pour regenerer "
                   "cartographie-%s.md, puis reviens continuer." % agent, "jaune"))
    print("  -> Ou utilise --force sur l'action ajouter pour passer outre (decision explicite).")
    return 1


# ------------------------------------------------------------
# Validation d'un gabarit externe (sous-commande ajouter-config)
# ------------------------------------------------------------

_TYPES_AUTORISES = ("question", "controle", "action")


def valider_gabarit_externe(nom, description, cases):
    """Valide un gabarit externe avant insertion dans gabarits-ligne.json.

    Regles :
      1. Le nom est conforme (lettres minuscules, chiffres, tirets).
      2. La description n'est pas vide.
      3. Les cases sont valides : chaque case a suffixe/type/titre ;
         les types sont dans (question, controle, action) ; les branches
         (question/controle) ont au moins 2 destinations existantes ;
         les suivants d'action pointent vers un suffixe existant ou REJOINT.
      4. La case REJOINT est presente.
    Retourne (ok, message_erreur).
    """
    if not re.fullmatch(r"[a-z0-9-]+", nom or ""):
        return False, "Nom de config invalide '%s' (lettres minuscules, chiffres, tirets)" % nom
    if not description or not description.strip():
        return False, "Description obligatoire pour la nouvelle config"
    if not isinstance(cases, list) or not cases:
        return False, "Gabarit vide : au moins une case requise"
    suffixes = []
    for i, c in enumerate(cases):
        if not isinstance(c, dict):
            return False, "Case %d : objet attendu" % (i + 1)
        suf = c.get("suffixe", "")
        typ = c.get("type", "")
        titre = c.get("titre", "")
        suffixes.append(suf)
        if not isinstance(suf, str):
            return False, "Case %d : suffixe manquant" % (i + 1)
        if typ not in _TYPES_AUTORISES:
            return False, "Case %d (%s) : type invalide '%s' (question/controle/action)" % (i + 1, suf, typ)
        if not titre or not isinstance(titre, str):
            return False, "Case %d (%s) : titre manquant" % (i + 1, suf)
    if "REJOINT" not in suffixes:
        return False, "La case REJOINT est obligatoire (retour au flux principal)"
    # Branches : destinations resolvables
    for i, c in enumerate(cases):
        suf = c.get("suffixe", "")
        typ = c.get("type", "")
        branches = c.get("branches") or []
        if typ in ("question", "controle"):
            if len(branches) < 2:
                return False, "Case %d (%s) : au moins 2 branches requises pour une decision" % (i + 1, suf)
            for r, d in branches:
                if d not in suffixes:
                    return False, "Case %d (%s) : destination de branche '%s' inexistante" % (i + 1, suf, d)
        else:
            suivant = c.get("suivant")
            if suivant is not None and suivant not in suffixes:
                return False, "Case %d (%s) : suivant '%s' inexistant" % (i + 1, suf, suivant)
    return True, None


# ------------------------------------------------------------
# Construction du bloc (numerotation conforme c<numero>[a-z]?)
# ------------------------------------------------------------

_LETTRES = "abcdefghijklmnopqrstuvwxyz"


def prochain_numero(cases):
    """Prochain numero libre pour un id cX (base c<numero> sans suffixe)."""
    nums = []
    for cid in cases:
        if cid.startswith("c"):
            reste = cid[1:]
            if reste.isdigit():
                nums.append(int(reste))
    return (max(nums) + 1) if nums else 0


def _destinations(case):
    """Toutes les destinations (branches + suivant) d une case."""
    dests = []
    for b in case.get("branches", []) or []:
        if b.get("vers"):
            dests.append(b["vers"])
    if case.get("suivant"):
        dests.append(case["suivant"])
    return dests


def _est_rejoint(case):
    """Vrai si la case est une case REJOINT (retour au flux principal)."""
    return "REJOINT" in str(case.get("titre", "")).upper()


def _est_fin(case):
    """Vrai si la case ne mene nulle part (fin de parcours)."""
    return not _destinations(case)


def predesseurs(cases):
    """Inverse des liens : id -> liste des ids qui pointent vers lui."""
    inv = {cid: [] for cid in cases}
    for cid, case in cases.items():
        for d in _destinations(case):
            if d in inv:
                inv[d].append(cid)
    return inv


def collecter_groupe(cases, racine):
    """Collecte le groupe de cases atteignable depuis racine (exclut les REJOINT).

    Retourne (ids_ordonnes, liens) : ids_ordonnes = liste des ids du groupe dans
    l ordre de decouverte (la racine en premier), liens = dict id -> case avec les
    liens INTERNES (vers/suivant pointeant vers un membre du groupe). Les liens
    externes sont ramenes a "REJOINT" (le clone les reconnectera).
    """
    vus = []
    en_attente = [racine]
    while en_attente:
        cid = en_attente.pop(0)
        if cid in vus or cid not in cases:
            continue
        case = cases[cid]
        if _est_rejoint(case):
            continue
        vus.append(cid)
        for d in _destinations(case):
            if d in cases and d not in vus and not _est_rejoint(cases.get(d, {})):
                en_attente.append(d)
    # Reconstruire les liens internes (externe -> "REJOINT")
    liens = {}
    for cid in vus:
        case = cases[cid]
        nouveau = dict(case)
        if case.get("type") in ("question", "controle"):
            branches = []
            for b in case.get("branches", []) or []:
                d = b.get("vers")
                if d in vus:
                    branches.append(dict(b, vers=d))
                else:
                    branches.append(dict(b, vers="REJOINT"))
            nouveau["branches"] = branches
        else:
            s = case.get("suivant")
            nouveau["suivant"] = s if s in vus else "REJOINT"
        liens[cid] = nouveau
    return vus, liens


def detecter_groupe(cases, source, mode, branche=None):
    """Detecte le groupe de cases a copier depuis une case source.

    mode : "complet" (remonter a la decision d entree puis tout le sous-chemin),
           "branche" (copier UNIQUEMENT la branche choisie d une decision),
           "suite" (copier le chemin qui part de la source jusqu au REJOINT).
    Retourne (ok, message|(racine, description)).
    """
    if source not in cases:
        return False, "Case source '%s' inexistante" % source
    case = cases[source]
    if mode == "suite":
        return True, (source, "suite depuis %s" % source)
    if mode == "branche":
        if case.get("type") not in ("question", "controle"):
            return False, "Le mode branche exige une decision (question/controle) : '%s' est de type %s" % (source, case.get("type"))
        if not branche:
            return False, "Le mode branche exige --branche <reponse> (OUI/NON/...)"
        dest = None
        for b in case.get("branches", []) or []:
            if b.get("reponse") == branche:
                dest = b.get("vers")
                break
        if not dest:
            return False, "Branche '%s' introuvable sur '%s' (branches: %s)" % (
                branche, source, ", ".join(b.get("reponse", "?") for b in case.get("branches", []) or []))
        return True, (dest, "branche '%s' de %s" % (branche, source))
    # mode complet : si la source est une decision, elle EST le point d entree
    # de la ligne (on copie sa suite complete). Sinon, remonter les predesseurs
    # jusqu a la 1re decision rencontree (point d entree de la ligne).
    if case.get("type") in ("question", "controle"):
        return True, (source, "groupe complet depuis la decision %s" % source)
    inv = predesseurs(cases)
    racine = source
    courant = source
    vu = set()
    while True:
        if courant in vu:
            break
        vu.add(courant)
        preds = [p for p in inv.get(courant, []) if not _est_rejoint(cases.get(p, {}))]
        if not preds:
            break
        p0 = preds[0]
        pred_case = cases.get(p0, {})
        if pred_case.get("type") in ("question", "controle"):
            racine = p0
            break
        racine = p0
        courant = p0
    return True, (racine, "groupe complet depuis %s" % racine)


def cloner_groupe(cases, ids_groupe, liens, base_num, titre_base):
    """Clone le groupe avec de nouveaux ids conformes c<numero>[a-z]?.

    Groupes jusqu a 27 cases : cX + suffixes lettres (cXa, cXb, ...).
    Groupes plus grands : numeros sequentiels c<base+i> (convention c<numero>
    toujours conforme). Retourne (bloc, mapping_ancien_vers_nouveau)."""
    mapping = {}
    if len(ids_groupe) <= 27:
        for i, cid in enumerate(ids_groupe):
            if i == 0:
                mapping[cid] = "c%d" % base_num
            else:
                mapping[cid] = "c%d%s" % (base_num, _LETTRES[i - 1])
    else:
        for i, cid in enumerate(ids_groupe):
            mapping[cid] = "c%d" % (base_num + i)
    bloc = {}
    for cid in ids_groupe:
        case = liens[cid]
        nouveau = {k: v for k, v in case.items() if k != "question" or case.get("type") not in ("question", "controle")}
        nouveau["titre"] = titre_base if cid == ids_groupe[0] and case.get("type") in ("question", "controle") else case["titre"]
        if case.get("type") in ("question", "controle"):
            q = case.get("question") or case["titre"]
            nouveau["question"] = "LIGNE [%s] : %s" % (titre_base, q)
            branches = []
            for b in case.get("branches", []) or []:
                d = b.get("vers")
                branches.append({"reponse": b.get("reponse"), "vers": mapping[d]})
            nouveau["branches"] = branches
        else:
            s = case.get("suivant")
            if s == "REJOINT":
                nouveau["suivant"] = "REJOINT"  # reconnecte par l appelant
            else:
                nouveau["suivant"] = mapping[s]
        bloc[mapping[cid]] = nouveau
    return bloc, mapping


def numeroter_bloc(spec, titre_base, rejoint, base_num):
    """Construit le bloc avec ids c<base_num>, c<base_num>a, c<base_num>b, ...

    Convention de nommage valider-case : c<numero>[a-z]? (pas de point).
    La case REJOINT du bloc pointe TOUJOURS vers le rejoint externe.
    """
    bloc = {}
    n = base_num
    ids = {}
    # 1ere passe : attribuer les ids reels (premiere case = cX, suivantes = cXa, cXb, ...)
    for i, (suffixe, typ, _q, titre, branches, suivant) in enumerate(spec["cases"]):
        if suffixe == "":
            cid = "c%d" % n
        else:
            cid = "c%d%s" % (n, _LETTRES[i - 1])
        ids[suffixe] = cid
    # 2e passe : construire les cases
    for i, (suffixe, typ, _q, titre, branches, suivant) in enumerate(spec["cases"]):
        cid = ids[suffixe]
        case = {"titre": titre, "type": typ}
        if typ in ("question", "controle"):
            q = titre_base if titre is None else titre
            case["question"] = "LIGNE [%s] : %s" % (titre_base, q)
            b = []
            for rep, dst in branches:
                b.append({"reponse": rep, "vers": ids[dst]})
            case["branches"] = b
        else:
            if suffixe == "REJOINT":
                case["suivant"] = rejoint
            else:
                case["suivant"] = ids[suivant] if suivant in ids else rejoint
        bloc[cid] = case
    return bloc


# ------------------------------------------------------------
# Validation auto (reprise generateurs-carte)
# ------------------------------------------------------------

def valider_auto(chemin, donnees):
    """Validation auto : guider-parcours --liste puis valider-case --modele --references."""
    print(_couleur("  [VALIDATION AUTO]", "bleu"))
    try:
        resultat = subprocess.run(
            [sys.executable, str(GUIDER_PY), str(chemin), "--liste"],
            capture_output=True, text=True, timeout=30,
        )
        if resultat.returncode != 0:
            print(_couleur("  [ERREUR] guider-parcours --liste a echoue", "rouge"), file=sys.stderr)
            print(resultat.stderr, file=sys.stderr)
            return False
        lignes = [l for l in resultat.stdout.splitlines() if l.strip()]
        print(_couleur("  [OK] guider-parcours --liste : %d lignes" % len(lignes), "vert"))
    except (OSError, subprocess.TimeoutExpired) as e:
        print(_couleur("  [ATTENTION] guider-parcours non lance: %s" % e, "jaune"), file=sys.stderr)
    try:
        resultat = subprocess.run(
            [sys.executable, str(VALIDER_CASE_PY), str(chemin), "--modele", "--references", "--dry-run"],
            capture_output=True, text=True, timeout=30,
        )
        lignes = [l for l in resultat.stdout.splitlines() if l.strip()]
        for l in lignes[-6:]:
            print(_couleur("  | " + l, "bleu"))
        if resultat.returncode != 0:
            print(_couleur("  [ERREUR] valider-case a signale des problemes", "rouge"), file=sys.stderr)
            return False
        print(_couleur("  [OK] valider-case : conforme", "vert"))
    except (OSError, subprocess.TimeoutExpired) as e:
        print(_couleur("  [ATTENTION] valider-case non lance: %s" % e, "jaune"), file=sys.stderr)
    return True


# ------------------------------------------------------------
# Actions
# ------------------------------------------------------------

def action_lister_configs(args):
    """Liste les gabarits disponibles (depuis gabarits-ligne.json)."""
    print("=== Gabarits de lignes (configs) ===")
    print("")
    for nom in sorted(GABARITS):
        spec = GABARITS[nom]
        nb_cases = len(spec["cases"])
        print("  %-10s : %s (%d cases)" % (nom, spec["description"], nb_cases))
    print("")
    print("Usage : generateurs-ligne.py <parcours.json> config <nom>")
    return 0


def action_config(args):
    """Detail d'un gabarit."""
    if args.config not in GABARITS:
        print(_couleur("ERREUR: Config inconnue '%s' (lister-configs pour la liste)" % args.config, "rouge"), file=sys.stderr)
        sys.exit(1)
    spec = GABARITS[args.config]
    print("=== Config : %s === " % args.config)
    print("  %s" % spec["description"])
    print("  Cases du bloc :")
    for i, (suffixe, typ, _q, titre, branches, suivant) in enumerate(spec["cases"]):
        nom = "cX" if suffixe == "" else ("cX" + _LETTRES[i - 1] if suffixe != "REJOINT" else "REJOINT")
        if branches:
            sortie = "branches %s" % ", ".join("%s->cX%s" % (r, _LETTRES[int(d[1:]) - 1]) for r, d in branches)
        else:
            sortie = "suivant %s" % ("REJOINT externe" if suivant == "REJOINT" else "cX" + _LETTRES[int(suivant[1:]) - 1])
        print("    %-10s (%s) %s | %s" % (nom, typ, titre, sortie))
    return 0


def action_ajouter(args):
    """Ajoute une ligne (bloc de cases) au parcours, avec dry/wet."""
    if args.config not in GABARITS:
        print(_couleur("ERREUR: Config inconnue '%s' (lister-configs pour la liste)" % args.config, "rouge"), file=sys.stderr)
        sys.exit(1)
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    agent = donnees["parcours"].get("agent", "agent")

    # 1. Verification carte Atlas (sauf --force)
    if not args.force:
        a_jour, raison = etat_cartographie(args.parcours, agent)
        if not a_jour:
            print(_couleur("[CARTE A REGENERER] %s" % raison, "jaune"))
            print(_couleur("  -> Active Atlas via SA carte (case c31 Cartographier) pour regenerer "
                           "cartographie-%s.md, puis reviens continuer. Utilise --force pour passer outre." % agent, "jaune"))
            sys.exit(1)
        print(_couleur("[CARTE A JOUR] %s" % raison, "vert"))

    # 2. Point d'attache : la case existante d'ou part la ligne
    attache = args.point_attache or donnees["parcours"].get("case_depart", "c0")
    if attache not in cases:
        print(_couleur("ERREUR: Case d'attache '%s' inexistante" % attache, "rouge"), file=sys.stderr)
        sys.exit(1)
    case_attache = cases[attache]
    type_attache = case_attache.get("type", "?")

    # 3. Determiner la cible de rejoint par defaut
    ancien_suivant = case_attache.get("suivant")
    if args.rejoint:
        rejoint = args.rejoint
        if rejoint not in cases:
            print(_couleur("ERREUR: Case de rejoint '%s' inexistante" % rejoint, "rouge"), file=sys.stderr)
            sys.exit(1)
    else:
        if type_attache in ("action", "indice") and ancien_suivant:
            rejoint = ancien_suivant
        else:
            # defaut : la fin existante la plus proche est inconnue -> on exige --rejoint
            print(_couleur("ERREUR: Impossible de determiner la case de rejoint : preciser --rejoint <case> "
                           "(le point d'attache '%s' est une %s sans suivant)" % (attache, type_attache), "rouge"), file=sys.stderr)
            sys.exit(1)

    # 4. Construire le bloc
    base_num = prochain_numero(cases)
    spec = GABARITS[args.config]
    titre_base = args.titre or "Ligne %s" % args.config
    bloc = numeroter_bloc(spec, titre_base, rejoint, base_num)
    ids_bloc = sorted(bloc)
    premier = "c%d" % base_num

    # 5. Cablage du point d'attache
    cablage = None
    if type_attache in ("question", "controle"):
        reponse = args.reponse or "NON"
        for b in case_attache.get("branches", []):
            if b.get("reponse") == reponse:
                print(_couleur("ERREUR: La branche '%s' existe deja sur '%s'" % (reponse, attache), "rouge"), file=sys.stderr)
                sys.exit(1)
        case_attache.setdefault("branches", []).append({"reponse": reponse, "vers": premier})
        cablage = "branche '%s' ajoutee sur %s -> %s" % (reponse, attache, premier)
    elif type_attache in ("action", "indice"):
        case_attache["suivant"] = premier
        cablage = "suivant de %s recable : %s -> %s (rejoint sur %s)" % (attache, ancien_suivant, premier, rejoint)
    else:
        print(_couleur("ERREUR: Point d'attache '%s' de type '%s' non cablable" % (attache, type_attache), "rouge"), file=sys.stderr)
        sys.exit(1)

    # 6. Dry-run / wet
    if args.dry_run:
        print(_couleur("[DRY-RUN] Ligne ajoutee (config %s, %d cases) :" % (args.config, len(bloc)), "jaune"))
        print("  Point d'attache : %s (%s) -> %s" % (attache, type_attache, premier))
        print("  Cablage : %s" % cablage)
        print("  Rejoint : %s" % rejoint)
        print("  Nouvelles cases : %s" % ", ".join(ids_bloc))
        return 0

    # Wet : appliquer
    cases.update(bloc)
    sauvegarder_parcours(args.parcours, donnees)
    print(_couleur("[OK] Ligne ajoutee (config %s, %d cases) : %s" % (args.config, len(bloc), ", ".join(ids_bloc)), "vert"))
    print("  Point d'attache : %s (%s) -> %s" % (attache, type_attache, premier))
    print("  Cablage : %s" % cablage)
    print("  Rejoint : %s" % rejoint)
    valider_auto(args.parcours, donnees)
    return 0


def action_ajouter_config(args):
    """Ajoute une nouvelle config (gabarit) reutilisable dans gabarits-ligne.json.

    Le gabarit est fourni par --gabarit <fichier.json> de structure
    {"cases": [{"suffixe": ..., "type": ..., "titre": ..., "branches": [[r, d], ...],
                "suivant": ...}, ...]} (format JSON externe des cases).
    Validation complete avant insertion ; dry-run simule sans ecrire.
    """
    # 1. Lire et valider le gabarit externe
    chemin = Path(args.gabarit)
    if not chemin.exists():
        print(_couleur("ERREUR: Fichier gabarit introuvable: %s" % chemin, "rouge"), file=sys.stderr)
        sys.exit(1)
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            donnees_gabarit = json.load(f)
    except json.JSONDecodeError as e:
        print(_couleur("ERREUR: JSON invalide: %s" % e, "rouge"), file=sys.stderr)
        sys.exit(1)
    cases_json = donnees_gabarit.get("cases") if isinstance(donnees_gabarit, dict) else None
    ok, erreur = valider_gabarit_externe(args.nom, args.description, cases_json)
    if not ok:
        print(_couleur("ERREUR: %s" % erreur, "rouge"), file=sys.stderr)
        sys.exit(1)

    # 2. Conflit de nom
    if args.nom in GABARITS and not args.force:
        print(_couleur("ERREUR: La config '%s' existe deja (--force pour ecraser)" % args.nom, "rouge"), file=sys.stderr)
        sys.exit(1)

    # 3. Construire la spec interne (tuples)
    spec = {
        "description": args.description,
        "cases": [_case_json_en_tuple(c) for c in cases_json],
    }

    # 4. Dry-run / wet
    if args.dry_run:
        print(_couleur("[DRY-RUN] Config '%s' pret a etre ajoutee (%d cases) :" % (args.nom, len(spec["cases"])), "jaune"))
        print("  Description : %s" % spec["description"])
        for i, (suffixe, typ, _q, titre, _branches, _suivant) in enumerate(spec["cases"]):
            nom_case = "cX" if suffixe == "" else ("cX" + _LETTRES[i - 1] if suffixe != "REJOINT" else "REJOINT")
            print("    %-8s (%s) %s" % (nom_case, typ, titre))
        print("  (Aucun fichier modifie)")
        return 0

    # Wet : insertion programmatique + sauvegarde triee
    GABARITS[args.nom] = spec
    sauvegarder_gabarits(GABARITS)
    print(_couleur("[OK] Config '%s' ajoutee a gabarits-ligne.json (%d cases)" % (args.nom, len(spec["cases"])), "vert"))
    print("  Description : %s" % spec["description"])
    print("  Disponible : generateurs-ligne.py <parcours.json> ajouter --config %s" % args.nom)
    return 0


def action_copier(args):
    """Copie une LIGNE existante (groupe de cases) depuis une case de la carte
    OU depuis une config, et la reclone sur un point d'attache. Dry/wet.

    Sources : --source <case> (avec --mode complet|branche|suite) ou
    --config <nom> (gabarit de gabarits-ligne.json).
    """
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    agent = donnees["parcours"].get("agent", "agent")

    # 1. Determiner la source (case OU config)
    if args.source:
        ok, res = detecter_groupe(cases, args.source, args.mode, args.branche)
        if not ok:
            print(_couleur("ERREUR: %s" % res, "rouge"), file=sys.stderr)
            sys.exit(1)
        racine, description = res
        ids_groupe, liens = collecter_groupe(cases, racine)
        if not ids_groupe:
            print(_couleur("ERREUR: Aucune case copiable depuis '%s'" % args.source, "rouge"), file=sys.stderr)
            sys.exit(1)
    elif args.config:
        if args.config not in GABARITS:
            print(_couleur("ERREUR: Config inconnue '%s' (lister-configs pour la liste)" % args.config, "rouge"), file=sys.stderr)
            sys.exit(1)
        spec = GABARITS[args.config]
        # simuler un groupe depuis la spec (tuples -> cases internes)
        base_num_tmp = prochain_numero(cases)
        bloc_tmp = numeroter_bloc(spec, "TMP", "REJOINT", base_num_tmp)
        ids_groupe = sorted(bloc_tmp)
        liens = bloc_tmp
        description = "config %s" % args.config
    else:
        print(_couleur("ERREUR: Preciser --source <case> ou --config <nom>", "rouge"), file=sys.stderr)
        sys.exit(1)

    # 2. Verification carte Atlas (sauf --force)
    if not args.force:
        a_jour, raison = etat_cartographie(args.parcours, agent)
        if not a_jour:
            print(_couleur("[CARTE A REGENERER] %s" % raison, "jaune"))
            print(_couleur("  -> Active Atlas via SA carte (case c31 Cartographier) pour regenerer "
                           "cartographie-%s.md, puis reviens continuer. Utilise --force pour passer outre." % agent, "jaune"))
            sys.exit(1)
        print(_couleur("[CARTE A JOUR] %s" % raison, "vert"))

    # 3. Point d'attache
    attache = args.point_attache or donnees["parcours"].get("case_depart", "c0")
    if attache not in cases:
        print(_couleur("ERREUR: Case d'attache '%s' inexistante" % attache, "rouge"), file=sys.stderr)
        sys.exit(1)
    case_attache = cases[attache]
    type_attache = case_attache.get("type", "?")

    # 4. Rejoint par defaut
    ancien_suivant = case_attache.get("suivant")
    if args.rejoint:
        rejoint = args.rejoint
        if rejoint not in cases:
            print(_couleur("ERREUR: Case de rejoint '%s' inexistante" % rejoint, "rouge"), file=sys.stderr)
            sys.exit(1)
    else:
        if type_attache in ("action", "indice") and ancien_suivant:
            rejoint = ancien_suivant
        else:
            print(_couleur("ERREUR: Impossible de determiner la case de rejoint : preciser --rejoint <case> "
                           "(le point d'attache '%s' est une %s sans suivant)" % (attache, type_attache), "rouge"), file=sys.stderr)
            sys.exit(1)

    # 5. Construire le clone
    base_num = prochain_numero(cases)
    titre_base = args.titre or ("Ligne copiee (%s)" % description)
    bloc, mapping = cloner_groupe(cases, ids_groupe, liens, base_num, titre_base)
    # reconnecter les REJOINT du clone vers le rejoint externe
    for cid in bloc:
        case = bloc[cid]
        if case.get("type") not in ("question", "controle") and case.get("suivant") == "REJOINT":
            case["suivant"] = rejoint
    premier = "c%d" % base_num

    # 6. Cablage du point d'attache
    cablage = None
    if type_attache in ("question", "controle"):
        reponse = args.reponse or "NON"
        for b in case_attache.get("branches", []):
            if b.get("reponse") == reponse:
                print(_couleur("ERREUR: La branche '%s' existe deja sur '%s'" % (reponse, attache), "rouge"), file=sys.stderr)
                sys.exit(1)
        case_attache.setdefault("branches", []).append({"reponse": reponse, "vers": premier})
        cablage = "branche '%s' ajoutee sur %s -> %s" % (reponse, attache, premier)
    elif type_attache in ("action", "indice"):
        case_attache["suivant"] = premier
        cablage = "suivant de %s recable : %s -> %s (rejoint sur %s)" % (attache, ancien_suivant, premier, rejoint)
    else:
        print(_couleur("ERREUR: Point d'attache '%s' de type '%s' non cablable" % (attache, type_attache), "rouge"), file=sys.stderr)
        sys.exit(1)

    # 7. Dry-run / wet
    if args.dry_run:
        print(_couleur("[DRY-RUN] Ligne copiee (%s, %d cases) :" % (description, len(bloc)), "jaune"))
        print("  Source : %s" % description)
        print("  Point d'attache : %s (%s) -> %s" % (attache, type_attache, premier))
        print("  Cablage : %s" % cablage)
        print("  Rejoint : %s" % rejoint)
        print("  Nouvelles cases : %s" % ", ".join(sorted(bloc)))
        return 0

    cases.update(bloc)
    sauvegarder_parcours(args.parcours, donnees)
    print(_couleur("[OK] Ligne copiee (%s, %d cases) : %s" % (description, len(bloc), ", ".join(sorted(bloc))), "vert"))
    print("  Point d'attache : %s (%s) -> %s" % (attache, type_attache, premier))
    print("  Cablage : %s" % cablage)
    print("  Rejoint : %s" % rejoint)
    valider_auto(args.parcours, donnees)
    return 0


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-ligne",
        description="Ajoute une LIGNE (chemin de bout en bout) a une carte de decision via des gabarits de groupes de cases (configs), apres verification de la carte cartographique d'Atlas. Dry/wet pour valider. Les configs sont externalisees dans gabarits-ligne.json et extensibles via ajouter-config.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # verifier
    p_ver = subparsers.add_parser("verifier", help="Verifier que la carte Atlas (cartographie-<agent>.md) est a jour")
    p_ver.add_argument("parcours", type=str, help="Chemin du parcours JSON")

    # lister-configs
    p_list = subparsers.add_parser("lister-configs", help="Lister les gabarits de lignes disponibles")
    p_list.add_argument("parcours", type=str, nargs="?", help="Chemin du parcours JSON (optionnel)")

    # config
    p_cfg = subparsers.add_parser("config", help="Afficher le detail d'un gabarit")
    p_cfg.add_argument("parcours", type=str, nargs="?", help="Chemin du parcours JSON (optionnel)")
    p_cfg.add_argument("config", type=str, help="Nom du gabarit (defaut, config-1, config-2, config-3)")

    # ajouter
    p_add = subparsers.add_parser("ajouter", help="Ajouter une ligne (groupe de cases) au parcours")
    p_add.add_argument("parcours", type=str, help="Chemin du parcours JSON")
    p_add.add_argument("--config", type=str, required=True, help="Gabarit a utiliser (defaut, config-1, config-2, config-3)")
    p_add.add_argument("--point-attache", dest="point_attache", type=str, default=None, help="Case existante d'ou part la ligne (defaut: case_depart)")
    p_add.add_argument("--rejoint", type=str, default=None, help="Case ou la ligne revient au flux (defaut: ancien suivant de l'attache)")
    p_add.add_argument("--titre", type=str, default=None, help="Titre de base de la ligne (defaut: Ligne <config>)")
    p_add.add_argument("--reponse", type=str, default=None, help="Reponse de la branche creee sur une question/controle (defaut: NON)")
    p_add.add_argument("--force", action="store_true", help="Passer outre une carte Atlas absente/perimee")
    p_add.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    p_add.add_argument("--verbose", action="store_true", help="Afficher les details")

    # ajouter-config
    p_addcfg = subparsers.add_parser("ajouter-config", help="Ajouter une nouvelle config (gabarit reutilisable) dans gabarits-ligne.json")
    p_addcfg.add_argument("nom", type=str, help="Nom de la config (lettres minuscules, chiffres, tirets)")
    p_addcfg.add_argument("--description", type=str, required=True, help="Description de la nouvelle config")
    p_addcfg.add_argument("--gabarit", type=str, required=True, help="Chemin du fichier JSON du gabarit ({cases: [...]})")
    p_addcfg.add_argument("--force", action="store_true", help="Ecraser une config existante du meme nom")
    p_addcfg.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    p_addcfg.add_argument("--verbose", action="store_true", help="Afficher les details")

    # copier
    p_cop = subparsers.add_parser("copier", help="Copier une LIGNE existante (groupe de cases) depuis une case de la carte ou une config, et la recloner sur un point d'attache")
    p_cop.add_argument("parcours", type=str, help="Chemin du parcours JSON")
    p_cop.add_argument("--source", type=str, default=None, help="Case source dont on copie la ligne (alternative a --config)")
    p_cop.add_argument("--config", type=str, default=None, help="Gabarit (config) a copier (alternative a --source)")
    p_cop.add_argument("--mode", type=str, choices=["complet", "branche", "suite"], default="complet", help="Mode de detection du groupe depuis --source (complet/branche/suite)")
    p_cop.add_argument("--branche", type=str, default=None, help="Reponse de la branche a copier (mode branche)")
    p_cop.add_argument("--point-attache", dest="point_attache", type=str, default=None, help="Case existante d'ou part la ligne copiee (defaut: case_depart)")
    p_cop.add_argument("--rejoint", type=str, default=None, help="Case ou la ligne copiee revient au flux (defaut: ancien suivant de l'attache)")
    p_cop.add_argument("--titre", type=str, default=None, help="Titre de base de la ligne copiee (defaut: Ligne copiee (...))")
    p_cop.add_argument("--reponse", type=str, default=None, help="Reponse de la branche creee sur une question/controle (defaut: NON)")
    p_cop.add_argument("--force", action="store_true", help="Passer outre une carte Atlas absente/perimee")
    p_cop.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
    p_cop.add_argument("--verbose", action="store_true", help="Afficher les details")

    for sub in (p_ver, p_list, p_cfg, p_add, p_addcfg, p_cop):
        sub.add_argument("--version", action="version", version="generateurs-ligne v%s" % VERSION)
    return parser


def main():
    verifier_nommage(sys.argv[0])
    if "--version" in sys.argv:
        print("generateurs-ligne v%s" % VERSION)
        return 0
    # Aide racine uniquement si AUCUNE sous-commande n'est donnee
    # (sinon argparse affiche l'aide du sous-parser, ex: ajouter --help)
    if "--aide" in sys.argv or "-h" in sys.argv or "--help" in sys.argv:
        if len(sys.argv) == 2 or sys.argv[1] in ("--aide", "-h", "--help"):
            construire_parser().print_help()
            return 0
    parser = construire_parser()
    args = parser.parse_args()

    if args.action == "verifier":
        return action_verifier(args)
    elif args.action == "lister-configs":
        return action_lister_configs(args)
    elif args.action == "config":
        return action_config(args)
    elif args.action == "ajouter":
        return action_ajouter(args)
    elif args.action == "ajouter-config":
        return action_ajouter_config(args)
    elif args.action == "copier":
        return action_copier(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
