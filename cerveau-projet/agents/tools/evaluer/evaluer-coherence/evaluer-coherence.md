---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combos-audit-general
---
# evaluer-coherence

**Version :** 0.2.5
**Statut :** prepare
**Categorie :** evaluer
**Chemin :** `agents/tools/evaluer/evaluer-coherence/`
**Proprietaire :** Themis (outil partage)

## Description

Evalue la coherence inter-fichiers : liens, references croisees, dossiers vides.

## Utilisation

```bash
bash evaluer-coherence.sh [DOSSIER]
# Version Python (recommandee)
python3 evaluer-coherence.py [DOSSIER]
```

## Ce qu'il verifie

- Liens internes casses ([texte](chemin) pointant vers des fichiers inexistants)
- Dossiers vides suspects (hors spec/todo/exemples)
- Agents declares dans AGENTS.md
- Outils references par les agents qui existent reelement

## Sortie

Rapport markdown sur stdout avec score /100.

## Code retour

| Code | Signification |
|---|---|
| 0 | Le dossier cible existe (meme avec des incoherences signalees) |
| 1 | Le dossier cible n'existe pas |

## Dependances

- bash, python (parseur de liens), tr

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete standardise. Bug corrige : exclusions ajoutees (convention-*, protocole-*, regles-*, templates, rvav) pour eviter les faux positifs sur les references pense-betes/ |
| 0.2.1 | 2026-08-07 | Lecon audit general : parseur Python pour les liens internes - ignore les blocs de code (``` et ~~~), les motifs generiques (texte, chemin, ancien.md, index.md, frere-b, etc.), les liens externes et les ancres. Resolution double (relative au fichier ET a la racine cerveau-projet). Exclusion du dossier exemples/ (problemes volontaires). Normalisation CRLF/LF pour Git Bash |
| 0.2.0-py | 2026-08-07 | Version Python creee (portage fidele : dossiers vides signalent spec/todo vides, scan outils au niveau 3 incluant les protections) |
| 0.2.1 | 2026-08-07 | Correction faux positifs: (1) resolution des liens ../ depuis le projet root (dossier) en plus de cerveau-projet/, (2) exclusion des commandes systeme (cat, grep, sed, basher) du scan des outils casses. Score coherence corrige de 25/100 a 50/100 (1 lien casse reel: badges-README-github.md). |
| 0.2.1-py | 2026-08-07 | Version Python corrigee (parite sh/py) |
| 0.2.2 | 2026-08-09 | Correction faux positifs : scan des outils references limite aux 11 agents officiels (AGENTS_ATTENDUS) au lieu de tous les dossiers de agents/ - classeur-variables/ et ses variables (statut-mission, contexte, resultats, erreurs) ne sont plus interpretees comme des outils inexistants. Parite py/sh maintenue |
| 0.2.3 | 2026-08-15 | Correction faux positifs (lecon Janus, non-regression barriere E) : (1) options de ligne de commande --xx exclues du scan (--parallele, --serial, --etat-tests), (2) mots francais simples entre backticks (conforme, success, probleme) exclus - un nom d outil du cerveau contient un tiret ou est connu des dossiers reels, (3) AGENTS_ATTENDUS passe de 11 a 15 agents (ajout hygie, hermes, gardien, argus) |
| 0.2.5 | 2026-08-19 | Mission liens casses (volet Vulcain) : ajout de `protocole-X` aux MOTIFS_GENERIQUES - les references [protocole-X/](protocole-X/) dans les lecons sont des exemples de format (placeholder documentaire), pas des liens reels. Resultat : evaluer-coherence passe de 5 a 0 lien casse |

---
