---
identite:
  type: analyse
  appartient_a: cameleon
  commun: false
---

# SUIVI DES MISSIONS DU CAMELEON -- la vue derivee

> Regeneree par la porte `suivi-cameleon` (MO-534). Jamais editee a la
> main : elle se RECALCULE. Les faits vivent dans
> `matrice/data/historiques-missions.jsonl` ; cette vue ne les recopie
> pas, elle les RASSEMBLE et elle DIT ce qu elle ne sait pas mesurer.

| Mesure | Valeur |
|---|---|
| Missions dans la trace (identifiants distincts) | 120 |
| dont terminees | 119 |
| dont creees sans fin | 1 |
| Durees mesurables | 110 |
| Durees NON mesurables | 67 |
| Periode couverte | 2026-09-06 -> 2026-10-03 |

Source : `matrice/data/historiques-missions.jsonl`.

## Ce que cette vue ne sait pas

- **67 mission(s) sans duree mesurable** : soit les
  bornes sont identiques (debut pose apres coup), soit une borne
  manque. Aucun de ces cas n est rendu 0 : un zero se lirait comme
  une mesure.
- **57 theme(s) nommes comme un TITRE** plutot
  qu un theme du vivier (`fichier`...). Une vue qui les normaliserait en silence
  cacherait la divergence ; elle les-marque donc a la volee.
- Aucune **note de BDD** ne porte ces missions : le journal des
  missions du cameleon est unHistorique de cloture, pas une trace
  d evenements. Rien n y dit les ports utilisees ni les fichiers
  touches -- cette information n existe pas encore, elle ne sera pas
  inventee ici.

## Missions

| Mission | Theme | Type | Duree | Objectif |
|---|---|---|---|---|
| M-089 | AUTO-EVOLUTION | mission-terminee | en cours | Corriger creer-outil.py pour generer des outils qui marchent du premie ...(+146) |
| M-091 | AUTO-EVOLUTION | mission-terminee | en cours | Creer outil porte unique pour lecons matrice (ajouter/lister/chercher) ...(+63) |
| M-092 | AUTO-EVOLUTION | mission-terminee | en cours | Etendre tester-theme.py : verifier que fichiers/dossiers pointes par r ...(+82) |
| M-093 | AUTO-EVOLUTION | mission-terminee | en cours | Instrumenter metriques proto (taux auto-valide/annule, recidives, temp ...(+132) |
| M-094 | AUTO-EVOLUTION | mission-terminee | en cours | Limiter le perimetre des scripts temporaires (modele v1 : tmp-<agent>/ ...(+406) |
| M-095 | MATRICE | mission-terminee | en cours | Modifier les instructions : tout message commencant par [mission] = AJ ...(+313) |
| M-096 | MATRICE | mission-terminee | en cours | Verifer et encoder : quand plusieurs missions sont en attente ET deja  ...(+370) |
| M-097 | MATRICE | mission-terminee | en cours | Etudier inter-round v1 (oracle mission-ajouter, pilote largue habilite ...(+265) |
| M-098 | AUTO-EVOLUTION | mission-terminee | en cours | Garde verifiant qu aucune ecriture ne sort de matrix/ (scan workspace  ...(+96) |
| M-099 | AUTO-EVOLUTION | mission-terminee | en cours | Controle ASCII strict automatise sur tout fichier matrice modifie. Pre ...(+51) |
| M-100 | AUTO-EVOLUTION | mission-terminee | en cours | Zero residu hors tmp-optimus/tmp-cameleon (convention M-094). Preuve : ...(+48) |
| M-101 | AUTO-EVOLUTION | mission-terminee | en cours | Automatiser reflexe L-016/C-006 : aucune mention Optimus/chemins inter ...(+98) |
| M-102 | AUTO-EVOLUTION | mission-terminee | en cours | Appliquer convention zero-valeurs-en-dur (secrets, chemins absolus, IP ...(+37) |
| M-103 | AUTO-EVOLUTION | mission-terminee | en cours | Graphe themes-protocoles-outils-BDD, cases mortes, dependances cassees ...(+53) |
| M-104 | AUTO-EVOLUTION | mission-terminee | en cours | Une commande rejouant tous les tests (themes, py_compile, integrite) a ...(+49) |
| M-105 | AUTO-EVOLUTION | mission-terminee | en cours | Tableau de bord : sante, file missions, stats auto-evolution. Preuve : ...(+32) |
| M-106 | AUTO-EVOLUTION | mission-terminee | en cours | Revert de toutes les modifs BDD-tracees d une periode (au-dela du fich ...(+63) |
| M-107 | AUTO-EVOLUTION | mission-terminee | en cours | Simuler une evolution (diff + impacts) sans ecrire. Preuve : dry-run d ...(+42) |
| M-108 | AUTO-EVOLUTION | mission-terminee | en cours | Mesurer tous les outils, optimiser les lents (garde-perimetre rglob 1. ...(+127) |
| M-109 | AUTO-EVOLUTION | mission-terminee | en cours | Mettre en place une suite de parcours (themes + mini-missions types) g ...(+234) |
| M-110 | AUTO-EVOLUTION | mission-terminee | en cours | Bapteme du feu : perimetre-write, ascii, tmp, invisibilite, valeurs-en ...(+120) |
| M-111 | MATRICE | mission-terminee | en cours | Creer matrice/espions-optimus/ : registre + espion integrite (empreint ...(+123) |
| M-112 | MATRICE | mission-terminee | en cours | Creer matrice/remorque-optimus/ : attelage contenant tous les equipeme ...(+116) |
| M-113 | MATRICE | mission-terminee | en cours | Deplacer matrice/espions-optimus -> _operateur/optimus-prime/espions e ...(+209) |
| M-114 | AUTO-EVOLUTION | mission-terminee | en cours | Etendre lanceur-non-regression : etape 5 compile+execute espions et re ...(+94) |
| M-115 | MATRICE | mission-terminee | en cours | Corriger demarrer-optimus-prime.md (3 frictions : porte bdd-lecons mor ...(+14) |
| M-116 | MATRICE | mission-terminee | en cours | Suite non-regression du FLUX (Matrice demarre ? pilote fonctionne ? fa ...(+9) |
| M-118 | MATRICE | mission-terminee | en cours | Tokens avant/apres dans sac-a-dos - imperatif 56 |
| M-119 | MATRICE | mission-terminee | en cours | Generateur de combos (pendant creer-outil) |
| M-120 | MATRICE | mission-terminee | en cours | Convention chemins/flags (problemes fondamentaux imperatif 24) |

_147 mission(s) plus anciennes non affichees (borne LIMITE_MISSIONS)._

## Themes par volume

| Theme | Missions |
|---|---|
| AUTO-EVOLUTION | 60 |
| MATRICE | 28 |
| CONTRATS | 7 |
| OUTIL | 7 |
| PILOTE | 5 |
| activer la veille-flux en boucle permane ...(+30) | 3 |
| ROUTINE | 2 |
| routine | 2 |
| ENTONNOIR | 2 |
| PERFORMANCES | 2 |
| reparer py_compile | 2 |
| fichier | 1 |

_56 theme(s) de faible volume non affiches._

## Anomalies

- `M-089` apparait plusieurs fois dans le journal.
- `M-090` apparait plusieurs fois dans le journal.
- `M-091` apparait plusieurs fois dans le journal.
- `M-092` apparait plusieurs fois dans le journal.
- `M-093` apparait plusieurs fois dans le journal.
- `M-094` apparait plusieurs fois dans le journal.
- `M-095` apparait plusieurs fois dans le journal.
- `M-096` apparait plusieurs fois dans le journal.
- `M-097` apparait plusieurs fois dans le journal.
- `M-098` apparait plusieurs fois dans le journal.
- `M-099` apparait plusieurs fois dans le journal.
- `M-100` apparait plusieurs fois dans le journal.
- `M-101` apparait plusieurs fois dans le journal.
- `M-102` apparait plusieurs fois dans le journal.
- `M-103` apparait plusieurs fois dans le journal.
- `M-104` apparait plusieurs fois dans le journal.
- `M-105` apparait plusieurs fois dans le journal.
- `M-106` apparait plusieurs fois dans le journal.
- `M-107` apparait plusieurs fois dans le journal.
- `M-108` apparait plusieurs fois dans le journal.
- `M-109` apparait plusieurs fois dans le journal.
- `M-110` apparait plusieurs fois dans le journal.
- `M-111` apparait plusieurs fois dans le journal.
- `M-112` apparait plusieurs fois dans le journal.
- `M-113` apparait plusieurs fois dans le journal.
- `M-114` apparait plusieurs fois dans le journal.
- `M-115` apparait plusieurs fois dans le journal.
- `M-116` apparait plusieurs fois dans le journal.
- `M-118` apparait plusieurs fois dans le journal.
- `M-119` apparait plusieurs fois dans le journal.
- `M-120` apparait plusieurs fois dans le journal.

