"""Categorie retiqueter : interface entre main.py et retiqueter/fonctions.py (MO-122).

Une porte de REPARATION ne refuse pas de reparer (raisonnement tenu en MO-115
pour le TYPE d'une mission) : elle accepte toute entree, quel que soit son
etat, et laisse une TRACE. Elle refuse en revanche TROIS choses -- une entree
inconnue (rien a corriger), une correction VIDE (ni tag ni date : elle ne sait
pas ce que l'appelant veut dire) et un RE-DATAGE sur une seconde DEJA OCCUPEE
(MO-124 : il recreerait la collision qu'il sert a reparer). Dans les trois cas
elle le DIT et n'ecrit rien.
"""
from ajouter.fonctions import assainir_ascii, separer_tags
from commun import charger_bdd, enregistrer_bdd, extraire_options
from retiqueter.fonctions import (
    occupants,
    re_dater_entree,
    retiqueter_entree,
    trouver,
    valider_horodatage,
)

NOMS_OPTIONS = ("id", "tags", "motif", "horodatage")

USAGE = (
    'Usage : python main.py retiqueter --id S-0XX [--tags "a,b"]'
    ' [--horodatage "AAAA-MM-JJ HH:MM:SS"] [--motif "..."]'
    " (au moins l'un des deux : --tags ou --horodatage)"
)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = assainir_ascii(options.get("id", ""))
    tags = [assainir_ascii(t) for t in separer_tags(options.get("tags", ""))]
    motif = assainir_ascii(options.get("motif", ""))
    horodatage_brut = assainir_ascii(options.get("horodatage", ""))

    if not identifiant or (not tags and not horodatage_brut):
        print(USAGE)
        return 2

    horodatage = None
    if horodatage_brut:
        horodatage = valider_horodatage(horodatage_brut)
        if horodatage is None:
            print(
                'ECART : horodatage illisible ("' + horodatage_brut
                + '") -- attendu "AAAA-MM-JJ HH:MM:SS" (rien ecrit).'
            )
            return 1

    donnees = charger_bdd()
    entree = trouver(donnees, identifiant)
    if entree is None:
        print("ECART : entree " + identifiant + " inconnue de la BDD (rien ecrit).")
        return 1

    if horodatage is not None:
        preneurs = occupants(donnees, horodatage, identifiant)
        if preneurs:
            print(
                "ECART : la seconde " + horodatage + " est deja occupee par "
                + ", ".join(str(e.get("id", "?")) for e in preneurs)
                + " -- re-dater ici recreerait la collision a reparer (rien ecrit)."
            )
            return 1

    morceaux = []
    verbe = ""
    if tags:
        avant = list(entree.get("tags", []))
        retiqueter_entree(entree, tags, motif)
        verbe = "retiquee"
        morceaux.append(
            "tags : " + ", ".join(tags)
            + " | avant : " + (", ".join(avant) if avant else "aucun")
        )
    if horodatage is not None:
        avant_date = str(entree.get("date", "?"))
        re_dater_entree(entree, horodatage, motif)
        verbe = verbe + " et re-datee" if verbe else "re-datee"
        morceaux.append("date : " + avant_date + " -> " + horodatage)

    empreinte = enregistrer_bdd(donnees)
    print(
        "Entree " + identifiant + " " + verbe + " (" + " ; ".join(morceaux)
        + ") -- motif : " + (motif if motif else "non donne")
        + " -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
