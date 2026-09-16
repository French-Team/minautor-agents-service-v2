---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
  mission: MO-098
  statut: constat
---

# MO-098 -- REVUE DES SEUILS DU COCKPIT

> Demande du createur (2026-09-15) : "lesquels sont encore en dur chez
> l'observateur plutot que declares par l'objet mesure ?"
> CONSTAT SEUL a l'origine (MO-098) : la revue ne modifiait rien, les
> propositions attendaient une decision.
>
> MISE A JOUR : le createur a tranche. **P4** a ete applique en MO-099, **P1 et
> P2** en MO-100, puis **P3** en MO-101 (lot REVUE-MO-098, round 1/3) -- voir
> les lignes marquees FAIT dans le tableau du point 5 et dans l'inventaire du
> point 3. Un constat qui ignore ce qui a ete applique devient un constat qui
> ment : les lignes concernees portent donc leur statut. **P6 reste
> ouverts** (lot REVUE-MO-098, rounds 2/3 et 3/3).

## 1. Methode (aucun verdict sans preuve)

Pour chaque valeur numerique utilisee dans une COMPARAISON, j'ai lu sur disque :
qui l'ecrit, qui la lit, et quelle valeur a ete MESUREE en face. Les mesures
datent du 2026-09-15 (sequentielle, machine de l'operateur).

## 2. Les trois classements (le critere de la revue)

| Verdict | Sens | Action |
|---|---|---|
| **A. DECLARE PAR L'OBJET** | la valeur appartient a l'objet mesure, il la declare et la publie, l'observateur lit | rien a faire -- c'est le motif de reference |
| **B. ECRIT CHEZ L'OBSERVATEUR** | l'observateur compare a un nombre qui ne lui appartient pas | a migrer vers l'objet (declarer + publier + lire) |
| **C. POLITIQUE LEGITIME** | le nombre est un choix du createur (affichage, fenetre, budget), pas une propriete de l'objet | garder, mais le NOMMER comme politique pour qu'il ne passe pas pour une mesure |
| **D. VALEUR MORTE** | personne ne la lit | supprimer, ou la brancher si son intention etait reelle |

## 3. Inventaire (constat, preuve par ligne)

| # | Seuil | Valeur | Domicile | Mesure en face | Verdict |
|---|---|---|---|---|---|
| 1 | budget de passe veille-flux | 2000 ms | **routine** (constants.py) -> publie dans `veille-cadence.json` -> lu par le cockpit | 1138 ms (1739 avant MO-097) | **A** -- motif de reference depuis MO-097 |
| 2 | cadence des routines | 300 / 900 s | **routine** (`INTERVALLE_DECLARE_SECONDES`), lu par `vie etat` et par `verifier-cadence` | battement median reel | **A** |
| 3 | echelle defcon | 1..5 | **machine-defcon** (porte + classeur V-002) | etat courant | **A** |
| 4 | perimetre cameleon | liste V-003 | **classeur-variables** | lecture cameleon | **A** |
| 5 | duree du bilan-periode | 500 ms | cockpit AVANT MO-100 ; desormais **outil** (`bilan-periode/constants.py:BUDGET_PASSE_MS`) -> publie dans sa sortie -> lu par le cockpit | **114 ms** mesures | **A depuis MO-100** -- **P2 APPLIQUE** (l'outil declare, publie, le cockpit lit, et dit BUDGET NON PUBLIE s'il manque) |
| 6 | volume du journal usages | cockpit AVANT MO-101 ; desormais **proprietaire du journal** (`bdd-usages/constants.py: SEUIL_OCTETS_JOURNAL` 16 Mo + `EVENEMENTS_GARDES_JOURNAL` 40000) -> publie par `bdd-usages lire` -> lu par le cockpit | 1259 lignes / 245 Ko le 15/09 (+240 Ko/jour) ; le plus long lecteur (`bilan-periode --periode mois`) reclame 30 jours (~7,2 Mo) | **A depuis MO-101** -- **P3 APPLIQUE** : borne DEDUITE du plus long lecteur, rotation LIEE a la valeur declaree (moteur partage), `SEUILS_PERFS` ne contient plus rien |
| 7 | duree de compilation | 400 ms | s'upprimee | non mesure : **aucun lecteur** | **D** -- **P1 APPLIQUE en MO-100** : la valeur morte est SUPPRIMEE (la brancher telle quelle aurait fait crier a tort, la compilation reelle etant a 1406 puis 794 ms) |
| 8 | fenetre de queue lue | 256 Ko | **11 fichiers** (`OCTETS_QUEUE*`) : 4 routines + journal-multi-encarts + 4 verifiers + lanceur de flux | chaque routine declare SA borne (`SEUIL_OCTETS_JOURNAL` : 2 Mo / 8 Mo / 512 Ko) | **B + duplication** -- **P4 APPLIQUE en MO-099** : regle unique dans le moteur partage, fenetre deduite de la borne declaree du journal lu ; 5 des 11 copies etaient MORTES (aucun lecteur) |
| 9 | delai d'un sous-processus | 120 s | **5 fichiers** (`TIMEOUT_SECONDES` / `TIMEOUT_COMBO_SECONDES`) | -- | **C duplique** |
| 10 | passes absorbees (observations) | 3 | observateur | 0 sur le service au redemarrage | **A depuis MO-097** (recul insuffisant) ; les seuils 3/5 restants sont des PARAMETRES D'EPREUVE (cobayes), donc legitimes |
| 11 | affichage du cockpit (10 resultats, 800 lignes, 5 entrees, 20 s, 2000 caracteres) | -- | cockpit | -- | **C** -- politique d'affichage, deja locale au cockpit |

## 4. Ce que la revue a trouve de plus grave : deux valeurs qui mentent

### 4.1 Une valeur MORTE qui rassurait (`py_compile_ms: 400`) -- **corrigee en MO-100**

> STATUT : supprimee du cockpit en MO-100 (P1). `grep py_compile_ms` ne rend
> plus aucune declaration vivante -- seulement les traces de cette revue et des
> BDD. Le diagnostic ci-dessous est conserve tel quel : il documente POURQUOI la
> brancher n'etait pas la bonne reponse.

Le cockpit declare un seuil de compilation a 400 ms et **aucun code ne le lit**
(`grep py_compile_ms` ne rend que sa declaration, ligne 222 de
`cockpit-matrice.py`). Qui lit ce fichier croit que la compilation est surveillee
a 400 ms : elle ne l'est pas. C'est la classe de faute de L-039 (un fichier que
sa porte ne trouve pas est un fichier mort), appliquee a une valeur.
Voir aussi MO-097 : la compilation REELLE de la veille a ete mesuree a 1406 ms
puis 794 ms -- brancher ce seuil tel quel ferait crier le cockpit a tort.

### 4.2 Une politique sans domicile (le volume du journal usages)
`usages_lignes: 50000` est compare au nombre de lignes de
`usages-outils-combos.jsonl`. Or AUCUN document de la Matrice ne declare la
capacite de ce journal : ni `bdd-usages/constants.py`, ni le plan de
conservation (MO-094), ni la BDD conservation n'en portent la valeur.
Deux politiques coexistent donc sans se connaitre : celle du cockpit (50000) et
celle de la rotation reellement executee le 15/09 (69519 lignes archivees,
500 gardees). Un seuil qui ne connait pas la rotation qui le precede ne mesure
rien.

### 4.3 Un motif copie onze fois (la fenetre de queue)
`256 * 1024` apparait dans **onze** fichiers sous des noms voisins
(`OCTETS_QUEUE`, `OCTETS_QUEUE_JOURNAL`). Les routines, elles, declarent chacune
LEUR borne de rotation (2 Mo pour la veille, 8 Mo pour l'espion, 512 Ko pour les
vigies) : la fenetre lue par les verifiers n'est reliee a aucune de ces bornes
declarees. C'est le motif L-029 (un moteur recopie diverge), ici applique a une
valeur : onze copies, onze derivees possibles, aucune source de verite.

## 5. Propositions (par cout croissant, aucune n'est engagee)

| # | Proposition | Cout | Risque |
|---|---|---|---|
| P1 | **FAIT en MO-100** : la valeur morte `py_compile_ms` est SUPPRIMEE du cockpit (le brancher tel quel aurait fait crier a tort : compilation reelle 1406 puis 794 ms) | -- | -- |
| P2 | **FAIT en MO-100** : budget declare chez l'outil (`BUDGET_PASSE_MS`), PUBLIE dans sa sortie ("Budget declare de l'outil : <n> ms"), LU par le cockpit ; publication absente => le cockpit DIT `BUDGET NON PUBLIE par l'outil` (aucun repli muet). Cobaye 6/6 (3 pieges) | -- | -- |
| P3 | **FAIT en MO-101** : capacite domiciliee chez le PROPRIETAIRE du journal (`bdd-usages`) -- et non chez `bdd-conservation`, qui n'est qu'un registre de classement (verifie : K-001 unique, aucune capacite) -- et DEDUITE du plus long lecteur (30 jours) ; rotation LIEE (verifiee a chaque ecriture depassee, moteur partage) ; publiee par `bdd-usages lire` et lue par le cockpit. Cobaye 7/7 (dont 4 pieges) | -- | -- |
| P4 | **FAIT en MO-099** : la fenetre est portee par le moteur partage (`rotation_journal.py`) et DEDUITE de la borne declaree du journal lu ; les 5 copies sans lecteur sont retirees ; la fenetre du verifier de rotation est renommee PARAMETRE D'EPREUVE | -- | -- |
| P5 | Un seul delai de sous-processus declare, par politique partagee | 5 fichiers | faible | **FAIT (MO-102)** : domicile unique = `matrice/data/commun/lancement.py` (`DELAI_SOUS_PROCESSUS_SECONDES = 120` + `delai_sous_processus()`). Les SIX copies sont parties : 3 constantes d'observateurs (`verifier-anti-spam-missions`, `verifier-exemptions-visibles`, `verifier-passes-non-redondantes`), 2 delais EN DUR (`verifier-rotation-journal`, `verifier-sans-attendre`) et la constante de la routine (`veille-flux/constants.py`). Preuve : les 5 observateurs rendent VERDICT OK en lisant la valeur a la source ; `grep` des delais recopies = vide. Note : `executer` garde SON `TIMEOUT_DEFAUT` -- c'est son objet, deja declare chez lui.
| P6 | Nommer explicitement les seuils de POLITIQUE du cockpit (affichage, fenetre, delai) pour qu'ils ne soient jamais pris pour des mesures | commentaires | nul |

## 6. Point de vigilance avant toute migration

Migrer un seuil ne suffit pas : il faut aussi REGARDER la valeur mesuree. Trois
lignes du tableau n'ont JAMAIS ete confrontees au reel : la 5 (500 ms contre
114 ms mesures), la 6 (50000 contre une politique de rotation qui n'existe sur
aucun disque) et la 7 (400 ms, aucune mesure, aucun lecteur). Le
motif de MO-097 est le seul complet : **declarer** chez l'objet, **publier** dans
son etat court, **lire** chez l'observateur, et **crier si la publication
manque** -- jamais de repli muet.

---

> Revue deposee par Optimus Prime (MO-098, Flux 2). Lecon liee : L-085.
