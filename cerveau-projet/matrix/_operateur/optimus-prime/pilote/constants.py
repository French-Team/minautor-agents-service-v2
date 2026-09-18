"""Constantes du pilote OPTIMUS (Flux 2) : chemins et valeurs.

Pilote dedie _operateur/optimus-prime/pilote/ (Flux 2, invisible cameleon).
Miroir du pilote cameleon (matrice/pilote/) mais isole : meme interface,
file/historique/entonnoir/intercom dedies, prefix MO-001, vivier partage+prive.
Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
from pathlib import Path

REPERTOIRE_PILOTE = Path(__file__).resolve().parent
# Racine matrix/ DETECTEE par le MARQUEUR PARTAGE (M-076 : matrice/data/commun/racine.py),
# jamais comptee a la main (L-013) -- c'est le motif de verifier-contrat-fondamental.
BORNES_REMONTEE = 30
_courant = REPERTOIRE_PILOTE
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant depuis " + str(REPERTOIRE_PILOTE))
REPERTOIRE_MATRIX = _courant
if REPERTOIRE_MATRIX.name != "matrix":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_MATRIX) + " n'est pas le dossier matrix/"
    )
REPERTOIRE_MATRICE = REPERTOIRE_MATRIX / "matrice"
REPERTOIRE_OPERATEUR = REPERTOIRE_MATRIX / "_operateur" / "optimus-prime"
REPERTOIRE_DATA = REPERTOIRE_MATRICE / "data"

# data/commun (motif unique M-076) : le dossier PARTAGE est installe dans
# sys.path. tokens.py y vit : l'espion de POIDS des injections (E-097,
# imperatif 56) et le sac-a-dos. Garde-fou L-006 : le dossier cible est
# verifie avant d'etre installe (jamais un chemin devine).
import sys as _sys

REPERTOIRE_COMMUN = REPERTOIRE_DATA / "commun"
if REPERTOIRE_COMMUN.name == "commun" and (REPERTOIRE_COMMUN / "tokens.py").is_file():
    _sys.path.insert(0, str(REPERTOIRE_COMMUN))

# Intercom prive Flux 2 : _operateur/maintenance (zone invisible cameleon, L-016)
REPERTOIRE_INTERCOM_OPTIMUS = REPERTOIRE_MATRIX / "_operateur" / "maintenance"
# Compat : ancien REPERTOIRE_INTERCOM pointe vers intercom Optimus prive
REPERTOIRE_INTERCOM = REPERTOIRE_INTERCOM_OPTIMUS

# File dediee Optimus : file-missions-optimus.json (jamais matrice/pilote/file-missions.json)
NOM_FILE = "file-missions-optimus.json"
CHEMIN_FILE = REPERTOIRE_PILOTE / NOM_FILE
# LEGACY ARCHIVE (2026-09-13) : une copie AU BIT PRES de la file du CAMELEON
# (`matrice/pilote/file-missions.json`, 89 missions M-001..M-089) trainait ici
# sous le nom `file-missions.json`. Aucun code ne la lisait, mais son NOM la
# faisait passer pour la file d'Optimus : on y lisait des missions `M-0xx` comme
# si elles etaient a lui. Renommee `file-missions-legacy-archive.json` --
# RENOMMEE, jamais supprimee (le fichier n'est pas suivi par git, une
# suppression serait irreversible et sans copie de secours).
# Les anciennes constantes `CHEMIN_FILE_LEGACY` et `CHEMIN_ENTONNOIR_LEGACY`
# sont RETIREES : aucune ligne de code ne les utilisait, et la migration
# qu'elles annoncaient n'a jamais ete ecrite. Une constante morte fait croire a
# un mecanisme qui n'existe pas.
# Meme regle que l'entonnoir, deja archive de la sorte
# (`entonnoir-files-legacy-archive.json`) : UNE seule file par flux.

# Entonnoir dedie Optimus (echelon 4) : meme logique, fichier separe
NOM_ENTONNOIR = "entonnoir-files-optimus.json"
CHEMIN_ENTONNOIR = REPERTOIRE_PILOTE / NOM_ENTONNOIR
# Historique dedie Optimus (jamais historiques-missions.jsonl du cameleon)
NOM_HISTORIQUE = "historiques-missions-optimus.jsonl"
CHEMIN_HISTORIQUE = REPERTOIRE_DATA / NOM_HISTORIQUE

# MARBRE (journal suivi-optimus) : la MEMOIRE des identifiants deja utilises.
# Le fichier appartient a l'outil data/outils/suivi-optimus (son NOM_BDD) ; le
# pilote ne fait que le LIRE. Sans lui, `prochain_id` ne regardait QUE la file
# et redistribuait un numero deja pris par une mission menee HORS file :
# collision mesuree le 2026-09-15 (MO-108 attribue deux fois) -- EO-121.
NOM_MARBRE = "suivi-optimus.jsonl"
CHEMIN_MARBRE = REPERTOIRE_DATA / NOM_MARBRE
NOM_HISTORIQUE_PRIVE = "historiques-missions-optimus.jsonl"
CHEMIN_HISTORIQUE_PRIVE = REPERTOIRE_OPERATEUR / NOM_HISTORIQUE_PRIVE

# Registre des THEMES : partage (vivier cameleon) + prive Optimus (_operateur/parcours/themes)
NOM_THEMES = "vivier-themes.json"
CHEMIN_THEMES = REPERTOIRE_DATA / NOM_THEMES
# Dossier prive des themes Optimus (PREPARATION, REPRISE-MISSION, AUTO-EVOLUTION, CREER-OUTIL, CONTRE-ANALYSE)
REPERTOIRE_THEMES_PRIVES = REPERTOIRE_OPERATEUR / "parcours" / "themes"

# Parcours utilisateur : theme dedie (guidage du remplissage de la fiche).
THEME_PROFIL = "USER-PROFIL"
CHEMIN_THEME_PROFIL = REPERTOIRE_THEMES_PRIVES / "theme-user-profil.json"
# Prefixe d'identifiant dedie Optimus : MO-001 (MissionOptimus), jamais M- du cameleon
PREFIXE_ID = "MO-"

# Mise en securite defcon (variable tenue par l'outil machine-defcon).
CLE_DEFCON = "defcon"
NIVEAU_DEFCON_MAX = 5
THEME_DEFCON = "DEFCON"
CHEMIN_CLASSEUR_VARIABLES = REPERTOIRE_DATA / "classeur-variables.json"

# BDD des MODIFICATIONS : le domicile de "quel fichier a ete touche par quoi"
# (indexee par FICHIER, chaque modification portant son detail et ses tags). Le
# pilote la LIT pour remplir les FICHIERS de la trace de mission (MO-139) : les
# colonnes vides de suivi-optimus.md ne venaient pas de la vue, elles venaient du
# fait que le pilote ne transmettait JAMAIS la liste des fichiers a la porte
# `noter` -- qui l'accepte pourtant depuis sa naissance. Zero-valeur-en-dur : la
# logique consomme CE chemin, elle ne le reconstruit pas.
NOM_MODIFICATIONS = "modifications-par-fichier.json"
CHEMIN_MODIFICATIONS = REPERTOIRE_DATA / NOM_MODIFICATIONS
# Fenetre de lecture du DETAIL pour attribuer une modification a une mission
# (MO-139). Convention MESUREE le 2026-09-16 : le detail d'une modification OUVRE
# sur la mission qui agit ("MO-136 (tracage de rattrapage...) : ..."), alors qu'une
# mention d'EXEMPLE arrive loin dans le texte (mesure : "MO-999", id de cobaye
# cite dans un detail qui recopie une commande, se trouvait a la position 319).
# Au-dela de la fenetre, la mention n'attribue rien : la derivation ne fabrique
# pas de faux fichier dans la trace.
FENETRE_MENTION_DETAIL = 60

# SUPER-COMBO D'ENTRETIEN DE LA TRACE (sc-003-auto-suivi) : le PILOTE le lance a
# chaque cloture de mission (demande createur, 2026-09-16). Il chaine la
# coherence file<->journal PUIS la regeneration de la vue. Avant, le pilote
# appelait la SEULE porte `vue` : l'ecart entre la file et le journal n'etait
# regarde que si quelqu'un y pensait -- une discipline d'agent, donc une affaire
# de memoire. Chemin ET verbe declares UNE fois (zero-valeur-en-dur).
CHEMIN_SUPER_COMBO_SUIVI = (
    REPERTOIRE_OPERATEUR / "super-combos" / "sc-003-auto-suivi" / "main.py"
)
VERBE_ENTRETIEN_SUIVI = "rapide"
# Le super-combo lance deux portes en sous-processus : la borne est large, mais
# elle EXISTE -- une porte morte ne doit jamais figer une cloture.
DELAI_ENTRETIEN_SUIVI = 120

# Protocole de pause session-matrix (M-080) : l'etat serialise pose par
# l'outil pause-session au niveau data/. S'il existe, la session est EN PAUSE.
NOM_ETAT_PAUSE = "session-matrix-etat.json"
CHEMIN_ETAT_PAUSE = REPERTOIRE_DATA / NOM_ETAT_PAUSE

# Porte de la trace de session (MO-121) : le chemin de l'outil bdd-sessions,
# declare UNE fois. Il etait recopie a DEUX endroits de commun.py (deux
# copies, deux comportements possibles -- L-029) ; le code le CONSOMME
# desormais, il ne le contient plus (zero-valeur-en-dur).
CHEMIN_PORTE_SESSIONS = REPERTOIRE_DATA / "outils" / "bdd-sessions" / "main.py"

# Porte de CONSERVATION (EO-147, MO-163) : le BALAYAGE de la famille des points
# de restauration. La porte `ecrire` cree un point a CHAQUE passage, donc chaque
# ecriture ajoute un element a classer -- et une classification faite a la main
# ne se termine jamais (mesure MO-162 : 29 points sans decision en une journee,
# dont 2 nes de la reparation de la verification elle-meme). Le pilote balaie
# donc a CHAQUE cloture, comme il purge sa zone jetable : une discipline
# qu'aucun instrument ne mesure depend de la memoire (lecon MO-136). Chemin,
# verbe et borne declares UNE fois (zero-valeur-en-dur).
CHEMIN_PORTE_CONSERVATION = REPERTOIRE_DATA / "outils" / "bdd-conservation" / "main.py"
VERBE_BALAYAGE_CONSERVATION = "balayer"
DELAI_BALAYAGE_CONSERVATION = 120
# L'ACTE de la MEME famille (EO-147) : le balayage n'ecrit que des DECISIONS, et
# une famille classee mais jamais archivee reste un travail EN ATTENTE -- donc une
# discipline d'agent, donc oubliee. Mesure de la fermeture d'EO-147 : 88 elements
# decidas `archiver` attendaient un geste manuel. Le pilote draine donc la famille
# a CHAQUE cloture, comme il vide sa zone jetable (MO-136). L'option `--lot oui`
# ne traite que les elements dont le verdict est DEJA trace : la decision vient
# toujours AVANT le geste (plan-conservation, section 5 : aucun element sans
# verdict ne bouge).
VERBE_ARCHIVAGE_CONSERVATION = "archiver"
OPTION_LOT_ARCHIVAGE_CONSERVATION = "--lot"
DELAI_ARCHIVAGE_CONSERVATION = 180
# Le CONTROLE de la MEME famille (EO-152, MO-165) : les deux gestes ci-dessus
# MAINTIENNENT la borne N=1 (une famille ne garde EN PLACE que son plus recent) ;
# ce verbe la MESURE. Mesure MO-164 : la case 8 (`controler-archives`) reste verte
# TOUT LE TEMPS -- elle mesure la PERTE, jamais la BORNE -- et 16 points STRUCTUREL
# en trop dans 10 familles sur 88 n'etaient vus par AUCUN instrument. Un controle
# que personne ne lance ne protege rien : le pilote le lance donc a CHAQUE cloture,
# APRES l'acte qui doit l'etablir.
VERBE_CONTROLE_BORNE_CONSERVATION = "controler-borne"
DELAI_CONTROLE_BORNE_CONSERVATION = 60
# L'ECHEC de ce controle part AU MARBRE (le pilote l'y note) : la vue la relira
# bien apres que la console s'est refermee, donc la MESURE de la porte -- les
# familles en exces et leurs identifiants -- doit voyager AVEC l'alerte. Sans
# borne, un incident qui toucherait toutes les familles transformerait la trace
# en mur de texte ; le plafond vit donc ici, une seule fois.
LONGUEUR_MESURE_ALERTE_CONSERVATION = 1200

# ZONE DES FICHIERS JETABLES d'Optimus (regle immuable perimetre-tmp) : c'est le
# PILOTE qui la VIDE a la cloture (MO-136), sur les DEUX chemins de fin (`fin` et
# `enregistrer`). Le point 4 de la regle etait une DISCIPLINE D'AGENT -- et le
# garde tmp dit lui-meme qu'il ne peut pas la verifier : une discipline non
# verifiee depend de la memoire, donc elle est oubliee. Un domicile, une
# constante (zero-valeur-en-dur).
NOM_ZONE_TMP = "tmp-optimus"
REPERTOIRE_ZONE_TMP = REPERTOIRE_MATRIX / NOM_ZONE_TMP
NOM_README_ZONE_TMP = "README.md"

# MOTEUR DE RECHERCHE (EO-131) : le projet se souvient mieux que l'agent, mais
# encore faut-il le lui DEMANDER au bon moment -- le sujet de la mission. Le
# pilote fournit donc la QUESTION dans l'injection (comme la posture), au lieu de
# laisser l'agent y penser. Chemin ET options sont declares UNE fois ici : la
# logique les consomme, elle ne les contient pas (zero-valeur-en-dur).
# L'option `--prive` ouvre la zone de l'operateur a la recherche : c'est le FLUX 2
# qui la porte. Le cameleon ne la recoit JAMAIS (L-016, coherence d'invisibilite).
CHEMIN_MOTEUR_RECHERCHE = REPERTOIRE_DATA / "outils" / "rechercher" / "main.py"
OPTIONS_MOTEUR_RECHERCHE = "--dans tous --prive"
GABARIT_COMMANDE_RECHERCHE = (
    "python3 " + str(CHEMIN_MOTEUR_RECHERCHE)
    + " rechercher --requete \"{question}\" " + OPTIONS_MOTEUR_RECHERCHE
)


BOITE_PILOTE_OUT = REPERTOIRE_INTERCOM / "pilote" / "outbox.jsonl"
BOITE_MATRICE_IN = REPERTOIRE_INTERCOM / "matrice" / "inbox.jsonl"

STATUT_EN_ATTENTE = "en-attente"
STATUT_EN_COURS = "en-cours"
STATUT_TERMINEE = "terminee"

# IDENTITE D'UNE MISSION : DEUX champs distincts (L-061 / MO-076).
# Un item d'entonnoir porte son TITRE en texte libre (`theme`, nom historique)
# ET son ROLE, choisi dans le vivier (`role`) : c'est le ROLE qui devient le
# champ `theme` (FERME) de la mission, le titre etant conserve en `titre` pour
# la lecture. Transporter le titre comme role bloquait l'injection (4 fois
# mesure : MO-070, MO-071, MO-072, MO-075).
CHAMP_ROLE_ITEM = "role"
CHAMP_TITRE_MISSION = "titre"

# POSTURE D'UNE MISSION (revision du 2026-09-14, MAILLON 2/5) : le ROLE de la
# mission porte DEUX choses distinctes -- la POSTURE (qui conduit : une
# PERSONNALITE du vivier, deduite du TYPE par la table fermee du pilote,
# `personnalites.py`) et le CHANTIER (le champ `theme`, deja ferme). Le cameleon
# avait une personnalite par mission ; Optimus n'en avait aucune. Le champ est
# declare ICI (proprietaire du contrat), jamais recopie dans la logique (L-035).
CHAMP_POSTURE_MISSION = "posture"
CATEGORIE_POSTURE = "PERSONNALITE"

# AUTO-VALIDATION D'UNE MISSION (EO-143 / MO-167, GO createur du 2026-09-18) :
# la garantie "une mission deja vue avec le createur s enchaine sans redemander"
# ne reposait que sur une ABSENCE (aucune porte d approbation dans la chaine :
# injection / fin / file / checklist verifies) et une LECON (L-019). Une garantie
# qui ne vit que dans une absence se re-cree au premier garde qui l ignore : le
# CHAMP la rend LISIBLE. Nom du champ et valeur declares ICI (proprietaire du
# contrat, L-035) ; la doctrine est portee par la regle immuable
# regles-immuables/auto-validation-missions.md.
CHAMP_AUTO_VALIDATION = "auto_validation"
VALEUR_AUTO_VALIDATION = "auto"

# INDEX DES MISSIONS AUTO-VALIDEES (3e jambe MO-175) : une LISTE D IDS vivant
# dans l ETAT DE L ENTONNOIR -- jamais une copie (une seule verite, lecon
# d EO-154 : c est la copie qui bloquait `retirer`). Le pilote LIT cet index
# pour decider de l ENCHAINEMENT ; il ne l ecrit JAMAIS (la queue appartient a
# l entonnoir). Meme litteral que entonnoir/listes.py -- les deux doivent
# rester EGAUX (une divergence rendrait l auto-validee invisible au pilote).
CLE_AUTO_VALIDEES = "auto_validees"

# DEFAUTS STRUCTURES D'UNE MISSION (R5, audit MO-174) : un OUTIL fautif rencontre
# EN TRAVAILLANT se declare a la cloture, et sa declaration VOYAGE avec la mission
# (fichier + journal + retour Matrice). Avant, le defaut n'existait que dans le
# RECIT du bilan : illisible pour tout instrument, et perdu au premier changement
# de session. Le format est JSONL -- un OBJET par defaut, champs FERMES : un champ
# inconnu, un champ requis vide ou un statut hors liste sont des REFUS, jamais des
# silences (un format qui accepte n'importe quoi ne structure rien : il donne
# l'illusion d'une trace).
OPTION_DEFAUTS = "defauts-fichier"
CHAMP_DEFAUTS_MISSION = "defauts"
CHAMPS_DEFAUTS = ("outil", "defaut", "reproduit", "reparation", "preuve", "statut")
CHAMPS_DEFAUTS_REQUIS = ("outil", "defaut")
# Le statut REPARE est declare ICI et consomme PAR le tuple : un second litteral
# ecrit ailleurs serait un jumeau muet (lecon de MO-175).
STATUT_DEFAUT_REPARE = "repare"
STATUTS_DEFAUT = (STATUT_DEFAUT_REPARE, "signale", "hors-perimetre", "bloque")

# RAPPEL DE ROUTE (R5, audit MO-174) : la route de l'outil fautif VOYAGE avec la
# mission. L'agent qui repare n'a pas a se souvenir de la doctrine -- elle est
# dans son sac-a-dos, comme la checklist et les lecons. Le DECLENCHEUR est le
# TYPE de la mission : `reparation` est le type DECLARE par le crochet `[outil]`
# (pilote/filtrer/entry.py) et il appartient a la liste FERMEE TYPES
# (checklist/listes.py). Ecrit ICI et lu d'ici (proprietaire du contrat, L-035) ;
# le garde CV-007 (verbe `crochets`) verifie qu'il appartient bien a TYPES -- une
# liste ou ce type serait renomme rendrait le rappel MUET sans rien dire.
TYPE_ROUTE_OUTIL = "reparation"
CHAMP_RAPPEL = "rappel"
RAPPEL_ROUTE_OUTIL = (
    "ROUTE OUTIL (protocole 10, regle immuable defaut-outil-repare-sur-place) : "
    "un defaut d'OUTIL se REPRODUIT, se REPARE DANS L'OUTIL (jamais a la main), "
    "se PROUVE, se TRACE, puis le travail REPREND. Un contournement manuel est "
    "une FAUTE de process, jamais une astuce -- et un outil CRITIQUE reste au "
    "CREATEUR. La route complete : protocoles/proto-10-route-outil-defaillant.md."
)

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
