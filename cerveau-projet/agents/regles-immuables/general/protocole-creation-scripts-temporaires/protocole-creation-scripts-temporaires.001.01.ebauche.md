---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Creation des Scripts Temporaires

**Version** : 0.2.11
**Statut** : ebauche
**Categorie** : General
**Agent** : Promethee
**Date** : 2026-08-13

Cadre l'utilisation des **scripts temporaires** par les agents : l agent cree
SON dossier temporaire a la racine du projet (`tmp-<agent>/`), ecrit ses
scripts jetables dedans, puis **SUPPRIME LE DOSSIER ENTIER en fin de mission**
(`rm -rf tmp-<agent>`). C est la **REGLE D ORIGINE** (restauree en v0.2.4,
demande utilisateur) : le dossier temporaire n existe QUE pendant la mission -
0 dossier `tmp-*` residuel a la racine apres la mission, 0 script eparpille a
la racine.

---

## Objectif

Mettre fin a la regression constatee par l'utilisateur : les agents
preferaient les **scripts temporaires jetables** (`.zz-*.py` / `.tmp-*.py`
poses a la racine) a nos outils, au point que le registre d'usage restait a
0 ligne (les scripts ne passent pas par le generateur -> invisibles pour les
controles). Ce protocole ferme la boucle :

- **CREER** : l agent cree SON dossier temporaire a la racine (`tmp-<agent>/`) ;
  jamais de script eparpille a la racine.
- **DECLARER** : toute creation d OUTIL TEMPORAIRE DE MISSION est journalisee
  au registre (`enregistrer-usage-outil --mode script-temporaire`).
- **SUPPRIMER** : le dossier temporaire est SUPPRIME EN FIN DE MISSION
  (`rm -rf tmp-<agent>`) : 0 residu, 0 dossier.
- **PROMOUVOIR** : 2e utilisation -> outil durable (Vulcain).
- **DETECTER** : `detecter-usage-scripts-temporaires` croise les sources
  (racine, git, lecons) avec le registre -> ecart = anomalie.

## Prerequis

1. Les 3 outils de la chaine existent : `generateurs-outil-temporaire`,
   `enregistrer-usage-outil` (v0.2.0, mode script-temporaire),
   `detecter-usage-scripts-temporaires`.
2. Le garde-fou `test-024-scripts-temporaires` est vert (0 script eparpille
   a la racine) et le garde-fou des dossiers residuels est vert (0 dossier
   `tmp-*` hors dossier de l agent courant).
3. L'agent a lu la documentation de l'outil avant de l'utiliser
   (protocole-outils).

## Le dossier temporaire de mission (regle d origine)

> **REGLE D ORIGINE (v0.2.4, demande utilisateur)** : chaque agent cree SON
> dossier temporaire a la racine du projet : `tmp-<agent>/` (ex: `tmp-buffy/`,
> `tmp-janus/`, `tmp-morpheus/`). Le nom SANS point est important : test-024
> ne detecte que les entrees commencant par `.tmp-` / `.zz-` (scripts jetables
> eparpilles) ; le dossier `tmp-<agent>` est invisible pour ce scan mais
> surveille par le garde-fou des dossiers residuels (aucun dossier `tmp-*`
> hors dossier de l agent courant - lu depuis le profil classeur).

| Etape | Action | Quand |
|---|---|---|
| **CREER** | `mkdir tmp-<agent>` (ou write_file cree le dossier au besoin) | Des le premier script de la mission |
| **ECRIRE** | `write_file` -> `tmp-<agent>/<script>.py` | Chaque script jetable |
| **EXECUTER** | **ENTONNOIR** : `python3 cerveau-projet/agents/tools/executer/executer-script-temporaire/executer-script-temporaire.py tmp-<agent>/<script>.py` (normalise + controle + execute ; puis `rm -f` du script dans la meme commande si jetable) | Diagnostic ponctuel |
| **SUPPRIMER** | `rm -rf tmp-<agent>` | **EN FIN DE MISSION** - avant de reactiver l agent suivant |

## Journalisation et redirections de sortie (v0.2.11, demande utilisateur 2026-08-16)

> **REGLE (anti-recurrence constat utilisateur)** : le dossier `tmp-<agent>/`
> est le SEUL endroit ou ecrire pendant une mission - y compris pour les
> JOURNAUX et les captures de sortie. Toute redirection d ecriture
> (`> fichier.log`, `2>&1 | tee`, captures de sortie) va dans
> `tmp-<agent>/<fichier>.log`, JAMAIS vers le `/tmp` du systeme ni aucun
> autre emplacement hors du workspace.
>
> - **AUTORISE** : `python3 outil.py ... > tmp-janus/nr.log 2>&1` (le journal
>   vit dans le dossier temporaire de mission, supprime avec lui).
> - **INTERDIT** : `> /tmp/nr.log`, `/tmp/ascii-out.txt`, tout fichier ecrit
>   dans le `/tmp` systeme : c est ecrire HORS du workspace, invisible pour
>   les garde-fous et laisse une trace hors projet.
>
> Le dossier `tmp-<agent>/` est supprime en fin de mission (`rm -rf
> tmp-<agent>`) : le journal disparait avec lui, 0 residu.

## Etapes

1. **BESOIN** : l'agent identifie une operation ponctuelle non couverte par
   les outils existants.
2. **VERIFIER** : chercher dans le catalogue `generateurs-commande` si une
   commande existe (toujours privilegier l'outil existant).
3. **CREER** : si aucun outil ne couvre le besoin, creer SON dossier
   temporaire `tmp-<agent>/` a la racine et y ecrire le script jetable
   (`write_file` -> `tmp-<agent>/<script>.py`). Jamais de script eparpille
   a la racine.
4. **DECLARER** : TOUT script temporaire de mission est journalise au
   registre : `enregistrer-usage-outil --agent <moi> --outil <nom-script>
   --mode script-temporaire --contexte <raison>` (le script lui-meme), puis
   CHAQUE outil utilise pendant la mission est declare egalement. Le
   squelette genere par `generateurs-outil-temporaire` v0.2.1 embarque ce
   bloc (variable AGENT + `declarer_usages()` en fin de main) : renseigner
   AGENT et completer les appels par outil. Les scripts jetables ephemeres
   (executes et supprimes dans la meme commande) ne sont pas declares.
5. **UTILISER** : executer le script par l **ENTONNOIR**
   (`executer-script-temporaire`) : normalisation automatique (BOM, CRLF,
   accents), controle de compilation systematique, execution transparente.
   L agent n a pas a verifier la conformite de son script : l entonnoir
   normalise avant d executer (et signale toute erreur de syntaxe AVANT
   execution).
6. **SUPPRIMER** : en fin de mission, SUPPRIMER LE DOSSIER ENTIER :
   `rm -rf tmp-<agent>` (0 residu, 0 dossier). Le garde-fou test-024 verifie
   l'absence de `.zz-*` / `.tmp-*` eparpilles a la racine et le garde-fou
   des dossiers residuels verifie l'absence de dossier `tmp-*` (hors dossier
   de l agent courant).
7. **PROMOUVOIR** : si le besoin se reproduit (2e utilisation), activer
   **Vulcain** pour creer l'outil durable (protocole 5 fichiers) ; Vulcain
   reactive ensuite l'agent precedent qui reprend sa mission.
8. **CONTROLER** : Janus / Themis lancent `detecter-usage-scripts-temporaires`
   a chaque controle croise ; un ecart (script trouve non declare) est
   signale comme anomalie.

## RVAV

- L'outil utilise est present dans le catalogue (ou le script temporaire est
  declare au registre).
- Aucun fichier `.zz-*` / `.tmp-*` eparpille a la racine en fin de mission
  (test-024).
- Aucun dossier `tmp-*` a la racine en fin de mission (dossier temporaire
  supprime - garde-fou des dossiers residuels).
- `detecter-usage-scripts-temporaires` retourne `0` (aucun ecart).
- La promotion en outil durable est actee des la 2e utilisation.
- Aucun journal / redirection de sortie vers le `/tmp` systeme : toute
  capture de sortie est dans `tmp-<agent>/` (regle v0.2.11).

## Exemples

**Exemple 1 - besoin ponctuel (valide)** :
```
Besoin : inserer 3 cases dans le parcours buffy (une seule fois).
1. Verifier : editer-parcours existe dans le catalogue -> l'utiliser.
   (aucun script temporaire necessaire)
```

**Exemple 2 - besoin non couvert (valide, script jetable)** :
```
Besoin : analyser un format de fichier inedit (une seule fois).
1. mkdir tmp-buffy (dossier temporaire de mission).
2. write_file : tmp-buffy/analyse-format.py.
3. python3 tmp-buffy/analyse-format.py && rm -f tmp-buffy/analyse-format.py.
4. En fin de mission : rm -rf tmp-buffy (0 dossier residuel).
```

**Exemple 3 - interdiction (invalide)** :
```
.zz-analyse-format.py pose a la racine SANS dossier ni declaration ->
anomalie detectee par test-024 et detecter-usage-scripts-temporaires.
tmp-buffy laisse a la racine en fin de mission (dossier non supprime) ->
anomalie detectee par le garde-fou des dossiers residuels.
```

## Commandes spawn_agents : eviter les erreurs d echappement JSON

### Regle d or

**TOUTE commande complexe passe par un script temporaire dans `tmp-<agent>/`
ecrit avec write_file** -- jamais une commande inline imbriquee dans
spawn_agents.

Le moteur spawn_agents transmet la commande dans un JSON : tout guillemet
imbrique, backslash, apostrophe dans un texte, chevron, pipe ou heredoc
dans la commande inline provoque une erreur de parsing JSON (dizaines
d erreurs `Invalid parameters for spawn_agents` observees sur les missions).
La methode fiable, eprouvee sur des dizaines de missions :

1. **CREER** : `mkdir tmp-<agent>` (ou write_file cree le dossier au besoin).
2. **ECRIRE** : `write_file` cree `tmp-<agent>/<sujet>.py` (coding ascii,
   contenu libre, aucun probleme d echappement).
3. **EXECUTER** : `basher` avec une commande simple :
   `cd /z/analyste-in-console && python3 tmp-<agent>/<sujet>.py && rm -f tmp-<agent>/<sujet>.py`
   (la suppression du script est DANS la commande : 0 residu meme en cas de
   re-essai).
4. **VERIFIER** : en fin de mission, `rm -rf tmp-<agent>` : 0 dossier
   residuel, 0 script a la racine.

### Cas a risque (interdits en inline)

- Guillemets imbriques (quotes dans des commandes avec quotes).
- Backslashes multiples (regex, chemins Windows).
- Apostrophes dans des textes melanges aux quotes.
- Chevrons (`<`, `>`) : redirections, heredocs.
- Pipes et sous-commandes imbriquees (`$(...)`, boucles).
- Multi-commandes avec echappements JSON imbriques.

### Procedure valide

```
1. mkdir tmp-morpheus
2. write_file : tmp-morpheus/diag.py  (contenu Python libre, coding ascii)
3. basher : cd /z/analyste-in-console && python3 tmp-morpheus/diag.py && rm -f tmp-morpheus/diag.py
4. en fin de mission : rm -rf tmp-morpheus (0 dossier residuel)
```

### Pieges connus

1. **test-024 et tmp-<agent>** : test-024 ne detecte que les scripts
   `.tmp-*` / `.zz-*` eparpilles a la racine. Les scripts DANS `tmp-<agent>/`
   sont invisibles pour lui. Le dossier `tmp-<agent>` est surveille par le
   garde-fou des dossiers residuels (aucun `tmp-*` hors dossier de l agent
   courant en fin de mission).
2. **Residu en cas de timeout** : si le basher timeout avant le `rm -f`,
   nettoyer a la main avant de relancer (sinon test-024 KO).
3. **Ne pas lancer un test qui scanne la racine depuis un script du dossier
   temporaire** : tout test qui scanne la racine (test-024, detecter-usage-
   scripts-temporaires) voit le DOSSIER `tmp-<agent>` de la mission courante ->
   lancer les controles en commande directe et, pour le garde-fou des dossiers
   residuels, apres suppression du dossier de l agent courant.

### Commandes bash des combos (meme regle, v0.2.1)

> **REGLE** : les commandes des combos (`combos-moteur`, definitions
> `definition-combo.json`) et du catalogue (`generateurs-commande`) suivent
> la MEME regle anti-echappement. L'interpolation `{var}` fait un
> remplacement BRUT puis `shlex.split` decoupe : toute valeur avec apostrophe
> non echappee casse la commande (`Commande invalide`). TOUJOURS quoter les
> variables dans les commandes (`--raison '{raison}'`), jamais les inserer
> brutes quand elles peuvent contenir apostrophe ou espace.

## La declaration des usages (v0.2.7, anti-recurrence registre a 0 ligne)

> **REGLE** : depuis la lecon du 2026-08-14 (3 missions completes sans
> aucune declaration au registre alors que les lecons etaient documentees),
> la declaration des usages est OBLIGATOIRE en fin de mission : le script
> temporaire lui-meme (mode script-temporaire) ET chaque outil utilise.
> Sans declaration, la mission est invisible pour les controles (lecon :
> registre reste a 0 ligne).
>
> Le squelette de `generateurs-outil-temporaire` v0.2.1 contient le bloc
> DECLARATION USAGES : variable `AGENT` a renseigner + fonctions
> `declarer_usage()` / `declarer_usages()` qui appellent
> `enregistrer-usage-outil --mode script-temporaire` pour le script lui-meme
> puis un appel par outil utilise. Le script refuse de s executer si AGENT
> n est pas renseigne (erreur explicite).
>
> En fin de mission, l agent documente lecon + declarations dans le registre
> AVANT d activer le maillon suivant de la chaine.

## Le triplet dans les outils temporaires (v0.2.6)

> **REGLE TRIPLET (demande utilisateur 2026-08-14)** : TOUT outil temporaire
> genere par `generateurs-outil-temporaire` (v0.2.0) embarque le **triplet**
> comme le template-test v0.3.0 :
> 1. **PROTECTIONS** : verifier_nommage (anti-renommage), --dry-run, gestion
>    erreur.
> 2. **OPTIONS ON/OFF** : --isoler N (isoler une fonction), --desactiver 1,3,5
>    (desactiver des fonctions sans toucher au code).
> 3. **CHRONO** : chrono par defaut (--no-chrono pour le couper), chrono_etape
>    + bilan_chrono.
>
> Un outil temporaire SANS triplet doit etre REGENERE avec le generateur
> v0.2.0 (jamais ecrit a la main sans protections/chrono).

## Mesure des tokens dans les scripts temp (PILOTE, v0.1 - optionnel)

> Volet "mesure de la fenetre de contexte" (demande utilisateur 2026-08-15).
> Les scripts temporaires peuvent rendre compte de leur consommation via
> l outil `analyser-tokens` (modele hybride : registres locaux + compteurs
> API si disponibles). PILOTE optionnel : aucun script existant n est migre
> tant que le pilote n est pas valide.
>
> Utilisation (optionnel, en fin de script) :
> ```
> subprocess.run([sys.executable, "cerveau-projet/agents/tools/analyser/"
>                 "analyser-tokens/analyser-tokens.py", "--no-chrono"],
>                capture_output=True, text=True)
> ```
> L estimation est HONNETE : source fiable = API (TOKENS_SESSION ou
> metadonnees-session-*.json), sinon estimation locale signalee.

## Bannir les timeouts exterieurs (v0.2.8, demande utilisateur 2026-08-15)

> **REGLE ABSOLUE** : AUCUN timeout exterieur autour de l execution d un
> script temporaire (jamais de `timeout <s>` autour de la commande, jamais
> de delai impose par le script appelant). La seule gestion du delai est
> INTERNE : les protections du triplet (dry-run, gestion erreur) et, pour
> les tests, le timeout du lanceur. Un script temp qui progresse ne doit
> JAMAIS etre coupe par un timeout exterieur.
>
> La logique ternaire, identique a protocole-tests v0.3.3 (demande
> utilisateur 2026-08-15) :
> 1. **REUSSITE** -> afficher immediatement (l agent ne JAMAIS attendre la
>    fin d un timeout pour continuer) ;
> 2. **ERREUR** -> stop immediat (protection erreur du triplet) ;
> 3. **DELAI DEPASSE SANS REPONSE NI ERREUR** -> c est une ERREUR
>    SILENCIEUSE a trouver/a resoudre, puis l agent RELANCE le script
>    corrige. Un timeout exterieur couperait le script sans rien expliquer :
>    banni.

## ZERO TIMEOUT EXTERNE D ORCHESTRATION (v0.2.9, decision utilisateur 2026-08-15)

> **REGLE ABSOLUE (decision utilisateur)** : les outils d ORCHESTRATION (les
> commandes qui lancent les scripts temporaires depuis le terminal) n imposent
> AUCUN timeout externe sur l execution des scripts conformes : l attente est
> INDEFINIE, et c est L UTILISATEUR qui est le DERNIER RECOURS (il interrompt
> manuellement si besoin).
>
> Les protections INTERNES du triplet sont les SEULES a trancher un blocage
> (dry-run, gestion erreur) ; les timeouts internes (lancer_protege, timeout
> du lanceur pour les tests) sont CONSERVES - on ne bannit que le timeout
> exterieur d orchestration, jamais les protections. Un timeout d
> orchestration dimensionne au plus juste tuerait un script legitime : AUCUN.

## L entonnoir (normalisation transparente, v0.2.5 -> v0.2.10)

> **REGLE ENTONNOIR (v0.2.10, anti-recurrence lecon 2026-08-15)** : TOUT
> script temporaire passe par `executer-script-temporaire` (categorie
> Executer) avant execution - **jamais de `python3` direct** sur un script
> de `tmp-<agent>/`, MEME pour un script qui ne fait qu un append. L
> entonnoir **normalise automatiquement** (BOM, CRLF -> LF, accents via le
> dictionnaire de `corriger-dictionnaire-accents`), **controle la
> compilation** (une erreur de syntaxe bloque l execution avant tout
> lancement) puis **execute**. Le script est re-ecrit normalise sur disque :
> il devient conforme pour toute utilisation ulterieure.
>
> **PROTECTION DE SORTIE LF (entonnoir v0.1.1)** : l entonnoir ne normalise
> pas seulement le script AVANT execution - apres l execution, il re-scanne
> les fichiers du projet modifies pendant la fenetre d execution (mtime >=
> depart) et les re-normalise (CRLF -> LF, BOM, accents). Sortie :
> `[SORTIE-LF] N fichier(s) re-normalise(s) en LF pur`.
>
> **POURQUOI JAMAIS python3 DIRECT (lecon 2026-08-15)** : un append direct
> dans un script temp (`io.open(f, "a")` sans `newline=""`) traduit LF en
> CRLF sur Windows - l outil du projet `ajouter-contenu-fichier` est protege
> (`newline=""`) mais les scripts temp ne l etaient pas. Le 2026-08-15, des
> scripts de fin de mission lances en `python3` direct ont reintroduit des
> CRLF dans `janus/corrections.md` (detectes par test-047). La regle est
> donc ABSOLUE : python3 direct sur un script temp = violation, quel que
> soit le script. L entonnoir protege a l entree (script) ET a la sortie
> (fichiers ecrits au runtime).
>
> **Transparence** : l agent n a RIEN a changer dans sa facon d ecrire - il
> ecrit son script comme d habitude (meme avec accents ou retours Windows),
> et c est le PARCOURS qui s adapte : le passage par l entonnoir est le
> chemin naturel d execution. Si le script est deja conforme, l entonnoir
> l execute tel quel (0 modification).

## Pieges courants

1. **Script eparpille a la racine** : INTERDIT. Tout script temporaire va
   dans le dossier `tmp-<agent>/`. Un `.tmp-*` / `.zz-*` a la racine = KO
   test-024, quel que soit l usage.
2. **Oubli de declaration** : un OUTIL TEMPORAIRE DE MISSION utilise sans
   declaration au registre apparait comme anomalie au controle croise.
3. **Dossier temporaire non supprime** : `tmp-<agent>` laisse a la racine en
   fin de mission = anomalie (garde-fou des dossiers residuels). Toujours
   `rm -rf tmp-<agent>` avant de reactiver l agent suivant.
4. **Trou d'outil non remonte** : si le meme besoin revient 2 fois, ce n'est
   plus un besoin ponctuel -> promotion outil durable (Vulcain), ne pas
   reutiliser un script temporaire.
5. **Le registre ne capture que ce qui passe par le generateur** : c'est
   pourquoi la declaration manuelle (mode script-temporaire) est obligatoire
   pour les OUTILS TEMPORAIRES DE MISSION.
6. **Journal dans le /tmp systeme** : toute capture de sortie redirigee
   vers `/tmp/...` = ecriture HORS workspace (regle v0.2.11). Les journaux
   vont dans `tmp-<agent>/fichier.log`, supprimes avec le dossier en fin de
   mission.

## Liens

- [generateurs-outil-temporaire](../../../tools/generateurs/generateurs-outil-temporaire/generateurs-outil-temporaire.md)
- [enregistrer-usage-outil](../../../tools/enregistrer/enregistrer-usage-outil/enregistrer-usage-outil.md)
- [detecter-usage-scripts-temporaires](../../../tools/detecter/detecter-usage-scripts-temporaires/detecter-usage-scripts-temporaires.md)
- [tester-lancer-non-regression](../../../tools/tester/tester-lancer-non-regression/tester-lancer-non-regression.md)
- [test-024-scripts-temporaires](../../../tools/tester/tests/test-024-scripts-temporaires/test-024-scripts-temporaires.py)
- [index-regles-general](index-regles-general.md)
