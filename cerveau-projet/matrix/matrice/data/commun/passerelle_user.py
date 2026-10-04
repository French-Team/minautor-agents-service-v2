"""Domicile unique de la PASSERELLE USER -- le dossier `user-demandes/` (MO-475, MO-492).

CE QU ELLE EST (son role, dit par son propre en-tete -- decision createur).
`user-demandes/user-demandes.md` est la PASSERELLE DE COMMUNICATION entre le USER
et OPTIMUS, via la Matrice : le user y ecrit ses demandes en clair, l une apres
l autre, et la Matrice les LIT, les SUIT et les EXTRAIT vers l entonnoir puis le
pilote. Ce n est donc PAS un dossier inerte : c est une SOURCE DE MISSIONS.

SON FORMAT (declare par son en-tete, et c est le user qui le tient).
Chaque demande est encadree par DEUX delimiteurs : celui qui la precede (le pattern
de debut) et le suivant (sa fin). Les patterns declares a ce jour : `##A-FAIRE###`,
`##FAIT###` (deja vu + execute), `##A-CONTROLER###` (execute, pas encore controle,
valide ou certifie), `##CERTIFIER###` (fait et certifie). Un pattern ne franchit
JAMAIS deux etapes dans la meme mission : chaque etape est une injection, donc une
mission. Le crochet d entree (`[mission]`, `[question]`, `[audit]`, `[revision]`,
`[preparer]`, `[???]`...) dit ce que la demande declenche.

SON CYCLE DE VIE (mesure -- c est ce qui la distingue d un journal).
Quand une mission a ete EXTRAITE, elle est RETIREE du fichier : a la fin, le
fichier conserve le HEAD (carte d identite + mode d emploi) et les demandes NON
ENCORE extraites. Le fichier ne grossit donc pas par accumulation : il se vide de
ce qui a ete servi.

POURQUOI ELLE EST HORS JUGEMENT (et ce n est PAS un oubli).
Le fichier est ecrit par le USER LUI-MEME, en continu, hors de TOUTE porte de la
Matrice (mesure MO-475 du 2026-09-26 : reecrit toutes les quelques secondes
pendant la session), et dans SA langue (accents, apostrophes, crochets). Ce n est
pas une source du projet : aucune porte ne le produit, aucune ne le repare. Le
CORRIGER mutilerait la parole du user (meme raison que `docs/`, MO-377), et le
juger comme une ecriture non attribuee accuserait une ecriture LEGITIME a chaque
passe. On ne juge pas ce qui n est pas une source ; on le DECLARE et on le DIT
(L-104 : une exclusion muette est un angle mort qu aucune suite ne voit).

LE DEFAUT REPARE ICI (mesure du 2026-09-29, round MO-492).
La decision du createur etait ECRITE DANS L INSTRUMENT QUI LA CONSOMME
(`controle-attribution.py`, constante `DOSSIER_DEMANDES_OPERATEUR`) au lieu de
l etre A SON DOMICILE : `garde-ascii`, un AUTRE instrument de la MEME maison,
accusait donc la MEME zone (code 1 sur `user-demandes/user-demandes.md`) et
`/sante` portait un rouge pour une ecriture LEGITIME. C est la famille exacte que
MO-377 avait fermee pour `docs/`. La regle qui fait foi l avait annonce :
`regles-immuables/ascii-strict.md` -- < une exception qui n est pas ECRITE ici sera
re-inventee par le prochain scan : c est ce fichier qui fait foi, pas le code >.

CONSOMMATEURS (une seule declaration, M-076) :
  - `controle-attribution.py` : hors du jugement d attribution (MO-475) ;
  - `garde-ascii.py` : mise HORS CHAMP, NOMMEE et COMPTEE (jamais accusee) ;
  - tout scan a venir qui parcourt la Matrice : il lit ici, il ne devine pas.

CE QUE CE MODULE NE FAIT PAS : il ne LIT pas la passerelle et n en extrait rien.
L extraction des demandes (vers l entonnoir puis le pilote), son readme, sa carte
d identite et son template de delimiteurs sont des TRAVAUX, pas des declarations :
ils sont deposes en item, jamais decides ici.
"""
import re

from cible import forme_canonique


NOM_PASSERELLE_USER = "user-demandes"
ROLE_PASSERELLE_USER = ("passerelle de communication user <-> optimus via la Matrice "
                        "(le user y ecrit ses demandes en clair, la Matrice les suit et "
                        "les extrait vers l entonnoir puis le pilote)")
MOTIF_PASSERELLE_USER = ("passerelle USER (user <-> optimus) -- ecrite en clair par le "
                         "user, hors de toute porte de la Matrice : jamais corrigee, "
                         "jamais accusee (decision createur MO-475)")


def chemin_canonique(chemin):
    """La forme canonique (relative a la racine de la Matrice), en forme POSIX.

    Le domicile de FORME est CONSOMME (cible.forme_canonique), jamais recopie :
    une forme qui depend de qui l ecrit ne se compare ni ne se mesure (EO-363).
    """
    return forme_canonique(chemin).replace("\\", "/")


# --- LA ZONE HORS ASCII (la passerelle) : la porte ecrire le CONSOMME -------
# La REGLE vit ici, a SON domicile, et la porte d ecriture la consomme (M-076).
# Elle existe parce que la passe use des mots non-ASCII (mesure : 101 caracteres,
# dont 2 U+00B0, dans le canal), et que ces caracteres sont ceux du createur, pas
# les notres : une porte qui les convertirait REECRIRAIT sa demande.

MOTIF_HORS_CHAMP_ASCI = (
    "hors ASCII : `user-demandes/` est la passerelle du createur (regle "
    "ascii-strict.md, decision MO-475). Ses fichiers portent les MOTS DU USER, "
    "qu on ne convertit pas et qu on ne refuse pas : la porte laisse passer et le "
    "dit. La conversion reste obligatoire PARTOUT ailleurs."
)


def hors_champ_ascii(chemin):
    """Le MOTIF qui dit pourquoi ce chemin est hors ASCII, ou None.

    Vrai pour la passerelle seule : `docs/` (zone des sources) est LECTURE SEULE,
    donc la porte la REFUSE a l ecriture -- ce n est pas la meme question. La
    passerelle s ecrit (le user y parle, l outil y depose) : elle est donc hors
    ASCII, pas hors ecriture.
    """
    if est_passerelle_user(chemin):
        return MOTIF_HORS_CHAMP_ASCI
    return None


def est_passerelle_user(chemin):
    """True si <chemin> designe la passerelle (PREMIER segment = user-demandes).

    La zone est designee par sa POSITION, comme `docs/` : c est ce qui distingue
    `user-demandes/` (la passerelle, a la racine de la Matrice) d un dossier
    homonyme plus profond, qui reste juge. La mesure a couvert les DEUX fichiers
    de la passerelle, y compris celui d un sous-dossier (`le-vivier/`).
    """
    canonique = chemin_canonique(chemin)
    if not canonique:
        return False
    return canonique.split("/", 1)[0] == NOM_PASSERELLE_USER


# --- LE FORMAT DU CANAL (mesure du 2026-09-29, MO-505) ------------------------
# La convention REELLE du canal, mesuree sur le corpus (34 blocs pour 34
# demandes) : chaque demande est PRECEDEE d un BLOC de lignes de patternes
# consecutives ; le PREMIER mot du bloc est l ETAT de la demande (mesure : 34/34 =
# A-FAIRE, donc aucune n avait encore ete extraite) ; les lignes suivantes du bloc
# forment son ECHELLE (les etapes preparees, dans l ordre du user) ; une ligne de
# patternes SANS mot est le pattern a lire que l en-tete declare. Le jugement vit
# ICI, une seule fois : la porte d extraction le CONSOMME (M-076).
ETATS = ("A-FAIRE", "FAIT", "A-CONTROLER", "CERTIFIER")
MOTIF_LIGNE_PATTERN = re.compile(r"^#+[A-Z0-9\-]*#*$")


def est_ligne_pattern(ligne):
    """True si <ligne> est une ligne de patternes : que des #, majuscules, chiffres, tirets.

    La forme est JUGEE, pas devinee : un titre markdown (`## Mode d emploi`) porte
    des minuscules -- il n est donc PAS un pattern, et le head du canal n en
    fabrique aucun par accident.

    ELLE COMMENCE EN COLONNE 0 (mesure du 2026-10-03, MO-558). Sans cette
    condition, le SQUELETTE du mode d emploi -- un bloc de patterns INDENTE,
    qu on montre a copier -- etait lu comme la tete d une demande, et le
    canal comptait 37 demandes au lieu de 36 : la fausse demande portait le
    texte du gabarit. Le createur ecrit ses patterns en colonne 0 (65 lignes
    mesurees) ; une ligne INDENTEE est une illustration dans un bloc de code.
    Sans cela, tout mode d emploi du canal se transformerait en demande.
    """
    if ligne[:1].isspace():
        return False
    # On ne refuse que le DEBUT en retrait, pas la FIN : un canal CRLF porte un
    #  en fin de ligne, et c est precisement ce  que l ancien 
    # absorbait. Le supprimer ici ferait qu aucune ligne de pattern ne serait
    # reconnue dans un canal CRLF -- et le retrait d une demande echouerait
    # (mesure : le maillon 68 le voit, il joue un canal CRLF entier).
    return bool(MOTIF_LIGNE_PATTERN.match(ligne.rstrip()))


def mot_pattern(ligne):
    """Le MOT d une ligne de patternes ("" pour le pattern a lire, celui sans mot)."""
    return ligne.strip().strip("#")


# --- L AVANCEMENT D UNE DEMANDE, DIT PAR SON BLOC (MO-561) -------------------
# C est le DERNIER mot du bloc de patterns qui dit ou on en est (decision
# createur 2026-10-03) : un bloc qui ne porte QUE le premier mot est une demande
# INTOUCHEE ; des qu il en porte un deuxieme, elle est ENGAGEE -- du travail a ete
# fait et elle attend d etre finie. L echelle se lit donc par sa FIN, jamais par
# son debut.
#
# DEUX valeurs et pas quatre : le createur a tranche la regle simple, une demande
# engagee passe avant une demande intouchee. Un palier par etape aurait ete plus
# fin et plus faux -- il aurait ordonne FAIT avant A-CONTROLER, alors que le
# createur veut que le CONTROLE d abord.
AVANCEMENT_ENGAGE = "engage"
AVANCEMENT_INTOUCHE = "intouche"


def avancement_de(demande):
    """L avancement d une demande du canal, deduit de son bloc de patterns.

    La REGLE vit ici, dans le domicile commun du canal, et une seule fois : les
    deux chemins qui deposent une demande l appellent (M-076). Une valeur deduite
    ne peut pas etre fausse : elle compte des MOTS, pas une intention.
    """
    echelle = demande.get("echelle") or []
    return AVANCEMENT_ENGAGE if len(echelle) > 1 else AVANCEMENT_INTOUCHE


def crochet_de(texte):
    """Le PREMIER crochet d entree du texte (ex. [mission], [???]), ou "".

    Le crochet appartient au USER : il n est jamais ferme ici, et un crochet
    inconnu est DIT par l appelant -- jamais corrige.
    """
    trouve = re.search(r"\[[^\]\n]{1,20}\]", texte)
    return trouve.group(0) if trouve else ""


# --- LE CROCHET D ENTREE, ET LE TYPE QU IL DECLARE (MO-562) -------------------
# La table crochet -> type est LA SEULE traduction du vocabulaire du user vers
# celui de la Matrice. Elle vit ICI, au DOMICILE COMMUN du canal, et une seule
# fois (M-076) : elle a deux consommateurs reels, et une copie chez chacun
# derive. Mesure MO-562 : la porte `deposer` ne lisait pas le crochet ecrit dans
# le titre, donc une demande `[question]` saisie a la main etait classee `dev`
# (item EO-482, type_source=defaut). Le createur ecrit pourtant TOUJOURS un
# crochet -- mesure : 36 demandes sur 36, et le crochet est en TETE du titre
# dans les 36. Une notation complete que rien ne lit est une notation perdue.
#
# On ne deplace pas la table pour la deplacer : elle reste ecrite ENTIERE et
# contestable d un seul regard -- a son seul domicile. C est l outil
# `passerelle-demandes` qui l emporte, pas la regle qui change.
CROCHETS_TYPES = {
    "mission": "dev",
    "revision": "revision",
    "audit": "audit",
    "question": "question",
    "???": "cadrage",
    "cablage": "cablage",
    "preparer": "preparer",
    "preparation": "preparer",
    "tache": "tache",
    "investigation": "investigation",
    "crochet": "crochet",
}


def nom_du_crochet(crochet):
    """Le NOM du crochet, crochets compris : `[question]` rend `question`.

    Un crochet INCONNU rend la CHAiNE VIDE telle quelle -- jamais une correction.
    Le crochet appartient au createur : une faute de frappe est une information,
    pas une faute a reparer.
    """
    nom = str(crochet or "").strip()
    if nom.startswith("[") and nom.endswith("]"):
        nom = nom[1:-1].strip()
    return nom


def type_du_crochet(crochet):
    """Le type que le crochet DECLARE, ou "" s il ne declare rien de connu.

    VIDE et non `dev` : un crochet qu on ne sait pas lire ne se replie SUR RIEN.
    L appelant decide -- il refuse, ou il demande -- mais il ne peut pas heriter
    d un type que personne n a ecrit.
    """
    return CROCHETS_TYPES.get(nom_du_crochet(crochet).lower(), "")


def crochet_de_tete(titre):
    """Le crochet d entree du TITRE, mais SEULEMENT s il est en tete.

    Mesure du 2026-10-03 (MO-562) : sur les 36 demandes du canal, le crochet est
    en tete dans les 36. Une mention de crochet AU MILIEU d une phrase n est pas
    une declaration de type : `crochet_de` la trouve, celle-ci ne la croit pas.
    C est la meme discipline que la ligne de pattern (MO-558) : on lit la FORME,
    jamais l intention.
    """
    tete = str(titre or "").lstrip()
    trouve = re.match(r"^\[[^\]\n]{1,20}\]", tete)
    return trouve.group(0) if trouve else ""


# --- LA RECONNAISSANCE D UNE DEMANDE DEJA SERVIE (EO-538, mesure MO-509) ---
# La REGLE vit ICI, dans le domicile commun, et une seule fois : les DEUX
# chemins qui deposent une demande du canal l Appellent (M-076 : un moteur se
# partage, il ne se recopie pas). Elle etait jusqu ici dans l outil
# `passerelle-demandes`, donc le second chemin -- l extraction du pilote --
# n en avait pas, et pouvait deposer une seconde fois une demande servie.
PREFIXE_TRACE_DEFAUT = "canal"


def normaliser(texte):
    """La CLEF de comparaison d une demande : ASCII, espaces, casse.

    Trois normalisations, et pas une de plus. Les espaces et la casse sont
    sans risque ; l ASCII est une transcription, pas un jugement. On ne retire
    NI ponctuation NI accents de fond : deux demandes qui different par un
    point d interrogation ne sont pas la meme demande.
    """
    from carte_ascii import convertir_texte  # local : le domicile ne tire pas le socle
    return " ".join(convertir_texte(str(texte))[0].split()).strip().lower()


def titre_sans_crochet(titre, crochet):
    """Le TITRE d une demande, CROCHET RETIRE.

    Le crochet (`[revision]`, `[mission]`, `[???]`) est une CLE DE CLASSEMENT
    posee par le user, pas une partie de sa demande : l item depose le porte
    dans son `theme`, donc comparer un titre crochet a un theme nu ne
    rencontres jamais rien. On retire donc le crochet -- et SEULEMENT lui : les
    mots du user ne sont jamais reecrits.
    """
    texte = str(titre or "").strip()
    marque = str(crochet or "").strip()
    if marque and texte.startswith(marque):
        texte = texte[len(marque):].strip()
    return texte


def reconnaitre_demande(theme, ligne, par_trace, par_theme,
                        prefixe_trace=PREFIXE_TRACE_DEFAUT):
    """("trace"|"texte", id) si la demande est DEJA servie, ("", "") sinon.

    On rend le NIVEAU de la reconnaissance : une trace est une PREUVE, une
    correspondance de texte est une DEDUCTION. L appelant l affiche, donc le
    createur sait sur quoi repose le refus.

    Les deux niveaux sont exiges dans cet ordre, et l ordre n est pas
    decoratif : la trace nomme une LIGNE du canal, donc elle vaut meme si le
    texte a ete reecrit depuis ; le theme ne vaut que si le texte est
    reste identique. Reconnaitre par la trace d abord refuse plus tot.

    Les arguments sont EXPLICITES (theme, ligne) et non un dictionnaire :
    les deux chemins nomment leurs champs differemment, et une fonction qui
    lit une forme impose une forme aux deux appelants.
    """
    marqueur = prefixe_trace + " l." + str(ligne)
    if marqueur in par_trace:
        return "trace", par_trace[marqueur]
    identifiant = par_theme.get(normaliser(theme), "")
    if identifiant:
        return "texte", identifiant
    return "", ""


def decouper_demandes(texte):
    """(entete, demandes, anomalies) -- le canal decoupe par ses patternes.

    Une DEMANDE est le texte entre son bloc de patternes et le bloc SUIVANT (ou la
    fin du fichier). Elle porte son ETAT (premier mot du bloc), son ECHELLE (tous
    les mots du bloc), son CROCHET, son TITRE (premiere ligne non vide), son TEXTE
    et ses BORNES de lignes (pour un retrait EXACT, sans toucher au reste).
    L ENTETE est tout ce qui precede le PREMIER bloc : c est le head du canal.
    Les ANOMALIES sont DITES, jamais tues : un bloc suivi d un autre bloc (demande
    vide) et un mot d etat hors du vocabulaire declare.
    """
    lignes = texte.split("\n")
    blocs = []
    index = 0
    while index < len(lignes):
        if est_ligne_pattern(lignes[index]):
            debut = index
            mots = []
            while index < len(lignes) and est_ligne_pattern(lignes[index]):
                mots.append(mot_pattern(lignes[index]))
                index += 1
            blocs.append((debut, index, mots))
            continue
        index += 1

    entete = lignes[:blocs[0][0]] if blocs else list(lignes)
    anomalies = []
    demandes = []
    for rang, (debut, apres, mots) in enumerate(blocs):
        fin = blocs[rang + 1][0] if rang + 1 < len(blocs) else len(lignes)
        corps = list(lignes[apres:fin])
        while corps and not corps[-1].strip():
            corps.pop()
        etat = mots[0] if mots else ""
        if not corps and rang + 1 < len(blocs):
            anomalies.append("ligne " + str(debut + 1)
                             + " : un bloc de patternes SANS demande")
        if etat not in ETATS and etat != "":
            anomalies.append("ligne " + str(debut + 1)
                             + " : mot d etat INCONNU (" + etat + ")")
        titre = ""
        for ligne in corps:
            if ligne.strip():
                titre = ligne.strip()
                break
        demandes.append({
            "etat": etat,
            "echelle": list(mots),
            "crochet": crochet_de(titre),
            "titre": titre,
            "texte": "\n".join(corps),
            "ligne_debut": debut + 1,
            "ligne_fin": fin,
            "lignes_bloc": apres - debut,
            "lignes_corps": len(corps),
        })
    return entete, demandes, anomalies


def retirer_demande(lignes, demandes, rang):
    """Les LIGNES du canal, la demande <rang> RETIREE -- et RIEN d autre ne bouge.

    Le retrait emporte le BLOC de la demande et son texte, jamais les voisins : on
    travaille sur les bornes mesurees, pas sur une reconstruction. La derniere
    demande emporte sa queue (la fin du fichier) en gardant UNE ligne finale.
    """
    lignes = list(lignes)
    demandes = list(demandes)
    cible = demandes[rang]
    debut = cible["ligne_debut"] - 1
    fin = demandes[rang + 1]["ligne_debut"] - 1 if rang + 1 < len(demandes) else len(lignes)
    nouvelles = lignes[:debut] + lignes[fin:]
    if rang + 1 == len(demandes):
        while nouvelles and not nouvelles[-1].strip():
            nouvelles.pop()
        nouvelles.append("")
    return nouvelles
