"""Fonctions communes de la porte chaine-pense-bete (EO-215, MO-224).

Chaque fonction fait UNE chose (convention-architecture-outils). AUCUNE
ecriture directe ici : tout fichier est ecrit par la PORTE unique, le passage
oblige du cerveau.
"""


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

import json
import re
import subprocess
import sys

from constants import (
    CHAMP_NEMESIS,
    NOM_PORTE_ECRIRE,
    ENCODAGE,
    EXTENSION,
    FORMAT_NUMERO,
    MARQUEURS_NEMESIS,
    NOM_COMPTEURS,
    NOM_INDEX,
    PREFIXES,
    REPERTOIRE_DOMICILE,
    SEPARATEUR_CARTE,
)
from constants import CHAMPS_ETAPE
# EO-287 : la resolution d un outil par son NOM est PARTAGEE (un seul domicile).
from resolution_outils import chemin_outil  # noqa: E402

# LA DATE DU VERBE D EXECUTION (MO-577) : `horodater` est le format des journaux de
# la Matrice, il est CONSOMME ici et RE-EXPORTE -- jamais recopie. L import vit
# dans ce module et pas dans le consommateur parce que c est ici que le
# `sys.path` vers `data/commun` est deja pose : un import de module de la
# Matrice place plus haut echouerait, et echouerait au premier usage.
from rotation_journal import horodater  # noqa: E402,F401


def lire_texte(chemin):
    """Lecture sans exception : un document illisible n'est pas un document."""
    try:
        return chemin.read_text(encoding=ENCODAGE)
    except (OSError, UnicodeDecodeError):
        return ""


def lignes_carte(texte):
    """Lignes de la CARTE D'IDENTITE seule (entre les deux separateurs)."""
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != SEPARATEUR_CARTE:
        return []
    carte = []
    for ligne in lignes[1:]:
        if ligne.strip() == SEPARATEUR_CARTE:
            break
        carte.append(ligne)
    return carte


def valeur_carte(texte, champ):
    """Valeur d'un champ de la carte (PREMIERE occurrence), sinon chaine vide."""
    for ligne in lignes_carte(texte):
        nu = ligne.strip()
        if nu.startswith(champ):
            return nu.split(champ, 1)[1].strip()
    return ""


def poser_champ(texte, champ, valeur):
    """Pose ou remplace un champ DANS la carte -- la ou il vit, jamais ailleurs."""
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != SEPARATEUR_CARTE:
        return texte
    fin = len(lignes)
    for index in range(1, len(lignes)):
        if lignes[index].strip() == SEPARATEUR_CARTE:
            fin = index
            break
    for index in range(1, fin):
        if lignes[index].strip().startswith(champ):
            lignes[index] = "  " + champ + " " + valeur
            return "\n".join(lignes) + "\n"
    lignes.insert(fin, "  " + champ + " " + valeur)
    return "\n".join(lignes) + "\n"


def retirer_champ(texte, champ):
    """RETIRE un champ de la carte -- le retrait, que `poser_champ` n avait pas.

    LE SENS INVERSE EXISTE PARCE QUE LA CHAINE A UN ETAT D EXECUTION (MO-577). Un
    `execute` pose par erreur doit pouvoir etre defait, et le defaire doit laisser
    la carte PROPRE : un champ d etape laisse apres le retour ferait passer le
    controle des chaines (qui lit chaque champ d etape comme un identifiant).
    """
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != SEPARATEUR_CARTE:
        return texte
    fin = len(lignes)
    for index in range(1, len(lignes)):
        if lignes[index].strip() == SEPARATEUR_CARTE:
            fin = index
            break
    gardees = [ligne for ligne in lignes[1:fin] if not ligne.strip().startswith(champ)]
    return "\n".join([lignes[0]] + gardees + lignes[fin:])


def corps_du_document(texte):
    """Lignes NON VIDES du corps (apres la carte)."""
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != SEPARATEUR_CARTE:
        return [ligne for ligne in lignes if ligne.strip()]
    for index in range(1, len(lignes)):
        if lignes[index].strip() == SEPARATEUR_CARTE:
            return [ligne for ligne in lignes[index + 1:] if ligne.strip()]
    return lignes


def a_trace_nemesis(texte):
    """La trace est DECLAREE (champ de carte) ET le passage ECRIT (marqueur)."""
    if not valeur_carte(texte, CHAMP_NEMESIS):
        return False
    return any(marqueur in texte for marqueur in MARQUEURS_NEMESIS)


# LA REGLE ASCII VIT A SON DOMICILE (EO-365 / MO-466) : le NFKD + `ignore` etait une
# TROISIEME copie de la meme regle, non declaree (les deux autres : bdd-sessions/
# ajouter et suivi-optimus/vue). Ce nom CONSOMME desormais le domicile (M-076).
from texte_ascii import vers_ascii  # noqa: E402


def titre_vers_slug(titre):
    """Slug ASCII d'un titre : minuscules, tirets, jamais un mot seul."""
    texte = vers_ascii(titre).lower()
    propre = re.sub(r"[^a-z0-9]+", "-", texte).strip("-")
    return propre or "sans-titre"


def charger_compteurs():
    """Compteurs de famille du domicile (une cle par PREFIXE declare)."""
    try:
        compteurs = json.loads(lire_texte(REPERTOIRE_DOMICILE / NOM_COMPTEURS))
    except (ValueError, TypeError):
        compteurs = {}
    if not isinstance(compteurs, dict):
        compteurs = {}
    for prefixe in PREFIXES.values():
        compteurs.setdefault(prefixe, 0)
    return compteurs


def identifiant_suivant(compteurs, etape):
    """L'id suivant de la famille, SANS le poser (l'appelant enregistre)."""
    prefixe = PREFIXES[etape]
    return prefixe + "-" + FORMAT_NUMERO.format(compteurs[prefixe] + 1)


def ecrire_par_la_porte(chemin, contenu, mode):
    """Ecrit par la PORTE unique (jamais a la main). Rend (code, sortie)."""
    commande = [sys.executable, str(chemin_outil(NOM_PORTE_ECRIRE)), "ecrire",
                "--fichier", str(chemin), "--contenu", contenu, "--mode", mode]
    resultat = lancer_enfant(commande, capture_output=True, text=True)
    return resultat.returncode, (resultat.stdout or "") + (resultat.stderr or "")


def enregistrer_compteurs(compteurs):
    """Les compteurs vivent au domicile, ecrits par la porte."""
    chemin = REPERTOIRE_DOMICILE / NOM_COMPTEURS
    mode = "remplacer" if chemin.is_file() else "creer"
    contenu = json.dumps(compteurs, indent=2, sort_keys=True) + "\n"
    return ecrire_par_la_porte(chemin, contenu, mode)


def document_par_identifiant(identifiant):
    """Le document dont la CARTE declare cet id -- jamais par le nom du fichier."""
    for chemin in sorted(REPERTOIRE_DOMICILE.glob("*" + EXTENSION)):
        texte = lire_texte(chemin)
        for champ in CHAMPS_ETAPE.values():
            if valeur_carte(texte, champ) == identifiant:
                return chemin, texte
    return None, ""


def rafraichir_index(nom_document, identifiant, titre, etape):
    """L'index dit l'etape COURANTE : sinon il MENT des la premiere avancee.

    Defaut trouve par le cobaye de MO-224 : naitre inscrivait l'objet, mais
    avancer ne touchait pas la ligne -- l'index affichait [pense-bete] pour un
    document arrive a [todo]. Un index qui ment est pire qu'un index absent :
    il fait croire qu'un objet dort alors que sa matiere est prete.
    """
    index = REPERTOIRE_DOMICILE / NOM_INDEX
    texte = lire_texte(index)
    if not texte:
        return ajouter_a_index(nom_document, identifiant, titre, etape)
    ligne = "- " + identifiant + " [" + etape + "] " + titre + " -- " + nom_document
    lignes = texte.splitlines()
    prefixe = "- " + identifiant + " "
    remplace = False
    for rang, existante in enumerate(lignes):
        if existante.startswith(prefixe):
            lignes[rang] = ligne
            remplace = True
            break
    if not remplace:
        lignes.append(ligne)
    return ecrire_par_la_porte(index, chr(10).join(lignes) + chr(10), "remplacer")


def ajouter_a_index(nom_document, identifiant, titre, etape):
    """L'index du domicile dit ce qui existe : une ligne par objet."""
    ligne = "- " + identifiant + " [" + etape + "] " + titre + " -- " + nom_document
    index = REPERTOIRE_DOMICILE / NOM_INDEX
    if not index.is_file():
        entete = chr(10).join([
            SEPARATEUR_CARTE,
            "identite:",
            "  type: index",
            "  appartient_a: optimus-prime",
            "  commun: false",
            SEPARATEUR_CARTE,
            "",
            "# Index de la chaine pense-bete -> spec -> todo-list",
            "",
            "> Une ligne par objet. Pose par la porte chaine-pense-bete.",
            "",
        ]) + chr(10)
        return ecrire_par_la_porte(index, entete + ligne + chr(10), "creer")
    return ecrire_par_la_porte(index, ligne + chr(10), "ajouter")
