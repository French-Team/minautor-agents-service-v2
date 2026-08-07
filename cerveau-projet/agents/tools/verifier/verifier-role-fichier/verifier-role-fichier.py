#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
verifier-role-fichier.py

Verifie qu'un fichier est utilise uniquement pour sa fonction prevue :
un index ne contient pas de suivi, une convention pas d'historique de suivi,
un protocole pas de TODO ni de statut de suivi, etc. Verifie aussi la
taille du fichier (seuil : 200 lignes).

Utilisation:
  verifier-role-fichier.py <fichier>

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

SEUIL_LIGNES = 200

# Motifs de sections interdites selon le type de fichier
SUIVI_COMMUN = r"^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire"
INDEX_INTERDIT = SUIVI_COMMUN + r"|^## .*Statut du|^## .*Corrections recentes|^## .*Notes de session|^## .*Lecons apprises"
CONVENTION_INTERDIT = SUIVI_COMMUN + r"|^## .*Historique"
PROTOCOLE_INTERDIT = SUIVI_COMMUN + r"|^## .*Statut"
HISTORIQUE_SEUL = r"^## .*Historique"
SPEC_TEMPLATE_INTERDIT = SUIVI_COMMUN


def afficher_aide():
    print("Usage: verifier-role-fichier.py <fichier>")
    print("")
    print("Verifie qu'un fichier est utilise pour sa fonction prevue.")
    print("")
    print("Exemples :")
    print("  verifier-role-fichier.py cerveau-projet/index-cerveau.md")
    print("  verifier-role-fichier.py cerveau-projet/pense-betes/index-pense-bete.md")


def trouver_ligne_suivante(lignes, index):
    """Retourne la prochaine ligne non vide apres index (base 0)."""
    for i in range(index + 1, len(lignes)):
        if lignes[i].strip():
            return lignes[i]
    return ""


def verifier_fichier(fichier):
    nom = os.path.basename(fichier)
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("[ERREUR] Impossible de lire le fichier : %s" % fichier)
        return 1

    lignes = contenu.split("\n")
    erreurs = 0

    def sections_interdites(pattern, libelle_type):
        """Trouve les sections correspondant au pattern et les signale."""
        nonlocal erreurs
        trouvailles = []
        for i, l in enumerate(lignes):
            if re.match(pattern, l):
                trouvailles.append((i, l))
        if not trouvailles:
            return
        if libelle_type in ("convention", "protocole"):
            # Certaines occurrences sont des descriptions de templates (tableaux)
            for idx, l in trouvailles[:1]:
                suivant = trouver_ligne_suivante(lignes, idx)
                if re.match(r"^\||^\[|^etat|^Type", suivant):
                    return  # C'est une definition, pas un suivi
        erreurs += 1
        print("[ERREUR] %s est un(e) %s et contient une section interdite :" % (fichier, libelle_type))
        for idx, l in trouvailles[:5]:
            print("  %d: %s" % (idx + 1, l))

    if nom.startswith("index-"):
        sections_interdites(INDEX_INTERDIT, "INDEX")
    elif nom.startswith("convention-"):
        sections_interdites(CONVENTION_INTERDIT, "CONVENTION")
    elif nom.startswith("protocole-"):
        sections_interdites(PROTOCOLE_INTERDIT, "PROTOCOLE")
        # Historique : autorise si c'est une description de template
        historiques = [(i, l) for i, l in enumerate(lignes) if re.match(HISTORIQUE_SEUL, l)]
        for idx, l in historiques[:1]:
            suivant = trouver_ligne_suivante(lignes, idx)
            if not re.match(r"^\||^\[", suivant):
                erreurs += 1
                print("[ERREUR] %s est un PROTOCOLE et contient une section interdite :" % fichier)
                print("  %d: %s" % (idx + 1, l))
    elif nom.startswith("spec-"):
        sections_interdites(SPEC_TEMPLATE_INTERDIT, "SPEC")
    elif nom.endswith("-template.md"):
        sections_interdites(SPEC_TEMPLATE_INTERDIT, "TEMPLATE")

    # Verifier la taille
    nb_lignes = len(lignes)
    if nb_lignes > SEUIL_LIGNES:
        print("[ATTENTION] %s fait %d lignes (seuil: %d)" % (fichier, nb_lignes, SEUIL_LIGNES))
        erreurs += 1

    if erreurs == 0:
        print("[OK] %s est conforme a son role" % fichier)
        return 0
    return 1


def main(argv):
    if not argv:
        afficher_aide()
        return 1

    if argv[0] in ("--aide", "--help", "-h"):
        afficher_aide()
        return 0

    if argv[0] == "--version":
        print("verifier-role-fichier v%s (%s)" % (VERSION, STATUT))
        return 0

    fichier = argv[0]
    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve : %s" % fichier)
        return 1

    return verifier_fichier(fichier)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
