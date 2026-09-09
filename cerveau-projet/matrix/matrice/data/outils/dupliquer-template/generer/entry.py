"""Categorie generer : orchestre la duplication du moule outil-bdd.

Interface entre main.py et les fonctions simples (generer/fonctions.py).
"""
from generer.fonctions import (
    ecrire_outil,
    lire_moules,
    substitutions,
    traduire,
    valider_parametres,
    verifier_outil_executable,
    verifier_sources,
)
from commun import extraire_options
from constants import MOULE_DEFAUT, NOMS_OPTIONS, REPERTOIRE_OUTILS  # noqa: F401 (NOMS_OPTIONS etendu)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    moule = options.get("moule", MOULE_DEFAUT)
    nom = options.get("nom", "")
    bdd = options.get("bdd", "")
    prefixe = options.get("prefixe", "")
    liste = options.get("liste", "")
    champ = options.get("champ", "")
    humain = options.get("humain", "")

    code, message = valider_parametres(moule, nom, bdd, prefixe, liste, champ)
    if code != 0:
        print(message)
        return code

    table = substitutions(moule, nom, bdd, prefixe, liste, champ, humain, options.get("nom-affiche", ""))
    moules = lire_moules(moule)
    if not moules:
        print("ECART : aucun moule trouve dans templates/" + moule + "/")
        return 1

    en_memoire = [traduire(chemin, table) for chemin in moules]
    code, messages = verifier_sources(en_memoire)
    if code != 0:
        print("ECARTS avant ecriture : " + " | ".join(messages))
        return 1

    repertoire_outil = REPERTOIRE_OUTILS / nom
    if repertoire_outil.exists():
        print("ECART : " + nom + " existe deja (jamais d'ecrasement).")
        return 2

    ecrire_outil(repertoire_outil, en_memoire)
    code, message = verifier_outil_executable(repertoire_outil, moule)
    if code != 0:
        print("ECART apres ecriture : " + message + " -- clone incomplet, a reparer avant usage.")
        return 1

    print(
        "Outil " + nom + " genere depuis le moule " + moule + " (" + str(len(en_memoire))
        + " fichiers) : compile, ASCII strict, sans jeton residuel, executable."
    )
    print("Suites attendues : fiche manuel + registre espion-integrite + premiere entree de la BDD.")
    return 0
