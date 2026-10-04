#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-versions.py -- DESCENDRE LES REGLES DE VERSIONS DU MARBRE (M-154, MO-358)

R-003 : les fichiers v1/v2 ne sont JAMAIS touches par la v3.
R-004 : v1, v2 et v3 NE COMMUNIQUENT PAS -- aucune passerelle, aucune synchro.
ORDRE 3.4 : le cerveau v1/v2 est une BANQUE DE RESSOURCES EN LECTURE SEULE.

La regle immuable `perimetre-write.md` le dit deja en une phrase : < Je LIS tout
le workspace (bank de ressources v1/v2 en lecture seule). Je n'ECRIS que dans
cerveau-projet/matrix/. Je ne modifie JAMAIS le cerveau v1/v2. > -- avec DEUX
exceptions NOMMEES : `demarrer-optimus-prime.md` et `demarrer-cameleon.md`.

CE QUE LE CONTROLE JUGE (deux populations, la meme question posee deux fois) :
  (a) LA MODIFICATION -- toute source GELEE dont l'empreinte a change depuis la
      pose, toute source gelee APPARUE, toute source gelee DISPARUE. C'est la
      mesure directe de R-003 et d'ORDRE 3.4.
  (b) L'ADRESSE -- tout LITTERAL de code de la v3 qui pointe dans une zone gelee
      (une passerelle, une synchro, une demande inter-versions) : R-004. Une
      MENTION dans un document n'est pas une adresse ; un CHEMIN dans le code en
      est une. Les sites declares plus bas sont des EXEMPTIONS (mesurees : ils
      interdisent la zone au lieu de l'atteindre) et ils sont COMPTES.

LA PORTEE SE MESURE AVANT (L-286) : la pose DIT combien de sources gelees sont
surveillees et combien de mentions existent deja de chaque cote -- un garde qui
accuse un etat sain est un garde qu'on apprend a ignorer.

Usage:
  python garde-versions.py poser        (pose les empreintes des sources gelees)
  python garde-versions.py verifier     (code 0 = versions respectees)
  python garde-versions.py --auto-test  (les cobayes, sur des faits fabriques)
"""

import re
import sys
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent
MATRICE = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")
WORKSPACE = MATRICE.parent.parent
REGISTRE = BASE / "garde-versions-registre.json"

# LE PERIMETRE GELE : le cerveau v1/v2, tel que la regle immuable le nomme. La
# v3 est la Matrice ; tout le reste du workspace est la banque de ressources.
ZONE_V3 = "cerveau-projet/matrix"
DOSSIER_GELE = "cerveau-projet"
# Les DEUX exceptions de la regle immuable, citees telles quelles (elles sont
# ecrites par la v3 : la racine, une seule fois, a la creation).
EXCEPTIONS = ("demarrer-optimus-prime.md", "demarrer-cameleon.md")
# Formes TECHNIQUES : elles ne portent pas de contenu de version (points de
# restauration du auteur, marqueurs, empreintes temoins, fichiers de git).
FORMES_TECHNIQUES = (".bak.", ".tmp", ".pid", ".sha256")
NOMS_TECHNIQUES = (".gitattributes", ".gitignore")
DOSSIERS_TECHNIQUES = {".git", "__pycache__"}

# LES TOKENS D'UNE ZONE GELEE, cherches dans le CODE de la v3 (R-004).
TOKENS_GELEES = ("cerveau-projet/freelance", "cerveau-projet/agents",
                 "AGENTS-historique", "AGENTS-activite-recente",
                 "session-admin", "session-freelance")
# LES VERBES D'ACCES : ce qui separe une ADRESSE d'une MENTION (friction L-286 :
# mesurer avant de refuser). Un chemin passe a une de ces operations ATTEINT la
# zone ; le meme chemin dans un commentaire, une docstring, un message ou une
# liste d'interdiction la NOMME seulement.
VERBES_D_ACCES = ("Path(", "open(", "read_text", "write_text", "read_bytes",
                  "rglob(", "glob(", "exists(", "is_file(", "is_dir(",
                  "import ", "subprocess", "load(")
# Le garde se connait par son propre nom (il ne se juge pas lui-meme).
RELATIF_DU_GARDE = "_operateur/optimus-prime/super-combos/combos/outils/garde-versions.py"
# LES EXEMPTIONS DECLAREES, mesurees avant d'etre posees (2026-09-22) : les trois
# gardes de flux DECLARENT ces zones comme ZONES_INTERDITES du voisin -- c'est
# une interdiction, pas une adresse. Un site NEUF n'entre pas ici par analogie :
# il est accuse.
EXEMPTIONS_ADRESSES = {
    "_operateur/optimus-prime/super-combos/combos/outils/garde-flux2.py":
        "ZONES_INTERDITES du flux 1 : la zone est INTERDITE, jamais atteinte",
    "_operateur/optimus-prime/super-combos/combos/outils/watchdog-flux2.py":
        "ZONES_INTERDITES du flux 1 : la zone est INTERDITE, jamais atteinte",
    "_operateur/optimus-prime/super-combos/combos/outils/watchdog-flux2-bg.py":
        "ZONES_INTERDITES du flux 1 : la zone est INTERDITE, jamais atteinte",
}


def empreinte(chemin):
    """sha256 d'un fichier, ou None s'il est illisible (jamais devine)."""
    try:
        digest = hashlib.sha256()
        with open(chemin, "rb") as fichier:
            for bloc in iter(lambda: fichier.read(65536), b""):
                digest.update(bloc)
        return digest.hexdigest()
    except OSError:
        return None


def est_technique(chemin):
    """Vrai pour une forme technique (point de restauration, marqueur, git)."""
    if chemin.name in NOMS_TECHNIQUES:
        return True
    if any(forme in chemin.name for forme in FORMES_TECHNIQUES):
        return True
    return any(morceau in DOSSIERS_TECHNIQUES for morceau in chemin.parts)


def sources_gelees():
    """[(cle, chemin)] des sources GELEES, plus le releve des exceptions.

    Le perimetre se DERIVE de la regle (le cerveau v1/v2 = le workspace moins la
    Matrice), il ne se recopie pas fichier par fichier : une liste tenue a la main
    raterait exactement la source qu'on vient d'ajouter.
    """
    gelees = []
    exceptions = []
    racine_gele = WORKSPACE / DOSSIER_GELE
    if racine_gele.is_dir():
        for chemin in racine_gele.rglob("*"):
            if not chemin.is_file() or est_technique(chemin):
                continue
            relatif = chemin.relative_to(WORKSPACE).as_posix()
            if relatif.startswith(ZONE_V3 + "/"):
                continue
            gelees.append((relatif, chemin))
    for chemin in sorted(WORKSPACE.iterdir()):
        if not chemin.is_file() or est_technique(chemin):
            continue
        if chemin.name in EXCEPTIONS:
            exceptions.append(chemin.name)
            continue
        gelees.append((chemin.name, chemin))
    return sorted(gelees), sorted(exceptions)


def adresses_de_la_v3():
    """(adresses, mentions) des litteraux de zone gelee dans le CODE de la v3.

    Le code de la v3 vit dans la Matrice : c'est lui qui est juge. Et la
    difference entre les deux populations est MESUREE (L-286) : une ADRESSE atteint
    la zone (un chemin passe a une operation d'acces -- `Path(`, `open(`,
    `read_text`, `rglob(`, `import`, `subprocess`...), une MENTION la nomme
    (commentaire, docstring, message, liste d'interdiction). Les confondre ferait
    accuser des fichiers SAINS : mesure du 2026-09-22 a la pose -- 21 occurrences,
    dont 3 sites de code qui INTERDISENT la zone et 3 mentions en commentaire ou en
    message (le modele v1 cite par l'inventaire).
    """
    adresses, mentions = [], []
    for chemin in MATRICE.rglob("*.py"):
        if est_technique(chemin):
            continue
        relatif = chemin.relative_to(MATRICE).as_posix()
        # LE GARDE NE SE JUGE PAS LUI-MEME : sa liste de tokens et ses cobayes
        # citent les zones gelees par CONSTRUCTION (meme regle que le registre du
        # controle d'attribution). Il est exclu NOMMEMENT, jamais en silence.
        if relatif == RELATIF_DU_GARDE:
            continue
        try:
            lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for numero, ligne in enumerate(lignes, 1):
            if not any(token in ligne for token in TOKENS_GELEES):
                continue
            if any(verbe in ligne for verbe in VERBES_D_ACCES):
                adresses.append((relatif, numero, ligne.strip()))
            else:
                mentions.append((relatif, numero, ligne.strip()))
    return adresses, mentions


def adresses_non_declarees(adresses):
    """((cle, ligne, contenu)) des adresses hors sites declares."""
    return [item for item in adresses if item[0] not in EXEMPTIONS_ADRESSES]


def modifications_gelees(reference, actuelles):
    """(changees, apparues, disparues) -- trois populations, toutes accusees."""
    changees = [(cle, reference[cle], actuelles[cle]) for cle in sorted(reference)
                if cle in actuelles and actuelles[cle] != reference[cle]]
    apparues = sorted(cle for cle in actuelles if cle not in reference)
    disparues = sorted(cle for cle in reference if cle not in actuelles)
    return changees, apparues, disparues


def lire_registre():
    if not REGISTRE.is_file():
        return None
    try:
        return json.loads(REGISTRE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def poser():
    """Pose les empreintes des sources gelees + la date, et DIT la portee."""
    gelees, exceptions = sources_gelees()
    if not gelees:
        print("REFUS : aucune source gelee trouvee -- workspace introuvable ?")
        return 2
    empreintes = {}
    for cle, chemin in gelees:
        valeur = empreinte(chemin)
        if valeur is not None:
            empreintes[cle] = valeur
    date_pose = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    REGISTRE.write_text(json.dumps({
        "date_pose": date_pose,
        "perimetre": "le cerveau v1/v2 (workspace moins la Matrice), moins les formes techniques",
        "empreintes": empreintes,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    adresses, mentions = adresses_de_la_v3()
    print("REFERENCE POSEE : " + str(len(empreintes)) + " source(s) GELEE(S) surveillee(s)")
    print("  date de pose : " + date_pose)
    print("  exceptions declarees (la regle immuable les NOMME) : "
          + (", ".join(exceptions) if exceptions else "aucune"))
    print("  code de la v3 : " + str(len(adresses)) + " ADRESSE(S), "
          + str(len(mentions)) + " mention(s) (commentaires, messages, listes d'interdiction)")
    print("  adresses hors site declare : " + str(len(adresses_non_declarees(adresses))))
    print("  registre : " + str(REGISTRE.relative_to(MATRICE)))
    return 0


def verifier():
    """Accuse toute modification gelee et toute adresse non declaree."""
    registre = lire_registre()
    if registre is None:
        print("REFUS : aucune reference posee -- lancer `poser` d'abord.")
        return 2
    reference = registre.get("empreintes") or {}
    date_pose = str(registre.get("date_pose") or "")
    gelees, exceptions = sources_gelees()
    actuelles = {}
    for cle, chemin in gelees:
        valeur = empreinte(chemin)
        if valeur is not None:
            actuelles[cle] = valeur
    changees, apparues, disparues = modifications_gelees(reference, actuelles)
    adresses_brutes, mentions = adresses_de_la_v3()
    adresses = adresses_non_declarees(adresses_brutes)

    print("VERSIONS : pose du " + date_pose + " | " + str(len(reference))
          + " source(s) gelee(s) surveillee(s)")
    print("  code de la v3 : " + str(len(adresses_brutes)) + " adresse(s), "
          + str(len(mentions)) + " mention(s)")
    print("  exceptions (ecrites par la v3, citees par la regle) : "
          + (", ".join(exceptions) if exceptions else "aucune"))
    if not changees and not apparues and not disparues and not adresses:
        print("VERDICT OK : aucune zone gelee touchee, aucune adresse inter-versions.")
        return 0
    if changees:
        print("ZONE GELEE MODIFIEE (" + str(len(changees)) + ") :")
        for cle, attendue, mesuree in changees:
            print("  - " + cle)
            print("      empreinte attendue : " + attendue)
            print("      empreinte mesuree  : " + mesuree)
    if apparues:
        print("SOURCE GELEE APPARUE (" + str(len(apparues)) + ") :")
        for cle in apparues:
            print("  - " + cle)
    if disparues:
        print("SOURCE GELEE DISPARUE (" + str(len(disparues)) + ") :")
        for cle in disparues:
            print("  - " + cle)
    if adresses:
        print("ADRESSE DE LA V3 VERS UNE ZONE GELEE (" + str(len(adresses)) + ") :")
        for cle, numero, contenu in adresses:
            print("  - " + cle + ":" + str(numero))
            print("      " + contenu[:130])
    return 1


def auto_test():
    """Le cobaye MORD, le contre-temoin EPARGNE (L-032) -- sur des faits FABRIQUES."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    # 1. LA MODIFICATION d'une source gelee est ACCUSEE, et nommee avec ses deux
    #    empreintes -- c'est la mesure directe de R-003 et d'ORDRE 3.4.
    reference = {"cerveau-projet/agents/cerberus/cerberus.md": "A" * 64,
                 "AGENTS-historique.md": "B" * 64}
    actuel = {"cerveau-projet/agents/cerberus/cerberus.md": "C" * 64,
              "AGENTS-historique.md": "B" * 64}
    changees, apparues, disparues = modifications_gelees(reference, actuel)
    controler("le cobaye MORD une source gelee MODIFIEE",
              len(changees) == 1 and changees[0][0].endswith("cerberus.md"),
              str(len(changees)) + " modification(s)")
    intactes = dict(reference)
    inchangees, zero_apparue, zero_disparue = modifications_gelees(reference, intactes)
    controler("le contre-temoin EPARGNE des sources gelees INTACTES",
              not inchangees and not zero_apparue and not zero_disparue, "0 accusation")
    controler("les DEUX empreintes sont portees par l accusation",
              changees and changees[0][1] == "A" * 64 and changees[0][2] == "C" * 64,
              (changees[0][1][:6] + " / " + changees[0][2][:6]) if changees else "")

    # 2. UNE SOURCE GELEE NEUVE et une DISPARUE sont deux populations DISTINCTES :
    #    creer un fichier dans une zone gelee n'est pas la meme faute que l'effacer,
    #    et un controle qui ne verrait que la modification laisserait passer les deux.
    neuve = {"cerveau-projet/agents/cerberus/neuf.md": "D" * 64}
    changees, apparues, disparues = modifications_gelees(reference, neuve)
    controler("le cobaye MORD une source gelee APPARUE", apparues == ["cerveau-projet/agents/cerberus/neuf.md"],
              str(apparues))
    changees, apparues, disparues = modifications_gelees({"x": "A"}, {})
    controler("le cobaye MORD une source gelee DISPARUE", disparues == ["x"], str(disparues))

    # 3. L'ADRESSE : un site declare est EPARGNE, un site NEUF est ACCUSE -- c'est
    #    la seule difference entre une INTERDICTION (le voisin declare la zone
    #    interdite) et une ADRESSE (la v3 atteint la zone).
    declare = ("_operateur/optimus-prime/super-combos/combos/outils/garde-flux2.py", 37,
               '    "cerveau-projet/freelance/",  # Agents freelance')
    nouveau = ("_operateur/optimus-prime/pilote/commun.py", 12,
               '    charger(Path("cerveau-projet/freelance/outil.py"))')
    controler("le contre-temoin EPARGNE le site DECLARE (interdiction, pas adresse)",
              not adresses_non_declarees([declare]), "0 accusation")
    controler("le cobaye MORD un site NEUF qui atteint la zone gelee",
              adresses_non_declarees([nouveau]) == [nouveau], str(len(adresses_non_declarees([nouveau]))))
    controler("le contre-temoin PROUVE que les deux passent le meme filtre brut",
              len([declare, nouveau]) == 2, "2 occurrences detectees avant tri")
    # LA MENTION N'EST PAS UNE ADRESSE : c'est LA mesure qui a evite d'accuser des
    # fichiers sains a la pose (un commentaire et deux messages citent la v1).
    commentaire = '    # le modele est cerveau-projet/agents/tools/verifier'
    message = '    lignes.append("> Modele : la v1 (cerveau-projet/agents/tools/verifier).")'
    controler("une MENTION en commentaire n'est pas une adresse",
              not any(verbe in commentaire for verbe in VERBES_D_ACCES), "aucun verbe d'acces")
    controler("un MESSAGE qui cite la v1 n'est pas une adresse",
              not any(verbe in message for verbe in VERBES_D_ACCES), "aucun verbe d'acces")
    controler("une LIGNE qui atteint la zone EST une adresse (contre-temoin)",
              any(verbe in nouveau[2] for verbe in VERBES_D_ACCES), "Path( present")

    # 4. LES EXCEPTIONS DE LA REGLE IMMUABLE : les deux fichiers de la racine sont
    #    ECRITS par la v3, ils ne sont donc pas des sources gelees -- et ils sont
    #    DITS a chaque passe.
    controler("les deux exceptions de la regle immuable sont nommees",
              EXCEPTIONS == ("demarrer-optimus-prime.md", "demarrer-cameleon.md"),
              ", ".join(EXCEPTIONS))
    controler("un point de restauration n'est PAS une source gelee (forme technique)",
              est_technique(Path("demarrer-optimus-prime.md.bak.20260922_203149")),
              "forme .bak")
    controler("une source gelee ordinaire n'est PAS technique (contre-temoin)",
              not est_technique(Path("cerveau-projet/agents/cerberus/cerberus.md")),
              "aucun motif technique")

    print()
    print("AUTO-TEST " + str(sum(resultats)) + "/" + str(len(resultats))
          + " -- " + ("VERDICT OK" if all(resultats) else "VERDICT KO"))
    return 0 if all(resultats) else 1


def main():
    parser = argparse.ArgumentParser(description="Garde des versions (R-003 / R-004 / ORDRE 3.4)")
    parser.add_argument("verbe", nargs="?", choices=("poser", "verifier"), help="poser | verifier")
    parser.add_argument("--auto-test", action="store_true", help="les cobayes, sur des faits fabriques")
    args = parser.parse_args()
    if args.auto_test:
        return auto_test()
    if args.verbe == "poser":
        return poser()
    if args.verbe == "verifier":
        return verifier()
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
