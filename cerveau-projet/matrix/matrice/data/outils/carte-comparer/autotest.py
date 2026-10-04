"""Cobaye de carte-comparer (MO-430) : le cobaye MORD, le contre-temoin EPARGNE.

Tout se passe dans la ZONE JETABLE du flux (dossier de forme mo-430-), retiree
TOUJOURS, meme si une epreuve leve. L outil est en LECTURE seule : le cobaye
POSE ses documents par la porte ecrire, puis comparer ne fait que les juger.
"""

import os
import shutil
import sys

# commun D ABORD : son bloc de lancement pose data/commun sur le chemin avant
# tout import du domicile partage (L-017).
from commun import lire_texte, relatif
from constants import CODE_ECHEC, CODE_OK, CODE_REFUS, ZONE_FRAGMENTS
from comparer.fonctions import comparer_corpus, comparer_fichier
from carte_identite import lire_carte, valider_carte

BLOC_CONFORME = ("---\nidentite:\n  type: outil\n  appartient_a: matrice\n"
                 "  commun: false\n  version: 1\n  date: 2026-09-26\n---\n")
BLOC_NON_CONFORME = ("---\nidentite:\n  type: type-invente\n"
                     "  appartient_a: matrice/sous-dossier\n  commun: peut-etre\n---\n")


def auto_test():
    """Une serie d epreuves : le cobaye mord, le contre-temoin epargne."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + str(detail))

    base = ZONE_FRAGMENTS / ("mo-430-cobaye-comparer-" + str(os.getpid()))
    try:
        base.mkdir(parents=True, exist_ok=True)
        bon = base / "bon.md"
        mauvais = base / "mauvais.md"
        brut = base / "sans-carte.md"
        # Le cobaye POSE ses documents en direct : la zone jetable est la sienne
        # (l outil, lui, ne ecrit JAMAIS -- c est ce que le 5e epreuve mesure).
        bon.write_text(BLOC_CONFORME + "\n# Bon\n", encoding="utf-8")
        mauvais.write_text(BLOC_NON_CONFORME + "\n# Mauvais\n", encoding="utf-8")
        brut.write_text("# Brut\n", encoding="utf-8")

        code = comparer_fichier({"fichier": relatif(bon), "modele": "complet"})
        controler("COBAYE : une carte conforme rend code 0 (CONFORME)",
                  code == CODE_OK, "code " + str(code))

        code = comparer_fichier({"fichier": relatif(mauvais), "modele": "complet"})
        controler("COBAYE : une carte non conforme rend code 1 (ecarts dits)",
                  code == CODE_ECHEC, "code " + str(code))

        code = comparer_fichier({"fichier": relatif(brut), "modele": "complet"})
        controler("COBAYE : un document SANS carte est REFUSE (carte-creer d abord)",
                  code == CODE_REFUS, "code " + str(code))

        code = comparer_corpus({"dans": relatif(base), "modele": "complet"})
        controler("COBAYE : le corpus est parcouru et ses ecarts rendus",
                  code == CODE_ECHEC, "code " + str(code))
        contenu = lire_texte(bon)
        controler("CONTRE-TEMOIN : le cobaye conforme n a RIEN change (lecture seule)",
                  contenu == BLOC_CONFORME + "\n# Bon\n", str(len(contenu)) + " caracteres")

        ecarts = valider_carte(lire_carte(BLOC_CONFORME), bon, relatif(base))
        controler("CONTRE-TEMOIN : une carte saine est EPARGNEE (zero ecart)",
                  ecarts == [], str(ecarts))
    finally:
        shutil.rmtree(base, ignore_errors=True)

    verts = resultats.count(True)
    print(str(verts) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1


if __name__ == "__main__":
    sys.exit(auto_test())
