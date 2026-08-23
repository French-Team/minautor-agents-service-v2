---
identite:
  nom: tools-commun
  version: 0.1.0
  cree: 2026-08-22
  type: reference
  appartient_a: forge
  commun: true
  tags: outils, commun, freelance, v2
  mot-cles: ["outils", "commun", "jarvis", "activation", "partages", "v2"]
  session: freelance
# Tools Communs -- Equipe Freelance (v2)

> Outils partages par TOUS les agents de la session-freelance.
> Forge en est le responsable.

---

## Principe

| Type | Emplacement | Usage |
|---|---|---|
| **Outil dedie** | `freelance/<agent>/tools/` | Outill specifique a un agent (ex: construire-agent pour Shuri) |
| **Outil commun** | `freelance/tools-commun/` | Outill utilise par plusieurs agents (activation, lecons, lecture...) |

**REGLE** : un outil ne vit QUE dans un seul endroit (P5, SSOT).

---

## Contenu de tools-commun/

```
tools-commun/
├── README.md                    <- ce fichier
├── activer/                     <- activation d'agents
├── lire/                        <- lectures partagees
├── consulter/                   <- consultations
├── enregistrer/                 <- enregistrements
└── valider/                     <- validations
```

---

## Ajouter un outil

1. Determiner si l'outil est DEDIE (un seul agent) ou COMMUN (plusieurs agents).
2. Creer le dossier dans l'emplacement appropriate.
3. Creer le .md (contrat/mode d'emploi), le .py (script), et si besoin le .json (donnees, D15).
4. Le .md contient la carte d'identite (D17) + la commande fonctions.
