"""Fonctions communes de l'outil verifier-conventions : une seule tache chacune."""
from constants import (
    APPARTIENT_A,
    ENCODAGE,
    NOM_INDEX,
    REPERTOIRE_CONVENTIONS,
    TYPE_ATTENDU,
)

# Le jugement des citations a un DOMICILE (M-076 / EO-479) : on le consomme, on
# ne le porte pas. Ni le motif de citation, ni la zone des sources ne sont
# recopies ici -- donc aucun des deux ne peut diverger d un verificateur a l autre.
from jugement_citations import juger_citations

REPERTOIRE = REPERTOIRE_CONVENTIONS


def lister_fichiers_conventions():
    """Retourne la liste triee des fichiers de convention (index exclu)."""
    if not REPERTOIRE_CONVENTIONS.exists():
        return []
    return sorted(
        chemin
        for chemin in REPERTOIRE_CONVENTIONS.glob("*.md")
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
    `data/commun/jugement_citations.py` (EO-479), consomme par les trois
    verificateurs d'indice -- conventions, protocoles et regles.

    CE QUE PORTAIT CETTE COPIE, ET CE QU ELLE FAISAIT (mesure du 2026-09-30).
    Le motif `MOTIF_FICHIER_MD` ne captait que le NOM de fichier, jamais le
    chemin : sur une ligne de table citant `../../../docs/une-source.md`, il
    ramenait `une-source.md`, le comparait aux noms du dossier, ne le trouvait
    pas, et le rendait dans `morts` -- un ecart ACCUSE sur une cible que la porte
    ECRIRE refuse d ecrire (zone_sources.py, MO-377). Le remede n existait pas.
    Elle rendait deux listes : il n'y avait meme pas de canal pour DIRE
    l'exemption (MO-075).

    Le troisieme verificateur, `verifier-protocoles`, portait deja la regle
    correcte depuis MO-489. Trois instruments de la meme maison, deux verdicts
    contraires sur la MEME ligne. On n'a pas ajoute l'exemption ici : cela aurait
    porte la regle a quatre endroits. Elle a ete deplacee la ou elle se consomme.
    """
    return juger_citations(lignes_index, fichiers_reels, REPERTOIRE)