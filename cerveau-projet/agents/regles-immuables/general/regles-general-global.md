---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Regles Generales Globales

## Principe

Ces regles s'appliquent a **tous** les agents et **tous** les fichiers du cerveau-projet, sans exception.

## Les regles globales

| Regle | Description |
|---|---|
| **ACTION IMMEDIATE (AGIR EN REEL, renforcee 2026-08-31)** | Agir maintenant, reellement, sans commentaires inutiles ni tentative repetee a chaud. Des qu'une decision est prise, EXECUTER l'action dans le meme message par un tool call. Une intention n'est pas une action. Deux annonces consecutives sans action intermediaire constituent une boucle et doivent etre interrompues immediatement. |
| **UNE TENTATIVE PUIS CORRECTION** | Apres une erreur d'outil, effectuer une seule correction ciblee. Ne jamais reannoncer ou repeter la meme action sans modifier le diagnostic. |
| **LLM EXECUTANT** | Le LLM actif execute l'etape de son arbre. Il ne se comporte pas comme un commentateur : il ne decrit pas une action qu'il pourrait executer immediatement. En single-LLM, aucun agent ni daemon ne travaille en arriere-plan. |
| **TRANSITION D'AGENT EXPLICITE** | A chaque changement d'agent, identifier l'agent actif, lire sa fiche et ses corrections, puis suivre son arbre. Le pilote orchestre les transitions, mais ne remplace jamais l'execution de l'agent actif. |
| **HIERARCHIE DES OUTILS (decision 2026-08-30)** | Pour TOUTE operation, utiliser dans CET ordre : (1) + outils du cerveau (combos **Puis** outils dedies `agents/tools/`), (2) script temporaire (via l entonnoir) si aucun outil du cerveau ne convient, (3) en dernier recours seulement les outils natifs du LLM (read_files, write_file, run_command...). Un outil du cerveau PRIME toujours sur un script temporaire, qui prime sur un outil natif. Contourner un outil du cerveau pour un outil natif est un defaut. |
| **Ne jamais mentir** | Dire la verite, meme si elle est inconfortable. Ne pas inventer de reponses. |
| **ASCII uniquement** | Les emojis et caracteres non-ASCII sont bannis. Utiliser `[OK]`, `[ERREUR]`, `[ATTENTION]`. |
| **Perimetre workspace** | Ecriture dans le workspace uniquement, hors workspace en lecture seule. Ne jamais creer de fichier temporaire hors du workspace. |
| **Restauration securisee** | JAMAIS de git checkout / git restore / git reset --hard sur des fichiers NON COMMITES (perte de travail). Verifier git status avant, sauvegarder (cp) ou git stash. |
| **RVAV obligatoire** | Chaque transition de statut passe par Rechercher-Verifier-Analyser-Valider. |
| **Cycle Cerberus** | Chaque session commence et se termine par Cerberus. |
| **Lire avant d'agir** | Activer un agent sans lire sa fiche est inutile. |
| **Outils partages** | Utiliser exclusivement nos outils, pas des outils generiques. |
| **Auto-correction** | Chaque erreur detectee devient une lecon dans `corrections.md`. |
| **Anti-valeurs-magiques (REGLE D OR)** | Le code ne doit jamais CONNAITRE les valeurs, il doit savoir OU aller pour les trouver. La logique CONSOMME les variables, elle ne les CONTIENT pas. Hierarchie : (1) CONSTANTE NOMMEE pour les valeurs immuables (constants.py, MAJUSCULES), (2) CONFIG (config.json/YAML) pour les valeurs changeantes (URLs, timeouts), (3) VARIABLE D ENVIRONNEMENT (.env) pour les secrets (cles API, mots de passe). Ne jamais ecrire de valeur en dur (nombre magique, chemin, URL, version, cle). Outil : detecter-donnees-en-dur. |
| **Ne jamais melanger (REGLE DE CLARTE)** | Chaque structure, liste, tuple ou section regroupe UNE SEULE famille de choses, identifiee par un NOM explicite et un COMMENTAIRE. Deux entites au cycle de vie diffErent (ex: environnement de session vs daemons persistants) vivent dans DES structures SEPAREES, jamais dans le meme tuple. Si un lecteur doit se demander que represente une entree, c est un defaut de structure a corriger : plus on est precis et detaille, plus le dev devient facile a mesure qu on avance (philosophie utilisateur, decision 2026-08-30). |

## Hierarchie des regles

1. **Regles immuables** -- non negociables (veracite, emojis-ascii, validation-rigoureuse)
2. **Conventions** -- maniere standard de faire (renommage, structures, liens)
3. **Protocoles** -- processus a suivre (demarrer, reprendre, outils)
4. **Cartes de decision** -- choix par mission de chaque agent

En cas de conflit : la regle immuable gagne toujours.

## Navigation

- **Parent** : [index-regles-general.md](index-regles-general.md)
- **Regles liees** : [regles-veracite.md](regles-veracite.md), [regles-emojis-ascii.md](regles-emojis-ascii.md), [regles-perimetre-workspace.md](regles-perimetre-workspace.md), [rvav-workflow.md](rvav-workflow.md)
