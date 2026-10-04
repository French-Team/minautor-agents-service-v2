# -*- coding: ascii -*-
"""fonctions/resume.py - module du combo RESUME."""
import re
from datetime import datetime
from lib_lecture import lire_texte, lire_jsonl, dernieres_lignes


def combo_resume(besoin):
    """v0.2.0 : temps 2 REEL - resume d'un fichier du workspace."""
    cible = besoin.strip().strip("'\"")
    contenu = lire_texte(cible)
    if contenu is None:
        return {
            "combo": "RESUME", "besoin": besoin, "statut": "INTROUVABLE",
            "reponse": ("fichier '%s' introuvable (chemin relatif a la "
                        "racine). Pour chercher un sujet : JARVIS CHERCHE."
                        % cible),
            "date": datetime.now().isoformat(timespec="seconds"),
        }
    lignes = contenu.splitlines()
    sections = []
    titre_courant = None
    for i, ligne in enumerate(lignes):
        m = re.match(r"^(#{1,3})\s+(.+)$", ligne.strip())
        if m:
            titre_courant = {"titre": m.group(2).strip(),
                             "niveau": len(m.group(1)), "ligne": i + 1}
            sections.append(titre_courant)
    # apercu : premier paragraphe non vide apres l'entete
    apercu = ""
    for ligne in lignes:
        l = ligne.strip()
        if l and not l.startswith("#") and not l.startswith("|") \
                and not l.startswith("---") and not l.startswith(">"):
            apercu = l[:200]
            break
    return {
        "combo": "RESUME", "besoin": besoin, "statut": "OK",
        "cible": cible,
        "lignes": len(lignes),
        "nb_sections": len(sections),
        "apercu": apercu,
        "sections": [{"titre": s["titre"], "niveau": s["niveau"],
                      "ligne": s["ligne"]} for s in sections[:40]],
        "date": datetime.now().isoformat(timespec="seconds"),
    }
