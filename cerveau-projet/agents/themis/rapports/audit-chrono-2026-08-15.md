# Audit Themis -- Chrono generalise + non-activation de Themis

Date : 2026-08-15

## 1. AUDIT DU TRIPLET CHRONO (point_actif / chrono_etape / bilan_chrono)

### 1.1 Tests (56 au total)
- Avec le triplet : 12 / 56 (21%)
- SANS le triplet : 44 / 56 (79%)
- Liste des tests SANS triplet (tous sauf test-029/044/050/056 et les
  re-verifies) : test-001 a 028, 030 a 043, 045, 046, 047+ (tous les garde-fous
  recents sauf ceux qui l ont deja).
- Verdict : le triplet n est PAS generalise. Le template v0.3.0 l impose aux
  NOUVEAUX tests (test-044 le verifie) mais les tests EXISTANTS n ont jamais
  ete migres (decision connue : on ne migre pas l existant).

### 1.2 Outils (.py : 119, .sh : 110)
- .py avec triplet : 1 / 119. .sh avec triplet : 1 / 110.
- Verdict : le triplet est quasi ABSENT des outils. Seuls quelques outils
  recents (generateurs) l ont.

### 1.3 Scripts temporaires
- Le protocole creation-scripts-temporaires impose le triplet. Les scripts
  recents (tmp-*/) suivent le modele (bilan chrono en fin). A verifier par
  echantillon dans la mission Vulcain.

### 1.4 Recommandation
- Ne PAS migrer les 44 tests existants (decision deja actee : le template
  v0.3.0 impose le triplet aux nouveaux tests uniquement).
- Pour les OUTILS : c est le vrai trou - les outils critiques (editer, creer,
  supprimer, valider, detecter) n ont pas de chrono. Recommande : ajouter le
  triplet chrono aux OUTILS CRITIQUES les plus utilises (priorite : ceux de la
  chaine de fin de mission et du lanceur), pas aux 119 d un coup.

## 2. DIAGNOSTIC : pourquoi Themis ne s active plus

### 2.1 Faits
- Derniere activation Themis : 2026-08-14 (hier).
- La fiche themis.md dit : "Activee automatiquement en fin de mission par les
  agents (axe D) : plus besoin de Cerberus".
- MAIS : les fins principales des 13 cartes vont TOUTES directement a Janus
  (FIN - Activer Janus) - aucune ne passe par Themis.
- Les cases "Activer Themis pour auditer" existent (buffy c22a/c27a/c8a/c40,
  morpheus c10a/c14a/c18, atlas c32/c11a, clio c12a/c17, janus c31, cerberus
  c22, athena c22, minerve c22, promethee c23) mais ce sont des ACTIONS
  OPTIONNELLES, pas des fins systematiques.

### 2.2 Cause racine
L axe D (declencheur automatique Themis avant Janus en fin de mission) est
documente dans la FICHE mais n a JAMAIS ete branche dans les CARTES. Les fins
de mission passent toutes par Janus directement -> Themis est hors de la route
-> elle n est jamais declenchee.

### 2.3 Proposition (a valider par Cerberus)
- Option A : inserer Themis dans la route de fin de mission : les fins
  principales passent par Themis (audit) PUIS Janus. C est le "second controle
  Themis avant Janus" deja documente pour certaines cartes (athena c23 "Retour
  de Themis", atlas c33...).
- Option B : Themis reste sur demande (Cerberus active) - c est l etat actuel
  effectif, mais en contradiction avec la fiche.
- RECOMMANDE : Option A (coherence fiche/cartes) - a traiter par Vulcain
  (modification des fins de cartes) en mission dediee.

## 3. RECLASSEMENT DES SERIES (constat pour Vulcain)
- Ordre actuel : a,b,c,d,e (fixe).
- KO recents (registre-tests) : e (3/106), c (2/9), d (0/1), tous (0/6).
- Demande utilisateur : les series avec le plus de KO passent en premier.
- Le registre-tests journalise chaque test (serie, verdict) -> source de
  donnees pour un classement dynamique par taux de KO.
