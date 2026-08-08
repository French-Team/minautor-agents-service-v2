---
identite:
  type: corrections
  appartient_a: vulcain
  commun: false
# Corrections et Surcharges -- Vulcain
# Constructeur d'outils reels

agent:
  nom-agent: "vulcain"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a Vulcain"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges
---

## [PHILOSOPHIE] Comment je fonctionne

### Philosophie 1 : La Portabilite d'Abord

**Ce que je suis** : Un agent qui cree des outils partout.

**Le Pourquoi** :
- Les utilisateurs ont des systemes differents
- Un outil qui ne marche que sur un systeme est inutile
- La portabilite = plus d'utilisateurs

**Le Comportement** :
Avant de choisir une technologie, je verifie :
1. Est-ce que c'est disponible sur tous les systemes ?
2. Est-ce que c'est facile a installer ?
3. Est-ce que c'est performant ?

---

### Philosophie 2 : Tester Avant de Valider

**Ce que je suis** : Un agent qui ne fait pas confiance.

**Le Pourquoi** :
- Un outil non teste est un outil casse
- Les tests revelent les problemes
- L'utilisateur merite la qualite

**Le Comportement** :
Avant de valider un outil :
1. Je teste sur au moins 2 systemes
2. Je verifie les cas limites
3. Je documente les resultats

---

### Philosophie 3 : La Documentation Technique

**Ce que je suis** : Un agent qui documente ses choix.

**Le Pourquoi** :
- Sans documentation, les outils sont incomprehensibles
- La documentation aide a la maintenance
- Elle permet l'amelioration

**Le Comportement** :
Pour chaque outil, je documente :
1. Le choix technologique
2. Les raisons du choix
3. Les alternatives envisagees
4. Les tests effectues

---

## [FEEDBACK] Ce que j'ai appris

### Lecon : La Portabilite est Sacree

**Ce qui s'est passe** :
J'ai cree un outil qui ne marchait que sur Linux.
L'utilisateur l'a teste sur Windows -> echec.

**Ce que j'ai compris** :
- La portabilite n'est pas une option -- c'est une necessite
- Un outil non portable est un outil casse
- Il faut toujours tester sur plusieurs systemes

**Ce que je fais maintenant** :
Avant de creer un outil, je verifie la disponibilite des technologies sur tous les systemes.

---

## [LECON] 2026-08-07 -- Renommage d outil

**Tache** : Deplacer mettre-a-jour-agents-md vers activer/activer-agent-principal

**Lecon** :
- Le nom d un outil doit refleter sa fonction reelle (activer l agent principal, pas "mettre a jour")
- La categorie du dossier determine le prefixe obligatoire (dossier activer/ -> prefixe activer-)
- Lors d un renommage d outil : 1) deplacement physique + renommage des fichiers, 2) contenu interne (.sh/.py/.md/spec/test), 3) ~120 references dans ~31 fichiers (fiches, template, index-tools, protocoles, README, AGENTS.md), 4) boucle retro-action, 5) index-tools (nouvelle section + compteurs), 6) README (categorie), 7) test reel du cycle activer/reactiver
- Preserver AGENTS-historique.md (journal historique) et les entrees Versionning qui documentent l ancien nom

---

## [LECON] 2026-08-07 -- Multi-session activer-agent-principal v0.3.0

**Tache** : Faire evoluer activer-agent-principal pour plusieurs LLM en parallele (multi-session)

**Lecon** :
- Chaque LLM demarre comme Cerberus mais doit avoir SON bloc dedie dans AGENTS.md (## Sessions LLM / ### Session : session-llm-N) avec SON agent principal
- Nouvelle action sidentifier : attribue le prochain session-llm-N libre (ou nom explicite), cree le bloc, Cerberus par defaut
- Session OBLIGATOIRE dans activer/reactiver : ne modifier QUE le bloc de la session visee (isolation)
- Historique global 4 colonnes : | date | session | agent | raison |
- Migration automatique de l ancienne structure (## Agent Principal Actuel -> ## Sessions LLM + session-llm-1)
- PIEGE CORRIGE : dans le .py, la migration retournait le contenu converti SANS le persister dans la branche identification (fichier restait ancienne structure) -- toujours ecrire le contenu migre
- PIEGE CORRIGE : apres migration, sidentifier doit utiliser session-llm-1 (cree par la migration) et afficher le message d identification
- Variable d environnement AGENTS_FILE / AGENTS_HISTORIQUE : indispensable pour tester sur copies
- Les tests (12/12) sont passes par Morpheus (regle delegation respectee)

---

## [LECON] 2026-08-07 -- Outil permanent au lieu de script temporaire

**Tache** : Creer remplacer-texte (remplacement massif multi-fichiers)

**Lecon** :
- Quand un script temporaire est cree pour un besoin recurrent (renommages massifs, mises a jour de references), il DOIT devenir un outil permanent du cerveau au lieu d etre re-ecrit a chaque fois.
- Outil cree : remplacer-texte (dossier remplacer/, prefixe remplacer-) avec paires ancien->nouveau, exclusions (AGENTS-historique.md, exemples/), dry-run, rapport, idempotence.
- Tests reels passes : nominal, dry-run, exclusions, idempotence, version sh.

---

## [LECON] 2026-08-07 -- Profil session classeur v0.3.1

**Tache** : Faire evoluer activer-agent-principal (v0.3.0 -> v0.3.1) pour ecrire/mettre a jour automatiquement le profil de session dans le classeur-variables

**Lecon** :
- Nouvelle fonction mettre_a_jour_profil_session (py + sh) : variable PAR SESSION `profil-session-<session>` dans stockage/variables-actuelles.md, format `| `profil-session-<session>` | session: <session> / agent: <agent> / date: <AAAA-MM-JJ HH:MM> | activer-agent-principal | <AAAA-MM-JJ> | [OK] |`
- Appelee a chaque sidentifier (Cerberus), activer (agent) et reactiver (Cerberus) ; ligne existante -> mise a jour, absente -> ajoutee a la fin du tableau
- Surcharge CLASSEUR_STOCKAGE par variable d environnement pour les tests (parite avec AGENTS_FILE/AGENTS_HISTORIQUE)
- PIEGE ECHAPPEMENT : dans un .sh, ne JAMAIS ecrire de backticks litteraux dans un bloc python -c "..." embarquee (commande substitution bash) ; utiliser $(python -c "sys.stdout.write(chr(96))") ou chr(96) en python pour construire les backticks
- PIEGE INSERTION PYTHON : quand on insere du code .py via un script python, les sequences 
 dans une chaine non-raw sont INTERPRETEES (vrais sauts de ligne dans le code insere) -- utiliser raw string r'''...''' ou chr(10) pour les escapes
- Tests formels passes par Morpheus (regle delegation respectee) : test-002 v0.3.1 (7/7) + regression test-001 v0.3.0 (12/12)

## [LECON] 2026-08-07 -- Regle de derivation profil-session v0.3.2

**Tache** : Corriger le nommage profil-session (verdict A REVOIR de Janus : profil-session-session-llm-1 au lieu de profil-session-llm-1)

**Lecon** :
- REGLE DE DERIVATION IMMUABLE : l'id de la variable = `profil-session-` + la partie du nom complet APRES le prefixe `session-` (session session-llm-1 -> id profil-session-llm-1). NE JAMAIS concatener profil-session- avec le nom complet.
- La regle est documentee dans le schema (variables-definition.md) comme reference unique
- PIEGE SLICE : en python, `session[7:]` retire un caractere de trop ("session-" fait 8 caracteres) -> id `-llm-1` -> ligne `profil-session--llm-1` (double tiret). TOUJOURS utiliser `session[len("session-"):]` (ou ${session#session-} en bash)
- PIEGE PARITE : corriger le .py ET le python embarque du .sh (2 endroits distincts)
- Quand une regle immuable est testee, ajouter un test NEGATIF (verifier qu'aucune valeur interdite n'est creee) en plus des tests positifs
- Le second controle de Janus a detecte l'ecart avant la mise en production - la confiance se gagne (cycle MORPHEUS -> JANUS indispensable)

## [LECON] 2026-08-07 -- Bug liaison id ecrasee (v0.3.5)

**Tache** : Corriger le bug MAJEUR "liaison id ecrasee par activer/reactiver (sessions fantomes)"

**Lecon** :
- SYMPTOME : au redemarrage, un LLM ne retrouvait pas sa session (l'outil creait une nouvelle session libre = session fantome) apres un cycle activer/reactiver.
- CAUSE RACINE : activer_agent et reactiver_cerberus appelaient mettre_a_jour_profil_session(session, agent) SANS llm_id, et cette fonction reecrivait la ligne du classeur SANS le champ id: -> la liaison posee par sidentifier etait ECRASEE.
- CORRECTION : quand llm_id n'est pas fourni, lire l'id deja lie dans la ligne existante du classeur et le PRESERVER (regex id: (\S+) dans le .py, grep -oE "id: [^ /]+" dans le .sh). Parite py + sh + doc .md + test-005 (28/28).
- REPARATION DONNEES : le bug ayant deja ecrase la liaison de session-llm-2 (id: llm-1 disparu), il a fallu re-lier la ligne via editer-fichier (l'outil corrige ne restaure pas les donnees deja corrompues).
- PIEGE REGRESSION : les tests 001/002/003 echouent sur des cas pre-existants (semantique de sidentifier changee en v0.3.3/v0.3.4 : l'argument n'est plus un nom de session mais un id LLM). Ne PAS attribuer ces echecs a une nouvelle version : comparer avec la version precedente (git show HEAD:... ) pour prouver qu'ils sont pre-existants (v0.3.4 originale : 7/5, 7/1, 17/4 identiques).
- PIEGE TEST : test-001 n'exporte pas CLASSEUR_STOCKAGE -> pendant la regression il a ecrit dans le VRAI classeur (profil-session-llm-1 modifie). Verifier les variables d'environnement de test apres chaque regression et restaurer les valeurs.

## [LECON] 2026-08-07 -- Regle alignement v0.4.0 (numero de session = id LLM)

**Tache** : Faire evoluer activer-agent-principal (v0.3.5 -> v0.4.0) : le numero de session porte le numero de l'id (llm-1 -> session-llm-1)

**Lecon** :
- REGLE ALIGNEMENT : id `llm-N` -> session `session-llm-N`. Le LLM se reconnait par lecture d'AGENTS.md : chaque bloc porte le champ `| **Id LLM** | <id> |` (source double AGENTS.md + classeur synchronises).
- CONFLIT : si session-llm-N est deja liee a un AUTRE id -> message ATTENTION + prochaine session libre (jamais deux LLM sur la meme session).
- ABSORPTION : une session-llm-N orpheline (bloc sans champ Id LLM) peut etre absorbee par l'id llm-N.
- Id NON numerique (llm-atlas) : pas d'alignement -> prochaine session libre + liaison (comportement v0.3.4 conserve).
- MIGRATION DONNEES : il a fallu absorber le bloc historique session-llm-1 (mission REPRISE deja executee) : mon bloc session-llm-2 est devenu session-llm-1 avec champ Id LLM = llm-1, la ligne classeur profil-session-llm-2 supprimee, et profil-session-llm-1 mise a jour avec la liaison id.
- PIEGE EFFACEMENT : quand une session change de nom (session-llm-2 -> session-llm-1), mettre a jour AGENTS.md ET le classeur (supprimer l'ancienne ligne profil) sinon doublon.
- Le second controle Janus suivra (mission dans la liste : Optimiser un outil -> OUI).

## [LECON] 2026-08-07 -- Guide-Parcours v0.1.0 (jeu de piste) - 2 bugs detectes par Morpheus

**Tache** : Construire l'outil guider-parcours (jeu de piste anti-oubli : navigation case par case dans un parcours JSON, indices outil/fichier/regle, branches) + parcours-vulcain.json prototype + fiche allegee.
**Lecon** :
- CONCEPT : au lieu de fiches 200+ lignes que les agents oublient de relire, chaque agent a un PARCOURS de cases ; l'outil guide affiche 1 case a la fois avec l'indice exact (outil, fichier, regle) et les branches selon la reponse. demarrer.md = case 0. Parcours = source de verite (fiche allegee).
- BUG 1 (NOMMAGE) : l'outil s'appelait guide-parcours dans le dossier guider/ -> verifier_nommage du .sh exige le PREFIXE DE LA CATEGORIE (guider-) et refusait de demarrer, alors que le .py (qui verifie le dossier de l'outil) acceptait. PIEGE : les 2 verifications de nommage template .py/.sh ne sont PAS identiques pour une categorie multi-mots -> renommer en guider-parcours (dossier + fichiers + spec + test + references index-tools + fiche) via remplacer-texte.
- BUG 2 (PARITE .sh) : executer_python lancait 'python3 << PYEOF' SANS transmettre $@ -> le python embarque recevait 0 argument ('chemin du parcours obligatoire'). CORRECTION : 'python3 - "$@" << PYEOF' (le tiret place les args dans sys.argv[1:]). PIEGE HEREDOC : dans un .sh, le bloc python embarque par heredoc IGNORE la ligne de commande si on ne transmet pas les arguments explicitement.
- PIEGE RENOMMAGE : quand on deplace un dossier d'outil (guide-parcours -> guider-parcours), creer les sous-dossiers cibles (spec/, tests/) AVANT les mv, sinon 'No such file or directory'.
- PIEGE GROUPE : remplacer-texte sur un dossier parent (tools/) avec exclusion du dossier deja renomme (--exclu-dossier guider) pour eviter double remplacement.
- PIEGE ASCII : dans une lecon, ne jamais ecrire de caractere accentue (ex: lancait sans cedille) -> lecon validee par valider-conformite-ascii.
- Test formel 14/14 passe par Morpheus (regle delegation respectee).

## [LECON] 2026-08-08 -- Spec-guider-parcours v0.2.12 : outil de reference generateurs-case

**Tache** : Documenter generateurs-case dans la spec-guider-parcours comme L OUTIL DE REFERENCE pour creer/editer/supprimer des cases (suite de l integration Buffy).
**Lecon** :
- CONCEPT : la spec-guider-parcours (v0.2.11) ne mentionnait PAS generateurs-case (0 occurrence) alors que c est l outil officiel de modification des cases (recablage auto + validation auto) -> un agent ou humain qui voulait creer une case ne trouvait pas l outil de reference dans la spec du format. Une spec de FORMAT doit documenter l OUTIL DE REFERENCE de ce format.
- CONTENU AJOUTE (v0.2.12) : section complete apres Exemple minimal et avant Patterns : sous-commandes (liste/ajouter/editer/supprimer), options cles (--case, --type, --titre, --question, --message, --suivant, --apres recablage auto, --branche, --indice-regle/outil/fichier, --vers, --dry-run), 3 exemples (ajouter/editer/supprimer), 6 regles d utilisation (--dry-run d abord, recablage auto, fin sans suivant exige --vers, garde-fou Pattern 5, rappel ASCII position 1, RE-AUDIT complet apres chaque operation). Tableau Emplacement des fichiers + critere d acceptation 17 ajoutes.
- METHODE : lire la spec complete AVANT d editer (structure, point d insertion, format CRLF respecte), s appuyer sur la doc generateurs-case.md pour des options fideles (jamais inventer une option).
- PIEGE ASCII : les guillemets ASCII obligatoires dans les exemples de commande (ex: indice-regle avec guillemets doubles) ; valider-conformite-ascii 0 a la fin.
- La spec est le contrat entre l outil et les parcours : chaque evolution de format (patterns, outil de reference) doit y etre documentee au meme moment.

## [CONFIG] Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown + Code"
  niveau_detail: "Complet"
  style_reponse: "Technique avec exemples"
  tester_avant_valider: true
  documenter_choix: true
  prioriser_portabilite: true
```

### Technologies par defaut

| Systeme | Technologie preferee |
|---|---|
| **Windows** | Bash (Git Bash) ou PowerShell |
| **Linux** | Bash |
| **Mac** | Bash |
| **Cross-platform** | Python ou Node.js |

---

## [STATS] Mon evolution

| Date | Lecon | Philosophie integree |
|---|---|---|
| 2026-08-05 | La portabilite est sacree | Portabilite d'Abord |
| 2026-08-05 | Tester avant de valider | Tester Avant de Valider |

---

## [NOTES] Notes de session

### Session du 2026-08-05

**Tache** : Creation de la fiche Vulcain

**Lecons apprises** :
- Vulcain est l'agent technique du cerveau-projet
- Il transforme les outils.md en outils reels
- La portabilite est sa priorite

---

## [CONNEXIONS] Connexions

| Fichier | Role |
|---|---|
| `vulcain.md` | Ma fiche principale |
| `AGENTS.md` | Fichier dynamique |
| `../../agents/regles-immuables/general/protocole-technologies/` | Protocole de choix technologique |
| `../../agents/regles-immuables/general/protocole-outils/` | Protocole de construction d'outils |

---

## [LECON] 2026-08-08 -- nettoyer-sessions v0.1.1 (parite sorties + bug latent 0\n0)

**Tache** : corriger la divergence de parite des sorties py/sh signalee par Morpheus (le .py affichait 'Nettoyage termine : N lignes supprimees', le .sh juste 'Nettoyage termine') et valider par retest Morpheus.
**Lecons** :
1. PARITE DES SORTIES : quand on cree un outil py+sh, les MESSAGES de sortie doivent etre strictement identiques (pas seulement les fichiers resultants) -- Morpheus a ajoute 6 assertions (reel + dry-run, CRLF normalise) qui figent la parite dans le test
2. BUG LATENT REVELE : nb=$(grep -c ... || echo 0) produit 0\n0 quand il y a 0 occurrence (grep -c affiche 0 ET echo 0 s execute) -> casse l arithmetique $((...)) du total -> TOUJOURS nb=$(grep -c ... 2>/dev/null); nb=${nb:-0} (piege deja documente, se manifeste des qu on utilise nb dans un calcul)
3. ORDRE DES BLOCS : dans une fonction, le test dry-run doit passer AVANT le test de valeur 0, sinon le message [DRY-RUN] Classeur : 0... est omis alors que le .py l affiche toujours -- l ordre des branches change la parite
4. LA BOUCLE FONCTIONNE : Morpheus a detecte le bug que mes validations de base (compile, ASCII, parite fichiers) ne voyaient pas -- la delegation des tests n est pas une formalite, elle protege la qualite
5. Versionner py/sh/md ENSEMBLE (0.1.0 -> 0.1.1) : la parite de version fait partie de la parite de l outil

## [LECON] 2026-08-08 -- valider-cartes-decision v0.3.0 (cible = parcours JSON)

**Tache** : mettre a jour valider-cartes-decision qui cherchait encore la section Carte de Decision dans les fiches allegees (-> --tous = 5/5 NON CONFORME a tort) pour valider le PARCOURS JSON, source de verite du guidage.
**Lecons** :
1. EVOLUTION DE CIBLE : quand un format change (fiches allegees v0.2.0 : la carte vit dans le parcours JSON), l OUTIL qui valide l ANCIEN format devient obsolete et produit des NON CONFORME a tort -- il faut migrer la cible de l outil DANS LA MEME logique que le format, pas seulement documenter
2. VALIDATIONS D UN PARCOURS : json.load, cles top-level (identite + parcours + cases), identite.type = parcours, case_depart existe, types valides (question/indice/controle/fin), references (suivant + branches.vers) vers des cases existantes, case c0 question de relecture (Pattern 4) -- les 6 controles couvrent la structure ET le standard de demarrage
3. PARITE .sh = WRAPPER : pour un outil dont la logique vit dans le .py, le .sh peut etre un wrapper pur (exec python3 "$PY_SCRIPT" "$@", pattern detecter-impacts) -- la parite des sorties est garantie PAR CONSTRUCTION (aucun doublon d en-tete, aucune divergence de logique)
4. INTERFACE PRESERVEE : combo-controle-outil appelle .py --tous -- une evolution de cible ne doit JAMAIS casser les appels existants (verifier les combos et parcours qui citent l outil)
5. --tous doit SCANNER les dossiers agents avec parcours/ (pas une liste en dur AGENTS_DEFAUT) : l outil devient automatiquement a jour quand un agent est cree
6. Test formel 24/24 (Morpheus, modele boucle) : --version, --tous 11/11, --agent, --fichier (parcours/.md), parcours corrompu = 3 erreurs, fichier inexistant, parite py/sh 4 cas, ASCII, nommage

## [LECON] 2026-08-08 -- valider-nommage v0.3.1 (bruit du scan recursif)

**Tache** : corriger le bruit du scan --recursive qui signalait en ERREUR les fichiers des sous-dossiers composants d un outil (tests/, spec/, protections/, __pycache__/).
**Lecons** :
1. STRUCTURE : le scan --recursive attend categorie/outil/fichiers directs. Les SOUS-DOSSERS COMPOSANTS (tests/, spec/, protections/, __pycache__/) ne sont pas des outils : leurs fichiers (test-*, spec-*) ont leur propre convention et ne doivent PAS etre valides avec le prefixe de la categorie parente
2. CORRECTION A 2 NIVEAUX : exclure les composants au niveau CATEGORIE (ex: tester/tests/) ET au niveau OUTIL (ex: activer-agent-principal/tests/) -- une seule exclusion laisse le bruit sur l autre niveau
3. PARITE : la liste d exclusion doit etre definie dans le .py (constante) ET le .sh (variable + grep -vE dans le find) -- les 2 modes recursifs (listdir .py, find .sh) doivent filtrer pareil
4. CAS PARTICULIER tester/ : protections/ est aussi un conteneur de composants (structure tester/protections/<outil>/) -- il faut l ajouter a la liste (c est le 3e conteneur apres tests/ et spec/)
5. REGRESSION : verifier l usage NORMAL (scan global tools/) ET l usage sur categorie/outil directement -- le bruit n etait visible que sur le 2e usage (scan global deja propre car il ne descend pas dans les sous-dossiers d outils)
6. Test formel 13/13 (Morpheus) : aucune regression -- les modes --mots-seuls et --type restent inchangees (la correction ne touche QUE le mode recursif de nommage)

## [LECON] 2026-08-08 -- Catalogue generateur 12 commandes (absorber les 2 combos)

**Tache** : etape 4 plan combo-orchestrateur -- declarer les 2 combos manquants (combos-valider-cerveau, combos-corriger-non-ascii) dans catalogue-commandes.json (10 -> 12 commandes).
**Lecons** :
1. Le catalogue est la SOURCE DE VERITE du generateur : chaque entree = un modele d appel d outil deja ecrit, corrige et valide -- ajouter une commande = copier le modele reel de l outil (script + parametres exacts), jamais une invention
2. FORMAT ENTREE : nom, description, interpreteur, script, modele ({parametre} en dur dans le modele), parametres (cle/question/type/obligatoire/defaut/flag/quoter) -- les parametres optionnels portent un defaut (flag -> defaut non, texte -> defaut valeur)
3. Les FLAGS se declarent avec type flag + champ flag (--detail, --stop, --dry-run, --all, --rapport) et defaut non : le generateur les omet si non, les ajoute si oui -- teste avec --reponses 'flag=oui'
4. LES COMBOS SONT ABSORBES DANS LE CATALOGUE : audit-general (deja present), valider-cerveau et corriger-non-ascii (ajoutes) -> le generateur peut composer la commande de N IMPORTE QUEL combo, c est la porte d entree des cases generateur du combos-moteur (Pattern 3)
5. VALIDATION : JSON valide (12 commandes), --liste 12, --commande + --reponses compose la commande exacte (avec defauts / avec flags), parite .sh (les 2 versions listent 12 et composent la meme commande -- la diff brute py/sh est uniquement CRLF vs LF, comportement Windows normal)
6. Le generateur et les 2 combos sont INCHANGES : seul le catalogue a ete modifie -- la source de verite des combos reste leurs dossiers agents/tools/combos/

## [LECON] 2026-08-08 -- Combos-moteur v0.1.0 (3 bugs detectes par Morpheus)

**Tache** : construire le moteur generique combos-moteur (py + sh) selon la spec-combos-moteur v0.1.0.
**Lecons** :
1. PIEGE CHEMIN_RACINE : depuis un script dans agents/tools/combos/combos-moteur/, il faut **5 remontees** depuis le FICHIER .py (combos-moteur -> combos -> tools -> agents -> cerveau-projet) mais **4 depuis le DOSSIER** du .sh (via COMBO_MOTEUR_DIR) -- j'ai d abord mis 4 partout -> chemin agents/agents/tools/ (generateur introuvable). La parite py/sh exige de compter le nombre de niveaux selon la base (fichier vs dossier).
2. PIEGE EXTRACTION GENERATEUR : generateurs-commande imprime la commande sur la ligne SUIVANTE le marqueur `=== COMMANDE A LANCER ===` (pas sur la meme ligne) -- prendre la premiere ligne non vide APRES le marqueur, sinon la commande generee est vide.
3. PIEGE PARITE SORTIE : dans le .py, `_couleur("=== COMBO TERMINE ===\n")` avec un \n integre ajoute un double saut de ligne absent du .sh (texte brut) -> les sorties py/sh divergent dans les tests de parite. Ne jamais mettre de \n dans _couleur, toujours dans un print() separe.
4. PIEGE TEST WINDOWS : dans un test Python, un script .sh doit etre appele avec ["bash", script, ...] sinon WinError 193 (pas une application Win32 valide).
5. Le modele du moteur (guider-parcours.py) : charger_definition + valider_definition + navigateur generique -- le combos-moteur suit le meme squelette pour les combos.

## [LECON] 2026-08-08 -- generateurs-carte v0.1.0 + generateurs-case v0.2.0 (etape OUTILS de la refonte du modele de cases)

**Tache** : creer l'outil CARTE (agit sur la carte COMPLETE) et etendre generateurs-case pour les GROUPES de cases (modele compose Pattern 7).
**Lecons** :
1. CONCEPT : generateurs-case = 1 case (liste/ajouter/editer/supprimer/ajouter-bloc) ; generateurs-carte = carte COMPLETE (creer un squelette patterns 4-5-6-7, analyser les chemins BFS, detecter 5 types d'anomalies, dupliquer un chemin avec recablage). Les deux sont complementaires et vivent cote a cote dans generateurs/.
2. ACTION ajouter-bloc (Pattern 7) : cree d'un coup decision (question 2 branches OUI->deviation / NON->suite) + deviation (indice -> rejoint) + rejoint (indice -> suite) -- ids par defaut cN/cNa/cNb, --suite obligatoire, --apres pour le recablage du suivant. Le bloc est navigable PARCOURS TERMINE sur les 2 branches.
3. ACTION creer : le squelette doit reproduire EXACTEMENT les cases des parcours reels (c0 question honnete OUI->c0c/INCERTAIN->c0b/NON->c0b, c0b RELIRE, c0c CONTEXTE avec lire-activite-recente + AGENTS.md, c1 Mission, fin active) -- un squelette qui oublie un pattern serait un faux depart.
4. ACTION analyser : BFS de case_depart vers les fins avec anti-boucle (jamais repasser par une case du chemin courant) -- 6 chemins pour le squelette (3 branches c0 x 2 branches c1), les impasses marquees [impasse].
5. ACTION detecter : 5 controles (references cassees, boucle d'attente regle 10 avec 'attente' dans titre/question + branche vers soi, cases inatteignables, cases sans sortie, decision a branche unique Pattern 7) -- la boucle d'attente n'est detectee QUE si le titre/question porte 'attente' (test negatif : branche vers soi sans 'attente' n'est pas une boucle d'attente).
6. ACTION dupliquer-chemin : BFS debut->fin, copies prefixees (d+id), references INTERNES recablees vers les copies, references EXTERNES restent sur les originales (les copies ne sont pas branchees automatiquement sauf --brancher-debut) -- detecter signalera donc les copies comme inatteignables (comportement attendu et documente).
7. PIEGE ARGPARSE : ne pas nommer une option --version sur une sous-commande qui recoit aussi le --version global de la boucle commune (conflit) -- renommer (--ver pour la version du parcours cree).
8. PIEGE HEREDOC .sh : le .sh de generateurs-case etait un heredoc complet (ancien pattern) -- je l'ai CONVERTI EN WRAPPER PUR (exec python3 -- "$@") : parite garantie par construction, plus de divergence de version entre les 2 fichiers.
9. VALIDATION : py_compile + bash -n, parite py/sh (analyser + liste identiques CRLF normalise), ASCII 0 sur 6 fichiers outils + spec v0.2.14 + index + fiche, nommage generateurs- OK, tests reels sur copies workspace (creer 6 cases, analyser 6 chemins, detecter 0 puis 5 anomalies, dupliquer 3 copies, ajouter-bloc navigation OUI/NON PARCOURS TERMINE).
6. Test 31/31 REUSSI par Morpheus (regle delegation respectee) : --liste, navigation OUI/NON, interpolation, generateur AUTO, variable manquante code 1, dry-run, parite, nommage, ASCII, syntaxe.

## [NOTES] Spec-combos-moteur + Pattern 3 2026-08-08 (combo orchestrateur)

**Mission** : specifier le format definition-combo.json (futur outil combos-moteur) + documenter le Pattern 3 (generateur -> execution) dans spec-guider-parcours v0.2.4.
**Lecons** :
1. Le COMBO devient l'orchestrateur : l'agent lance UN combo (definition-combo.json lu par combos-moteur, meme philosophie que guider-parcours lit parcours-<agent>.json) au lieu d'une suite d'outils -- plus transparent, plus fiable, plus digeste
2. Le dataflow du combo : chaque case generateur appelle generateurs-commande --reponses (mode AUTO, alimente par les variables) -> compose la commande ; la case outil l'execute -> sortie = variable ; la case controle decide si le resultat est transmis BRUT ou si un generateur s'intercale
3. Le generateur-commande reste INCHANGE : le moteur fait le lien avec --reponses -- le generateur est la source de verite de la syntaxe (modele valide du catalogue), il devient INCONTOURNABLE comme composeur des cases generatrices
4. Variables : memoire INTERNE du combo (dict) par defaut, persistance optionnelle vers classeur-variables (persistant: true) -- pas d'ecriture disque a chaque case
5. Le Pattern 3 est documente dans spec-guider-parcours (bump v0.2.3 -> v0.2.4) : une case de parcours peut pointer vers un combo (indice outil combos-moteur + indice fichier spec) -- la procedure d'audit passe de 2 a 3 patterns (point 3 dedie) + critere d'acceptation 11
6. PIEGE ASCII : j'ai d'abord ecrit 'enchain-er' avec un i accentue (i circonflexe, U+00EE) dans le Pattern 3 -- detecte et corrige en 'enchainer' avant la validation ; verifier le texte dans les sections ajoutees, pas seulement le contenu recopie
7. Separation des domaines : le combo (definition JSON) est un fichier du cerveau (Buffy), le moteur est un outil (Vulcain) -- la spec le documente pour eviter les conflits
8. Bump spec-guider 0.2.3 -> 0.2.4 + doc guider-parcours 0.2.9 -> 0.2.10 (regle 8 ajoutee) -- les CLI de guider-parcours restent inchangees (distinction version doc vs outil)

## [NOTES] Spec-guider-parcours v0.2.3 2026-08-08 (prototype vulcain cas legitime assume)

**Mission** : documenter le prototype vulcain comme cas legitime ASSUME (fins independantes) au lieu de le corriger (demande utilisateur).
**Lecons** :
1. Le prototype vulcain est desormais documente comme CAS LEGITIME ASSUME : fins independantes par chemin (construire c9, modifier c15, autre c18/c19) = choix documente, PAS un defaut a corriger
2. La reformulation est coherente avec la regle 8 AUTONOMIE : ne pas converger est legitime quand chaque parcours reste individuel et complet -- le Pattern 1 (convergence) est une factorisation recommandee, pas une obligation absolue
3. Les cas particuliers de la procedure d'audit sont maintenant 2 : routage (cerberus, Pattern 2 non applicable) + prototype (vulcain, fins independantes assumees) -- le rapport Themis doit etre aligne (recommandation 2 : plus de correction a faire)
4. Bump spec 0.2.2 -> 0.2.3 + doc 0.2.8 -> 0.2.9 -- CLI inchangees

## [NOTES] Spec-guider-parcours v0.2.2 2026-08-08 (regle d'autonomie des parcours)

**Mission** : ajouter la regle d'autonomie des parcours dans la spec (demande utilisateur : chaque parcours doit rester individuel pour pouvoir etre complete par la suite).
**Lecons** :
1. REGLE 8 AUTONOMIE : chaque parcours est un fichier INDIVIDUEL par agent, la convergence est uniquement INTRA-parcours (factorisation interne des cases communes d'un meme parcours), AUCUN partage de cases entre parcours, chaque parcours est complet et validable independamment
2. La regle documente une realite deja vraie : l'audit a confirme qu'aucun des 11 parcours ne reference les cases d'un autre (0 reference croisee) -- la regle verrouille l'intention pour les futures creations
3. La convergence du Pattern 1 est une FACTORISATION INTERNE (les chemins d'un meme agent rejoignent SES cases communes), pas un partage inter-parcours -- la regle 8 le rend explicite pour lever l'ambiguite
4. La procedure d'audit a une sous-section Autonomie (verifier l'absence de references croisees) en plus des Pattern 1-2
5. Bump spec 0.2.1 -> 0.2.2 + doc guider-parcours 0.2.7 -> 0.2.8 (regle 7 AUTONOMIE ajoutee dans la section Regles de la doc) -- les CLI restent 0.1.0-py/-sh

## [NOTES] Spec-guider-parcours v0.2.1 2026-08-08 (procedure d'audit des 2 patterns)

**Mission** : documenter dans la spec la procedure d'audit des 2 patterns validee par l'audit des 11 parcours par Themis.
**Lecons** :
1. La procedure d'audit est maintenant dans la spec (section dediee v0.2.1) : Pattern 1 (case Mission question + branches + convergence, --liste + lecture structurelle), Pattern 2 (verification structurelle : PREMIER element des indices des cases d'ecriture = regle ASCII, plus fiable qu'une simple recherche de texte), cas particuliers legitimes (routage sans case d'ecriture, prototype sans convergence), revalidation complete (json.load + --liste + --reponses + ASCII)
2. L'audit de Themis a revele que la verification par grep seul ('REGLE IMMUABLE ASCII' present dans le fichier) ne suffit pas : la REGLE doit etre en POSITION 1 des indices -- d'ou la verification structurelle documentee
3. Quand une procedure est validee par un audit externe (Themis), la capitaliser dans la spec de l'outil pour que les prochaines creations naissent conformes et que l'audit soit reproductible
4. Bump spec 0.2.0 -> 0.2.1 (documentation seulement) + doc guider-parcours 0.2.6 -> 0.2.7 (reference spec) -- les CLI restent 0.1.0-py/-sh (version outil inchangee, distinction version outil vs doc vs spec)

## [NOTES] Doc guider-parcours v0.2.1 2026-08-07 (liste complete des parcours)

**Mission** : completer la liste des parcours dans la doc (ajout cerberus + buffy -> 6 parcours).
**Lecons** :
1. La liste Emplacement des parcours doit TOUJOURS etre synchronisee avec les parcours reels (agents/*/parcours/*.json) -- apres chaque creation de parcours, verifier si la doc a besoin d etre completee (cerberus et buffy manquaient)
2. Un bump de version DOC mineur (0.2.0 -> 0.2.1) suffit pour une mise a jour de liste -- les CLI restent inchangees
3. Ne jamais supprimer l'historique : la ligne 0.2.0 est mise a jour (liste completee) ET une ligne 0.2.1 est ajoutee pour tracer le changement

## [NOTES] Doc guider-parcours v0.2.0 2026-08-07 (reference spec + patterns)

**Mission** : mettre a jour la doc de l'outil pour referencer la spec v0.2.0 et les 2 patterns.
**Lecons** :
1. Bump de la DOC seulement : la version de la doc passe a 0.2.0 mais les CLI restent 0.1.0-py/-sh (l'outil n'a pas change, seule la doc evolue) -- distinguer version de l'outil et version de la documentation
2. La doc doit rester SYNCHRONISEE avec la spec : section Patterns + regles 5-6 ajoutees a la doc, identiques a la spec v0.2.0 (regles 6-7 du format) -- le lien Spec en en-tete et le tableau Versionning documentent la coherence
3. La liste des parcours de la doc doit couvrir TOUS les parcours existants (vulcain, morpheus, clio, janus) -- pas seulement le prototype

## [NOTES] Spec-guider-parcours v0.2.0 2026-08-07 (patterns)

**Mission** : documenter dans la spec les 2 patterns valides en production (demande utilisateur).
**Lecons** :
1. Le pattern MULTI-MISSIONS (case Mission + branches + chemins convergents) est documente dans la spec : un parcours peut couvrir plusieurs missions d'un agent, les chemins convergent vers les cases communes (verdict, lecons, retour) pour eviter la duplication -- exemple reel : parcours-janus.json (30 cases, 3 chemins)
2. Le rappel ASCII est devenu une REGLE DE FORMAT (regle 6 + Pattern 2) : toute case qui ecrit dans un fichier DOIT porter un indice regle ASCII en TETE de sa liste indices -- verification par grep 'REGLE IMMUABLE ASCII'
3. Versionner une spec : la version vit dans le .md (v0.1.0 -> v0.2.0), pas de dossier versions/ -- conserver le statut ebauche tant que l'outil n'est pas en production

## [NOTES] Spec-guider-parcours v0.2.5 2026-08-08 (Pattern 4 : case Question Honnete en case 0)

**Mission** : figer le nouveau standard de demarrage dans la spec -- la case c0 Question Honnete de relecture + c0b RELIRE obligatoire + case_depart = c0.
**Lecons** :
1. Le Pattern 4 documente ce qui etait deja une realite de production : les 11 parcours portent c0 (question memoire, SANS relire) + c0b (RELIRE obligatoire, corrections puis fiche) et demarrent en c0 -- l'audit Themis 11/11 (CONFORME 100/100) est la preuve de validite citee dans la spec
2. La regle 9 du format generalise le standard : TOUT parcours demarre en c0, branches exactes OUI -> c1 / INCERTAIN -> c0b / NON -> c0b, c0b -> c1, case_depart = c0, question contenant 'memoire' + 'SANS relire' -- un parcours qui ne demarre pas en c0 est un ecart
3. La procedure d'audit passe de 3 a 4 patterns : section 4 dediee (case_depart c0, question memoire, branches exactes, c0b RELIRE + corrections + fiche, navigation OUI/NON/INCERTAIN -> PARCOURS TERMINE) + renumero des sections 4-6 -> 5-7 + critere d'acceptation 12
4. Le Pattern 4 a un exemple JSON complet (parcours + c0 + c0b + c1) et l'exemple reel des 11 parcours -- les futurs parcours naissent conformes
5. SYNCHRONISATION TRIANGLE (spec + doc + fiche) : bump spec 0.2.4 -> 0.2.5 (header agent + historique) + doc guider-parcours 0.2.10 -> 0.2.11 (header spec, section Patterns 4, regle 9, versionning) + fiche vulcain (reference spec v0.2.3 -> v0.2.5 + entree historique) -- les 3 doivent referencer la meme version de spec
6. PIEGE ASCII : dans la formulation de la question honnete, eviter les guillemets non-ASCII -- utiliser la question exacte telle que portee par les parcours (mots 'memoire' et 'SANS relire' en MAJUSCULES) ; verifier le texte des sections ajoutees avec valider-conformite-ascii
7. Un bump de SPEC (documentation) n'impacte pas les CLI : guider-parcours.py/.sh restent 0.1.0-py/-sh -- seule la spec + la doc evoluent

## [NOTES] Convention identification v0.5.0 (2026-08-08) -- aucun mot seul

**Mission** : renommer les champs d'identification pour ne jamais utiliser un mot seul
(nom, role, statut...). Decision utilisateur : Id LLM -> Nom LLM (en tete du bloc),
Nom -> Nom Agent, Role -> Role Agent. Fiches YAML : nom -> nom-agent, role -> role-agent,
statut -> statut-<agent>. role_principal et role_specifique restent (deja composees).

**Livrables** :
1. activer-agent-principal v0.5.0 (py + sh) : bloc session en Nom LLM (EN TETE) / Nom Agent /
Role Agent ; reconstruction complete du bloc en ordre canonique a chaque edition ; migration
automatique des anciens champs (Nom -> Nom Agent, Role -> Role Agent, Id LLM -> Nom LLM) ;
table Sessions connues en colonne Nom LLM ; lecture retrocompatible (Id LLM|Nom LLM)
2. lister-agents v0.3.0 (py + sh) : lecture role-agent / statut-<agent> avec repli anciens noms
3. evaluer-agents v0.2.2 (py + sh) : verification de l'agent actif sur **Nom Agent** (le grep
'Nom' simple matcherait desormais **Nom LLM** en premier -- piege detecte)
4. Tests : test-007 v0.5.0 cree (22/22), test-001/002/006 mis a jour (nouveaux champs)

**Lecons** :
1. LA RECONSTRUCTION COMPLETE DU BLOC (pas le remplacement ligne a ligne) est la seule
approche fiable pour une migration de champs : elle garantit l'ordre canonique (Nom LLM en
TETE), l'insertion des champs manquants et la migration des anciens noms en une passe
2. RETROCOMPAT LECTURE : toujours accepter l'ancien nom en lecture (Id LLM|Nom LLM) le temps
que tous les blocs soient migres -- sinon un ancien bloc casse la reconnaissance
3. PIEGE grep 'mot seul' : un grep 'Nom' matche **Nom LLM** en premier -- chercher le champ
complet (**Nom Agent**) avant l'ancien nom
4. PIEGE test negatif : un grep -q qui ne trouve rien retourne 1 -- pour un check 'AUCUN champ',
inverser la logique (if grep; then check 1; else check 0) sinon le test echoue a tort
5. PARITE py/sh : reconstruire le bloc a l'identique dans les deux versions (l'en-tete du
tableau et la ligne vide doivent etre re-emis) ; sinon le .sh reimprime l'ancien en-tete en parasite
6. La convention 'jamais de mot seul' vaut pour les CHAMPS IDENTIFIANTS (nom, role, statut) --
les mots composees deja qualifies (role_principal, role_specifique) restent inchanges
7. REGLE FONDAMENTALE (2026-08-08) : la detection des mots seuls doit distinguer 3 categories :
   (a) IDENTIFIANTS generiques interdits (nom, role, statut, id, date, cible -> liste noire explicite),
   (b) cles de SCHEMA de fiche autorisees (version, cree, specialites, forces, faiblesses -> liste blanche),
   (c) exceptions structurelles du format identite (type, commun, tags, appartient_a).
   Un detecteur qui signale TOUT mot seul produit des faux positifs massifs (fiches agents) :
   il faut une liste noire ciblee, pas une regex universelle.
8. LES TRACES DOCUMENTAIRES sont des documents figes : les rapports (janus/controles, corrections.md,
   mission-condenseur) documentent d'anciennes conventions et NE SONT PAS corriges. Le detecteur
   --mots-seuls ignore les dossiers de traces (controles, rapports, retro-actions, historique,
   exemples) en mode recursif + les fichiers traces assumes (mission-condenseur.md).
9. INTERPOLATION {var} : accepter les TIRETS (kebab-case) dans les noms de variables -- le regex
   [A-Za-z0-9_]+ rate {ma-variable} et laisse la cle brute non substituee. Toujours utiliser
   [A-Za-z0-9_-]+ (bug detecte lors du test de la case critere du combos-moteur).
10. CASE CRITERE combos-moteur v0.2.0 : l'embranchement AUTOMATIQUE (fichier-existe, egalite,
    non-vide, sortie-contient, fichier-contient) avec vers-vrai/vers-faux repond a la decision
    utilisateur 'les criteres dans les combos, pas dans les cartes'. La validation exige
    condition.type connu + vers-vrai ET vers-faux existants.

## [LECON] 2026-08-08 -- Regles immuables dans les generateurs (garde-fou RVAV + delegation + ASCII)

**Tache** : ajouter les REGLES IMMUABLES dans les generateurs (constat utilisateur : RVAV absent de generateurs-case/carte 0 occurrence -> les nouvelles cartes/cases ne rappelaient plus les regles immuables ; la delegation etait court-cuitee : tests faits par l'agent au lieu de Morpheus, Janus jamais active).
**Lecons** :
1. UN GENERATEUR PORTE LES REGLES DU FORMAT QU IL PRODUIT : si les regles immuables (RVAV, delegation, ASCII) ne sont pas dans les generateurs, TOUTE nouvelle carte/case nee de l'outil nait SANS ces regles -- la chaine de delegation se degrade silencieusement a chaque generation. Le generateur est le point d'entree : c est la qu il faut rappeler les regles.
2. GARDE-FOU NON BLOQUANT (pattern existant Pattern 5) : l'avertissement est JAUNE, l'operation reussit quand meme, l'agent decide -- jamais bloquer la generation, toujours rappeler.
3. generateurs-case v0.2.1 : fonction formuler_avertissement_regles_immuables(case) appelee a la construction (construire_case) + edition (action_editer) + ajouter-bloc (les 3 cases du bloc) -- detection : (a) case d'ECRITURE (indice outil creer/ecrire/editer/ajouter/inserer/copier-fichier) sans rappel ASCII en position 1 -> RAPPEL ASCII (Pattern 2) + RAPPEL RVAV ; (b) case fin avec message morpheus/janus/active/reactive -> RAPPEL DELEGATION chaine bout-en-bout (spec v0.2.15) ; (c) autre fin -> RAPPEL RVAV avant activation.
4. generateurs-carte v0.1.1 : le squelette creer est ENRICHI -- case c2b RVAV avant la fin (regle RVAV complete + fichier rvav-workflow) + rappel ASCII dans c2 + fin c9 rappelant la chaine bout-en-bout (J ACTIVE le maillon suivant a MA fin, dernier maillon REACTIVE Cerberus avec bilan consolide). Un squelette qui oublie RVAV/delegation est un faux depart.
5. PIEGE TEST : generateurs-carte prend l ordre `creer <parcours>` (action avant chemin), generateurs-case `<parcours> <action>` (chemin avant action) -- les 2 CLI sont differentes, ne pas copier l ordre de l un dans l autre.
6. PIEGE OPTION : `--vers` n existe que pour supprimer (pas pour ajouter) -- un ajout de fin avec --vers echoue silencieusement dans le test.
7. VALIDATION : py_compile + bash -n, parite py/sh (wrapper pur .sh = parite par construction), ASCII 0 sur 5 fichiers, nommage OK, tests reels sur copies workspace (3 cas de garde-fou : fin delegation -> rappel chaine ; edition fin -> rappel chaine ; case ecriture sans ASCII -> rappel ASCII + RVAV).

## [LECON] 2026-08-08 -- verifier-documents-manquants v0.3.0 (extension .py + branchement procedure 4g)

**Tache** : etendre l outil EXISTANT verifier-documents-manquants pour couvrir les .py (il ne verifiait que les paires .sh/.md) et le brancher dans la procedure 4g du Pattern 9 (decision utilisateur : etendre l outil existant, pas en creer un nouveau).
**Lecons** :
1. UN OUTIL EXISTE MAIS N EST PAS BRANCHE = INVISIBLE (lecon des outils fantomes) : verifier-documents-manquants existait depuis le debut mais (a) ne couvrait pas les .py (les parcours referencent surtout les .py depuis la vague 2) et (b) n etait PAS cite dans la procedure 4g du Pattern 9 -- la spec disait verifier a la main que le .md deduit existe, alors que l outil le fait automatiquement. Avant d ecrire une verification manuelle dans une spec, chercher l outil qui l automatise deja.
2. EXTENSION .PY : la logique de paire est identique (script -> .md du meme nom), on ajoute une 2e passe pour .py et le .md doit trouver son script en .sh OU .py (un .md avec .sh mais sans .py n est PAS un manquant : la regle est au moins un script).
3. FILTRE FAUX POSITIFS ELARGI : le scan tools/ revelait 9 manquants qui etaient TOUS des faux positifs non couverts -- dossier tests/, prefixe tester- (avec -v0xx : les fichiers de test versionnes), suffixe -test.md, et outils-base.md (document de support racine). PIEGE : ne PAS filtrer tout tester- : les outils REELS tester-protection-* (dossier tester/protections/) doivent rester verifies -- le filtre ne les ecarte que dans tests/ ou avec -v0xx.
4. WRAPPER PUR : le .sh (heredoc 248 lignes avec un bug de structure) est converti en wrapper pur (exec python3 du .py a cote, pattern guider-parcours v0.3.0) -- parite garantie par construction, plus de divergence de version ni de bug de heredoc.
5. VALIDATION : parite py/sh, test negatif (un .py sans .md est detecte 1 manquant), scan complet tools/ = 0 manquant (110 .sh, 95 .py, 111 .md), protections toujours verifiees, ASCII 0 sur 4 fichiers, branchement verifie dans la spec (procedure 4g point 3 = lancer l outil, resultat attendu 0 manquant).
6. VERSION DOCUMENTEE : la doc .md v0.3.0 reference le Pattern 9 et la procedure 4g comme usage principal (situation Quand l utiliser + relation avec guider-parcours).

## [LECON] 2026-08-08 -- generateurs-carte v0.2.0 (squelette conforme aux 11 patterns : Pattern 10 + Pattern 3)

**Tache** : mettre a jour le squelette creer de generateurs-carte pour integrer le Pattern 10 (une carte = un role) et le Pattern 3 (rappel des combos) dans les nouvelles cartes (decision utilisateur, suite du constat stabilite des cartes -- la spec-guider-parcours est passee a v0.2.19 avec les 11 patterns, mais le squelette nait encore avec les patterns 4-5-6-7-8).
**Lecons** :
1. UN SQUELETTE DE CARTE EST LE MOMENT D ENTRER DANS LE CYCLE DE VIE : si le squelette n integre pas un pattern au moment ou il est ajoute a la spec, TOUTE carte nee de l outil apres cette date nait SANS ce pattern -- les futures cartes se degradent silencieusement. Le squelette doit suivre la spec pattern par pattern (ici v0.2.19 = 11 patterns).
2. POSITIONNEMENT DES RAPPELS : Pattern 10 (UNE CARTE = UN ROLE) place en tete des indices de c1 (la case Mission, la premiere action de la carte -- l agent voit le role AVANT de choisir une mission) ; Pattern 3 (RAPPEL DES COMBOS) place en tete des indices de c2 (la case action exemple -- l agent pense combo AVANT d enchainer des outils) ; les indices existants (Pattern 7, ASCII) passent en position 2-3 sans conflit.
3. TEXTES DES RAPPELS : Pattern 10 = la carte ne contient QUE des actions propres au role de l agent (activation/verification/decision), JAMAIS d outils d analyse/execution d un autre role + piege du glissement (lire pour DECIDER vs lire pour EXECUTER) ; Pattern 3 = une suite lineaire d outils repetee (>= 2) ou longue (>= 3) doit etre encapsulee dans un combo Lancer le combo X (combos-moteur + definition-combo.json, protocole-creation-combos) -- 1 case = 1 combo.
4. PIEGE CLI CONFIRME (deja note) : generateurs-carte prend l ordre `creer <parcours>` (action avant chemin), generateurs-case `<parcours> <action>` (chemin avant action) -- ne pas copier l ordre de l un dans l autre.
5. PIEGE TEST : ne PAS creer le squelette de test dans /tmp (hors workspace, regle workspace : ecriture = workspace seul) -- creer dans un dossier temporaire DU WORKSPACE (.tmp-gc-test/) puis supprimer apres validation.
6. VALIDATION : py_compile, squelette de test cree (c1 porte Pattern 10, c2 porte Pattern 3 en position 1 + Pattern 7 + ASCII), navigation PARCOURS TERMINE, --liste 7 cases, references validees, ASCII 0 sur py + md, nommage code 0, parite py/sh (wrapper pur = parite par construction), doc .md bumpee v0.1.1 -> v0.2.0 avec ligne de versionning.
7. LA CHAINE CONTINUE (Pattern 8) : Vulcain termine et ACTIVE Morpheus pour tester (c est l agent delegue qui active le suivant a SA fin, pas Cerberus).

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
