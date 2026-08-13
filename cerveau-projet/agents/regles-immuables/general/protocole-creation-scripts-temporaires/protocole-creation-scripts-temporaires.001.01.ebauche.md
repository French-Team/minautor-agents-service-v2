---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Creation des Scripts Temporaires

**Version** : 0.2.1
**Statut** : ebauche
**Categorie** : General
**Agent** : Promethee
**Date** : 2026-08-13

Cadre l'utilisation des **scripts temporaires** par les agents : quand un
besoin ponctuel ne peut pas etre couvert par un outil existant, l'agent passe
par le generateur dedie, DECLARE sa creation au registre d'usage, et supprime
le script en fin de mission. Interdiction formelle des scripts jetables
poses a la racine du projet sans declaration.

---

## Objectif

Mettre fin a la regression constatee par l'utilisateur : les agents
preferaient les **scripts temporaires jetables** (`.zz-*.py` / `.tmp-*.py`
poses a la racine) a nos outils, au point que le registre d'usage restait a
0 ligne (les scripts ne passent pas par le generateur -> invisibles pour les
controles). Ce protocole ferme la boucle :

- **CREER** : uniquement via `generateurs-outil-temporaire` (jamais a la
  racine du projet sans passer par le generateur).
- **DECLARER** : toute creation est journalisee au registre
  (`enregistrer-usage-outil --mode script-temporaire`).
- **SUPPRIMER** : duree de vie courte, 0 residu en fin de mission.
- **PROMOUVOIR** : 2e utilisation -> outil durable (Vulcain).
- **DETECTER** : `detecter-usage-scripts-temporaires` croise les sources
  (racine, git, lecons) avec le registre -> ecart = anomalie.

## Prerequis

1. Les 3 outils de la chaine existent : `generateurs-outil-temporaire`,
   `enregistrer-usage-outil` (v0.2.0, mode script-temporaire),
   `detecter-usage-scripts-temporaires`.
2. Le garde-fou `test-024-scripts-temporaires` est vert (0 script a la
   racine).
3. L'agent a lu la documentation de l'outil avant de l'utiliser
   (protocole-outils).

## Etapes

1. **BESOIN** : l'agent identifie une operation ponctuelle non couverte par
   les outils existants.
2. **VERIFIER** : chercher dans le catalogue `generateurs-commande` si une
   commande existe (toujours privilegier l'outil existant).
3. **CREER** : si aucun outil ne couvre le besoin, utiliser
   `generateurs-outil-temporaire` (jamais un fichier ecrit a la main a la
   racine). Le script est cree dans le dossier indique par le generateur.
4. **DECLARER** : avant toute utilisation, journaliser au registre :
   `enregistrer-usage-outil --agent <moi> --outil <nom-script> --mode
   script-temporaire --contexte <raison>`. La declaration sert de preuve :
   un script trouve sans declaration est une anomalie.
5. **UTILISER** : executer le script pour l'operation ponctuelle.
6. **SUPPRIMER** : supprimer le script en fin de mission (0 residu). Le
   garde-fou test-024 verifie l'absence de `.zz-*` / `.tmp-*` a la racine.
7. **PROMOUVOIR** : si le besoin se reproduit (2e utilisation), activer
   **Vulcain** pour creer l'outil durable (protocole 5 fichiers) ; Vulcain
   reactive ensuite l'agent precedent qui reprend sa mission.
8. **CONTROLER** : Janus / Themis lancent `detecter-usage-scripts-temporaires`
   a chaque controle croise ; un ecart (script trouve non declare) est
   signale comme anomalie.

## RVAV

- L'outil utilise est present dans le catalogue (ou le script temporaire est
  declare au registre).
- Aucun fichier `.zz-*` / `.tmp-*` a la racine en fin de mission (test-024).
- `detecter-usage-scripts-temporaires` retourne `0` (aucun ecart).
- La promotion en outil durable est actee des la 2e utilisation.

## Exemples

**Exemple 1 - besoin ponctuel (valide)** :
```
Besoin : inserer 3 cases dans le parcours buffy (une seule fois).
1. Verifier : editer-parcours existe dans le catalogue -> l'utiliser.
   (aucun script temporaire necessaire)
```

**Exemple 2 - besoin non couvert (valide, avec declaration)** :
```
Besoin : analyser un format de fichier inedit (une seule fois).
1. Creer via generateurs-outil-temporaire (script dans le dossier dedie).
2. Declarer : enregistrer-usage-outil --mode script-temporaire.
3. Utiliser, puis supprimer (0 residu).
4. detecter-usage-scripts-temporaires : 0 ecart.
```

**Exemple 3 - interdiction (invalide)** :
```
.zz-analyse-format.py pose a la racine SANS declaration ni passage par le
generateur -> anomalie detectee par test-024 et detecter-usage-scripts-
temporaires.
```


## Commandes spawn_agents : eviter les erreurs d echappement JSON

### Regle d or

**TOUTE commande complexe passe par un script temporaire ecrit avec
write_file** -- jamais une commande inline imbriquee dans spawn_agents.

Le moteur spawn_agents transmet la commande dans un JSON : tout guillemet
imbrique, backslash, apostrophe dans un texte, chevron, pipe ou heredoc
dans la commande inline provoque une erreur de parsing JSON (dizaines
d erreurs `Invalid parameters for spawn_agents` observees sur les missions).
La methode fiable, eprouvee sur des dizaines de missions :

1. **ECRIRE** : `write_file` cree `.tmp-<agent>-<sujet>.py` (coding ascii,
   contenu libre, aucun probleme d echappement).
2. **EXECUTER** : `basher` avec une commande simple :
   `cd /z/analyste-in-console && python3 .tmp-xxx.py && rm -f .tmp-xxx.py`
   (la suppression est DANS la commande : 0 residu meme en cas de re-essai).
3. **VERIFIER** : `ls .tmp-*.py .zz-*` -> 0 residu attendu.

### Cas a risque (interdits en inline)

- Guillemets imbriques (quotes dans des commandes avec quotes).
- Backslashes multiples (regex, chemins Windows).
- Apostrophes dans des textes melanges aux quotes.
- Chevrons (`<`, `>`) : redirections, heredocs.
- Pipes et sous-commandes imbriquees (`$(...)`, boucles).
- Multi-commandes avec echappements JSON imbriques.

### Procedure valide

```
1. write_file : .tmp-morpheus-diag.py  (contenu Python libre, coding ascii)
2. basher : cd /z/analyste-in-console && python3 .tmp-morpheus-diag.py && rm -f .tmp-morpheus-diag.py
3. verification : ls .tmp-*.py .zz-*  (0 residu)
```

### Pieges connus

1. **test-024 auto-incrimination** : lancer test-024 depuis un script
   temporaire `.tmp-*.py` a la racine -> le garde-fou detecte le script qui
   le lance et casse (KO auto-inflige). TOUJOURS lancer test-024 en commande
   directe, jamais depuis un script temporaire.
2. **Residu en cas de timeout** : si le basher timeout avant le `rm -f`,
   nettoyer a la main avant de relancer (sinon test-024 KO).
3. **Ne pas lancer de test depuis un script temporaire** : tout test qui
   scanne la racine (test-024, detecter-usage-scripts-temporaires) se voit
   lui-meme -> toujours commande directe.

### Commandes bash des combos (meme regle, v0.2.1)

> **REGLE** : les commandes des combos (`combos-moteur`, definitions
> `definition-combo.json`) et du catalogue (`generateurs-commande`) suivent
> la MEME regle anti-echappement. L'interpolation `{var}` fait un
> remplacement BRUT puis `shlex.split` decoupe : toute valeur avec apostrophe
> non echappee casse la commande (`Commande invalide`). TOUJOURS quoter les
> variables dans les commandes (`--raison '{raison}'`), jamais les inserer
> brutes quand elles peuvent contenir apostrophe ou espace.

## Pieges courants

1. **Script a la racine** : interdiction formelle. Toujours passer par le
   generateur (qui journalise et valide le nommage).
2. **Oubli de declaration** : un script utilise sans declaration au registre
   apparait comme anomalie au controle croise.
3. **Residu non supprime** : test-024 casse la non-regression si un
   `.zz-*` / `.tmp-*` traine a la racine.
4. **Trou d'outil non remonte** : si le meme besoin revient 2 fois, ce n'est
   plus un besoin ponctuel -> promotion outil durable (Vulcain), ne pas
   reutiliser un script temporaire.
5. **Le registre ne capture que ce qui passe par le generateur** : c'est
   pourquoi la declaration manuelle (mode script-temporaire) est obligatoire
   pour les scripts crees par generateurs-outil-temporaire.

## Liens

- [generateurs-outil-temporaire](../../../tools/generateurs/generateurs-outil-temporaire/generateurs-outil-temporaire.md)
- [enregistrer-usage-outil](../../../tools/enregistrer/enregistrer-usage-outil/enregistrer-usage-outil.md)
- [detecter-usage-scripts-temporaires](../../../tools/detecter/detecter-usage-scripts-temporaires/detecter-usage-scripts-temporaires.md)
- [tester-lancer-non-regression](../../../tools/tester/tester-lancer-non-regression/tester-lancer-non-regression.md)
- [test-024-scripts-temporaires](../../../tools/tester/tests/test-024-scripts-temporaires/test-024-scripts-temporaires.py)
- [index-regles-general](index-regles-general.md)
