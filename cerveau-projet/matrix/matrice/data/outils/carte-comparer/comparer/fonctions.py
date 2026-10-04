"""Logique de carte-comparer : presence des champs du MODELE, conformite.

LA REFERENCE est le modele de reference (decision createur MO-430) : ses
cles donnent les champs a presence. La CONFORMITE vient du DOMICILE partage
(carte_identite valider_carte) : les memes jugements que le garde, consommes
jamais copie (M-076). L outil ne change rien : il REND un rapport.
"""
# commun D ABORD : son bloc de lancement pose data/commun (cible,
# carte_identite, ...) sur le chemin avant tout import du domicile partage.
from commun import lire_texte, relatif
from constants import (CODE_ECHEC, CODE_OK, CODE_REFUS, DOSSIERS_IGNORES,
                       EXTENSIONS_CORPUS, LIMITE_LIGNES, MODELE_COMPLET,
                       MODELE_MINIMAL, MOTIF_POINT_RESTAURATION,
                       RACINE_MATRICE, REPERTOIRE_OUTIL)

from cible import resoudre
from carte_identite import lire_carte, valider_carte


def charger_modele(choix):
    """(cles du modele dans leur ordre, refus) : la REFERENCE des champs."""
    chemin = MODELE_COMPLET if choix == "complet" else MODELE_MINIMAL
    texte = lire_texte(chemin)
    carte = lire_carte(texte)
    if carte is None:
        return [], "modele illisible : " + str(chemin)
    return list(carte), None


def presence(carte, cles_modele):
    """(presentes, absentes) : quels champs du modele la carte porte-t-elle ?"""
    presentes, absentes = [], []
    for cle in cles_modele:
        if str(carte.get(cle, "")).strip():
            presentes.append(cle)
        else:
            absentes.append(cle)
    return presentes, absentes


def comparer_fichier(options):
    """Le rapport d UNE carte face au modele : presence des champs, conformite."""
    brut = options.get("fichier")
    chemin, motif = resoudre(brut, REPERTOIRE_OUTIL)
    if chemin is None:
        print("REFUS : " + motif)
        return CODE_REFUS
    if not chemin.is_file():
        print("REFUS : ce n'est pas un fichier : " + str(chemin))
        return CODE_REFUS
    texte = lire_texte(chemin)
    carte = lire_carte(texte)
    if carte is None:
        print("REFUS : " + relatif(chemin) + " n a PAS de carte a comparer"
              " (poser la carte d abord : carte-creer)")
        return CODE_REFUS
    cles_modele, refus = charger_modele(options.get("modele", "complet"))
    if refus:
        print("REFUS : " + refus)
        return CODE_ECHEC
    presentes, absentes = presence(carte, cles_modele)
    ecarts = valider_carte(carte, chemin, REPERTOIRE_OUTIL)
    print("CARTE : " + relatif(chemin) + " (modele " + options.get("modele", "complet") + ")")
    print("  champs presents (" + str(len(presentes)) + "/" + str(len(cles_modele))
          + ") : " + (", ".join(presentes) if presentes else "aucun"))
    if absentes:
        print("  champs absents du modele : " + ", ".join(absentes))
    if ecarts:
        print("  conformite : " + str(len(ecarts)) + " ecart(s) -- NON CONFORME")
        for ecart in ecarts:
            print("    - " + ecart)
        return CODE_ECHEC
    print("  conformite : CONFORME (zero ecart)")
    return CODE_OK


def documents_du_corpus(base):
    """Les documents du perimetre, sans le bruit (caches, .bak, zones techniques)."""
    trouves = []
    for extension in EXTENSIONS_CORPUS:
        for chemin in sorted(base.rglob("*" + extension)):
            # Les exclusions se jugent SOUS la base : la base elle-meme peut
            # vivre dans une zone technique (zone de cobaye, par exemple).
            sous_base = chemin.relative_to(base).parts
            if any(dossier in sous_base for dossier in DOSSIERS_IGNORES):
                continue
            if MOTIF_POINT_RESTAURATION in chemin.name:
                continue
            if not chemin.is_file():
                continue
            trouves.append(chemin)
    return trouves


def comparer_corpus(options):
    """Le rapport du CORPUS : presence par champ, conformite carte par carte."""
    brut = options.get("dans") or str(RACINE_MATRICE)
    base, motif = resoudre(brut, REPERTOIRE_OUTIL)
    if base is None:
        print("REFUS : perimetre : " + motif)
        return CODE_REFUS
    if not base.is_dir():
        print("REFUS : --dans doit nommer un DOSSIER : " + str(base))
        return CODE_REFUS
    cles_modele, refus = charger_modele(options.get("modele", "complet"))
    if refus:
        print("REFUS : " + refus)
        return CODE_ECHEC
    fichiers = documents_du_corpus(base)
    if not fichiers:
        print("REFUS : aucun document sous " + str(base))
        return CODE_REFUS
    sans_carte = []
    ecarts_total = []
    presents = dict.fromkeys(cles_modele, 0)
    avec_carte = 0
    for chemin in fichiers:
        carte = lire_carte(lire_texte(chemin))
        if carte is None:
            sans_carte.append(relatif(chemin))
            continue
        avec_carte += 1
        presentes, _absentes = presence(carte, cles_modele)
        for cle in presentes:
            presents[cle] += 1
        for ecart in valider_carte(carte, chemin, REPERTOIRE_OUTIL):
            ecarts_total.append(relatif(chemin) + " : " + ecart)
    print("CORPUS : " + relatif(base) + " -- " + str(len(fichiers)) + " document(s), "
          + str(avec_carte) + " avec carte, " + str(len(sans_carte)) + " sans carte")
    print("  presence des champs du modele (sur " + str(avec_carte) + " carte(s)) :")
    for cle in cles_modele:
        print("    " + cle + " : " + str(presents[cle]) + "/" + str(avec_carte))
    if sans_carte:
        print("  sans carte (" + str(len(sans_carte)) + ") : "
              + ", ".join(sans_carte[:LIMITE_LIGNES])
              + (" ..." if len(sans_carte) > LIMITE_LIGNES else ""))
    if ecarts_total:
        print("  conformite : " + str(len(ecarts_total)) + " ecart(s) -- NON CONFORME")
        for ecart in ecarts_total[:LIMITE_LIGNES]:
            print("    - " + ecart)
        if len(ecarts_total) > LIMITE_LIGNES:
            print("    ... " + str(len(ecarts_total) - LIMITE_LIGNES) + " autre(s)")
        return CODE_ECHEC
    print("  conformite : " + str(avec_carte) + " carte(s) CONFORME (zero ecart)")
    return CODE_OK
