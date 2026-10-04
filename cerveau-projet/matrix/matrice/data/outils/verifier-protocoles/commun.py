"""Fonctions communes de l'outil verifier-protocoles : une seule tache chacune."""
from constants import (
    APPARTIENT_A,
    ENCODAGE,
    NOM_INDEX,
    REPERTOIRE_PROTOCOLES,
    TYPE_ATTENDU,
)

# Le jugement des citations a un DOMICILE (M-076 / EO-479) : on le consomme, on
# ne le porte pas. Le motif de citation et la zone des sources y sont deduits --
# ni l un ni l autre n est recopie ici, donc ni l un ni l autre ne peut diverger.
from jugement_citations import juger_citations


def lister_fichiers_protocoles():
    """Retourne la liste triee des fichiers de protocole (index exclu)."""
    if not REPERTOIRE_PROTOCOLES.exists():
        return []
    return sorted(
        chemin
        for chemin in REPERTOIRE_PROTOCOLES.glob("*.md")
        if chemin.name != NOM_INDEX
    )


def lire_lignes(chemin):
    """Retourne les lignes du fichier (sans fins de ligne)."""
    with open(chemin, "r", encoding=ENCODAGE) as flux:
        return flux.read().splitlines()


def detecter_non_ascii(chemin):
    """Retourne les ecarts ASCII du fichier (format fichier:ligne:colonne).

    Etancheite (decision createur, audit protections 2026-09-09) : seul le
    NOM du fichier est affiche, jamais son chemin complet (les chemins
    internes ne doivent pas fuir vers le cameleon).
    """
    ecarts = []
    for numero, ligne in enumerate(lire_lignes(chemin), 1):
        for colonne, caractere in enumerate(ligne, 1):
            if ord(caractere) > 127:
                ecarts.append(chemin.name + ":" + str(numero) + ":" + str(colonne))
    return ecarts


def extraire_frontmatter(lignes):
    """Retourne les lignes du front-matter (entre les deux ---), ou liste vide."""
    if not lignes or lignes[0].strip() != "---":
        return []
    for numero in range(1, len(lignes)):
        if lignes[numero].strip() == "---":
            return lignes[1:numero]
    return []


def verifier_frontmatter(chemin):
    """Verifie le front-matter identite (type + appartient_a). Retourne les ecarts."""
    ecarts = []
    entete = extraire_frontmatter(lire_lignes(chemin))
    if not entete:
        return ["front-matter identite absent"]
    for ligne in entete:
        contenu = ligne.strip()
        if contenu.startswith("type:") and contenu.split(":", 1)[1].strip() != TYPE_ATTENDU:
            ecarts.append("type attendu '" + TYPE_ATTENDU + "'")
        if contenu.startswith("appartient_a:") and contenu.split(":", 1)[1].strip() != APPARTIENT_A:
            ecarts.append("appartient_a non conforme au marbre (voir le front-matter attendu)")
    if not any(ligne.strip().startswith("type:") for ligne in entete):
        ecarts.append("champ 'type' absent du front-matter")
    if not any(ligne.strip().startswith("appartient_a:") for ligne in entete):
        ecarts.append("champ 'appartient_a' absent du front-matter")
    return ecarts


def verifier_index(lignes_index, fichiers_reels):
    """Compare l'index aux fichiers reels. Retourne (manquants, morts, hors_champ).

    Ce jugement n'est PLUS ici : il vit au DOMICILE UNIQUE
    `data/commun/jugement_citations.py` (EO-479), que les trois verificateurs
    d'indice consomment -- conventions, protocoles et regles.

    POURQUOI DEPLACER, ET NON AJOUTER (M-076). Ce fichier portait, jusqu au
    2026-09-30, la SEULE copie correcte de la regle : les chemins relatifs
    reconnus jusqu au bout, la zone des sources du createur exemptee et DITE
    (MO-489). Ses deux jumeaux, eux, portaient une autre copie, qui tronquait la
    citation a sa QUEUE et accusait donc une source du createur de etre un
    fichier mort -- sans remede, la porte ECRIRE refusant cette zone. Trois
    instruments de la meme maison, deux verdicts contraires sur la meme ligne.

    On ne pouvait pas ajouter une exemption aux deux jumeaux : cela aurait porte
    la regle a QUATRE endroits, et la prochaine divergence aurait ete inevitable.
    La regle ONE, elle se consomme ; elle ne se recopie pas.

    Le detail de la regle (motif, zone des sources, exemptions DITEES) est donc
    lu a son domicile : `jugement_citations.py`. Ce docstring ne le recopie pas.
    """
    return juger_citations(lignes_index, fichiers_reels, REPERTOIRE_PROTOCOLES)