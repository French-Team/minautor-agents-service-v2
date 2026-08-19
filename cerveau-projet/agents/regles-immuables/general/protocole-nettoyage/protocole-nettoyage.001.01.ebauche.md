---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Nettoyage du Workspace

**Version** : 0.1.0
**Statut** : ebauche
**Categorie** : General
**Agent** : Hygie
**Date** : 2026-08-14

Cadre le **cycle de nettoyage** du workspace : snapshot -> detection ->
verdict -> suppression. Hygie est le SEUL agent habilite a supprimer sans
demande prealable, mais uniquement des RESIDUS PROUVES. L outil de detection
est `detecter-residus` (compartimente par zone : `cerveau-projet/` /
`workspace/`).

---

## Objectif

Mettre en oeuvre la demande utilisateur : un agent de nettoyage de bout en
bout qui scrute le projet avec les combos en place, en **compartimentant les
dossiers** (`cerveau-projet/` et `workspace/` futurs), prend un **snapshot**
a chaque nettoyage (consulte au nettoyage suivant), supprime avec
tracabilite, et demande des preuves d honnetete quand un changement ou un
fichier present est suspect (via la delegation d un agent habilite).

**Pourquoi ce protocole ?**
- Avant, la suppression etait possible par tout agent sans cadre : des
  residus (scripts `.tmp-*`, rapports egare, fichiers de version) trainaient
  a la racine.
- La regle "SEUL Hygie supprime" etait documentee dans SA fiche et mecanisee
  par le test-045 (cartes + registre), mais AUCUN protocole global ne
  documentait la CHAINE COMPLETE du nettoyage (snapshot -> detection ->
  verdict -> suppression -> rapport).
- `protocole-purification` ne couvre PAS les residus du workspace : il
  concerne la purification des CONTENUS des fichiers apres validation.

## Prerequis

1. L agent est Hygie (seul habilite a supprimer sans demande prealable).
2. L outil `detecter-residus` existe (compartimentation par zone, option
   `--zone cerveau-projet|workspace|tous`).
3. L outil `snapshot-nettoyage` existe (snapshot de l etat avant nettoyage,
   rotation 7 jours).
4. Le combo `combo-nettoyage-hygie` enchaene la boucle (snapshot ->
   detection -> verdict -> suppression -> rapport).
5. Les garde-fous sont en place : test-045 (seul Hygie supprime - cartes +
   registre), test-046 (compartimentation etanche), test-024 (0 script
   eparpille a la racine).

## La chaine de nettoyage (cycle complet)

| Etape | Action | Outil | Verdict |
|---|---|---|---|
| 1. **SNAPSHOT** | Capturer l etat du workspace AVANT toute action | `snapshot-nettoyage` | Snapshot cree (preuve de tracabilite) |
| 2. **DETECTER** | Scanner les residus par zone (cerveau-projet / workspace) | `detecter-residus --zone <zone> --detail` | Liste des residus classes par zone |
| 3. **VERDICT** | La detection a-t-elle trouve des residus ? | `combo-nettoyage-hygie` (case c5) | OUI -> supprimer / NON -> fin propre |
| 4. **PROUVER** | Si doute sur l honnetete d un changement/fichier | Delegation Pattern 5 (janus ou agent proprietaire) | Preuve obtenue |
| 5. **SUPPRIMER** | Supprimer les RESIDUS PROUVES uniquement | `supprimer-fichier` / `supprimer-dossier` | 0 fichier de travail legitime touche |
| 6. **VERIFIER** | Re-lancer la detection : 0 residu restant ? | `detecter-residus --tous` | PROPRE / residus restants |
| 7. **RAPPORT** | Documenter le nettoyage + rotation des snapshots | Rapport + `snapshot-nettoyage` | Rapport ecrit, snapshots > 7 jours supprimes |

## Regles immuables

1. **SNAPSHOT AVANT SUPPRESSION** : jamais de suppression sans snapshot de
   l etat du workspace. Chaque nettoyage CONSULTE le snapshot precedent.
2. **SEUL HYGIE SUPPRIME** : aucun autre agent n a `supprimer-fichier` /
   `supprimer-dossier` dans SA carte (test-045 8b) ni dans ses declarations
   au registre (test-045 8c).
3. **RESIDUS PROUVES UNIQUEMENT** : fichiers temporaires (`tmp-*`, `.zz-*`,
   `.tmp-*`), rapports egare hors des dossiers de rapport, fichiers de
   version a la racine, dossiers residuels. JAMAIS un fichier de travail
   legitime (fiche, parcours, outil, protocole, regle, source) sans preuve
   d honnetete (snapshot + avis).
4. **COMPARTIMENTATION** : les zones `cerveau-projet/` et `workspace/` sont
   scannees separement ; les residus sont classes par zone (test-046).
5. **DETECTION PARTAGEE, SUPPRESSION EXCLUSIVE** : `detecter-residus` peut
   etre utilise par d autres agents en CONTROLE (ex: Janus c21 "Verifier les
   impacts" - il DETECTE sans supprimer). L exclusivite porte sur la
   SUPPRESSION, jamais sur la detection.
6. **NIVEAU REGLE IMMUABLE** : la regle "SEUL HYGIE SUPPRIME" est documentee
   au niveau REGLE IMMUABLE dans
   [regles-groupes-agents.md](../regles-groupes-agents.md) (section "Regles de
   gouvernance exclusives"), en plus de la fiche Hygie (comportement) et de
   ce protocole (processus). Les trois niveaux sont synchronises et
   verifies par le test-045 (point 8e : regle immuable documentee).

## Etapes

1. **SNAPSHOT** : `snapshot-nettoyage` avant toute action.
2. **DETECTER** : `detecter-residus --zone cerveau-projet --detail` puis
   `--zone workspace` (ou `--zone tous`).
3. **VERDICT** : lire la liste des residus classes par zone ; s il n y en a
   aucun -> fin propre (rapport PROPRE).
4. **PROUVER** : si un fichier suspect est un fichier de travail legitime ou
   si un changement parait douteux, activer via MA carte l agent habilite
   (janus pour un controle, l agent proprietaire du fichier pour une
   verification). Ne JAMAIS supprimer sans preuve.
5. **SUPPRIMER** : supprimer les residus PROUVES avec `supprimer-fichier` /
   `supprimer-dossier` (tracabilite : chaque suppression est listee).
6. **VERIFIER** : re-lancer `detecter-residus --tous` : 0 residu = PROPRE.
7. **RAPPORT** : documenter le nettoyage (snapshot + liste supprimee +
   verdict) ; rotation des snapshots (plus de 7 jours supprimes).

## RVAV

- Un snapshot existe AVANT la premiere suppression du nettoyage.
- `detecter-residus --tous` apres nettoyage retourne 0 residu (PROPRE).
- Aucun fichier de travail legitime supprime (preuve d honnetete si doute).
- test-045 (seul Hygie supprime) et test-046 (compartimentation) verts.
- Rapport de nettoyage ecrit + rotation des snapshots effectuee.

## Exemples

**Exemple 1 - nettoyage simple (valide)** :
```
1. snapshot-nettoyage -> snapshot-2026-08-14-0900.json
2. detecter-residus --zone tous --detail
3. Verdict : 2 rapports egare a la racine + 3 fichiers .tmp-*
4. Suppression (residus PROUVES) : supprimer-fichier x5
5. detecter-residus --tous -> 0 residu -> PROPRE
6. Rapport + rotation snapshots
```

**Exemple 2 - doute d honnetete (valide)** :
```
1. snapshot + detection -> 1 fichier "version.txt" a la racine suspect
2. Ce fichier pourrait etre un fichier de version legitime -> preuve requise
3. Delegation Pattern 5 : activer janus (controle) OU clio (proprietaire
   de version-readme.txt) pour prouver l honnetete
4. Preuve obtenue -> supprimer ou conserver selon la preuve
```

**Exemple 3 - interdiction (invalide)** :
```
Supprimer un parcours.json ou une fiche agent sans snapshot ni preuve ->
violation (residu NON prouve). Supprimer sans snapshot -> violation.
```

## Pieges

1. **Sur-nettoyage** : supprimer un fichier de travail legitime sans preuve
   d honnetete (regle 3). Toujours demander la preuve en cas de doute.
2. **Suppression sans snapshot** : la tracabilite disparait. Toujours
   snapshot AVANT.
3. **Zone confondue** : un residu de `cerveau-projet/` classe dans
   `workspace/` ou l inverse (test-046). Toujours `--zone` explicite.
4. **Confusion detection/suppression** : un agent (ex: Janus) peut DETECTER
   avec `detecter-residus` en controle, mais seul Hygie SUPPRIME.
5. **Snapshot precedent ignore** : chaque nettoyage doit consulter le
   snapshot precedent (rotation 7 jours) avant d agir.

## Liens

- [detecter-residus](../../../tools/detecter/detecter-residus/detecter-residus.md)
- [combo-nettoyage-hygie](../../../tools/combos/combo-nettoyage-hygie/combo-nettoyage-hygie.md)
- [fiche Hygie](../../../../agents/hygie/hygie.md)
- [regles-groupes-agents](../regles-groupes-agents.md) (regle immuable "SEUL HYGIE SUPPRIME" - niveau reference pour tous)
- [protocole-purification](../protocole-purification/protocole-purification.001.01.ebauche.md)
- [regles-perimetre-workspace](../regles-perimetre-workspace.md)
- [test-045-hygie-garde-fou](../../../tools/tester/tests/test-045-hygie-garde-fou/test-045-hygie-garde-fou.py)
- [test-046-hermes-fautes](../../../tools/tester/tests/test-046-hermes-fautes/test-046-hermes-fautes.py)
- [index-regles-general](../index-regles-general.md)
