# Outil -- Modifier AGENTS.md

**Categorie** : Mettre a jour
**Version** : 0.2.0
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Modifier AGENTS.md de maniere fiable et structuree.

**Pourquoi cet outil ?**
- AGENTS.md est un fichier critique -- les erreurs cassent le cycle
- Cet outil est concu SPECIFIQUEMENT pour AGENTS.md
- Il gere la structure et les formats automatiquement
- Il est fiable et teste

---

## Utilisation

```
mettre-a-jour-modifier-agents-md(action="activer", agent="Buffy", raison="Mission correction")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `action` | string | Oui | "activer" ou "reactiver" |
| `agent` | string | Si activer | Nom de l'agent a activer |
| `raison` | string | Oui | Raison du changement |
| `mission` | string | Non | Description de la mission |

---

## Actions disponibles

### 1. Activer un agent

```
mettre-a-jour-modifier-agents-md(
  action="activer",
  agent="Buffy",
  raison="Corriger les fichiers",
  mission="Mettre a jour demarrer.md"
)
```

**Fait :**
1. Lit AGENTS.md
2. Met a jour la section "Agent Principal Actuel"
3. Ajoute l'entree dans l'historique
4. Ecrit le fichier

### 2. Reactiver Cerberus

```
mettre-a-jour-modifier-agents-md(
  action="reactiver",
  raison="Mission terminee",
  agent_precedent="Buffy"
)
```

**Fait :**
1. Lit agents/cerberus/cerberus.md
2. Lit AGENTS.md
3. Met a jour avec "Nom: Cerberus"
4. Ajoute l'entree dans l'historique
5. Ecrit le fichier

---

## Format de sortie

### Section "Agent Principal Actuel"

```markdown
## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | [agent] |
| **Role** | [role de l'agent] |
| **Derniere mise a jour** | [date] |
| **Fiche** | [lien] |
| **Corrections** | [lien] |
| **Active par** | [agent precedent] |
| **Raison** | [raison] |
```

### Historique (AGENTS-historique.md)

```
| [date et heure] | [agent] | [raison] |
```

**Format de l'horodatage** : `YYYY-MM-DD HH:MM` (date + heure precise)

**Regles de l'historique** :
- **Heure incluse** : chaque entree porte la date ET l'heure (HH:MM) pour situer precisement les groupes d'interventions
- **Ordre decroissant** : les entrees les plus recentes sont en HAUT du tableau
- **Limite 150** : le fichier ne conserve que les 150 interventions les plus recentes (les plus anciennes sont retirees automatiquement)

---

## Ce que fait cet outil

| Capacite | Description |
|---|---|
| Specifique a AGENTS.md | Concu pour ce fichier critique |
| Gere le format | La structure est maintenue automatiquement |
| Lit cerberus.md | Lit le fichier de Cerberus pour la reactivation |
| Valide le resultat | Verifie que la modification est correcte |
| Fiable et teste | Fonctionne a chaque fois |
| Horodatage HH:MM | Date + heure precise dans l'historique |
| Ordre decroissant | Les plus recentes en haut |
| Limite 150 | Tronque automatiquement a 150 entrees |

---

## Exemple complet

### Utilisation

```
1. Appeler mettre-a-jour-modifier-agents-md(action="reactiver", ...)
2. L'outil lit cerberus/cerberus.md
3. L'outil met a jour AGENTS.md
4. C'est fait -- fiablement
```

---

## Dependances

- `AGENTS.md` -- fichier a modifier
- `agents/cerberus/cerberus.md` -- lu lors de la reactivation

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0-beta | 2026-08-06 | Historique : horodatage HH:MM + ordre decroissant + limite 150 |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels avec protections (activation, reactivation, limite 150, ordre decroissant), VERSION ajoutee au script, promotion prepare |

---

## Notes

- Cet outil est CRITIQUE -- il gere le fichier le plus important
- La reactivation lit cerberus.md (pas corrections.md sauf en cas d'erreur)
- Chaque erreur ici casse tout le cycle

---
