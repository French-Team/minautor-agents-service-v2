# verifier-conformite-fiche
**Version** : 0.2.1

Outil de verification de la conformite des fiches agents au template
[fiche-agent-template.md](../../../fiche-agent-template.md), selon le
**modele par role** (noyau obligatoire + variante de famille).

## Description

Verifie qu'une fiche agent (`agents/<agent>/<agent>.md`) suit la structure
du template de fiche. Les sections `## X` du template sont lues
**DYNAMIQUEMENT** : l'outil reste donc valide apres toute mise a jour du
template (ajout/suppression de section).

**Modele par role (v0.2.0)** : chaque fiche doit contenir le NOYAU
obligatoire (fiche-agent-template.md) PLUS les sections de la VARIANTE de
sa famille :

| Famille | Fichier variante | Agents |
|---|---|---|
| `cerveau-projet` | [fiche-template-variante-cerveau.md](../../../fiche-template-variante-cerveau.md) | cerberus, buffy, vulcain, morpheus, janus, atlas, themis, clio |
| `trio` | [fiche-template-variante-trio.md](../../../fiche-template-variante-trio.md) | athena, promethee, minerve |

La famille est determinee par `--variante`, sinon lue du frontmatter de la
fiche (cle `famille:`), sinon une valeur par defaut par agent.

## Utilisation

### Verifier UNE fiche (famille auto)

```
python3 verifier-conformite-fiche.py --agent buffy
```

### Verifier UNE fiche avec variante explicite

```
python3 verifier-conformite-fiche.py --agent minerve --variante trio
```

### Verifier une SELECTION

```
python3 verifier-conformite-fiche.py --agents buffy,cerberus --variante cerveau-projet
```

### Verifier TOUTES les fiches + rapport markdown

```
python3 verifier-conformite-fiche.py --tous --rapport rapport-impact.md
```

## Ce que l'outil verifie (par fiche)

| Controle | Detail |
|---|---|
| **Frontmatter YAML** | delimiteur `---` en premiere ligne, cle `agent:` ou `nom-agent:` presente, delimiteur de cloture dans les 100 premieres lignes |
| **Sections du noyau** | chaque section `## X` du template noyau doit etre presente dans la fiche (SECTIONS MANQUANTES = ecart) |
| **Sections de la variante** | chaque section de la variante de la famille doit etre presente (SECTIONS MANQUANTES = ecart) |
| **Sections en plus** | ni noyau ni variante -- specifiques au role de l'agent, TOLEREES et NON BLOQUANTES, signalees en avertissement (~) |
| **Ordre** | verifie SEPAREMENT a l'interieur du noyau et de la variante (les fiches peuvent intercaler leurs sections specifiques) |

## Exemples de sortie

```
=== verifier-conformite-fiche v0.2.0 ===
Noyau   : .../fiche-agent-template.md (8 sections)
Cibles  : 2 fiche(s): buffy, themis
Variante: cerveau-projet (2 sections)

[OK] buffy (cerveau-projet) : CONFORME
[KO] themis (cerveau-projet) : ECARTS
     - SECTIONS MANQUANTES: ## Forces et Faiblesses; ## Style de travail
     - SECTIONS SPECIFIQUES (tolerees): ## PROTOCOLE DE RAPPORT; ...

=== RESULTAT : 1 CONFORME / 1 ECARTS (sur 2 fiche(s)) ===
```

## Quand l'utiliser

- **Apres une refonte du template ou d'une variante** : mesurer l'impact sur
  les 11 fiches (`--tous --rapport`) avant de corriger
- **Avant de creer une fiche** : verifier que le template est a jour
- **Controle de sante des fiches agents** : croiser avec le protocole
  sante-fichiers-agents (Janus)

## Relation avec les autres outils

- `valider-conventions` : verifie les conventions generales (frontmatter,
  titre) sur n'importe quel fichier -- complementaire
- `verifier-role-fichier` : verifie qu'un fichier est utilise pour sa fonction
- `editer-fichier-agents` : corrige une fiche (ajout/suppression de section,
  correcteur ASCII) apres les ecarts signales par cet outil
- `evaluer-structure` / `evaluer-agents` : evaluent la structure du cerveau
  dans son ensemble

## Versionning

| Version | Date | Changement |
|---|---|---|
| 0.1.0 | 2026-08-11 | Creation : lecture dynamique des sections du template, cibles --agent/--agents/--tous, --rapport, --dry-run, --verbose. Rapport d impact initial conserve (rapport-impact-v010-2026-08-11.md) |
| 0.2.0 | 2026-08-11 | MODELE PAR ROLE : option --variante (cerveau-projet/trio), famille lue du frontmatter de la fiche, sections de variante manquantes = ecarts, ordre separe noyau/variante. Rapports v020 conserve (2 CONFORME / 9 ECARTS) |
| 0.2.1 | 2026-08-11 | CORRECTION : sections SPECIFIQUES (ni noyau ni variante) = TOLEREES NON BLOQUANTES (avertissement ~). Verdict CONFORME = 0 ecart bloquant. 11/11 CONFORME apres correction des 9 fiches (rapport-impact-v021-2026-08-11.md) |
