# -*- coding: ascii -*-
# mesurer.py -- mesure les tokens SORTIE (resultats d'outils executes)
# D15 : separe du code, extensible via sources.json
import json
import os
from pathlib import Path


def charger_sources(chemin_data):
    """Charge les sources de donnees a mesurer depuis sources.json."""
    if not os.path.isfile(chemin_data):
        return {"sources": []}
    with open(chemin_data, encoding="utf-8") as f:
        return json.load(f)


def taille_octets(chemin):
    """Taille en octets d'un fichier, 0 si introuvable."""
    try:
        return os.path.getsize(chemin)
    except OSError:
        return 0


def compter_lignes_jsonl(chemin):
    """Compte les lignes valides dans un fichier JSONL."""
    if not os.path.isfile(chemin):
        return 0
    count = 0
    try:
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    try:
                        json.loads(ligne)
                        count += 1
                    except ValueError:
                        pass
    except OSError:
        pass
    return count


def mesurer_source(racine, source):
    """Mesure une source de sortie (fichier ou repertoire)."""
    chemin = Path(racine) / source["chemin"]
    type_src = source.get("type", "fichier")
    cat = source.get("categorie", "autre")
    label = source.get("label", chemin.name)

    if type_src == "jsonl":
        taille = taille_octets(str(chemin))
        lignes = compter_lignes_jsonl(str(chemin))
        return {
            "chemin": str(chemin.relative_to(racine)),
            "label": label,
            "categorie": cat,
            "type": "jsonl",
            "taille_octets": taille,
            "nb_entrees": lignes,
        }
    elif type_src == "repertoire":
        total_octets = 0
        nb_fichiers = 0
        if chemin.is_dir():
            for f in chemin.rglob("*"):
                if f.is_file():
                    total_octets += taille_octets(str(f))
                    nb_fichiers += 1
        return {
            "chemin": str(chemin.relative_to(racine)),
            "label": label,
            "categorie": cat,
            "type": "repertoire",
            "taille_octets": total_octets,
            "nb_fichiers": nb_fichiers,
        }
    else:
        taille = taille_octets(str(chemin))
        return {
            "chemin": str(chemin.relative_to(racine)),
            "label": label,
            "categorie": cat,
            "type": "fichier",
            "taille_octets": taille,
        }


def mesurer_toutes_sources(racine, sources_config):
    """Mesure toutes les sources definies dans sources.json."""
    return [mesurer_source(racine, s) for s in sources_config.get("sources", [])]


def calculer_tokens_sortie(resultats, chars_par_token=4.0):
    """Convertit les tailles de sortie en tokens estimes."""
    total_octets = sum(r["taille_octets"] for r in resultats)
    total_tokens = int(total_octets / chars_par_token)
    par_categorie = {}
    for r in resultats:
        cat = r["categorie"]
        if cat not in par_categorie:
            par_categorie[cat] = {"octets": 0, "tokens": 0, "sources": 0}
        par_categorie[cat]["octets"] += r["taille_octets"]
        par_categorie[cat]["tokens"] += int(r["taille_octets"] / chars_par_token)
        par_categorie[cat]["sources"] += 1
    return {
        "total_octets": total_octets,
        "total_tokens": total_tokens,
        "par_categorie": par_categorie,
        "nb_sources": len(resultats),
        "chars_par_token": chars_par_token,
    }


def comparer_snapshots_sortie(precedent, courant):
    """Compare deux snapshots de sortie, retourne les deltas."""
    if not precedent:
        return {"nouveau": True, "delta_tokens": courant["total_tokens"]}
    delta = courant["total_tokens"] - precedent.get("total_tokens", 0)
    return {
        "nouveau": False,
        "delta_tokens": delta,
        "precedent_tokens": precedent.get("total_tokens", 0),
        "courant_tokens": courant["total_tokens"],
    }
