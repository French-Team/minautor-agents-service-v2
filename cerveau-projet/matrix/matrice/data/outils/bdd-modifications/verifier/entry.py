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
from cible import niveau_de_chemin
from constants import CHEMIN_BDD
from verifier.fonctions import (verifier_cles_anchorables,
                                verifier_cles_canoniques, verifier_integrite)


def executer(arguments):
    if "--auto-test" in arguments:
        return auto_test()
    empreinte_enregistree = lire_empreinte()
    empreinte_reelle = calculer_empreinte_si_existe(CHEMIN_BDD)
    succes, message = verifier_integrite(empreinte_reelle, empreinte_enregistree)
    print(message)
    donnees = charger_bdd()
    ok_cles, message_cles = verifier_cles_canoniques(donnees, canoniser_cle)
    print(message_cles)
    # L ANCRAGE (MO-577) : la FORME peut etre juste et le fichier absent.
    # On rend ce controle meme quand la forme casse -- un rouge qui cache le
    # rouge suivant coute un tour de plus.
    def designer(cle):
        return niveau_de_chemin(cle, CHEMIN_BDD)[0]
    ok_ancre, message_ancre = verifier_cles_anchorables(donnees, designer)
    print(message_ancre)
    return 0 if (succes and ok_cles and ok_ancre) else 1


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

    # L ANCRAGE (MO-577) : le trou que la FORME ne voit pas. Le cobaye est une
    # cle CANONIQUE qui ne designe rien -- elle passe donc le controle de forme,
    # et c est precisement ce qui rend l autre controle necessaire.
    def designer_rien(_cle):
        return None
    def designer_tout(cle):
        return cle
    orphelines = {"fichiers": {canonique: {"modifications": [], "tags": []}}}
    ok_orph, message_orph = verifier_cles_anchorables(orphelines, designer_rien)
    controler("le controle d ANCRAGE MORD sur une cle qui ne designe rien",
              not ok_orph, message_orph[:110])
    ok_anc, message_anc = verifier_cles_anchorables(orphelines, designer_tout)
    controler("le contre-temoin EPARGNE une BDD entierement ancree",
              ok_anc, message_anc[:110])
    # LE CONTRE-TEMOIN DU CONTRE-TEMOIN : une cle FAUSSE mais designee ne doit
    # pas etre accusee d ancrage -- c est le controle de FORME qui la prend.
    faux_mais_ancres = {"fichiers": {"cle-qui-nexiste-pas.md": {"modifications": [], "tags": []}}}
    ok_faux, _ = verifier_cles_anchorables(faux_mais_ancres, designer_tout)
    controler("l ancrage ne se Melange pas avec la FORME", ok_faux,
              "une cle fausse mais designee est du ressort de la forme, pas de l ancrage")

    # LE SOLDER (MO-577) : une entree soldee reste une entree. Sans ce temoin,
    # solder criait 249 entrees perdues au premier essai -- et il avait raison.
    from canoniser.ossuaires import solder_les_orphelines
    portees = [{"date": "2026-09-22 00:00:00", "action": "noter", "detail": "X"}]
    bdd_soldee = {"fichiers": {"matrice/data/lecons.json": {"modifications": portees, "tags": ["t"]}}}
    rapport, avant_s, apres_s = solder_les_orphelines(bdd_soldee, designer_rien, "test")
    controler("le solder MORD sur une cle qui ne designe rien",
              len(rapport) == 1, str(rapport[:1]))
    controler("le solder NE PERD AUCUNE entree (elles changent de tiroir)",
              avant_s == apres_s and sum(apres_s.values()) == 1,
              str(sum(apres_s.values())) + " entree(s) apres le solder")
    controler("le solder est REVERSIBLE : la fiche porte cle, entrees et motif",
              bool(bdd_soldee.get("ossuaires"))
              and "cle" in bdd_soldee["ossuaires"][0]
              and "motif" in bdd_soldee["ossuaires"][0],
              "champ ossuaires = " + str(len(bdd_soldee.get("ossuaires", []))))

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
    # LE VERBE retirer + LA CORRECTION DE L ACTION (demande createur 2026-09-26).
    # Cobaye : une fiche porte une note ERRONEE ; on la RETIRE -> elle quitte les
    # modifications ET survit ENTIERE dans `retraits` (le retrait est reversible).
    # Contre-temoin : une fiche SAINE dont aucun extrait ne correspond n est PAS
    # touchee -- c est choisir_position qui refuse AVANT tout retrait.
    from corriger.fonctions import choisir_position, corriger_entree
    from retirer.fonctions import CHAMP_RETRAITS, retirer_entree
    fiche_ret = {"modifications": [
        {"date": "2026-09-26 00:00:00", "action": "cree", "detail": "NOTE ERRONEE", "tags": ["a"]},
        {"date": "2026-09-26 00:01:00", "action": "modifie", "detail": "NOTE JUSTE", "tags": ["b"]},
    ], "tags": ["a", "b"]}
    code_ret, message_ret = retirer_entree(fiche_ret, 0, "note erronee")
    controler("le cobaye MORD : la note fautive quitte les modifications",
              code_ret == 0 and len(fiche_ret["modifications"]) == 1
              and fiche_ret["modifications"][0]["detail"] == "NOTE JUSTE", message_ret[:120])
    controler("le retrait n efface RIEN : la note survit ENTIERE dans les retraits (reversible)",
              len(fiche_ret.get(CHAMP_RETRAITS, [])) == 1
              and fiche_ret[CHAMP_RETRAITS][0]["entree"]["detail"] == "NOTE ERRONEE", "")
    controler("le retrait NOMME la note (action comprise)",
              fiche_ret[CHAMP_RETRAITS][0]["entree"].get("action") == "cree", "")
    saine = {"modifications": [{"date": "2026-09-26 00:02:00", "action": "modifie",
                                "detail": "SANS RAPPORT"}]}
    positions_absentes = [i for i, e in enumerate(saine["modifications"])
                          if "NOTE ERRONEE" in e.get("detail", "")]
    controler("le contre-temoin EPARGNE : aucun extrait ne correspond -> aucun retrait",
              positions_absentes == [] and len(saine["modifications"]) == 1, "")
    code_amb, _, message_amb = choisir_position([0, 1], "X", "")
    controler("l ambiguite est REFUSEE (deux candidats -> --index exige)",
              code_amb == 2, message_amb[:110])
    fiche_cor = {"modifications": [{"date": "2026-09-26 00:03:00", "action": "cree",
                                    "detail": "D", "tags": ["x"]}]}
    code_cor, message_cor = corriger_entree(fiche_cor, 0, [], "motif", "corrige")
    controler("le cobaye MORD : l ACTION d une note se corrige SANS toucher ses tags",
              code_cor == 0 and fiche_cor["modifications"][0]["action"] == "corrige"
              and fiche_cor["modifications"][0]["tags"] == ["x"], message_cor[:120])
    code_rien, _ = corriger_entree(fiche_cor, 0, [], "", "corrige")
    controler("le contre-temoin EPARGNE : une correction sans changement n ecrit rien",
              code_rien == 1, "")
    return 0 if all(resultats) else 1
