"""Logique de carte-editer : remplacer la CARTE ENTIERE, PAR LA PORTE.

La conformite du nouveau bloc vient du DOMICILE partage (carte_identite
valider_carte) : les memes jugements que le garde, consommes jamais copie
(M-076).
"""
# commun D ABORD : son bloc de lancement pose data/commun (cible,
# carte_identite, ...) sur le chemin avant tout import du domicile partage.
from commun import extraire_bloc, lire_texte, poser_bloc, relatif
from constants import CODE_ECHEC, CODE_OK, CODE_REFUS, ENCODAGE, REPERTOIRE_OUTIL

from cible import resoudre
from carte_identite import lire_carte, valider_carte


def editer(options):
    """Remplace le front-matter du document par le bloc fourni -- par la porte."""
    brut = options.get("fichier")
    chemin, motif = resoudre(brut, REPERTOIRE_OUTIL)
    if chemin is None:
        print("REFUS : " + motif)
        return CODE_REFUS
    if not chemin.is_file():
        print("REFUS : ce n'est pas un fichier : " + str(chemin))
        return CODE_REFUS
    texte = lire_texte(chemin)
    ancien = extraire_bloc(texte)
    if ancien is None:
        print("REFUS : " + relatif(chemin) + " n a PAS de carte a remplacer"
              " (poser la carte d abord : carte-creer)")
        return CODE_REFUS
    brut_nouveau = options.get("nouveau-fichier")
    source, motif_source = resoudre(brut_nouveau, REPERTOIRE_OUTIL)
    if source is None:
        print("REFUS : nouveau bloc : " + motif_source)
        return CODE_REFUS
    bloc = lire_texte(source)
    if not bloc.strip():
        print("REFUS : nouveau bloc VIDE : " + relatif(source))
        return CODE_REFUS
    nouvelle_carte = lire_carte(bloc)
    if nouvelle_carte is None:
        print("REFUS : ce n'est PAS une carte : " + relatif(source)
              + " (front-matter `identite:` attendu entre deux ---)")
        return CODE_REFUS
    ecarts = valider_carte(nouvelle_carte, chemin, REPERTOIRE_OUTIL)
    if ecarts:
        print("REFUS : nouveau bloc non conforme :")
        for ecart in ecarts:
            print("  - " + ecart)
        return CODE_REFUS
    if not bloc.endswith("\n"):
        bloc = bloc + "\n"
    if bloc == ancien:
        print("RIEN A FAIRE : " + relatif(chemin) + " porte deja CE bloc")
        return CODE_OK
    code, message = poser_bloc(chemin, ancien, bloc, "editer-" + chemin.stem)
    if code != CODE_OK:
        print(str(message))
        return code
    print("CARTE REMPLACEE : " + relatif(chemin) + " (champs : "
          + ", ".join(cle for cle in nouvelle_carte) + ")")
    return CODE_OK
