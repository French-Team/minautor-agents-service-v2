#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
entry.py - POINT D'ENTREE de jarvis (P1 : orchestrateur).

Delegue au module jarvis.py (parsing CLI + dispatch, protocole 14).
L auto-verification harnais est faite par jarvis.main().

Usage :
    python3 entry.py --help
    python3 entry.py demarrage

Proprietaire : Vision
Version : 0.11.0
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import jarvis  # noqa: E402


if __name__ == "__main__":
    jarvis.main()
