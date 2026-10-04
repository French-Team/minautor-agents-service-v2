"""Fonctions simples de la categorie solder : SOLDER un item DEJA satisfait.

MO-423 (EO-379). Un item nomme un FAIT, pas la mission : QUATRE items du lot
REPRISE DU RETARD (EO-310, EO-276, EO-277, EO-307) decrivaient un travail DEJA
livre -- la mission nee pour eux a du le CONSTATER (verdict deja-faite) au lieu de
le construire. La consommation transforme un item en mission ; or un audit qui lit
l ENONCE d un item mesure le TEXTE, jamais le DISQUE (L-155). D ou ce verbe : un
item dont le travail EXISTE DEJA se SOLDE -- il sort de l entonnoir AVEC la PREUVE
qui l a satisfait (fichier:ligne, porte/verbe, mesure), au lieu de naitre en
mission. Un solde SANS preuve est REFUSE : un solde muet serait exactement le
defaut qu il ferme.
"""


def solder_item(etat, identifiant, preuve, motif=""):
    """(code, message) : sort l item de TOUT l entonnoir et TRACE sa PREUVE.

    Le retrait emprunte les DEUX portes de `retirer` (vrac puis files) et recompose
    le brin -- un solde qui oublierait une place laisserait l item reverdir au
    prochain tissage. La trace vit dans l ETAT (CLE_SOLDES), son domicile : elle se
    lit quand l item n est plus la, et elle DIT ce qui l a satisfait.
    """
    try:
        from listes import (CHAMP_MOTIF_SOLDE, CHAMP_PREUVE_SOLDE, CHAMP_SOLDE_LE,
                            CLE_SOLDES)
        from stockage import horodater, verifier_famille
        from retirer.fonctions import (recomposer_brin, retirer_des_files,
                                       retirer_du_vrac)
    except ImportError:  # importe comme paquet (depuis le pilote) : chemins complets
        from entonnoir.listes import (CHAMP_MOTIF_SOLDE, CHAMP_PREUVE_SOLDE,
                                      CHAMP_SOLDE_LE, CLE_SOLDES)
        from entonnoir.stockage import horodater, verifier_famille
        from entonnoir.retirer.fonctions import (recomposer_brin, retirer_des_files,
                                                 retirer_du_vrac)

    preuve = str(preuve or "").strip()
    if not preuve:
        return 2, ("REFUS (solde sans preuve) : un solde doit DIRE ce qui a satisfait "
                   "l item -- fichier:ligne, porte/verbe, ou mesure. Un solde muet ne "
                   "prouve rien (MO-423).")
    code, message = verifier_famille(identifiant)
    if code != 0:
        return code, message
    soldes = etat.setdefault(CLE_SOLDES, [])
    for solde_connu in soldes:
        if str(solde_connu.get("id")) == str(identifiant):
            return 0, ("item deja solde : " + str(identifiant)
                       + " (rien a faire -- la trace existe deja)")
    porte, message_porte = retirer_du_vrac(etat, identifiant)
    if porte != 0:
        porte, message_porte = retirer_des_files(etat, identifiant)
    if porte != 0:
        return 1, "item inconnu (vrac et files) : " + str(identifiant)
    recomposer_brin(etat)
    solde = {"id": str(identifiant), CHAMP_PREUVE_SOLDE: preuve,
             CHAMP_SOLDE_LE: horodater()}
    motif = str(motif or "").strip()
    if motif:
        solde[CHAMP_MOTIF_SOLDE] = motif
    soldes.append(solde)
    return 0, ("Item " + str(identifiant) + " SOLDE (retire, NON consomme en mission)"
               + " -- preuve : " + preuve)
