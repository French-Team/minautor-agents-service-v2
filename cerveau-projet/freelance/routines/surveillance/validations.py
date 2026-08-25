# -*- coding: ascii -*-
"""validations.py - UNE tache : heuristiques prudentes sur un fichier
modifie (protocole 18). SIGNALE sans bloquer.

Restaure du dossier routines-server.bak-20260823-1700 lors de la
resolution des alertes EDITH du 2026-08-24 : detection.py l'importe
depuis ce repertoire (sys.path de surveiller-modifications.py).
"""

import re


def valider(chemin_absolu):
    """Retourner la liste des violations suspectees :
    [{regle, detail}] - vide si rien de suspect."""
    violations = []
    try:
        brut = open(chemin_absolu, "rb").read()
    except OSError:
        return violations
    try:
        contenu = brut.decode("utf-8")
    except UnicodeDecodeError:
        violations.append({"regle": "D4",
                           "detail": "fichier non decodable en UTF-8"})
        return violations

    # M7/P10 : niveaux comptes hors bootstrap P10
    for i, l in enumerate(contenu.splitlines(), 1):
        if re.search(r"parent(\.parent){2,}", l) and \
                "_p =" not in l and "AGENTS.md" not in l:
            violations.append({"regle": "M7/P10",
                               "detail": f"ligne {i}: niveaux comptes "
                                         f"({l.strip()[:60]})"})

    # D4 : header coding ascii avec contenu non-ascii
    header = contenu[:200].lower()
    if "coding: ascii" in header and any(ord(c) > 127 for c in contenu):
        violations.append({"regle": "D4",
                           "detail": "header coding:ascii mais contenu "
                                     "non-ASCII present"})

    # ASCII strict pour les JSON de parcours
    if chemin_absolu.endswith(".json") and "parcours" in chemin_absolu:
        non_ascii = [c for c in contenu if ord(c) > 127]
        if non_ascii:
            violations.append({"regle": "ASCII",
                               "detail": f"{len(non_ascii)} caractere(s) "
                                         f"non-ASCII dans un JSON de parcours"})

    # P4/M5 : session litterale codee en dur
    for i, l in enumerate(contenu.splitlines(), 1):
        if re.search(r"[\"']session-\d[\"']", l) or \
                re.search(r"default=[\"']session-", l):
            violations.append({"regle": "P4/M5",
                               "detail": f"ligne {i}: session litterale "
                                         f"codee en dur"})
            break

    return violations
