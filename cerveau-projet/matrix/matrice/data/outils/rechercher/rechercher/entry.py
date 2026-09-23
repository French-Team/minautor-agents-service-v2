"""Entree du verbe rechercher : moteur de recherche unifie (fichiers + BDD).

Contrat de la porte (MO-069) :
- une option de FILTRE filtre vraiment (--tag, --mot-cle, --source, --periode) ;
- une option illisible est REFUSEE (code 2), jamais ignoree en silence ;
- une coupe (troncature) et un ecart (entree sans date) sont DITS dans les deux
  sorties (humaine et --json) : un resultat muet sur ses propres limites ment ;
- la sortie --json est en ASCII pur (ensure_ascii) : une console cp1252 ne peut
  plus faire echouer la porte ;
- une option qui ne s'applique pas au mode demande est REFUSEE, jamais ignoree
  (--prive ne vaut que pour les fichiers) ;
- le perimetre du scan est DIT quand il sort de l'ordinaire : --prive inclut les
  zones L-016, et la sortie le declare (EO-126).

DEUX FACONS DE CHERCHER (2026-09-21, demande createur) :
- par TEXTE (`--requete`) : rend des LIGNES (et des NOMS de fichiers) ;
- par CARTE (`--champ`) : rend des DOCUMENTS -- ceux dont la CARTE D'IDENTITE
  porte TOUS les champs demandes. La grammaire de la carte vit dans son domicile
  (matrice/data/commun/carte_identite.py), pas ici.
  `--champ` prend UNE valeur groupee (`cle=valeur[;cle=valeur]`, le `:` valant le
  `=`) : le parseur partage garde une valeur par nom d'option, donc une option
  REPETEE serait ecrasee en silence -- elle est REFUSEE, avec la syntaxe.
  Le rapport DIT le perimetre de la reponse (documents lus, avec/sans carte,
  exclus invisibles L-016, troncature) : un document SANS carte ne peut pas
  repondre a une combinaison, et le taire ferait passer un corpus incomplet pour
  un "0 resultat".
"""
import sys
import os

# Ajoute le repertoire courant au path pour les imports locaux
# L-013 : aucun niveau compte a la main. Le dossier de CET outil est celui qui
# porte son commun.py (marqueur) : la remontee est VERIFIEE, jamais supposee (MO-177).
REPERTOIRE_ENTREE = os.path.dirname(os.path.abspath(__file__))
REPERTOIRE_OUTIL = os.path.dirname(REPERTOIRE_ENTREE)
if not os.path.isfile(os.path.join(REPERTOIRE_OUTIL, "commun.py")):
    raise RuntimeError("Dossier de l'outil introuvable depuis " + REPERTOIRE_ENTREE
                       + " : commun.py est absent de " + REPERTOIRE_OUTIL)
sys.path.insert(0, REPERTOIRE_OUTIL)

from commun import (
    scanner_cartes,
    scanner_fichiers,
    scanner_bdd,
    filtrer_par_periode,
    formatter_hit,
    extraire_options,
    periode_valide,
    signaler_inconnues,
)
from constants import (
    BDD_SOURCES,
    DANS_VALEURS,
    DEFAUT_DANS,
    LIMITE_DEFAUT,
    LIMITE_FICHIERS,
    LIMITE_LIGNES_JSONL,
    NOM_OPTION_CHAMP,
    NOM_OPTION_JSON,
    NOM_OPTION_PRIVE,
    NOMS_OPTIONS_RECHERCHER,
)

# La grammaire de la carte (domicile data/commun/carte_identite.py) : cette porte
# la CONSOMME -- cles du corpus et valeurs vues servent au REFUS NOMME, jamais a
# une liste tenue ici (mesure 2026-09-21 : les cles libres d'une carte ne se
# devinent pas, elles se LISENT sur le corpus).
from carte_identite import (  # noqa: E402
    SEPARATEUR_DEMANDES,
    cles_du_corpus,
    demandes as demandes_de_carte,
    valeurs_vues,
)

# La liste des zones invisibles qui est AFFICHEE est la MEME que celle qui est
# APPLIQUEE : elle vient du domicile data/commun/invisibilite.py (plancher +
# zones DECLAREES V-003). Sans cela, la porte excluait les zones declarees tout
# en annoncant les trois historiques -- un message qui ment sur son perimetre
# (mesure MO-151, reparation MO-152).
from invisibilite import zones_exclues  # noqa: E402

# La liste est EVALUEE une fois : les trois usages (aide, sortie machine, message
# d ouverture) doivent dire la MEME chose que le filtre applique.
ZONES_INVISIBLES = zones_exclues()

# Options qui ne s'appliquent qu'aux BDD : les accepter sur --dans fichiers
# serait une option qui ne filtre rien (lecon EO-107).
OPTIONS_BDD = ("tag", "mot_cle", "source")


def rechercher(arguments):
    """Verbe rechercher : --requete [--dans] [--tag] [--mot-cle] [--source] [--periode] [--json] [--limite]

    Codes retour :
      0 = succes (au moins 1 hit)
      1 = aucun resultat (la recherche a abouti)
      2 = refus (option manquante, illisible ou hors perimetre d'application)
    """
    options = extraire_options(arguments, NOMS_OPTIONS_RECHERCHER)
    # EO-179 : cette porte DECLARE deja, en tete de fichier, qu une option
    # illisible est REFUSEE (code 2), jamais ignoree en silence -- ce n etait
    # vrai que du CONTENU. Une option INCONNUE (--dossier, --option-bidon) etait
    # SAUTEE : mesure du 2026-09-19, code 0 et balayage par DEFAUT, alors que
    # l appelant croyait avoir restreint sa recherche. Elle est desormais
    # REFUSEE, NOMMEE, avec les options reconnues et l usage.
    code_inconnues = signaler_inconnues(
        options, "rechercher", NOMS_OPTIONS_RECHERCHER,
        usage='Usage: rechercher --requete <texte> [--dans fichiers|bdd|tous]'
              ' [--tag ...] [--mot-cle ...] [--source ...] [--periode 30j]'
              ' [--limite N] [--json] [--prive]'
              ' | rechercher --champ "cle=valeur[;cle=valeur]" [--prive]')
    if code_inconnues != 0:
        return code_inconnues

    # Validation
    requete = options.get("requete", "").strip()

    # Une option REPETEE `--champ` serait ECRASEE en silence (le parseur partage
    # garde UNE valeur par nom) : le premier filtre disparaitrait sans un mot, et
    # l'appel croirait avoir restreint sa recherche. On la REFUSE, et on DIT la
    # syntaxe groupee (mesure 2026-09-21).
    if arguments.count("--" + NOM_OPTION_CHAMP) > 1:
        print("ERREUR : --" + NOM_OPTION_CHAMP + " ne se repete pas"
              " (l'option repetee serait ecrasee en silence).")
        print("  une seule valeur, champs groupes par " + SEPARATEUR_DEMANDES
              + " : --" + NOM_OPTION_CHAMP
              + " \"type=convention" + SEPARATEUR_DEMANDES
              + "appartient_a=optimus-prime\"")
        return 2

    champ_brut = options.get(NOM_OPTION_CHAMP, "").strip()
    couples = []
    if champ_brut:
        couples, illisibles = demandes_de_carte(champ_brut)
        if illisibles:
            print("ERREUR : --" + NOM_OPTION_CHAMP + " illisible : "
                  + ", ".join(illisibles))
            print("  forme attendue : --" + NOM_OPTION_CHAMP
                  + " \"cle=valeur" + SEPARATEUR_DEMANDES + "cle=valeur\""
                  " (le : vaut le =)")
            print("  ex : --" + NOM_OPTION_CHAMP
                  + " \"type=convention" + SEPARATEUR_DEMANDES
                  + "appartient_a=optimus-prime\"")
            return 2

    if not requete and not couples:
        print("ERREUR : --requete ou --champ requis. Ex: --requete \"defcon\"")
        print("Usage: rechercher --requete <texte> [--dans fichiers|bdd|tous]")
        print("       [--tag <tag>] [--mot-cle <texte>] [--source <nom>]")
        print("       [--periode 7j] [--json] [--limite N] [--prive]")
        print("       | rechercher --champ \"type=convention"
              + SEPARATEUR_DEMANDES + "appartient_a=optimus-prime\"")
        print("       --prive : inclut les zones invisibles L-016 ("
              + ", ".join(ZONES_INVISIBLES) + ")")
        return 2

    # Deux MODES de recherche : les melanger ne filtrerait pas ce que l'appelant
    # croit. Un filtre qui ne filtre pas est un affichage (lecon EO-107) : refuse,
    # et dit.
    if couples and requete:
        print("ERREUR : --requete (texte) et --" + NOM_OPTION_CHAMP
              + " (carte) sont DEUX modes de recherche distincts.")
        print("  --requete rend des LIGNES ; --" + NOM_OPTION_CHAMP
              + " rend des DOCUMENTS qui portent la carte.")
        print("  les combiner donnerait un filtre muet : lancez-les separement.")
        return 2

    dans = options.get("dans", DEFAUT_DANS)
    if dans not in DANS_VALEURS:
        print("ERREUR : --dans doit etre parmi " + ", ".join(DANS_VALEURS))
        return 2

    tag = options.get("tag", "").strip() or None
    mot_cle = options.get("mot_cle", "").strip() or None
    source_nom = options.get("source", "").strip() or None
    periode = options.get("periode", "").strip() or None
    mode_json = NOM_OPTION_JSON in options
    # --prive (EO-126) : drapeau, donc on lit sa PRESENCE, jamais une valeur.
    inclure_prive = NOM_OPTION_PRIVE in options

    # --source inconnue : REFUS qui nomme les sources valides (EO-109).
    # Une faute de frappe doit etre une erreur, pas un "0 resultat" muet.
    if source_nom and source_nom not in BDD_SOURCES:
        print("ERREUR : --source inconnue : " + source_nom)
        print("Sources valides : " + ", ".join(BDD_SOURCES))
        return 2

    # Un filtre BDD sur un scan de fichiers ne filtre rien : on le dit.
    if dans == "fichiers":
        for nom in OPTIONS_BDD:
            if options.get(nom, "").strip():
                print("ERREUR : --" + nom.replace("_", "-")
                      + " ne s'applique qu'aux BDD (--dans bdd ou tous).")
                return 2
    # Le pendant : une option de FICHIERS sur un scan de BDD ne filtre rien non
    # plus -- meme refus, meme raison (une option qui ne filtre pas est un
    # affichage).
    if inclure_prive and dans == "bdd":
        print("ERREUR : --" + NOM_OPTION_PRIVE
              + " ne s'applique qu'aux FICHIERS (--dans fichiers ou tous).")
        return 2
    # Le pendant pour la carte : les documents a carte sont des FICHIERS. Un
    # scan de BDD ne les sert pas -- l'accepter serait une option qui ne filtre
    # rien, et l'appel croirait avoir interroge les cartes (EO-107).
    if couples and dans == "bdd":
        print("ERREUR : --" + NOM_OPTION_CHAMP + " cherche des DOCUMENTS"
              " (cartes d'identite) ; --dans bdd ne les sert pas.")
        print("  utilisez --dans fichiers (defaut : " + DEFAUT_DANS + ").")
        return 2

    # --periode illisible : REFUS (un filtre temporel qui ne filtre pas est un
    # affichage -- EO-110).
    if periode and not periode_valide(periode):
        print("ERREUR : --periode attend <nombre><j|m|a> (ex: 7j, 30j, 3m, 1a).")
        return 2

    # --limite doit etre un entier positif (avant : int() levait une exception).
    limite_brute = options.get("limite", str(LIMITE_DEFAUT)).strip()
    if not limite_brute.isdigit() or int(limite_brute) <= 0:
        print("ERREUR : --limite attend un entier positif.")
        return 2
    limite = int(limite_brute)

    tous_hits = []
    sources_tronquees = []
    ecartes_sans_date = 0
    erreur_scan = ""
    rapport_carte = None

    # Scan par CARTE (combinaison de champs) : les DOCUMENTS repondent, et le
    # rapport DIT ce qu'il a lu et ce qu'il a retire. Le vocabulaire des champs
    # vient du CORPUS lu, jamais d'une liste supposee : un champ qu'aucune carte
    # ne porte est une faute de frappe, et elle est REFUSEE en nommant les champs
    # reels -- sinon l'appel lirait "0 resultat" comme un fait (L-055).
    if couples:
        hits_cartes, rapport_carte = scanner_cartes(couples, inclure_prive=inclure_prive)
        cles_vues = cles_du_corpus(rapport_carte["cartes"])
        inconnus = sorted({cle for cle, _ in couples if cle not in cles_vues})
        if inconnus:
            print("ERREUR : champ(s) INCONNU(S) du corpus scanne : " + ", ".join(inconnus))
            print("  champs reellement portes par les cartes : "
                  + (", ".join(sorted(cles_vues)) if cles_vues else "(aucune carte lue)"))
            print("  perimetre : " + str(rapport_carte["avec_carte"])
                  + " document(s) a carte lus sur " + str(rapport_carte["documents_lus"]))
            if rapport_carte["exclus_invisibles"]:
                print("  " + str(rapport_carte["exclus_invisibles"])
                      + " document(s) hors du perimetre L-016 ("
                      + str(len(ZONES_INVISIBLES)) + " zones declarees, dont "
                      + ", ".join(ZONES_INVISIBLES[:3]) + " ...) : --"
                      + NOM_OPTION_PRIVE + " les inclut.")
            return 2
        tous_hits.extend(hits_cartes)
        if periode:
            tous_hits, ecartes_cartes = filtrer_par_periode(tous_hits, periode)
            ecartes_sans_date += ecartes_cartes

    # Scan fichiers
    if not couples and dans in ("fichiers", "tous"):
        hits_fichiers, nb_f, limit_f, msg_f = scanner_fichiers(
            requete, inclure_prive=inclure_prive)
        if msg_f:
            erreur_scan = msg_f
        if periode:
            hits_fichiers, ecartes_f = filtrer_par_periode(hits_fichiers, periode)
            ecartes_sans_date += ecartes_f
        tous_hits.extend(hits_fichiers)

    # Scan BDD
    if not couples and dans in ("bdd", "tous"):
        hits_bdd, nb_b, limit_b, tronquees = scanner_bdd(
            requete, tag=tag, mot_cle=mot_cle, source_nom=source_nom
        )
        sources_tronquees.extend(tronquees)
        if periode:
            hits_bdd, ecartes_b = filtrer_par_periode(hits_bdd, periode)
            ecartes_sans_date += ecartes_b
        tous_hits.extend(hits_bdd)

    if erreur_scan:
        print("ERREUR : " + erreur_scan)
        return 2

    # Tri par score (BDD) puis fichier (par defaut)
    tous_hits.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Limite
    nb_total = len(tous_hits)
    if nb_total > limite:
        tous_hits = tous_hits[:limite]
        nb_limite = True
    else:
        nb_limite = False

    # Sortie
    if mode_json:
        import json
        resultat = {
            "requete": requete,
            "dans": dans,
            "trouve": nb_total,
            "retourne": len(tous_hits),
            "limite_atteinte": nb_limite,
            "tronque": sources_tronquees,
            "ecartes_sans_date": ecartes_sans_date,
            "filtres": {"tag": tag, "mot_cle": mot_cle, "source": source_nom,
                        "periode": periode,
                        "champs": [{"cle": cle, "valeur": valeur}
                                  for cle, valeur in couples]},
            # Le PERIMETRE du mode carte est DIT, chiffre : combien de documents
            # lus, combien a carte, combien sans carte (ils ne peuvent pas
            # repondre), combien ecartes par l'invisibilite L-016, troncature.
            "carte": rapport_carte,
            # L'etat du filtre L-016 est DIT : une sortie machine qui a inclus la
            # zone privee sans le dire ferait croire a un perimetre ordinaire.
            "prive": inclure_prive,
            "zones_invisibles": list(ZONES_INVISIBLES),
            "hits": tous_hits,
        }
        # ensure_ascii : la sortie machine reste de l'ASCII pur, encodable par
        # n'importe quelle console (EO-105).
        print(json.dumps(resultat, ensure_ascii=True, indent=2))
    else:
        if couples:
            print("Recherche par CARTE : "
                  + ", ".join(cle + "=" + valeur for cle, valeur in couples))
            print("Documents a carte : " + str(rapport_carte["avec_carte"])
                  + " / " + str(rapport_carte["documents_lus"]) + " lus"
                  + " | sans carte : " + str(rapport_carte["sans_carte"])
                  + " (un document sans carte ne peut pas repondre a une combinaison)")
            if rapport_carte["exclus_invisibles"]:
                print("Exclus invisibles L-016 : "
                      + str(rapport_carte["exclus_invisibles"]) + " document(s) ("
                      + str(len(ZONES_INVISIBLES)) + " zones declarees, dont "
                      + ", ".join(ZONES_INVISIBLES[:3]) + " ...) -- sans --"
                      + NOM_OPTION_PRIVE + ", ces zones restent invisibles.")
            if rapport_carte["hors_perimetre"]:
                print("Hors perimetre : " + str(rapport_carte["hors_perimetre"]))
            if rapport_carte["tronque"]:
                print("TRONQUE : " + str(LIMITE_FICHIERS) + " documents atteints --"
                      " le resultat est COUPE, pas complet.")
        else:
            print(f"Recherche : \"{requete}\" (dans {dans})")
        if tag or mot_cle or source_nom or periode:
            filtres_actifs = []
            if tag:
                filtres_actifs.append("tag=" + tag)
            if mot_cle:
                filtres_actifs.append("mot-cle=" + mot_cle)
            if source_nom:
                filtres_actifs.append("source=" + source_nom)
            if periode:
                filtres_actifs.append("periode=" + periode)
            print("Filtres : " + ", ".join(filtres_actifs))
        print(f"Trouves : {nb_total} | Retournes : {len(tous_hits)}")
        if inclure_prive:
            print("Zone privee INCLUSE (" + ", ".join(ZONES_INVISIBLES)
                  + ") -- sans --prive, ces zones restent invisibles.")
        if nb_limite:
            print(f"Limite atteinte ({limite})")
        if sources_tronquees:
            print("TRONQUE : source(s) coupee(s) a " + str(LIMITE_LIGNES_JSONL)
                  + " lignes : " + ", ".join(sources_tronquees))
        if ecartes_sans_date:
            print("ECARTES faute de date (periode " + str(periode) + ") : "
                  + str(ecartes_sans_date))
        print("")
        for i, h in enumerate(tous_hits):
            print(formatter_hit(h, i))
        if not tous_hits:
            # Un 0 MUET laisserait croire que rien n'existe. En mode carte, on DIT
            # quelles valeurs existent pour chaque champ demande : la difference
            # entre "ce document n'existe pas" et "je me suis trompe de valeur"
            # est decisionnelle.
            if couples and rapport_carte is not None:
                for cle, _ in couples:
                    vues = valeurs_vues(rapport_carte["cartes"], cle)
                    print("  " + cle + " : valeurs reellement portees -> "
                          + (", ".join(vues) if vues else "(aucune)"))
            print("  (aucun resultat)")

    return 0 if tous_hits else 1
