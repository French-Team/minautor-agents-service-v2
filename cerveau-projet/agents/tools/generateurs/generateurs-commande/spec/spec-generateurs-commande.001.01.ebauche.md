---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- generateurs-commande

**Statut :** ebauche
**Version :** 0.3.2
**Categorie :** generateurs
**Date :** 2026-08-07
**Historique :** v0.3.2 (GARDE-FOU REGISTRE : un agent 'inconnu' (resolution AGENTS.md impossible) n est JAMAIS journalise - analyser-noms-maj flaguerait AGENT_INCONNU et casserait la non-regression ; le --agent explicite reste prioritaire, 2026-09-02) -> v0.3.1 (MULTI-SESSIONS : _session_appelante lit SESSION_LLM puis le classeur-variables, plus de session-llm-1 figee -- chaque session journalise SON agent actif, 2026-08-19) -> v0.2.6 (booleens des combos : composer_commande accepte True/False, flag du modele gouverne, 2026-08-16) -> v0.2.4 (alignement spec/outil, round 11 coherence documentaire : version de la spec synchronisee avec la version de l outil 0.2.4) -> v0.2.2 (creation/derniere version documentee, 2026-08-07)

---

## Objectif

Fournir un generateur de commandes complexes utilise par TOUS les agents. L'agent ne compose plus lui-meme les commandes avec les bons parametres : il repond aux questions posees par l'outil (ou fournit les reponses en une fois), et l'outil compose et affiche la commande exacte a lancer, sans erreur de syntaxe ni parametre oublie.

**Principe fondateur** : chaque commande generee provient d'un modele deja ecrit, corrige et valide (`catalogue-commandes.json`), jamais d'une composition libre. L'outil ne reinvente jamais un appel d'outil.

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Catalogue | `catalogue-commandes.json` : chaque commande = modele + parametres (question, type, defaut, choix) |
| 2 | Liste | `--liste` : afficher les commandes disponibles (nom + description) |
| 3 | Choix interactif | Menu : selection par numero ou par nom |
| 4 | Questions | Une question par parametre (type texte, choix, flag oui/non) |
| 5 | Validation | Obligatoire, choix restreint, oui/non pour les flags |
| 6 | Composition | Modele rempli + echappement des valeurs (guillemets si espaces ou `quoter: true`) |
| 7 | Non-interactif | `--reponses 'cle=valeur;cle2=valeur2'` pour les tests et l'automatisation |
| 8 | Erreur obligatoire manquant | En mode `--reponses`, un parametre obligatoire absent = erreur immediate |
| 9 | Abandon EOF | En mode interactif, fin de l'entree standard = abandon propre (pas de boucle infinie) |
| 10 | Parite .py/.sh | Les deux versions lisent le meme catalogue et produisent la meme commande |

## Interface

```bash
python3 generateurs-commande.py [--liste] [--commande NOM] [--reponses 'a=b;c=d'] [OPTIONS]
bash generateurs-commande.sh [--liste] [--commande NOM] [--reponses 'a=b;c=d'] [OPTIONS]
```

Options : `--liste`, `--commande`, `--reponses`, `--catalogue`, `--dry-run`, `--verbose`, `--help`, `--version`.

## Format du catalogue

```json
{
  "nom": "activer-activer",
  "description": "Activer un agent principal dans une session LLM",
  "interpreteur": "python3",
  "script": "cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py",
  "modele": "activer {session} {agent} {raison}",
  "parametres": [
    { "cle": "session", "question": "Session LLM cible ?", "type": "texte", "obligatoire": true },
    { "cle": "agent", "question": "Agent a activer ?", "type": "choix", "choix": ["Cerberus", "Buffy", "Vulcain"], "obligatoire": true },
    { "cle": "raison", "question": "Raison de la mission ?", "type": "texte", "obligatoire": true, "quoter": true }
  ]
}
```

Types de parametres : `texte` (libre), `choix` (liste), `flag` (oui/non -> ajoute le flag ou rien), `quoter: true` (encapsule dans des guillemets).

## Tests requis

| Cas | Attendu |
|---|---|
| Liste | `--liste` affiche toutes les commandes du catalogue |
| Nominal interactif | Menu -> selection -> questions -> commande composee correcte |
| Nominal non-interactif | `--reponses` complete + valide -> commande composee correcte |
| Choix invalide | Valeur hors liste refusee, code retour 1 |
| Obligatoire manquant | En `--reponses` : erreur immediate, code retour 1 |
| Flag non | Le flag est absent de la commande |
| Flag oui | Le flag est present dans la commande |
| Quoting | Valeur avec espaces encapsulee entre guillemets |
| EOF | Entree standard epuisee -> abandon propre, pas de boucle infinie |
| Parite | `.py` et `.sh` produisent la meme commande pour le meme `--commande --reponses` |
| Nommage | valider-nommage OK (dossier generateurs/ -> prefixe generateurs-) |
| ASCII | 0 caractere non-ASCII |
| Syntaxe | bash -n OK, python3 -m py_compile OK |

## Livrables

- `generateurs-commande.sh` (bash)
- `generateurs-commande.py` (python)
- `catalogue-commandes.json` (source de verite)
- `generateurs-commande.md` (documentation)
- `spec/spec-generateurs-commande.001.01.ebauche.md` (ce fichier)
