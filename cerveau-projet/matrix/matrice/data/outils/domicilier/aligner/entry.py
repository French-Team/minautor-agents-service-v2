"""Entree du verbe aligner : garder la PORTE avant la main.

Role : ORCHESTRER (options -> plan -> premisses -> alignement). --simuler est le
DEFAUT : sans --publier, la remorque se contente de DIRE ce qu'elle ferait.
"""
from aligner.fonctions import executer
from constants import NOM_PLAN_DEFAUT, REPERTOIRE_PLANS
from commun import CLE_SANS_VALEUR, charger_plan, extraire_options, verifier_premisses

NOMS_CONNUS = ("plan", "publier", "simuler", "perimetre")
DRAPEAUX = ("publier", "simuler")

REFUS_EXCLUSIF = "--publier et --simuler sont exclusifs : la remorque ne devine pas ce qu'on veut d'elle."


def executer_verbe(arguments):
    options = extraire_options(arguments, NOMS_CONNUS, drapeaux=DRAPEAUX)
    sans_valeur = options.get(CLE_SANS_VALEUR)
    if sans_valeur:
        print("REFUS : option privee de valeur : " + ", ".join("--" + nom for nom in sans_valeur))
        return 2
    if options.get("publier") and options.get("simuler"):
        print("REFUS : " + REFUS_EXCLUSIF)
        return 2
    chemin = options.get("plan") or str(REPERTOIRE_PLANS / NOM_PLAN_DEFAUT)
    try:
        plan = charger_plan(chemin)
    except ValueError as erreur:
        print("REFUS : " + str(erreur))
        return 2
    ecarts = verifier_premisses(plan)
    if ecarts:
        print("REFUS : le plan n'est pas sur ses premisses (rien n'a ete lu ni ecrit) :")
        for ecart in ecarts:
            print("  - " + ecart)
        return 2
    return executer(plan, ecrire_vraiment=bool(options.get("publier")), perimetre=options.get("perimetre"))
