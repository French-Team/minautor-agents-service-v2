# detecter-ecritures-hors-cycle

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** detecter

## Pourquoi cet outil ?

GARDE-FOU ANTI-DERIVE : detecte les ecritures de fichiers de travail qui
echappent au cycle d activation (Cerberus -> agent -> Cerberus).

La derive constatee le 2026-08-17 (l IA a travaille en solo sans activations
formelles) a montre que les ecritures directes de fichiers contournent tous les
outils du projet. Cet outil les detecte a posteriori en croisant les fichiers
modifies avec la chronologie des activations.

## Ce que fait l outil

1. Lit le DERNIER horodatage d activation dans `AGENTS-historique.md` et
   l agent actif dans `AGENTS.md` (session-llm-1).
2. Collecte les fichiers modifies :
   - PRIMAIRE : `git status --porcelain -uall` + `git diff --name-only HEAD`
   - SECOURS : si git indisponible, fichiers dont le mtime est posterieur au
     dernier horodatage d activation.
3. Exclut la coordination/les traces : `.git/`, `workspace/`,
   `classeur-variables/`, `traces/`, `tmp-*`, `.tmp-*`, `.zz-*`,
   `__pycache__/`, `AGENTS.md`, `AGENTS-historique.md`, + `.tmpignore`.
4. Verdict :
   - **OK** : aucun fichier de travail modifie hors cycle.
   - **KO** (code 1) : des fichiers de travail sont modifies APRES la derniere
     activation alors que l agent actif est Cerberus (coordination).
   - **ATTENTION** (code 0) : des fichiers sont modifies alors qu un agent de
     travail est actif (couverture presumee par la mission en cours).

## Utilisation

```
python3 detecter-ecritures-hors-cycle.py
python3 detecter-ecritures-hors-cycle.py --rapport ecarts-hors-cycle.md
python3 detecter-ecritures-hors-cycle.py --depuis "2026-08-17 19:47"
python3 detecter-ecritures-hors-cycle.py --agent cerberus
```

## Options

| Option | Description |
|---|---|
| `--depuis <horodatage>` | Reference au lieu de la derniere activation (YYYY-MM-DD HH:MM) |
| `--agent <nom>` | Forcer l agent actif (defaut : lu dans AGENTS.md) |
| `--rapport <fichier>` | Ecrire le rapport markdown |
| `--verbose` | Detail par fichier |
| `--version` | Afficher la version |
| `--aide` | Afficher l aide (alias de -h) |

## Limites

- La prevention est impossible : les ecritures directes du LLM (write_file)
  contournent les outils du projet. Cet outil DETECTE, il n empeche pas.
- Le mode ATTENTION (agent de travail actif) ne tranche pas le domaine de
  l agent : un agent qui edite un fichier hors de son domaine est signale par
  `evaluer-processus` (registre) et le verrou d habilitation, pas ici.
- Il doit etre lance a un point de controle (debut de round, non-regression
  Janus) pour reveler une derive avant qu elle ne s accumule.
