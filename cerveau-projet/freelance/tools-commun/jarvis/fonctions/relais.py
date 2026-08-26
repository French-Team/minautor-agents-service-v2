# -*- coding: ascii -*-
"""fonctions/relais.py - SUPPRIME (decision utilisateur 2026-08-26).

Le relais EDITH->stark a ete RETIRE : il poussait automatiquement les
messages du hub d'EDITH vers stark ([RELAI]) et inondait son inbox de
P1 (69 non-lus signales par flux/harnais).

Nouveau modele (valide 2026-08-26) : les routines d'EDITH (vigie,
notation) deposent a JARVIS UNIQUEMENT une DEMANDE D'ACTIVATION EDITH ;
JARVIS active EDITH qui fait SON travail (4 W / questionnaire) et
transmet SON rapport a JARVIS, qui route ensuite (Stark decide, Forge
applique via rating-agents). Plus aucun relais automatique vers stark.

Cette fonction reste appelee par le daemon et jarvis.py mais ne fait
plus rien (compatibilite) : elle retourne 0.
"""

VERSION = "0.2.0"


def relayer_vers_stark():
    """SUPPRIME (decision utilisateur 2026-08-26) : plus aucun relais
    automatique EDITH->stark. Les demandes d'EDITH vont a JARVIS qui
    active EDITH ; le rapport d'EDITH route ensuite via JARVIS.
    Retourne 0 (compatibilite : encore appele par le daemon)."""
    return 0


def cmd_relayer(args=None):
    n = relayer_vers_stark()
    print("[JARVIS] Relai : %d message(s) du hub transmis a stark."
          % n if n else "[JARVIS] Relai : rien a transmettre.")
