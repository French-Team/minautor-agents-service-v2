"""Fonctions communes de l'outil domicilier : lire une classe, batir une delegation.

Chaque fonction fait UNE chose (convention-architecture-outils). La remorque ne
COMPREND pas la classe : elle lit chaque texte, extrait le bloc EXACT de la
fonction, et le remplace par une DELEGATION au domicile (le motif est PARTAGE,
jamais recopie -- M-076).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from constants import (
    CHAMPS_PLAN,
    CHAMPS_PLAN_OPTIONNELS,
    DOSSIERS_IGNORES,
    DOSSIERS_TECHNIQUES,
    ENCODAGE,
    EXTENSIONS_CLASSE,
    INDENTATION,
    MOTIF_POINT_RESTAURATION,
    PERIMETRE,
    PLACEHOLDER_EXTRAS,
    NOM_PORTE_ECRIRE,
    RACINE,
    ZONE_FRAGMENTS,
)

# Le DOMICILE partage (EO-158) : le parseur d options est PARTAGE, jamais
# recopie -- cette remorque est NEE de ce constat, elle ne va pas le contredire.
from options import CLE_SANS_VALEUR, extraire_options  # noqa: E402
# EO-287 : la resolution d un outil par son NOM est PARTAGEE (un seul domicile).
from resolution_outils import chemin_outil  # noqa: E402


def lire_texte(chemin):
    """Texte UTF-8 d'un fichier, ou chaine vide s'il est illisible."""
    try:
        return Path(chemin).read_text(encoding=ENCODAGE)
    except (OSError, UnicodeDecodeError):
        return ""


def lister_fichiers(perimetre=None):
    """Fichiers candidats du perimetre (sans bruit : .bak, archives, zones tmp)."""
    base = Path(perimetre) if perimetre else PERIMETRE
    ignores = DOSSIERS_IGNORES if base.resolve() == PERIMETRE else DOSSIERS_TECHNIQUES
    trouves = []
    for extension in EXTENSIONS_CLASSE:
        for p in sorted(base.rglob("*" + extension)):
            if any(dossier in p.parts for dossier in ignores):
                continue
            if MOTIF_POINT_RESTAURATION in p.name:
                continue
            trouves.append(p)
    return trouves


def bloc_fonction(texte, fonction):
    """Bloc EXACT de la fonction : de sa ligne jusqu'au retour a la colonne 0.

    Le bloc n'est jamais REDEVINE : il est LU dans le fichier. C'est ce qui rend
    le remplacement exact (l'editeur de la porte l'exige) et l'alignement sur.
    """
    lignes = texte.splitlines()
    debut = None
    for i, ligne in enumerate(lignes):
        if re.match(r"def " + re.escape(fonction) + r"\(", ligne):
            debut = i
            break
    if debut is None:
        return None
    fin = debut + 1
    while fin < len(lignes) and (not lignes[fin].strip() or lignes[fin].startswith(INDENTATION)):
        fin += 1
    while fin > debut and not lignes[fin - 1].strip():
        fin -= 1
    return "\n".join(lignes[debut:fin])


def est_alignee(texte, plan):
    """La copie CONSOMME-t-elle deja le domicile ? (le marqueur du plan le dit)"""
    return plan["marqueur"] in texte


def deriver_extras(bloc):
    """Suffixe d'appel DEDUIT du texte ancien : drapeaux + mode sans tirets.

    Mesure MO-171 : dix outils declarent des drapeaux (json, recursif, prive,
    verbose, integration, etat) et deux nomment leurs options sans tirets de
    tete. La deduction est CONSERVATRICE : un plan peut toujours la corriger par
    `extras` (c'est ainsi que `maintenir` a recu son drapeau `etat`, qui ne
    marchait avant que par une valeur vide accidentelle).
    """
    if not bloc:
        return ""
    sans_tirets = bool(re.search(r"lstrip", bloc) or "startswith" not in bloc)
    trouve = re.search(r"if nom in (\([^)]*\)|[A-Z_]+)\s*:", bloc)
    extras = ""
    if trouve:
        extras += ", drapeaux=" + trouve.group(1)
    if sans_tirets:
        extras += ", sans_tirets=True"
    return extras


def construire_delegation(plan, extras):
    """Bloc de remplacement : la docstring, l'import du domicile, l'appel."""
    return "\n".join([
        "def " + plan["fonction"] + "(arguments, noms_connus):",
        plan["docstring"],
        plan["import"],
        plan["appel"].replace(PLACEHOLDER_EXTRAS, extras),
    ])


def chemin_domicile(plan):
    """Chemin absolu du module qui porte le CONTRAT de la classe."""
    return RACINE / plan["domicile"]


def verifier_premisses(plan):
    """Refus NOMME : un plan dont une premisse est fausse ne doit rien aligner.

    1. le DOMICILE existe et porte la fonction (sinon on delegue vers du vide) ;
    2. le MARQUEUR cite le module du domicile (sinon la marque est incoherente) ;
    3. chaque EXCLUSION existe ET contient la fonction (une exclusion qui
       n'exclut rien est un mensonge : mesure MO-171, un balayage doit DIRE ses
       exclusions, pas les oublier).
    """
    ecarts = []
    domicile = chemin_domicile(plan)
    if not domicile.is_file():
        ecarts.append("domicile introuvable : " + plan["domicile"])
    else:
        module = domicile.stem
        if not re.search(r"def " + re.escape(plan["fonction"]) + r"\(", lire_texte(domicile)):
            ecarts.append("le domicile ne porte PAS la fonction : " + plan["fonction"])
        if module not in plan["marqueur"]:
            ecarts.append("le marqueur ne cite pas le module du domicile : " + module)
    for chemin in plan.get("exclus", []):
        cible = RACINE / chemin
        if not cible.is_file():
            ecarts.append("exclusion introuvable : " + chemin)
        elif not re.search(r"def " + re.escape(plan["fonction"]) + r"\(", lire_texte(cible)):
            ecarts.append("exclusion qui n'exclut RIEN (pas de " + plan["fonction"] + ") : " + chemin)
    return ecarts


def charger_plan(chemin):
    """Lit et VERIFIE le plan : champs fermes presents, listes bien typees."""
    try:
        donnees = json.loads(Path(chemin).read_text(encoding=ENCODAGE))
    except (OSError, json.JSONDecodeError) as erreur:
        raise ValueError("plan illisible : " + str(erreur))
    manquants = [champ for champ in CHAMPS_PLAN if not donnees.get(champ)]
    if manquants:
        raise ValueError("plan incomplet, champs manquants : " + ", ".join(manquants))
    for champ in CHAMPS_PLAN_OPTIONNELS:
        donnees.setdefault(champ, [] if champ in ("exclus", "attendu") else {})
    if donnees["derive"] and PLACEHOLDER_EXTRAS not in donnees["appel"]:
        raise ValueError("derive demande mais l'appel ne porte pas " + PLACEHOLDER_EXTRAS)
    donnees["_chemin"] = str(chemin)
    return donnees


def relatif(chemin):
    """Chemin du workspace, tel que la PORTE l'attend (racine-relative)."""
    return Path(chemin).resolve().relative_to(RACINE).as_posix()


def auditer(plan, perimetre=None):
    """Rapport de classe : copies, deja alignees, a aligner, exclues, HORS PLAN.

    `hors_plan` est le TROU : une copie ni alignee ni declaree exclue. Un plan
    qui laisse un trou n'a pas fini son travail -- et le rapport le DIT, au lieu
    de compter les copies alignees et de se taire sur les autres.
    """
    exclues = list(plan.get("exclus", []))
    alignees, a_aligner, hors_plan = [], [], []
    for chemin in lister_fichiers(perimetre):
        rel = relatif(chemin)
        texte = lire_texte(chemin)
        if not re.search(r"def " + re.escape(plan["fonction"]) + r"\(", texte):
            continue
        if rel in exclues or rel == plan["domicile"]:
            continue
        if est_alignee(texte, plan):
            alignees.append(rel)
        else:
            a_aligner.append(rel)
    vus = set(alignees) | set(a_aligner) | set(exclues) | {plan["domicile"]}
    hors_plan, disparues = [], []
    attendu = plan.get("attendu") or []
    if attendu:
        # PERIMETRE DECLARE : une copie que le plan ne LISTE pas est un TROU (le
        # plan doit etre mis a jour), et une copie listee qui ne porte plus la
        # fonction dit que le plan est PERIME. Sans `attendu`, le plan travaille
        # en perimetre ouvert -- et le rapport le DIT au lieu de le taire.
        hors_plan = [rel for rel in alignees + a_aligner if rel not in set(attendu)]
        base = Path(perimetre).resolve() if perimetre else PERIMETRE
        for rel in attendu:
            chemin = (RACINE / rel).resolve()
            if rel in vus or not chemin.is_file() or base not in chemin.parents:
                continue
            disparues.append(rel)
    return {
        "classe": plan["classe"],
        "domicile": plan["domicile"],
        "perimetre_declare": bool(attendu),
        "alignees": alignees,
        "a_aligner": a_aligner,
        "exclues": exclues,
        "hors_plan": hors_plan,
        "disparues": disparues,
    }


def appeler_porte(arguments):
    """Passe par le DERNIER outil qui a le droit d'ecrire : la porte."""
    p = subprocess.run([sys.executable, str(chemin_outil(NOM_PORTE_ECRIRE))] + arguments,
                       capture_output=True, text=True, cwd=str(RACINE))
    sortie = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()
    return p.returncode, (sortie[-1] if sortie else "code " + str(p.returncode))


def ecrire_fragment(chemin, contenu):
    """Ecrire un fragment, c'est DEJA passer par la porte (aucun raccourci)."""
    return appeler_porte(["ecrire", "--fichier", relatif(chemin), "--mode", "remplacer", "--contenu", contenu])


def publier(rel, bloc, delegation, simuler=True):
    """Aligne UNE copie. Retourne (code, message).

    --simuler est le defaut : rien ne s'ecrit. En publication, les fragments
    passent par la porte puis la cible est remplacee PAR la porte : si la
    validation refuse, la cible reste INTACTE (garantie EO-129).
    """
    if simuler:
        return 0, "SIMULE : " + rel + " (" + str(len(bloc.splitlines())) + " ligne(s) -> delegation)"
    etiquette = Path(rel).stem + "-" + str(len(rel))
    ancien = ZONE_FRAGMENTS / ("mo172-ancien-" + etiquette + ".txt")
    nouveau = ZONE_FRAGMENTS / ("mo172-nouveau-" + etiquette + ".txt")
    for chemin, contenu, nom in ((ancien, bloc, "ancien"), (nouveau, delegation, "nouveau")):
        code, message = ecrire_fragment(chemin, contenu)
        if code != 0:
            return 1, "REFUS fragment " + nom + " de " + rel + " : " + message
    code, message = appeler_porte(["editer", "--fichier", rel,
                                   "--ancien-fichier", relatif(ancien),
                                   "--nouveau-fichier", relatif(nouveau)])
    if code != 0:
        return 1, "REFUS " + rel + " : " + message + " (la cible est INTACTE)"
    return 0, "ALIGNE : " + rel
