---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Verification de Coherence

**Version** : 0.2.0
**Statut** : Ebauche
**Date creation** : 2026-08-10
**Agent** : Themis (evaluatrice croisee) -- generalisation des lecons du re-audit README

> **REGLE IMMUABLE (synchronisation 2026-08-16)** : **CLIO est le SEUL agent
> habilite a METTRE A JOUR le README** (regle immuable regles-groupes-agents.md,
> section SEUL CLIO MET A JOUR LE README). Ce protocole documente la
> VERIFICATION de coherence du README (apres une mise a jour) - il ne donne
> PAS le droit de mise a jour : seul Clio edite le README, Themis le
> verifie, Janus le controle croise.
>
> **Garde-fou** : [test-020-combos-clio](../../../tools/tester/tests/test-020-combos-clio/test-020-combos-clio.py) (carte Clio) + verrou `proteger-verrou-habilitation`.
**Historique** : v0.2.0 (ajout E8 : verification automatique de coherence des SEUILS BUDGET PONDERE entre specs et outils -- grep croise des 5 valeurs 100/0,5/1/3,0/160 sur 6 fichiers, lecon des audits de coherence budget pondere du 2026-08-11) -> v0.1.0 (creation, 2026-08-10)

---

## Objectif

Definir la procedure de verification de coherence d'un fichier markdown a
compteurs/tables/badges (typiquement le README) apres une mise a jour, pour
garantir qu'il reflete l'etat reel du projet.

**Perimetre etendu (v0.2.0)** : la meme exigence de coherence s'applique aux
SEUILS du BUDGET PONDERE des indices de cases (100 / 0,5 / 1 / 3,0 / 160) :
les specs, le .md d'outil et les codes (valider-case, generateurs-case)
doivent tous porter les MEMES valeurs (E8). Une divergence de seuil entre deux
fichiers = incoherence a corriger, meme si chaque fichier est coherent en
interne.

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
| 5 | Fichiers BUDGET PONDERE (6) | spec-refonte-cartes-decision, spec-valider-case, spec-guider-parcours, valider-case.md, valider-case.py, generateurs-case.py |

---

## Etapes

```
SOURCES DE VERITE -> ANCIENS TOTAUX -> STRUCTURE -> BADGES -> CATEGORIES VIRTUELLES
        1                  2             3           4              5
-> BUDGET PONDERE -> NORMES -> VERDICT
        6               7          8
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Croiser les sources de verite | Lancer l'outil officiel (mettre-a-jour-readme --verifier, combos-analyse-projet) : 0 ecart attendu. Un total officiel = la reference, pas une estimation | mettre-a-jour-readme --verifier, combos-analyse-projet |
| E2 | Scanner les ANCIENS TOTAUX dans TOUT le fichier | Chercher TOUTES les anciennes versions connues du total (ex : 82, 83, 85, 108, 117) dans chaque ligne, Y COMPRIS l'arborescence commentee et les phrases libres -- pas seulement les compteurs de la table. Le --maj ne touche PAS l'arborescence | grep regex de toutes les versions connues |
| E3 | Verifier la STRUCTURE apres tout tri | En-tete de table presente ET separateur '|---|---|---|' situe JUSTE APRES l'en-tete (pas n'importe quel separateur du fichier : les tables multiples ont plusieurs separateurs). Verifier la structure (pas seulement le contenu) apres tout reordonnancement automatique | lecture structurelle, regex positionnelle |
| E4 | Verifier les BADGES | Compter les occurrences 'img.shields.io/badge/' dans chaque LIGNE (une ligne peut porter 6 badges) -- ne pas filtrer par ligne contenant 'badge'. Comparer chaque valeur au total officiel | grep -o 'img.shields.io/badge/' + parse des valeurs |
| E5 | Verifier les CATEGORIES VIRTUELLES | Certaines categories n'ont pas de dossier physique (ex : templates = outil-template.md a la racine tools/). Les ajouter au comptage manuel (118 dossiers + 1 virtuel = 119) | ls, comptage manuel |
| E6 | Verifier les NORMES | ASCII strict 0 non-ASCII + LF pur (0 CRLF) | valider-conformite-ascii |
| E7 | Croiser les SEUILS BUDGET PONDERE (grep croise) | Les 5 valeurs (100 car / 0,5 / 1 / 3,0 / 160) doivent etre IDENTIQUES dans les 6 fichiers. Fichiers TEXTES (3 specs + valider-case.md) : grep des valeurs dans chaque fichier. Codes : grep des constantes -- valider-case.py doit porter `SEUIL_COURT = 100`, `BUDGET_INDICES = 3.0`, `SEUIL_TEXTE = 160` ; generateurs-case.py `SEUIL_COURT = 100`, `BUDGET_INDICES = 3.0`, `SEUIL_REGLE_DEFAUT = 160`. Anti-recurrence : l'ancienne regle `> 3 indices` doit etre ABSENTE des 6 fichiers | grep croise des 5 valeurs sur les 6 fichiers |
| E8 | Verdict | VALIDE si 0 ecart sur E1-E7 ; sinon A REVOIR avec liste exacte des fichiers/lignes concernes | - |

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| [R]echercher | Rassembler le fichier, les sources de verite, les anciennes versions connues des totaux, la structure attendue des tables, les 6 fichiers du budget pondere |
| [V]erifier | Appliquer E1 a E7 : checklist complete (compteurs, anciens totaux, structure, badges, categories virtuelles, budget pondere, normes) |
| [A]nalyser | Distinguer les VRAIS ecarts des faux positifs (artefact __pycache__, separateur d'une AUTRE table, badge sur une ligne multi-badges) |
| [V]alider | Verdict VALIDE / A REVOIR et rapport avec preuves chiffrees |

> **REGLE ABSOLUE** : Ne jamais valider sur la seule base des compteurs de la
> table. La coherence = compteurs ET structure ET absence d'anciens totaux dans
> TOUT le fichier. Pour le budget pondere, un fichier coherent en interne mais
> porteur d'un seuil different des autres = incoherence (E7).

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

### Exemple 3 : seuil budget pondere divergent

```
Verification de coherence budget pondere (6 fichiers) :
  E7 : grep croise 100/0,5/1/3,0/160
       - spec-refonte, spec-valider-case, spec-guider-parcours : 5/5 valeurs OK
       - valider-case.md : ligne Allegement -> '> 3 indices OU texte > 160'
         (ancienne regle) -> 0,5 et 3,0 ABSENTS -> A REVOIR
  Parade : corriger le .md avec les valeurs de la spec de reference (v0.1.3),
           puis re-grep croise -> 5/5 OK partout
  E8 : verdict A REVOIR tant qu'un fichier porte un seuil divergent
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
| **Seuil divergent entre .md et spec** | Le .md d'un outil porte l'ancienne regle (ex : > 3 indices) alors que sa spec est a jour | Croiser systematiquement les 6 fichiers du budget pondere (E7), pas seulement spec + code |
| **Virgule vs point decimal** | Les fichiers textes ecrivent 0,5 et 3,0 (virgule) ; les codes Python ecrivent 0.5 et 3.0 (point) | Ne pas comparer brute : comparer la VALEUR (5 seuils) dans chaque registre, pas la graphie |
| **Valeur a plusieurs usages** | 100 = seuil COURT mais aussi 100% ASCII ; 1 = poids LONG mais aussi numero d'agent | Cibler les occurrences CONTEXTUELLES (accompagnees de car./unite/budget), pas le chiffre nu |

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
| [spec-refonte-cartes-decision](../../../../docs-dev-cerveau-projet/spec-refonte-cartes-decision.001.01.ebauche.md) | Reference des seuils budget pondere (v0.1.3) |
| [spec-valider-case](../../../tools/valider/valider-case/spec/spec-valider-case.001.01.ebauche.md) + [valider-case.md](../../../tools/valider/valider-case/valider-case.md) | Spec + doc d'outil a croiser (E7) |
| [spec-guider-parcours](../../../tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md) | Spec Pattern 16 ALLEGEMENT a croiser (E7) |
| [valider-case.py](../../../tools/valider/valider-case/valider-case.py) + [generateurs-case.py](../../../tools/generateurs/generateurs-case/generateurs-case.py) | Constantes code du budget pondere (SEUIL_COURT / BUDGET_INDICES / SEUIL_TEXTE) |
