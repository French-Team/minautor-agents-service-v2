"""Fonctions simples de la categorie verifier : une seule tache chacune."""


def verifier_cles_canoniques(donnees, canoniser):
    """ECART quand une cle n'est pas a SA forme canonique (EO-363, 2026-09-22).

    C'est le GARDE du domicile unique : `noter` canonise ce qu'il ecrit, et ce
    controle refuse (EN LE DISANT) une cle posee autrement -- a la main, ou par
    un appelant qui ecrirait la BDD lui-meme. La regle n'a qu'un domicile :
    `canoniser` est PASSEE en argument, jamais recopiee ici (L-029).

    Retourne (succes, message) : le message NOMME les cles fautives et le remede,
    pour qu'un rouge ne coute pas trois essais (friction 77).
    """
    fichiers = (donnees or {}).get("fichiers", {}) or {}
    fautives = sorted(cle for cle in fichiers if canoniser(cle) != cle)
    if not fautives:
        return True, ("Cles canoniques : " + str(len(fichiers))
                      + " cle(s), toutes relatives a la racine de la Matrice.")
    return False, ("ECART : " + str(len(fautives)) + " cle(s) NON canonique(s) -- la forme "
                   "attendue est RELATIVE a la racine de la Matrice : "
                   + ", ".join(fautives[:6]) + (" ..." if len(fautives) > 6 else "")
                   + " (remede : bdd-modifications canoniser)")


def verifier_cles_anchorables(donnees, designer):
    """ECART quand une cle, meme CANONIQUE, ne DESIGNE aucun fichier (MO-577).

    LE TROUS QUE LA FORME NE VOIT PAS. `verifier_cles_canoniques` controle la
    FORME : une cle relative et prefixee-la comme il faut passe. Mesure du
    2026-10-04 : sur 1174 cles, 213 designaient un fichier inexistant -- donc 213
    fiches muettes, porteuses de 275 entrees d historique, qu aucun controle ne
    voyait. Une forme juste ne garantit pas qu elle ANCRE.

    CE QUE CE CONTROLE FAIT ET NE FAIT PAS. Il ne DISPARAIT rien et ne purge
    rien : une disparition est une DECISION de conservation, prise par une autre
    porte, avec son motif. Ici on se contente de DIRE -- un registre qui porte
    des fiches mortes sans le dire laisse croire a une histoire complete, et c
    ce mensonge-la qui coute cher (MO-576 : six accuses sans auteur).

    La regle d ancrage est PASSEE en argument, jamais recopiee : un seul
    domicile (L-029). Le message nomme les marches et le nombre, pour qu un rouge
    ne coute pas trois essais (friction 77).
    """
    fichiers = (donnees or {}).get("fichiers", {}) or {}
    orphelines = sorted(cle for cle in fichiers if not designer(cle))
    if not orphelines:
        return True, ("Cles ancrables : " + str(len(fichiers))
                      + " cle(s) designent chacune un fichier existant.")
    porteuses = sum(len((fichiers[cle].get("modifications", []) or []))
                    for cle in orphelines)
    return False, ("ECART : " + str(len(orphelines)) + " cle(s) ORPHELINE(s) -- la forme "
                   "est canonique mais le fichier n existe plus : "
                   + ", ".join(orphelines[:6])
                   + (" ..." if len(orphelines) > 6 else "")
                   + " | entrees d historique portees : " + str(porteuses)
                   + " (une cle ORPHELINE ne se purge pas ici : c est une decision"
                     " de conservation, prise par bdd-conservation declarer-disparition)")


def verifier_integrite(empreinte_reelle, empreinte_enregistree):
    """Compare l'empreinte recalculee a l'empreinte enregistree (etalon-or).

    Retourne (succes, message) : le message dit ce qui casse, ou pourquoi.
    """
    if empreinte_reelle is None:
        return (False, "ECART : la BDD est absente ou illisible a l'emplacement attendu.")
    if empreinte_enregistree is None:
        return (False, "ECART : aucune empreinte enregistree (la BDD n'a jamais ete ecrite par l'outil).")
    if empreinte_reelle == empreinte_enregistree:
        return (True, "Integrite verifiee : empreinte " + empreinte_reelle[:16] + "...")
    return (
        False,
        "ECART : empreinte reelle "
        + empreinte_reelle[:16]
        + "... != enregistree "
        + empreinte_enregistree[:16]
        + "... (la BDD a ete modifiee hors de l'outil).",
    )
