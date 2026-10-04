"""Fonctions communes de l'outil rechercher : perimetre, scan BDD, scan fichiers, score.

Chaque fonction fait UNE chose (convention-architecture-outils).
Moteur unifie palier 1 : scan Python + scan JSON, AUCUNE dependance externe.

Lecons de l'audit MO-057 (corrigees en MO-069) :
- un fichier BINAIRE (.db) n'est pas du texte : il n'est plus scanne ;
- une BDD .json se lit par ENTREE, jamais par section entiere (1 hit = 1 entree) ;
- une option de FILTRE filtre (--tag, --mot-cle), elle ne se contente pas de noter ;
- une limite de lecture qui coupe est DITE, jamais muette (lecon MO-055) ;
- un chemin de code jamais couru ne prouve rien : ripgrep (absent du PATH) est retire.
"""
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

from constants import (
    ALLOWLIST_PREFIXES,
    ALLOWLIST_RACINE,
    BDD_SOURCES,
    BDD_SOURCES_PARTAGEES,
    BDD_SOURCES_PRIVEES,
    CARACTERES_MOTIF,
    DOSSIER_SQLITE,
    ENCODAGE,
    EXTENSIONS_BINAIRES,
    EXTENSIONS_IGNOREES,
    EXTENSIONS_SQLITE,
    FICHIER_PAR_SOURCE,
    FICHIERS_SQLITE_EXCLUS,
    FIN_PLURIEL,
    LIMITE_BDD,
    LIMITE_FICHIERS,
    LIMITE_LIGNES_JSONL,
    LIMITE_PAR_FICHIER,
    NOMS_OPTIONS_DRAPEAU,
    RACINE,
    REPERTOIRE_DATA,
    REPERTOIRE_MATRIX,
    SQLITE_PUBLIQUES,
    SUR_CARTE,
    SUR_CONTENU,
    SUR_NOM,
    SUFFIXE_PLURIEL,
)

# Le contrat d invisibilite L-016/CV-006 (plancher + zones DECLAREES V-003 du
# classeur) vit dans SON domicile : cette porte le CONSOMME, elle ne le recopie
# pas (M-076 ; L-100/L-102 : trois copies divergeaient en silence, et la V-003
# n etait lue par AUCUN outil de lecture -- mesure MO-151).
from invisibilite import est_invisible  # noqa: E402
from vocabulaire_invisible import contient_invisible  # noqa: E402

# Le PERIMETRE (est-ce DANS la Matrice ?) vit dans SON domicile (data/commun/
# cible.py) : cette porte le CONSOMME, elle ne le recopie pas (M-076 -- mesure
# MO-184 : cinq perimetres, quatre jugeaient un PREFIXE avant la resolution).
from cible import est_dans_matrice  # noqa: E402

# La GRAMMAIRE de la carte d'identite vit dans SON domicile (data/commun/
# carte_identite.py, M-076) : cette porte la CONSOMME, elle ne la recopie pas.
# C'est le MEME lecteur que celui du garde des cartes -- un document ne peut donc
# pas etre "une carte" pour l'un et "pas une carte" pour l'autre (mesure
# 2026-09-21 : la grammaire n'existait qu'en UNE copie, il en fallait deux).
from carte_identite import (  # noqa: E402
    correspond,
    liens_de_carte,
    lire_carte,
)
from carte_identite import EXTENSION as EXTENSION_CARTE  # noqa: E402
from carte_identite import resume as resume_carte  # noqa: E402

# Le VOCABULAIRE des MOTS VIDES et le DECOUPAGE du francais vivent au MEME domicile
# que la question de recherche injectee (data/commun/recherche_mission.py, M-076) :
# le pilote et le moteur de recherche lisent la MEME liste -- deux copies
# divergeraient (L-029). Le moteur CONSOMME `mots_utiles`, il ne la recopie pas.
from recherche_mission import mots_utiles  # noqa: E402


# --- Perimetre ---


def dans_perimetre(chemin_relatif):
    """True si le chemin RESOLU est dans la Matrice (ou allowlist racine).

    MO-184 (EO-178), meme contrat que la porte ecrire (MO-183) : on RESOUT avant
    de juger. Un prefixe `matrix/...` n est plus un laissez-passer -- il ne vaut
    que si le chemin resolu tombe VRAIMENT dans la Matrice.
    """
    brut = str(chemin_relatif).replace("\\", "/").strip()
    if not brut:
        return False
    while brut.startswith("./"):
        brut = brut[2:]
    while brut.startswith("/"):
        brut = brut[1:]
    nom = brut.split("/")[-1]
    if "/" not in brut and (
        nom in ALLOWLIST_RACINE
        or any(nom.startswith(p) for p in ALLOWLIST_PREFIXES)
    ):
        return True
    return est_dans_matrice(resoudre_chemin(brut))


def est_zone_invisible(path_absolu):
    """True si path contient une zone L-016 invisible (domicile data/commun).

    La liste ne vit plus ici : le plancher et les zones DECLAREES par la
    Matrice (V-003 du classeur) sont dans `data/commun/invisibilite.py`, que les
    quatre outils de lecture consomment (MO-152).
    """
    return est_invisible(path_absolu)


def resoudre_chemin(chemin_relatif):
    """Retourne le Path absolu (depuis RACINE)."""
    brut = str(chemin_relatif).strip()
    return (RACINE / brut).resolve()


def est_fichier_ignore(nom_fichier):
    """True si le fichier n'est ni du texte scannable ni une source de resultat.

    Un binaire lu comme du texte produit des U+FFFD (taux de remplacement) : il
    pourrit les extraits et fait crasher une sortie machine sur console cp1252.
    On l'EXCLUT par extension au lieu de le lire en esperant que ca passe.
    """
    nom = str(nom_fichier).lower()
    return nom.endswith(EXTENSIONS_IGNOREES) or nom.endswith(EXTENSIONS_BINAIRES)


# --- LECTURE D UNE REQUETE : MOTIF OU LANGAGE NATUREL (MO-375) ---------------


def est_motif(requete):
    """Vrai si la requete porte la FORME d un motif (un metacaractere regex).

    Le contrat historique (regex supportee) est CONSERVE : une requete-motif est
    employee TELLE QUELLE. Une requete SANS metacaractere est du TEXTE : elle se
    decoupe en TERMES. Mesure d origine (MO-368) : 5 zeros sur 12 requetes
    reelles, TOUS des phrases a plusieurs mots compilees comme un seul motif.
    """
    return any(caractere in requete for caractere in CARACTERES_MOTIF)


def motif_terme(mot):
    """Le MOTIF d un terme : le mot, son PLURIEL tolere.

    Le s ou le x final est FACULTATIF dans le motif : < outil > trouve < outils >,
    < lecons > trouve < lecon >. La base est le mot prive de ce s ou de ce x.
    """
    base = mot[:-1] if mot.endswith(FIN_PLURIEL) and len(mot) > 2 else mot
    return re.escape(base) + SUFFIXE_PLURIEL


def termes_requete(requete):
    """Les MOTIFS DES TERMES d une requete, ou None (requete LITTERALE).

    Rend None quand la requete est un MOTIF (elle ne se decoupe pas), et None
    aussi quand aucun terme utile ne reste (que des mots vides) : dans les DEUX
    cas l appelant emploie la requete TELLE QUELLE -- une requete ne se vide
    jamais en silence (L-055).

    Le vocabulaire des mots vides n est PAS recopie ici : il vit a son domicile
    (data/commun/recherche_mission.mots_utiles, M-076), que la question de
    recherche injectee par le pilote consomme DEJA.
    """
    if est_motif(requete):
        return None
    motifs = [motif_terme(mot) for mot in mots_utiles(requete)]
    return motifs or None


class Filtre:
    """Le FILTRE d une requete : un motif regex, ou des TERMES lies en ET.

    POURQUOI UNE CLASSE (mesure MO-375) : les avant-regards ( (?=.*terme) )
    disent juste < la ligne porte TOUS les termes >, mais leur cout est
    QUADRATIQUE -- re.search essaie CHAQUE position de depart et chacun relit la
    fin de la ligne, si bien qu une requete en ET sur des lignes longues faisait
    passer une recherche de ~1 s a plus de 3 min (cobaye MO-375). Le filtre tient
    donc la MEME exigence avec un cout LINEAIRE par terme : un search par terme,
    et le premier temoin (celui du premier terme trouve) sert d extrait.

    DEUX MODES, jamais melanges (mesure MO-368) :
      - MOTIF : la requete porte un metacaractere -> un seul motif, tel quel ;
      - LANGAGE NATUREL : un motif par TERME (mots vides retires, pluriel tolere),
        TOUS exiges -- l ordre des mots n importe plus.
    """

    def __init__(self, requete):
        termes = termes_requete(requete)
        if termes is None:
            self.motif = requete
            self._termes = [re.compile(requete, drapeaux_requete())]
        else:
            self.motif = "".join(termes)
            self._termes = [re.compile(terme, drapeaux_requete())
                            for terme in termes]

    def search(self, texte):
        """Le premier TEMOIN si TOUS les termes repondent, sinon None.

        Meme contrat que re.Pattern.search, et de largeur NON nulle : c est le
        match du premier terme trouve, ce qui laisse extraire_autour MONTRER le
        terme (un filtre en ET n a aucune largeur a montrer).
        """
        temoin = None
        for terme in self._termes:
            trouve = terme.search(texte)
            if trouve is None:
                return None
            if temoin is None:
                temoin = trouve
        return temoin


def drapeaux_requete():
    """Les drapeaux de compilation : casse ignoree, et points sur les sauts.

    DOTALL est necessaire aux avant-regards : une entree de BDD est un texte d une
    ligne, mais un fichier lu en bloc ne l est pas -- sans lui, un terme present
    sur une AUTRE ligne ne compterait pas.
    """
    return re.IGNORECASE | re.DOTALL


def valider_requete(requete):
    """Le REFUS NOMME d une requete-motif invalide, sinon "" (mesure MO-424).

    La requete qui porte un METACARACTERE (est_motif) est lue comme un MOTIF et
    compilee TELLE QUELLE : un motif invalide (`[`, `(`, `*`, `?`, `+`) faisait
    remonter un re.PatternError AVEC TRACEBACK, et un crash n enonce aucun remede
    -- la seule forme que la doctrine interdit sans exception. Cette garde compile
    la requete AVANT tout scan et rend le PROBLEME et le REMEDE ; l appelant la
    refuse (code 2). Elle vit au domicile de la LECTURE d une requete (M-076).
    """
    if not requete:
        return ""
    try:
        Filtre(requete)
    except re.error as erreur:
        return ("expression reguliere invalide : " + str(erreur)
                + " ; la requete porte un METACARACTERE ("
                + " ".join(CARACTERES_MOTIF) + ") : elle est lue comme un MOTIF,"
                " jamais comme du texte. Corrigez le motif, ou retirez le"
                " metacaractere (ou echappez-le par un anti-slash) pour une"
                " recherche en LANGAGE NATUREL.")
    return ""


# --- Scan fichiers (Python seul) ---


def scanner_fichiers(requete, dans="fichiers", repertoire=None, inclure_prive=False):
    """Scan fichiers en Python (ripgrep retire : absent du PATH, branche morte).

    Retourne (hits, nb_trouves, nb_limites, msg).
    hit = {"fichier": str, "ligne": int, "sur": str, "texte": str}.

    `inclure_prive` (EO-126) leve le filtre des zones L-016 pour CE scan. Il est
    FAUX par defaut : le moteur reste etanche au cameleon tant que personne ne le
    demande explicitement. Un moteur qui ne peut pas lire la maison de son propre
    operateur n'est pas prudent, il est AVEUGLE -- et un aveugle qui dit "0
    resultat" est indiscernable d'une absence (lecon MO-055).
    """
    if repertoire is None:
        repertoire = REPERTOIRE_MATRIX
    elif not isinstance(repertoire, Path):
        repertoire = Path(repertoire)

    try:
        hits, nb_limites = _scan_python(requete, repertoire)
    except re.error as erreur:
        return [], 0, False, "expression reguliere invalide : " + str(erreur)

    # Filtre perimetre + zones invisibles (le filtre L-016 se leve SEULEMENT sur
    # demande explicite : --prive).
    filtres = []
    for h in hits:
        fp = Path(h["fichier"])
        relatif = fp.relative_to(RACINE) if fp.is_relative_to(RACINE) else fp
        if not dans_perimetre(str(relatif)):
            continue
        if not inclure_prive and est_zone_invisible(fp):
            continue
        filtres.append(h)

    nb_trouves = len(filtres)
    return filtres, nb_trouves, nb_limites, ""


def mesurer_ecartes_invisibles(requete, repertoire=None):
    """Pour DIRE un 0 (MO-448) : rejoue le scan SANS le filtre L-016 et COMPTE.

    Rend (total_visibles, total_en_zones_invisibles). Le premier est ce que le scan
    filtre a deja regarde, le second est ce qu il a ECARTE -- le chiffre qu un 0 muet
    cache. N est appele QUE quand un scan a rendu 0 : le cout est borne au cas rare
    qu il sert a expliquer (un 0 se lit comme une absence s il ne dit pas pourquoi).
    """
    if repertoire is None:
        repertoire = REPERTOIRE_MATRIX
    elif not isinstance(repertoire, Path):
        repertoire = Path(repertoire)
    try:
        hits, _ = _scan_python(requete, repertoire)
    except re.error:
        return 0, 0
    visibles = 0
    invisibles = 0
    for h in hits:
        fp = Path(h["fichier"])
        relatif = fp.relative_to(RACINE) if fp.is_relative_to(RACINE) else fp
        if not dans_perimetre(str(relatif)):
            continue
        if est_zone_invisible(fp):
            invisibles += 1
        else:
            visibles += 1
    return visibles, invisibles


def _scan_python(requete, repertoire):
    """Scan du CONTENU et du NOM, retourne (hits, nb_limites).

    Deux facons de trouver un fichier, donc deux sortes de hits (EO-126) :
    - par son NOM (`sur` = SUR_NOM, `ligne` = 0) : chercher un fichier par son
      nom rendait 0 resultat alors qu'il existait -- mesure du 2026-09-16 :
      "zone_tmp" ne trouvait pas matrice/data/commun/zone_tmp.py ;
    - par son CONTENU (`sur` = SUR_CONTENU).
    Le champ `sur` est ce qui permet au lecteur (humain ou machine) de ne pas
    confondre les deux -- un nom n'est pas une ligne.
    """
    hits = []
    pattern = Filtre(requete)
    try:
        for racine_d, dossiers, fichiers in os.walk(str(repertoire)):
            # Filtre dossiers
            dossiers[:] = [
                d for d in dossiers
                if d not in ("__pycache__", ".git")
            ]
            for nom_f in sorted(fichiers):
                if est_fichier_ignore(nom_f):
                    continue
                fp = Path(racine_d) / nom_f
                if pattern.search(nom_f):
                    hits.append({
                        "fichier": str(fp),
                        "ligne": 0,
                        "sur": SUR_NOM,
                        "texte": nom_f,
                    })
                    if len(hits) >= LIMITE_FICHIERS:
                        return hits, True
                try:
                    with open(fp, "r", encoding=ENCODAGE, errors="replace") as f:
                        for i, ligne in enumerate(f, 1):
                            if pattern.search(ligne):
                                hits.append({
                                    "fichier": str(fp),
                                    "ligne": i,
                                    "sur": SUR_CONTENU,
                                    "texte": ligne.strip(),
                                })
                                if len(hits) >= LIMITE_FICHIERS:
                                    return hits, True
                except (OSError, UnicodeDecodeError):
                    continue
    except OSError:
        pass
    return hits, False


# --- Scan par CARTE D'IDENTITE (combinaison de champs) ---


def lien_vers(carte, demande):
    """Le lien DECLARE qui repond a la demande, ou None (aucun).

    DEUX FORMES admises, et la tolerance est DITE par l appelant :
      - EXACTE : le lien declare EST la demande -- la forme CANONIQUE, celle que
        le garde des cartes exige (chemin depuis la racine des documents) ;
      - SUFFIXE : le lien declare FINIT par la demande -- un appel qui ecrit
        `cible.py` (ou `commun/cible.py`) obtient sa reponse au lieu d un 0
        trompeur (lecon MO-055 : un 0 muet se lit comme une absence).
    La demande est normalisee (antislashs, prefixes `./` et `/`) : une seule forme
    de chemin dans toute la Matrice. Les liens viennent de la GRAMMAIRE
    (liens_de_carte), jamais d un decoupage refait ici (M-076).
    """
    brut = str(demande or "").replace("\\", "/").strip()
    while brut.startswith("./"):
        brut = brut[2:]
    while brut.startswith("/"):
        brut = brut[1:]
    if not brut:
        return None
    declares = liens_de_carte(carte)
    for lien in declares:
        if lien == brut:
            return lien
    for lien in declares:
        if lien.endswith("/" + brut):
            return lien
    return None


def scanner_cartes(couples, inclure_prive=False, repertoire=None, lien=None):
    """Documents dont la CARTE porte TOUS les couples demandes, un hit PAR DOCUMENT.

    Pourquoi ce mode (demande createur, 2026-09-21) : chercher "convention" rend
    les LIGNES qui PARLENT de conventions (106 hits de texte) ; chercher
    `appartient_a=optimus-prime;type=convention` doit rendre les DOCUMENTS qui
    SONT la chose. Un nom de fichier, une ligne de contenu et un document qui
    porte une carte sont trois sortes de resultats : le hit dit laquelle.

    En mode LIEN (`lien` non vide), la carte doit DE PLUS declarer la demande :
    c est le GRAPHE DES LIENS -- retrouver les documents connectes a un fichier
    donne. Les deux modes se cumulent (champs ET lien), et le lien trouve est
    PORTE par le hit : l appelant peut dire quelle forme a repondu.

    Un document SANS carte ne correspond jamais (il ne peut pas repondre a une
    combinaison) : il est COMPTE, jamais tu -- un corpus incomplet qu'on tairait
    se lirait "0 resultat", indiscernable d'une absence (lecon MO-055).

    Rend (hits, rapport). Le rapport porte le PERIMETRE et ses manques :
    documents_lus, avec_carte, sans_carte, exclus_invisibles, hors_perimetre,
    tronque, et les CARTES lues (vocabulaire et valeurs, pour un refus NOMME).
    """
    if repertoire is None:
        repertoire = REPERTOIRE_MATRIX
    elif not isinstance(repertoire, Path):
        repertoire = Path(repertoire)

    rapport = {
        "documents_lus": 0,
        "avec_carte": 0,
        "sans_carte": 0,
        "exclus_invisibles": 0,
        "hors_perimetre": 0,
        "illisibles": 0,
        "tronque": False,
        "cartes": [],
    }
    hits = []
    for chemin in _parcourir_documents(repertoire):
        fp = Path(chemin)
        relatif = fp.relative_to(RACINE) if fp.is_relative_to(RACINE) else fp
        # Le MEME perimetre et le MEME filtre L-016 que le scan de texte : deux
        # portes de lecture ne peuvent pas avoir deux perimetres (MO-184).
        if not dans_perimetre(str(relatif)):
            rapport["hors_perimetre"] += 1
            continue
        if not inclure_prive and est_zone_invisible(fp):
            rapport["exclus_invisibles"] += 1
            continue
        rapport["documents_lus"] += 1
        carte = lire_carte(_lire_texte(fp))
        if carte is None:
            rapport["sans_carte"] += 1
            continue
        rapport["avec_carte"] += 1
        rapport["cartes"].append(carte)
        if correspond(carte, couples) and (not lien or lien_vers(carte, lien) is not None):
            lien_trouve = lien_vers(carte, lien) if lien else None
            hits.append({
                "fichier": str(fp),
                "ligne": 0,
                "sur": SUR_CARTE,
                "texte": resume_carte(carte)
                         + ((" | lien=" + lien_trouve) if lien_trouve else ""),
                "lien": lien_trouve,
                "carte": carte,
            })
            if len(hits) >= LIMITE_FICHIERS:
                rapport["tronque"] = True
                break

    hits.sort(key=lambda h: h["fichier"])
    return hits, rapport


def _parcourir_documents(repertoire):
    """Chemins des fichiers `.md` du repertoire (memes exclusions que le scan)."""
    for racine_d, dossiers, fichiers in os.walk(str(repertoire)):
        dossiers[:] = [d for d in dossiers if d not in ("__pycache__", ".git")]
        for nom_f in sorted(fichiers):
            if not nom_f.endswith(EXTENSION_CARTE):
                continue
            if est_fichier_ignore(nom_f):
                continue
            yield Path(racine_d) / nom_f


def _lire_texte(chemin):
    """Texte d'un fichier (jamais une exception qui remonte au visage de l'agent)."""
    try:
        with open(chemin, "r", encoding=ENCODAGE, errors="replace") as fichier:
            return fichier.read()
    except OSError:
        return ""


# --- Scan BDD (palier 1 : scan JSON par ENTREE) ---


def scanner_bdd(requete, sources=None, tag=None, mot_cle=None, source_nom=None,
                inclure_prive=False):
    """Scan les BDD JSON/JSONL/SQLite, une ENTREE a la fois.

    Retourne (hits, nb_trouves, nb_limites, sources_tronquees).
    hit = {"source": str, "cle": str, "valeur": any, "score": float, "extrait": str}.

    Une option de FILTRE filtre : --tag et --mot-cle RETIRENT les entrees qui ne
    correspondent pas, ils n'ajoutent pas de score (sinon "filtrer" ne filtre rien).

    SOURCES PRIVEES (L-016) : `frictions` est le contenu de l Operateur ; elle ne
    se sert QUE sous `inclure_prive` (--prive, la fenetre privee d Optimus), jamais
    au cameleon. Le filtre `contient_invisible` ne s y applique PAS : il cacherait a
    l Operateur ses propres mots (L-100), ce serait une cecite, pas une protection.
    """
    sqlite_srcs = decouvrir_sqlite()
    if sources is None:
        sources = (tuple(BDD_SOURCES) + tuple(BDD_SOURCES_PARTAGEES)
                   + tuple(BDD_SOURCES_PRIVEES) + tuple(sorted(sqlite_srcs)))

    hits = []
    pattern = Filtre(requete) if requete else None
    prefiltre = pattern if _prefiltre_possible(pattern) else None
    nb_limites = False
    sources_tronquees = []

    for src in sources:
        if source_nom and src != source_nom:
            continue
        base = sqlite_srcs.get(src)
        chemin_prive = BDD_SOURCES_PRIVEES.get(src)
        chemin_partage = BDD_SOURCES_PARTAGEES.get(src)
        if chemin_prive is not None:
            # SOURCE JSON PRIVEE (L-016, MO-482) : declaree dans la ZONE INVISIBLE,
            # servie UNIQUEMENT sous --prive (jamais au cameleon).
            chemin = REPERTOIRE_MATRIX / chemin_prive
            privee = True
        elif chemin_partage is not None:
            # SOURCE JSON PARTAGEE (decision createur 2026-09-27) : declaree HORS
            # data/ mais VISIBLE -- servie SANS --prive (les deux agents la lisent).
            chemin = REPERTOIRE_MATRIX / chemin_partage
            privee = False
        elif base is not None:
            # Une source SQLite DECOUVERTE se lit par un ADAPTATEUR, jamais comme
            # du texte ; sa PRIVACITE est une POLITIQUE, pas une decouverte.
            chemin = base["chemin"]
            privee = src not in SQLITE_PUBLIQUES
        else:
            fichier = FICHIER_PAR_SOURCE.get(src)
            if not fichier:
                continue
            chemin = REPERTOIRE_DATA / fichier
            privee = False
        if privee and not inclure_prive:
            continue
        if not chemin.is_file():
            continue
        # Zone invisible L-016 (domicile) : une BDD declaree exclue ne se sert
        # JAMAIS, meme par le chemin BDD. La garde de chemin ne couvrait que les
        # FICHIERS : mesure MO-153, le moteur servait 101 entrees de suivi-optimus
        # alors que cette zone est declaree exclue depuis M-084.
        # Zone invisible L-016 : une BDD declaree exclue ne se sert JAMAIS par
        # defaut -- mais `--prive` (la fenetre privee d'Optimus) l'OUVRE, comme il
        # ouvre les zones invisibles dans les FICHIERS (EO-126). Sans cela, des
        # sources JSON declarees (lecons, sessions) rendaient un 0 MUET par ici :
        # la promesse de `--source lecons` n'etait vraie que sur le papier.
        if est_invisible(chemin) and not inclure_prive:
            continue

        try:
            if base is not None:
                entrees, tronque = _lire_source_sqlite(chemin, base["tables"])
            else:
                entrees, tronque = _lire_source(chemin, prefiltre)
        except (OSError, json.JSONDecodeError):
            continue
        if tronque:
            sources_tronquees.append(src)

        for cle, valeur in entrees:
            texte_recherche = texte_de(valeur)

            # L-016 a la LIVRAISON (domicile data/commun/vocabulaire_invisible.py) :
            # une entree qui nomme l invisible ne se livre jamais -- MEME regle que
            # l injection, qui la tenait deja (MO-153 : le moteur servait la BDD brute).
            if not privee and contient_invisible(texte_recherche):
                continue

            # 1) La RECHERCHE : la requete doit correspondre
            if pattern and not pattern.search(texte_recherche):
                continue
            # 2) Les FILTRES : ils retirent ce qui ne correspond pas
            if tag and tag.lower() not in [t.lower() for t in tags_de(valeur)]:
                continue
            if mot_cle and mot_cle.lower() not in texte_recherche.lower():
                continue

            hits.append({
                "source": src,
                "cle": str(cle),
                "valeur": valeur,
                "score": calculer_score_requete(requete, texte_recherche),
                "extrait": extraire_autour(pattern, texte_recherche),
            })
            if len(hits) >= LIMITE_BDD:
                nb_limites = True
                break

    # Tri par score descendant (tri stable : a score egal, l'ordre d'insertion reste)
    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits, len(hits), nb_limites, sources_tronquees


def _prefiltre_possible(pattern):
    """Vrai si la ligne BRUTE et la valeur re-encodee portent le meme texte.

    Optimisation : sur un JSONL de 67521 lignes, seules les lignes qui peuvent
    correspondre sont analysees par json.loads (la lecture n'est plus tronquee en
    silence pour rester rapide). Le raccourci n'est honnete que pour un motif
    ASCII SANS anti-slash : un caractere echappe (\u00e9, \n) n'apparait pas tel
    quel dans le texte brut.
    """
    if pattern is None:
        return False
    motif = pattern.motif
    return motif.isascii() and "\\" not in motif


def texte_de(valeur):
    """Texte interrogeable d'une entree (dict, liste, scalaire)."""
    if isinstance(valeur, dict):
        return json.dumps(valeur, ensure_ascii=False)
    if isinstance(valeur, (list, tuple)):
        return " ".join(str(v) for v in valeur)
    return str(valeur)


def tags_de(valeur):
    """Liste des tags d'une entree (dict seulement, jamais devine)."""
    if not isinstance(valeur, dict):
        return []
    tags = valeur.get("tags", [])
    if isinstance(tags, str):
        return [tags]
    if isinstance(tags, (list, tuple)):
        return [str(t) for t in tags]
    return []


def extraire_autour(pattern, texte, marge=40):
    """Extrait la premiere occurrence (marge de chaque cote), ou vide."""
    if not pattern or not texte:
        return ""
    m = pattern.search(texte)
    if not m:
        return ""
    debut = max(0, m.start() - marge)
    fin = min(len(texte), m.end() + marge)
    return texte[debut:fin]


def _est_conteneur(donnees):
    """Vrai si ce dict est une SECTION a descendre, faux si c'est UNE entree.

    Signal d'une section : au moins une valeur est un dict, ou une LISTE DE
    DICTS (une liste d'entrees). Les scalaires et les listes de scalaires sont
    des CHAMPS d'entree : le compteur scalaire d'une BDD ne doit pas faire
    retomber tout le fichier en un seul bloc (bug attrape par le cobaye MO-069 :
    `compteur` entier rendait lecons.json entier "racine").
    """
    if not isinstance(donnees, dict) or not donnees:
        return False
    for valeur in donnees.values():
        if isinstance(valeur, dict):
            return True
        if isinstance(valeur, list) and any(isinstance(v, dict) for v in valeur):
            return True
    return False


def _cle_entree(prefixe, index, item):
    """Cle lisible d'une entree : <section>/<id> quand l'entree porte un id."""
    if isinstance(item, dict) and item.get("id"):
        base = prefixe + "/" if prefixe else ""
        return base + str(item["id"])
    return prefixe + "[" + str(index) + "]"


def _entrees_json(donnees, prefixe=""):
    """Aplatit un JSON en ENTREES : 1 entree = 1 hit, jamais une section entiere."""
    if isinstance(donnees, list):
        return [
            (_cle_entree(prefixe, index, item), item)
            for index, item in enumerate(donnees)
        ]
    if _est_conteneur(donnees):
        entrees = []
        for cle, valeur in donnees.items():
            chemin = (prefixe + "/" + str(cle)) if prefixe else str(cle)
            entrees.extend(_entrees_json(valeur, chemin))
        return entrees
    return [(prefixe or "racine", donnees)]


def _tables_sqlite(chemin):
    """Les tables d ENTREE d une base (sqlite_master), triees ; [] si illisible."""
    import sqlite3
    try:
        with sqlite3.connect(str(chemin)) as conn:
            return [ligne[0] for ligne in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
                " AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    except (sqlite3.Error, OSError):
        return []


def decouvrir_sqlite():
    """Les BDD SQLite de DOSSIER_SQLITE, DECOUVERTES (jamais declarees une a une).

    Retourne {stem: {"chemin": Path, "tables": [noms...]}}, trie par stem. Sont
    ECARTES : les fichiers hors extensions SQLite, les fichiers EXCLUS (un INDEX
    n est pas une BDD), et une base SANS table d entree. Decouvrir ne PUBLIE rien :
    la publication est une politique (SQLITE_PUBLIQUES), appliquee par scanner_bdd.
    """
    trouvees = {}
    if not DOSSIER_SQLITE.is_dir():
        return trouvees
    for chemin in sorted(DOSSIER_SQLITE.iterdir()):
        if not chemin.is_file():
            continue
        if chemin.suffix.lower() not in EXTENSIONS_SQLITE:
            continue
        if chemin.name in FICHIERS_SQLITE_EXCLUS:
            continue
        tables = _tables_sqlite(chemin)
        if not tables:
            continue
        trouvees[chemin.stem] = {"chemin": chemin, "tables": tables}
    return trouvees


def sources_bdd():
    """Les sources BDD DISPONIBLES : les JSON (publiques + PARTAGEES + PRIVEES) + les SQLite DECOUVERTES."""
    return tuple(list(BDD_SOURCES) + list(BDD_SOURCES_PARTAGEES)
                 + list(BDD_SOURCES_PRIVEES) + sorted(decouvrir_sqlite()))


def sources_bdd_privees():
    """Les sources BDD PRIVEES (L-016) : les JSON privees DECLAREES + les SQLite
    decouvertes non PUBLIQUES. Servies seulement sous --prive."""
    privees = list(BDD_SOURCES_PRIVEES)
    privees += [stem for stem in sorted(decouvrir_sqlite())
                if stem not in SQLITE_PUBLIQUES]
    return tuple(privees)


def _lire_source_sqlite(chemin, tables):
    """Lit une BDD SQLite par un ADAPTATEUR, retourne (entrees, tronque).

    AUCUN fichier n est MIGRE : les TABLES sont LUES telles quelles (exception
    assumee, data-readme.md 2026-09-26). Une entree par LIGNE, cle = <table>/<id>
    (l id quand la table en porte un, son RANG sinon -- une table sans id reste
    servie, elle n est pas rendue muette). Les noms de tables viennent de la
    DECOUVERTE (sqlite_master), jamais du code de lecture.
    """
    import sqlite3
    entrees = []
    try:
        with sqlite3.connect(str(chemin)) as conn:
            conn.row_factory = sqlite3.Row
            for table in tables:
                nom = "\"" + str(table).replace("\"", "\"\"") + "\""
                for rang, ligne in enumerate(conn.execute("SELECT * FROM " + nom)):
                    donnees = dict(ligne)
                    cle = donnees.get("id", rang)
                    entrees.append((str(table) + "/" + str(cle), donnees))
    except (sqlite3.Error, OSError):
        return [], False
    return entrees, False


def _lire_source(chemin, prefiltre=None):
    """Lit une source BDD, retourne (entrees, tronque).

    `tronque` dit qu'une coupe a eu lieu : une limite muette est une cecite
    (lecon MO-055) -- l'appelant DOIT la rendre visible.
    """
    if chemin.suffix == ".jsonl":
        entrees = []
        tronque = False
        with open(chemin, "r", encoding=ENCODAGE, errors="replace") as f:
            for i, ligne in enumerate(f):
                if i >= LIMITE_LIGNES_JSONL:
                    tronque = True
                    break
                ligne = ligne.strip()
                if not ligne:
                    continue
                if prefiltre and not prefiltre.search(ligne):
                    continue
                try:
                    entrees.append((str(i), json.loads(ligne)))
                except json.JSONDecodeError:
                    continue
        return entrees, tronque
    with open(chemin, "r", encoding=ENCODAGE, errors="replace") as f:
        donnees = json.load(f)
    return _entrees_json(donnees), False


# --- Score & tri ---


def calculer_score_requete(requete, texte):
    """Score de pertinence : occurrences des TERMES (au moins 1 pour un hit).

    Un motif en ET est de largeur NULLE : findall y rendrait un vide a chaque
    position et le score ne mesurerait plus rien (defaut attrape par le cobaye
    MO-375). Le score se compte donc PAR TERME ; une requete-motif garde son
    unique terme, la requete elle-meme (comportement historique conserve).
    """
    if not requete or not texte:
        return 0.0
    motifs = termes_requete(requete) or [requete]
    total = 0
    for motif in motifs:
        total += len(re.findall(motif, texte, drapeaux_requete()))
    return float(max(1, total))


def formatter_hit(hit, index):
    """Formate un hit pour sortie human.

    Un hit de NOM n'a pas de ligne : l'afficher comme `<fichier>:0` ferait croire
    a une ligne zero qui n'existe pas (EO-126).
    """
    src = hit.get("source", "fichier")
    if src == "fichier":
        if hit.get("sur") == SUR_CARTE:
            # Le DOCUMENT repond : pas de numero de ligne a afficher (l'afficher
            # comme `<fichier>:0` ferait croire a une ligne zero qui n'existe pas).
            return (
                f"  {index + 1}. {hit['fichier']}\n"
                f"     (carte) {hit['texte'][:160]}"
            )
        if hit.get("sur") == SUR_NOM:
            return (
                f"  {index + 1}. {hit['fichier']}\n"
                f"     (nom de fichier)"
            )
        return (
            f"  {index + 1}. {hit['fichier']}:{hit['ligne']}\n"
            f"     {hit['texte'][:120]}"
        )
    extrait = hit.get("extrait", "")[:120]
    return (
        f"  {index + 1}. [{src}] cle={hit['cle']} score={hit['score']:g}\n"
        f"     {extrait}"
    )


# --- Periode ---


def periode_valide(periode_str):
    """Vrai si la periode est <nombre><j|m|a> (7j, 30j, 3m, 1a).

    Une periode illisible est REFUSEE : un filtre qui ne filtre pas est un
    affichage (lecon EO-110).
    """
    return bool(re.fullmatch(r"\d+[jma]", str(periode_str or "").strip().lower()))


def _date_limite(periode_str):
    """Date plancher pour la periode (None si illisible)."""
    if not periode_valide(periode_str):
        return None
    nombre = int("".join(c for c in periode_str if c.isdigit()))
    unite = periode_str[-1].lower()
    jours = {"j": nombre, "m": nombre * 30, "a": nombre * 365}[unite]
    return datetime.now() - timedelta(days=jours)


def _date_entree(valeur):
    """Date d'une entree BDD, ou None (jamais devinee)."""
    if not isinstance(valeur, dict):
        return None
    for champ in ("date", "date_creation", "cree", "deposee_le", "terminee_le"):
        brut = valeur.get(champ)
        if not brut or not isinstance(brut, str):
            continue
        try:
            return datetime.fromisoformat(brut.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            continue
    return None


def filtrer_par_periode(hits, periode_str):
    """Filtre les hits par periode. Retourne (filtres, nb_ecartes_sans_date).

    Une entree SANS date n'est pas "gardee par defaut" : elle est ECARTEE et
    COMPTEE -- sans quoi la periode ne retire rien et l'agent croit interroger
    une fenetre (EO-110).
    """
    limite = _date_limite(periode_str)
    if limite is None:
        return hits, 0

    filtres = []
    ecartes = 0
    for h in hits:
        if h.get("source", "fichier") == "fichier":
            fp = Path(h["fichier"])
            try:
                mtime = datetime.fromtimestamp(fp.stat().st_mtime)
            except (OSError, ValueError):
                ecartes += 1
                continue
            if mtime >= limite:
                filtres.append(h)
            continue
        date_entree = _date_entree(h.get("valeur"))
        if date_entree is None:
            ecartes += 1
            continue
        if date_entree >= limite:
            filtres.append(h)
    return filtres, ecartes


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus, drapeaux=NOMS_OPTIONS_DRAPEAU)


def signaler_inconnues(options, outil, noms_connus, usage=""):
    """Voir le CONTRAT du domicile partage (EO-179) : refus NOMME d une inconnue."""
    from options import signaler_inconnues as repartir  # domicile partage (EO-179)
    return repartir(options, outil, noms_connus, usage=usage)
