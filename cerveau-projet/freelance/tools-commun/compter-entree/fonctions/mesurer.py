# -*- coding: ascii -*-
# mesurer.py -- mesure la taille des fichiers lus par l'LLM = tokens entree
# D15 : separe du code, extensible via patterns.json
import json
import os
from pathlib import Path


def charger_patterns(chemin_data):
    """Charge les patterns de fichiers a mesurer depuis patterns.json."""
    if not os.path.isfile(chemin_data):
        return {"fichiers": [], "glob": []}
    with open(chemin_data, encoding="utf-8") as f:
        return json.load(f)


def taille_octets(chemin):
    """Taille en octets d'un fichier, 0 si introuvable."""
    try:
        return os.path.getsize(chemin)
    except OSError:
        return 0


def mesurer_fichiers(racine, patterns):
    """Mesure tous les fichiers matchant les patterns.
    Retourne liste de {chemin, taille_octets, categorie}."""
    resultats = []
    for entree in patterns.get("fichiers", []):
        chemin = Path(racine) / entree["chemin"]
        cat = entree.get("categorie", "autre")
        label = entree.get("label", chemin.name)
        taille = taille_octets(str(chemin))
        resultats.append({
            "chemin": str(chemin.relative_to(racine)),
            "label": label,
            "categorie": cat,
            "taille_octets": taille,
        })
    for glob_entry in patterns.get("glob", []):
        motif = Path(racine) / glob_entry["pattern"]
        cat = glob_entry.get("categorie", "autre")
        label = glob_entry.get("label", "")
        for chemin in sorted(Path(racine).glob(str(motif.relative_to(racine)))):
            if chemin.is_file():
                taille = taille_octets(str(chemin))
                resultats.append({
                    "chemin": str(chemin.relative_to(racine)),
                    "label": label or chemin.name,
                    "categorie": cat,
                    "taille_octets": taille,
                })
    return resultats


def calculer_tokens(resultats, chars_par_token=4.0):
    """Convertit les tailles en tokens estimes."""
    total_octets = sum(r["taille_octets"] for r in resultats)
    total_tokens = int(total_octets / chars_par_token)
    # Regrouper par categorie
    par_categorie = {}
    for r in resultats:
        cat = r["categorie"]
        if cat not in par_categorie:
            par_categorie[cat] = {"octets": 0, "tokens": 0, "fichiers": 0}
        par_categorie[cat]["octets"] += r["taille_octets"]
        par_categorie[cat]["tokens"] += int(r["taille_octets"] / chars_par_token)
        par_categorie[cat]["fichiers"] += 1
    return {
        "total_octets": total_octets,
        "total_tokens": total_tokens,
        "par_categorie": par_categorie,
        "nb_fichiers": len(resultats),
        "chars_par_token": chars_par_token,
    }


def comparer_snapshots(precedent, courant):
    """Compare deux snapshots, retourne les deltas."""
    if not precedent:
        return {"nouveau": True, "delta_tokens": courant["total_tokens"]}
    delta = courant["total_tokens"] - precedent.get("total_tokens", 0)
    evolution = []
    prec_cat = precedent.get("par_categorie", {})
    for cat, info in courant.get("par_categorie", {}).items():
        ancien = prec_cat.get(cat, {}).get("tokens", 0)
        diff = info["tokens"] - ancien
        if diff != 0:
            evolution.append({"categorie": cat, "delta_tokens": diff})
    return {
        "nouveau": False,
        "delta_tokens": delta,
        "evolution": evolution,
        "precedent_tokens": precedent.get("total_tokens", 0),
        "courant_tokens": courant["total_tokens"],
    }
