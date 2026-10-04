#!/usr/bin/env python3
# -*- coding: ascii -*-
"""Vol etats v1 -- transitions strictes du protocole bout en bout."""

import json
from datetime import datetime

ETATS = ("DEPOSEE", "DECOLLAGE", "LARGUEE", "PRISE", "EN_TRAVAIL",
         "FIN", "RECUPEREE", "RETOUR AEROPORT", "CLOTUREE", "QUARANTAINE")
TRANSITIONS = {
    "DEPOSEE": ("DECOLLAGE", "QUARANTAINE"),
    "DECOLLAGE": ("LARGUEE", "QUARANTAINE"),
    "LARGUEE": ("PRISE", "QUARANTAINE"),
    "PRISE": ("EN_TRAVAIL", "QUARANTAINE"),
    "EN_TRAVAIL": ("FIN", "QUARANTAINE"),
    "FIN": ("RECUPEREE", "RETOUR AEROPORT", "QUARANTAINE"),
    "RECUPEREE": ("RETOUR AEROPORT", "QUARANTAINE"),
    "RETOUR AEROPORT": ("CLOTUREE", "QUARANTAINE"),
    "CLOTUREE": (),
    "QUARANTAINE": (),
}


def maintenant():
    return datetime.now().isoformat(timespec="seconds")


def creer_vol(mission_id, agent, super_pilote=False):
    return {
        "vol_id": "%s-%s" % (agent, mission_id),
        "mission_id": mission_id,
        "agent": agent,
        "super_pilote": bool(super_pilote),
        "etat": "DEPOSEE",
        "historique": [{"etat": "DEPOSEE", "date": maintenant()}],
    }


def transition(vol, nouvel_etat, preuve=None):
    actuel = vol.get("etat")
    if nouvel_etat not in TRANSITIONS.get(actuel, ()):
        raise ValueError("transition interdite: %s -> %s" % (actuel, nouvel_etat))
    if nouvel_etat == "FIN" and not (preuve or {}).get("bilan", "").strip():
        raise ValueError("FIN exige un bilan explicite")
    if nouvel_etat == "EN_TRAVAIL" and not (preuve or {}).get("reaction"):
        raise ValueError("EN_TRAVAIL exige une reaction agent")
    if nouvel_etat == "CLOTUREE" and not (preuve or {}).get("retour_oracle"):
        raise ValueError("CLOTUREE exige un retour Oracle")
    vol["etat"] = nouvel_etat
    evenement = {"etat": nouvel_etat, "date": maintenant()}
    if preuve:
        evenement["preuve"] = preuve
    vol.setdefault("historique", []).append(evenement)
    return vol


def charger(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def sauver(path, vol):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(vol, fh, ensure_ascii=True, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    vol = creer_vol("demo", "agent")
    for etat, preuve in (("DECOLLAGE", None), ("LARGUEE", None),
                         ("PRISE", None), ("EN_TRAVAIL", {"reaction": True}),
                         ("FIN", {"bilan": "demonstration terminee"}),
                         ("RECUPEREE", None), ("RETOUR AEROPORT", None),
                         ("CLOTUREE", {"retour_oracle": True})):
        transition(vol, etat, preuve)
    print(json.dumps(vol, ensure_ascii=True, indent=2))
