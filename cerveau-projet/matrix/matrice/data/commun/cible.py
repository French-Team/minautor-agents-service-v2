"""Le DOMICILE de la resolution d un CHEMIN DE CIBLE (argument d un outil).

Probleme fondamental (convention-chemins-liens-noms-flags, point 1.1) : un
chemin d argument resolu contre le CWD depend de QUI lance. Mesure du
2026-09-17 (friction 80) : sc-001 acceptait `--fichier <relatif a matrix/>`
lance depuis la racine, et REFUSAIT la MEME cible lancee depuis son propre
dossier -- deux verdicts pour un seul fichier, et un rouge qui accusait la
cible au lieu d accuser l ancrage.

Trois formes couvertes, dans CET ordre :
  1. chemin ABSOLU : tel quel, aucune base ;
  2. relatif a la RACINE du workspace (celle qui porte AGENTS.md) ;
  3. relatif a <racine>/cerveau-projet/matrix, puis <racine>/matrix.

Le cwd n est JAMAIS une base. Un refus NOMME les bases essayees : un refus qui
ne dit pas OU il a cherche coute trois essais (friction 77).

La racine est DETECTEE par le motif partage (racine.py, L-013) : ce module la
CONSOMME, il ne la recopie jamais (M-076 : une valeur recopiee derive en
silence ; L-100/L-102).

Ce module porte aussi le PERIMETRE : est-ce que ce chemin est DANS la Matrice ?
Cinq outils (la porte ecrire + les quatre lecteurs lire, lister, rechercher,
benchmark) posaient la meme question et y repondaient chacun a sa facon ; quatre
d entre eux jugeaient un PREFIXE (`matrix/...`) avant toute resolution, donc un
chemin declare dans le perimetre pouvait resoudre AILLEURS (MO-183/MO-184). La
regle vit ICI, une seule fois : est_dans_matrice + motif_hors_perimetre.
"""
import os
from pathlib import Path

from racine import detecter_racine

# Les deux formes reelles du depot : la Matrice vit sous cerveau-projet/matrix,
# et peut vivre directement sous la racine dans une installation depliee.
NOMS_MATRICE = ("cerveau-projet/matrix", "matrix")


def _racine_matrice_de(depart):
    """Le dossier de la MATRICE, deduit du motif partage (jamais d'un parents[N])."""
    racine = detecter_racine(depart)
    for nom in NOMS_MATRICE:
        candidat = racine / nom
        if candidat.is_dir():
            return candidat
    return racine


def forme_canonique(chemin, depart=None):
    """La FORME CANONIQUE d'un chemin de la Matrice : RELATIVE A SA RACINE.

    UN SEUL DOMICILE DE FORME (M-076) : les CLES de la BDD des modifications
    (EO-363) et les LIENS d'une carte d'identite (EO-347) sont la MEME question --
    < sous quelle forme un fichier de la Matrice se NOMME-t-il ? > -- et la
    reponse est ici, une fois.

    Mesure du 2026-09-22 (EO-363) : la BDD portait 935 cles = 232 prefixees
    < cerveau-projet/matrix/ > + 703 relatives, et 158 fichiers sous les DEUX
    formes -- donc DEUX histoires pour un seul fichier. La cause : la porte
    enregistrait la cle TELLE QU'ON LA LUI DONNAIT, et la forme dependait donc du
    repertoire courant de l'appelant. Un lien de carte a exactement le meme
    risque : une forme qui depend de qui l'ecrit ne se mesure ni ne se compare.

    Formes acceptees : un chemin ABSOLU dans la Matrice, une forme prefixee
    (un des NOMS_MATRICE), ou une forme deja relative. Idempotente : une forme
    canonique se rend ELLE-MEME. Un chemin HORS Matrice est rendu TEL QUEL -- on
    ne devine pas, l'appelant le DIT.
    """
    texte = str(chemin or "").strip().replace("\\", "/")
    while texte.startswith("./"):
        texte = texte[2:]
    if not texte:
        return ""
    brut = Path(texte)
    if brut.is_absolute():
        base = Path(os.path.normpath(str(_racine_matrice_de(depart or __file__))))
        try:
            return Path(os.path.normpath(str(brut))).relative_to(base).as_posix()
        except ValueError:
            return texte
    for nom in NOMS_MATRICE:
        if texte == nom:
            return ""
        if texte.startswith(nom + "/"):
            texte = texte[len(nom) + 1:]
            break
    return os.path.normpath(texte).replace("\\", "/")


def bases(depart):
    """Les bases d ancrage, dans l ordre : la racine du workspace, puis matrix/."""
    racine = detecter_racine(depart)
    return (racine,) + tuple(racine / nom for nom in NOMS_MATRICE)


NIVEAUX = ("matrice", "_operateur", "agents", "docs", "user-demandes")

# Ce qui distingue une CLE OSSUAIRE d une ancre posee : la forme est belle, le
# fichier n existe pas. Motif unique, ecrit ici, lu par tous (M-076).
MOTIF_OSSUAIRE = ("cle ORPHELINE : la forme normalisee ne designe AUCUN fichier "
                  "existant sous aucun niveau -- le fichier a disparu, ou la cle "
                  "a ete posee a la main : ")


def niveau_de_chemin(chemin, depart=None):
    """L ESCALIER : (cle ou None, forme sans niveau ou "", chemin absolu ou None).

    La forme d abord (un seul domicile, `forme_canonique`), puis on retire UN
    segment de tete a la fois et on teste l existence a chaque marche. On s
    arrete au premier fichier REEL trouve.

    POURQUOI RETIRER ET NON AJOUTER (mesure du 2026-10-04). On pourrait croire
    qu il faut DESCENDRE, essayer `racine/matrice/<forme>` puis
    `racine/_operateur/<forme>`. Sur la cle reelle
    `matrice/matrice/data/data-readme.md`, aucune de ces marches n existe : le
    fichier est a la racine et c est un NIVEAU EN TETE QUI DOIT TOMBER.

    DEUX GARDES, parce qu elles ne se valent pas. La forme qui designe deja un
    fichier est ACCEPTEE telle quelle, sans qu on la touche : une cle correcte
    ne bouge jamais. Un nom NU (sans separateur) suit la regle des noms nus, qui
    est celle de `chemin_de_cle` -- on ne la recopie pas ici (L-029).
    """
    forme = forme_canonique(chemin, depart)
    if not forme:
        return (None, "", None)
    base = racine_matrice(depart if depart is not None else __file__)
    if (base / forme).is_file():
        return (forme, forme, str(base / forme))
    if "/" not in forme:
        return (forme, "", str(base / forme))
    segments = forme.split("/")
    for taille in range(1, len(segments)):
        candidat = "/".join(segments[taille:])
        ancre = base / candidat
        if ancre.is_file():
            return (candidat, candidat, str(ancre))
    return (None, "", None)


def resoudre_escalier(chemin, depart=None):
    """(chemin absolu ou None, motif) : le refus NOMME les marches (friction 77)."""
    forme, sans_niveau, ancre = niveau_de_chemin(chemin, depart)
    if ancre is not None:
        detail = ("la forme designait deja un fichier"
                  if forme == sans_niveau
                  else "un niveau en trop a ete retire : " + repr(sans_niveau))
        return (ancre, "cible presente (" + detail + ") : " + ancre)
    base = racine_matrice(depart if depart is not None else __file__)
    # La forme rendue est la forme NORMALISEE, pas le resultat de l escalier --
    # qui vaut None a l echec. Un refus qui affiche `forme None` ne donne rien a
    # corriger a l appelant ; il montre donc ce qu il a ESSAYE, et combien de
    # marches ont ete remontees.
    normalisee = forme_canonique(chemin, depart)
    marches = len(str(normalisee).split("/")) if normalisee else 0
    return (None, MOTIF_OSSUAIRE + repr(str(chemin)) + " -- forme normalisee "
            + repr(normalisee) + " -- escalier monte sous " + str(base)
            + " : aucune des " + str(marches)
            + " marches possibles ne designe un fichier")


def resoudre(fichier, depart):
    """(chemin, motif) : ancre <fichier> sur la racine detectee depuis <depart>.

    Rend (None, motif) si la cible est introuvable -- et le motif NOMME alors
    les bases essayees, pour que l appelant puisse le dire tel quel.
    """
    brut = Path(str(fichier).strip())
    if not brut.name:
        return None, "cible vide (aucun chemin fourni)"
    if brut.is_absolute():
        if brut.exists():
            return brut, "cible presente : " + str(brut)
        return None, "cible INTROUVABLE : " + str(brut) + " (chemin absolu)"
    essayees = bases(depart)
    for base in essayees:
        candidat = base / brut
        if candidat.exists():
            return candidat, "cible presente : " + str(candidat)
    return None, (
        "cible INTROUVABLE : " + str(fichier) + " -- essaye sous "
        + ", ".join(str(base) for base in essayees)
        + " (le cwd n est JAMAIS une base : convention 1.1)"
    )


def racine_matrice(depart):
    """La racine de la MATRICE : le dossier qui porte `matrice/` et `_operateur/`.

    C est la base de travail des chemins de BDD (plan de conservation : chemins
    relatifs a la racine `matrix/`). Deux installations reelles : la Matrice vit
    sous `<racine>/cerveau-projet/matrix` (depot de developpement) ou directement
    sous `<racine>/matrix` (installation depliee). Si aucune n existe, on rend la
    racine du workspace : un appelant qui tenterait d ecrire DANS la Matrice sera
    refuse plus loin par le perimetre, jamais ici en silence.
    """
    racine = detecter_racine(depart)
    for nom in NOMS_MATRICE:
        candidat = racine / nom
        if candidat.is_dir():
            return candidat
    return racine


def resoudre_dans_matrice(fichier, depart):
    """(chemin, motif) : ancre une DESTINATION (cible A CREER) sur la Matrice.

    Pourquoi une fonction de plus que `resoudre` : `resoudre` exige que la cible
    EXISTE -- c est une verification de LECTURE. Une destination, elle, n existe
    pas encore ; mais elle n a qu UNE base possible et DECLAREE (la Matrice), la
    ou les sources se cherchent dans une liste de bases.

    Toute cible qui SORTIRAIT de la Matrice (chemin absolu dehors, ou `..`) est
    REFUSEE : c est le plan de conservation qui l exige (aucune operation hors de
    `matrix/`). Le refus NOMME la base, pour que l appelant puisse le dire tel quel.
    """
    base = racine_matrice(depart)
    brut = Path(str(fichier).strip())
    if not brut.name:
        return None, "destination vide (aucun chemin fourni)"
    candidat = brut if brut.is_absolute() else base / brut
    candidat = Path(os.path.normpath(str(candidat)))
    try:
        candidat.relative_to(base)
    except ValueError:
        return None, (
            "destination REFUSEE : " + str(fichier) + " sort de la Matrice ("
            + str(base) + ")"
        )
    return candidat, "destination dans la Matrice : " + str(candidat)


def racine_matrice_stricte(depart=None):
    """La racine de la Matrice, ou None si AUCUNE n a ete trouvee.

    Difference avec racine_matrice : celle-ci rend la racine du WORKSPACE en
    repli, ce qui est juste pour ANCRER une destination (on ecrira dans la
    Matrice si elle existe) mais FAUX pour JUGER un perimetre -- un perimetre
    dont la base serait la racine du workspace accepterait tout le workspace.
    Ici, AUCUN repli : None veut dire aucune Matrice, et l appelant REFUSE.
    """
    racine = detecter_racine(depart if depart is not None else __file__)
    for nom in NOMS_MATRICE:
        candidat = racine / nom
        if candidat.is_dir():
            return candidat
    return None


def est_dans_matrice(chemin, depart=None):
    """True si <chemin>, RESOLU, tombe SOUS la racine REELLE de la Matrice.

    MO-184 (EO-178) : des perimetres jugeaient un PREFIXE (`matrix/...`) avant
    toute resolution -- un chemin declare dans le perimetre pouvait donc resoudre
    AILLEURS (mesure MO-183 : la porte ecrire a cree une arborescence
    <racine>/matrix/ HORS de la Matrice). La regle vit ICI, une seule fois : les
    perimetres la CONSOMMENT au lieu de la recopier (M-076).
    """
    base = racine_matrice_stricte(depart)
    if base is None:
        return False
    try:
        Path(chemin).resolve().relative_to(Path(base).resolve())
        return True
    except (ValueError, OSError, RuntimeError):
        return False


# --- L ALLOWLIST DE LA RACINE DU WORKSPACE (decision, un seul domicile) ------
# DEUX fichiers APPARTIENNENT a la Matrice tout en vivant a la RACINE du
# workspace : AGENTS.md et demarrer-*.md. La porte ECRIRE les accepte depuis
# toujours, avec ses PROPRES constantes ; les AUTRES perimetres, non -- donc le
# fichier de demarrage etait MODIFIABLE mais pas ATTESTABLE (mesure MO-410 :
# benchmark `perimetre` et `bdd` ROUGES, note BDD avec EMPREINTE ABSENTE).
# La DECISION vit desormais ici, avec ses fonctions, une seule fois : les
# perimetres la CONSOMMENT (M-076 -- une copie derive en silence).
ALLOWLIST_RACINE = ("AGENTS.md",)
ALLOWLIST_PREFIXES = ("demarrer-",)


def est_fichier_racine_allowliste(chemin, depart=None):
    """True si le chemin RESOLU est un fichier ALLOWLISTE de la RACINE du workspace.

    On juge le chemin RESOLU, JAMAIS un prefixe ni un nom nu suppose : un
    `demarrer-...` pose ailleurs n est pas allowliste. C est ce qui rend le
    fichier de demarrage ATTESTABLE -- et ce qui laisse un fichier de la racine
    HORS allowlist refuse partout (le cobaye negatif).
    """
    try:
        resolu = Path(chemin).resolve()
    except (OSError, RuntimeError):
        return False
    racine = detecter_racine(depart if depart is not None else chemin)
    if racine is None or resolu.parent != Path(racine).resolve():
        return False
    nom = resolu.name
    return nom in ALLOWLIST_RACINE or any(nom.startswith(p) for p in ALLOWLIST_PREFIXES)


def est_dans_perimetre(chemin, depart=None):
    """DANS la Matrice, OU fichier ALLOWLISTE de la racine du workspace.

    Le fichier de demarrage n est pas DANS la Matrice : il est A COTE, a la racine.
    La decision de l y rattacher est la MEME des deux cotes -- la porte ECRIRE le
    modifie, la BDD l atteste -- donc celui qui juge le perimetre CONSOMME cette
    fonction au lieu de repondre seul (mesure MO-411 : cinq perimetres, un seul
    domicile).
    """
    return est_dans_matrice(chemin, depart) or est_fichier_racine_allowliste(chemin, depart)


def cle_attestable(chemin, depart=None):
    """La CLE sous laquelle un fichier se NOMME et s ATTESTE, ou None (hors perimetre).

    DANS la Matrice : `forme_canonique` (relative a sa racine) -- la cle de la BDD.
    ALLOWLISTE a la racine : son NOM NU (ex. demarrer-optimus-prime.md), qui est
    DEJA la cle sous laquelle bdd-modifications l a note. HORS des deux : None --
    l appelant DIT que rien ne peut etre atteste, il n INVENTE pas une cle.
    """
    if est_dans_matrice(chemin, depart):
        return forme_canonique(chemin, depart)
    if est_fichier_racine_allowliste(chemin, depart):
        return Path(str(chemin)).name
    return None


def chemin_de_cle(cle, depart=None):
    """L INVERSE de `cle_attestable` : une CLE canonique -> le chemin ABSOLU.

    Une cle de la Matrice se RE-ANCRE sur la racine de la Matrice ; une cle
    ALLOWLISTEE (nom NU, sans separateur) sur la RACINE DU WORKSPACE -- sans quoi
    on chercherait le fichier de demarrage DANS la Matrice, ou il n est pas (c est
    exactement ce qui rendait son empreinte ABSENTE). Un nom nu qui n est PAS
    allowliste reste un chemin de la Matrice : la porte ne devine pas.
    """
    brut = str(cle or "").strip()
    nu = Path(brut).name == brut
    if nu and (brut in ALLOWLIST_RACINE
               or any(brut.startswith(p) for p in ALLOWLIST_PREFIXES)):
        return Path(detecter_racine(depart if depart is not None else __file__)) / brut
    return racine_matrice(depart if depart is not None else __file__) / brut


def arbres_matrice(depart=None):
    """Les ARBRES a BALAYER : la Matrice ENTIERE, a UN SEUL domicile (M-076).

    EO-277 : un balayage ecrivait ses dossiers EN DUR dans son propre corps
    (`for dossier in ("matrice", "_operateur")` -- scan-valeurs: cite). La RACINE
    donc HORS du balayage : deux points de restauration y vivaient, jamais vus,
    et le balayage rendait EN ORDRE.

    Le defaut n etait PAS un oubli de liste : la notion `les arbres de la
    Matrice` n avait aucun domicile, donc le premier appelant l a mise dans sa
    poche -- M-076 ne protege qu une valeur qui A une maison (L-100 : une valeur
    recopiee derive en silence).

    Elle vit ICI, et elle est COMPLETE : la racine REELLE, sans repli -- un
    perimetre dont la base serait le workspace accepterait tout le workspace
    (voir racine_matrice_stricte). Un consommateur qui doit EXCLURE une zone l
    exclut EN LE DISANT chez lui ; il ne retrecit pas le domicile.
    """
    racine = racine_matrice_stricte(depart)
    if racine is None:
        return []
    return [racine]


def motif_hors_perimetre(chemin, usage="lecture", depart=None):
    """Le refus NOMME la Matrice reelle et les formes acceptees (friction 77).

    Un refus qui ne dit pas OU il a cherche coute trois essais. Un seul domicile
    pour le MOTIF lui-meme : les cinq perimetres le consomment (M-076) -- le mot
    `usage` dit seulement quel perimetre parle (lecture, ecriture).
    """
    base = racine_matrice_stricte(depart)
    if base is None:
        return ("REFUS : hors perimetre " + usage + " -- AUCUNE Matrice trouvee depuis "
                + str(detecter_racine(depart if depart is not None else __file__))
                + " (ni matrix/, ni cerveau-projet/matrix/) : " + str(chemin))
    return ("REFUS : hors perimetre " + usage + " -- la Matrice vit sous " + str(base)
            + " : formes acceptees = chemin ABSOLU dans la Matrice, chemin relatif a la "
            "racine (cerveau-projet/matrix/...) ; allowlist racine = AGENTS.md, "
            "demarrer-*.md : " + str(chemin))
