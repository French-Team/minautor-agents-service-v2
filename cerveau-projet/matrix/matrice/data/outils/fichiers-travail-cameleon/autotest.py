"""Cobaye de la porte des fichiers de travail du cameleon (MO-378).

Le cobaye MORD, le contre-temoin EPARGNE (L-032) -- sur un dossier JETABLE
fourni par la fabrique PARTAGEE (cobayes_jetables.fixtures), qui le retire
TOUJOURS, meme si une epreuve leve. Aucune epreuve ne touche la zone reelle.
"""

from cobayes_jetables import fixtures

from commun import elements_zone, journal_lire, mission_du_nom, nom_canonique
from constants import ACTION_CREE, ACTION_PURGE
from nommer.fonctions import nommer
from vider.fonctions import vider


def auto_test():
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    with fixtures("cobaye-fichiers-travail-cameleon-") as dossier:
        zone = dossier / "tmp-cobaye"
        zone.mkdir(parents=True, exist_ok=True)
        journal = dossier / "cobaye-journal.jsonl"

        nom, _ = nom_canonique("M-378", "bilan", "txt")
        controler("le nom canonique se compose en forme M-", nom == "m-378-bilan.txt", str(nom))
        _, refus_mission = nom_canonique("MO-378", "bilan", "txt")
        controler("une mission de forme MO- est REFUSEE (forme du cameleon)",
                  refus_mission is not None, str(refus_mission)[:70])
        _, refus_extension = nom_canonique("M-378", "bilan", "exe")
        controler("une extension hors liste est REFUSEE",
                  refus_extension is not None, str(refus_extension)[:70])
        controler("le nom canonique se RELIT en mission",
                  mission_du_nom(nom) == "m-378", str(mission_du_nom(nom)))

        controler("la zone est VIDE avant la pose",
                  not elements_zone(zone, journal), "0 element")
        code, message, _ = nommer(zone, "M-378", "bilan", "txt", "cameleon", journal)
        apres = elements_zone(zone, journal)
        controler("la pose reussit", code == 0, message)
        controler("lister VOIT le fichier pose par la porte",
                  [element["nom"] for element in apres] == ["m-378-bilan.txt"],
                  str([element["nom"] for element in apres]))
        controler("il est classe CANONIQUE et porte sa mission",
                  bool(apres) and apres[0]["classe"] == "canonique"
                  and apres[0]["mission"] == "m-378",
                  apres[0]["classe"] if apres else "")

        (zone / "paires").mkdir()
        (zone / "routeur.ancien").write_text("x", encoding="utf-8")
        classes = {element["nom"]: element["classe"] for element in elements_zone(zone, journal)}
        controler("un FICHIER pose a la main est VU comme RESIDU",
                  classes.get("routeur.ancien") == "residu", str(classes.get("routeur.ancien")))
        controler("un DOSSIER pose a la main est VU comme RESIDU",
                  classes.get("paires") == "residu", str(classes.get("paires")))
        controler("le fichier de la porte n est PAS un residu (contre-temoin)",
                  classes.get("m-378-bilan.txt") == "canonique",
                  str(classes.get("m-378-bilan.txt")))

        code, rapport = vider(zone, None, "cameleon", journal)
        restants = elements_zone(zone, journal)
        controler("vider SOLDE la zone", not restants, str(len(restants)))
        controler("vider NOMME les trois elements retires",
                  sorted(rapport["supprimes"]) == ["m-378-bilan.txt", "paires", "routeur.ancien"],
                  str(sorted(rapport["supprimes"])))
        actes = [(entree.get("action"), entree.get("nom")) for entree in journal_lire(journal)]
        controler("le journal DIT la pose",
                  (ACTION_CREE, "m-378-bilan.txt") in actes, str(actes))
        controler("le journal DIT CHAQUE purge",
                  all((ACTION_PURGE, element) in actes for element in rapport["supprimes"]),
                  str(actes))
        controler("le contre-temoin est AVEUGLE : sans la porte, aucun acte n est trace",
                  journal_lire(dossier / "cobaye-journal-absent.jsonl") == [], "0 entree")

    print("AUTO-TEST : " + str(sum(resultats)) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1
