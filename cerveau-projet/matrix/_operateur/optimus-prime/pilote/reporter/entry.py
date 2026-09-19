"""Categorie reporter : PARQUER la mission en cours, TRACEE (EO-182).

Interface entre main.py et les fonctions simples (reporter/fonctions.py).
Le --raison est OBLIGATOIRE : un report sans raison est un abandon silencieux,
et un abandon silencieux n'est pas un report.

Ce que ce verbe NE fait PAS, et c'est delibered : il n'EFFACE rien, ne VIDE rien
et ne SORT la mission d'aucune file -- il la remet EN ATTENTE, avec sa raison et
son compteur de reports.
"""
from commun import charger_file, extraire_options
from reporter.fonctions import reporter_mission

NOMS_OPTIONS = ("raison",)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    raison = (options.get("raison") or "").strip()
    if not raison:
        print('Usage : python main.py reporter --raison "..."')
        print("        La raison est OBLIGATOIRE : sans elle, un report serait un abandon muet.")
        return 2
    return reporter_mission(charger_file, raison)
