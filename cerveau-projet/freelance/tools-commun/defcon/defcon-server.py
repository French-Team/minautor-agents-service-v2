#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
defcon-server.py -- OBSOLETE depuis v0.1.1 (protocole 14).

Le point d'entree est desormais entry.py (structure entry.py +
fonctions/, auto-verification harnais protocole 21). Ce fichier est
conserve comme relais de compatibilite : il delegue a entry.py.
"""

import os
import sys

sys.exit(os.system("%s %s" % (
    sys.executable,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.py"))))
