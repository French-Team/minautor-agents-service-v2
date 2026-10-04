"""Point d entree global de l outil inventaire-systeme.

Role : DIRIGER (parser la commande, router vers la categorie). Aucune logique
metier ici (convention-architecture-outils).

LA FICHE MACHINE (MO-251) : un seul fichier dit sur quelle machine vit la
Matrice, et une seule PORTE le tient a jour. Le fichier est la memoire DURABLE
(il survit au redemarrage) ; l injection du pilote en sert la section courte
RESUME MACHINE aux missions (entree contexte-machine du catalogue).

Usage :
    python main.py mesurer
        (mesure la machine et ECRIT la fiche matrice/data/systeme-machine.md)
    python main.py lire [--resume]
        (la fiche entiere, ou seulement la section servie a l injection)
    python main.py verifier
        (la fiche contre la machine FRAICHE, et l entree d injection declaree)

Codes : 0 = OK, 1 = ecart(s) nomme(s), 2 = refus (jamais un silence).
"""
import sys

import fiche
import mesure
import verif
from constants import TITRE_RESUME

COMMANDES = ("mesurer", "lire", "verifier")
# UN DRAPEAU EST AUSSI UNE OPTION CONNUE (contrat du domicile options.py, point 4) :
# oublier `resume` dans les noms connus le ferait refuser comme inconnue.
OPTIONS_LIRE = ("resume",)
DRAPEAUX_LIRE = ("resume",)
NOM_OUTIL = "inventaire-systeme"


def _options(arguments, noms_connus, drapeaux=()):
    """Les options par le DOMICILE partage (EO-158) : le contrat est consomme, jamais recopie."""
    from options import extraire_options
    return extraire_options(arguments, noms_connus, drapeaux=drapeaux,
                            outil=NOM_OUTIL + " -- " + " ".join(COMMANDES),
                            usage=__doc__)


def mesurer(arguments=()):
    """Mesure la machine, compose la fiche, l ecrit. Rend 0.

    AUCUNE OPTION n est declaree (T2/T4 de PB-002) : tout --xxx est donc REFUSE et
    NOMME par le domicile, AVANT toute mesure. Un verbe qui ne declare rien ne doit
    pas AVALER une option inconnue en silence (defaut mesure le 2026-09-20 :
    `inventaire-systeme mesurer --option-bidon` rendait code 0, le resultat du defaut).
    """
    _options(arguments, ())
    donnees = mesure.mesurer_tout()
    chemin = fiche.ecrire(fiche.composer(donnees))
    systeme = donnees["systeme"]
    print("Fiche machine ECRITE : " + str(chemin))
    print("  Machine : " + systeme["os"] + " " + systeme["version"]
          + " (" + systeme["arch"] + ") -- hote " + systeme["hote"])
    print("  Outils  : " + ", ".join(
        entree["nom"] + (" " + entree["version"] if entree["disponible"] else " ABSENT")
        for entree in donnees["outils"]))
    return 0


def lire(arguments):
    """Imprime la fiche, ou sa seule section servie. Rend 0, ou 2 si elle manque."""
    options = _options(arguments, OPTIONS_LIRE, DRAPEAUX_LIRE)
    texte = fiche.lire()
    if texte is None:
        print("REFUS : la fiche machine est ABSENTE (" + str(fiche.CHEMIN_FICHE)
              + ") -- le remede est `" + NOM_OUTIL + " mesurer`.")
        return 2
    if options.get("resume"):
        extrait = fiche.section(texte, TITRE_RESUME)
        if extrait is None:
            print("REFUS : la section " + TITRE_RESUME + " est ABSENTE de la fiche"
                  " -- le remede est `" + NOM_OUTIL + " mesurer` (l injection la"
                  " demande par ce nom).")
            return 2
        print(extrait)
        return 0
    print(texte)
    return 0


def verifier(arguments=()):
    """Verifie la fiche contre la machine fraiche et contre le catalogue. Rend 0, 1 ou 2.

    AUCUNE OPTION n est declaree (T2/T4 de PB-002) : tout --xxx est REFUSE et NOMME.
    """
    _options(arguments, ())
    code, ecarts = verif.verifier()
    print("== INVENTAIRE SYSTEME : verifier ==")
    print("  fiche : " + str(fiche.CHEMIN_FICHE))
    if code == 2:
        for ecart in ecarts:
            print("REFUS : " + ecart)
        return 2
    for ecart in ecarts:
        print("  ECART : " + ecart)
    if ecarts:
        print("VERDICT : " + str(len(ecarts)) + " ecart(s) -- remedes : `"
              + NOM_OUTIL + " mesurer` pour une fiche PERIMEE, et l entree"
              " `contexte-machine` du catalogue d injection (avant-mission) pour un"
              " ecart de catalogue. Une fiche perimee se lit comme un fait (L-055).")
        return 1
    print("VERDICT OK : la fiche dit la machine, la machine dit la fiche, et le"
          " catalogue d injection declare la section servie.")
    return 0


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    if arguments[0] == "mesurer":
        return mesurer(arguments[1:])
    if arguments[0] == "lire":
        return lire(arguments[1:])
    return verifier(arguments[1:])


if __name__ == "__main__":
    # Le SAC A DOS est la porte commune des outils (usage journalise dans
    # usages-outils-combos.jsonl, refus de l option en tete, enveloppe) : une porte
    # qui l oublie est MUETTE au journal -- sa mesure serait aveugle (contrat 6b).
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
