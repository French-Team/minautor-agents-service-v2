"""Cobaye de carte-creer (MO-430) : le cobaye MORD, le contre-temoin EPARGNE.

Tout se passe dans la ZONE JETABLE du flux (dossier de forme mo-430-), retiree
TOUJOURS, meme si une epreuve leve. L'ecriture est REELLE (la meme porte que la
vie reelle) : un controle qui n'ecrit rien ne prouve rien (L-032).
"""

import os
import shutil
import sys

# commun D ABORD : son bloc de lancement pose data/commun (carte_identite, ...)
# sur le chemin avant tout import du domicile partage (L-017).
from commun import appeler_porte, lire_texte, relatif
from constants import CODE_OK, CODE_REFUS, ZONE_FRAGMENTS
from creer.fonctions import poser, valider
from carte_identite import lire_carte


def auto_test():
    """Une serie d epreuves : le cobaye mord, le contre-temoin epargne."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + str(detail))

    base = ZONE_FRAGMENTS / ("mo-430-cobaye-creer-" + str(os.getpid()))
    try:
        base.mkdir(parents=True, exist_ok=True)
        cible = base / "document.md"
        code, message = appeler_porte(
            ["ecrire", "--fichier", relatif(cible), "--mode", "creer",
             "--contenu", "# Cobaye\n\nContenu de test.\n"]
        )
        controler("le cobaye EST cree par la porte ecrire",
                  code == CODE_OK, "code " + str(code) + " : " + str(message))

        code = poser({"fichier": relatif(cible), "type": "outil",
                      "appartient-a": "matrice"})
        texte = lire_texte(cible)
        carte = lire_carte(texte)
        controler("COBAYE : la carte est posee et relisible",
                  code == CODE_OK and carte is not None
                  and carte.get("type") == "outil",
                  "code " + str(code) + " / carte " + str(carte))
        controler("COBAYE : le contenu d origine est conserve SOUS la carte",
                  "Contenu de test." in texte, str(len(texte)) + " caracteres")

        code = poser({"fichier": relatif(cible), "type": "outil",
                      "appartient-a": "matrice"})
        controler("COBAYE : la DEUXIEME pose est REFUSEE (carte deja presente)",
                  code == CODE_REFUS, "code " + str(code))

        deuxieme = base / "deuxieme.md"
        appeler_porte(["ecrire", "--fichier", relatif(deuxieme), "--mode", "creer",
                       "--contenu", "# Deuxieme\n"])
        code = poser({"fichier": relatif(deuxieme), "type": "type-invente",
                      "appartient-a": "matrice"})
        controler("COBAYE : un type HORS vocabulaire ferme est REFUSE",
                  code == CODE_REFUS, "code " + str(code))

        code = poser({"fichier": relatif(deuxieme), "type": "outil",
                      "appartient-a": "matrice/sous-dossier"})
        controler("COBAYE : une appartenance en CHEMIN est REFUSEE",
                  code == CODE_REFUS, "code " + str(code))

        code = poser({"fichier": relatif(base / "absent.md"), "type": "outil",
                      "appartient-a": "matrice"})
        controler("COBAYE : un fichier ABSENT est REFUSE nommement",
                  code == CODE_REFUS, "code " + str(code))

        saine = ("---\nidentite:\n  type: outil\n  appartient_a: matrice\n"
                 "  commun: false\n---\n\n# Sain\n")
        ecarts = valider(saine, cible)
        controler("CONTRE-TEMOIN : une carte saine est EPARGNEE (zero ecart)",
                  ecarts == [], str(ecarts))
    finally:
        shutil.rmtree(base, ignore_errors=True)

    verts = resultats.count(True)
    print(str(verts) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1


if __name__ == "__main__":
    sys.exit(auto_test())
