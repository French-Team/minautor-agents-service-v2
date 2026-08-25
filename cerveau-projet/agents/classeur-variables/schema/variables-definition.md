---
identite:
  type: classeur
  appartient_a: commun
  commun: true
---
# Schema -- Definition des Variables
---

## Variables

### Variable : profil-systeme

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant : profil-systeme |
| `os` | string | [OK] | Systeme d'exploitation (ex: Windows 10) |
| `bash` | string | [OK] | Bash disponible et version, ou "absent" |
| `python` | string | [OK] | Python disponible et version, ou "absent" |
| `node` | string | [NON] | Node.js disponible et version, ou "absent" |
| `git` | string | [OK] | Git disponible et version, ou "absent" |
| `source` | string | [OK] | Outil qui a ecrit : verifier-systeme |
| `date_maj` | datetime | [OK] | Date de derniere mise a jour du profil |

> **Usage** : ce profil est consulte par les agents pour choisir la version d'un outil
> (`.py` si Python dispo, sinon `.sh`). Voir `protocole-technologies`.

### Variable : profil-session (une par session)

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant : profil-session-<session-id> (ex: profil-session-admin) |
| `session` | string | [OK] | Nom complet de session (ex: session-admin) |
| `agent_principal` | string | [OK] | Agent principal actuel de la session |
| `date_identification` | datetime | [OK] | Date de derniere identification/activation |
| `source` | string | [OK] | Outil qui a ecrit : activer-agent-principal |
| `date_maj` | datetime | [OK] | Date de derniere mise a jour |

> **Usage** : une variable PAR session LLM.
> **REGLE DE DERIVATION (IMMUABLE)**: l'id de la variable = `profil-session-` + la partie du nom complet de session APRES le prefixe `session-`.
> Exemple : session `session-admin` -> id `profil-session-admin` ; session `session-freelance` -> id `profil-session-freelance`.
> NE JAMAIS concatener `profil-session-` avec le nom complet (`profil-session-session-admin` est INTERDIT).
> Elle est ecrite et mise a jour automatiquement par `activer-agent-principal`
> a chaque sidentifier/activer/reactiver. Permet a chaque LLM de connaitre
> SA session et SON agent principal depuis le classeur.

Pour ajouter une variable, utiliser le template suivant :

```markdown
## Variable : [nom-variable]

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant unique |
| `valeur` | any | [OK] | Valeur de la variable |
| `source` | string | [OK] | Fonction qui a ecrit la variable |
| `date_creation` | datetime | [OK] | Date de creation |
| `date_modification` | datetime | [NON] | Date de derniere modification |
| `description` | string | [NON] | Description de la variable |
```

---

## Types autorises

| Type | Description | Exemple |
|---|---|---|
| `string` | Texte | `"hello"` |
| `number` | Nombre | `42` |
| `boolean` | Booleen | `true` |
| `objet` | Objet JSON | `{"cle": "valeur"}` |
| `array` | Tableau | `[1, 2, 3]` |
| `null` | Valeur nulle | `null` |

---

## Navigation

- **Parent** : [index-classeur.md](../index-classeur.md)
- **Stockage** : [stockage/variables-actuelles.md](../stockage/variables-actuelles.md)
- **Historique** : [historique/historique-modifications.md](../historique/historique-modifications.md)
