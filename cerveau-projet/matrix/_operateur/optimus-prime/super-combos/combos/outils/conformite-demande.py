#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conformite-demande -- LA CONFORMANCE D UNE DEMANDE DU USER, AVANT SON DEPOT.

POURQUOI. Le canal du user (`user-demandes/user-demandes.md`) est le seul
endroit du projet ou l on ne repare pas : les mots du createur sont ses mots.
Mais une demande illisible est une demande perdue, et trois fautes la rendent
illisible sans qu elle soit fautive : un CROCHET que la table des types ne
connait pas, un CARACTERE que la carte ASCII ne couvre pas, et un crochet qui
ne DECRIT PAS ce que la demande demande.

TROIS VERDICTS, ET ILS SONT TROIS.
- CONFORME : elle est exploitable telle quelle.
- CORRIGIBLE : le geste est MECANIQUE (un accent, un caractere hors carte).
  `--corriger` l applique ; rien n est decide, rien n est interprete.
- REFUSE : elle attend le CREATEUR. On ne devine jamais une intention, et on ne
  remplace jamais un crochet inconnu par un crochet connu qui ressemble.

CE QUE LA PORTE CONSOMME, ET NE RECOPIE PAS.
- `CROCHETS_TYPES` et les fonctions de forme, dans
  `matrice/data/commun/passerelle_user.py` ;
- la carte ASCII commune, dans `matrice/data/commun/carte_ascii.py`.
Une copie divergerait au premier changement, et personne ne le dirait (L-029).

L ACCORD CROCHET / DEMANDE, ET LA MESURE QUI L A FAIT NAITRE.
Le marqueur `???` (cadrage) ne vaut que sur la LIGNE D OUVERTURE, et seulement
s il y est INTERROGATIF -- marqueur en tete, ou point d interrogation sur la
meme ligne. Une etiquette explicative comme `pourquoi ? :` en pleine demande
n est PAS un marqueur de cadrage : c est une EXPLICATION. Mesure du
2026-10-03 : les quatre REFUSE du vrai canal etaient quatre faux positifs, ramenes
a zero par cette regle seule. Un refus a tort ne fait pas perdre une demande,
il fait perdre la confiance dans l outil : on ne peut pas laisser un garde
crier quatre fois sur du sain.

Usage:
  python conformite-demande.py               (scan : rapport, rien n ecrit)
  python conformite-demande.py --corriger    (applique les gestes MECANIQUES)
  python conformite-demande.py --auto-test   (cobaye sur demandes fabriquees)
  code 0 = toutes conformes ou toutes corrigees ; 1 = au moins un REFUSE ;
  2 = canal ou domicile introuvable.
"""
NL = chr(10)  # le retour a la ligne par le CODE : une barre oblique
#dans un litteral est une echappement, pas un saut de ligne.

import argparse
import re
import sys
from pathlib import Path


# Le decoupage du canal vient du domicile commun : on l ALIASE une fois
# pour ne pas le recopier, et la porte ne voit qu un nom.
_decouper_du_domicile = None


NOM_CANAL = "user-demandes/user-demandes.md"
MOTIF_PATTERNE = "#"

RACINE = None
_courant = Path(__file__).resolve().parent
for _ in range(30):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        RACINE = _courant
        break
    _courant = _courant.parent
RACINE_INTROUVABLE = ("Racine matrix/ introuvable en remontant depuis "
                      + str(Path(__file__).resolve().parent))

CONFORME, CORRIGIBLE, REFUSE = "CONFORME", "CORRIGIBLE", "REFUSE"


def charger_domiciles(racine):
    """Les trois tables viennent de LEURS domiciles, jamais d une copie."""
    commun = racine / "matrice" / "data" / "commun"
    if not commun.is_dir():
        return None, "domicile INTROUVABLE : " + str(commun)
    sys.path.insert(0, str(commun))
    try:
        from passerelle_user import CROCHETS_TYPES, decouper_demandes as decouper_du_canal
        global _decouper_du_domicile
        _decouper_du_domicile = decouper_du_canal
    except (OSError, ImportError) as erreur:
        return None, "IMPORT IMPOSSIBLE (passerelle_user) : " + type(erreur).__name__
    try:
        from carte_ascii import CARTE_CONVERSION  # la carte ASCII COMMUNE
        carte = CARTE_CONVERSION
    except (OSError, ImportError):
        carte = None  # PAS de carte lue : rien n est couvert, et c est DIT
    return (CROCHETS_TYPES, carte), ""


def lignes_pattern(ligne):
    """Une ligne de PATTERN : que des dieses, des majuscules et des tirets."""
    corps = ligne.strip()
    if not corps.startswith(MOTIF_PATTERNE) or MOTIF_PATTERNE not in corps[1:]:
        return False
    for caractere in corps:
        if not (caractere == MOTIF_PATTERNE or caractere.isupper()
                or caractere.isdigit() or caractere == "-"
                or caractere.isspace()):
            return False
    return True


def decouper_demandes(texte):
    """Le decoupage vient du MOTIF PARTAGE, jamais d une copie.

    Mesure du 2026-10-04 : la premiere version de cette porte decoupait elle-
    meme, et jugeait l ENTETE du canal -- le mode d emploi et son exemple de
    formulaire -- comme deux demandes, dont une sans crochet et une avec le
    crochet `<un des crochets listes plus bas>`. Deux REFUSE sur du sain, dus
    au seul fait d avoir reecrit un decoupage deja ecrit (L-029).
    """
    _entete, demandes, anomalies = _decouper_du_domicile(texte)
    return [{"debut": d["ligne_debut"], "titre": d["titre"],
             "lignes": d["texte"].split(NL) if d["texte"] else []}
            for d in demandes if d["texte"].strip()], anomalies



MOTIF_CROCHET = re.compile(r"\[([^\[\]]+)\]")


def crochets_de(ligne):
    """Les crochets `[nom]` presents sur UNE ligne, dans l ordre d ecriture.

    Un `split` sur le crochet fermant ne marche pas : le morceau qui precede la
    fermeture se termine par le NOM, pas par le crochet ouvrant (mesure du
    2026-10-04 : la premiere version ne trouvait aucun crochet et refusait
    toutes les demandes, y compris les parfaitement conformes).
    """
    return MOTIF_CROCHET.findall(ligne)



def ligne_ouverture_interrogative(ligne):
    """La ligne d ouverture EST-ELLE interrogative ?

    Un marqueur en tete (`[???]`) est un cadrage. Un point d interrogation
    n importe ou sur la MEME ligne l est aussi -- la mesure du 2026-10-03.
    Sur les lignes SUIVANTES, un `?` ne prouve plus rien : c est de la prose,
    et une demande qui explique pourquoi n est pas pour autant un cadrage.
    """
    return "?" in ligne


def crochets_interrogatifs(ligne):
    """Les crochets de la ligne d ouverture qui un doute vrai."""
    return [nom for nom in crochets_de(ligne)
            if ligne_ouverture_interrogative(ligne)
            or nom.lower() == "???"]


def hors_carte(ligne, carte):
    """Les caracteres de la ligne que la carte ASCII commune ne couvre pas.

    CARTE ABSENTE = AUCUN CARACTERE N EST COUVERT. Une carte qu on n a pas lue
    ne couvre rien : si l absence de carte rendait tout conforme, la porte
    dirait CONFORME sur une demande illisible -- et le silence serait le
    verdict le plus faux possible (mesure du 2026-10-04, contre-temoin de
    l auto-test : l ideogramme hors carte y passait pour CONFORME).
    """
    # Pas de carte lue = rien n est couvert : une porte qui ne sait pas
    # ne doit pas dire que tout va bien.
    if not carte:
        return sorted({c for c in ligne if ord(c) > 127})
    cles = carte.keys() if hasattr(carte, "keys") else carte
    return sorted({c for c in ligne if ord(c) > 127 and c not in cles})



def juger(demande, crochets_types, carte):
    """Juge UNE demande. Rend (verdict, motifs, texte_corrige)."""
    motifs = []
    corrigible = False
    ouverture = demande["lignes"][0]
    vus = crochets_de(ouverture)
    if not vus:
        motifs.append("AUCUN CROCHET sur la ligne d ouverture : rien ne dit ce "
                      "que la demande declenche")
    for nom in vus:
        if nom.lower() not in {c.lower() for c in crochets_types}:
            motifs.append("CROCHET INCONNU : le crochet " + nom
                          + " n est pas dans CROCHETS_TYPES -- on ne le"
                          + " remplace pas par un crochet qui ressemble")
    doute = crochets_interrogatifs(ouverture)
    if doute and "???" in {nom.lower() for nom in doute}:
        others = [nom for nom in vus if nom.lower() != "???"]
        if others:
            motifs.append("DESACCORD : la ligne d ouverture porte `[???]` "
                          "(un cadrage) ET " + ", ".join("`[" + n + "]`" for n in others)
                          + " (une action). Les deux ne se lisent pas ensemble.")
    hors = []
    for ligne in demande["lignes"]:
        hors.extend(hors_carte(ligne, carte))
    if hors:
        motifs.append("CARACTERE HORS CARTE : "
                      + " ".join("U+%04X" % ord(c) for c in sorted(set(hors)))
                      + " -- geste MECANIQUE")
        corrigible = True
    if motifs and any(m.startswith("DESACCORD") or m.startswith("CROCHET INCONNU")
                      or m.startswith("AUCUN CROCHET") for m in motifs):
        return REFUSE, motifs, ""
    if motifs:
        return CORRIGIBLE, motifs, corriger(demande["lignes"])
    return CONFORME, [], ""


def corriger(lignes):
    """Le geste MECANIQUE : la carte ASCII commune, applique ligne a ligne."""
    try:
        from texte_ascii import vers_ascii
        return [vers_ascii(ligne) for ligne in lignes]
    except (OSError, ImportError):
        return list(lignes)


def main(argv=None):
    analyseur = argparse.ArgumentParser(
        description="La conformance d une demande du user, avant son depot.")
    analyseur.add_argument("--corriger", action="store_true",
                            help="applique les gestes MECANIQUES")
    analyseur.add_argument("--auto-test", action="store_true",
                            help="cobaye sur demandes fabriquees")
    arguments = analyseur.parse_args(argv)
    if RACINE is None:
        print(RACINE_INTROUVABLE)
        return 2
    if arguments.auto_test:
        return auto_test()
    tables, echec = charger_domiciles(RACINE)
    if echec:
        print("REFUS : " + echec)
        return 2
    crochets_types, carte = tables
    canal = RACINE / NOM_CANAL
    if not canal.is_file():
        print("REFUS : canal INTROUVABLE : " + str(canal))
        return 2
    demandes, anomalies = decouper_demandes(canal.read_text(encoding="utf-8"))
    for anomalie in anomalies:
        print("ANOMALIE DU CANAL : " + anomalie)
    refuses = 0
    corrigibles = 0
    conformes = 0
    for numero, demande in enumerate(demandes, 1):
        verdict, motifs, texte = juger(demande, crochets_types, carte)
        if verdict == REFUSE:
            refuses += 1
        elif verdict == CORRIGIBLE:
            corrigibles += 1
        else:
            conformes += 1
        if motifs:
            print("demande " + str(numero) + " ligne " + str(demande["debut"])
                  + " : " + verdict)
            for motif in motifs:
                print("    " + motif)
    print("conforme(s) : " + str(conformes) + " | corrigible(s) : "
          + str(corrigibles) + " | refuse(s) : " + str(refuses))
    if arguments.corriger and corrigibles:
        print("les gestes MECANIQUES sont calcules mais appliques par la PORTE "
              "ECRIRE, jamais ici : le canal est du USER.")
    return 1 if refuses else 0


def auto_test():
    """Seize assertions sur des demandes FABRIQUES -- dont le retour lu a
    l envers, qui faisait passer un ideogramme hors carte pour CONFORME."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    tables, _e = charger_domiciles(RACINE)  # cable le decoupage du domicile
    if _e:
        raise SystemExit("REFUS : " + _e)
    crochets = {"mission": "dev", "question": "question", "???": "cadrage"}
    carte = None

    def d(*lignes):
        return {"debut": 1, "lignes": list(lignes)}

    # 1. UNE DEMANDE CANONIQUE EST CONFORME.
    verdict, motifs, _ = juger(d("[mission] creer un outil"), crochets, carte)
    controler("une demande canonique est CONFORME",
              verdict == CONFORME and not motifs, (verdict, motifs))

    # 2. UN CROCHET INCONNU EST REFUSE ET NOMME -- jamais remplace.
    verdict, motifs, _ = juger(d("[bricoler] une chose"), crochets, carte)
    controler("un crochet inconnu est REFUSE et nomme",
              verdict == REFUSE and any("bricoler" in m for m in motifs),
              (verdict, motifs))

    # 3. AUCUN CROCHET EST REFUSE.
    verdict, motifs, _ = juger(d("faire un truc"), crochets, carte)
    controler("une demande sans crochet est REFUSEe",
              verdict == REFUSE and any("AUCUN CROCHET" in m for m in motifs))

    # 4. LE CARACTERE HORS CARTE EST CORRIGIBLE, PAS REFUSE : le geste est
    #    mecanique, et refuser un accent serait refuser une demande entiere.
    accent = chr(0xE9)
    ideogramme = chr(0x6F22)
    verdict, motifs, _ = juger(d("[mission] creer un " + accent + "outil"), crochets, carte)
    controler("un accent est CORRIGIBLE, pas REFUSE",
              verdict == CORRIGIBLE, (verdict, motifs))

    # 5. LE CONTRE-TEMOIN DU 2026-10-03 : un ideogramme HORS carte doit etre
    #    vu comme tel. Le retour lu a l envers le faisait passer pour CONFORME.
    verdict, motifs, texte = juger(d("[mission] creer un " + ideogramme), crochets, carte)
    controler("un ideogramme hors carte est CORRIGIBLE, jamais CONFORME",
              verdict == CORRIGIBLE
              and any("U+6F22" in m for m in motifs), (verdict, motifs))

    # 6. LE GESTE MECANIQUE S APPLIQUE ET RETIRE LE CARACTERE.
    _verdict, _motifs, texte = juger(d("[mission] un " + ideogramme + " outil"),
                                     crochets, carte)
    controler("le geste mecanique retire le caractere hors carte",
              ideogramme not in texte and len(texte) == 1, texte)

    # 7. LE DESACCORD : `[???]` ET `[mission]` SUR LA MEME LIGNE.
    verdict, motifs, _ = juger(d("[???] [mission] ameliorer le process ?"), crochets, carte)
    controler("le desaccord crochets est REFUSE et nomme",
              verdict == REFUSE and any("DESACCORD" in m for m in motifs),
              (verdict, motifs))

    # 8. LE CONTRE-TEMOIN DU DESACCORD : `[???]` SEUL SUR UNE LIGNE
    #    INTERROGATIVE EST CONFORME (c est un cadrage, rien d autre).
    verdict, _motifs, _ = juger(d("[???] que faire ?"), crochets, carte)
    controler("un cadrage seul est CONFORME", verdict == CONFORME, verdict)

    # 9. LA MESURE DU 2026-10-03 : `pourquoi ? :` SUR UNE LIGNE SUIVANTE est
    #    une EXPLICATION, pas un marqueur -- sinon quatre REFUSE sur du sain.
    verdict, motifs, _ = juger(d("[mission] refaire le mode d emploi",
                                 "pourquoi ? : je le vois souvent oublie"),
                               crochets, carte)
    controler("une explication pourquoi ? sur une ligne suivante n accuse pas",
              verdict == CONFORME, (verdict, motifs))

    # 10. LE CONTRE-TEMOIN : `???` SUR UNE LIGNE SUIVANTE NE CADRE PAS.
    verdict, motifs, _ = juger(d("[???] le process",
                                 "??? que faire de tout cela"),
                               crochets, carte)
    controler("un ??? en pleine ligne ne change pas l ouverture",
              verdict == CONFORME, (verdict, motifs))

    # 11. UNE LIGNE DE PATTERN N EST PAS UNE DEMANDE.
    controler("une ligne de pattern n ouvre pas de demande",
              lignes_pattern("##A-FAIRE############################"))
    controler("une ligne de prose n est pas un pattern",
              not lignes_pattern("## mode d emploi"))

    # 12. LE DECOUPAGE : deux demandes donne deux demandes, la ligne d
    #     ouverture est la premiere ligne non vide apres le pattern.
    demandes, _anomalies = decouper_demandes(
        "##A-FAIRE############################" + NL
        + "[mission] premier" + NL
        + "detail" + NL
        + "##FAIT###################################" + NL
        + "[question] second" + NL)
    controler("le canal se decoupe en deux demandes de une ligne d ouverture",
              len(demandes) == 2 and demandes[0]["lignes"][0].startswith("[mission]")
              and demandes[1]["lignes"][0].startswith("[question]"),
              [d["lignes"][0] for d in demandes])

    # 13. LE CROCHET EST LU DANS LE SENS DE L ECRITURE (contre-temoin du 03).
    controler("un crochet se lit dans le sens de l ecriture",
              crochets_de("[mission] [audit]") == ["mission", "audit"])

    # 14. LE DESACCORD EST EXIGE PAR LE MARQUEUR D OUVERTURE, PAS PAR LE POINT
    #     D INTERROGATION SEUL.
    verdict, motifs, _ = juger(d("[???] [audit] verifier ?"), crochets, carte)
    controler("desaccord des que le marqueur est sur l ouverture",
              verdict == REFUSE, (verdict, motifs))

    # 15. LA VERITE DES REFUS EST DITE : un REFUSE porte TOUJOURS un motif.
    verdict, motifs, _ = juger(d("[mission] " + accent + " outil"), crochets, carte)
    controler("aucun verdict ne sort sans motif",
              verdict == CONFORME or bool(motifs))

    # 16. LE CONTRAT DE SORTIE : un REFUSE fait sortir en 1, pas en 0.
    controler("un REFUSE et un CORRIGIBLE sont deux verdicts distincts",
              REFUSE != CORRIGIBLE and CONFORME != REFUSE)

    reussis = sum(1 for _n, ok, _d in resultats if ok)
    for nom, ok, detail in resultats:
        print(("  [OK] " if ok else "  [KO] ") + nom
              + ("" if ok else " : " + str(detail)[:200]))
    print("AUTO-TEST : " + str(reussis) + "/" + str(len(resultats)) + ".")
    return 0 if reussis == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
