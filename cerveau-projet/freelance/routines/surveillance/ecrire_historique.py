# -*- coding: ascii -*-
# ecrire_historique.py -- met a jour tokens-historique.md
# D15 : fonctions partagees par les routines compter-entree et compter-sortie
import json
import os
from datetime import datetime
from pathlib import Path


def trouver_fichier_historique(racine):
    """Chemin vers tokens-historique.md."""
    return Path(racine) / "cerveau-projet" / "freelance" / "historique" / "tokens-historique.md"


def lire_etat_actuel(chemin):
    """Lit l'etat actuel depuis le fichier, retourne dict."""
    etat = {"entree": 0, "sortie": 0, "total": 0, "derniere_mise_a_jour": "-"}
    if not chemin.exists():
        return etat
    try:
        contenu = chemin.read_text(encoding="utf-8")
        for ligne in contenu.split("\n"):
            if "| Tokens ENTREE |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    try:
                        etat["entree"] = int(parts[1])
                    except ValueError:
                        pass
            elif "| Tokens SORTIE |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    try:
                        etat["sortie"] = int(parts[1])
                    except ValueError:
                        pass
            elif "| Tokens TOTAL |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    try:
                        etat["total"] = int(parts[1])
                    except ValueError:
                        pass
            elif "| Derniere mise a jour |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    etat["derniere_mise_a_jour"] = parts[1]
    except (OSError, UnicodeDecodeError):
        pass
    return etat


def mettre_a_jour_etat(chemin, tokens_entree, tokens_sortie):
    """Met a jour la section 'Etat actuel' du fichier."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = tokens_entree + tokens_sortie
    contenu = ""
    if chemin.exists():
        try:
            contenu = chemin.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass

    lignes = contenu.split("\n")
    nouvelles_lignes = []
    for ligne in lignes:
        if "| Tokens ENTREE |" in ligne:
            nouvelles_lignes.append("| Tokens ENTREE | %d |" % tokens_entree)
        elif "| Tokens SORTIE |" in ligne:
            nouvelles_lignes.append("| Tokens SORTIE | %d |" % tokens_sortie)
        elif "| Tokens TOTAL |" in ligne:
            nouvelles_lignes.append("| Tokens TOTAL | %d |" % total)
        elif "| Derniere mise a jour |" in ligne:
            nouvelles_lignes.append("| Derniere mise a jour | %s |" % now)
        else:
            nouvelles_lignes.append(ligne)

    chemin.write_text("\n".join(nouvelles_lignes), encoding="utf-8")


def ajouter_ligne_historique(chemin, tokens_entree, tokens_sortie, delta_entree,
                              delta_sortie, notes=""):
    """Ajoute une ligne au tableau historique."""
    now = datetime.now().strftime("%H:%M")
    total = tokens_entree + tokens_sortie
    ligne = "| %s | %d | %d | %d | %+d | %+d | %s |" % (
        now, tokens_entree, tokens_sortie, total,
        delta_entree, delta_sortie, notes)

    contenu = ""
    if chemin.exists():
        try:
            contenu = chemin.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass

    # Trouver la fin du tableau (derniere ligne qui commence par "| " et n'est pas un separateur)
    lignes = contenu.split("\n")
    idx_insertion = len(lignes)
    for i in range(len(lignes) - 1, -1, -1):
        ligne_courante = lignes[i].strip()
        if ligne_courante.startswith("| ") and "---" not in ligne_courante:
            idx_insertion = i + 1
            break
        elif ligne_courante == "":
            continue
        else:
            break

    lignes.insert(idx_insertion, ligne)
    chemin.write_text("\n".join(lignes), encoding="utf-8")
