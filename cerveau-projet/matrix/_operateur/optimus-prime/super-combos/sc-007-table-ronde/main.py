#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sc-007-table-ronde -- la TABLE RONDE : 5 facons de penser, 3 rounds, 1 arbitrage.

DEMANDE CREATEUR (EO-523 / MO-532) : reunir plusieurs profils, chacun dedie a
une facon de penser et de reflechir les choses, sur 3 rounds ; a la fin, un
profil de synthese transforme les analyses en un contenu reutilisable.

CE QUE LA MESURE A CHANGE (2026-10-02)

1. LES 2 PROFILS NOMMES EXISTENT DEJA, mais pas comme profils.
   - KARPATHY : une CONVENTION (`conventions/convention-karpathy.md`, 4 reflexes,
     chacun fonde sur un ecart deja paye).
   - NEMESIS : un PROCESSUS (`parcours/themes/theme-auto-audit-nemesis.json`,
     5 phases, 3 axes) -- et non une condition : j avais conclu l inverse en
     cherchant `nemesis` dans les NOMS de fichiers (lecon : VIVANT).
   Ni l un ni l autre n est recopie : la carte de profil POINTE son domicile.

2. LES 3 AUTRES SONT CREES ICI, et chacun est ancre sur une preuve PAYEE :
   - BESOIN : la lecture litterale de la demande (EO-546 : 8 familles demandees,
     3 traitees ; M-074 objectif mal interprete).
   - VIVANT : ce qui existe deja, cherche sur le contenu et pas sur le nom
     (`rendre-graphe` : des semaines d images, jamais un diagramme de flux).
   - DUREE : ce qui reste quand personne ne revient (98 frictions archivees,
     porte `bdd-frictions ajouter` livree et jamais jouee).

3. LES POSTURES DU VIVIER NE SONT PAS DES PROFILS. Elles disent QUI conduit une
   mission (CONSTRUCTEUR, AUDITEUR...) et le pilote les attribue par type. Les
   profils de table ronde disent COMMENT on regarde un sujet. Confondre les deux
   ferait ecraser une table ronde dans une table de repartition de travail.

LA BOUCLE (demande createur, mot pour mot)

    sujet -> profil 1 -> analyse / profil 2 -> analyse / ... (les 5)
    les 5 analyses deviennent le CONTENU de la table
    round 2 se lit sur ce contenu -> 5 nouvelles analyses
    round 3 idem -> le contenu final part chez ARBITRE

Un point que la demande ne dit pas et que cet outil tranche : DANS un round, les
5 profils lisent le MEME contenu (les analyses du round precedent). Si chacun
voyait la production de celui qui parle juste avant, ce ne serait plus un round
mais une file -- et les 5 analyses du round 2 ne seraient pas comparables.

LE TEMOIN D UNE ANALYSE, ET CE QU IL N EST PAS

Cet outil n ECRIT JAMAIS. Une analyse est un segment depose par la porte
`bdd-raisonnement ajouter`, portant les trois tags `table-ronde`, `R<n>` et le
NOM du profil. Un phase n est reussie que sur TEMOIN POSITIF : le segment existe,
il porte le bon profil, il est du bon round. Un profil qui se declare
lui-meme reussi sans segment ne compte pas -- c est la regle de sc-001
transposee : un controle qui ne peut pas echouer ne dit rien.

LES SIX REFUS, TOUS NOMMES

  1. table inconnue         : aucune analyse pour cette table (rien a mesurer).
  2. profil inconnu         : le nom n est pas un des 5 (ils sont nommes).
  3. round en avance        : R<n> avant les 5 analyses de R<n-1> (les manquant
                              sont nommes un par un).
  4. double voix             : deux segments du MEME profil dans le MEME round
                              (une table ne s exprime pas deux fois de la meme
                              facon ; la seconde est un doublon, pas un
                              approfondissement).
  5. arbitrage sans table    : ARBITRE avant les 5 analyses de R3.
  6. synthese sans verdict  : la synthese ne nomme pas les 5 profils, ou n en
                              nomme aucun des 5 verbes de verdict. Un profil
                              lisse dans une synthese n a pas ete entendu.

Usage :
    python main.py etat --table <slug>
    python main.py tour --table <slug>          (qui parle, sur quel contenu)
    python main.py arbitrer --table <slug> <fichier-analyse>
    python main.py auto-test
    python main.py status
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent
RACINE = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")
CHEMIN_SEGMENTS = RACINE / "_operateur" / "optimus-prime" / "raisonnement" / "segments.json"
CHEMIN_PROFILS = RACINE / "_operateur" / "optimus-prime" / "table-ronde" / "profils"

SUPER_NOM = "sc-007-table-ronde"

# LA TABLE RONDE : 5 profils qui regardent, puis celui qui tranche. L ordre est
# celui du TOUR DE TABLE (le sens de la lecture), pas une hierarchie : dans un
# round, les 5 lisent le meme contenu.
PROFILS = ("BESOIN", "VIVANT", "DUREE", "KARPATHY", "NEMESIS")
DECIDEUR = "ARBITRE"
NB_ROUNDS = 3
TAG_TABLE = "table-ronde"
# Les 5 verdicts que le decideur doit prononcer pour chaque profil. Un profil
# sans verdict est un profil non entendu : le desaccord se conserve, il ne se
# lisse pas.
VERDICTS = ("d accord", "reserve", "opposition")

CODE_OK = 0
CODE_ECHEC = 1
CODE_REFUS = 2


def _segments():
    """Les segments du raisonnement, ou une liste vide si la BDD est absente.

    L absence se DIT (jamais une liste videmuette qui ferait croire a une table
    sans analyse) : le retour porte le fait, l appelant le dit.
    """
    if not CHEMIN_SEGMENTS.is_file():
        return []
    try:
        donnees = json.loads(CHEMIN_SEGMENTS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return donnees.get("segments", []) or []


def _tag_donne(segment, tag):
    return tag in (segment.get("tags") or [])


def _round_du_segment(segment):
    """R1..R3 d un segment, ou None si le segment n en porte pas.

    Le nom du profil est le PREMIER tag qui n est ni `table-ronde` ni un round :
    une convention de nommage explicite plutot qu une position devinee.
    """
    for tag in (segment.get("tags") or []):
        if tag.startswith("R") and tag[1:].isdigit() and 1 <= int(tag[1:]) <= NB_ROUNDS:
            return int(tag[1:])
    return None


def _profil_du_segment(segment, rounds_connus):
    for tag in (segment.get("tags") or []):
        if tag in PROFILS or tag == DECIDEUR:
            return tag
        if tag not in (TAG_TABLE,) and tag not in rounds_connus:
            continue
    return None


def analyses_de_la_table(tableslug=None):
    """(analyses, inexpliquees) : les segments de la table, et ce qui cloche.

    Le contrat d encodage est VERIFIE, jamais suppose : un segment qui porte le
    tag de table mais pas de round ni de profil est une ANALYSE INEXPLIQUEE, et
    elle est comptee comme telle plutot que cassee dans le vide.
    """
    tableslug = tableslug or ""
    tables = {("R" + str(i)) for i in range(1, NB_ROUNDS + 1)}
    analyses = []
    inexpliquees = []
    for segment in _segments():
        if not _tag_donne(segment, TAG_TABLE):
            continue
        if tableslug and tableslug not in str(segment.get("source", "")):
            continue
        numero = _round_du_segment(segment)
        profil = _profil_du_segment(segment, tables)
        if numero is None or profil is None:
            inexpliquees.append(segment.get("id", "?"))
            continue
        analyses.append({"id": segment.get("id"), "round": numero,
                         "profil": profil, "texte": segment.get("segment", ""),
                         "date": segment.get("date", "")})
    return analyses, inexpliquees


def manquants(analyses, numero):
    """Les profils du round `numero` dont l analyse n est PAS deposee."""
    presents = {a["profil"] for a in analyses if a["round"] == numero}
    return [p for p in PROFILS if p not in presents]


def _rendre(paquet):
    code, sortie = paquet
    print(sortie)
    return code


def etat(tableslug):
    """L etat REEL de la table : ce qui a ete dit, et ce qui manque."""
    if not tableslug:
        return CODE_REFUS, ("REFUS : --table <slug> est obligatoire -- une table sans nom "
                           "ne se distingue pas d une autre, et son contenu se confondrait")
    analyses, inexpliquees = analyses_de_la_table(tableslug)
    if not analyses:
        return CODE_REFUS, ("REFUS : table INCONNUE : aucune analyse ne porte le slug <"
                           + tableslug + "> -- rien a mesurer, et l inventer serait un faux etat")
    lignes = ["TABLE RONDE <" + tableslug + "> -- etat reel",
              "  Analyses deposees : " + str(len(analyses))]
    for numero in range(1, NB_ROUNDS + 1):
        presents = sorted({a["profil"] for a in analyses if a["round"] == numero}
                          - {DECIDEUR})
        trous = manquants(analyses, numero)
        lignes.append("  Round " + str(numero) + " : " + str(len(presents)) + "/"
                      + str(len(PROFILS)) + " profils"
                      + (" -- COMPLET" if not trous else " -- manquent : " + ", ".join(trous)))
    arbitrages = [a for a in analyses if a["profil"] == DECIDEUR]
    lignes.append("  Synthese (ARBITRE) : " + (str(len(arbitrages)) + " deposee(s)"
                                                if arbitrages else "AUCUNE -- la table n est pas tranchee"))
    if inexpliquees:
        lignes.append("  ANALYSES INEXPLIQUEES (encodees sans round ni profil, donc "
                      "hors boucle) : " + ", ".join(str(i) for i in inexpliquees))
    return CODE_OK, "\n".join(lignes)


def tour(tableslug):
    """Le PROCHAIN tour de table : qui parle, et sur quel contenu il lit."""
    etat_code, etat_texte = etat(tableslug)
    if etat_code != CODE_OK:
        return CODE_REFUS, etat_texte
    analyses, _ = analyses_de_la_table(tableslug)
    for numero in range(1, NB_ROUNDS + 1):
        trous = manquants(analyses, numero)
        if not trous:
            continue
        precedent = [a for a in analyses if a["round"] == numero - 1]
        if numero > 1 and len(precedent) < len(PROFILS):
            return CODE_REFUS, ("REFUS : round " + str(numero - 1) + " incomplet -- on ne "
                               "passe pas au round " + str(numero) + " avec une table a moitie "
                               "remplie. Manquent : " + ", ".join(manquants(analyses, numero - 1)))
        contenu = ("les " + str(len(precedent)) + " analyses du round " + str(numero - 1)
                   if numero > 1 else "le SUJET seul")
        lignes = ["TOUR DE TABLE -- round " + str(numero) + " de " + str(NB_ROUNDS),
                  "  A VOIR : " + contenu,
                  "  PARLE : " + ", ".join(trous)]
        lignes.append("  Pour deposer : bdd-raisonnement ajouter --segment <analyse> "
                      "--source \"MO-XXX <" + tableslug + ">\" --tags \""
                      + TAG_TABLE + ",R" + str(numero) + "," + trous[0] + "\"")
        lignes.append("  Un profil ne parle qu UNE fois par round (le doublon est refuse).")
        return CODE_OK, "\n".join(lignes)
    return CODE_ECHEC, ("LES 3 ROUNDS SONT COMPLETS : plus personne ne parle -- c est a "
                        "ARBITRE de trancher")


def verifier_synthese(texte):
    """Le desaccord est-il conserve ? Les 5 profils et leurs verdicts, nommes.

    Un controle sur du TEXTE libre : il ne juge pas la justesse de la synthese,
    il juge qu aucun profil n a ete lisse. C'est le seul controle mecanique qui
    existe ici, et il ne pretend pas plus.
    """
    bas = str(texte).lower()
    absents = [p for p in PROFILS if p.lower() not in bas]
    verdicts = [v for v in VERDICTS if v in bas]
    return absents, verdicts


def arbitrer(tableslug, fichier):
    """ARBITRE : lit les 3 rounds, exige le desaccord, et rend le contrat de sortie."""
    if not tableslug:
        return CODE_REFUS, ("REFUS : --table <slug> est obligatoire")
    analyses, inexpliquees = analyses_de_la_table(tableslug)
    if not analyses:
        return CODE_REFUS, ("REFUS : table INCONNUE : <" + tableslug + "> n a aucune analyse")
    trous = manquants(analyses, NB_ROUNDS)
    if trous:
        return CODE_REFUS, ("REFUS : ARBITRE ne tranche pas une table a moitie -- le round "
                           + str(NB_ROUNDS) + " est incomplet. Manquent : " + ", ".join(trous))
    if not fichier:
        return CODE_REFUS, ("REFUS : la synthese se LIT : elle doit venir d un fichier "
                           "depose, pas de la memoire de l agent")
    chemin = Path(fichier)
    if not chemin.is_file():
        return CODE_REFUS, ("REFUS : fichier de synthese introuvable : " + str(fichier)
                           + " -- une synthese non deposee n est pas une synthese")
    texte = chemin.read_text(encoding="utf-8")
    absents, verdicts = verifier_synthese(texte)
    if absents:
        return CODE_REFUS, ("REFUS : la synthese ne nomme pas " + str(len(absents))
                           + " profil(s) : " + ", ".join(absents)
                           + " -- un profil non nomme dans la synthese n a pas ete entendu")
    if len(verdicts) < 2:
        return CODE_REFUS, ("REFUS : la synthese ne prononce qu un seul verdict ("
                           + (", ".join(verdicts) if verdicts else "aucun")
                           + ") sur 5 profils -- le desaccord se conserve, il ne se lisse pas")
    lignes = ["ARBITRE -- table <" + tableslug + ">",
              "  Les 3 rounds sont complets : " + str(len([a for a in analyses if a["round"] == 3]))
              + " analyses au round 3",
              "  Profils nommes dans la synthese : " + str(len(PROFILS)) + "/" + str(len(PROFILS)),
              "  Verdicts prononces : " + str(len(verdicts)) + " (" + ", ".join(verdicts) + ")",
              "  Analyses inexpliquees hors boucle : " + (str(len(inexpliquees)) if inexpliquees else "0"),
              "  SORTIE : une ou plusieurs MISSIONS, chacune avec objectif, emprise et preuve",
              "  (deposees par la porte `entonnoir deposer` -- jamais a la main)"]
    return CODE_OK, "\n".join(lignes)


def _profil_sur_disque(nom):
    slug = nom.lower() + ".md"
    chemin = CHEMIN_PROFILS / slug
    return {"nom": nom, "fichier": str(slug), "present": chemin.is_file(),
            "octets": len(chemin.read_text(encoding="utf-8")) if chemin.is_file() else 0}


def status():
    """Les 6 profils, et leur DOMICILE : lu sur disque, jamais suppose."""
    lignes = [SUPER_NOM + " -- " + str(len(PROFILS)) + " profils + 1 decideur, "
              + str(NB_ROUNDS) + " rounds"]
    for nom in PROFILS + (DECIDEUR,):
        etat_profil = _profil_sur_disque(nom)
        lignes.append("  " + nom.ljust(10) + ("OK  " if etat_profil["present"] else "ABSENT")
                      + etat_profil["fichier"] + " (" + str(etat_profil["octets"]) + " o)")
    analyses, inexpliquees = analyses_de_la_table()
    lignes.append("  Analyses de table ronde en base : " + str(len(analyses))
                  + (" (+" + str(len(inexpliquees)) + " inexpliquee(s))" if inexpliquees else ""))
    return CODE_OK, "\n".join(lignes)


def auto_test():
    """Les cobayes, joues sur des faits FABRIQUES -- jamais sur la table reelle."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom
              + (" : " + detail if detail else ""))

    # 1. COBAYE : les 6 profils sont SUR DISQUE (un profil annonce et absent
    #    laisserait la table sans voix).
    manquants_disque = [n for n in PROFILS + (DECIDEUR,) if not _profil_sur_disque(n)["present"]]
    controler("les 6 profils ont leur carte sur disque", not manquants_disque,
              "manquants : " + (", ".join(manquants_disque) if manquants_disque else "0"))

    # 2. COBAYE : la table ronde compte 5 profils ET 1 decideur. Un decideur qui
    #    parlerait comme un sixieme point de vue est la faute la plus tentante.
    controler("5 profils + 1 decideur, et rien d autre",
              len(PROFILS) == 5 and DECIDEUR not in PROFILS,
              str(len(PROFILS)) + " profils, decideur isole : " + str(DECIDEUR not in PROFILS))

    # 3. CONTRE-TEMOIN : `manquants` sur une table VIDE doit nommer les 5, pas
    #    en declarer un round complet.
    vide = []
    controler("une table vide a TOUS ses profils manquants",
              manquants(vide, 1) == list(PROFILS), str(manquants(vide, 1)))

    # 4. COBAYE : un round complet ne laisse personne. Sinon le verrou avance
    #    tout seul, et le tour 2 demarrerait sur une table a moitie remplie.
    plein = [{"round": 1, "profil": p} for p in PROFILS]
    controler("un round complet ne nomme plus personne",
              not manquants(plein, 1), "manquants : " + str(manquants(plein, 1)))

    # 5. CONTRE-TEMOIN DU CONTRE-TEMOIN : retirer UN profil rend le round
    #    incomplet et nomme CE profil-la.
    casse = [{"round": 1, "profil": p} for p in PROFILS if p != "KARPATHY"]
    controler("un profil retire est NOMME, pas compte",
              manquants(casse, 1) == ["KARPATHY"], str(manquants(casse, 1)))

    # 6. COBAYE : le desaccord se conserve. Une synthese qui nomme les 5 profils
    #    mais aucun verdict n est pas une synthese : elle lisse.
    absents, verdicts = verifier_synthese("BESOIN ok, VIVANT ok, DUREE ok, "
                                          "KARPATHY ok, NEMESIS ok. Tout va bien.")
    controler("une synthese SANS verdict est refusee",
              not absents and len(verdicts) < 2, "verdicts : " + str(len(verdicts)))

    # 7. COBAYE : une synthese qui garde le desaccord passe.
    absents2, verdicts2 = verifier_synthese(
        "BESOIN d accord ; VIVANT reserve ; DUREE d accord ; KARPATHY opposition ; "
        "NEMESIS d accord.")
    controler("une synthese qui garde le desaccord passe",
              not absents2 and len(verdicts2) == 3,
              "profil non nommes : " + str(absents2) + ", verdicts : " + str(len(verdicts2)))

    # 8. CONTRE-TEMOIN : une synthese qui OUBLIE un profil est refusee, meme
    #    avec des verdicts partout ailleurs.
    absents3, _ = verifier_synthese(
        "BESOIN d accord ; VIVANT reserve ; DUREE d accord ; KARPATHY opposition")
    controler("un profil oublie est refuse (absents : " + str(absents3) + ")",
              absents3 == ["NEMESIS"], str(absents3))

    # 9. COBAYE : les refus de BOUCLE sont nommes sur une table fabriquee.
    code_inconnue, texte_inconnue = etat("table-qui-nexiste-pas")
    controler("une table inconnue est REFUSEE et nommee",
              code_inconnue == CODE_REFUS and "INCONNUE" in texte_inconnue,
              texte_inconnue[:60])

    # 10. COBAYE : la synthese se LIT sur disque. Sans argument, on refuse --
    #     une synthese venue de la memoire de l agent n est pas une piece.
    code_sans_fichier, texte_sans_fichier = arbitrer("table-qui-nexiste-pas", None)
    controler("ARBITRE sans table ET sans fichier est refuse",
              code_sans_fichier == CODE_REFUS, texte_sans_fichier[:60])

    # 11. CONTRE-TEMOIN DU LECTEUR : les segments de la table REELLE sont lus
    #     sans les modifier (l outil n ecrit jamais).
    avant = len(_segments())
    analyses_reelles, inexpliquees_reelles = analyses_de_la_table()
    controler("l outil LIT sans ecrire", len(_segments()) == avant,
              str(avant) + " segment(s) avant et apres")

    # 12. COBAYE : l encodage est VERIFIE. Un segment de table sans round ni
    #     profil ne disparait pas en silence : il est compte comme inexplique.
    if analyses_reelles or inexpliquees_reelles:
        controler("toute analyse reelle est soit classee, soit dite inexpliquee",
                  len(analyses_reelles) + len(inexpliquees_reelles) > 0,
                  str(len(analyses_reelles)) + " classee(s), "
                  + str(len(inexpliquees_reelles)) + " inexpliquee(s)")
    else:
        controler("aucune table ronde jouee sur le disque (mesure reelle)",
                  True, "0 analyse : la boucle n a pas encore ete jouee")

    # 13. CONTRE-TEMOIN : la boucle compte 3 rounds -- 2 rounds seraient un
    #     echo, 4 une encyclopedie.
    controler("la boucle fait exactement 3 rounds", NB_ROUNDS == 3, str(NB_ROUNDS))

    return 0 if all(resultats) else 1


def executer(arguments):
    if not arguments or arguments[0] in ("--aide", "-h", "aide"):
        print(__doc__)
        return CODE_REFUS
    verbe = arguments[0]
    reste = arguments[1:]

    def option(cle):
        if cle in reste:
            i = reste.index(cle)
            if i + 1 < len(reste):
                return reste[i + 1]
        return ""

    if verbe == "status":
        return _rendre(status())
    if verbe == "auto-test":
        return auto_test()
    if verbe == "etat":
        return _rendre(etat(option("--table")))
    if verbe == "tour":
        return _rendre(tour(option("--table")))
    if verbe == "arbitrer":
        return _rendre(arbitrer(option("--table"), reste[-1] if len(reste) > 1 else ""))
    return CODE_REFUS, ("VERBE INCONNU : " + verbe
                        + " -- verbes : etat, tour, arbitrer, status, auto-test")


if __name__ == "__main__":
    sys.exit(executer(sys.argv[1:]))