# PROTOCOLE 17 -- Modifier les outils de securite

> Ce protocole s'applique QUAND Mecano modifie un fichier
> dans cerveau-projet/freelance/tools-commun/securite/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## IDENTITE DU DOSSIER

| Champ | Valeur |
|---|---|
| **Chemin** | cerveau-projet/freelance/tools-commun/securite/ |
| **Proprietaire** | Vision (habilitation exclusive) |
| **Type** | Securite d'acces |
| **Encodage** | ASCII + LF |

---

## COMPOSANTS

### 1. lecteur-de-carte/

| Fichier | Role |
|---|---|
| lecteur-de-carte.py | Verifie si un agent a le droit d'acceder a un outil |
| lecteur-de-carte.md | Mode d'emploi |
| cartes-data.json | Donnees des cartes d'acces (D15) |

### 2. verrou-outils/

| Fichier | Role |
|---|---|
| verrou-outils.py | Applique les verrous sur les outils |
| verrou-outils.md | Mode d'emploi |
| verrous-data.json | Donnees des verrous (D15) |
| journal-acces.jsonl | Journal des tentatives d'acces (APPEND-ONLY) |

---

## POURQUOI CE DOSSIER EST CRITIQUE

C'est le SYSTEME DE SECURITE de la v2.
Si il est casse, les agents peuvent acceder a des outils non autorises
ou sont bloques de leurs propres outils.

---

## REGLE ABSOLUE

> JE NE MODIFIE JAMAIS les outils de securite sans avoir TESTE
> qu'un agent AUTORISE peut toujours acceder a ses outils
> et qu'un agent NON AUTORISE est toujours bloque.
> LE JOURNAL D'ACCES EST APPEND-ONLY : je n'efface JAMAIS.

---

## AVANT de commencer

1. **Lire lecteur-de-carte.py EN ENTIER**
2. **Lire verrou-outils.py EN ENTIER**
3. **Lire cartes-data.json** : comprendre les cartes existantes
4. **Lire verrous-data.json** : comprendre les verrous existants**
5. **Lire journal-acces.jsonl** : comprendre les dernieres tentatives
6. **Verifier les dependances** : aucun module externe

---

## APRES modification

1. **Tester lecteur-de-carte.py** : un agent autorise passe ?
2. **Tester verrou-outils.py** : un agent non autorise est bloque ?
3. **Verifier le journal-acces.jsonl** : les nouvelles entrees sont la ?
4. **Mettre a jour le cahier de dev** : noter ce qui a change

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| Pas de suppression d'entrees du journal | Tracabilite perdue |
| Pas de modification de cartes-data.json sans verification | Un agent perd l'acces |
| Pas de modification de verrous-data.json sans verification | Un outil devient inaccessible |
| Pas de changement de logique de verification | Risque de faille de securite |
| Pas de modification sans test | Risque de blocage total |
