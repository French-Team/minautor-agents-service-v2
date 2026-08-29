# redemarrer-session -- REDEMARRAGE D'UNE SESSION APRES BUG (DEFCON 5)

> **Ni v1, ni v2.** Cet outil vit dans `outils-llm/` a la racine du projet.
> Il redemarre une session SANS devoir la fermer d'abord, en reprenant la
> main sur le LLM apres un BUG.

- **Version** : 0.1.1
- **Fichier** : `outils-llm/redemarrer-session.py`
- **Dependances** : Python stdlib uniquement (aucun import v1/v2)

---

## Pourquoi cet outil

Si tu dois redemarrer une session, c'est que le flux est **surement
bugge** et que le **LLM a repris la main** (ce qui est un probleme). Ce
redemarrage sert a **reprendre la main sur le LLM**.

**Le piege a eviter** : si le redemarrage n'etait que la suite de la
session qui a mene au bug, on reviendrait dans la situation precedente.
C'est pourquoi cet outil **declenche DEFCON 5 (arret total)** : le flux
bugge est GELE et la reprise ne peut se faire que par un
**PROTOCOLE DE SECOURS** (diagnostic du bug, reparations, descente
DEFCON 5 -> 4 -> 3 -> 2 avec decision utilisateur a chaque etape).

## Ce que l'outil fait (transparent, dans l'ordre)

1. **Verifier/reparer les serveurs SANS fermer** : un serveur tombe de la
   session est relance par SA commande de demarrage (jamais besoin de
   `fermer-session` d'abord).
2. **Declarer DEFCON 5 (arret total)** avec la raison du bug :
   - v1 : `oracle.py defcon-declarer "<raison>"`
   - v2 : `jarvis.py stop-dev --raison "<raison>"`
3. **Reprendre la main sur le LLM** : l'agent actif de la session redevient
   le point d'entree (`cerberus` en v1, `stark` en v2) via
   `activer-agent-principal activer --forcer` (outrepasse le garde-fou de
   double activation : c'est le but d'une reprise apres bug). La raison
   d'activation ordonne explicitement : NE PAS reprendre le flux bugge,
   lancer le protocole de secours. **L'activation historise la reprise**
   (voie officielle, bon format, Etat DEBUT) : on n'ecrit JAMAIS en plus
   (ecriture maison = ancien format + doublon dans l'encart, bug signale
   par l'utilisateur).

## Utilisation

```bash
python3 outils-llm/redemarrer-session.py <id> <session> [--raison "<texte>"] [--dry-run]
```

| Argument | Valeur | Role |
|---|---|---|
| `<id>` | ex: glm5, freebuff | Id LLM de la session |
| `<session>` | `admin` ou `freelance` | `admin` = serveurs v1 + cerberus ; `freelance` = v2 + stark |
| `--raison` | texte | Raison du bug (audit) - defaut : reprise apres bug |
| `--dry-run` | option | Simule : etat seul, AUCUN effet |

Exemples :

```bash
python3 outils-llm/redemarrer-session.py glm5 admin
python3 outils-llm/redemarrer-session.py freebuff freelance --raison "flux casse, LLM a repris la main"
python3 outils-llm/redemarrer-session.py glm5 admin --dry-run
```

## Resultat

```
=== REDEMARRAGE TERMINE (reprise apres BUG) ===
  DEFCON 5 = ARRET TOTAL : le flux bugge est GELE.
  Le LLM ne doit PAS continuer la session precedente.

  PROTOCOLE DE SECOURS (reprise uniquement par ici) :
   1. Cerberus lance le DIAGNOSTIC du bug (jamais la suite du flux bugge).
   2. Reparations validees -> DEFCON 4 : oracle.py defcon-changer (v1) / jarvis.py defcon-changer (v2)
   3. Reprise surveillee   -> DEFCON 3
   4. Reprise totale       -> DEFCON 2
  Chaque descente de DEFCON exige la DECISION EXPLICITE de l'utilisateur.

  Reprise de session : outils-llm/demarrer-llm.py glm5 admin
```

## Regles

- **Neutre** : aucun import v1/v2 (appels en sous-processus uniquement).
- **Redemarre sans fermer** : les serveurs qui tournent restent en marche
  (aucune extinction) ; seuls ceux qui sont tombes sont relances.
- **DEFCON 5 systematique** : la reprise apres bug n'est JAMAIS une simple
  suite de session - le flux bugge est gele, le protocole de secours est
  obligatoire.
- **Reprise de main forcee** : `--forcer` sur l'activation (garde-fou
  outrepassable SEULEMENT par cette reprise de secours).
- **ASCII strict + LF pur** : conventions du cerveau respectees.
- **`--dry-run`** : etat seul, AUCUN effet (sans danger).

## Historique des versions

| Version | Date | Changement |
|---|---|---|
| 0.1.1 | 2026-08-29 | BUG FIX (utilisateur) : l'outil ecrivait sa propre ligne d'historisation avec l'ANCIEN format v1 (5 colonnes) + en DOUBLE (l'activation de cerberus/stark historise deja la reprise). Correction : suppression totale de l'historisation maison - la reprise est tracee par l'activation (voie officielle, colonne Etat DEBUT) + defcon.jsonl. Code mort supprime (helpers d'ecriture maison). |
| 0.1.0 | 2026-08-29 | Creation (decision utilisateur : redemarrer sans fermer, reprise apres bug avec DEFCON 5 + protocole de secours) |
