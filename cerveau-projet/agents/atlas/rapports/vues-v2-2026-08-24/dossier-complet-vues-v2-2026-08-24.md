# Dossier complet des vues v2 -- ARBRES de decision

- **Date** : 2026-08-24
- **Auteur** : Atlas (mission vues-v2, carte v0.5.7)
- **Outil** : `convertir-carte-mermaid --arbres` (v0.3.0, Vulcain)
- **Source de verite** : `freelance/<agent>/parcours/arbre-<agent>.json`

> Document NON NORMATIF : il decrit le contenu des vues v2, il n autorise
> et n interdit rien aux agents. Les regles applicables restent les cartes
> et les regles-immuables.

## Difference ARBRE v2 vs CARTE v1

| | Carte v1 | Arbre v2 |
|---|---|---|
| Fichier | `parcours-<agent>.json` | `arbre-<agent>.json` |
| Structure | `cases` (case_depart, cases, suivant/branches, fins) | `racine` (question + branches) -> `theme-*.json` (redirects) -> `fins.json` |
| Vue | cartes-vues/mermaid/ | cartes-vues/arbres/ |
| Outil | `convertir-carte-mermaid` (sans --arbres) | `convertir-carte-mermaid --arbres` |
| Agents | 19 agents v1 | 9 agents v2 |

## Les 9 agents v2 avec arbre de decision

| Agent | Role | Fichiers |
|---|---|---|
| stark | Coordinateur equipe freelance, responsable JARVIS | arbre-stark.json + theme-*.json + fins.json |
| shuri | Constructeur des agents de la v2 | arbre-shuri.json + theme-*.json + fins.json |
| forge | Responsable des outils v2 | arbre-forge.json + theme-*.json + fins.json |
| rogers | Gardien des regles, conventions et protocoles | arbre-rogers.json + theme-*.json + fins.json |
| parker | Explorateur / diagnostiqueur | arbre-parker.json + theme-*.json + fins.json |
| jarvis | Intelligence derriere le serveur, assistant de Stark | arbre-jarvis.json + theme-*.json + fins.json |
| vision | Gardien exclusif de JARVIS | arbre-vision.json + theme-*.json + fins.json |
| fury | Testeur reel HORS-ROUND | arbre-fury.json + theme-*.json + fins.json |
| edith | Observatrice (cellule dormante) | arbre-edith.json + theme-*.json + fins.json |

## Vues generees (cartes-vues/arbres/)

| Agent | .mmd | .svg |
|---|---|---|
| edith | [edith.mmd](../../../../cartes-vues/arbres/edith.mmd) | [edith.svg](../../../../cartes-vues/arbres/edith.svg) |
| forge | [forge.mmd](../../../../cartes-vues/arbres/forge.mmd) | [forge.svg](../../../../cartes-vues/arbres/forge.svg) |
| fury | [fury.mmd](../../../../cartes-vues/arbres/fury.mmd) | [fury.svg](../../../../cartes-vues/arbres/fury.svg) |
| jarvis | [jarvis.mmd](../../../../cartes-vues/arbres/jarvis.mmd) | [jarvis.svg](../../../../cartes-vues/arbres/jarvis.svg) |
| parker | [parker.mmd](../../../../cartes-vues/arbres/parker.mmd) | [parker.svg](../../../../cartes-vues/arbres/parker.svg) |
| rogers | [rogers.mmd](../../../../cartes-vues/arbres/rogers.mmd) | [rogers.svg](../../../../cartes-vues/arbres/rogers.svg) |
| shuri | [shuri.mmd](../../../../cartes-vues/arbres/shuri.mmd) | [shuri.svg](../../../../cartes-vues/arbres/shuri.svg) |
| stark | [stark.mmd](../../../../cartes-vues/arbres/stark.mmd) | [stark.svg](../../../../cartes-vues/arbres/stark.svg) |
| vision | [vision.mmd](../../../../cartes-vues/arbres/vision.mmd) | [vision.svg](../../../../cartes-vues/arbres/vision.svg) |

Index : [index.md](../../../../cartes-vues/arbres/index.md)

## Structure d un .mmd arbre (exemple stark)

```
flowchart TD
    START(["Debut"]) --> RACINE
    RACINE{"<question>"}
    RACINE -- "<reponse>" --> THEME-<nom>
    THEME-<nom>["<but du theme>"]
    THEME-<nom> -- "besoin N" --> THEME-<nom>-B<N>
    THEME-<nom>-B<N>["<besoin>"]
    THEME-<nom> --> FIN-<case>
    FIN-<case>(["<titre fin depuis fins.json>"])
```

## Verification

- `convertir-carte-mermaid --arbres --verifier` : rc=0, "9 arbres v2
  synchronises avec leur .mmd et .svg : OK"
- test-101-arbres-mermaid-garde-fou : 11/11 OK (preuves negatives incluses)
- ASCII strict + LF pur sur tous les fichiers
