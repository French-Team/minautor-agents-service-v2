"""Fonctions simples de la categorie retirer : une seule tache chacune.

POURQUOI CE VERBE (demande createur 2026-09-26) : la porte n'avait que noter /
corriger / lire / verifier / canoniser. `corriger` reattribue les TAGS (et
desormais l ACTION et le DETAIL) d'une entree EN PLACE, mais ne peut PAS faire
disparaitre une note dont l'existence meme est fautive (par exemple une
CREATION annoncee pour un fichier qui preexistait). Une note erronee restait
donc dans l'histoire et mentait. Ce verbe RETIRE une entree fautive, et le
retrait est TRACE et REVERSIBLE : l'entree retiree voyage ENTIEREMENT dans un
temoin de retrait (le champ `retraits`), donc rien n'est efface en silence
(lecon L-055 : un retrait se DIT, il ne se tait pas).

L'AMBIGUITE EST REFUSEE, jamais tranchee : deux entrees qui contiennent le meme
extrait ont la meme forme, et deviner laquelle retirer effacerait la mauvaise
ligne EN SILENCE. L'appelant desambigue avec --index. La regle de choix vit dans
son domicile (corriger.fonctions.choisir_position) et elle est CONSOMMEE ici,
jamais recopiee (M-076 ; L-029 : une regle recopiee derive en silence).
"""
from datetime import datetime

# LE NOM DU CHAMP DE RETRAIT vit ICI et est relu par l'auto-test : une seule
# forme, ecrite et lue au meme endroit (M-076).
CHAMP_RETRAITS = "retraits"


def retirer_entree(fiche, position, motif=""):
    """Retire UNE entree de la fiche et trace le retrait. Retourne (code, message).

    L'entree retiree n'est PAS perdue : elle est recopiee ENTIEREMENT dans
    `retraits` (date, action, detail, tags, empreinte), avec la date du retrait
    et son motif. Un retrait sans temoin serait un effacement (L-055), et un
    effacement ne se repare pas.
    """
    entrees = fiche.get("modifications", [])
    if position < 0 or position >= len(entrees):
        return 2, "Position hors plage : " + str(position) + "."
    entree = entrees[position]
    retiree = dict(entree)
    del entrees[position]
    fiche.setdefault(CHAMP_RETRAITS, []).append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "motif": motif,
        "entree": retiree,
    })
    return 0, ("Entree " + str(position + 1) + " du " + str(entree.get("date", "?"))
               + " (action " + str(entree.get("action", "?")) + ") RETIREE et tracee dans "
               + CHAMP_RETRAITS + " (reversible)"
               + (" ; motif : " + motif if motif else "") + ".")
