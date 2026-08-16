---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole Argus -- Detection et Signalement des Contradictions

**Version** : 0.1.0
**Statut** : ebauche
**Categorie** : General
**Agent** : Argus (detecteur de contradictions)
**Date** : 2026-08-16

Cadre la facon dont Argus DETECTE et SIGNALE les contradictions (cases des
parcours, regles et protocoles, historique git). Il ne corrige JAMAIS : il
signale, l'agent habilite corrige.

---

## Objectif

Garantir qu'aucune incoherence signalee n'est un faux positif : chaque
signalement porte OBLIGATOIREMENT 4 elements (type, gravite, fichier+ligne,
2 sources croisees) et le cycle signalement -> correction est materialise
(rapport en preuve + activation de l'agent habilite).

**Pourquoi ce protocole ?**
- Argus a ete cree (2026-08-15) pour reperer les contradictions accumulees
  depuis le debut du projet (regles, protocoles, cases en conflit).
- Son premier test reel (2026-08-16) a revele que l'outil ne couvrait qu'une
  fraction de la mission ; le re-test v0.1.1 confirme l'outil fonctionnel.
- Sans protocole de signalement, le risque est double : signaler des faux
  positifs (le cout du temps des agents correcteurs) ou ne rien signaler
  (les contradictions restent cachees).

---

## Regles detaillees

### R1. Les 4 elements OBLIGATOIRES d'un signalement

Chaque incoherence signalee porte obligatoirement :

| Element | Contenu | Exemple |
|---|---|---|
| 1. Type | Le type de contradiction (code de l'outil) | `REF_MORTE`, `CONTRADICTION_REGLE`, `GIT_RESIDU_ACTUEL` |
| 2. Gravite | critique / majeur / mineur | majeur |
| 3. Fichier + ligne | La preuve de localisation | `regles-groupes-agents.md:100` |
| 4. 2 sources croisees | Les 2 sources qui confirment l'incoherence (regle DOUBLE SOURCE) | parcours JSON + regle immuable ; fiche + registre ; git log + fichier actuel |

Sans ces 4 elements, l'incoherence n'est PAS signalee (anti-faux-positif).

### R2. JE DETECTE, JE NE CORRIGE PAS

Argus detecte et signale. La correction appartient a l'agent habilite selon
le type d'incoherence :

| Type d'incoherence | Agent habilite |
|---|---|
| Fiches, parcours, regles, protocoles | Buffy |
| Outils | Vulcain |
| Tests | Morpheus |
| Residus / workspace | Hygie |

### R3. Les cas types (choix d'audit)

| Cas | Commande | Verdict attendu |
|---|---|---|
| Parcours JSON (tous) | `detecter-contradictions.py --cases` | PROPRE ou liste |
| Parcours JSON (un seul, copie, preuve) | `detecter-contradictions.py --fichier <chemin>` | liste ou PROPRE |
| Regles et protocoles (structure + contenu croise) | `detecter-contradictions.py --regles` | PROPRE ou liste |
| Git (log + residus actuels) | `detecter-contradictions.py --git` | PROPRE ou liste |
| Tous les audits | `detecter-contradictions.py --tous` | PROPRE ou liste |

### R4. La preuve negative quand 0 contradiction mais soupcon

Si un audit retourne PROPRE (0 contradiction) MAIS qu'un soupcon existe
(une incoherence est suspectee sur une source), Argus ne conclut PAS
"rien a signaler" sans preuve : il cree une COPIE du fichier suspect sous
`tmp-argus/`, y injecte la contradiction suspectee, lance
`--fichier <copie>` et verifie que l'outil la detecte. La preuve valide
(ou infirme) le soupcon. Un verdict PROPRE sans preuve negative quand il y
a soupcon est un signalement incomplet.

### R5. Le cycle signalement -> correction

1. Argus lance l'audit (R3).
2. Si contradiction(s) : verifier les 4 elements (R1), verifier dans
   2 sources (R4/R1.4), classer par gravite.
3. Rediger le rapport d'incoherences (preuves = fichiers + lignes +
   2 sources croisees).
4. Activer l'agent habilite selon R2 avec le rapport en preuve.
5. A la reactivation, verifier le rapport de l'agent (controle croise).
6. Reactiver Cerberus avec le bilan.

---

## Application

Argus applique ce protocole a CHAQUE mission de detection, en suivant son
parcours case par case (la case c7 reference ce protocole pour le rapport,
la case c30 applique la preuve negative R4 avant de conclure).

---

## Liens

- [index-regles-general.md](../index-regles-general.md)
- [fiche argus](../../../../agents/argus/argus.md)
- [detecter-contradictions](../../../../agents/tools/detecter/detecter-contradictions/detecter-contradictions.md)
- [regles-groupes-agents.md](../regles-groupes-agents.md)
