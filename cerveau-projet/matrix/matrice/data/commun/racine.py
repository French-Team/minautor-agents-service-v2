"""Motif unique de detection de la racine du workspace.

L-013 : AUCUN outil ne compte ses ../ a la main -- la racine est DETECTEE
en remontant jusqu'au dossier contenant AGENTS.md (pattern v1, decision M-008).
CE module est l'UNIQUE definition du motif : les constants.py l'importent,
ils ne le recopient jamais (M-076 : duplications supprimees).
"""
from pathlib import Path

BORNES_REMONTEE = 30


def detecter_racine(depart):
    """Remonte depuis <depart> jusqu'au dossier contenant AGENTS.md."""
    courant = Path(depart).resolve()
    for _ in range(BORNES_REMONTEE):
        if (courant / "AGENTS.md").is_file():
            return courant
        if courant.parent == courant:
            break
        courant = courant.parent
    raise RuntimeError("Racine du workspace introuvable (AGENTS.md absent en remontant).")
