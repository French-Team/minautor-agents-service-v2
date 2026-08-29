# fermer-session -- FERMETURE EXCLUSIVE D'UNE SESSION LLM

> **Ni v1, ni v2.** Cet outil vit dans `outils-llm/` a la racine du projet,
> hors de `cerveau-projet/agents/` (v1) et hors de `cerveau-projet/freelance/` (v2).
> Il ferme une session LLM : arrete les serveurs de la session PROPRement
> et VERIFIE qu'ils sont bien fermes.

- **Version** : 0.1.1
- **Fichier** : `outils-llm/fermer-session.py`
- **Dependances** : Python stdlib uniquement (aucun import v1/v2)

---

## Pourquoi cet outil

`demarrer-llm.py` demarre une session et lance les serveurs. Il manquait
l'operation inverse : fermer la session en eteignant les serveurs
proprement, avec VERIFICATION qu'ils sont bien arretes (pas de processus
fantome qui traine). L'arret doit etre propre : chaque serveur est arrete
par SA commande d'arret officielle, puis verifie (pidfile supprime +
processus non vivant). Si un serveur refuse de mourir, l'outil force et
re-verifie.

## Quel serveur pour quelle session

| Session | Serveurs eteints | Commande d'arret officielle |
|---|---|---|
| `admin` (v1) | oracle-server + routines-server v1 | `oracle-demarrage.py arret` |
| `freelance` (v2) | daemon routines JARVIS | `jarvis.py arret` |

## Utilisation

```bash
python3 outils-llm/fermer-session.py <id> <session> [--dry-run]
```

| Argument | Valeur | Role |
|---|---|---|
| `<id>` | ex: glm5, freebuff | Id LLM de la session a fermer (historise) |
| `<session>` | `admin` ou `freelance` | `admin` = serveurs v1 ; `freelance` = serveurs v2 |
| `--dry-run` | option | Simule : affiche l'etat des serveurs SANS rien arreter |

Exemples :

```bash
python3 outils-llm/fermer-session.py glm5 admin            # v1 : oracle + routines
python3 outils-llm/fermer-session.py freebuff freelance    # v2 : daemon JARVIS
python3 outils-llm/fermer-session.py glm5 admin --dry-run  # etat seul, rien n'est arrete
```

Options : `--help` / `-h` (aide), `--version`.

## Ce que l'outil fait (transparent, dans l'ordre)

1. **Identifier les serveurs de la session** (pidfiles + pids actuels).
2. **Arret propre** via la commande d'arret officielle :
   - v1 : `oracle-demarrage.py arret --confirme-doc` (oracle-server +
     routines-server v1, pidfiles supprimes par la commande).
   - v2 : `jarvis.py arret --session session-freelance` (daemon routines
     JARVIS : resume de session + arret du daemon).
3. **VERIFIER chaque serveur** : pidfile absent/assaini ET processus non
   vivant (sonde OpenProcess, Windows-safe - ne TERMINE pas).
4. **Force si besoin** : SIGTERM puis `taskkill /F`, re-verification.
5. **Historiser UNIQUEMENT en cas d'arret force** : en arret propre, c'est
   `oracle-demarrage` (v1) / `jarvis` (v2) qui historisent DEJA leur arret
   (voie officielle) - ecrire en plus creerait un DOUBLON dans l'encart.
   En arret force, l'historisation passe par la voie OFFICIELLE de la
   session (`oracle.py historiser systeme ...` v1 / `jarvis.py historiser
   --agent systeme ...` v2) : jamais d'ecriture maison, l'encart garde
   SON format et sa colonne Etat.
6. **Afficher le verdict** : un serveur encore actif -> code 1 (session
   NON fermee proprement) ; tous arretes -> code 0.

## Resultat

```
=== VERIFICATION (serveurs bien fermes ?) ===
  oracle-server            : ARRETE        (pid 15376 arrete, pidfile nettoye)
  routines-server v1       : ARRETE        (pid 17768 arrete, pidfile nettoye)
=== FERMETURE TERMINEE : serveurs eteints et verifies ===
  La session est recoverable par : outils-llm/demarrer-llm.py glm5 admin
```

## Regles

- **Neutre** : l'outil n'importe AUCUN module v1 ni v2 (appels en
  sous-processus uniquement, comme demarrer-llm).
- **ASCII strict + LF pur** : conventions du cerveau respectees.
- **Arret propre d'abord, force en dernier recours** : chaque serveur passe
  par SA commande d'arret officielle avant toute action forcee.
- **Verification obligatoire** : un serveur n'est declare ferme que si
  pidfile supprime ET processus non vivant. Jamais de supposition.
- **`--dry-run`** : etat des serveurs seul, AUCUN arret (sans effet).

## Historique des versions

| Version | Date | Changement |
|---|---|---|
| 0.1.1 | 2026-08-29 | BUG FIX (utilisateur) : l'outil ecrivait dans l'encart avec l'ANCIEN format v1 (5 colonnes `| Heure | Agent | id | Type | Raison |`) -> la routine encart hurlait 'Etat inconnu R' ; et il ecrivait EN DOUBLE (oracle-demarrage/jarvis historisent deja leur arret propre). Correction : plus AUCUNE ecriture maison - en arret propre on ne re-ecrit pas (pas de doublon), en arret force on passe par la voie officielle (`oracle.py historiser` / `jarvis.py historiser`, bon format + Etat). Code mort supprime (helpers d'ecriture maison). |
| 0.1.0 | 2026-08-29 | Creation (decision utilisateur : fermer la session et eteindre les serveurs proprement avec verification) |
