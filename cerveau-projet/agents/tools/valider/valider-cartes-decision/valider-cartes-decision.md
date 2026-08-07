# valider-cartes-decision

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** valider
**Chemin :** `agents/tools/valider/valider-cartes-decision/`
**Proprietaire :** Janus (outil partage)

---

## Objectif

Verifier que les agents respectent les cartes de decision dans leurs fichiers.

**Pourquoi cet outil ?**
- Les agents peuvent ne pas respecter les cartes de decision
- Les cartes peuvent etre incompletes ou incorrectes
- Cet outil automatise la verification
- Il garantit la coherence du systeme

---

## Utilisation

```
valider-cartes-decision(agent="Buffy")
valider-cartes-decision(tous="true")
valider-cartes-decision(fichier="chemin/vers/fichier.md")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `agent` | string | Non | Nom de l'agent a verifier |
| `tous` | boolean | Non | Verifier tous les agents |
| `fichier` | string | Non | Verifier un fichier specifique |

---

## Ce que l'outil verifie

### 1. Presence de la section "Carte de Decision"

```
[ ] La section existe
[ ] Elle est placee apres "Vue d'ensemble"
[ ] Elle contient "CARTE DE DECISION" en majuscules
```

### 2. Structure de la carte

```
[ ] Tableau "Missions disponibles" present
[ ] Chaque mission a un nom
[ ] Chaque mission a des etapes
[ ] Chaque mission a des protocoles
```

### 3. Detail des missions

```
[ ] Chaque mission a un titre "Mission : [nom]"
[ ] Chaque mission a "QUAND" (condition de declenchement)
[ ] Chaque mission a un tableau d'etapes
[ ] Chaque etape a : Action, Protocole, Sortie
```

### 4. Regles absolues

```
[ ] Au moins une regle absolue est definie
[ ] La regle est en majuscules
[ ] La regle est pertinente pour l'agent
```

---

## Format de sortie

### Format tableau (defaut)

```markdown
## Resultat de la validation -- Agent Buffy

| Verification | Statut | Notes |
|---|---|---|
| Section Carte de Decision | [OK] | Presente |
| Tableau Missions | [OK] | 5 missions |
| Detail des missions | [OK] | Toutes completes |
| Regles absolues | [OK] | 2 regles |

**Verdict** : [OK] CONFORME
```

### Format detaille

```markdown
## Resultat detaille

### Mission : Creer un fichier

| Etape | Action | Protocole | Statut |
|---|---|---|---|
| 1 | Verifier le nommage | convention-renommage | [OK] |
| 2 | Verifier la structure | convention-structures | [OK] |
| 3 | Creer le fichier | - | [OK] |
| 4 | Mettre a jour l'index | - | [OK] |
```

---

## Erreurs courantes

| Erreur | Correction |
|---|---|
| Section manquante | Ajouter "## CARTE DE DECISION" |
| Pas de tableau missions | Ajouter tableau avec Missions/Etapes/Protocoles |
| Etape sans protocole | Ajouter protocole ou "-" si aucun |
| Pas de regle absolue | Ajouter au moins une regle en majuscules |

---

## Dependances

- `agents/[nom]/[nom].md` -- fichier de l'agent a verifier

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |

---

## Notes

- Cet outil est ESSENTIEL pour maintenir la qualite des cartes
- Il doit etre execute apres chaque modification de carte
- Les resultats doivent etre documentes

---
