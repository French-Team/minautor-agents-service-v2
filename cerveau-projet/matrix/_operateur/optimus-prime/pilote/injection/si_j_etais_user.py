#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
si_j_etais_user.py -- LA SOURCE D INJECTION < SI J ETAIS USER > (MO-416, EO-432).

POURQUOI CE DOMICILE (decision du createur, 2026-09-25). La phase < si j etais user >
n est PAS un crochet : aucun nouveau mot entre crochets. Elle fait partie du PRINCIPE
DE RAISONNEMENT pendant le travail, et c est le PILOTE qui la sert AU MOMENT ou on en a
besoin. Le TEXTE de la phase vit chez sa famille
(pilote/protocoles/proto-13-si-j-etais-user.md) et n est JAMAIS recopie ici (M-076) :
ce module est le domicile du MOMENT -- il DECIDE, a partir de la mission, si la source
sert, il le DIT (le motif est ce que l agent lit ET ce que la trace declare), et il
SERT les trois questions du protocole en les LISANT a leur domicile.

LES MOMENTS (fermes, declares ici -- aucun seuil dans le code) :
  - demande : l objectif demande la phase MOT POUR MOT ;
  - encore  : l objectif dit qu un resultat se REDEMANDE (famille < je dois refaire >,
              < a la main >, < chaque fois > du proto-13).

CE QU IL REND. decider(titre, objectif) -> un dict a quatre cles : applique (bool),
moment (str), motif (str -- POURQUOI), questions (liste lue au domicile). Le protocole
illisible ne supprime PAS la decision : elle applique quand meme et le motif le DIT
(une lecture muette serait un angle mort, L-055 / L-163).

Usage:
  python3 si_j_etais_user.py --titre "..." --objectif "..."   (la decision, lisible)
  python3 si_j_etais_user.py --auto-test                      (cobaye + contre-temoins)
"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
CHEMIN_PROTOCOLE = (BASE.parent.parent / "protocoles"
                    / "proto-13-si-j-etais-user.md")

# LES MOMENTS : liste FERMEE, declaree ICI. Le jour ou un moment manque, il s ajoute
# ici et le cobaye de `--auto-test` le couvre -- jamais une valeur posee en passant.
MOTS_DEMANDE = ("si j etais user", "si j etais un user", "si j etais l user")
MOTS_ENCORE = ("refaire", "encore", "chaque fois", "a chaque fois", "a la main",
               "manuellement", "systematiquement", "repetitif", "repetitive",
               "recopier", "dupliquer", "toujours pareil")
MOMENTS = (
    {"id": "demande", "mots": MOTS_DEMANDE,
     "libelle": "l objectif DEMANDE la phase, mot pour mot"},
    {"id": "encore", "mots": MOTS_ENCORE,
     "libelle": "l objectif REDEMANDE un geste (famille < je dois refaire > du proto-13)"},
)
TITRE_SECTION = "la question"
NOMBRE_QUESTIONS = 3
PREMIERE_DUREE = "2026-09-25 21:30:00"


def lire_questions():
    """Les trois questions de la phase, LUES dans le protocole (son domicile, M-076).

    Rend [] si le domicile est illisible : l appelant le DIT, il ne l avale pas.
    """
    try:
        lignes = CHEMIN_PROTOCOLE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    debut = None
    for index, ligne in enumerate(lignes):
        if not ligne.startswith("#"):
            continue
        if TITRE_SECTION in ligne.lstrip("#").strip().lower():
            debut = index
            break
    if debut is None:
        return []
    questions = []
    for ligne in lignes[debut + 1:]:
        depouille = ligne.strip()
        if not depouille:
            continue
        if depouille.startswith("#") and questions:
            break
        if len(depouille) > 1 and depouille[0].isdigit() and depouille[1] == ".":
            questions.append(depouille)
        elif questions:
            questions[-1] = questions[-1] + " " + depouille
    return questions


def decider(titre, objectif):
    """La DECISION, et son POURQUOI : la source sert-elle CE round, et a quel moment ?"""
    texte = (str(titre or "") + " " + str(objectif or "")).lower()
    for moment in MOMENTS:
        for mot in moment["mots"]:
            if mot not in texte:
                continue
            questions = lire_questions()
            motif = ("moment <" + moment["id"] + "> : " + moment["libelle"]
                     + " (mot repere : <" + mot + ">)")
            if not questions:
                motif += (" ; les questions du protocole n ont PAS pu etre lues a leur"
                          " domicile (" + str(CHEMIN_PROTOCOLE) + ")")
            return {"applique": True, "moment": moment["id"], "motif": motif,
                    "questions": questions}
    return {"applique": False, "moment": "",
            "motif": ("aucun moment : l objectif ne REDEMANDE aucun geste et ne demande"
                      " pas la phase mot pour mot"),
            "questions": []}


def auto_test():
    """Le cobaye MORD sur les moments, les contre-temoins EPARGNENT le reste."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    questions = lire_questions()
    controler("les questions se LISENT a leur domicile (jamais recopiees)",
              len(questions) == NOMBRE_QUESTIONS,
              str(len(questions)) + " question(s) lue(s) dans " + CHEMIN_PROTOCOLE.name)
    cobaye_demande = decider("TITRE", "Si j etais user, qu est-ce que je ne voudrais pas refaire ?")
    controler("il MORD sur la DEMANDE mot pour mot",
              cobaye_demande["applique"] and cobaye_demande["moment"] == "demande",
              cobaye_demande["motif"][:88])
    cobaye_encore = decider("TITRE", "je dois refaire ce geste a la main chaque fois")
    controler("il MORD sur un resultat qui se REDEMANDE",
              cobaye_encore["applique"] and cobaye_encore["moment"] == "encore",
              cobaye_encore["motif"][:88])
    controler("la decision EMPORTE les questions",
              len(cobaye_encore["questions"]) == NOMBRE_QUESTIONS,
              str(len(cobaye_encore["questions"])) + " question(s) servie(s)")
    temoin = decider("corriger le libelle", "corriger le libelle du bouton du formulaire")
    controler("il EPARGNE une mission qui ne redemande RIEN",
              not temoin["applique"], temoin["motif"][:88])
    vide = decider("", "")
    controler("il EPARGNE un objectif vide",
              not vide["applique"], "aucun moment : aucune accusation")
    gagnes = sum(1 for resultat in resultats if resultat)
    print("")
    print("AUTO-TEST SI J ETAIS USER : " + str(gagnes) + "/" + str(len(resultats)) + " temoins")
    if gagnes != len(resultats):
        print("VERDICT : KO -- la source ne mord pas (ou n epargne pas) comme elle le dit.")
        return 1
    print("VERDICT : OK -- la source MORD sur les moments et EPARGNE le reste.")
    return 0


def main():
    arguments = sys.argv[1:]
    if "--auto-test" in arguments:
        return auto_test()
    options = {}
    for nom, cle in (("--titre", "titre"), ("--objectif", "objectif")):
        if nom in arguments:
            position = arguments.index(nom)
            if position + 1 < len(arguments):
                options[cle] = arguments[position + 1]
    if not options:
        print(__doc__)
        print("REFUS : donner --titre / --objectif, ou --auto-test.")
        return 2
    decision = decider(options.get("titre", ""), options.get("objectif", ""))
    print("SOURCE SI J ETAIS USER -- "
          + ("APPLIQUE" if decision["applique"] else "NE SERT PAS CE ROUND"))
    print("  moment : " + (decision["moment"] or "(aucun)"))
    print("  motif  : " + decision["motif"])
    for rang, question in enumerate(decision["questions"], 1):
        print("  " + str(rang) + ". " + question)
    return 0


if __name__ == "__main__":
    sys.exit(main())
