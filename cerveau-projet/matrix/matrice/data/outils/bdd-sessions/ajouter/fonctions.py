"""Fonctions simples de la categorie ajouter : une seule tache chacune."""
from datetime import datetime

from constants import PREFIXE_ENTREE

# LA REGLE ASCII VIT A SON DOMICILE (EO-365 / MO-466) : `assainir_ascii` etait la
# COPIE d une regle que suivi-optimus portait aussi (`vers_ascii`). Deux copies
# divergent en silence (L-029) : elles CONSOMMENT desormais data/commun/texte_ascii.py
# (M-076). Le NOM local est CONSERVE -- retiqueter/entry.py l importe d ici.
from texte_ascii import vers_ascii as assainir_ascii  # noqa: E402


# CONTRAT DE TRANSPORT des listes (frictions 72 et 73) : les tags voyagent joints
# par un caractere qui vit dans son DOMICILE (data/commun/transport_listes.py) --
# cette fonction le CONSOMME au lieu de le recopier, comme les dix autres portes de
# BDD (M-076 ; L-100/L-102 : une forme recopiee derive en silence).
from transport_listes import decouper_liste  # noqa: E402


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] -- le separateur vient de son domicile."""
    return decouper_liste(chaine_tags)


def prochain_id(donnees):
    """Calcule l'identifiant de la prochaine entree (compteur incremente)."""
    donnees["compteur"] = donnees.get("compteur", 0) + 1
    return PREFIXE_ENTREE + str(donnees["compteur"]).zfill(3)


def ajouter_entree(donnees, contenu, tags, source):
    """Ajoute UNE entree taguee a la liste. Ne touche a rien d'autre."""
    entree = {
        "id": prochain_id(donnees),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session": assainir_ascii(contenu),
        "tags": [assainir_ascii(t) for t in tags],
        "source": assainir_ascii(source),
    }
    donnees.setdefault("sessions", []).append(entree)
    return entree
