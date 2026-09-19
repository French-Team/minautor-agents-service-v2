"""Fonctions communes de la porte chaine-pense-bete (EO-215, MO-224).

Chaque fonction fait UNE chose (convention-architecture-outils). AUCUNE
ecriture directe ici : tout fichier est ecrit par la PORTE unique, le passage
oblige du cerveau.
"""
import json
import re
import subprocess
import sys
import unicodedata

from constants import (
    CHAMP_NEMESIS,
    CHEMIN_PORTE_ECRIRE,
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


def titre_vers_slug(titre):
    """Slug ASCII d'un titre : minuscules, tirets, jamais un mot seul."""
    normalise = unicodedata.normalize("NFKD", titre)
    texte = normalise.encode("ascii", "ignore").decode("ascii").lower()
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
    commande = [sys.executable, str(CHEMIN_PORTE_ECRIRE), "ecrire",
                "--fichier", str(chemin), "--contenu", contenu, "--mode", mode]
    resultat = subprocess.run(commande, capture_output=True, text=True)
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
