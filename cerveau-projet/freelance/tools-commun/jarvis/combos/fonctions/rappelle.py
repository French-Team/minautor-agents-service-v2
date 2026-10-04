# -*- coding: ascii -*-
"""fonctions/rappelle.py - module du combo RAPPELLE."""
import re
from datetime import datetime
from lib_lecture import lire_texte, lire_jsonl, dernieres_lignes


def combo_rappelle(besoin):
    """v0.3.0 : temps 2 REEL partiel - decisions D1-D18 de proposition-v2.md.
    Sous-partie BDD-lecons : PLACEHOLDER (attend la livraison Forge)."""
    sujet = besoin.strip().strip("'\"")
    contenu = lire_texte("cerveau-projet/freelance/proposition-v2.md")
    if contenu is None:
        return {"combo": "RAPPELLE", "statut": "ERREUR",
                "reponse": "proposition-v2.md introuvable",
                "date": datetime.now().isoformat(timespec="seconds")}
    # extraire les lignes-tableaux des decisions (| Dn | **titre** | ...)
    decisions = []
    for n, ligne in enumerate(contenu.splitlines(), 1):
        m = re.match(r"\|\s*(D\d+)\s*\|\s*\*\*(.+?)\*\*\s*\|", ligne.strip())
        if m:
            decisions.append({"id": m.group(1), "titre": m.group(2),
                              "ligne": n})
    motif = sujet.lower()
    if motif and motif not in ("tout", "decisions"):
        filtreees = [d for d in decisions
                     if motif in d["id"].lower() or motif in d["titre"].lower()]
        if filtreee := filtreees:
            decisions = filtreees
    return {
        "combo": "RAPPELLE", "besoin": besoin, "statut": "OK_PARTIEL",
        "source": "cerveau-projet/freelance/proposition-v2.md",
        "nb_decisions": len(decisions),
        "decisions": decisions,
        "lecons_bdd": ("PLACEHOLDER - la BDD des lecons est en attente "
                       "de la mission Forge"),
        "date": datetime.now().isoformat(timespec="seconds"),
    }
