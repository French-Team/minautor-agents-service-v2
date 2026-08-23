---
identite:
  nom: templates-v2
  version: 0.1.0
  cree: 2026-08-22
  type: documentation
  appartient_a: shuri
  commun: false
  mot-cles: ["templates", "guide", "creation", "agents", "v2", "marvel"]
---
# Templates V2 - Guide d'utilisation

> Source de verite pour la creation d'agents v2.
> Shuri suit CE template exactement. Aucune deviation.

---

## Fichiers du template

| Fichier | Usage |
|---|---|
| `template-agent-v2.md` | Fiche de l'agent (D17) |
| `template-corrections-v2.md` | Corrections et lecons |
| `template-arbre-v2.json` | Arbre de decisions (racine) |
| `template-theme-v2.json` | Un theme dans l'arbre |
| `template-fins-v2.json` | Fins centralisees |

---

## Procedure de creation d'un agent

### 1. Creer la structure
```
freelance/<agent>/
├── <agent>.md              <- template-agent-v2.md
├── corrections.md          <- template-corrections-v2.md
├── parcours/
│   ├── arbre-<agent>.json  <- template-arbre-v2.json
│   ├── theme-<theme>.json  <- template-theme-v2.json (un par theme)
│   └── fins.json           <- template-fins-v2.json
└── tools/                  <- vide au depart
```

### 2. Remplir la fiche
- Remplacer `<NomMarvel>` par le nom du heros
- Remplacer `<agent>` par le nom en minuscules
- Remplacer `<Role>` par le role precise
- Remplacer les citations par celles du personnage
- Remplacer `<domaine>` par le domaine de competence

### 3. Definir les themes
- **THEME_PRINCIPAL** : le role principal de l'agent
- **LIRE** : toujours present (consulter l'information)
- **COORDONNER** : toujours present (retour a Stark)
- Themes optionnels selon le role

### 4. Creer les fichiers theme
- Un fichier par theme
- Chaque theme a des "redirects" (besoins concrets)
- Chaque redirect a un "action" : procedure ou redirection
- Chaque theme finit par un lien vers fins.json

### 5. Creer fins.json
- **fin-theme** : retour a l'arbre (toujours present)
- **fin-stark** : retour a Stark via JARVIS (toujours present)
- **fin-inter-round** : reactivation de l'appelant (optionnel)

---

## Regles absolues

| Regle | Detail |
|---|---|
| **PAS de parcours V1** | Pas de parcours-*.json lineaire. Uniquement ARBRE |
| **PAS de dependance v1** | Pas de modification des outils v1 |
| **PAS d'enregistrement v1** | Pas dans activer-agent-principal |
| **JARVIS** | Toute communication passe par JARVIS |
| **Theme MARVEL** | Nom de heros en anglais, majuscule initiale |
| **D17** | Fiche avec grade, medaille, notation, mot-cles |
| **D15** | Separation code/donnees |
| **UTF-8/CRLF** | Standard v2/freelance |

---

## Exemple: creation de Parker

```
1. Verifier nom: Parker (Spider-Man) -> MARVEL OK
2. Creer structure: freelance/parker/ + parcours/ + tools/
3. Creer fiche: parker.md (copper, notation 50)
4. Creer corrections: corrections.md
5. Creer arbre: arbre-parker.json (themes: EXPLORER, LIRE, DIAGNOSTIQUER, COORDONNER)
6. Creer themes: theme-explorer.json, theme-lire.json, theme-diagnostiquer.json, theme-coordonner.json
7. Creer fins: fins.json
8. Mettre a jour AGENTS.md + proposition-v2.md
9. Valider: verifier structure, coherence, conformite
```
