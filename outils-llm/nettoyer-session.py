#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
outils-llm/nettoyer-session.py - NETTOYAGE EXCLUSIF D UNE SESSION.

Vide l encart et l historique de la session demandee (v1 ou v2),
purge la BDD, vide les inbox/outbox JARVIS si freelance.
Sans question : obéit comme un soldat.
"""

import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
RACINE = Path(__file__).resolve().parent.parent

AGENTS_MD = RACINE / "AGENTS.md"

# Fichiers par session
FILES = {
    "session-admin": {
        "encart": RACINE / "AGENTS-activite-recente.md",
        "corps": RACINE / "AGENTS-historique.md",
        "encoding": "ascii",
        "newline": "\n",
    },
    "session-freelance": {
        "encart": RACINE / "AGENTS-activite-recente-v2.md",
        "corps": RACINE / "AGENTS-historique-v2.md",
        "encoding": "utf-8",
        "newline": "\r\n",
    },
}

# JARVIS (freelance seulement)
JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"
INBOX_DIR = JARVIS_DIR / "inbox"
OUTBOX_DIR = JARVIS_DIR / "outbox"
BDD_FILE = JARVIS_DIR / "historique" / "historique.db"


def lire(path):
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        try:
            return path.read_text(encoding="latin-1").replace("\r\n", "\n")
        except OSError:
            return ""


def ecrire(path, contenu, encoding="utf-8", newline="\r\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    contenu = contenu.replace("\r\n", "\n").replace("\n", newline)
    with open(path, "w", encoding=encoding, newline="") as fh:
        fh.write(contenu)


def vider_encart(session):
    """Vider l encart de la session (garder header + en-tete tableau)."""
    cfg = FILES[session]
    path = cfg["encart"]
    contenu = lire(path)
    if not contenu:
        print("  [ENCART] Fichier absent ou deja vide")
        return 0

    # Trouver la section de la session
    section = "## Activites recentes -- %s" % session
    lignes = contenu.split("\n")
    idx_section = None
    for i, l in enumerate(lignes):
        if l.strip() == section:
            idx_section = i
            break

    if idx_section is None:
        print("  [ENCART] Section '%s' non trouvee" % session)
        return 0

    # Trouver la fin de la section (prochain ## ou fin de fichier)
    fin = len(lignes)
    for i in range(idx_section + 1, len(lignes)):
        if lignes[i].strip().startswith("## "):
            fin = i
            break

    # Garder : header YAML + section + en-tete tableau + separateur
    # Supprimer : toutes les lignes de donnees apres le separateur
    header_lines = lignes[:idx_section + 1]
    # Trouver l en-tete et le separateur
    entete_idx = None
    sep_idx = None
    for i in range(idx_section + 1, fin):
        if lignes[i].strip().startswith("|") and "Grade" in lignes[i]:
            entete_idx = i
        if entete_idx is not None and "---" in lignes[i]:
            sep_idx = i
            break

    if entete_idx is not None and sep_idx is not None:
        # Garder header + section + en-tete + separateur, supprimer le reste
        new_lines = lignes[:sep_idx + 1]
        # Ajouter le reste du fichier (apres la section)
        new_lines.extend(lignes[fin:])
    else:
        # Pas de tableau detecte, garder tel quel
        new_lines = lignes

    nb_supprime = fin - (sep_idx + 1 if sep_idx else idx_section + 1)
    contenu_new = "\n".join(new_lines)
    ecrire(path, contenu_new, cfg["encoding"], cfg["newline"])
    print("  [ENCART] %d entrees supprimees" % max(0, nb_supprime))
    return nb_supprime


def vider_corps(session):
    """Vider le corps historique de la session (garder headers par date)."""
    cfg = FILES[session]
    path = cfg["corps"]
    contenu = lire(path)
    if not contenu:
        print("  [CORPS] Fichier absent ou deja vide")
        return 0

    lignes = contenu.split("\n")
    # Garder uniquement les headers de section (## JJ/MM/AAAA) et le header YAML
    new_lines = []
    in_yaml = False
    for l in lignes:
        if l.strip() == "---":
            new_lines.append(l)
            in_yaml = not in_yaml
            continue
        if in_yaml:
            new_lines.append(l)
            continue
        if l.strip().startswith("## "):
            new_lines.append(l)
            continue
        # Supprimer les lignes de donnees (- ...)
        # et les lignes vides entre sections
        # On garde juste les headers

    # Supprimer les sections vides (header suivi de rien)
    final = []
    skip_empty = False
    for i, l in enumerate(new_lines):
        if l.strip().startswith("## ") and i + 1 < len(new_lines):
            # Verifier si la section suivante est vide
            next_data = None
            for j in range(i + 1, len(new_lines)):
                if new_lines[j].strip().startswith("## "):
                    break
                if new_lines[j].strip().startswith("- "):
                    next_data = new_lines[j]
                    break
            if next_data is None:
                # Section vide, ne pas l ajouter
                continue
        final.append(l)

    nb_supprime = len(lignes) - len(final)
    contenu_new = "\n".join(final)
    ecrire(path, contenu_new, cfg["encoding"], cfg["newline"])
    print("  [CORPS] %d lignes supprimees" % nb_supprime)
    return nb_supprime


def vider_jarvis():
    """Vider les inbox/outbox JARVIS."""
    nb = 0
    for dossier, nom in [(INBOX_DIR, "inbox"), (OUTBOX_DIR, "outbox")]:
        if dossier.exists():
            for f in dossier.glob("*.jsonl"):
                f.unlink()
                nb += 1
                print("  [JARVIS] %s/%s supprime" % (nom, f.name))
    if nb == 0:
        print("  [JARVIS] inbox/outbox deja vides")
    return nb


def purger_bdd():
    """Purger la BDD (entrees > 7 jours)."""
    if not BDD_FILE.exists() or BDD_FILE.stat().st_size == 0:
        print("  [BDD] Absente ou vide")
        return 0
    try:
        conn = sqlite3.connect(str(BDD_FILE))
        # Compter avant
        avant = conn.execute("SELECT COUNT(*) FROM historique").fetchone()[0]
        # Purger > 7 jours
        seuil = datetime.now().timestamp() - 7 * 86400
        conn.execute("DELETE FROM historique WHERE date_iso < ?",
                     (datetime.fromtimestamp(seuil).strftime("%Y-%m-%dT%H:%M:%S"),))
        apres = conn.execute("SELECT COUNT(*) FROM historique").fetchone()[0]
        conn.commit()
        conn.close()
        supprime = avant - apres
        print("  [BDD] %d entrees purgees (%d restantes)" % (supprime, apres))
        return supprime
    except Exception as e:
        print("  [BDD] Erreur: %s" % e)
        return 0


def nettoyer(llm_id, session):
    print("=== NETTOYAGE SESSION (outils-llm/nettoyer-session.py v%s) ===" % VERSION)
    print("  id     : %s" % llm_id)
    print("  session: %s" % session)

    total = 0

    # 1. Vider l encart
    print()
    print("--- Encart ---")
    total += vider_encart(session)

    # 2. Vider le corps/historique
    print()
    print("--- Historique ---")
    total += vider_corps(session)

    # 3. Si freelance, vider JARVIS + purger BDD
    if session == "session-freelance":
        print()
        print("--- JARVIS ---")
        vider_jarvis()
        print()
        print("--- BDD ---")
        purger_bdd()

    # 4. Historiser le nettoyage
    print()
    print("--- Historisation ---")
    from pathlib import Path
    sys.path.insert(0, str(RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis" / "fonctions"))
    try:
        from historique import historiser
        historiser("systeme", "NETTOYAGE SESSION: encart + historique vides", "R",
                   session=session)
        print("  [HISTORISATION] nettoyage trace")
    except Exception as e:
        print("  [HISTORISATION] Erreur: %s" % e)

    print()
    print("=== NETTOYAGE TERMINE : %d elements supprimes ===" % total)
    return 0


def afficher_aide():
    print("usage: nettoyer-session.py <id> <session>")
    print()
    print("NETTOYAGE EXCLUSIF D UNE SESSION - outils-llm/")
    print("Vide l encart et l historique de la session demandee.")
    print("Pour freelance : vide aussi inbox/outbox JARVIS + purge BDD.")
    print()
    print("exemples :")
    print("  python3 outils-llm/nettoyer-session.py glm5 admin")
    print("  python3 outils-llm/nettoyer-session.py freebuff freelance")
    print()
    print("options :")
    print("  --help, -h   Afficher cette aide")


def main(argv):
    if argv and argv[0] in ("--help", "-h", "aide"):
        afficher_aide()
        return 0
    if not argv or len(argv) < 2:
        print("ERREUR: id et session obligatoires")
        afficher_aide()
        return 1
    llm_id = argv[0]
    session = argv[1]
    if session in ("admin", "freelance"):
        session = "session-" + session
    if not session.startswith("session-"):
        print("ERREUR: session invalide '%s' (admin ou freelance attendu)" % argv[1])
        return 1
    return nettoyer(llm_id, session)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
