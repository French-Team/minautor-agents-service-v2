# -*- coding: ascii -*-
"""fonctions/defcon.py - Echelle DEFCON pour Oracle (v1).

5 = ARRET TOTAL | 4 = VALIDATION DES REPARATIONS
| 3 = REPRISE SURVEILLEE | 2 = REPRISE TOTALE.
Transitions legales : 5->4->3->2 uniquement (comme JARVIS v2).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

FILES_DIR = Path(__file__).parent.parent / "files"
DEFCON_FILE = FILES_DIR / "defcon.jsonl"

ECHELLE = {
    5: "ARRET TOTAL",
    4: "VALIDATION DES REPARATIONS",
    3: "REPRISE SURVEILLEE",
    2: "REPRISE TOTALE",
}


def niveau_courant():
    """Dernier niveau DEFCON journalise (None si aucun)."""
    if not DEFCON_FILE.exists():
        return None
    dernier = None
    for l in DEFCON_FILE.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            e = json.loads(l)
        except ValueError:
            continue
        if e.get("niveau"):
            dernier = e["niveau"]
    return dernier


def changer(nouveau, commentaire, par="oracle"):
    """Changer de niveau avec controle de transition legale.
    Retourne (entree, erreur)."""
    if nouveau not in ECHELLE:
        return None, f"niveau invalide '{nouveau}'"
    courant = niveau_courant()
    transitions = {5: 4, 4: 3, 3: 2}
    if courant is None:
        return None, "aucun DEFCON 5 declare : rien a faire"
    attendu = transitions.get(courant)
    if nouveau != attendu:
        return None, (f"transition illegale {courant}->{nouveau}. "
                      f"Seule transition legale depuis DEFCON {courant} : "
                      f"DEFCON {attendu}")
    entree = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "niveau": nouveau,
        "signification": ECHELLE[nouveau],
        "commentaire": commentaire,
        "par": par,
    }
    with open(DEFCON_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree, None


def declarer_arret(raison, par="oracle"):
    """Declarer un DEFCON 5 (arret total) - point d'entree unique."""
    entree = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "niveau": 5,
        "signification": ECHELLE[5],
        "commentaire": raison,
        "par": par,
    }
    with open(DEFCON_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree


def journal(limite=10):
    """Journal recent des changements DEFCON."""
    if not DEFCON_FILE.exists():
        return []
    lignes = [l for l in DEFCON_FILE.read_text(encoding="utf-8").splitlines()
              if l.strip()]
    resultats = []
    for l in lignes[-limite:]:
        try:
            resultats.append(json.loads(l))
        except ValueError:
            continue
    return resultats


def cmd_defcon(args=None):
    """Afficher l'etat DEFCON courant + le journal recent."""
    courant = niveau_courant()
    if courant is None:
        print("[DEFCON] Aucun etat DEFCON (fonctionnement normal).")
        return
    print(f"[DEFCON] Niveau {courant} : {ECHELLE[courant]}")
    print("  Journal recent :")
    for e in journal(5):
        print(f"    {e.get('date')} - niveau {e.get('niveau')} - "
              f"{str(e.get('commentaire', ''))[:60]}")


def cmd_changer_defcon(args):
    """Descendre d'un niveau (5->4->3->2, transitions legales)."""
    entree, erreur = changer(args.niveau, args.commentaire)
    if erreur:
        print(f"[DEFCON] ERREUR: {erreur}")
        return
    print(f"[DEFCON] Niveau {entree['niveau']} : {entree['signification']}")
    print(f"  {entree['commentaire']}")


def cmd_declarer(args):
    """Declarer un DEFCON 5 (arret total)."""
    entree = declarer_arret(args.raison, par=getattr(args, "par", "oracle"))
    print(f"[DEFCON] Niveau {entree['niveau']} : {entree['signification']}")
    print(f"  {entree['commentaire']}")
