#!/usr/bin/env bash
# -*- coding: ascii -*-
# detecter-decalages-catalogue.sh
# Wrapper pur : delegue au .py (parite par construction).
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
python3 "$(dirname "$0")/detecter-decalages-catalogue.py" "$@"
