# -*- coding: ascii -*-
"""fonctions/cherche.py - module du combo CHERCHE."""
import os
from datetime import datetime
from lib_lecture import lire_texte, lire_jsonl, dernieres_lignes
from lib_lecture import chemin_reel as chemin_reelle
from commun import RACINE


def combo_cherche(besoin):
    """v0.2.0 : temps 2 REEL - recherche locale fichiers/dossiers/contenu."""
    parties = besoin.strip().split()
    if not parties:
        return {"combo": "CHERCHE", "statut": "ERREUR",
                "reponse": "motif manquant : CHERCHE <motif> [--dossier X]",
                "date": datetime.now().isoformat(timespec="seconds")}
    motif = parties[0].lower()
    dossier = "."
    for j, p in enumerate(parties):
        if p == "--dossier" and j + 1 < len(parties):
            dossier = parties[j + 1]
    base = os.path.join(RACINE, dossier) if chemin_reelle(dossier) else RACINE
    exclus = {".git", "__pycache__", "node_modules", "inbox", "outbox"}
    par_nom, par_contenu = [], []
    for racine_courante, dossiers, fichiers in os.walk(base):
        dossiers[:] = [d for d in dossiers if d not in exclus]
        for f in fichiers:
            reel = os.path.join(racine_courante, f)
            relatif = os.path.relpath(reel, RACINE).replace("\\", "/")
            if motif in f.lower() and len(par_nom) < 30:
                par_nom.append(relatif)
            try:
                if os.path.getsize(reel) > 1_000_000:
                    continue
                with open(reel, "r", encoding="utf-8", errors="ignore") as fh:
                    for n, ligne in enumerate(fh, 1):
                        if motif in ligne.lower():
                            par_contenu.append(
                                "%s:%d: %s" % (relatif, n, ligne.strip()[:140]))
                            if len(par_contenu) >= 40:
                                raise StopIteration
            except StopIteration:
                pass
            except OSError:
                continue
    return {
        "combo": "CHERCHE", "besoin": besoin, "statut": "OK",
        "motif": motif, "dossier": dossier,
        "fichiers_correspondants": par_nom,
        "occurrences_contenu": par_contenu,
        "total": len(par_nom) + len(par_contenu),
        "note_web": ("si le sujet sort du projet, JARVIS complete par une "
                     "recherche web avant de repondre"),
        "date": datetime.now().isoformat(timespec="seconds"),
    }
