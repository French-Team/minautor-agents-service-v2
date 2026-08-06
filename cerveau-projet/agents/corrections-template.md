---
# Corrections et Surcharges — [Nom de l'agent]
# Ce fichier contient les regles specifiques a cet agent
# Il surcharge ou complete la fiche d'agent principale

agent:
  nom: "[nom-agent]"
  version_corrections: "0.2.0"
  derniere_mise_a_jour: "2026-08-06"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a l'agent"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
  - philosophie: "Principe de comportement appris"
  - lecon: "Lecon apprise apres une erreur"
---

# Corrections et Surcharges

---

## REGLES — Regles specifiques

| Regle | Description |
|---|---|
| **[Regle 1]** | [Description] |
| **[Regle 2]** | [Description] |

---

## PHILOSOPHIE — Principes de comportement

| Philosophie | Description |
|---|---|
| **[Philosophie 1]** | [Description] |
| **[Philosophie 2]** | [Description] |

---

## LECONS — Lecons apprises (cycle d'auto-correction)

| Date | Lecon | Philosophie liee |
|---|---|---|
| [Date] | [Lecon apprise] | [Philosophie] |
| [Date] | [Lecon apprise] | [Philosophie] |

> **PRINCIPE** : Chaque erreur detectee devient une lecon. Les lecons sont lues
> a chaque activation et evitees lors des missions suivantes.

---

## CONFIG — Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Standard"
  style_reponse: "Direct"
```

### Outils et methodes

| Outil/Method | Usage |
|---|---|
| [Outil 1] | [Usage] |
| [Outil 2] | [Usage] |

---

## NOTES — Notes de session

### Session du [Date]

**Tache** : [Description]

**Erreurs detectees** :
- [Erreur 1]
- [Erreur 2]

**Lecons apprises** :
- [Lecon 1]
- [Lecon 2]

---

## CONNEXIONS — Connexions

| Fichier | Role |
|---|---|
| `[nom-agent].md` | Fiche principale de l'agent |
| `AGENTS.md` | Fichier dynamique de l'agent principal |
| `../index-agents.md` | Index des agents |
| `../../pense-betes/regles-immuables/general/regles-emojis-ascii.md` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/regles-veracite.md` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/protocole-auto-correction/` | Auto-correction |
| `../../pense-betes/regles-immuables/general/protocole-installer-regles/` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/protocole-identification/` | **IMMUABLE** |

---
