"""Entree du verbe rechercher : moteur de recherche unifie (fichiers + BDD).

Contrat de la porte (MO-069) :
- une option de FILTRE filtre vraiment (--tag, --mot-cle, --source, --periode) ;
- une option illisible est REFUSEE (code 2), jamais ignoree en silence ;
- une coupe (troncature) et un ecart (entree sans date) sont DITS dans les deux
  sorties (humaine et --json) : un resultat muet sur ses propres limites ment ;
- la sortie --json est en ASCII pur (ensure_ascii) : une console cp1252 ne peut
  plus faire echouer la porte.
"""
import sys
import os

# Ajoute le repertoire courant au path pour les imports locaux
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commun import (
    scanner_fichiers,
    scanner_bdd,
    filtrer_par_periode,
    formatter_hit,
    extraire_options,
    periode_valide,
)
from constants import (
    BDD_SOURCES,
    DANS_VALEURS,
    DEFAUT_DANS,
    LIMITE_DEFAUT,
    LIMITE_LIGNES_JSONL,
    NOMS_OPTIONS_RECHERCHER,
)

# Options qui ne s'appliquent qu'aux BDD : les accepter sur --dans fichiers
# serait une option qui ne filtre rien (lecon EO-107).
OPTIONS_BDD = ("tag", "mot_cle", "source")


def rechercher(arguments):
    """Verbe rechercher : --requete [--dans] [--tag] [--mot-cle] [--source] [--periode] [--json] [--limite]

    Codes retour :
      0 = succes (au moins 1 hit)
      1 = aucun resultat (la recherche a abouti)
      2 = refus (option manquante, illisible ou hors perimetre d'application)
    """
    options = extraire_options(arguments, NOMS_OPTIONS_RECHERCHER)

    # Validation
    requete = options.get("requete", "").strip()
    if not requete:
        print("ERREUR : --requete requis. Ex: --requete \"defcon\"")
        print("Usage: rechercher --requete <texte> [--dans fichiers|bdd|tous]")
        print("       [--tag <tag>] [--mot-cle <texte>] [--source <nom>]")
        print("       [--periode 7j] [--json] [--limite N]")
        return 2

    dans = options.get("dans", DEFAUT_DANS)
    if dans not in DANS_VALEURS:
        print("ERREUR : --dans doit etre parmi " + ", ".join(DANS_VALEURS))
        return 2

    tag = options.get("tag", "").strip() or None
    mot_cle = options.get("mot_cle", "").strip() or None
    source_nom = options.get("source", "").strip() or None
    periode = options.get("periode", "").strip() or None
    mode_json = "json" in options

    # --source inconnue : REFUS qui nomme les sources valides (EO-109).
    # Une faute de frappe doit etre une erreur, pas un "0 resultat" muet.
    if source_nom and source_nom not in BDD_SOURCES:
        print("ERREUR : --source inconnue : " + source_nom)
        print("Sources valides : " + ", ".join(BDD_SOURCES))
        return 2

    # Un filtre BDD sur un scan de fichiers ne filtre rien : on le dit.
    if dans == "fichiers":
        for nom in OPTIONS_BDD:
            if options.get(nom, "").strip():
                print("ERREUR : --" + nom.replace("_", "-")
                      + " ne s'applique qu'aux BDD (--dans bdd ou tous).")
                return 2

    # --periode illisible : REFUS (un filtre temporel qui ne filtre pas est un
    # affichage -- EO-110).
    if periode and not periode_valide(periode):
        print("ERREUR : --periode attend <nombre><j|m|a> (ex: 7j, 30j, 3m, 1a).")
        return 2

    # --limite doit etre un entier positif (avant : int() levait une exception).
    limite_brute = options.get("limite", str(LIMITE_DEFAUT)).strip()
    if not limite_brute.isdigit() or int(limite_brute) <= 0:
        print("ERREUR : --limite attend un entier positif.")
        return 2
    limite = int(limite_brute)

    tous_hits = []
    sources_tronquees = []
    ecartes_sans_date = 0
    erreur_scan = ""

    # Scan fichiers
    if dans in ("fichiers", "tous"):
        hits_fichiers, nb_f, limit_f, msg_f = scanner_fichiers(requete)
        if msg_f:
            erreur_scan = msg_f
        if periode:
            hits_fichiers, ecartes_f = filtrer_par_periode(hits_fichiers, periode)
            ecartes_sans_date += ecartes_f
        tous_hits.extend(hits_fichiers)

    # Scan BDD
    if dans in ("bdd", "tous"):
        hits_bdd, nb_b, limit_b, tronquees = scanner_bdd(
            requete, tag=tag, mot_cle=mot_cle, source_nom=source_nom
        )
        sources_tronquees.extend(tronquees)
        if periode:
            hits_bdd, ecartes_b = filtrer_par_periode(hits_bdd, periode)
            ecartes_sans_date += ecartes_b
        tous_hits.extend(hits_bdd)

    if erreur_scan:
        print("ERREUR : " + erreur_scan)
        return 2

    # Tri par score (BDD) puis fichier (par defaut)
    tous_hits.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Limite
    nb_total = len(tous_hits)
    if nb_total > limite:
        tous_hits = tous_hits[:limite]
        nb_limite = True
    else:
        nb_limite = False

    # Sortie
    if mode_json:
        import json
        resultat = {
            "requete": requete,
            "dans": dans,
            "trouve": nb_total,
            "retourne": len(tous_hits),
            "limite_atteinte": nb_limite,
            "tronque": sources_tronquees,
            "ecartes_sans_date": ecartes_sans_date,
            "filtres": {"tag": tag, "mot_cle": mot_cle, "source": source_nom,
                        "periode": periode},
            "hits": tous_hits,
        }
        # ensure_ascii : la sortie machine reste de l'ASCII pur, encodable par
        # n'importe quelle console (EO-105).
        print(json.dumps(resultat, ensure_ascii=True, indent=2))
    else:
        print(f"Recherche : \"{requete}\" (dans {dans})")
        if tag or mot_cle or source_nom or periode:
            filtres_actifs = []
            if tag:
                filtres_actifs.append("tag=" + tag)
            if mot_cle:
                filtres_actifs.append("mot-cle=" + mot_cle)
            if source_nom:
                filtres_actifs.append("source=" + source_nom)
            if periode:
                filtres_actifs.append("periode=" + periode)
            print("Filtres : " + ", ".join(filtres_actifs))
        print(f"Trouves : {nb_total} | Retournes : {len(tous_hits)}")
        if nb_limite:
            print(f"Limite atteinte ({limite})")
        if sources_tronquees:
            print("TRONQUE : source(s) coupee(s) a " + str(LIMITE_LIGNES_JSONL)
                  + " lignes : " + ", ".join(sources_tronquees))
        if ecartes_sans_date:
            print("ECARTES faute de date (periode " + str(periode) + ") : "
                  + str(ecartes_sans_date))
        print("")
        for i, h in enumerate(tous_hits):
            print(formatter_hit(h, i))
        if not tous_hits:
            print("  (aucun resultat)")

    return 0 if tous_hits else 1
