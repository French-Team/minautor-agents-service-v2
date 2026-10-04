#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legende-crochets -- LA LEGENDE DES CROCHETS ET DES PATTERNS, GENEREE.

POURQUOI. Le canal du user (`user-demandes/user-demandes.md`) porte sa legende
dans son HEAD, sous les yeux de celui qui ecrit la demande. Cette legende
donne trois choses : les PATTERNS d etape (ou en est ma demande), les CROCHETS
(ce que je demande, ce que ca declenche), et la regle de l accord entre les
deux. Une legende recopiee est une legende qui vieillit : un crochet ajoute a la
table des patrons et absent de la legende met la demande dans une file
differente de celle qu elle annonce, et rien ne le dit.

ELLE EST GENEREE, ET DEPUIS LES DOMICILES.
- les PATTERNS viennent de `ETATS`, dans `matrice/data/commun/passerelle_user.py` ;
- la liste des CROCHETS vient de `CROCHETS_TYPES`, au MEME domicile.
Ce qui n est PAS genere : les DESCRIPTIONS. Elles sont de la prose du createur,
elles vivent dans cette porte, et la porte les CONTROLE contre les tables --
c est le seul endroit ou le controle est possible, puisque c est le seul endroit
ou les deux moities sont reunies.

TROIS REFUS, ET ILS SONT CHOISIS.
- un CROCHET DE LA TABLE SANS DESCRIPTION : le crochet est declare par le code,
  il n existe donc pas de demande qui le declenche correctement. On ne le
  rendrait pas muet ;
- une DESCRIPTION ORPHELINE : une description pour un crochet que la table ne
  declare plus est une description qui ment au user ;
- un `.md` DERIVE QUI N EST PAS A JOUR : la porte verifie par defaut et n
  ecrit rien. Regenerer sans le dire effacerait la preuve que la legende
  s etait decalee.

Usage:
  python legende-crochets.py                 (verifie : le .md est-il a jour ?)
  python legende-crochets.py --ecrire        (regenere les blocs, sortie a publier)
  python legende-crochets.py --sortie <f>    (nom du fichier produit par --ecrire)
  python legende-crochets.py --auto-test     (cobaye sur tables fabriquees)
  code 0 = a jour (ou ecrit) ; 1 = le .md derive n est pas a jour ; 2 = refus.
"""
import argparse
import sys
from pathlib import Path

NL = chr(10)  # le retour a la ligne par le CODE : une barre oblique
#dans un litteral est une echappement, pas un saut de ligne.

# --- LES DESCRIPTIONS : prose du createur, calees sur les tables ---------------
DESCRIPTIONS_CROCHETS = (
    ("mission", "construire, creer ou corriger", "le travail part en CONSTRUCTION"),
    ("tache", "une commande a executer",
     "une tache : corriger, mesurer ou construire"),
    ("revision", "revoir l existant et le dire AVANT d ecrire", "revision de l existant"),
    ("question", "une reponse, sans construire", "une reponse, avant toute construction"),
    ("audit", "un etat des lieux, lecture seule", "un rapport, aucune reparation"),
    ("???", "tu ne sais pas encore ce qu il faut faire",
     "un CADRAGE : la liste des actions est preparee avant le travail"),
    ("preparer", "preparer, cadrer ou planifier", "une preparation"),
    ("preparation", "idem [preparer]", "une preparation"),
    ("cablage", "sur une demande ancienne : verifier son CABLAGE",
     "controle du cablage"),
    ("investigation",
     "sur une demande ancienne : verifier qu elle a abouti ET qu elle est "
     "fonctionnelle, puis certifier", "investigation, puis certification"),
    ("crochet", "creer, corriger ou retirer un mot entre crochets",
     "le PROCESS de fabrication, injecte par le pilote"),
)
DESCRIPTIONS_ETATS = (
    ("A-FAIRE", "a faire : rien n a encore ete vu"),
    ("FAIT", "vu et execute"),
    ("A-CONTROLER", "execute, mais pas encore controle, valide ou certifie"),
    ("CERTIFIER", "fait, controle et certifie"),
)

# Les deux blocs, dans l ordre du canal. Les JUGES sont nommes par le canal.
DEBUT = "<!-- CROCHETS:DEBUT -->"
FIN = "<!-- CROCHETS:FIN -->"
NOM_CANAL = "user-demandes/user-demandes.md"

# --- LA RACINE, par MARQUEUR ---------------------------------------------------
RACINE = None
_courant = Path(__file__).resolve().parent
for _ in range(30):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        RACINE = _courant
        break
    _courant = _courant.parent
RACINE_INTROUVABLE = ("Racine matrix/ introuvable en remontant depuis "
                      + str(Path(__file__).resolve().parent))


def lire_tables(racine):
    """Les tables viennent du DOMICILE COMMUN, jamais d une copie locale."""
    commun = racine / "matrice" / "data" / "commun"
    if not commun.is_dir():
        return None, "domicile INTROUVABLE : " + str(commun)
    sys.path.insert(0, str(commun))
    try:
        from passerelle_user import CROCHETS_TYPES, ETATS
    except (OSError, ImportError) as erreur:
        return None, "IMPORT IMPOSSIBLE : " + type(erreur).__name__
    return (CROCHETS_TYPES, ETATS), ""


def controler_coherence(crochets, etats, descriptions_crochets, descriptions_etats):
    """LES TROIS REFUS. Rend la liste des fautes, vide si tout concorde."""
    fautes = []
    nommes = {nom for nom, _a, _b in descriptions_crochets}
    for crochet in sorted(crochets):
        if crochet not in nommes:
            fautes.append("CROCHET DECLARE SANS DESCRIPTION : `" + crochet
                          + "` est dans CROCHETS_TYPES et nowhere dans la legende")
    for nom, _a, _b in descriptions_crochets:
        if nom not in crochets:
            fautes.append("DESCRIPTION ORPHELINE : `" + nom
                          + "` a une description mais n est plus dans CROCHETS_TYPES")
    nommes_etats = {nom for nom, _d in descriptions_etats}
    for etat in sorted(etats):
        if etat not in nommes_etats:
            fautes.append("PATTERN DECLARE SANS SIGNIFICATION : `" + etat
                          + "` est dans ETATS et pas dans la legende")
    for nom, _d in descriptions_etats:
        if nom not in etats:
            fautes.append("SIGNIFICATION ORPHELINE : `" + nom
                          + "` a une signification mais n est plus dans ETATS")
    return fautes


def bloc_patterns(etats, descriptions_etats):
    """Les patterns dans l ORDRE DE LECTURE, pas dans l ordre d un ensemble.

    Une table est un dict : iterer sur elle donne un ordre qui n est celui
    d AUCUNE lecture. L ordre vient donc des DESCRIPTIONS (la prose du
    createur), et la table ne fait que valider.
    """
    lignes = [DEBUT,
              "| Pattern | Ce qu il signifie |",
              "|---|---|"]
    for nom, description in descriptions_etats:
        if nom in etats:
            lignes.append("| `##" + nom + "###` | " + description + " |")
    lignes.append(FIN)
    # PAS de saut de ligne apres le juge : le canal ecrit son FIN puis change
    # de ligne lui-meme, et un saut de plus decalerait tout ce qui suit.
    return NL.join(lignes)


def bloc_crochets(crochets, descriptions_crochets):
    """Meme discipline : l ordre est celui de la PROSE, la table valide."""
    lignes = [DEBUT,
              "| Crochet | Ce que tu demandes | Ce que ca declenche |",
              "|---|---|---|"]
    declares = set(crochets)
    for nom, demande, declenche in descriptions_crochets:
        if nom in declares:
            lignes.append("| `[" + nom + "]` | " + demande + " | " + declenche + " |")
    lignes.append(FIN)
    # PAS de saut de ligne apres le juge : le canal ecrit son FIN puis change
    # de ligne lui-meme, et un saut de plus decalerait tout ce qui suit.
    return NL.join(lignes)
def channeliser(texte, remplacement):
    """LE CANAL EST DU USER : on ne le reecrit pas, on rend ses blocs.

    C est le TEXTE DU CANAL qui decide ou sont les juges : la porte ne place
    rien la ou elle ne Salt pas. Un bloc absent est un refus nomme.
    """
    if DEBUT not in texte or FIN not in texte:
        return None, ("le canal ne porte pas les deux juges " + DEBUT + " / " + FIN)
    morceaux = []
    curseur = 0
    while True:
        debut = texte.find(DEBUT, curseur)
        if debut < 0:
            morceaux.append(texte[curseur:])
            break
        fin = texte.find(FIN, debut)
        if fin < 0:
            return None, DEBUT + " sans son " + FIN
        morceaux.append(texte[curseur:debut])
        morceaux.append(remplacement)
        curseur = fin + len(FIN)
    return "".join(morceaux), ""



def main(argv=None):
    analyseur = argparse.ArgumentParser(
        description="La legende des crochets et des patterns, generee.")
    analyseur.add_argument("--ecrire", action="store_true",
                            help="regenere les blocs (sortie a publier)")
    analyseur.add_argument("--sortie", default="",
                            help="nom du fichier produit par --ecrire")
    analyseur.add_argument("--auto-test", action="store_true",
                            help="cobaye sur tables fabriquees")
    arguments = analyseur.parse_args(argv)
    if RACINE is None:
        print(RACINE_INTROUVABLE)
        return 2
    if arguments.auto_test:
        return auto_test()
    tables, echec = lire_tables(RACINE)
    if echec:
        print("REFUS : " + echec)
        return 2
    crochets, etats = tables
    fautes = controler_coherence(crochets, etats, DESCRIPTIONS_CROCHETS,
                                 DESCRIPTIONS_ETATS)
    for faute in fautes:
        print("REFUS : " + faute)
    if fautes:
        return 2
    # Le canal est sous `matrix/`, comme tout le reste : le chercher a la racine
    # du WORKSPACE le declarait INTROUVABLE alors qu il existe, et un refus
    # faux fait croire que la legende n a pas de source.
    canal = RACINE / NOM_CANAL
    if not canal.is_file():
        print("REFUS : canal INTROUVABLE : " + str(canal))
        return 2
    motifs = [bloc_patterns(etats, DESCRIPTIONS_ETATS),
              bloc_crochets(crochets, DESCRIPTIONS_CROCHETS)]
    indices = []
    texte = canal.read_text(encoding="utf-8")
    curseur = 0
    for _ in range(2):
        debut = texte.find(DEBUT, curseur)
        if debut < 0:
            print("REFUS : le canal ne porte pas " + DEBUT)
            return 2
        fin = texte.find(FIN, debut) + len(FIN)
        indices.append((debut, fin))
        curseur = fin
    a_jour = True
    for motif, (debut, fin) in zip(motifs, indices):
        if texte[debut:fin] != motif:
            a_jour = False
            if not arguments.ecrire:
                print("PERIME : le bloc du canal ne colle plus a sa table"
                      " (il faut --ecrire).")
    if not a_jour and not arguments.ecrire:
        return 1
    if not arguments.ecrire:
        print("a jour : les deux blocs collent a leur table.")
        return 0
    sortie = "\n".join(motifs)
    if arguments.sortie:
        chemin = RACINE / arguments.sortie
        chemin.write_text(sortie, encoding="utf-8", newline="")
        print("ecrit : " + str(chemin))
        return 0
    print(sortie, end="")
    return 0


# --- L AUTO-TEST ---------------------------------------------------------------

def auto_test():
    """Cinq assertions sur des tables FABRIQUES, dont un CONTRE-TEMOIN reel."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    crochets = {"mission": "dev", "question": "question", "controle": "audit"}
    etats = ("A-FAIRE", "FAIT")

    # 1. LE CONTRE-TEMOIN REEL : un crochet de la table SANS description est
    #    REFUSE et NOMME -- c est l accident que la porte existe pour attraper.
    fautes = controler_coherence(crochets, etats, DESCRIPTIONS_CROCHETS,
                                 DESCRIPTIONS_ETATS)
    controler("un crochet declare sans description est REFUSE et nomme",
              any("`controle`" in faute and "SANS DESCRIPTION" in faute
                  for faute in fautes), fautes)

    # 2. UNE DESCRIPTION ORPHELINE EST REFUSEE (le crochet a disparu de la table).
    fautes = controler_coherence({"mission": "dev"}, etats, DESCRIPTIONS_CROCHETS,
                                 DESCRIPTIONS_ETATS)
    controler("une description orpheline est refusee",
              any("ORPHELINE" in faute for faute in fautes))

    # 3. LES TABLES CONCORDANTES NE PRODUISENT AUCUNE FAUTE.
    complet = {nom: "" for nom, _a, _b in DESCRIPTIONS_CROCHETS}
    tous_etats = {nom: "" for nom, _d in DESCRIPTIONS_ETATS}
    controler("des tables concordantes ne produisent aucune faute",
              controler_coherence(complet, tous_etats, DESCRIPTIONS_CROCHETS,
                                  DESCRIPTIONS_ETATS) == [])

    # 4. LE BLOC EST GENERE : il porte un crochet de la table, pas une recopie.
    bloc = bloc_crochets(complet, DESCRIPTIONS_CROCHETS)
    controler("le bloc genere porte tous les crochets declares",
              all("[" + nom + "]" in bloc for nom in complet), bloc[:200])
    controler("le bloc des patterns est genere depuis ETATS",
              "##FAIT###" in bloc_patterns(tous_etats, DESCRIPTIONS_ETATS))

    # 5. UN CANAL SANS LES JUGES EST UN REFUS, ET LA SORTIE EST INCHANGEE.
    rendu, echec = channeliser("avant" + DEBUT + "corps" + FIN + "apres",
                               bloc)
    controler("le canal n est reecrit que dans ses deux blocs",
              rendu == "avant" + bloc + "apres" and not echec, rendu[:200])
    _rendu, echec = channeliser("pas de juge ici", bloc)
    controler("un canal sans les juges est un refus nomme",
              bool(echec) and "juges" in echec, echec)

    reussis = sum(1 for _n, ok, _d in resultats if ok)
    for nom, ok, detail in resultats:
        print(("  [OK] " if ok else "  [KO] ") + nom
              + ("" if ok else " : " + str(detail)[:200]))
    print("AUTO-TEST : " + str(reussis) + "/" + str(len(resultats)) + ".")
    return 0 if reussis == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
