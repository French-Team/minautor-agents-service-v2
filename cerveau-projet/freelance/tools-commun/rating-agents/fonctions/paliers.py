# -*- coding: ascii -*-
"""fonctions/paliers.py - definition des paliers de notation (v0.1.0).

HAUSSE (performance) : COPPER -> SILVER -> OR
BAISSE (problemes)   : A_REVOIR -> A_REPARER -> DECLASSE

A_REVOIR  : derapage leve - l agent doit etre relu/eduque (Chiron)
A_REPARER : problemes confirmes - mission de reparation requise
DECLASSE  : l agent ne peut plus travailler seul jusqu a reparation
"""

HAUSSE = ["COPPER", "SILVER", "OR"]
BAISSE = ["A_REVOIR", "A_REPARER", "DECLASSE"]

# qui peut noter (habilitations par defaut, D15 surchargeable)
NOTATEURS = ["stark", "jarvis", "fury", "rogers"]


def palier_valide(palier):
    return palier in HAUSSE + BAISSE


def est_baisse(palier):
    return palier in BAISSE
