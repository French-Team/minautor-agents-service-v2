"""Fonctions communes de l'outil verifier-protocoles : une seule tache chacune."""
import re

from constants import (
    APPARTIENT_A,
    ENCODAGE,
    NOM_INDEX,
    REPERTOIRE_PROTOCOLES,
    TYPE_ATTENDU,
)

MOTIF_CHEMIN_MD = re.compile(r"[A-Za-z0-9_\-./]+\.md")


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
    """Compare l'index (lignes de tableau) aux fichiers reels. Retourne (manquants, morts).

    Les citations peuvent etre des noms simples (fichiers du dossier) ou
    des chemins relatifs (vers docs/, la fiche...). Une citation est MORT
    seulement si sa cible n'existe pas (nom absent du dossier, chemin
    relatif inexistant).
    """
    citations = []
    for ligne in lignes_index:
        if ligne.strip().startswith("|"):
            citations.extend(MOTIF_CHEMIN_MD.findall(ligne))
    noms_reels = {chemin.name for chemin in fichiers_reels}
    uniques = sorted(set(citations))
    morts = []
    for citation in uniques:
        if "/" in citation:
            existe = (REPERTOIRE_PROTOCOLES / citation).exists()
        else:
            existe = citation in noms_reels
        if not existe:
            morts.append(citation)
    noms_cites = {citation.rsplit("/", 1)[-1] for citation in uniques}
    return sorted(noms_reels - noms_cites), morts
