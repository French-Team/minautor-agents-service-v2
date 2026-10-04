"""Cobaye de carte-modifier (MO-430) : le cobaye MORD, le contre-temoin EPARGNE.

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
from modifier.fonctions import changer
from carte_identite import lire_carte

BLOC = ("---\nidentite:\n  type: outil\n  appartient_a: matrice\n"
        "  commun: false\n  version: 1\n---\n")


def auto_test():
    """Une serie d epreuves : le cobaye mord, le contre-temoin epargne."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + str(detail))

    base = ZONE_FRAGMENTS / ("mo-430-cobaye-modifier-" + str(os.getpid()))
    try:
        base.mkdir(parents=True, exist_ok=True)
        cible = base / "document.md"
        appeler_porte(["ecrire", "--fichier", relatif(cible), "--mode", "creer",
                       "--contenu", BLOC + "\n# Cobaye\n\nContenu.\n"])

        code = changer({"fichier": relatif(cible), "cle": "type", "valeur": "readme"})
        carte = lire_carte(lire_texte(cible))
        controler("COBAYE : une cle PRESENTE est remplacee",
                  code == CODE_OK and carte.get("type") == "readme",
                  "code " + str(code) + " / " + str(carte))

        code = changer({"fichier": relatif(cible), "cle": "statut", "valeur": "en-cours"})
        carte = lire_carte(lire_texte(cible))
        controler("COBAYE : une cle ABSENTE est inseree (avec indentation)",
                  code == CODE_OK and carte.get("statut") == "en-cours",
                  "code " + str(code) + " / " + str(carte))
        controle = lire_texte(cible)
        controler("COBAYE : l insertion garde les cles voisines et le corps",
                  "  version: 1" in controle and "# Cobaye" in controle,
                  str(len(controle)) + " caracteres")

        code = changer({"fichier": relatif(cible), "cle": "statut", "supprimer": True})
        carte = lire_carte(lire_texte(cible))
        controler("COBAYE : --supprimer RETIRE le champ",
                  code == CODE_OK and "statut" not in carte,
                  "code " + str(code) + " / " + str(carte))

        code = changer({"fichier": relatif(cible), "cle": "type", "valeur": "type-invente"})
        carte = lire_carte(lire_texte(cible))
        controler("COBAYE : un type HORS vocabulaire est REFUSE (cible intacte)",
                  code == CODE_REFUS and carte.get("type") == "readme",
                  "code " + str(code))

        code = changer({"fichier": relatif(cible), "cle": "type", "supprimer": True})
        carte = lire_carte(lire_texte(cible))
        controler("COBAYE : retirer une cle OBLIGATOIRE est REFUSE",
                  code == CODE_REFUS and carte.get("type") == "readme",
                  "code " + str(code))

        code = changer({"fichier": relatif(cible), "cle": "stauts", "valeur": "x"})
        controler("COBAYE : une faute de frappe de CLE est NOMMEE (refus)",
                  code == CODE_REFUS, "code " + str(code))

        code = changer({"fichier": relatif(cible), "cle": "commun", "valeur": "peut-etre"})
        carte = lire_carte(lire_texte(cible))
        controler("COBAYE : une valeur fausse rend la carte non conforme -> REFUSE",
                  code == CODE_REFUS and carte.get("commun") == "false",
                  "code " + str(code))

        code = changer({"fichier": relatif(cible), "cle": "version", "valeur": "2"})
        carte = lire_carte(lire_texte(cible))
        controler("CONTRE-TEMOIN : un changement CONFORME est EPARGNE du refus",
                  code == CODE_OK and carte.get("version") == "2",
                  "code " + str(code) + " / " + str(carte))
        controler("CONTRE-TEMOIN : le bloc relisible est toujours un bloc",
                  extraire_bloc(lire_texte(cible)) is not None, "bloc present")
    finally:
        shutil.rmtree(base, ignore_errors=True)

    verts = resultats.count(True)
    print(str(verts) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1


if __name__ == "__main__":
    sys.exit(auto_test())
