#!/usr/bin/env bash
# -*- coding: ascii -*-
# enregistrer-usage-outil.sh
# Wrapper pur : delegue au .py (parite par construction).
# Version : 0.2.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
python3 "$(dirname "$0")/enregistrer-usage-outil.py" "$@"
