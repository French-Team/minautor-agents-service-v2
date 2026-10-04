# detecter-contradictions

**Version** : 0.1.3
**Statut** : ebauche
**Categorie** : Detecter
**Agent** : Argus (detecteur de contradictions)

## Role

Croise les sources du cerveau-projet pour trouver et comparer les
contradictions dans les CASES (parcours JSON), les REGLES et PROTOCOLES
(regles-immuables/general/), et l'HISTORIQUE GIT (git log --all, evolutions
vraies et fausses). Argus DETECTE et SIGNALE : il ne corrige jamais, l agent
habilite corrige.

## Pourquoi cet outil ?

- Depuis le debut du projet, du code a ete ajoute et a pu entrer en conflit
  (regles, protocoles, cases) sans etre detecte.
- On a besoin d un agent dedie (Argus) auquel on fait appel quand on constate
  des problemes incoherents, avec des techniques et outils specialises.
- La lecture du depot git (git log --all) montre TOUTES les evolutions du
  projet, vraies et fausses : les fichiers modifies hors protocole, les
  residus de versions, les corrections abandonnees.

## Detections

| Audit | Type | Gravite | Exemple |
|---|---|---|---|
| --cases | FIN_NON_JOIGNABLE | critique | fin jamais atteignable depuis la case de depart |
| --cases | CAS_ORPHELINE | majeur | case jamais atteignable (le maillon manquant) |
| --cases | BOUCLE_BLOQUANTE | majeur | cycle sans sortie entre 2+ cases |
| --cases | REF_MORTE | majeur | suivant/branche vers une case inexistante |
| --fichier | (idem cases) | - | audit d UN parcours JSON arbitraire (copie, preuve) |
| --regles | REF_CASSEE | majeur | lien markdown vers un fichier inexistant |
| --regles | TITRE_DOUBLON | mineur | titre de section duplique (hors titres generiques) |
| --regles | CONTRADICTION_REGLE | majeur | 2 regles de FICHIERS DIFFERENTS, meme sujet, marqueurs opposes (SEUL vs PEUT/JAMAIS) |
| --regles | REGLE_DOUBLON | mineur | meme formulation de regle dans 2 fichiers (desynchronisation suspecte) |
| --coherence | REGLE_PROTOCOLE | majeur | regle IMMUABLE omet/contredit une etape du protocole associe (ex: OUI -> mission au lieu de OUI -> c0c -> mission) |
| --coherence | REGLE_ABSENTE | majeur | section ### X (IMMUABLE) attendue absente de regles-groupes-agents.md |
| --coherence | REGLE_SANS_REFERENCE | mineur | regle IMMUABLE ne reference pas son protocole associe |
| --coherence | PROTOCOLE_ABSENT | mineur | protocole associe a une regle IMMUABLE introuvable |

Table REGLE_PROTOCOLE (v0.1.3) : RELIRE -> protocole-activation, RELEVE -> protocole-activation, SEUL HYGIE -> protocole-nettoyage, SEUL JANUS -> protocole-tests, SEUL MORPHEUS -> protocole-tests, SEUL CLIO -> protocole-verification-coherence, SEUL BUFFY -> protocole-controle-buffy, LE MODELE DE CONFIANCE -> protocole-controle-statuts
| --git | GIT_RESIDU_TEMP | mineur | commit passe avec fichier temporaire (.tmp-/.zz-/tmp-*) |
| --git | GIT_RESIDU_ACTUEL | majeur | residu PRESENT a la racine (tmp-*/, .tmp-*, fichiers de version) |

## Usage

```bash
# Tous les audits (cases + regles + coherence + git)
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --tous

# Un audit seul
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --cases
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --regles
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --coherence
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --git

# Audit cible d UN parcours JSON (copie, preuve negative)
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --fichier copie-parcours.json

# Rapport markdown
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --tous --rapport rapport-contradictions.md

# Details
python3 cerveau-projet/agents/tools/detecter/detecter-contradictions/detecter-contradictions.py --tous --verbose
```

## Options

| Option | Description |
|---|---|
| `--tous` | Lance les 4 audits (cases, regles, coherence, git) |
| `--cases` | Audit des parcours JSON uniquement |
| `--regles` | Audit des regles/protocoles (structure + contenu croise) |
| `--coherence` | Audit de coherence regle gravee <-> protocole associe (IMMUABLE) |
| `--git` | Lecture git (lecture seule) + croisement working tree |
| `--fichier <chemin>` | Audit cases d UN parcours JSON arbitraire |
| `--rapport <fichier>` | Ecrit le rapport markdown classe par gravite |
| `--verbose` | Detail des verifications |
| `--version` / `--aide` | Version / aide |

## Regles d Argus

- **JE DETECTE, JE NE CORRIGE PAS** : chaque incoherence est SIGNALEE avec
  preuves (fichier + ligne + sources croisees), la correction appartient a
  l agent habilite.
- **DOUBLE SOURCE** : une incoherence n est signalee que si elle est
  verifiee dans au moins 2 sources (anti-faux-positif).
- **LECTURE GIT EN LECTURE SEULE** : git log --all est lu, jamais modifie
  (pas de commit, pas de checkout, pas de reset).

## Versions

| Version | Date | Description |
|---|---|---|
| 0.1.3 | 2026-08-16 | Table REGLE_PROTOCOLE complete : SEUL CLIO -> protocole-verification-coherence (coherence README), LE MODELE DE CONFIANCE -> protocole-controle-statuts (second controle Janus) - les 8 regles IMMUABLE ont desormais toutes un protocole croise |
| 0.1.2 | 2026-08-16 | Audit COHERENCE REGLE/PROTOCOLE (--coherence) : croise chaque section ### X (IMMUABLE) de regles-groupes-agents.md avec son protocole associe (activation, nettoyage, tests, controle-buffy) - mots-mecanisme obligatoires par regle (c0/c0b/OUI/INCERTAIN/NON pour RELIRE, activation/execution/round pour RELEVE), flux OUI -> cible (omission c0c = REGLE_PROTOCOLE majeur), reference croisee regle->protocole (mineur). Preuve reelle : DETECTE l ecart RELIRE OUI -> mission vs protocole OUI -> c0c -> mission. Motivation : le controle croise Argus a decouvert cet ecart manuellement - on le mechanise |
| 0.1.1 | 2026-08-16 | Ameliorations (suite test de comportement Argus) : option --fichier pour auditer UN parcours arbitraire (resout le scan fixe) ; audit regles CROISE sur le contenu (CONTRADICTION_REGLE : SEUL vs PEUT/JAMAIS entre 2 fichiers differents, REGLE_DOUBLON) avec anti-faux-positif (tableaux/liens/lignes mixtes ignores, seuil durei) ; audit git enrichi (GIT_RESIDU_ACTUEL : residus presents a la racine) ; libelle des resultats = nom reel du fichier audite. Preuves : --fichier detecte REF_MORTE + CAS_ORPHELINE injectees, injection regles opposees detectee, etat reel = 2 residus reels signales, 0 faux positif regle |
| 0.1.0 | 2026-08-15 | Creation (mission Argus, etape 2/3) : audit cases (base detecter-cablages-manquants), audit regles (refs cassees, titres dupliques), audit git (lecture seule), rapport classe par gravite, options --tous/--cases/--regles/--git/--rapport/--verbose. Preuve negative reelle : REF_MORTE injectee detectee a 100% |
