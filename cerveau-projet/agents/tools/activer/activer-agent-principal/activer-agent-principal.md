# activer-agent-principal

**Categorie** : Activer
**Version** : 0.3.4
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Modifier AGENTS.md de maniere fiable et structuree, en supportant plusieurs sessions LLM en parallele.
Ecrit et met a jour automatiquement le profil de session (`profil-session-<session>`) dans le classeur-variables.

**Pourquoi cet outil ?**
- AGENTS.md est un fichier critique -- les erreurs cassent le cycle
- Plusieurs LLM peuvent travailler sur le meme projet : chacun a SON bloc dedie et SON agent principal
- Cet outil est concu SPECIFIQUEMENT pour AGENTS.md
- Il gere la structure et les formats automatiquement
- Il est fiable et teste

---

## Utilisation

Version Python (recommandee) :

```bash
python3 activer-agent-principal.py <action> [parametres]     # depuis le dossier de l'outil
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py <action> [parametres]   # depuis la racine du projet (FIABLE)
```

Version bash equivalente : `activer-agent-principal.sh` (meme logique).

> **FIABILITE** : utiliser le chemin complet depuis la racine du projet. Le nom nu `activer-agent-principal` ne fonctionne pas (pas dans le PATH).

**Session obligatoire** : toutes les actions (sauf `sidentifier` et `sessions`) prennent l'identifiant de session en premier argument.

**REGLE UTILISATEUR (identification)** : au demarrage, la section sessions de AGENTS.md est VIDE. Le 1er LLM qui devient Cerberus recoit `session-llm-1`. Tout LLM suivant recoit AUTOMATIQUEMENT la prochaine session libre (`session-llm-2`, `session-llm-3`...) -- un numero deja attribue n est JAMAIS repris. Appeler `sidentifier` SANS argument au demarrage : l'outil attribue la session correcte. Si une session est demandee explicitement alors qu'elle est deja attribuee, l'outil attribue la prochaine libre et l'affiche clairement.

Variable d'environnement pour les tests : `AGENTS_FILE` (surcharger le chemin de AGENTS.md) et `AGENTS_HISTORIQUE`.

---

## Actions disponibles

### 1. S'identifier (demarrage d'un LLM)

```bash
python3 activer-agent-principal.py sidentifier <llm-id>   # MODE ID (recommande)
python3 activer-agent-principal.py sidentifier            # compatibilite heritage
```

**MODE ID (RECOMMANDE)** : chaque LLM possede SON id (donne par l'utilisateur au lancement).
L'outil compare l'id aux sessions enregistrees dans le classeur :
- id deja lie -> retrouve SA session (redemarrage du meme LLM)
- id inconnu -> cree la prochaine session libre (llm-1, llm-2...) et LIE l'id a cette session

La liaison id <-> session est persistee dans le classeur (ligne `profil-session-<id>`
avec `id: <llm-id>` dans la valeur). Deux LLM differents ne partagent jamais une session.

**Fait :**
1. Sans argument : attribue le prochain `session-llm-N` libre (1er LLM -> `session-llm-1`)
2. Si la session demandee est deja attribuee : attribue AUTOMATIQUEMENT la prochaine libre avec un message clair
3. Cree le bloc de session s'il n'existe pas
4. Met Cerberus comme agent principal de la session (le LLM demarre comme Cerberus)
5. Affiche la session attribuee + ajoute l'entree dans l'historique

### 2. Activer un agent (dans sa session)

```bash
python3 activer-agent-principal.py activer session-llm-1 Buffy "Corriger les fichiers" "Mettre a jour demarrer.md"
```

**Fait :**
1. Lit AGENTS.md
2. Met a jour UNIQUEMENT le bloc "### Session : session-llm-1"
3. Ajoute l'entree dans l'historique (avec la session)
4. Ecrit le fichier

### 3. Reactiver Cerberus (dans sa session)

```bash
python3 activer-agent-principal.py reactiver session-llm-1 "Mission terminee" Buffy
```

**Fait :**
1. Lit agents/cerberus/cerberus.md
2. Lit AGENTS.md
3. Met a jour UNIQUEMENT le bloc "### Session : session-llm-1" avec "Nom: Cerberus"
4. Ajoute l'entree dans l'historique
5. Ecrit le fichier

### 4. Lister les sessions

```bash
python3 activer-agent-principal.py sessions
```

Affiche chaque session et son agent principal actuel.

---

## Format de sortie

### Section "Sessions LLM" (multi-session)

```markdown
## Sessions LLM

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom** | [agent] |
| **Role** | [role de l'agent] |
| **Derniere mise a jour** | [date] |
| **Fiche** | [lien] |
| **Corrections** | [lien] |
| **Active par** | [agent precedent] |
| **Raison** | [raison] |

### Session : session-llm-2

| Champ | Valeur |
|---|---|
...
```

Chaque session LLM possede son propre bloc et son propre agent principal. L'outil ne modifie JAMAIS le bloc d'une autre session.

### Migration automatique

Si AGENTS.md contient encore l'ancienne section "## Agent Principal Actuel" (mono-session), le premier appel convertit automatiquement vers "## Sessions LLM" avec le bloc "### Session : session-llm-1" en conservant les valeurs actuelles.

### Historique (AGENTS-historique.md)

```
| [date et heure] | [session] | [agent] | [raison] |
```

La colonne session identifie quel LLM a effectue l'action.

**Format de l'horodatage** : `YYYY-MM-DD HH:MM` (date + heure precise)

**Regles de l'historique** :
- **Heure incluse** : chaque entree porte la date ET l'heure (HH:MM) pour situer precisement les groupes d'interventions
- **Ordre decroissant** : les entrees les plus recentes sont en HAUT du tableau
- **Limite 150** : le fichier ne conserve que les 150 interventions les plus recentes (les plus anciennes sont retirees automatiquement)

---

## Ce que fait cet outil

| Capacite | Description |
|---|---|
| Multi-session | Un bloc dedie par LLM (session-llm-N), agent principal isole par session |
| sidentifier | Attribution automatique du prochain session-llm-N libre au demarrage |
| Session obligatoire | Aucune activation sans session -- les sessions sont isolees |
| Migration | Convertit automatiquement l'ancienne structure mono-session |
| Specifique a AGENTS.md | Concu pour ce fichier critique |
| Gere le format | La structure est maintenue automatiquement |
| Lit cerberus.md | Lit le fichier de Cerberus pour la reactivation |
| Valide le resultat | Verifie que la modification est correcte |
| Fiable et teste | Fonctionne a chaque fois |
| Horodatage HH:MM | Date + heure precise dans l'historique |
| Colonne session | L'historique global identifie la session dans chaque entree |
| Ordre decroissant | Les plus recentes en haut |
| Limite 150 | Tronque automatiquement a 150 entrees |
| Verification ASCII | Refuse toute raison contenant un caractere non-ASCII (lecon permanente 2026-08-07) |
| Profil session classeur | Ecrit/met a jour `profil-session-<id>` (regle de derivation : partie apres `session-`) dans le classeur-variables a chaque sidentifier/activer/reactiver |

---

## Exemple complet

### Demarrage d'un LLM (identification)

```
1. Appeler activer-agent-principal.py sidentifier
2. L'outil attribue session-llm-N (ou le nom fourni)
3. Le bloc de session est cree avec Cerberus comme agent principal
4. Le LLM utilise sa session pour toutes ses activations
```

### Cycle dans une session

```
1. Appeler activer-agent-principal.py activer session-llm-1 <agent> "<mission>"
2. L'agent execute sa mission
3. Appeler activer-agent-principal.py reactiver session-llm-1 "Mission terminee" <agent>
4. Cerberus reprend dans la session
```

---

## Dependances

- `AGENTS.md` -- fichier a modifier
- `agents/cerberus/cerberus.md` -- lu lors de la reactivation
- Variable d'environnement `AGENTS_FILE` / `AGENTS_HISTORIQUE` (tests sur copies)
- `classeur-variables/stockage/variables-actuelles.md` -- profil de session (ecrit a chaque action)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0-beta | 2026-08-06 | Historique : horodatage HH:MM + ordre decroissant + limite 150 |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels avec protections (activation, reactivation, limite 150, ordre decroissant), VERSION ajoutee au script, promotion prepare |
| 0.2.1 | 2026-08-07 | Lecon permanente ASCII : verifier_ascii() avant toute ecriture (raison non-ASCII REFUSEE) + verifier_fichier_ascii() post-ecriture (WARNING si corruption pre-existante). Cause racine : caractere U+00E9 corrompu trouve dans AGENTS-historique.md lors de l'audit general |
| 0.2.0-py | 2026-08-07 | Version Python creee (activer-agent-principal.py), basee sur outil-template.py. Portage fidele : actions activer/reactiver, historique HH:MM decroissant limite 150, verification ASCII avant ecriture |
| 0.3.0 | 2026-08-07 | MULTI-SESSION LLM : nouvelle action sidentifier (attribution session-llm-N + Cerberus par defaut), action sessions (lister), session OBLIGATOIRE dans activer/reactiver, structure AGENTS.md en blocs ### Session : <id> isoles (un agent principal par LLM), migration automatique de l'ancienne structure mono-session, historique 4 colonnes (date, session, agent, raison), champs Fiche/Corrections suivis par agent actif, Themis ajoute aux roles, surcharge AGENTS_FILE/AGENTS_HISTORIQUE par variables d'environnement pour les tests |
| 0.3.1 | 2026-08-07 | PROFIL SESSION CLASSEUR : nouvelle fonction mettre_a_jour_profil_session (py + sh) ecrit/met a jour la variable `profil-session-<session>` dans classeur-variables/stockage/variables-actuelles.md a chaque sidentifier (Cerberus), activer (agent) et reactiver (Cerberus). Ligne existante -> mise a jour ; ligne absente -> ajoutee a la fin du tableau. Surcharge CLASSEUR_STOCKAGE pour les tests |
| 0.3.2 | 2026-08-07 | REGLE DE DERIVATION (correction Janus A REVOIR) : id de la variable = profil-session- + partie apres le prefixe session- du nom complet (session-llm-1 -> profil-session-llm-1). Le prefixe profil-session-session-* est INTERDIT. Correction py + sh + spec + doc
| 0.3.3 | 2026-08-07 | REGLE UTILISATEUR (identification) : au demarrage la section sessions est VIDE, le 1er LLM devient session-llm-1. Si une session demandee est deja attribuee, attribution AUTOMATIQUE de la prochaine libre avec message clair (jamais de reprise d'un numero attribue). Correction sidentifier py + sh
| 0.3.4 | 2026-08-07 | MODE ID : sidentifier <llm-id> compare l'id aux sessions enregistrees (classeur) - id connu = SA session, id inconnu = creation prochaine libre + liaison id dans la ligne profil-session. Chaque LLM a SON id, jamais de partage de session |
| Renommage | 2026-08-07 | Deplacement dans le dossier activer/ + renommage de mettre-a-jour-agents-md vers activer-agent-principal (l outil sert a activer/reactiver l agent principal dans AGENTS.md). ~120 references mises a jour dans 31 fichiers + spec + boucle retro-action |

---

## Notes

- Cet outil est CRITIQUE -- il gere le fichier le plus important
- La reactivation lit cerberus.md (pas corrections.md sauf en cas d'erreur)
- Chaque erreur ici casse tout le cycle

---
