---
identite:
  nom: harnais-nr
  version: 0.1.0
  cree: 2026-08-26
  type: outil
  appartient_a: forge
  commun: true
  statut: actif
  mot-cles: ["non-regression", "suites", "tests", "nr", "harnais", "v2"]
  tags: non-regression, suites, tests, v2, forge
  session: freelance
# HARNAIS-NR -- Cadre de suites de NON-REGRESSION (v2)

> COMMANDE FONCTIONS : `python3 cerveau-projet/freelance/tools-commun/harnais-nr/entry.py --help`

---

## Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Nom** | harnais-nr |
| **Version** | 0.1.0 (PHASE 1 : cadre) |
| **Role** | Moteur de suites de non-regression declarees en donnees (D15) |
| **Proprietaire** | Forge |

## Principe

Une SUITE = un dossier `suites/nr-<x>/` avec SA config `suite.json`.
Les tests sont des DONNEES (commande, rc attendu, sortie attendue,
fichiers verifies) - jamais du code. AUCUNE valeur en dur dans le code :
tout est dans `harnais-nr-data.json` ou les suite.json.

**Principe NR absolu** : apres une suite, le workspace est IDENTIQUE
(hash avant = hash apres sur le perimetre, sinon ECART).

## Securites (config D15)

| Securite | Effet |
|---|---|
| bak_avant_ecriture | .bak-nr avant toute ecriture declaree |
| rollback_sur_echec | restauration garantie meme en cas d'echec |
| lecture_seule_par_defaut | un test qui modifie doit declarer ecriture_autorisee |
| sandbox_temp | .nr-sandbox/ pour les ecrits temporaires des commandes |
| hors_perimetre_interdit | tout fichier cible hors perimetre = refus immediat |

## Commandes

```bash
python3 entry.py lister
python3 entry.py executer --suite nr-jarvis [--test X] [--rapport]
python3 entry.py executer --toutes [--rapport]
```

## Suites prevues (phase 2 - a creer puis replicer par agent)

nr-jarvis (Vision), nr-agents (Shuri), nr-commun (Forge), nr-<agent>...
