"""Motif UNIQUE de la fiche profil utilisateur (matrix/USER-PROFIL.md).

Un seul etat du profil, une seule definition des champs attendus : la routine
`vigie-profil`, le pilote et les verificateurs IMPORTENT ce module, ils ne
recopient jamais la logique (M-076 : le motif partage ne se duplique pas).

MO-051 : le motif porte aussi l'ECRITURE (lire_valeurs + ecrire_valeurs). Le
questionnaire du parcours USER-PROFIL les utilise : sans elles il regenerait la
fiche depuis un template, donc il ecrasait tout (le parcours dit "ne jamais
ecraser les reponses existantes"). Le format d'une ligne de tableau reste
DECLARE ici et nulle part ailleurs.

Bug corrige (MO-043) : deux verificateurs pointaient un cran trop bas
(`_operateur/optimus-prime/USER-PROFIL.md` et `_operateur/USER-PROFIL.md`),
fichiers mythiques : ils annoncaient donc la fiche "absente" a chaque
demarrage et declenchaient un questionnaire bloque sur l'entree standard.
Ici le chemin est DETECTE (remontee gardee) : il ne peut plus se decaler.
"""
from pathlib import Path

NOM_FICHE = "USER-PROFIL.md"
MARQUEUR_MATRICE = ("matrice", "data")
BORNES_REMONTEE = 30

SEPARATEUR_TABLEAU = "|"
COLONNE_LIBELLE = 1
COLONNE_VALEUR = 2
COLONNE_STATUT = 3
COLONNES_MINIMUM = 4

MARQUEURS_VIDES = ("A remplir", "A choisir", "")

# Champs attendus (Informations Personnelles + Preferences) : un seul vide
# declenche l'alerte.
CHAMPS_ATTENDUS = (
    "Pseudo",
    "Age",
    "Langue",
    "Fuseau horaire",
    "Style de conversation",
    "Sujets d'interet",
    "Mode d'apprentissage",
    "Niveau technique",
)

# Champs optionnels (Contact + Notes) : informatifs, jamais declencheurs.
CHAMPS_OPTIONNELS = (
    "Email",
    "Discord",
    "Autre",
    "Commentaires",
    "Suggestions",
)


def repertoired_matrix(depart):
    """Remonte depuis <depart> jusqu'au dossier matrix/ qui contient matrice/data."""
    courant = Path(depart).resolve()
    for _ in range(BORNES_REMONTEE):
        if courant.name == "matrix" and (courant / MARQUEUR_MATRICE[0] / MARQUEUR_MATRICE[1]).is_dir():
            return courant
        if courant.parent == courant:
            break
        courant = courant.parent
    raise RuntimeError("Dossier matrix/ introuvable en remontant depuis " + str(depart))


def chemin_profil(depart):
    """Chemin de la fiche profil (a la racine de matrix/)."""
    return repertoired_matrix(depart) / NOM_FICHE


def lire_lignes(chemin):
    """Lignes de la fiche, ou None si elle est absente/illisible."""
    if not chemin.exists():
        return None
    try:
        return chemin.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None


def extraire_champ(ligne):
    """Retourne (libelle, rempli) d'une ligne de tableau, ou None.

    Ligne utile : | **Libelle** | Valeur | Statut |
    Rempli = valeur non vide ET statut hors marqueurs vides.
    """
    if SEPARATEUR_TABLEAU not in ligne:
        return None
    morceaux = [m.strip() for m in ligne.split(SEPARATEUR_TABLEAU)]
    if len(morceaux) < COLONNES_MINIMUM:
        return None
    libelle = morceaux[COLONNE_LIBELLE].replace("*", "").strip()
    if not libelle:
        return None
    valeur = morceaux[COLONNE_VALEUR]
    statut = morceaux[COLONNE_STATUT]
    if statut in MARQUEURS_VIDES or valeur in MARQUEURS_VIDES:
        return libelle, False
    return libelle, True


def etat(depart):
    """Etat de remplissage de la fiche.

    Retourne {present, chemin, attendus_remplis, attendus_vides,
    optionnels_vides, pourcentage}.
    """
    chemin = chemin_profil(depart)
    lignes = lire_lignes(chemin)
    if lignes is None:
        return {
            "present": False,
            "chemin": str(chemin),
            "attendus_remplis": [],
            "attendus_vides": list(CHAMPS_ATTENDUS),
            "optionnels_vides": [],
            "pourcentage": 0,
        }

    remplis = set()
    for ligne in lignes:
        champ = extraire_champ(ligne)
        if champ is None:
            continue
        libelle, est_rempli = champ
        if est_rempli:
            remplis.add(libelle)

    attendus_remplis = [c for c in CHAMPS_ATTENDUS if c in remplis]
    return {
        "present": True,
        "chemin": str(chemin),
        "attendus_remplis": attendus_remplis,
        "attendus_vides": [c for c in CHAMPS_ATTENDUS if c not in remplis],
        "optionnels_vides": [c for c in CHAMPS_OPTIONNELS if c not in remplis],
        "pourcentage": int(100 * len(attendus_remplis) / len(CHAMPS_ATTENDUS)),
    }


def cle(etat_profil):
    """Cle stable d'un etat (champs attendus vides) : signature anti-spam."""
    import hashlib

    brut = "|".join(sorted(etat_profil["attendus_vides"])) + "#" + str(etat_profil["present"])
    return hashlib.sha256(brut.encode("utf-8")).hexdigest()


def description(etat_profil, nom_fiche=NOM_FICHE):
    """Description courte, vraie et actionnable de l'etat (pour un signal)."""
    if not etat_profil["present"]:
        return (
            "Fiche " + nom_fiche + " ABSENTE a la racine de matrix/ : le parcours "
            "USER-PROFIL doit la recreer puis la remplir avec l'utilisateur."
        )
    return (
        "Fiche " + nom_fiche + " incomplete (" + str(etat_profil["pourcentage"])
        + "% des champs attendus) : " + str(len(etat_profil["attendus_vides"]))
        + " champ(s) a remplir avec l'utilisateur -- "
        + ", ".join(etat_profil["attendus_vides"])
        + ". Parcours : theme USER-PROFIL (questionnaire amical, une question a la fois)."
    )


def valeur_brute(ligne):
    """Valeur brute (cellule Valeur) d'une ligne de tableau, ou "" si ce n'en est pas une."""
    if SEPARATEUR_TABLEAU not in ligne:
        return ""
    morceaux = ligne.split(SEPARATEUR_TABLEAU)
    if len(morceaux) < COLONNES_MINIMUM:
        return ""
    return morceaux[COLONNE_VALEUR].strip()


def lire_valeurs(chemin):
    """Valeurs des champs REMPLIS : {libelle: valeur} ("" = encore a remplir).

    Meme jugement que `etat()` : une ligne dont le statut ou la valeur porte un
    marqueur vide ("A remplir", "A choisir") vaut "" -- un placeholder n'est
    PAS une reponse (sinon un ecrivain conserverait "Formel / Decontracte / Mixte"
    en croyant que le champ est deja rempli).
    """
    valeurs = {}
    for ligne in lire_lignes(chemin) or []:
        champ = extraire_champ(ligne)
        if champ is None:
            continue
        libelle, est_rempli = champ
        valeurs[libelle] = valeur_brute(ligne) if est_rempli else ""
    return valeurs


def ecrire_valeurs(chemin, valeurs, statut_fiche=None):
    """Met a jour la fiche SUR PLACE : seules les lignes des champs fournis changent.

    Rien d'autre n'est regenere (intro, frontmatter, contact, ajouts manuels) :
    c'est la seule facon de tenir "ne jamais ecraser les reponses existantes"
    sans dependre d'un template -- un template, lui, ecrase tout le reste.
    Ecriture atomique (tmp + remplacement), LF forces.
    Retourne (libelles_ecrits, libelles_sans_ligne) : un champ demande dont la
    ligne n'existe pas est SIGNALE, jamais devine ni ajoute en silence.
    """
    lignes = lire_lignes(chemin)
    if lignes is None:
        return [], sorted(valeurs)
    ecrits = set()
    resultat = []
    for ligne in lignes:
        if SEPARATEUR_TABLEAU in ligne:
            morceaux = ligne.split(SEPARATEUR_TABLEAU)
            if len(morceaux) >= COLONNES_MINIMUM:
                libelle = morceaux[COLONNE_LIBELLE].replace("*", "").strip()
                if libelle in valeurs and valeurs[libelle] != "":
                    morceaux[COLONNE_VALEUR] = " " + valeurs[libelle] + " "
                    morceaux[COLONNE_STATUT] = " Rempli "
                    ligne = SEPARATEUR_TABLEAU.join(morceaux)
                    ecrits.add(libelle)
        elif statut_fiche and ligne.strip().startswith("statut:"):
            ligne = "  statut: " + statut_fiche
        resultat.append(ligne)
    chemin_tmp = chemin.with_name(chemin.name + ".tmp")
    with open(chemin_tmp, "w", encoding="utf-8", newline="\n") as flux:
        flux.write("\n".join(resultat) + "\n")
    chemin_tmp.replace(chemin)
    return sorted(ecrits), sorted(set(valeurs) - ecrits)
