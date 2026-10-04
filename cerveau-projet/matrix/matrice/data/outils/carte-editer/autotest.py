"""Cobaye de carte-editer (MO-430) : le cobaye MORD, le contre-temoin EPARGNE.

Tout se passe dans la ZONE JETABLE du flux (dossier de forme mo-430-), retiree
TOUJOURS, meme si une epreuve leve. L'ecriture est REELLE (la meme porte que la
vie reelle) : un controle qui n'ecrit rien ne prouve rien (L-032).
"""

import os
import shutil
import sys

# commun D ABORD : son bloc de lancement pose data/commun sur le chemin avant
# tout import du domicile partage (L-017).
from commun import appeler_porte, extraire_bloc, lire_texte, relatif
from constants import CODE_OK, CODE_REFUS, ZONE_FRAGMENTS
from editer.fonctions import editer
from carte_identite import lire_carte, valider_carte

BLOC_A = ("---\nidentite:\n  type: outil\n  appartient_a: matrice\n"
          "  commun: false\n---\n")
BLOC_B = ("---\nidentite:\n  type: readme\n  appartient_a: optimus-prime\n"
          "  commun: false\n---\n")


def auto_test():
    """Une serie d epreuves : le cobaye mord, le contre-temoin epargne."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + str(detail))

    base = ZONE_FRAGMENTS / ("mo-430-cobaye-editer-" + str(os.getpid()))
    try:
        base.mkdir(parents=True, exist_ok=True)
        cible = base / "document.md"
        appeler_porte(["ecrire", "--fichier", relatif(cible), "--mode", "creer",
                       "--contenu", BLOC_A + "\n# Cobaye\n\nContenu.\n"])
        nouveau = base / "nouveau.txt"
        appeler_porte(["ecrire", "--fichier", relatif(nouveau), "--mode", "creer",
                       "--contenu", BLOC_B])

        code = editer({"fichier": relatif(cible), "nouveau-fichier": relatif(nouveau)})
        texte = lire_texte(cible)
        carte = lire_carte(texte)
        controler("COBAYE : la carte ENTIERE est remplacee",
                  code == CODE_OK and carte is not None
                  and carte.get("type") == "readme"
                  and carte.get("appartient_a") == "optimus-prime",
                  "code " + str(code) + " / " + str(carte))
        controler("COBAYE : le corps du document est conserve",
                  "# Cobaye" in texte and "Contenu." in texte, str(len(texte)) + " caracteres")
        controler("COBAYE : le bloc remplace est BIEN le bloc B (extraire_bloc)",
                  extraire_bloc(texte) == BLOC_B, str(extraire_bloc(texte))[:60])

        refus = base / "refus.txt"
        appeler_porte(["ecrire", "--fichier", relatif(refus), "--mode", "creer",
                       "--contenu", "ceci n est pas une carte\n"])
        code = editer({"fichier": relatif(cible), "nouveau-fichier": relatif(refus)})
        controler("COBAYE : un bloc NON carte est REFUSE (cible intacte)",
                  code == CODE_REFUS and lire_carte(lire_texte(cible)).get("type") == "readme",
                  "code " + str(code))

        mechant = base / "mechant.txt"
        appeler_porte(["ecrire", "--fichier", relatif(mechant), "--mode", "creer",
                       "--contenu", "---\nidentite:\n  type: type-invente\n"
                                    "  appartient_a: matrice\n  commun: false\n---\n"])
        code = editer({"fichier": relatif(cible), "nouveau-fichier": relatif(mechant)})
        controler("COBAYE : un type HORS vocabulaire est REFUSE (cible intacte)",
                  code == CODE_REFUS and lire_carte(lire_texte(cible)).get("type") == "readme",
                  "code " + str(code))

        sans = base / "sans-carte.md"
        appeler_porte(["ecrire", "--fichier", relatif(sans), "--mode", "creer",
                       "--contenu", "# Sans carte\n"])
        code = editer({"fichier": relatif(sans), "nouveau-fichier": relatif(nouveau)})
        controler("COBAYE : un document SANS carte est REFUSE (carte-creer d abord)",
                  code == CODE_REFUS and lire_carte(lire_texte(sans)) is None,
                  "code " + str(code))

        ecarts = valider_carte(lire_carte(BLOC_B), cible, relatif(base))
        controler("CONTRE-TEMOIN : un bloc sain est EPARGNE (zero ecart)",
                  ecarts == [], str(ecarts))
    finally:
        shutil.rmtree(base, ignore_errors=True)

    verts = resultats.count(True)
    print(str(verts) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1


if __name__ == "__main__":
    sys.exit(auto_test())
