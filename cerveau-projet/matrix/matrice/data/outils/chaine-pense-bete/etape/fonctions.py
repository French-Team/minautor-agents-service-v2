"""Fonctions de la categorie etape : naitre, avancer, etat (EO-215, MO-224).

LA CHAINE : un objet, TROIS etapes. L'AVANCEMENT est pose ICI, par la porte,
des que les conditions tiennent -- la trace NEMESIS est une CONDITION LUE.
"""
from pathlib import Path

from commun import (
    horodater,
    a_trace_nemesis,
    ajouter_a_index,
    charger_compteurs,
    corps_du_document,
    document_par_identifiant,
    ecrire_par_la_porte,
    enregistrer_compteurs,
    identifiant_suivant,
    poser_champ,
    retirer_champ,
    rafraichir_index,
    titre_vers_slug,
    valeur_carte,
)
from constants import (
    CHAMPS_ETAPE,
    CHAMP_EXECUTE_LE,
    CHAMP_PREUVE,
    CHAMP_STATUT,
    CHAMP_TITRE,
    ENCODAGE,
    ETAPE_EXECUTE,
    ETAPE_PENSE_BETE,
    ETAPE_TODO,
    ETAPES,
    ETAPES_AVANCEMENT,
    EXTENSION,
    MESSAGE_AVANCE,
    MESSAGE_EXECUTE,
    MESSAGE_RETOUR,
    MESSAGE_NAISSANCE,
    MIN_LIGNES_CORPS,
    NEMESIS_EXIGE_A_PARTIR_DE,
    NOM_INDEX,
    PREFIXES,
    REFUS_DEJA_EXECUTE,
    REFUS_DERNIERE,
    REFUS_PAS_EXECUTE,
    REFUS_PAS_TODO,
    REFUS_PREUVE_INTROUVABLE,
    REFUS_PREUVE_NON_NOMMEE,
    REFUS_PREUVE_VIDE,
    REFUS_TODO_ABSENT,
    REFUS_HORS_PERIMETRE,
    REFUS_INTROUVABLE,
    REFUS_NEMESIS,
    REFUS_STRUCTURE,
    REPERTOIRE_DOMICILE,
    SEPARATEUR_CARTE,
    STATUT_INITIAL,
)

NOM_OUTIL = "chaine-pense-bete"
NOMS_OPTIONS_NAITRE = ("titre", "objectif")
NOMS_OPTIONS_AVANCER = ("id",)
NOMS_OPTIONS_EXECUTER = ("id", "preuve")
NOMS_OPTIONS_REVENIR = ("id",)
USAGE_NAITRE = "chaine-pense-bete naitre --titre \"...\" [--objectif \"...\"]"
USAGE_AVANCER = "chaine-pense-bete avancer --id PB-001"
USAGE_EXECUTER = "chaine-pense-bete executer --id PB-001 --preuve <chemin>"
USAGE_REVENIR = "chaine-pense-bete revenir --id PB-001"
USAGE_ETAT = "chaine-pense-bete etat [--id PB-001]"


def _options(arguments, noms_connus, usage):
    """Consomme le PARSEUR PARTAGE (data/commun/options.py) : jamais une copie."""
    from options import extraire_options, signaler_inconnues
    options = extraire_options(arguments, noms_connus)
    return options, signaler_inconnues(options, NOM_OUTIL, noms_connus, usage)


def executer_etape(arguments):
    """Le VERBE traite : main.py l'a valide, il n'est jamais devine ici."""
    if arguments[0] == "naitre":
        return naitre(arguments)
    if arguments[0] == "avancer":
        return avancer(arguments)
    if arguments[0] == "executer":
        return executer(arguments)
    if arguments[0] == "revenir":
        return revenir(arguments)
    return etat(arguments)


def _document_initial(titre, identifiant, objectif):
    """Le document d'un pense-bete : carte complete + corps minimal."""
    lignes = [
        SEPARATEUR_CARTE,
        "identite:",
        "  type: chaine",
        "  appartient_a: optimus-prime",
        "  commun: false",
        "  " + CHAMP_TITRE + " " + titre,
        "  " + CHAMP_STATUT + " " + STATUT_INITIAL,
        "  " + CHAMPS_ETAPE[ETAPE_PENSE_BETE] + " " + identifiant,
        SEPARATEUR_CARTE,
        "",
        "# " + titre,
        "",
        "## Pense-bete -- la demande clarifiee",
        "",
        objectif or "(a clarifier)",
        "",
        "## Ce qui est deja mesure",
        "",
        "(a ecrire)",
        "",
        "## Ce qui reste a mesurer",
        "",
        "(a ecrire)",
        "",
    ]
    return "\n".join(lignes) + "\n"


def naitre(arguments):
    """Ouvre l'ETAPE 1 (pense-bete) au domicile du createur (A1)."""
    if not REPERTOIRE_DOMICILE.is_dir():
        print(REFUS_HORS_PERIMETRE + str(REPERTOIRE_DOMICILE))
        return 2
    options, code = _options(arguments, NOMS_OPTIONS_NAITRE, USAGE_NAITRE)
    if code:
        return code
    titre = (options.get("titre") or "").strip()
    if not titre:
        print(USAGE_NAITRE)
        return 2
    compteurs = charger_compteurs()
    identifiant = identifiant_suivant(compteurs, ETAPE_PENSE_BETE)
    nom = "chaine-" + titre_vers_slug(titre) + EXTENSION
    contenu = _document_initial(titre, identifiant, (options.get("objectif") or "").strip())
    code, sortie = ecrire_par_la_porte(REPERTOIRE_DOMICILE / nom, contenu, "creer")
    if code:
        print(sortie.strip())
        return code
    compteurs[PREFIXES[ETAPE_PENSE_BETE]] += 1
    enregistrer_compteurs(compteurs)
    ajouter_a_index(nom, identifiant, titre, STATUT_INITIAL)
    print(MESSAGE_NAISSANCE + identifiant + " (" + nom + ")")
    return 0


def _etape_suivante(etape):
    """L etape de PRODUCTION qui suit, ou None -- jamais devinee au-dela.

    `avancer` parcourt `ETAPES_AVANCEMENT`, pas `ETAPES` (MO-577). Les trois
    premieres etapes sont une production de documents ; l etat d execution a son
    propre verbe et sa PROPRE CONDITION -- une preuve constatee sur le disque. Si
    `avancer` franchissait `todo` tout seul, le defaut qu on repare (un statut pose
    sans fait) reviendrait par la porte d avant.
    """
    if etape not in ETAPES_AVANCEMENT:
        return None
    index = ETAPES_AVANCEMENT.index(etape)
    return (ETAPES_AVANCEMENT[index + 1]
            if index + 1 < len(ETAPES_AVANCEMENT) else None)


def _condition_manquante(texte, etape):
    """Le REFUS le plus precis d'abord : structure, puis la trace NEMESIS."""
    if len(corps_du_document(texte)) < MIN_LIGNES_CORPS:
        return REFUS_STRUCTURE
    if ETAPES.index(etape) >= ETAPES.index(NEMESIS_EXIGE_A_PARTIR_DE) and not a_trace_nemesis(texte):
        return REFUS_NEMESIS
    return ""


def avancer(arguments):
    """Pose l'etape suivante SI les conditions tiennent -- et elles sont LUES."""
    options, code = _options(arguments, NOMS_OPTIONS_AVANCER, USAGE_AVANCER)
    if code:
        return code
    identifiant = (options.get("id") or "").strip()
    if not identifiant:
        print(USAGE_AVANCER)
        return 2
    chemin, texte = document_par_identifiant(identifiant)
    if chemin is None:
        print(REFUS_INTROUVABLE + identifiant)
        return 2
    etape = valeur_carte(texte, CHAMP_STATUT)
    suivante = _etape_suivante(etape)
    if suivante is None:
        print(REFUS_DERNIERE)
        return 2
    refus = _condition_manquante(texte, etape)
    if refus:
        print(refus)
        return 2
    compteurs = charger_compteurs()
    nouvel_id = identifiant_suivant(compteurs, suivante)
    texte = poser_champ(texte, CHAMPS_ETAPE[suivante], nouvel_id)
    texte = poser_champ(texte, CHAMP_STATUT, suivante)
    code, sortie = ecrire_par_la_porte(chemin, texte, "remplacer")
    if code:
        print(sortie.strip())
        return code
    compteurs[PREFIXES[suivante]] += 1
    rafraichir_index(chemin.name, identifiant, valeur_carte(texte, CHAMP_TITRE), suivante)
    enregistrer_compteurs(compteurs)
    print(MESSAGE_AVANCE + identifiant + " -> " + suivante + " (" + nouvel_id + ")")
    return 0


def _preuve_constatee(chemin_preuve):
    """(code, message) : la preuve est-elle un FAIT sur le disque ?

    LA PORTE NE JUGE PAS L ACCOMPLISSEMENT : elle constate qu un fichier existe et
    qu il n est pas vide. C est la limite assumee du modele -- un `execute` pose
    la-dessus dit "ce fichier existe", pas "ce travail est bon". Trois refus
    distincts parce que trois manques different : non nommee (rien n a ete dit),
    introuvable (dit, absent du disque), vide (present, sans contenu). Un refus
    unique obligerait a deviner lequel des trois est survenu.
    """
    if not chemin_preuve:
        return 2, REFUS_PREUVE_NON_NOMMEE
    chemin = Path(chemin_preuve)
    if not chemin.is_file():
        return 2, REFUS_PREUVE_INTROUVABLE + str(chemin)
    try:
        contenu = chemin.read_text(encoding=ENCODAGE)
    except (OSError, UnicodeDecodeError) as erreur:
        return 2, REFUS_PREUVE_INTROUVABLE + str(chemin) + " (" + type(erreur).__name__ + ")"
    if not contenu.strip():
        return 2, REFUS_PREUVE_VIDE + str(chemin)
    return 0, ""


def executer(arguments):
    """L etat EXECUTE -- pose SEULEMENT sur une preuve constatee (MO-577)."""
    options, code = _options(arguments, NOMS_OPTIONS_EXECUTER, USAGE_EXECUTER)
    if code:
        return code
    identifiant = (options.get("id") or "").strip()
    if not identifiant:
        print(USAGE_EXECUTER)
        return 2
    chemin, texte = document_par_identifiant(identifiant)
    if chemin is None:
        print(REFUS_INTROUVABLE + identifiant)
        return 2
    etape = valeur_carte(texte, CHAMP_STATUT)
    if etape == ETAPE_EXECUTE:
        print(REFUS_DEJA_EXECUTE + valeur_carte(texte, CHAMP_EXECUTE_LE) + ")")
        return 2
    if etape != ETAPE_TODO:
        print(REFUS_PAS_TODO + etape + chr(34))
        return 2
    if not valeur_carte(texte, CHAMPS_ETAPE[ETAPE_TODO]):
        print(REFUS_TODO_ABSENT)
        return 2
    chemin_preuve = (options.get("preuve") or "").strip()
    code_preuve, message = _preuve_constatee(chemin_preuve)
    if code_preuve:
        print(message)
        return code_preuve
    compteurs = charger_compteurs()
    nouvel_id = identifiant_suivant(compteurs, ETAPE_EXECUTE)
    texte = poser_champ(texte, CHAMPS_ETAPE[ETAPE_EXECUTE], nouvel_id)
    texte = poser_champ(texte, CHAMP_PREUVE, chemin_preuve)
    texte = poser_champ(texte, CHAMP_EXECUTE_LE, horodater())
    texte = poser_champ(texte, CHAMP_STATUT, ETAPE_EXECUTE)
    code, sortie = ecrire_par_la_porte(chemin, texte, "remplacer")
    if code:
        print(sortie.strip())
        return code
    compteurs[PREFIXES[ETAPE_EXECUTE]] += 1
    enregistrer_compteurs(compteurs)
    rafraichir_index(chemin.name, identifiant, valeur_carte(texte, CHAMP_TITRE), ETAPE_EXECUTE)
    print(MESSAGE_EXECUTE + identifiant + " -> " + ETAPE_EXECUTE + " (" + nouvel_id
          + ") -- preuve : " + chemin_preuve)
    return 0


def revenir(arguments):
    """LE RETOUR : un `execute` se DEFait. Une porte qui ne sait que poser n est pas
    reversible, donc tout ce qu elle pose est dans le sens unique -- et ce qui est
    dans le sens unique finit par avoir tort.

    Le champ `execute:` est RETIRE avec le statut : le controle des chaines lit
    chaque champ d etape comme un identifiant et refuse un objet dont un id
    d etape posterieure au statut est encore present. Revenir sans le retirer
    produirait donc un objet que le controle accuse -- et l agent aurait raison de
    se fier a ce refus.
    """
    options, code = _options(arguments, NOMS_OPTIONS_REVENIR, USAGE_REVENIR)
    if code:
        return code
    identifiant = (options.get("id") or "").strip()
    if not identifiant:
        print(USAGE_REVENIR)
        return 2
    chemin, texte = document_par_identifiant(identifiant)
    if chemin is None:
        print(REFUS_INTROUVABLE + identifiant)
        return 2
    if valeur_carte(texte, CHAMP_STATUT) != ETAPE_EXECUTE:
        print(REFUS_PAS_EXECUTE + valeur_carte(texte, CHAMP_STATUT) + chr(34))
        return 2
    for champ in (CHAMPS_ETAPE[ETAPE_EXECUTE], CHAMP_PREUVE, CHAMP_EXECUTE_LE):
        texte = retirer_champ(texte, champ)
    texte = poser_champ(texte, CHAMP_STATUT, ETAPE_TODO)
    code, sortie = ecrire_par_la_porte(chemin, texte, "remplacer")
    if code:
        print(sortie.strip())
        return code
    rafraichir_index(chemin.name, identifiant, valeur_carte(texte, CHAMP_TITRE), ETAPE_TODO)
    print(MESSAGE_RETOUR + identifiant + " -> " + ETAPE_TODO)
    return 0


def etat(arguments):
    """Ce qui EXISTE : l'index du domicile, ou le detail d'un objet."""
    options, code = _options(arguments, ("id",), USAGE_ETAT)
    if code:
        return code
    identifiant = (options.get("id") or "").strip()
    if identifiant:
        chemin, texte = document_par_identifiant(identifiant)
        if chemin is None:
            print(REFUS_INTROUVABLE + identifiant)
            return 2
        print("Document : " + chemin.name)
        print("  " + CHAMP_STATUT + " " + valeur_carte(texte, CHAMP_STATUT))
        for etape in ETAPES:
            valeur = valeur_carte(texte, CHAMPS_ETAPE[etape])
            if valeur:
                print("  " + etape + " : " + valeur)
        if valeur_carte(texte, CHAMP_EXECUTE_LE):
            print("  preuve : " + valeur_carte(texte, CHAMP_PREUVE))
            print("  execute le : " + valeur_carte(texte, CHAMP_EXECUTE_LE))
        print("  nemesis : " + ("oui" if a_trace_nemesis(texte) else "non"))
        return 0
    index = REPERTOIRE_DOMICILE / NOM_INDEX
    if not index.is_file():
        print("aucun objet dans la chaine (index absent : " + NOM_INDEX + ")")
        return 0
    print(index.read_text(encoding=ENCODAGE).strip())
    return 0
