"""texte_ascii -- le DOMICILE de la conversion en ASCII (EO-365 / MO-466).

POURQUOI CE FICHIER EXISTE. La MEME regle -- decomposer NFKD, puis encoder ASCII
avec `errors=ignore` -- vivait en DEUX exemplaires recopies, sans domicile partage :
  - assainir_ascii (data/outils/bdd-sessions/ajouter/fonctions.py) ;
  - vers_ascii     (data/outils/suivi-optimus/vue/fonctions.py).
Deux copies d une meme regle divergent en silence (L-029) : le jour ou l une
apprend un cas (une ligature, un tiret typographique), l autre l ignore. Elles
CONSOMMENT desormais ce domicile (M-076), comme les dix autres portes de BDD
consomment deja transport_listes.

OU L ASCII EST OBLIGATOIRE, OU IL EST SEULEMENT SOUHAITE (la question d EO-365,
tranchee ici).
  - OBLIGATOIRE pour une CLE : un TAG de BDD se CHERCHE, donc il se normalise a
    l ECRITURE (bdd-modifications noter) COMME a la RECHERCHE (lire). Mesure du
    2026-09-22 : 1 seul tag non-ASCII dans toute la BDD, ecrit par l operateur --
    il etait INTOUVRABLE par une recherche sur son propre nom.
  - SOUHAITE pour le TEXTE LIBRE : le detail d une note, le contenu d une session,
    la source. Le projet les ecrit deja en ASCII strict par la porte ECRIRE ; les
    normaliser une SECONDE fois reecrirait des notes accentuees deja ecrites sans
    rien gagner a la lecture (le JSON echange les accents en echappement de toute
    facon).
"""
import unicodedata


def vers_ascii(texte):
    """Ramene <texte> a l ASCII pur. None reste None (jamais la chaine 'None').

    NFKD decompose les accents (e-acute -> e + accent) ; l encodage ASCII avec
    `errors=ignore` rejette ce qui reste (mojibake, emojis, symboles). Mesure du
    2026-09-14 (MO-092) : un appelant Windows a envoye des accents mutiles (U+FFFD
    via le codec console) et la BDD a stocke du mojibake -- la porte NE FAIT PAS
    CONFIANCE a l appelant.
    """
    if texte is None:
        return None
    decompose = unicodedata.normalize("NFKD", str(texte))
    return decompose.encode("ascii", errors="ignore").decode("ascii")
