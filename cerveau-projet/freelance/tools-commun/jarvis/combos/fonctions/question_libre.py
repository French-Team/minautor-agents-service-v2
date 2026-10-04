# -*- coding: ascii -*-
"""fonctions/question_libre.py - module du combo QUESTION_LIBRE."""
import re
from datetime import datetime
from lib_lecture import lire_texte
from etat import combo_etat
from cherche import combo_cherche
from rappelle import combo_rappelle
from resume import combo_resume


def combo_question_libre(besoin):
    """v0.3.0 : temps 2 REEL - analyse l'intention et dispatch."""
    q = besoin.lower()
    if re.search(r"\betat\b|\bbloque\b|statut|qui travaille", q):
        cible = "ETAT"
    elif re.search(r"rappele|rappelle|decision\b|\bd\d+\b|memoire", q):
        cible = "RAPPELLE"
    elif re.search(r"\.md|\.py|\.json|\.txt|resume|resum", q):
        cible = "RESUME"
    elif re.search(r"cherche|ou est|trouve|existe|liste", q):
        cible = "CHERCHE"
    else:
        return {
            "combo": "?", "besoin": besoin, "statut": "AMBIGU",
            "reponse": ("question libre non classee. Je sais repondre a : "
                        "ETAT (etat du systeme), RESUME <fichier> "
                        "(synthese), CHERCHE <motif> (recherche), "
                        "RAPPELLE <sujet> (memoire des decisions)."),
            "date": datetime.now().isoformat(timespec="seconds")}
    args = besoin.split()
    # retirer les mots d'intention pour ne passer que la cible utile
    utiles = [m for m in args if m.lower() not in (
        "qui", "quoi", "quel", "quelle", "est", "le", "la", "les", "de",
        "du", "des", "un", "une", "et", "?", "cherche", "resume", "resum",
        "rappele", "rappelle", "moi", "pour", "sur")]
    sous_besoin = " ".join(utiles) if utiles else besoin
    # le token le plus SPECIFIQUE d'abord : une reference Dxx, sinon le
    # plus long mot (evite les motifs generiques comme "ou" ou "fichier")
    specifique = [m for m in utiles if re.fullmatch(r"D\d+", m,
                                                    re.IGNORECASE)]
    if specifique:
        sous_besoin = specifique[0]
    elif utiles:
        sous_besoin = max(utiles, key=len)
    if cible == "ETAT":
        resultat = combo_etat(sous_besoin)
    elif cible == "RESUME":
        resultat = combo_resume(sous_besoin)
    elif cible == "CHERCHE":
        resultat = combo_cherche(sous_besoin)
    else:
        resultat = combo_rappelle(sous_besoin)
    return {
        "combo": "?", "besoin": besoin, "statut": "OK",
        "dispatch_vers": cible,
        "resultat": resultat,
        "date": datetime.now().isoformat(timespec="seconds")}
