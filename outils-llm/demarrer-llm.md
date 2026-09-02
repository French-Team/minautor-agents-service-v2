# demarrer-llm -- DEMARRAGE EXCLUSIF DU LLM

> **Ni v1, ni v2.** Cet outil vit dans `outils-llm/` a la racine du projet,
> hors de `cerveau-projet/agents/` (v1) et hors de `cerveau-projet/freelance/` (v2).
> Il est exclusif au demarrage d'une session LLM : le LLM ne doit PLUS
> reflechir ni poser de question au demarrage -- il suit les ordres.

- **Version** : 0.1.2
- **Fichier** : `outils-llm/demarrer-llm.py`
- **Dependances** : Python stdlib uniquement (aucun import v1/v2)

---

## Pourquoi cet outil

Avant : `demarrer.md` pointait vers `guider-parcours` (outil V1) et le LLM
ne savait pas quoi faire : il posait des questions, perdait du temps, et en
session-freelance il ne pouvait pas utiliser les outils v1. De plus, 3
sources d'etat divergeaient (bloc session, table Sessions connues, classeur).

Apres : le LLM lit `demarrer.md` (ordre imperatif), l'utilisateur fournit
`id=<id>` + `session=<admin|freelance>`, et **l'outil fait tout le reste**.

---

## Utilisation

```bash
python3 outils-llm/demarrer-llm.py <id> <session>
```

| Argument | Valeur | Role |
|---|---|---|
| `<id>` | ex: glm5, freebuff | L'outil reconnait l'id (existe -> retrouve sa session ; inconnu -> le cree) |
| `<session>` | `admin` ou `freelance` | L'outil mene l'agent dans la bonne session |

Exemples :

```bash
python3 outils-llm/demarrer-llm.py glm5 admin       # session-admin (equipe v1)
python3 outils-llm/demarrer-llm.py freebuff freelance  # session-freelance (equipe v2)
```

Options : `--help` / `-h` (aide), `--version`.

---

## Ce que l'outil fait (transparent, dans l'ordre)

1. **Verifier/creer l'id** : appelle `activer-agent-principal sidentifier
   <id> <session>` (sous-processus) pour creer ou retrouver la liaison
   id <-> session (agent principal Cerberus).
2. **Determiner l'agent a incarner** :
   - `session-admin`    -> agent actif du bloc (ex: vulcain) ; Cerberus
     seulement si le bloc est vide/cerberus.
   - `session-freelance` -> **TOUJOURS Stark** (point d'entree, decision
     utilisateur 2026-08-26) : Stark est le coordinateur, il passe par
     JARVIS qui reprend le controle et rappelle les agents (ex: Vision
     pour finir sa mission) si besoin. JAMAIS l'agent du bloc directement.
   - En freelance, l'outil **active Stark dans le bloc session** (via
     activer-agent-principal activer) puis **lance la chaine de demarrage
     JARVIS** : `jarvis.py demarrage` (daemon routines + DEFCON + files +
     operationnel) pour que les serveurs tournent comme avant.
3. **Synchroniser les 3 sources** : bloc AGENTS.md + table Sessions connues
   + classeur variables. Si elles divergent, l'outil les aligne sur le bloc
   et le SIGNALE (le bloc est la source de verite).
4. **Historiser le demarrage** (3 destinations) : encart
   `AGENTS-activite-recente.md` (50 max), corps `AGENTS-historique.md`
   pour session-admin (v1, ASCII+LF) ; `AGENTS-activite-recente-v2.md` +
   `AGENTS-historique-v2.md` pour session-freelance (v2, UTF8+CRLF) -
   fichiers SEPARES par session (decision 2026-08-26)
   (100 max), BDD `historique.db` (7 jours).
5. **Afficher l'agent actif** : fiche, corrections, et le parcours/arbre a
   suivre (parcours JSON v1 pour un agent de `agents/`, arbre v2 pour un
   agent de `freelance/`).

---

## Resultat pour le LLM

```
=== RESULTAT DU DEMARRAGE ===
  Agent actif   : vision
  Session       : session-freelance
  ID LLM        : freebuff
  Fiche         : cerveau-projet/freelance/vision/vision.md
  Corrections   : cerveau-projet/freelance/vision/corrections.md
  PROCHAINES ETAPES :
  1. Relis TA fiche puis TES corrections
  2. Suis TON arbre de decisions :
     cerveau-projet/freelance/vision/parcours/arbre-vision.json
```

Le LLM arrive : **ACTIVE + HISTORISE + PARCOURS DEMARRE** -- sans question.

---

## Regles

- **Neutre** : l'outil n'importe AUCUN module v1 (`agents/`) ni v2
  (`freelance/`). Il appelle `activer-agent-principal` uniquement en
  sous-processus pour `sidentifier` (creation/retrouvaille de session).
- **ASCII strict + LF pur** : conventions du cerveau respectees.
- **Le bloc est la source de verite** : si table/classeur divergent, ils
  sont realignes sur le bloc et l'ecart est signale.
- **Jamais d'agent par defaut** : en session-freelance, l'agent incarne
  est celui du bloc (ex: vision), pas Stark/JARVIS systematiquement.

---

## Historique des versions

| Version | Date | Changement |
|---|---|---|
| 0.1.2 | 2026-09-02 | Reference parcours v1 : le repli v1 (branche elif parcours-<agent>.json affichant guider-parcours) est RETIRE - tous les agents ont un arbre v2 ; message de repli indique que les parcours v1 sont des archives marbre (decision utilisateur 2026-09-02, references v1) |
| 0.1.1 | 2026-08-26 | Point d'entree freelance = Stark (jamais l'agent du bloc) + lancement de la chaine de demarrage JARVIS (jarvis.py demarrage : daemon routines + DEFCON + files + operationnel) |
| 0.1.0 | 2026-08-26 | Creation (decision utilisateur : outil exclusif au demarrage, ni v1 ni v2, transparent) |
