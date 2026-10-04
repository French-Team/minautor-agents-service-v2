"""Categorie generer : orchestre la duplication d'un moule (outil bdd, theme bdd, routine).

Interface entre main.py et les fonctions simples (generer/fonctions.py).
"""
from generer.fonctions import (
    appliquer_surcharge,
    ecrire_outil,
    lire_moules,
    repertoire_cible,
    substitutions,
    traduire,
    valider_cadence,
    valider_parametres,
    verifier_outil_executable,
    verifier_sources,
)
from commun import extraire_options
from constants import MOULE_DEFAUT, MOULE_ROUTINE, NOMS_OPTIONS, ZONES  # noqa: F401 (NOMS_OPTIONS etendu)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    moule = options.get("moule", MOULE_DEFAUT)
    nom = options.get("nom", "")
    bdd = options.get("bdd", "")
    prefixe = options.get("prefixe", "")
    liste = options.get("liste", "")
    champ = options.get("champ", "")
    humain = options.get("humain", "")
    role = options.get("role", "")
    cadence = options.get("cadence", "")
    zone = options.get("zone", "")

    code, message = valider_parametres(moule, nom, bdd, prefixe, liste, champ, role, zone)
    if code != 0:
        print(message)
        return code

    code, message = valider_cadence(moule, cadence)
    if code != 0:
        print(message)
        return code

    table = substitutions(moule, nom, bdd, prefixe, liste, champ, humain,
                          options.get("nom-affiche", ""), role, cadence)
    moules = lire_moules(moule)
    if not moules:
        print("ECART : aucun moule trouve dans templates/" + moule + "/")
        return 1

    en_memoire = [traduire(chemin, table) for chemin in moules]
    if zone:
        en_memoire = appliquer_surcharge(en_memoire, table, ZONES[zone]["moule"])
    code, messages = verifier_sources(en_memoire)
    if code != 0:
        print("ECARTS avant ecriture : " + " | ".join(messages))
        return 1

    repertoire_clone = repertoire_cible(moule, nom, zone)
    if repertoire_clone.exists():
        print("ECART : " + nom + " existe deja (jamais d'ecrasement).")
        return 2

    ecrire_outil(repertoire_clone, en_memoire)
    code, message = verifier_outil_executable(repertoire_clone, moule)
    if code != 0:
        print("ECART apres ecriture : " + message + " -- clone incomplet, a reparer avant usage.")
        return 1

    print(
        "Clone " + nom + " genere depuis le moule " + moule
        + ((" + surcharge " + zone) if zone else "")
        + " (" + str(len(en_memoire))
        + " fichiers) : compile, ASCII strict, sans jeton residuel, executable."
    )
    if moule == MOULE_ROUTINE:
        print("Suites attendues : remplir passe/fonctions.passer(), declarer la routine dans"
              " le serveur (routines/vie/constants.py), puis prouver --once + arret cooperatif.")
    else:
        print("Suites attendues : fiche manuel + registre espion-integrite + premiere entree de la BDD.")
    return 0
