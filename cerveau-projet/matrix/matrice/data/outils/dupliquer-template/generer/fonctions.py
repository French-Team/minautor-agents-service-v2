"""Fonctions simples de la categorie generer : une seule tache chacune."""


import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, lot -- fin du residu) -----------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Bloc AUTOSUFFISANT : il ne depend ni de l ordre des imports du fichier, ni de la
# presence d un `import subprocess` de module (mesure du 2026-09-25 : deux fichiers
# casses par ces deux pieges, invisibles au py_compile).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())

import py_compile
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from constants import (
    CADENCE_DEFAUT_ROUTINE,
    FORMAT_HORODATAGE_GENERATION,
    CHEMIN_MOULE,
    MOTIF_JETON,
    MOTIF_NOM,
    MOTIF_NOM_ROUTINE,
    MOTIF_NOM_THEME,
    MOULE_ROUTINE,
    NOM_MOULE_PRINCIPAL,
    PLANCHER_CADENCE_ROUTINE,
    REPERTOIRE_OUTILS,
    REPERTOIRE_ROUTINES,
    REPERTOIRE_TEMPLATES,
    SUFFIXE_MOULE,
    ZONES,
)


USAGES_PAR_MOULE = {
    "outil-bdd": 'Usage : python main.py generer --moule outil-bdd --nom bdd-xxx --bdd xxx.json --prefixe X --liste xxx --champ xxx',
    "theme-bdd": 'Usage : python main.py generer --moule theme-bdd --nom theme-xxx --bdd xxx.json --prefixe TH [--nom-affiche "NOM"]',
    "routine": 'Usage : python main.py generer --moule routine --nom <nom> --role "<ce que la routine fait>" [--cadence 300]',
}


def valider_parametres(moule, nom, bdd, prefixe, liste, champ, role, zone=""):
    """Verifie la forme des parametres SELON LE MOULE (forme fermee par moule).

    Retourne (code, message) : code 2 si un parametre manque ou deroge.
    `zone` : une zone NOMMEE (ZONES) RESERVE la surcharge hors-data au moule
    outil-bdd et cible le repertoire declare pour cette zone (L-016).
    """
    if zone and zone not in ZONES:
        return 2, "Option --zone inconnue : " + repr(zone) + " (connues : " + ", ".join(ZONES) + ")."
    if zone and moule != "outil-bdd":
        return 2, ("Option --zone " + zone + " : reservee au moule outil-bdd"
                   " (chaque zone est une surcharge d outil-bdd).")
    requis = {
        "outil-bdd": [nom, bdd, prefixe, liste, champ],
        "theme-bdd": [nom, bdd, prefixe],
        "routine": [nom, role],
    }.get(moule)
    if requis is None:
        return 2, "Moule inconnu : " + repr(moule) + " (moules connus : " + ", ".join(USAGES_PAR_MOULE) + ")"
    if not all(requis):
        return 2, USAGES_PAR_MOULE.get(moule, "Usage : consulter la fiche du manuel.")
    if moule == MOULE_ROUTINE:
        motif = MOTIF_NOM_ROUTINE
    elif moule == "theme-bdd":
        motif = MOTIF_NOM_THEME
    else:
        motif = MOTIF_NOM
    if not motif.match(nom):
        return 2, "Nom invalide pour ce moule : " + repr(nom) + " (forme attendue : " + motif.pattern + ")"
    # Un clone ne remplace JAMAIS un vivant : la cible est nommee AVANT d'ecrire
    # quoi que ce soit (la routine a son propre vivier : routines/, pas outils/).
    if repertoire_cible(moule, nom).exists():
        return 2, "ECART : " + nom + " existe deja (jamais d'ecrasement)."
    if moule != MOULE_ROUTINE and REPERTOIRE_OUTILS is None:
        return 1, "ECART : le dossier outils/ est introuvable."
    return 0, ""


def valider_cadence(moule, cadence):
    """Verifie la cadence DECLAREE (en secondes) d'une routine.

    Un outil n'a pas de cadence : l'option est ignoree pour les autres moules.
    Une valeur absente vaut la cadence du modele-mere (le generateur l'ecrit
    dans le clone, il ne la laisse pas en jeton).
    """
    if moule != MOULE_ROUTINE or not cadence:
        return 0, ""
    if not cadence.isdigit() or int(cadence) < PLANCHER_CADENCE_ROUTINE:
        return 2, ("Cadence invalide : " + repr(cadence) + " (secondes entieres >= "
                   + str(PLANCHER_CADENCE_ROUTINE) + " attendues).")
    return 0, ""


def repertoire_cible(moule, nom, zone=""):
    """Le dossier ou le clone atterrit : un OUTIL sous data/outils/, une ROUTINE
    sous routines/, ou le REPERTOIRE DECLARE de la zone demandee (ZONES) quand
    `--zone` est donne -- invisible (Optimus) ou partagee (cameleon). La cible
    vient de la table ZONES, jamais d un chemin en dur ici."""
    if zone:
        return ZONES[zone]["repertoire"] / nom
    if moule == MOULE_ROUTINE:
        return REPERTOIRE_ROUTINES / nom
    return REPERTOIRE_OUTILS / nom


def substitutions(moule, nom, bdd, prefixe, liste, champ, humain, nom_affiche, role="", cadence=""):
    """Retourne la table des jetons -> valeurs SELON LE MOULE.

    Chaque moule ne consomme que SES jetons : un jeton absent du moule
    recoit une valeur vide (le generateur refuse tout jeton residuel de
    toute facon, donc une erreur de moule reste detectee).
    """
    table = {
        "__NOM_OUTIL__": nom,
        "__NOM_BDD__": bdd,
        "__PREFIXE_ID__": prefixe,
    }
    if moule == "outil-bdd":
        humain = humain or champ
        table.update(
            {
                "__CLE_LISTE__": liste,
                "__CHAMP__": champ,
                "__HUMAIN__": humain,
                "__HUMAIN_CAP__": (humain[0].upper() + humain[1:]) if humain else "",
            }
        )
    if moule == "theme-bdd":
        table["__NOM_AFFICHE__"] = nom_affiche or prefixe.upper()
    if moule == MOULE_ROUTINE:
        table.update(
            {
                "__NOM_ROUTINE__": nom,
                "__CADENCE_SECONDES__": str(int(cadence) if cadence else CADENCE_DEFAUT_ROUTINE),
                "__ROLE_ROUTINE__": role,
                "__DATE_GENERATION__": datetime.now().strftime(FORMAT_HORODATAGE_GENERATION),
            }
        )
    return table


def lire_moules(moule):
    """Retourne la liste triee des fichiers .moule du template demande (liste vide si absent)."""
    racine = REPERTOIRE_TEMPLATES / moule
    if not racine.exists():
        return []
    return sorted(chemin for chemin in racine.rglob("*" + SUFFIXE_MOULE) if chemin.is_file())


def traduire(chemin_moule, table):
    """Retourne le chemin de destination et le contenu traduit (jetons remplaces).

    Le chemin cible est relatif a la RACINE DU MOULE (le dossier direct de
    templates/, a n'importe quelle profondeur de fichier .moule).
    """
    racine_moule = chemin_moule.parent
    while racine_moule.parent.name != "templates":
        racine_moule = racine_moule.parent
    chemin_relatif = chemin_moule.relative_to(racine_moule)
    cible = Path(str(chemin_relatif)[: -len(SUFFIXE_MOULE)])
    contenu = chemin_moule.read_text(encoding="utf-8")
    for jeton, valeur in table.items():
        contenu = contenu.replace(jeton, valeur)
    return cible, contenu


def appliquer_surcharge(en_memoire, table, moule_surcharge):
    """Remplace, dans le clone EN MEMOIRE, les fichiers surcharges par le moule
    de zone (`moule_surcharge` vient de la table ZONES, jamais d un nom en dur).

    La surcharge porte UNIQUEMENT les fichiers qui changent HORS de data/ :
    constants.py (la BDD vit un niveau au-dessus de l outil) et DESCRIPTION.md.
    Un fichier de la surcharge dont la cible n existe pas dans le moule de base
    est AJOUTE ; un fichier du moule de base sans surcharge est conserve tel quel.
    """
    surcharges = {}
    for chemin in lire_moules(moule_surcharge):
        cible, contenu = traduire(chemin, table)
        surcharges[str(cible)] = contenu
    if not surcharges:
        return en_memoire
    resultat = []
    remplaces = set()
    for cible, contenu in en_memoire:
        cle = str(cible)
        if cle in surcharges:
            resultat.append((cible, surcharges[cle]))
            remplaces.add(cle)
        else:
            resultat.append((cible, contenu))
    for cle, contenu in surcharges.items():
        if cle not in remplaces:
            resultat.append((Path(cle), contenu))
    return resultat


def verifier_sources(en_memoire):
    """Verifie CHAQUE source AVANT ecriture : py_compile + ASCII + aucun jeton residuel.

    Retourne (code, messages) : code 1 si au moins un ecart (jamais d'outil a moitie livre).
    """
    messages = []
    with tempfile.TemporaryDirectory() as dossier_temp:
        for cible, contenu in en_memoire:
            if MOTIF_JETON.search(contenu):
                messages.append("jeton residuel dans " + str(cible))
                continue
            if any(octet > 127 for octet in contenu.encode("utf-8")):
                messages.append("non-ASCII dans " + str(cible))
                continue
            if cible.suffix != ".py":
                continue
            source_temp = Path(dossier_temp) / cible.name
            source_temp.write_text(contenu, encoding="utf-8", newline="\n")
            try:
                py_compile.compile(str(source_temp), doraise=True)
            except Exception as erreur:
                messages.append("py_compile echoue pour " + str(cible) + " : " + str(erreur))
    return (1 if messages else 0), messages


def verifier_outil_executable(repertoire_clone, moule):
    """Verifie le clone executable, SELON LE MOULE : le moule doit porter
    main.py.moule (controle contre le TEMPLATE, pas contre le clone), puis le
    clone doit avoir le comportement attendu.

    Un OUTIL sans argument rend sa docstring + code 2. Une ROUTINE, elle, se
    prouve par UNE PASSE (`--once`, code 0) : la lancer sans argument demarrerait
    son demon -- la verification ne le fait JAMAIS, et c'est le `--once` lui-meme
    qui doit rester sans PID (MO-053).
    """
    if not (REPERTOIRE_TEMPLATES / moule / NOM_MOULE_PRINCIPAL).exists():
        return 1, "le moule principal " + NOM_MOULE_PRINCIPAL + " est absent du template " + moule
    if moule == MOULE_ROUTINE:
        arguments, code_attendu = ["--once"], 0
    else:
        arguments, code_attendu = [], 2
    resultat = lancer_enfant(
        [sys.executable, str(repertoire_clone / "main.py")] + arguments,
        capture_output=True,
        text=True,
        check=False,
    )
    if resultat.returncode == code_attendu:
        return 0, ""
    return 1, ("le clone n'a pas le comportement attendu ("
               + (" ".join(arguments) if arguments else "sans argument")
               + " : code " + str(resultat.returncode) + ", attendu " + str(code_attendu) + ")")


def ecrire_outil(repertoire_clone, en_memoire):
    """Ecrit le clone (atomique par conception : rien n'est ecrit si les verifications ont echoue)."""
    for cible, contenu in en_memoire:
        destination = repertoire_clone / cible
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w", encoding="utf-8", newline="\n") as flux:
            flux.write(contenu)
