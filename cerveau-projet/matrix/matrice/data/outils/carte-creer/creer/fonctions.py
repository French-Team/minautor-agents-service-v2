"""Logique de carte-creer : le bloc du MODELE, la pose PAR LA PORTE.

Aucune regle de forme n'est recopiee ici : cles obligatoires, vocabulaire ferme,
separateurs interdits, forme canonique des liens viennent du DOMICILE partage
(matrice/data/commun/carte_identite.py et cible.py) -- le meme jugement que le
garde verifier-cartes-identite, consomme jamais copie (M-076).
"""
from datetime import datetime

# commun D ABORD : son bloc de lancement pose data/commun (cible,
# carte_identite, ...) sur le chemin avant tout import du domicile partage.
from commun import appeler_porte, poser_bloc, relatif
from constants import (CHOIX_MODELE_DEFAUT, CODE_ECHEC, CODE_OK, CODE_REFUS,
                       CLES_REQUISES, ENCODAGE, FORMAT_DATE, MODELE_COMPLET,
                       MODELE_MINIMAL, REPERTOIRE_OUTIL, VALEURS_DEFAUT)

from cible import resoudre
from carte_identite import lire_carte, valider_carte

COMMUN_VRAI = "true"
COMMUN_FAUX = "false"


def charger_modele(choix):
    """(texte du modele de reference, refus) -- la source des champs."""
    chemin = MODELE_COMPLET if choix == "complet" else MODELE_MINIMAL
    try:
        texte = chemin.read_text(encoding=ENCODAGE)
    except OSError as erreur:
        return "", "modele illisible : " + str(erreur)
    if lire_carte(texte) is None:
        return "", "modele illisible : aucune carte dans " + chemin.name
    return texte, None


def valeur_de(cle, options, aujourdhui):
    """Valeur d'une champ de modele : option fournie, sinon defaut declare.

    Rend None pour un champ sans valeur ici : il est OMIT du bloc et DIT a
    l'ecart, jamais rempli d un placeholder silencieux.
    """
    if cle == "type":
        return options.get("type")
    if cle == "appartient_a":
        return options.get("appartient-a")
    if cle == "date":
        return options.get("date") or aujourdhui
    if cle in ("commun", "version", "statut"):
        return options.get(cle) or VALEURS_DEFAUT[cle]
    if cle in ("liens", "tags"):
        return options.get(cle)
    return None


def construire_bloc(cles_modele, options):
    """Le front-matter, dans L'ORDRE des champs du modele (reference)."""
    aujourdhui = datetime.now().strftime(FORMAT_DATE)
    lignes = ["---", "identite:"]
    omis = []
    for cle in cles_modele:
        valeur = valeur_de(cle, options, aujourdhui)
        if valeur is None or not str(valeur).strip():
            omis.append(cle)
            continue
        lignes.append("  " + cle + ": " + str(valeur).strip())
    lignes.append("---")
    return "\n".join(lignes) + "\n", omis


def valider(texte, chemin):
    """La conformite : jugee par le DOMICILE partage, jamais par cet outil."""
    return valider_carte(lire_carte(texte), chemin, REPERTOIRE_OUTIL)


def poser(options):
    """Pose la carte en tete du document -- toute ecriture passe par la porte."""
    brut = options.get("fichier")
    chemin, motif = resoudre(brut, REPERTOIRE_OUTIL)
    if chemin is None:
        print("REFUS : " + motif)
        return CODE_REFUS
    if not chemin.is_file():
        print("REFUS : ce n'est pas un fichier : " + str(chemin))
        return CODE_REFUS
    texte = ""
    try:
        texte = chemin.read_text(encoding=ENCODAGE)
    except (OSError, UnicodeDecodeError) as erreur:
        print("REFUS : fichier illisible : " + str(erreur))
        return CODE_REFUS
    if texte.strip() and lire_carte(texte) is not None:
        print("REFUS : " + relatif(chemin) + " porte DEJA une carte "
              "(changer un champ : carte-modifier ; remplacer la carte : carte-editer)")
        return CODE_REFUS
    choix = (options.get("modele") or CHOIX_MODELE_DEFAUT).strip().lower()
    modele, refus = charger_modele(choix)
    if refus:
        print("REFUS : " + refus)
        return CODE_ECHEC
    cles_modele = list(lire_carte(modele))
    bloc, omis = construire_bloc(cles_modele, options)
    if any(cle in omis for cle in CLES_REQUISES):
        print("REFUS : champ obligatoire du modele sans valeur : "
              + ", ".join(cle for cle in CLES_REQUISES if cle in omis))
        return CODE_REFUS
    ecarts = valider(bloc, chemin)
    if ecarts:
        print("REFUS : carte non conforme :")
        for ecart in ecarts:
            print("  - " + ecart)
        return CODE_REFUS
    if not texte.strip():
        code, message = appeler_porte(["ecrire", "--fichier", relatif(chemin),
                                       "--mode", "remplacer", "--contenu", bloc])
    else:
        code, message = poser_bloc(chemin, texte, bloc + "\n" + texte,
                                   "creer-" + chemin.stem)
    if code != CODE_OK:
        print(str(message))
        return CODE_ECHEC if code == CODE_OK else code
    champs = ", ".join(cle for cle in cles_modele if cle not in omis)
    print("CARTE POSEE : " + relatif(chemin) + " (modele " + choix + " ; champs : "
          + champs + ")")
    if omis:
        print("champs du modele omis (sans valeur) : " + ", ".join(omis))
    return CODE_OK
