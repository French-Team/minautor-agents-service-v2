"""Domicile UNIQUE du jugement des citations d index (M-076 / EO-479).

AVANT, CE JUGEGMENT VIVAIT EN TROIS COPIES. `verifier-protocoles` jugeait les
CHEMINS relatifs (MOTIF_CHEMIN_MD) et exemptees la zone des sources du createur
(MO-489) ; `verifier-conventions` et `verifier-regles` portaient MOTIF_FICHIER_MD,
dont le `findall` ne capture que la QUEUE d un chemin (`docs/une-source.md` ->
`une-source.md`) et la compare aux noms du dossier. Une ligne d index citant une
cible de `docs/` etait donc ACCUSEE MORTE par les deux jumeaux -- alors que la
porte ECRIRE, seul passage d ecriture, REFUSE cette zone en la nommant
(`zone_sources.py`, MO-377). Deux instruments de la meme maison, deux verdicts
contraires sur la meme ligne, dont un sans remede possible.

MESURE DU 2026-09-30 (avant reparation, sur une ligne de table fantome, zone
jetable puis purgee) :
  - `verifier-protocoles` : morts = [], hors_champ = ['<docs/...>.md : cible ABSENTE']
  - `verifier-conventions` : morts = ['<docs/...>.md']  <-- le rouge sans remede
  - `verifier-regles`      : idem, par le meme chemin de code

CE QUI EST DIT ICI, ET N EST PAS REINVENTE PLUS LOIN.
  - La ZONE DES SOURCES vient de son domicile `zone_sources.est_zone_sources` --
    jamais d une liste recopiee dans ce fichier (M-076 : une decision qui a un
    domicile ne se recopie pas, elle se consomme).
  - La FORME d un chemin vient de `zone_sources.chemin_canonique`.

LE CONTRAT, en trois sorties et jamais quatre :
  (manquants, morts, hors_champ)
  - `manquants` : un fichier du dossier que l index ne cite pas. ACCUSE.
  - `morts`     : une citation dont la cible n existe pas, HORS zone des sources.
                  ACCUSE. La porte ECRIRE peut la reparer : le remede existe.
  - `hors_champ`: une citation de la zone des sources. JAMAIS accusee -- elle est
                  MESUREE et DITE, avec sa cible PRESENTE ou ABSENTE. Elle ne
                  compte dans aucun verdict (MO-489) mais elle ne se TAIT pas
                  (MO-075) : une exemption muette est un angle mort.

UNE SEULE FORME DE CITATION EST RECONNUE, celle du chemin complet. Le motif
capte les segments, les points et les tirets, donc `../../../docs/x.md` sort
ENTIER et non par sa queue : c etait precisement la queue qui faisait
confondre une source du createur avec un fichier du dossier. Un nom simple
(`proto-12-loi-du-round.md`) reste un nom simple et se juge contre les noms
reels : la forme n a pas disparu, elle s applique partout.
"""
import re

from zone_sources import MOTIF_ZONE_SOURCES, est_zone_sources

# Le chemin COMPLET, segments et points compris -- c est la difference avec
# MOTIF_FICHIER_MD, qui tronquait a la queue.
MOTIF_CITATION = re.compile(r"[A-Za-z0-9_\-./]+\.md")


def juger_citations(lignes_index, fichiers_reels, repertoire):
    """Compare l index (lignes de TABLEAU) aux fichiers reels.

    Retourne (manquants, morts, hors_champ) -- trois sorties, jamais quatre.
    `repertoire` est le dossier des fichiers reels : il sert a resoudre une
    citation relative (la Matrice ecrit cote, jamais dans `docs/`).
    """
    cites = []
    for ligne in lignes_index:
        if ligne.strip().startswith("|"):
            cites.extend(MOTIF_CITATION.findall(ligne))
    noms_reels = {chemin.name for chemin in fichiers_reels}
    uniques = sorted(set(cites))

    morts = []
    hors_champ = []
    for citation in uniques:
        if "/" in citation:
            # Une citation relative se resout CONTRE LE DOSSIER, jamais contre
            # les noms : c est ce qui permet de distinguer une source du
            # createur (hors champ) d un fichier ecrivable (accusable).
            cible = repertoire / citation
            if est_zone_sources(cible):
                hors_champ.append(
                    citation + " : " + ("cible PRESENTE" if cible.exists()
                                       else "cible ABSENTE")
                )
                continue
            existe = cible.exists()
        else:
            existe = citation in noms_reels
        if not existe:
            morts.append(citation)

    noms_cites = {citation.rsplit("/", 1)[-1] for citation in uniques}
    return sorted(noms_reels - noms_cites), morts, hors_champ


def decrire_hors_champ(hors_champ):
    """Formule les faits hors champ pour l affichage. JAMAIS un ecart.

    La FORMULATION vit ici, avec la regle qu elle explique, et pas dans chacun
    des trois verificateurs : trois-tools trois formulations, c est trois verites
    sur la meme exemption. Elle rappelle pourquoi la citation n est pas comptee
    (MO-489) et pourquoi elle n est pas muette (MO-075).
    """
    return [
        fait + " -- " + MOTIF_ZONE_SOURCES + " : MESUREE, jamais accusee (la"
        " porte ECRIRE refuse cette zone : l'index ne peut pas reparer cette cible)"
        for fait in hors_champ
    ]


def afficher_dit(titre, faits):
    """Affiche un groupe DIT : ce qui est MESURE sans etre JUGE. Jamais un ecart.

    Ce groupe ne parait QUE s'il a quelque chose a dire -- un garde n'imprime pas
    une exemption vide -- mais quand il a quelque chose a dire, il le DIT : une
    exemption muette est un angle mort qu'aucune suite ne voit (doctrine des
    exemptions visibles, MO-075). Il ne retourne rien et ne compte JAMAIS dans
    le verdict (MO-489 : ce qui n'est pas de notre ressort ne fait pas un ecart,
    mais ne se tait pas non plus).

    IL EST ICI, ET NON DANS CHAQUE VERIFICATEUR (EO-479). L'affichage DIT etait
    ecrit dans le seul `verifier-protocoles` ; le porter dans les deux autres
    aurait produit TROIS copies d'une meme ligne d'affichage. C'est le meme
    defaut que le jugement lui-meme, une ligne plus haut.
    """
    if not faits:
        return
    print("DIT   " + titre)
    for fait in faits:
        print("  - " + fait)
