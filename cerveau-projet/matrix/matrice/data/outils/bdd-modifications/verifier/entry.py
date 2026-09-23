"""Categorie verifier : integrite de la BDD, cle canonique, et auto-test.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).

DEUX controles depuis EO-363 : l'empreinte (etalon-or, la BDD n'a pas ete
modifiee hors de l'outil) ET la CLE CANONIQUE (un seul domicile de cle par
fichier). Les deux sont rendus, meme quand le premier casse : un rouge qui cache
le second coute un tour de plus.
"""
from canoniser.fonctions import comparer_recensements, recenser_modifications
from commun import (calculer_empreinte_si_existe, canoniser_cle, charger_bdd,
                    lire_empreinte)
from constants import CHEMIN_BDD
from verifier.fonctions import verifier_cles_canoniques, verifier_integrite


def executer(arguments):
    if "--auto-test" in arguments:
        return auto_test()
    empreinte_enregistree = lire_empreinte()
    empreinte_reelle = calculer_empreinte_si_existe(CHEMIN_BDD)
    succes, message = verifier_integrite(empreinte_reelle, empreinte_enregistree)
    print(message)
    ok_cles, message_cles = verifier_cles_canoniques(charger_bdd(), canoniser_cle)
    print(message_cles)
    return 0 if (succes and ok_cles) else 1


def auto_test():
    """Le cobaye MORD, le contre-temoin EPARGNE (L-032) -- sur des faits FABRIQUES.

    Aucune epreuve ne touche le disque : la cle canonique est eprouvee sur des
    chaines, et le controle sur une BDD fabriquee en memoire. Rejouable telle
    quelle : c'est la preuve, pas un recit de preuve.
    """
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    prefixee = "cerveau-projet/matrix/_operateur/optimus-prime/suivi-pilote/README.md"
    canonique = canoniser_cle(prefixee)
    controler("le cobaye MORD : la cle PREFIXEE est ramenee a sa forme relative",
              canonique == "_operateur/optimus-prime/suivi-pilote/README.md", canonique)
    controler("le contre-temoin EPARGNE : la cle canonique se rend ELLE-MEME",
              canoniser_cle(canonique) == canonique, canonique)
    seconde = "matrix/_operateur/optimus-prime/pilote/commun.py"
    controler("le cobaye MORD aussi sur l autre forme reelle de la Matrice",
              canoniser_cle(seconde) == "_operateur/optimus-prime/pilote/commun.py",
              canoniser_cle(seconde))
    fabriquee = {"fichiers": {
        prefixee: {"modifications": [{"date": "2026-09-22 00:00:00"}], "tags": []},
        canonique: {"modifications": [{"date": "2026-09-21 00:00:00"}], "tags": []},
    }}
    ok, message = verifier_cles_canoniques(fabriquee, canoniser_cle)
    controler("le controle MORD sur une cle NON canonique", not ok, message[:110])
    fabriquee["fichiers"] = {canonique: fabriquee["fichiers"][canonique]}
    ok_propre, message_propre = verifier_cles_canoniques(fabriquee, canoniser_cle)
    controler("le controle EPARGNE une BDD a cle canonique", ok_propre, message_propre[:110])

    # LE TEMOIN DE NON-PERTE (EO-363) : le nombre d'entrees ne prouve RIEN, le
    # recensement prouve tout. Le cobaye qui importe est celui qui SAUVE le
    # compte en echangeant deux entrees -- l'ancien garde (un total) l'aurait
    # laisse passer en silence.
    entrees = [{"date": "2026-09-22 00:00:00", "action": "noter", "detail": "A"},
               {"date": "2026-09-22 00:01:00", "action": "noter", "detail": "B"}]
    bdd_avant = {"fichiers": {canonique: {"modifications": list(entrees), "tags": []}}}
    meme_compte_autre_contenu = [dict(entrees[0], detail="C"), entrees[1]]
    bdd_apres = {"fichiers": {canonique: {"modifications": meme_compte_autre_contenu, "tags": []}}}
    recensement_avant = recenser_modifications(bdd_avant)
    recensement_apres = recenser_modifications(bdd_apres)
    controler("le recensement compte AUTANT d'entrees avant qu'apres (le piege est arme)",
              sum(recensement_avant.values()) == sum(recensement_apres.values()),
              str(sum(recensement_avant.values())) + " = " + str(sum(recensement_apres.values())))
    ok_perte, message_perte = comparer_recensements(recensement_avant, recensement_apres)
    controler("le cobaye MORD : a COMPTE egal, une entree CHANGEE est refusee",
              not ok_perte, message_perte[:150])
    controler("le refus NOMME l'entree protegee (il ne dit pas qu'un nombre)",
              "detail" in message_perte, message_perte[:110])
    desordonne = {"fichiers": {canonique: {"modifications": list(reversed(entrees)), "tags": []}}}
    ok_ordre, message_ordre = comparer_recensements(recensement_avant,
                                                    recenser_modifications(desordonne))
    controler("le contre-temoin EPARGNE : l ORDRE des entrees n'est pas une perte",
              ok_ordre, message_ordre[:110])
    return 0 if all(resultats) else 1
