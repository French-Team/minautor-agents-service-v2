"""Categorie noter : orchestre l'enregistrement d'un evenement de la trace.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import ajouter_ligne, extraire_options, lire_evenements
from constants import ACTIONS, PREFIXE_CAMELEON, PREFIXE_MISSION
from noter.fonctions import construire_evenement, separer_liste

NOMS_OPTIONS = ("mission", "theme", "action", "detail", "fichiers", "portes", "duree-s",
                "si-absent")

# Valeurs qui arment le mode `--si-absent` (jamais devinees : il faut le mot).
VALEURS_SI_ABSENT = ("oui", "1", "true", "vrai")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    mission = options.get("mission", "")
    theme = options.get("theme", "")
    action = options.get("action", "")
    detail = options.get("detail", "")
    fichiers = separer_liste(options.get("fichiers", ""))
    portes = separer_liste(options.get("portes", ""))
    duree_s = options.get("duree-s", "")

    if not action or not detail:
        print('Usage : python main.py noter --mission MO-XXX --theme SUIVI --action <action> --detail "..."  (Optimus : MO- ; M- = cameleon)')
        return 2

    # Garde prefixe (M-030 / correction createur) : une mission du cameleon
    # notee ici sort du perimetre Flux 2. Les deux prefixes viennent de
    # constants.py (PREFIXE_CAMELEON / PREFIXE_MISSION), jamais recopies.
    if mission.startswith(PREFIXE_CAMELEON):
        print(
            "AVERTISSEMENT prefixe : mission '" + mission + "' commence par "
            + PREFIXE_CAMELEON + " (cameleon). Les missions Optimus sont "
            + PREFIXE_MISSION + "xxx (pilote/constants.py PREFIXE_ID)."
        )
    if action not in ACTIONS:
        print(
            "Action inconnue : " + repr(action)
            + " (actions fermees : " + ", ".join(ACTIONS) + ")"
        )
        return 2

    # MODE `--si-absent oui` (MO-108) : COMBLER LE TROU, JAMAIS DOUBLER.
    # Le PILOTE s'en sert pour declarer les BORNES d'une mission (debut/fin) :
    # mesure du 2026-09-15 -- MO-105 et MO-106 ont ete closes SANS fin au marbre
    # parce que la declaration reposait sur la MEMOIRE de l'agent. L'ancien appel
    # automatique avait ete retire (MO-030) parce qu'il fabriquait un 2e debut et
    # un 2e fin : avec ce mode le pilote n'ecrit QUE si l'evenement manque, donc
    # le doublon est impossible par construction. Le DEFAUT reste inchange (la
    # porte note ce que l'agent declare, reprises comprises) : ce mode n'interdit
    # RIEN a l'agent, il evite au pilote de doubler.
    si_absent = options.get("si-absent", "").strip().lower() in VALEURS_SI_ABSENT
    if si_absent and mission:
        for evenement in lire_evenements():
            if (evenement.get("mission") == mission
                    and evenement.get("action") == action):
                print("SI-ABSENT : " + mission + " porte deja un evenement '" + action
                      + "' -- RIEN ecrit (le trou est comble, rien n'est double).")
                return 0

    # Garde anti-doublon : NON. Mesure du 2026-09-13 -- `verifier` considere
    # qu'un doublon debut/fin est un ECART, SAUF pour une mission de reprise
    # declaree (REPRISES_DOUBLON_OK : meme mission menee sur 2 sessions, 2 debut
    # + 2 fin legitimes). Un refus sec ici interdirait a l'agent un fait REEL,
    # et ferait diverger la porte du controle qui la juge (paire porte/garde-fou
    # neutralisee). La porte NOTE ce que l'agent declare ; c'est `verifier` qui
    # JUGE la trace. Le vrai coupable du doublon MO-061 n'est pas ici : c'est le
    # verbe `enregistrer` du pilote, qui NOTAIT un debut deja present -- corrige
    # dans _operateur/optimus-prime/pilote/file/fonctions.py.

    # Garde anti-fin-orpheline (revision createur) : une fin sans debut
    # ouvert auto-cree le debut manquant (historique jamais reecrit).
    if action == "fin" and mission:
        debuts = [e for e in lire_evenements()
                  if e.get("mission") == mission and e.get("action") == "debut"]
        if not debuts:
            implicite = construire_evenement(
                mission, theme, "debut",
                "Debut implicite (garde anti-fin-orpheline) : mission prise en charge.",
                [], [], "")
            ajouter_ligne(implicite)
            print("Debut implicite cree pour " + mission + " (aucun debut note).")

    evenement = construire_evenement(mission, theme, action, detail, fichiers, portes, duree_s)
    empreinte = ajouter_ligne(evenement)
    print(
        "Evenement note (action : " + action
        + ", mission : " + (mission or "-")
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0