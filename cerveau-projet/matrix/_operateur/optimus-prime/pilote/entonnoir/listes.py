"""Listes FERMEES de l'entonnoir : types, categories, urgences, regles de classement.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
Une valeur hors liste est REFUSEE : la structure ne derive jamais (decision createur).

NOMMAGE : ce module s'appelle listes.py (PAS constants.py) pour ne pas entrer en
collision avec les modules du pilote (le script importe depuis son propre dossier).
"""
# Echelon 1 : les types de missions (file d'arrivee de l'echelon 0).
# revision : nouveau type (decision createur 2026-09-07, mot-crochet [revision]).
# `investigation` : nouveau type (demande createur 2026-10-02, MO-525) --
# controler qu une ANCIENNE demande a ete menee a son terme, qu elle est
# fonctionnelle, puis la valider et la certifier. Voisin de `cablage`, qui
# controle le BRANCHEMENT ; l un regarde l effet, l autre le fil.
# `tache` : nouveau type (demande createur 2026-10-02, mot-crochet [tache]) --
# une commande d EXECUTION. La nature est celle de la COMMANDE, pas de son
# effet : une tache peut corriger, mesurer ou construire. Ce qui la distingue de
# `dev`, c est que le createur a deja tranche en l ecrivant : elle ne laisse rien
# au classement.
TYPES = ("dev", "reparation", "doc", "audit", "revision", "question", "cadrage", "cablage",
         "preparer", "investigation", "tache")

# Echelon 2 : les categories DANS chaque type (la file-type se deroule ici).
CATEGORIES = {
    "dev": ("outil", "routine", "bdd", "pilote", "matrice", "autre"),
    "reparation": ("outil", "routine", "bdd", "pilote", "marbre", "autre"),
    "doc": ("manuel", "contrat", "lecon", "autre"),
    "audit": ("marbre", "flux", "file", "autre"),
    "revision": ("marbre", "contrat", "regle", "protocole", "autre"),
    # Les quatre types du CANAL USER (decision createur 2026-09-30). Ils ne
    # corrigent rien : ils nomment une demande du user qu aucune des cinq
    # categories precedentes ne savait dire. `question` attend une REPONSE --
    # d ou `reponse`, que `dev` ne veut pas dire. `cablage` porte le controle
    # d un CABLAGE, pas d un contenu. `preparer` est un travail de cadrage
    # amont. `cadrage` est le type de [???] : le user demande la liste des
    # actions AVANT de resoudre, donc un travail dont le livrable est un plan.
    "question": ("reponse", "explication", "autre"),
    "cadrage": ("plan", "exploration", "autre"),
    "cablage": ("cablage", "contrat", "autre"),
    "preparer": ("plan", "cadrage", "autre"),
    # `investigation` : on controle l EFFET obtenu, pas son branchement.
    "investigation": ("controle", "certification", "autre"),
    # `tache` : une COMMANDE. Ce qui est produit n est pas son objet, c est son
    # resultat -- donc pas de categorie qui nomme une matiere (pas de bdd, pas de
    # protocole). On dit ce qu on FAIT : executer, produire, deliver.
    "tache": ("execution", "production", "autre"),
}

# Categorie par defaut d'un type (quand aucun mot-cle ne parle).
CATEGORIES_DEFAUT = {
    "dev": "autre",
    "reparation": "autre",
    "doc": "autre",
    "audit": "autre",
    "revision": "autre",
    "question": "reponse",
    "cadrage": "plan",
    "cablage": "cablage",
    "preparer": "plan",
    "investigation": "controle",
    "tache": "execution",
}

# Echelon 3 : les niveaux d'urgence (du plus urgent au moins urgent).
# --- AUTO-VALIDATION (MO-175, decision createur 2026-09-18) -------------------
# Le verdict vit dans l ENREGISTREMENT DE LA MISSION (jamais dans un document),
# il est RENDU par un AVIS MULTI-AXES a la CREATION, et il ouvre la FILE
# AUTO-VALIDEE -- transverse aux types : elle ne contient QUE les items declares
# auto-valides au moment de la creation (decision du createur).
# --- ETIQUETTES DE L ITEM (nom de champ : une seule declaration, L-035) ------
# MO-213 : la categorie se REPARE comme le role (`retiqueter --categorie`), donc
# son nom de champ devient une constante consommee, plus un litteral disperse.
CHAMP_CATEGORIE = "categorie"
CHAMP_AUTO_VALIDATION = "auto_validation"
CHAMP_AUTO_AXES = "auto_validation_axes"

# LE REJEU DE L AUTO-VALIDATION (EO-491). Les axes sont poses A LA NAISSANCE et
# plus JAMAIS rejoues : un item corrige garde donc un vote que son texte ne
# justifie plus, et aucun verbe ne pouvait le remettre a jour. Deux champs, deux
# sens :
#   auto_validation_texte : l EMPREINTE du texte sur lequel le vote a ete rendu.
#     C est la PROVENANCE du vote -- sans elle, un rejeu ne peut pas distinguer
#     "rien n a bouge" de "le texte a bouge", et il debiterait du bruit.
#   reevaluations : la TRACE des rejeux (date, verdict avant/apres, axes bougees).
#     Un rejeu sans trace d ecart serait invisible ; avec elle, il est auditable
#     comme le sont les corrections.
CHAMP_AUTO_VALIDATION_TEXTE = "auto_validation_texte"
CHAMP_REEVALUATIONS = "reevaluations"
VERDICT_AUTO = "auto"
VERDICT_NON = "non"
# L auto-validation est un INDEX d ids (JAMAIS une copie de mission) : une mission
# presente dans deux listes = deux verites, et le brin se BLOQUE dessus (mesure
# MO-175 : tresser ne rend jamais la main quand un id vit dans deux files).
CLE_AUTO_VALIDEES = "auto_validees"
# MEMOIRE DE NAISSANCE (MO-334) : l identite de chaque item CONSOMME, gardee dans
# l ETAT de l entonnoir -- l item emporte ses trois champs en partant, et sa tombe
# les dit. Elle se lit quand l item n est plus la, jamais a sa place. Meme litteral
# que pilote/constants.py -- les deux doivent rester EGAUX.
CLE_MEMOIRE_NAISSANCE = "memoire_naissance"

# --- LE SOLDE D UN ITEM DEJA SATISFAIT (EO-379, MO-423) -----------------------
# Un item nomme un FAIT, pas la mission. QUATRE items du lot REPRISE DU RETARD
# (EO-310, EO-276, EO-277, EO-307) decrivaient un travail DEJA livre : la mission
# nee pour eux a du CONSTATER (verdict deja-faite) au lieu de construire. Un audit
# qui lit l ENONCE d un item mesure le TEXTE, jamais le DISQUE (L-155). D ou le
# SOLDE : l item sort de l entonnoir AVEC la PREUVE qui l a satisfait, sans naitre
# en mission. La trace vit dans l ETAT, a cote de la memoire de naissance -- elle se
# lit quand l item n est plus la. Meme discipline que la memoire : un solde SANS
# preuve est REFUSE (un solde muet serait exactement le defaut qu il ferme).
CLE_SOLDES = "soldes"
CHAMP_PREUVE_SOLDE = "preuve"
CHAMP_MOTIF_SOLDE = "motif"
CHAMP_SOLDE_LE = "solde_le"
# Nom de la file LEGACY (avant la conversion en index) : garde pour l auto-soin.
CLE_LEGACY_AUTO_VALIDEE = "auto-validee"
# Le TYPE PROPOSE au depot (R5, audit MO-174) : le crochet du createur peut le
# DECLARER (`deposer --type`), sinon il est propose par mots entiers. Il est
# desormais PORTE par l item -- plus seulement IMPRIME : un type affiche puis
# perdu ne route rien, et le crochet redeviendrait decoratif.
CHAMP_TYPE_PROPOSE = "type_propose"
MOT_CLE_DECLARE = "type declare"
# L ORIGINE du type (EO-192, decision createur 2026-09-19) : l item doit dire D OU
# vient son type, sinon le classement ne peut pas savoir ce qu il a le DROIT de
# consommer. Meme discipline que role_source (declaration / table). Trois valeurs,
# aucune devinee :
#   declaration -> le crochet du createur ou --type : SOUVERAIN, il CLASSE ;
#   mot-cle     -> la table MOTS_CLES_TYPES a parle (mot ENTIER) : elle PROPOSE ;
#   defaut      -> personne n a parle : c est un repli, il ne classe rien.
CHAMP_TYPE_SOURCE = "type_source"
SOURCE_TYPE_DECLARATION = "declaration"
SOURCE_TYPE_MOT_CLE = "mot-cle"
SOURCE_TYPE_DEFAUT = "defaut"
# Le nom NU de l avis (super-combo hors pilote) : le chemin se resout chez qui appelle.
NOM_EVALUATEUR = "evaluer-auto-validation.py"

# --- SOURCES (F1, 2026-09-19, decision createur) ------------------------------
# Le champ `source` etait LIBRE pour l agent et lu comme un ENUM a UNE seule
# valeur par l avis d auto-validation (axe `deja-vu`) : un champ, DEUX sens
# (meme classe que EO-154, deja tranchee). Mesure : la MEME mission rendait POUR
# avec `createur` nu et CONTRE avec une trace honnete datee -- l avis refusait
# donc d enchainer exactement ce que l agent avait pris soin de tracer.
# La provenance est desormais FERMEE : une valeur hors liste se REFUSE (elle ne
# se replie pas), et la trace libre (date, motif) vit dans CHAMP_SOURCE_TRACE.
# ORDRE SIGNIFICATIF : SOURCES[0] est la provenance par DEFAUT, et c est le SEUL
# cas ou l avis vote POUR sur `deja-vu` (une reparation vue avec le createur).
SOURCES = ("createur", "veille", "redeport", "audit-nemesis")
# La TRACE libre (date, motif, contexte) de la provenance : son PROPRE champ,
# jamais le champ ferme `source` -- un champ, un sens.
# MO-421 : la case [depot] du CADRAGE met dans `--trace` la PLACE du maillon
# (<chaine, maillon k/n>) ; ce champ est donc la PORTEUSE de l ORDRE. Il SURVIT
# desormais a la naissance : recopie sur la MISSION par le pont et par le chemin
# manuel (commun.trace_depuis_item / trace_de_l_item), et AFFICHE par l injection.
# Avant, l item mourait a la naissance et l ordre n etait plus lisible nulle part
# (mesure : 0 maillon sur 7 ne declarait son rang).
CHAMP_SOURCE_TRACE = "source_trace"

# --- LA LISTE DES OUTILS PREPAREE SUR L ITEM (EO-313, demande createur 2026-09-20) --
# Un item peut DECLARER les outils que SA mission va appeler. Pourquoi sur l ITEM et
# non sur la mission : l item est la MEMOIRE DURABLE (il survit au redemarrage, la
# mission n existe qu au chargement), et c est l item que la porte `preparer` atteint
# AVANT que la mission existe. Le pont item -> mission la RECOPIE.
# Sans elle, les outils d une mission etaient une FONCTION DE SON TYPE
# (checklist/listes.py OUTILS_PAR_TYPE) : deux missions du meme type recevaient les
# MEMES outils, et un outil qu UNE mission precise appelle ne pouvait pas lui etre livre.
CHAMP_OUTILS = "outils"
# Trace de la preparation : la liste d AVANT est conservee, comme role_avant et
# categorie_avant -- on ne reecrit jamais une identite en silence.
CHAMP_OUTILS_LE = "outils_le"
CHAMP_OUTILS_AVANT = "outils_avant"
# Le PLAFOND n est PAS recopie ici : il vit au domicile de l INJECTION
# (pilote/constants.py PLAFOND_OUTILS_MODE_EMPLOI), que la porte `preparer` importe.
# Un plafond recopie est un plafond qui derive, et la porte refuserait alors une
# liste que l injection servirait volontiers (ou l inverse).

# --- L IMPORTANCE D UN ITEM (EO-457, demande createur 2026-09-27) -------------
# Les DEUX champs d importance d un item viennent du DOMICILE de la carte
# d identite (matrice/data/commun/carte_identite.py) : ils sont CONSOMMES, jamais
# recopies (M-076). L item les RECOPIE depuis la carte de son document source
# quand elle existe, sinon il prend les DEFAUTS du domicile. GRAVITE (la bande)
# d abord, NIVEAU (le raffinement dans la bande) ensuite.
def _domicile_importance():
    """Le module DOMICILE de l importance, ou un REFUS NOMME (jamais un defaut muet).

    La racine `matrix` se DETECTE par marqueur (aucun parents[N] nu) : un domicile
    introuvable ARRETE le chargement -- une importance devinee serait exactement le
    critere invente que la mission interdit.
    """
    import sys as _sys
    from pathlib import Path as _Path
    depart = _Path(__file__).resolve()
    for parent in depart.parents:
        domicile = parent / "matrice" / "data" / "commun"
        if (domicile / "carte_identite.py").is_file():
            if str(domicile) not in _sys.path:
                _sys.path.append(str(domicile))
            import carte_identite as _carte
            return _carte
    raise RuntimeError("domicile carte_identite introuvable depuis " + str(depart))


_CARTE_IDENTITE = _domicile_importance()
CHAMP_GRAVITE = _CARTE_IDENTITE.CLE_GRAVITE
CHAMP_NIVEAU = _CARTE_IDENTITE.CLE_NIVEAU
GRAVITES = _CARTE_IDENTITE.GRAVITES
GRAVITE_DEFAUT = _CARTE_IDENTITE.GRAVITE_DEFAUT
NIVEAU_DEFAUT = _CARTE_IDENTITE.NIVEAU_DEFAUT

URGENCES = ("bloquante", "haute", "normale", "basse")

# Urgence par defaut quand le createur ne precise pas.
URGENCE_DEFAUT = "normale"

# Urgence obligatoire pour une mission deposee par la veille (M-020).
URGENCE_VEILLE = "bloquante"

# Regles de classement propose (echelon 1) : mot-cle dans theme+objectif -> type.
MOTS_CLES_TYPES = (
    ("reparer", "reparation"),
    ("reparation", "reparation"),
    ("raccorder", "dev"),
    ("construire", "dev"),
    ("creer", "dev"),
    ("verifier", "audit"),
    ("audit", "audit"),
    ("documenter", "doc"),
    ("manuel", "doc"),
    ("contrat", "doc"),
    ("revision", "revision"),
    ("reviser", "revision"),
)

# Regles de classement propose (echelon 2) : mot-cle -> categorie.
MOTS_CLES_CATEGORIES = (
    ("outil", "outil"),
    ("bdd", "bdd"),
    ("routine", "routine"),
    ("pilote", "pilote"),
    ("marbre", "marbre"),
    ("manuel", "manuel"),
    ("contrat", "contrat"),
    ("lecon", "lecon"),
    ("protocole", "protocole"),
    ("regle", "regle"),
)

# Prefixe des ITEMS de CET entonnoir (regle CV-009 : une famille = un prefixe,
# jamais partage). E- etait emis par les DEUX entonnoirs avec DEUX compteurs
# separes (cameleon/fichier 89, Optimus/fichier 101) : les deux plages se
# recouvraient (E-084..E-089 emis des deux cotes), donc le meme id designait
# deux items differents -- exactement la maladie de M- (mission d'Optimus
# portant le prefixe du cameleon). Meme remede : Optimus prend SON prefixe.
# Le cameleon garde E- : ses ids sont dans des journaux en AJOUT SEUL
# (historiques-missions.jsonl), un renommage les ferait mentir.
PREFIXE_ITEM = "EO-"

# Chemin du fichier des files de l'entonnoir (a cote de file-missions.json).
# Nom CANONIQUE de l'entonnoir OPTIMUS (alignement MO-033) : le pilote
# (constants.py NOM_ENTONNOIR + commun.py CHEMIN_ENTONNOIR) lit/ecrit deja
# entonnoir-files-optimus.json -- l'outil ecrivait l'ANCIEN nom
# "entonnoir-files.json", donc les missions deposees n'etaient pas vues
# par le pilote. Jamais le nom du cameleon (matrice/pilote/entonnoir-files.json).
NOM_ENTONNOIR = "entonnoir-files-optimus.json"
