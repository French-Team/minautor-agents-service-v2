#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constantes de selecteur-flux -- la DECLARATION d'un VERIFICATEUR en lecture seule.

CE QUE CE DOSSIER EST (mesure du 2026-09-23) : un VERIFICATEUR one-shot
(`verifier-selecteur.py`), ne AVANT le moule (sa provenance le declare
`anterieure`) et SANS les invariants d'une routine de boucle : aucun PID propre,
aucune cadence, aucun journal, aucun etat -- et AUCUNE ECRITURE (mesure : zero
site d'ecriture dans son script ; il LIT le selecteur et deux PID de watchdog).
C'est pourquoi ce fichier ne porte NI cadence NI PID NI etat : les y mettre
aurait ete un moule MENTEUR.

POURQUOI IL EXISTE QUAND MEME (friction du 2026-09-23) : le CONTROLE
D'ATTRIBUTION lit la declaration d'une routine dans SES constantes. Un dossier de
`routines/` sans declaration lisible est un SILENCE, et le controle le DIT a
chaque passe (`declarations de routine NON LUES`) -- sans pouvoir distinguer
"n'ecrit rien, donc rien a declarer" de "declaration illisible". Cette case est
VIDE PARCE QUE C'EST VRAI : le jour ou selecteur-flux ecrira un fichier, c'est
ICI qu'il se declare, et le controle le lira sans qu'aucune liste soit retouchee.
"""

# LES PRODUCTIONS DE LA ROUTINE : les fichiers qu'elle ECRIT et qui ne sont PAS
# des sources -- ni ses etats courts de forme conventionnelle (etat, journal,
# cadence, PID). Vide ET verifie vide : ce verificateur n'ecrit rien.
PRODUCTIONS = ()
