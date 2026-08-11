---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Verification de Coherence

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-10
**Agent** : Themis (evaluatrice croisee) -- generalisation des lecons du re-audit README

---

## Objectif

Definir la procedure de verification de coherence d'un fichier markdown a
compteurs/tables/badges (typiquement le README) apres une mise a jour, pour
garantir qu'il reflete l'etat reel du projet.

**Pourquoi ce protocole ?**
- L'audit Themis du 2026-08-10 a revele que les compteurs de la table peuvent
  etre a jour alors qu'un ancien total subsiste ailleurs dans le fichier
  (arborescence commentee : "83 outils" residuel apres la MAJ 119)
- Un tri automatique de table peut ECRASER l'en-tete et le separateur sans
  erreur de contenu -- la verification de STRUCTURE est indispensable
- Les badges shields.io sont tous sur une ligne unique : un grep par ligne les
  manque
- Certaines categories comptees sont VIRTUELLES (pas de dossier physique)

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Fichier modifie | README.md ou tout fichier markdown avec compteurs/tables/badges |
| 2 | Sources de verite disponibles | L'outil qui compte l'etat reel (mettre-a-jour-readme, combos-analyse-projet, ou comptage manuel) |
| 3 | Contexte de la MAJ | Savoir ce qui devait changer (totaux, categories, badges) |
| 4 | Outils de controle | valider-conformite-ascii, valider-liens, grep/regex |

---

## Etapes

```
SOURCES DE VERITE -> ANCIENS TOTAUX -> STRUCTURE -> BADGES -> CATEGORIES VIRTUELLES
        1                  2             3           4              5
-> NORMES -> VERDICT
    6           7
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Croiser les sources de verite | Lancer l'outil officiel (mettre-a-jour-readme --verifier, combos-analyse-projet) : 0 ecart attendu. Un total officiel = la reference, pas une estimation | mettre-a-jour-readme --verifier, combos-analyse-projet |
| E2 | Scanner les ANCIENS TOTAUX dans TOUT le fichier | Chercher TOUTES les anciennes versions connues du total (ex : 82, 83, 85, 108, 117) dans chaque ligne, Y COMPRIS l'arborescence commentee et les phrases libres -- pas seulement les compteurs de la table. Le --maj ne touche PAS l'arborescence | grep regex de toutes les versions connues |
| E3 | Verifier la STRUCTURE apres tout tri | En-tete de table presente ET separateur '|---|---|---|' situe JUSTE APRES l'en-tete (pas n'importe quel separateur du fichier : les tables multiples ont plusieurs separateurs). Verifier la structure (pas seulement le contenu) apres tout reordonnancement automatique | lecture structurelle, regex positionnelle |
| E4 | Verifier les BADGES | Compter les occurrences 'img.shields.io/badge/' dans chaque LIGNE (une ligne peut porter 6 badges) -- ne pas filtrer par ligne contenant 'badge'. Comparer chaque valeur au total officiel | grep -o 'img.shields.io/badge/' + parse des valeurs |
| E5 | Verifier les CATEGORIES VIRTUELLES | Certaines categories n'ont pas de dossier physique (ex : templates = outil-template.md a la racine tools/). Les ajouter au comptage manuel (118 dossiers + 1 virtuel = 119) | ls, comptage manuel |
| E6 | Verifier les NORMES | ASCII strict 0 non-ASCII + LF pur (0 CRLF) | valider-conformite-ascii |
| E7 | Verdict | VALIDE si 0 ecart sur E1-E6 ; sinon A REVOIR avec liste exacte des lignes concernees | - |

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| [R]echercher | Rassembler le fichier, les sources de verite, les anciennes versions connues des totaux, la structure attendue des tables |
| [V]erifier | Appliquer E1 a E6 : checklist complete (compteurs, anciens totaux, structure, badges, categories virtuelles, normes) |
| [A]nalyser | Distinguer les VRAIS ecarts des faux positifs (artefact __pycache__, separateur d'une AUTRE table, badge sur une ligne multi-badges) |
| [V]alider | Verdict VALIDE / A REVOIR et rapport avec preuves chiffrees |

> **REGLE ABSOLUE** : Ne jamais valider sur la seule base des compteurs de la
> table. La coherence = compteurs ET structure ET absence d'anciens totaux dans
> TOUT le fichier.

---

## Exemples

### Exemple 1 : ancien total dans l'arborescence

```
MAJ du README : table a 119, titre a 119, badge Outils-119
Verification :
  E1 : mettre-a-jour-readme --verifier -> TOTAL 119, 0 ecart
  E2 : grep '83' -> ligne 54 de l'arborescence : "Boite a outils (83 outils)"
       -> A REVOIR : le --maj ne touche pas l'arborescence commentee
  E7 : verdict A REVOIR (1 ecart reel : total 83 residuel ligne 54)
```

### Exemple 2 : en-tete ecrase par un tri

```
Tri alphabetique automatique de la table (32 lignes) :
  E3 : l'en-tete '| Categorie | Outils | Usage |' a ete remplace par la
       premiere ligne de donnees -> structure cassee SANS erreur de contenu
  Parade : verifier en-tete + separateur positionnels apres tout tri
  E7 : verdict A REVOIR, restauration de l'en-tete, re-verification
```

---

## Pieges courants

| Piege | Consequence | Parade |
|---|---|---|
| **Separateurs multiples** | Le premier '|---|---|---|' du fichier appartient a une AUTRE table (piliers, agents) | Localiser l'en-tete '| Categorie |' PUIS le separateur juste apres |
| **Ancien total dans l'arborescence** | Table/titre/badge a jour mais ligne commentee avec l'ancien total | Scanner les anciennes versions connues dans TOUT le fichier, pas seulement la table |
| **Badges sur une ligne unique** | Un grep par ligne ne voit qu'une seule occurrence alors que la ligne en porte 6 | Compter 'img.shields.io/badge/' dans la ligne, parser chaque valeur |
| **Categories virtuelles** | Comptage manuel inferieur d'1 (118 vs 119) car un dossier physique manque | Connaitre les categories virtuelles (templates = outil-template.md racine) |
| **Tri qui ecrase l'en-tete** | Reordonnancement sans erreur de contenu mais structure cassee | Verifier en-tete + separateur positionnels (E3) apres tout tri |
| **Artefact __pycache__** | Faux ecart "compteur introuvable (reel = 0)" | Ignorer par convention (artefact Python) |

---

## Liens

| Reference | Usage |
|---|---|
| [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md) | Structure des protocoles (en-tete + 7 sections) |
| [rvav-workflow](../rvav-workflow.md) | Boucle obligatoire avant verdict |
| [regles-veracite](../regles-veracite.md) | Ne jamais mentir ou inventer |
| [regles-emojis-ascii](../regles-emojis-ascii.md) | ASCII strict |
| [mettre-a-jour-readme](../../../tools/mettre-a-jour/mettre-a-jour-readme/) | Source de verite des compteurs du README |
| [combos-analyse-projet](../../../tools/combos/combos-analyse-projet/) | Source de verite croisee (ecarts README vs realite) |
| [rapport-audit-coherence-readme](../../../themis/rapports/rapport-audit-coherence-readme-2026-08-10.md) | Cas reel ayant genere ce protocole |
