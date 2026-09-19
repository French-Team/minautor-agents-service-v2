#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-vocabulaire-etat.py -- Consommateurs qui RECOPIENT un vocabulaire d'etat

Friction 53 (MO-129/MO-134) : la classe "vocabulaire d'etat recopie" se refermait
sur le cas traite et revenait par un AUTRE consommateur, car aucun outil ne
DERIVAIT les valeurs des etats ni ne cherchait leurs copies. Cet outil le fait.

Ni valeur ni domicile n'est ecrit a la main :
  - DECLARATIONS : tout module portant un CONTENEUR au pluriel exact (URGENCES,
    TYPES, STATUTS, TAGS...) ou une CONSTANTE unitaire prefixee (STATUT_ACTIVE,
    URGENCE_VEILLE, TAG_SESSION_OUVERTE) declare ses valeurs (membres d'un
    conteneur, CLES d'un dictionnaire). Le fichier qui la porte est un DOMICILE,
    et il est DECOUVERT, jamais liste ici.
  - OBSERVATIONS : les valeurs reellement ECRITES dans les donnees (BDD, JSON).

Puis il SIGNALE, sans jamais reparer :
  - ORPHELINES : une valeur ecrite dans les donnees et declaree NULLE PART
    (une fiche invisible se lit comme une fiche inexistante : L-100) ;
  - DOMICILES MULTIPLES : la meme valeur portee par deux maisons sans lien
    (deux declarations du meme etat peuvent diverger en silence : friction 52) ;
  - COPIES : un litteral egal a une valeur declaree AILLEURS, retenu seulement en
    CONTEXTE D'ETAT (comparaison, collection/table, affectation a un nom d'etat,
    argument nomme d'etat). Un CHAMP ou une OPTION qui porte le meme mot n'est
    PAS une copie : l'outil ne compte pas les homonymes, il compte les copies.

LIMITE ASSUMEE : deux vocabulaires DISTINCTS qui partagent un mot (urgence
"haute" et niveau d'alerte "haute") sont comptes ensemble. L'outil SIGNALE, le
pilote TRANCHE : c'est une mesure a lire, pas un verdict.

code 0 = aucun signal, 1 = signaux a traiter.
Lecture seule.
Usage:
    python verifier-vocabulaire-etat.py [--racine <chemin>] [--court]
"""

import ast
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
# L'outil vit dans la zone : remonter jusqu a matrix/ puis descendre dans matrice/.
RACINE_MATRIX = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")

# --- Donnees ou l'etat s'ECRIT (observation de terrain) --------------------
BDD = {
    "matrice/data/frictions.db": "frictions",
    "matrice/data/modifications.db": "modifications",
}
CHAMPS_OBS = ("type", "gravite", "frequence", "statut")
JSONS = (
    ("_operateur/optimus-prime/pilote/file-missions-optimus.json", "missions", "statut"),
    ("_operateur/optimus-prime/pilote/entonnoir-files-optimus.json", "vrac", "urgence"),
)

# Deux formes declarantes, et elles seulement :
#   - le CONTENEUR, nom exactement au pluriel : il porte tout un vocabulaire ;
#   - la CONSTANTE unitaire, prefixee.
# Un conteneur SUFFIXE (TYPES_DOSSIER, TAGS_SAC_A_DOS) designe une AUTRE chose :
# il declare du vocabulaire, mais pas celui-la, et l'accepter fabriquerait des
# "domiciles multiples" qui n'existent pas.
MOTIF_CONTENEUR = r"^(STATUTS|ETATS|URGENCES|GRAVITES|FREQUENCES|DEMANDES|TYPES|TAGS)$"
MOTIF_UNITAIRE = r"^(STATUT|ETAT|URGENCE|GRAVITE|FREQUENCE|DEMANDE|TAG)_[A-Z_]+$"
MOTIF_NOM_ETAT = r"^(statut|etat|statuts|urgence|gravite|frequence|demande|archivage)[a-z_]*$"

EXCLUS = ("__pycache__", "tmp-optimus", "tmp-cameleon", "tmp-test", ".git", "purification")


def nom_dit_etat(nom):
    return bool(re.match(MOTIF_CONTENEUR, nom) or re.match(MOTIF_UNITAIRE, nom))


def nom_est_etat(nom):
    return bool(re.match(MOTIF_NOM_ETAT, nom))


def acceptable(valeur):
    """Valeur candidate : courte, un seul mot, ni chemin ni extension."""
    if not isinstance(valeur, str) or not valeur or len(valeur) > 24:
        return False
    return not any(c in valeur for c in " \n/\\.:,")


def valeurs_portees(litteral):
    """Les valeurs d'une constante : membres d'un conteneur, CLES d'un dict."""
    if isinstance(litteral, dict):
        return list(litteral.keys())
    if isinstance(litteral, (tuple, list, set)):
        return list(litteral)
    return [litteral]


def option(nom, defaut):
    """Valeur d'une option de la ligne de commande (jamais devinee)."""
    arguments = sys.argv[1:]
    if nom in arguments:
        index = arguments.index(nom)
        if index + 1 < len(arguments):
            return arguments[index + 1]
    return defaut


def fichiers_code(racine):
    """Les fichiers de code SOUS la racine controlee.

    L'exclusion est RELATIVE a la racine (lecon du garde de chemins) : une racine
    volontairement placee dans une zone exclue doit pouvoir etre controlee.
    """
    for chemin in sorted(racine.rglob("*.py")):
        if any(x in chemin.relative_to(racine).parts for x in EXCLUS):
            continue
        yield chemin


def relatif(racine, chemin):
    return str(chemin.relative_to(racine)).replace("\\", "/")


def declarations(racine):
    """{valeur: {constante: domicile}} -- les DOMICILES sont DECOUVERTS."""
    trouve = defaultdict(dict)
    for chemin in fichiers_code(racine):
        try:
            arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        fichier = relatif(racine, chemin)
        for noeud in arbre.body:
            if not isinstance(noeud, ast.Assign):
                continue
            noms = [t.id for t in noeud.targets if isinstance(t, ast.Name)]
            if not noms or not nom_dit_etat(noms[0]):
                continue
            try:
                litteral = ast.literal_eval(noeud.value)
            except (ValueError, SyntaxError):
                continue
            for valeur in valeurs_portees(litteral):
                if acceptable(valeur):
                    trouve[valeur].setdefault(noms[0], fichier)
    return trouve


def observations(racine):
    """{valeur: [origine]} -- ce que les donnees portent reellement."""
    trouve = defaultdict(list)
    for rel, table in BDD.items():
        chemin = racine / rel
        if not chemin.is_file():
            continue
        conn = sqlite3.connect(str(chemin))
        try:
            colonnes = [d[1] for d in conn.execute("PRAGMA table_info(" + table + ")")]
            for colonne in colonnes:
                if colonne not in CHAMPS_OBS:
                    continue
                requete = "SELECT DISTINCT " + colonne + " FROM " + table + " LIMIT 20"
                for (valeur,) in conn.execute(requete):
                    if acceptable(valeur):
                        trouve[valeur].append(table + "." + colonne)
        finally:
            conn.close()
    for rel, cle, champ in JSONS:
        chemin = racine / rel
        if not chemin.is_file():
            continue
        try:
            bloc = json.loads(chemin.read_text(encoding="utf-8")).get(cle) or []
        except (OSError, ValueError):
            continue
        for item in (bloc.values() if isinstance(bloc, dict) else bloc):
            if isinstance(item, dict) and acceptable(item.get(champ)):
                trouve[item[champ]].append(cle + "[]." + champ)
    return trouve


def _parents(arbre):
    parents = {}
    for noeud in ast.walk(arbre):
        for enfant in ast.iter_child_nodes(noeud):
            parents[enfant] = noeud
    return parents


def _valeurs(noeuds, vocabulaire):
    return {n.value for n in noeuds
            if isinstance(n, ast.Constant) and n.value in vocabulaire}


def contexte(noeud, parents, vocabulaire):
    """Pourquoi ce litteral EST une copie (None : ce n'en est pas une)."""
    parent = parents.get(noeud)
    if isinstance(parent, ast.Compare):
        return "comparaison"
    if isinstance(parent, (ast.Set, ast.Tuple, ast.List)):
        if len(_valeurs(parent.elts, vocabulaire)) >= 2:
            return "collection"
    if isinstance(parent, ast.Dict):
        if len(_valeurs([k for k in parent.keys if k], vocabulaire)) >= 2:
            return "table"
    if isinstance(parent, ast.Assign):
        for cible in parent.targets:
            noms = [t.id for t in ast.walk(cible) if isinstance(t, ast.Name)]
            if any(nom_est_etat(n) for n in noms):
                return "affectation"
    if isinstance(parent, ast.Call):
        for mot in parent.keywords:
            if mot.arg and nom_est_etat(mot.arg) and mot.value is noeud:
                return "argument"
    return None


def chercher_copies(racine, trouve):
    """{fichier: [(ligne, valeur, motif)]} -- sauf ce que le fichier declare."""
    par_fichier = defaultdict(list)
    for chemin in fichiers_code(racine):
        fichier = relatif(racine, chemin)
        try:
            arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        a_lui = {v for v, d in trouve.items() if fichier in d.values()}
        parents = _parents(arbre)
        for noeud in ast.walk(arbre):
            if not (isinstance(noeud, ast.Constant) and noeud.value in trouve):
                continue
            if noeud.value in a_lui:
                continue
            motif = contexte(noeud, parents, trouve)
            if motif:
                par_fichier[fichier].append((noeud.lineno, noeud.value, motif))
    return par_fichier


def main():
    arguments = sys.argv[1:]
    court = "--court" in arguments
    racine = Path(option("--racine", str(RACINE_MATRIX))).resolve()
    if not racine.is_dir():
        print("Racine introuvable : " + str(racine))
        return 2
    print("VOCABULAIRE D'ETAT -- consommateurs qui recopient (lecture seule)")
    print("Racine : " + str(racine))

    trouve = declarations(racine)
    observe = observations(racine)

    maisons_par_valeur = {v: sorted(set(d.values())) for v, d in trouve.items()}
    declarants = sorted({f for maisons in maisons_par_valeur.values() for f in maisons})

    print("\n[1] DECLARATIONS : " + str(len(trouve)) + " valeurs, "
          + str(len(declarants)) + " DOMICILE(S) decouvert(s)")
    for domicile in declarants:
        constantes = sorted({c for v, d in trouve.items() for c, f in d.items() if f == domicile})
        print("    " + domicile)
        if not court:
            print("        " + ", ".join(constantes))

    orphelines = {v: o for v, o in observe.items() if v not in trouve}
    print("\n[2] ORPHELINES (ecrites dans les donnees, declarees nulle part) : "
          + str(len(orphelines)))
    for valeur, origines in sorted(orphelines.items()):
        print("    ! " + valeur.ljust(20) + " <- " + " | ".join(sorted(set(origines))))

    multiples = {v: f for v, f in maisons_par_valeur.items() if len(f) > 1}
    print("\n[3] DOMICILES MULTIPLES (une valeur, deux maisons sans lien) : " + str(len(multiples)))
    for valeur, maisons in sorted(multiples.items()):
        print("    ! " + valeur.ljust(20) + " <- " + " | ".join(maisons))

    par_fichier = chercher_copies(racine, trouve)
    total = sum(len(set(h)) for h in par_fichier.values())
    print("\n[4] COPIES EN DUR (contexte d'etat seulement) : " + str(total)
          + " dans " + str(len(par_fichier)) + " fichier(s)")
    for fichier in sorted(par_fichier):
        hits = sorted(set(par_fichier[fichier]))
        print("    " + fichier + "  (" + str(len(hits)) + ")")
        for ligne, valeur, motif in hits:
            if not court:
                print("        L" + str(ligne).ljust(5) + valeur.ljust(20) + " [" + motif + "]")

    signaux = total + len(orphelines) + len(multiples)
    print("\nSIGNAL : " + str(signaux) + " a traiter (" + str(total) + " copies, "
          + str(len(orphelines)) + " orpheline(s), " + str(len(multiples))
          + " domicile(s) multiple(s)).")
    return 1 if signaux else 0


if __name__ == "__main__":
    sys.exit(main())
