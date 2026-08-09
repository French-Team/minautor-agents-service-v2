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

## [LECON] 2026-08-08 -- OUTIL verifier-restauration-sure cree + INCIDENT catalogue ecrase (git checkout) + REGENERATION

**Mission 1 (demande utilisateur)** : creer verifier-restauration-sure (detecte les fichiers non commites avant restauration git - application de la regle Restauration securisee). Cree dans verifier/verifier-restauration-sure/ (.py + .sh wrapper + .md + spec/) : git status --porcelain, mode global (verdict OK/ATTENTION) + mode --fichier (code 0/1), rappel de la regle, parite py/sh. Tests : fichier modifie code 1, fichier sur code 0, hors workspace code 2, parite OK.
**INCIDENT (faute grave, a ne JAMAIS reproduire)** : pendant l ajout de la commande au catalogue generateurs-commande, j ai reecrit le JSON avec json.dumps(indent=1) -> reformatage massif (2997 insertions / 385 suppressions) ; pour l annuler j ai lance git checkout -- catalogue-commandes.json SANS VERIFIER git status -> le fichier avait des modifications NON COMMITEES (la piste A avait porte le catalogue de 13 a 98 commandes, non commitees) -> 85 commandes ECRASEES. C est EXACTEMENT l incident piste B que la regle Restauration securisee interdit. La lecon Buffy (git status avant checkout, sauvegarde cp ou stash) etait connue mais PAS appliquee.
**Reparation** : regeneration complete du catalogue selon la methode piste A (lecon buffy 499-511) : script parse la ligne usage: de chaque outil (--aide/--help, argparse standard ET custom) -> positionnels + flags (avec valeur/booleens) -> modele + parametres ; 13 commandes originales conservees ; entrees speciales corrigees manuellement (10 : valider-nommage, valider-relecture, verifier-systeme, valider-cartes-decision, rechercher-pense-betes/specs/todos, nettoyer-sessions, verifier-restauration-sure, combos-moteur, generateurs-carte). Resultat : 105 commandes (13 originales + 92 ajoutees), 0 script relatif, 0 modele parasite, refs parcours 53/53 couvertes, 13 originales intactes (non-regression combos OK), ASCII 0.
**Lecons** :
1. FAUTE GRAVE : JAMAIS git checkout / git restore / git reset --hard sur des fichiers non commites - la regle existe (regles-general-global + protocole-gestion-defaillances Etape 3) et je l ai VIOLEE. Toujours verifier git status AVANT, sauvegarder (cp) ou git stash.
2. PIEGE json.dumps : reecrire un JSON avec json.dumps(indent different) reformate TOUT le fichier - toujours editer chirurgicalement (inserer les lignes au format exact, indent 2 espaces pour le catalogue, CRLF) ou faire un diff --stat avant/apres.
3. PARSEUR usage: : les flags entre crochets [--debut DEBUT] doivent etre strips AVANT le test startswith(--) ; la continuation multiligne de usage: doit s arreter des qu une ligne n est pas alignee (texte de description) ; le nom du script dans usage: doit etre exclu des positionnels.
4. DEDUPLICATION PAR NOM (pas par script) : 13 commandes originales ont des scripts partages (activer-agent-principal.py couvert par activer-sidentifier/activer/activer-reactiver/activer-sessions ET par activer-agent-principal) - les noms d outils reels doivent etre ajoutes meme si leur script est deja couvert, seuls les doublons de NOM sont exclus.
5. VALIDATION REGENERATION : refs parcours 53/53, 13 originales intactes, 0 parasite {--flag}, 0 script relatif, generation reelle des commandes (valider-nommage --type outil test.py, verifier-restauration-sure --fichier x.md), non-regression combos-moteur --liste, ASCII 0, diff 1961+ / 0-.
6. Outils crees/mis a jour : verifier-restauration-sure (nouveau), index-tools.md (Verifier 4->5, Total 103->104), catalogue-commandes.json (13->105). Le test formel revient a Morpheus (REGLE ABSOLUE).
| VERITE | La regle Restauration securisee protege le travail non commite - mais elle ne sert que si chaque agent la VERIFIE avant toute commande git destructive. Verifier git status, toujours. |

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

## [LECON] 2026-08-08 -- PISTE C VOLET 1 : champ catalogue optionnel sur les indices outil (guider-parcours v0.3.1)

**Mission** : etendre le format des indices outil avec un champ catalogue optionnel (reference a la commande du catalogue generateurs-commande) et l afficher dans guider-parcours. Strategie validee par l utilisateur : champ AJOUTE + commande en dur CONSERVEE comme fallback.
**Lecons** :
1. FORMAT : l indice outil accepte maintenant 4 cles : nom, chemin, commande, catalogue (optionnel) -- le catalogue = nom de la commande dans catalogue-commandes.json, la commande en dur reste le fallback. Le champ est OPTIONNEL : absence = comportement historique, les 11 parcours existants restent PARCOURS TERMINE sans modification.
2. AFFICHAGE : guider-parcours afficher_indices affiche catalogue: <nom> + une ligne PASSE PAR LE GENERATEUR avec la commande du generateur (--commande <nom>) quand le champ est present -- le Pattern 9 (LIRE AVANT USAGE deduit du chemin) reste intact et s affiche dans les deux cas.
3. PARITE : le .sh est un wrapper pur qui delegue au .py (parite par construction) -- le test de parite sur le parcours de test confirme PARITE OK.
4. NON-REGRESSION : la navigation des 11 parcours (sans champ catalogue) reste PARCOURS TERMINE 11/11 -- le champ est strictement additif.
5. PIEGE rfind : inserer du texte en fin de la longue ligne Historique de la spec avec txt.rfind(marker) a cible la mauvaise occurrence (la ligne 12 Agent plutot que la ligne 13) -- pour les lignes uniques et longues, cibler l index de ligne exact (lignes[12] += ajout).
6. VALIDATION : py_compile, bash -n, parite py/sh, navigation avec et sans champ catalogue (parcours de test), non-regression 11/11, ASCII 0 sur 4 fichiers (py/sh/md/spec).
| VERITE | Une reference au catalogue (champ catalogue) rend chaque commande des parcours retracable et recomposable via generateurs-commande, sans casser les commandes en dur existantes |

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
## [LECON] 2026-08-08 -- OUTIL verifier-restauration-sure + INCIDENT catalogue ecrase (git checkout) + REGENERATION

**Mission 1 (demande utilisateur)** : creer verifier-restauration-sure (detecter les fichiers non commites avant restauration git - application de la regle Restauration securisee, lecon incident piste B). Cree dans verifier/verifier-restauration-sure/ (.py + .sh wrapper + .md + spec/) : git status --porcelain, mode global (OK/ATTENTION) + mode --fichier (code 0/1), hors workspace code 2, parite py/sh, rappel de la regle. index-tools mis a jour (104 -> 105).

**INCIDENT (FAUTE GRAVE -- la lecon piste B s est REPRODUITE)** : pendant l ajout de la commande au catalogue, json.dumps(indent=1) a reformate tout le fichier (2997 insertions). Pour annuler, j ai lance `git checkout -- catalogue-commandes.json` SANS verifier l etat de travail : le fichier contenait 98 commandes NON COMMITEES (piste A) -> restaure a 13, 85 commandes perdues. C est EXACTEMENT le scenario de l incident piste B, malgre le garde-fou documente. La regle Restauration securisee etait en memoire mais PAS APPLIQUEE (verifier git status avant).

**REPARATION** : regeneration complete du catalogue selon la methode de la lecon piste A (corrections buffy 499-511) : scan des 94 outils reels (.py hors tester/spec/combos), parsing de l aide (usage: + continuation stricte + filtrage du nom d outil), 13 commandes originales conservees intactes, entrees speciales corrigees (generateurs-carte subcommandes, combos-moteur, verifier-restauration-sure aide custom). RESULTAT : 105 commandes, 0 script relatif, 0 modele parasite ({--flag}), toutes les 53 refs parcours couvertes, non-regression combos OK, generation reelle verifiee (valider-nommage, verifier-restauration-sure).

**LECONS (a integrer)** :
1. JAMAIS git checkout / git restore / git reset --hard sur un fichier NON COMMITE : verifier git status AVANT toute restauration (la regle existe, il faut l APPLIQUER meme en urgence).
2. Les fichiers DERIVES (catalogue-commandes.json genere par script) doivent garder leur script de generation : la regeneration a sauve la mission.
3. json.dumps reformate TOUT un fichier : pour editer un JSON, insertion chirurgicale texte (indentation 2 espaces + CRLF respectes).
4. Un --aide custom (pas argparse) n expose pas usage: -> entree speciale du catalogue.
5. Le parseur doit ignorer le nom de l outil dans usage: (positionnel parasite).
## [LECON] 2026-08-08 -- OUTIL generateurs-regenerer-catalogue cree (remplacant durable du script temporaire piste A)

**Objet** : creer un outil PERMANENT pour regenerer/synchroniser le catalogue-commandes.json du generateur, en extrayant les VRAIES descriptions depuis les en-tetes .py (eviter de re-corriger a la main apres chaque regeneration - lecon piste A : 63 entrees cosmetiques corrigees par Buffy).
**Livrable** : generateurs-regenerer-catalogue/ (.py + .sh wrapper + .md + spec/) dans la categorie generateurs/. Modes : --dry-run (defaut) / application (synchronisation preservant l existant) / --force (reconstruction complete).
**Test de bout en bout** : outil fictif temporaire cree dans generateurs/ -> dry-run le propose avec la description extraite du docstring -> supprime sans residu. Dry-run sur catalogue reel : 86 outils scannes, 82 preserves, 0 a ajouter (aucune regression).
**Lecons** :
1. REGLE NOMNAGE : le nom d un outil DOIT commencer par le prefixe de la CATEGORIE (generateurs-*) - j ai d abord cree regenerer-catalogue/ (ERREUR valider-nommage : prefixe dossier manquant) puis renomme en generateurs-regenerer-catalogue/ (git mv + mv des 4 fichiers).
2. SCHEMA IDENTITE : un outil .py/.sh doit porter le bloc identite: (type/appartient_a/commun) sinon detecter-impacts le signale NON MIGRE - ajoute apres le shebang (comme verifier-systeme).
3. AUTO-EXCLUSION : le regenerateur doit s exclure lui-meme du scan (outil_dir == generateurs-regenerer-catalogue) sinon il s ajouterait a son propre catalogue.
4. La spec est un FICHIER IMPLIQUE de l outil (detecter-impacts la reference) : la toucher apres modification du .py pour passer le VERDICT a jour.
5. Extraction descriptions : 2 formats d en-tete (.py docstring triple-quote / commentaires #), jointure des phrases coupees par : ou ,, translitteration ASCII NFKD, limite ~90 caracteres. Les 13 commandes originales + 3 entrees speciales (generateurs-carte, combos-moteur, verifier-restauration-sure) ne sont jamais regenerees.
6. PIEGE CRLF PARASITE (encore) : normaliser LF en memoire puis reecrire CRLF uniforme - le json.dumps(indent=2) + replace(n, rn) est maintenant la methode propre pour ce fichier.

## [LECON] 2026-08-08 -- DIVERGENCE VERSION generateurs-commande.sh corrigee (parite py/sh)

**Objet** : corriger la divergence de version pre-existante detectee par Morpheus : le .sh affichait VERSION=0.1.0-beta (ligne 18) alors que le .py affiche VERSION=0.2.0 (ligne 41) - le wrapper n'avait jamais ete mis a jour lors des versions successives du .py.

**Correction** : generateurs-commande.sh ligne 18 : VERSION="0.2.0" (alignement sur le .py). STATUT deja coherent (ebauche dans les 2).

**Validations** :
1. Parite --version py/sh OK (texte identique, seul artefact CRLF sous Windows - normalise avec tr -d '\r').
2. Parite --liste OK (contenu des commandes identique).
3. Generation reelle via .sh OK (commande valider-nommage generee correctement).
4. bash -n OK + ASCII 0 non-ASCII.
5. Scan complet des parametres type=choix dans le catalogue : 0 choix vide, 0 trop court sur 105 commandes (le seul cas generateurs-carte avait deja ete corrige par Morpheus avec choix=[creer, analyser, dupliquer]).

**Lecons** :
1. A CHAQUE version du .py d'un outil, verifier que le .sh wrapper est aligne (VERSION, STATUT) - la parite --version doit etre testee a chaque modification (lecon Morpheus T5).
2. Le scan des parametres choix a liste vide doit devenir un reflexe apres toute regeneration du catalogue (lecon Morpheus T3 : le test de generation reelle est le seul moyen de detecter les choix vides).
3. Sous Windows, un diff py/sh peut afficher une fausse divergence due au CRLF - normaliser avec tr -d '\r' avant de conclure.

## [LECON] 2026-08-09 -- REGLE DES 5 FICHIERS apres modification de version (controle Janus)

**Objet** : documenter la regle issue du controle Janus (detecter-impacts, 2026-08-09) : apres TOUTE modification de version d un outil, verifier les 5 fichiers du dossier outil et distinguer les versions propres des fichiers de donnees.

**Contexte** : le controle Janus sur ma modification de generateurs-commande.sh (VERSION 0.2.0) a detecte 1 IMPACT REEL OUBLIE : spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 affichait encore Version : 0.1.0-beta (au lieu de 0.2.0, aligne sur py/sh/md). J avais aligne py/sh mais oublie la spec.

**La regle des 5 fichiers** : apres TOUTE modification de version d un outil, verifier l alignement VERSION (et STATUT) dans les 5 fichiers du dossier outil :
1. `<outil>.py` -- VERSION dans le code
2. `<outil>.sh` -- VERSION dans le wrapper (lecon Morpheus T5 : le wrapper garde souvent une version obsolete)
3. `<outil>.md` -- Version dans l en-tete de documentation
4. `spec/spec-<outil>...md` -- Version dans l en-tete de la spec (CIBLE DE CETTE LECON : c est le fichier le plus souvent oublie)
5. `<catalogue ou index associe>` -- SI le dossier contient un fichier de donnees (ex: catalogue-commandes.json) ou un index : DISTINGUER les versions

**Distinguer les versions propres (ne pas confondre)** :
- `catalogue-commandes.json` a SA PROPRE version top-level (ligne 2, ex: 0.1.0-beta) qui n est PAS la version de l outil : une modification de version de l outil n impose PAS de changer la version du catalogue (fichier de donnees).
- `index-tools.md` reference la version de l INDEX lui-meme (ligne 9, ex: v0.2.0) : pas la version des outils listes.
- Les fichiers qui citent le NOM de l outil sans sa version (parcours des agents, corrections, controles) ne sont PAS impactes par une modification de version.

**Lecon sur detecter-impacts** : les marquages [NON MIS A JOUR] massifs apres une modification sont souvent des ARTEFACTS TEMPORELS (le fichier modifie est plus recent que les fichiers qui le citent). Croiser la NATURE de la modification (version) avec le CONTENU des references (nom vs version) avant de conclure : tous les NON MIS A JOUR ne sont pas des impacts reels.

**Action restante (mission separee)** : corriger spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 : Version 0.1.0-beta -> 0.2.0.

## [LECON] 2026-08-09 -- IMPACT SPEC CORRIGE : spec-generateurs-commande Version 0.1.0-beta -> 0.2.0 (regle des 5 fichiers appliquee)

**Objet** : corriger l impact reel oublie detecte par le controle Janus : la spec de generateurs-commande affichait Version 0.1.0-beta alors que py/sh/md etaient en 0.2.0. C etait l action restante de la lecon des 5 fichiers.

**Correction** : spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 : Version : 0.1.0-beta -> Version : 0.2.0 (edition chirurgicale, CRLF preserve).

**Validations** :
1. Une seule occurrence de 0.1.0-beta dans la spec (ligne 10) - aucune autre a corriger.
2. 0.1.0-beta absent apres correction, 0.2.0 present (1 occurrence).
3. valider-conformite-ascii : 0 non-ASCII.
4. CRLF preserve (89/89).
5. detecter-impacts sur la spec : 2 fichiers NON MIS A JOUR (janus/corrections.md, vulcain/corrections.md) = ARTEFACTS (rapports/lecons qui documentent l incident, pas des references de version a aligner).
6. Dossier outil desormais ALIGNE : py=0.2.0, sh=0.2.0, md=0.2.0, spec=0.2.0 (les 4 fichiers de version).

**Lecons** :
1. La regle des 5 fichiers (documentee le 2026-08-09) est appliquee : apres toute modification de version, py/sh/md/spec doivent etre alignes. La spec est bien le fichier le plus souvent oublie - exactement ce que la lecon predic.
2. detecter-impacts apres modification de la spec signale les rapports/lecons qui documentent l incident : ce sont des artefacts (contexte documentaire), pas des impacts reels - croiser avec la nature de la modification (version) et le contenu des references.
3. La boucle est complete : controle Janus (impact detecte) -> lecon des 5 fichiers (documentee) -> indice de carte c12 (v0.2.4) -> correction de l impact (spec 0.2.0). Cercle vertueux lecon -> carte -> application -> verification.

## [LECON] 2026-08-09 -- OUTIL detecter-divergences-version cree (scan durable des spec divergentes)

**Objet** : creer un outil DURABLE pour remplacer les scripts temporaires de Janus (.tmp-scan-versions*.py) qui scannaient les spec/ divergentes de leur .py (regle des 5 fichiers).

**Livrable** : detecter/detecter-divergences-version/ (.py + .sh wrapper + .md + spec/ + bloc identite). Scan recursif des spec/ sous une racine, extraction de la version spec (5 formats : en-tete prioritaire, tableau frontmatter, versionning, titre, tableau historique - lecon Janus), croisement avec la version VERSION= du .py associe, verdicts ALIGNE / DIVERGENT (base) / DIVERGENT (suffixe) / SANS VERSION / SANS PY. Options : --racine (defaut cerveau-projet), --liste, --export, --version.

**Validations** :
1. Scan reel : retrouve les 6 divergences de Janus (regenerer-catalogue 0.1.0 vs 1.0.0, lister-agents, lister-outils, verifier-systeme, combos-moteur suffixe, guider-parcours) + 1 decouverte (activer-agent-principal : spec historique 0.3.4 vs py 0.5.0 avec ligne d historique MALFORMEE - 2 colonnes sans date).
2. py_compile + bash -n OK ; valider-nommage OK ; ASCII 0 sur les 4 fichiers ; parite --version py/sh OK (via python - normaliser le CRLF, le diff shell affiche un faux positif).
3. detecter-impacts : identite reconnue, 3 fichiers du dossier [A JOUR].
4. index-tools : Detecter 5->6, Total 105->106, ligne ajoutee.
5. Catalogue generateurs-commande : entree ajoutee par regenerateur (106 commandes), puis CORRIGEE (le regenerateur a cree un parametre 'chemin' positionnel au lieu de 'racine' avec defaut ; corrige en modele '--racine {racine}' + defaut cerveau-projet) - generation reelle OK.

**Lecons** :
1. Le regenerateur de catalogue cree des parametres par defaut (positionnels 'chemin') qui ne correspondent pas toujours a l'API reelle de l'outil (flags comme --racine) : VERIFIER la generation reelle via generateurs-commande apres synchronisation et corriger l'entree en entree SPECIALE si besoin.
2. L'extraction de version des spec a 5 formats + la priorite en-tete (lecon Janus) est maintenant DUPLIQUEE dans un outil durable : ne plus scanner a la main.
3. Les spec avec lignes d'historique MALFORMEES (2 colonnes sans date) peuvent induire l'extraction en erreur : les signaler (cas activer-agent-principal) pour nettoyage, sans conclure seul.
4. La boucle lecon -> outil -> verification est complete : le scan manuel de Janus devient un outil reutilisable pour le prochain controle.

---

## [LECON] 2026-08-09 -- CORRECTION 6 DIVERGENCES spec/py (regle des 5 fichiers)

**Mission** : aligner les 5 spec divergentes sur leur .py + documenter le cas particulier guider-parcours.
**Contexte** : suite du scan detecter-divergences-version (outil cree ce jour) qui avait revele 6 spec divergentes sur 11.

**Actions realisees** :
1. **generateurs-regenerer-catalogue** : spec 0.1.0 -> 1.0.0 (3 emplacements : en-tete `# Version :`, frontmatter `version:`, titre historique) -- alignee sur py 1.0.0
2. **lister-agents** : spec 0.2.0 -> 0.4.0-py (tableau historique + reference texte) -- alignee sur py 0.4.0-py
3. **lister-outils** : spec 0.2.0 -> 0.3.0-py (tableau historique) -- alignee sur py 0.3.0-py
4. **verifier-systeme** : spec 0.2.0 -> 0.2.1-py (tableau historique) -- alignee sur py 0.2.1-py
5. **combos-moteur** : spec 0.2.0-ebauche -> 0.2.0-beta (en-tete) -- alignee sur py 0.2.0-beta (suffixe coherent)
6. **guider-parcours** : CAS LEGITIME ASSUME -- la spec versionne les PATTERNS v0.2.x (0.2.20), distincts de l'outil 0.3.1. Decision : documenter dans le .md de detecter-divergences-version comme cas legitime, NE PAS aligner la spec.

**Lecons** :
1. Une spec peut porter sa version a PLUSIEURS endroits (en-tete, frontmatter, titre, tableau historique, reference texte) : TOUT aligner, pas seulement le premier trouve
2. La version d'EN-TETE prime, mais les spec " prepare " (sans champ Version d'en-tete) portent leur version dans le TABLEAU HISTORIQUE -- verifier le format avant de chercher
3. Distinguer divergence de BASE (regenerer-catalogue 0.1.0 vs 1.0.0 = ecart majeur) vs de SUFFIXE (combos-moteur ebauche vs beta = coherence de suffixe)
4. Cas legitimes assumes (guider-parcours, prototype vulcain) : ne PAS aligner aveuglement -- documenter la decision dans l'outil qui scanne pour eviter les faux positifs repetitifs
5. Verifier l'ASCII sur CHAQUE fichier modifie apres edition chirurgicale (0 non-ASCII sur les 6)

**Validation finale** : rescan detecter-divergences-version = 5 spec ALIGNEES, 2 divergences restantes = guider-parcours (cas legitime documente) + activer-agent-principal (hors perimetre, ligne d'historique malformee a nettoyer separement).

---

## [LECON] 2026-08-09 -- LIGNES HISTORIQUE SANS DATE = IGNOREES par detecter-divergences-version

**Mission** : corriger les 2 lignes d'historique malformees de la spec activer-agent-principal (faux divergent).

**Contexte** : l'outil detecter-divergences-version lit la version d'une spec prepare dans le tableau historique via la regex `| AAAA-MM-JJ | version |` (derniere ligne avec date). Les lignes SANS DATE sont IGNOREES -> l'outil retombe sur la derniere ligne DATER (0.3.4) au lieu de la version courante reelle (0.5.0) -> faux DIVERGENT.

**Actions realisees** :
1. Ligne 290 : `| 0.3.2 | Vulcain | ...` -> `| 2026-08-07 | 0.3.2 | Vulcain | ...` (date verifiee par git blame, commit 55994e04)
2. Ligne 291 : `| 0.5.0 | Vulcain | ...` -> `| 2026-08-08 | 0.5.0 | Vulcain | ...` (date verifiee par git blame, commit 993738a6)

**Lecons** :
1. Les lignes du tableau historique d'une spec DOIVENT TOUJOURS porter leur date reelle (AAAA-MM-JJ) : sans date, detecter-divergences-version les ignore et lit une version anterieure -> faux divergent
2. Ne JAMAIS inventer une date : utiliser `git blame -L <lignes> --date=short <fichier>` pour retrouver la date de modification reelle
3. Apres correction, RESCAN avec l'outil pour confirmer le passage ALIGNE (boucle de validation)

**Validation finale** : rescan = activer-agent-principal ALIGNE (0.5.0 = 0.5.0) ; synthese 12 spec | 9 ALIGNEES | 1 DIVERGENT (guider-parcours = cas legitime assume documente) | 2 SANS VERSION/SPEC ; ASCII 0 ; CRLF preserve 291/291.
## [LECON] 2026-08-09 -- valider-nommage v0.3.2 (formats speciaux combos/tests)

**Mission** : faire evoluer valider-nommage pour reconnaitre les 2 formats speciaux et eliminer les bruits preexistants (definition-combo.json + test-XXX-*.py).
**Lecons** :
1. Les formats speciaux LEGITIMES doivent etre reconnus par l outil, pas documentes comme bruit : definition-combo.json (dossier combos/combo-*/) et test-XXX-nom-outil.(py|sh|md) (dossier tests/test-XXX-*/) passent maintenant avec 0 ERREUR - la detection repose sur le DOSSIER PARENT (prefixe combo- / test-) en plus du nom du fichier
2. La regle est : un format special est accepte quand le nom du fichier ET le dossier parent sont coherents (definition-combo.json DANS combos/combo-*, test-XXX-* DANS tests/test-XXX-*) - eviter d accepter trop large (ex: n importe quel .json dans combos/)
3. PARITE py/sh : la meme logique doit etre portee dans les 2 fichiers (regex bash vs PATTERN_OUTIL python) et verifiee par --version (v0.3.2-py / v0.3.2) + tests croises (meme fichier -> meme resultat)
4. REGLE DES 5 FICHIERS : apres toute modification de version d un outil py+sh, verifier py, sh, md (versionning + doc) + spec + catalogue/index le cas echeant - ici md mis a jour avec la ligne 0.3.2
5. NON-REGRESSION : verifier 3 cas apres modification : les formats speciaux passent (0 ERREUR), les outils normaux passent toujours, les VRAIS mauvais nommages restent detectes (cree un fichier reel mal nomme dans le workspace - un fichier inexistant donne 0 ERREUR et fausse la verification)
6. Le test formel v0.3.0 (tester-valider-nommage-v030.sh, 13/13) passe toujours - le mode --mots-seuls non regresse

**Validation finale** : v0.3.2-py/v0.3.2, 15 combos 0 ERREUR, 4 tests 0 ERREUR, mauvais nommage detecte, test v0.3.0 13/13, ASCII 0 sur 3 fichiers.
## [LECON] 2026-08-09 -- CORRECTION CATALOGUE valider-relecture (suite test reel Atlas)

**Contexte** : le test reel d Atlas a revele que l entree catalogue valider-relecture composait --fichier {fichier} alors que l outil v0.2.0-py utilise --agent <nom> (+ --verbose optionnel) -> ERREUR Option inconnue : --fichier. C etait le SEUL vrai decalage du catalogue (scan 106 entrees : valider-nommage et verifier-systeme = faux positifs --help vs --aide).

**Correction appliquee** :
1. catalogue-commandes.json v0.2.0 -> v0.2.1 : modele "--agent {agent} {verbose}", parametres agent (texte, obligatoire) + verbose (type flag, flag --verbose, optionnel) - format identique a analyser-dependances/inverse
2. generateurs-commande.md : mention "Catalogue v0.2.0 : 106 commandes" -> "Catalogue v0.2.1 : 106 commandes" (regle des 5 fichiers : catalogue + doc .md alignes; la spec ne mentionne pas la version du catalogue - rien a faire)
3. test-005 point 14 : verifiait catalogue version == 0.2.0 en dur -> obsolete apres bump -> aligne 0.2.1 (2 lignes : description + verifier) -> 26/26 VALIDE

**Validations** : JSON valide 106 commandes, composition py/sh identique (--agent atlas), verbose=oui -> --verbose present, execution reelle code 0 [OK], navigation atlas c8 affiche catalogue + PASSE PAR LE GENERATEUR SANS commande en dur, ASCII 0 sur catalogue/doc/test, regenerateur dry-run 83 preserves 0 ajoute (correction survivra).

**Lecons** :
1. UN TEST REEL VAUT PLUS QU UN TEST FORMELL : c est l execution reelle (Atlas) qui a revele le decalage modele/interface que les 26 points du test-005 ne voyaient pas - toujours comparer le modele du catalogue a l interface reelle (--aide) quand on cree/modifie une entree
2. UN TEST QUI VERIFIE UNE VERSION EXACTE devient obsolete des que la version change legitimement - l aligner (ou le signaler a Morpheus) plutot que de figer la version pour satisfaire le test
3. detecter-impacts signale des fichiers reference qui mentionnent le CHEMIN du catalogue (dependance stable, ex: protocole-creation-combos) : faux positifs si la version du catalogue n y figure pas - verifier le CONTENU avant de conclure a une non-mise a jour
4. La regle des 5 fichiers s applique au couple catalogue + doc .md (version du catalogue documentee); la spec ne la porte pas toujours - verifier les 2 endroits (doc + spec) quand on bumpe le catalogue
## [LECON] 2026-08-09 -- INSTITUTIONNALISATION detecter-decalages-catalogue (infraction Atlas corrigee)

**Contexte** : Atlas (explorateur) avait ecrit scan-catalogue.py dans son dossier explorations/ pendant son audit - DOUBLE INFRACTION : (a) les outils vivent dans agents/tools/<categorie>/<outil>/ et non dans le dossier d un agent, (b) un explorateur n est pas habilite a creer des outils (role Vulcain). Mission : institutionnaliser l outil (deplacer + structure officielle) et garder le rapport comme trace dans explorations/.

**Actions** : deplacement vers tools/detecter/detecter-decalages-catalogue/ (renommage detecter-decalages-catalogue, prefixe de categorie, meme famille que detecter-divergences-version) ; structure officielle py (identite) + sh (wrapper pur) + md (LIRE AVANT USAGE) + spec + entree catalogue (v0.2.1 -> v0.2.2, 106 -> 107) + index-tools.md + doc generateurs-commande.md (Catalogue v0.2.2 : 107 commandes) + test-005 point 14 aligne (0.2.1 -> 0.2.2) ; RACINE corrigee (5 niveaux a explorations/, 6 niveaux a tools/detecter/<outil>/).

**Validations** : py_compile + bash -n OK, --version v0.1.0, nommage 0 ERREUR, ASCII 7/7, composition generateur --sortie present / retire si vide, execution reelle rapport + synthese (106 conformes / 0 decalage / 1 non testable = test formel / 0 alerte), test-005 26/26, regenerateur dry-run 88 scannes 84 preserves 0 ajoute, detecter-impacts VERDICT tous a jour.

**Lecons** :
1. UNE CARTE = UN ROLE (Pattern 10) : un explorateur qui decouvre un besoin d OUTIL signale a Cerberus (qui active Vulcain), il ne cree pas l outil - meme si le script semble simple et utile
2. TRACE vs OUTIL : un rapport de mission vit dans le dossier de l agent (explorations/, controles/) ; un script reutilisable vit dans tools/ avec la structure officielle - ne jamais melanger
3. RACINE : le nombre de niveaux .. dans un script = profondeur du dossier depuis la racine (explorations/ = 5, tools/detecter/<outil>/ = 6) - a recalculer a chaque deplacement
4. MODELE DU CATALOGUE = INTERFACE REELLE : `{sortie}` compose en positionnel, `--sortie {sortie}` compose le flag - TOUJOURS tester la commande generee contre l interface de l outil (le scan l a revele)
5. AJOUTER UN OUTIL AU CATALOGUE = bump de version + alignement doc (compteur 106 -> 107) + test-005 (point 14 version en dur) - la regle des 5 fichiers s etend au trio catalogue/doc/test
6. Le regenerateur preserve les entrees manuelles (dry-run 84 preserves) : ajouter l entree dans le catalogue est sur et rejouable
## [LECON] 2026-08-09 -- OUTIL cartographier-parcours cree (v0.1.0, categorie cartographier/)

**Mission** : creer l outil cartographier-parcours (decision utilisateur - Atlas cartographie le parcours d un agent dans un fichier pour ses analyses rapides). Decisions : sortie = dossier du parcours audite (cartographie-<agent>.md), format = arbre ASCII, branchement carte Atlas = mission Buffy ulterieure.
**Livrables** : cartographier-parcours.py (lecture seule, 100% stdlib, ASCII strict) + .sh (wrapper pur exec python3) + .md + spec/ + entree catalogue-commandes.json (107 -> 108) + index-tools.md (nouvelle categorie Cartographier, total 106 -> 107).
**Rendu** : en-tete (agent, version, depart, nb cases, nb chemins) + arbre ASCII (1ere occurrence, branches marquees, [convergence] pour les re-visites, `|--` / `--`) + impasses + boucles + chemins BFS (logique reutilisee de generateurs-carte analyser).
**Lecons** :
1. REUTILISATION : la detection des chemins (BFS anti-boucle, impasses) existe deja dans generateurs-carte analyser - je l ai portee au lieu de la reimplementer. La cartographie est un RENDU en fichier de ce que generateurs-carte affiche en console.
2. ARBRE ASCII : le premier jet affichait les cases 2 fois (branche de c0 + noeud enfant) - correction : fonction descendre(cid, prefixe, lien, contexte) avec affichees set (1ere occurrence) et marquage [convergence], liens |-- / `-- selon derniere branche.
3. PIEGE INSERTION CATALOGUE (grave, a ne jamais refaire) : inserer une entree JSON dans le catalogue par concatenation de lignes a MAL indente (6/8 espaces au lieu de 4/6) - le JSON est reste valide PAR CHANCE apres 5 reparations (retrait de blocs residuels + reinsertion au bon niveau + repositionnement alphabetique). REGLE : pour ajouter une entree au catalogue, copier le bloc d une entree EXISTANTE avec l outil lire-fichier/editer-fichier (indentation exacte 4/6/10), ou utiliser generateurs-regenerer-catalogue qui regenere tout - JAMAIS d insertion manuelle a la volee.
4. PIEGE ASCII DOC : les guillemets francais ' ' et les accents (complete) passes dans le .md et la spec - detectes par valider-conformite-ascii (4 + 5 caracteres) et corriges. VERIFIER valider-conformite-ascii sur TOUS les fichiers crees AVANT de declarer l outil pret (md + spec inclus, pas seulement py/sh).
5. PARITE .sh : wrapper pur (exec python3 "$PY_SCRIPT" "$@") - la parite des sorties est garantie PAR CONSTRUCTION (pattern detecter-impacts, valider-cartes-decision). Version py/sh identiques (v0.1.0).
6. REGLE DES 5 FICHIERS : py, sh, md, spec, tests/ - les tests formels sont DELEGUES a Morpheus (REGLE ABSOLUE), pas ecrits par moi.
7. L OUTIL EST EN LECTURE SEULE : il ne modifie jamais le parcours source - le fichier genere est un derive (comme detecter-impacts genere un rapport).
## [LECON] 2026-08-09 -- PLAN FIGER LF : outil corriger-fins-de-ligne cree + outils d ecriture corriges

**Contexte** : diagnostic Cerberus (decision utilisateur) : la regle immuable exige LF mais nos outils d ecriture produisaient du CRLF (creer-fichier.py ecrivait via Path.write_text -> traduction CRLF Windows) et detecter-usage-outils-externes les sanctionnait comme traces d outils externes -> boucle de conflits permanente. Git autocrlf=true aggravait (warnings checkout).

**Livrables** :
1. OUTIL corriger-fins-de-ligne v0.1.0 (categorie corriger/) : py + sh (wrapper pur) + md + spec + entree catalogue (108 -> 109, v0.2.2 -> v0.2.3) + index-tools (categorie Corriger 5 -> 6, total 107 -> 108). Fonctions : fichier/dossier --recursive, --dry-run, --verbose, detection binaire (octet nul) ignore, idempotent (2e passe = 0 converti), erreur chemin introuvable.
2. 11 OUTILS D ECRITURE CORRIGES pour produire du LF (newline='' sur open texte, ou open explicite a la place de write_text) : creer-fichier (write_text -> open newline=''), ecrire-fichier (backup + ecriture + append), ajouter-contenu-fichier, inserer-contenu-fichier, gerer-sous-mission (json.dump), generateurs-squelette-pense-bete/spec/todo, creer-remplir-pense-bete/spec/todo (write_text -> open).

**Validations** : py_compile 12/12 + bash -n, --version py/sh identiques v0.1.0, dry-run sans modification, conversion reelle CRLF->LF verifiee octets, idempotence, binaire intact, erreur chemin, TEST REEL : creer-fichier ecrit desormais du LF (CRLF:0 LF:1), ASCII 0 sur 12 fichiers modifies, catalogue JSON valide 109 trie, generateur compose la commande.

**Lecons** :
1. LA CAUSE RACINE DU CRLF ETAIT NOS OUTILS, pas Git : Path.write_text() et open() en mode texte traduisent \n en \r\n sur Windows. Git autocrlf=true n etait qu un amplificateur. Corriger les outils = tarir la source ; .gitattributes = figer le depot (mission 2 Buffy).
2. LE SCAN DES ECRITURES : open(..., 'w'/'a'...) SANS newline= et write_text() = sources de CRLF. Le mode binaire ('wb') est safe. Pattern correct : open(f, 'w', encoding='utf-8', newline='') (comme remplacer-texte.py).
3. NE PAS TOUCHER AUX TESTS DE MORPHEUS : les tests (test-002, test-006) ecrivent volontairement des fichiers invalides - hors perimetre, laisse tels quels.
4. INSERTION CATALOGUE : manipulation JSON programmatique (json.load -> insertion dans la liste a la position triee -> json.dumps(ensure_ascii=True, indent=2)) = fiable a 100% ; l insertion par concatenation de lignes (lecon cartographier-parcours) reste INTERDITE.
5. LES FICHIERS .pyc COMMITES : py_compile regenere les .pyc -> les restaurer avec git restore (fichiers commites) pour ne pas polluer le working tree.
6. PIEGE HEREDOC : les scripts heredoc avec backslashes echouent en JSON - ecrire les scripts dans des fichiers .tmp puis les executer.
## [LECON] 2026-08-09 -- TESTS OBSOLETES CORRIGES (versions en dur alignees sur la realite)

**Contexte** : la non-regression post-migration FIGER LF (Morpheus) a revele que 2 tests codent des versions en dur devenues obsoletes apres des bumps legitimes : test-004 (parcours morpheus v0.1.2) et test-005 (catalogue 0.2.2, atlas v0.1.2).

**Livrables** :
1. test-004-combos-tester-outil.py : v0.1.2 -> v0.1.3 (3 occurrences : docstring, commentaire, verifier 7a) + .md (1 occurrence).
2. test-005-generateurs-commande.py : catalogue 0.2.2 -> 0.2.3 (docstring + verifier 14), atlas v0.1.2 -> v0.1.5 (docstring, titre, commentaire de section x2, verifier 17, except 17) + note historique v0.1.2 -> v0.1.5 ajoutee + .md (titre, description, tableau d evolution complete, section 17).

**Resultats** : test-004 16/16 VALIDE (avant 15/16), test-005 25 OK / 1 KO (avant 23/26) - seul KO restant = point 18 (1 commande en dur restante case c30 atlas = PISTE C, mission separee, NON modifie).

**Validations** : ASCII 0 sur les 4 fichiers, LF pur (CRLF 0), py_compile OK, aucun fichier cree hors test.

**Lecons** :
1. Les tests qui verifient une version doivent etre mis a jour A CHAQUE bump de version du fichier cible - c est la regle des 5 fichiers appliquee aux tests.
2. NE PAS toucher les versions du generateur (v0.2.1) : seules les 3 versions cibles (morpheus 0.1.3, catalogue 0.2.3, atlas 0.1.5) etaient obsoletes - verifier la SOURCE DE VERITE avant de remplacer.
3. Les notes historiques (v0.1.1 -> v0.1.2) sont PRESERVEES et completees (ajout d une ligne v0.1.2 -> v0.1.5) - ne jamais effacer l historique.
4. Le point 18 (piste C) reste KO volontairement : la mission ne couvre pas la conversion de la derniere commande en dur (case c30 atlas).
## [LECON] 2026-08-09 -- FAUX POSITIF EVALUER-COHERENCE CORRIGE (scan limite aux 11 agents)

**Contexte** : la non-regression post-migration (Morpheus) a revele que evaluer-coherence signalait 4 outils introuvables (statut-mission, contexte, resultats, erreurs) - en realite des VARIABLES du classeur-variables, pas des outils.

**Cause racine** : la section 4 (Outils references par les agents) des 2 versions py et sh iterait sur TOUS les dossiers de agents/ ayant un fichier nom.md. Le dossier classeur-variables/ possede classeur-variables.md et etait donc scanne comme une fiche d agent, ses variables entre backticks etant interpretees comme des outils inexistants.

**Correction structurelle** : scan limite aux 11 agents officiels (AGENTS_ATTENDUS) au lieu de os.listdir (py) / find -type d (sh). classeur-variables/ et tout futur dossier non-agent sont ignores PAR CONCEPTION (pas une liste d exclusion a maintenir, mais un scan borne).

**Versions** : bump 0.2.1 vers 0.2.2 dans py (VERSION + docstring), sh (VERSION + en-tete), md (Version + tableau Versionning). Pas de spec existante.

**Verifications** : py et sh affichent tous deux OK Tous les outils references existent (0 faux positif), parite py/sh confirmee, test-001-evaluer-agents-coherence 8/8 REUSSI (le point 6 attendait deja cette correction), ASCII 0, LF pur, py_compile + bash -n OK, 0 residu.

**Lecons** :
1. Un scan qui itere sur os.listdir / find -type d d un dossier racine balaye TOUS les sous-dossiers, pas seulement les cibles prevues - borner le scan a une liste explicite (AGENTS_ATTENDUS) est plus robuste qu ajouter des exclusions une par une.
2. Le classeur-variables est un dossier de DONNEES dans agents/, pas une fiche d agent : il ne doit jamais etre scanne comme tel.
3. Le .sh de evaluer-coherence est lent par conception (2 find par backtick par fiche : ~100s) - c est un comportement connu, la version py est la reference pour l usage courant.
4. Parite py/sh : appliquer la MEME correction aux 2 versions, puis prouver la parite en executant les 2 (sorties identiques sur la section corrigee).
## [LECON] 2026-08-09 -- ECART P14 : identification vulcain.md mise a jour (parcours v0.2.8)

**Mission** : corriger l'ecart P14 du re-audit Themis -- vulcain.md (mtime 11:02) plus ancien que parcours-vulcain.json (mtime 13:05, v0.2.8).

**Actions** :
1. Section PARCOURS de vulcain.md : mention parcours v0.2.8 ajoutee au lien Parcours.
2. Spec du format alignee v0.2.5 -> v0.2.25 (version reelle de la spec-guider-parcours).
3. Entree d'historique 2026-08-09 ajoutee (corrections Buffy P2 + P12, bump v0.2.7 -> v0.2.8).

**Resultats** : vulcain.md passe de NON MIS A JOUR a A JOUR dans detecter-impacts (mtime 13:09 > 13:05). ASCII 0, LF pur.

**Lecons** :
1. Une fiche d'agent reference son parcours comme SOURCE DE VERITE : a chaque bump de version du parcours par un autre agent (Buffy, etc.), la fiche doit etre mise a jour en meme temps -- sinon detecter-impacts la signale NON MIS A JOUR (Pattern 14).
2. La spec du format est referencee dans la fiche (spec-guider-parcours) : sa version doit rester alignee (v0.2.25 ici) pour eviter des references obsoletes.
3. Les notes de mission (mission-*.md, priorite-outils.md, resume-creation-outils.md) sont des documents figes (type: note, sans champ version) : detecter-impacts les signale mais c'est une JUSTIFICATION legitime -- il ne faut pas les toucher pour le seul plaisir d'un mtime recent.
4. detecter-impacts compare les mtime : apres toute edition, verifier que le fichier cible est bien plus recent que la modification source avant de conclure.
## [LECON] 2026-08-09 -- PATTERN 15 MODE MONO-LLM documente dans la spec-guider-parcours (v0.2.26)

**Mission** : documenter le Pattern 15 (MODE MONO-LLM) dans la spec-guider-parcours apres le diagnostic Cerberus (2 missions arretees apres l'activation de Themis).

**Diagnostic (Cerberus)** : la carte de Cerberus case c10 ordonne de continuer (suivant c7) ; activer-agent-principal.py ne fait AUCUN sous-processus (0 subprocess/os.system/Popen/exec) -- il ecrit 3 fichiers de trace ; en mode multi-LLM l'arret apres activation est correct (un autre LLM reprend) ; en mode mono-LLM l'arret bloque la mission.

**Modifications spec-guider-parcours (v0.2.25 -> v0.2.26)** :
1. Titre aligne v0.2.19 -> v0.2.26 (decalage preexistant corrige).
2. Pattern 15 insere apres le Pattern 14 (regles : l'activation ne clot PAS le tour, l'agent active est joue immediatement dans le meme tour, l'arret n'est valable qu'en mode multi-LLM).
3. Procedure 4c renommee RE-AUDIT COMPLET DES 15 PATTERNS + procedure 4m (mode mono-llm) ajoutee.
4. Critere 26 (MODE MONO-LLM) ajoute a la section criteres d'acceptation (1 a 26).
5. Historique + Agent (ligne 12/13) : entree v0.2.26 ajoutee.
6. Section Patterns valides en production : 14 -> 15 patterns.

**Impacts alignes (Pattern 14)** : vulcain.md (spec v0.2.25 -> v0.2.26), guider-parcours.md (spec v0.2.5 -> v0.2.26 -- reference obsolete de longue date corrigee au passage). Les fiches agents referencent la spec sans version precise : pas d'impact de version.

**Validations** : ASCII 0 + LF pur sur les 3 fichiers modifies (spec, vulcain.md, guider-parcours.md), coherence verifiee (6 occurrences Pattern 15, 11 occurrences v0.2.26, 5 occurrences 15 patterns), 0 residu .tmp.

**Lecons** :
1. Un diagnostic d'arret de mission doit distinguer : la carte (structure), l'outil (mecanisme) et le comportement LLM (execution) -- ici les 3 niveaux ont ete examines, la cause etait le comportement mono-LLM.
2. Le titre d'une spec peut prendre du retard par rapport a son historique : verifier le titre (ligne # Spec) a chaque bump, pas seulement l'historique.
3. Une spec modifiee IMPACTE les fichiers qui la referencent avec une version : verifier avec detecter-impacts ET grep des versions dans les fiches/docs.
## [LECON] 2026-08-09 -- CORRECTION Pattern 15 v0.2.27 : JAMAIS D'ARRET, meme en multi-LLM

**Mission** : corriger le Pattern 15 (v0.2.26) qui autorisait l'arret apres activation en mode multi-LLM. Correction utilisateur : les LLM travaillent EN PARALLELE chacun dans sa session -- l'activation documente le role de SA session uniquement, elle ne delegue JAMAIS l'execution a un autre LLM (aucun relais n'existe).

**Modifications spec-guider-parcours (v0.2.26 -> v0.2.27)** :
1. Titre du Pattern 15 : 'MODE MONO-LLM' -> 'JAMAIS D ARRET APRES L ACTIVATION'.
2. Intro : suppression de la fausse idee de relais (un AUTRE LLM prend le relais) -> les LLM travaillent en parallele, l'activation documente le role de SA session uniquement.
3. Regle 3 : 'l'arret n'est VALABLE qu'en mode multi-LLM' -> 'l'arret est TOUJOURS fautif dans AUCUN mode'.
4. Regle 5 : suppression du cas particulier qui autorisait l'arret en multi-LLM.
5. Conclusion : pas d'arret dans AUCUN mode (mono comme multi).
6. Critere 26 : renomme 'JAMAIS D ARRET APRES L ACTIVATION (v0.2.27)' avec la meme correction.
7. Versions : titre + historique + Agent + patterns valides + procedure 4c/4m -> v0.2.27.
8. Impacts alignes : vulcain.md et guider-parcours.md (spec v0.2.26 -> v0.2.27).

**Validations** : 0 formulation fautive restante (la seule occurrence restante est la trace HISTORIQUE de v0.2.26 dans la ligne 13, suivie de la correction v0.2.27 -- comportement correct de l'historique), 11x v0.2.27, ASCII 0 + LF pur sur les 3 fichiers, 0 residu.

**Lecons** :
1. Une regle documentee peut etre corrigee par l'utilisateur quelques minutes apres sa creation : l'historique doit TRACER la version fautive PUIS la correction (ne pas effacer la trace), mais le CORPS du pattern doit etre corrige partout (intro, regles, conclusion, critere).
2. Le mode multi-LLM n'implique AUCUN relais : chaque LLM travaille en parallele dans sa session. La delegation entre agents est un changement de ROLE dans la meme session, jamais un transfert vers un autre LLM.
3. Quand l'utilisateur corrige une formulation, verifier TOUTES les occurrences (intro, regles, conclusion, critere, historique) -- un grep cible ('valable qu.en mode multi-LLM') confirme qu'il ne reste que la trace historique legitime.
## [LECON] 2026-08-09 -- OUTIL generateurs-outil-temporaire cree (generateur d'outil temporaire standardise)

**Mission** : creer le generateur d'outil temporaire (design utilisateur valide : tous les agents habilites, promotion systematique a la 2e utilisation, forme Python seul). Outil cree : py + sh + md + spec + index-tools + entree catalogue (110 commandes).

**Comportement de l'outil** : genere un script `tmp-<besoin>.py` DANS le workspace uniquement (jamais hors workspace, jamais dans tools/), en-tete standard (identite type: outil-temporaire, ASCII strict, LF, 100% stdlib, version 0.1.0-tmp), dry-run par defaut (--force pour ecrire), refuse l'ecrasement, et affiche la QUESTION DE PROMOTION a la fin : besoin recurrent (2e utilisation) ? -> OUI = ACTIVER VULCAIN directement (maillon de chaine), Vulcain cree l'outil durable (protocole 5 fichiers) puis REACTIVE L'AGENT PRECEDENT.

**Lecons** :
1. PIEGE DOUBLE PREFIXE : le nom du besoin est deja prefixe tmp- (ex: tmp-mesurer-taille) ; le template du script genere NE doit PAS re-ajouter tmp- dans le docstring/print (le double tmp-tmp-mesurer-taille est apparu au test). Passer le nom avec prefixe au template et l'utiliser tel quel.
2. PIEGE INSERTION JSON DANS UN CATALOGUE : pour inserer une entree apres un bloc, ne JAMAIS chercher la premiere ligne '},' (c'est la fermeture du PREMIER sous-objet, ex: le premier parametre) -- il faut partir de la ligne '{' d'ouverture du bloc et compter les accolades (avec gestion des chaines) jusqu'au '}' qui ramene a 0. Ma 1re tentative a insere l'entree AU MILIEU de la liste parametres de generateurs-commande (JSON restait valide mais entree parasite).
3. PIEGE REFORMATAGE JSON : ne jamais re-ecrire un catalogue avec json.dumps global (le format du fichier n'est pas un json.dumps standard : diff 47% a indent=2) -- reparer CHIRURGICALEMENT par lignes (supprimer le bloc parasite, inserer l'entree bien formatee a la bonne indentation) puis verifier git diff minimal (ici -29/+29 = parasite supprime + bonne entree).
4. Detection du workspace : remonter depuis le script jusqu'au dossier contenant AGENTS.md (marqueur robuste, fonctionne pour toutes les racines).
5. Verification systematique : nommage valider-nommage OK, ASCII 0 sur les 5 fichiers + index, LF pur, parite py/sh (--version, dry-run, generation reelle), test bout en bout (generation + execution du script genere + suppression 0 residu), detecter-impacts A JOUR.
## [LECON] 2026-08-09 -- GUILLEMETS FRANCAIS AJOUTES AU DICTIONNAIRE (v0.2.1)

**Mission** : ameliorer les outils corriger pour couvrir les guillemets francais U+00AB/U+00BB (lecon Themis du 2026-08-09 : l outil repondait [OK] Aucune correction necessaire alors que le fichier contenait des guillemets francais).

**Modifications** (7 fichiers) :
1. Dictionnaire partage `corriger-dictionnaire-accents.txt` : +2 entrees U+00AB et U+00BB vers guillemet droit double (coherent avec les guillemets courbes U+201C/U+201D qui vont deja vers le guillemet droit).
2. Les 2 outils consommateurs (corriger-accents-zones-sensibles + corriger-dictionnaire-accents) beneficient automatiquement du dictionnaire : aucun changement de code necessaire, seulement le bump de version 0.2.0-py -> 0.2.1-py (py + sh + md des 2 outils) + ligne d historique + mention des caracteres couverts dans la doc.

**Lecons** :
1. LA MODIFICATION D UN DICTIONNAIRE PARTAGE PROFITE A TOUS LES CONSOMMATEURS : corriger-accents-zones-sensibles (py+sh), corriger-dictionnaire-accents (py+sh) lisent le meme fichier .txt - une seule source de verite, aucun changement de code dans les scripts.
2. PIEGE TESTS PARALLELES : lancer 2 outils de correction EN PARALLELE sur le MEME fichier fausse les resultats (le 1er voit 0 fichier car le 2e a deja tout corrige) - toujours tester sequentiellement avec des fichiers neufs par outil.
3. PIEGE DOSSIERS EXCLUS : les noms de dossier contenant .tmp ou test- sont exclus par defaut (--exclure node_modules,.git,.agents,.backup,.tmp,test-,dictionnaire-,exemples) - un test dans .tmp-test-xxx donne Fichiers analyses: 0. Utiliser un dossier neutre (ex: .zz-xxx).
4. VERSION PY VS SH : les .py supportent --version, les .sh NON (erreur preexistante) - la parite --version py/sh n est pas applicable a ces outils, verifier plutot la parite de comportement (meme nombre de corrections, meme resultat).
5. REGLE DES 5 FICHIERS : apres modification de version, verifier py, sh, md des 2 outils + ligne d historique + doc mention des caracteres couverts - ici 6 fichiers outils + 1 dictionnaire = 7, tous ASCII 0 (sauf le dictionnaire, exception volontaire), LF pur, nommage OK.
6. detecter-impacts sur un .txt de donnees echoue (pas de frontmatter identite:) - c est normal, ce n est pas un outil migre ; les references NON MIS A JOUR signalees sont des fichiers qui mentionnent l outil sans version (bruit connu, 0 impact manquant reel).
## [LECON] 2026-08-09 -- SYMBOLES MANQUANTS AJOUTES AU DICTIONNAIRE (v0.2.2)

**Mission** : ajouter au dictionnaire partage corriger-dictionnaire-accents.txt les familles de caracteres non-ASCII courants encore manquantes (suite directe des guillemets francais v0.2.1).

**Modifications** (7 fichiers) :
1. Dictionnaire partage : +15 entrees -> 66 entrees utiles (68 lignes hors # avec 2 commentaires de section) : fleches verticales et doubles (U+2191 -> ^, U+2193 -> v, U+2194 -> <->, U+21D0 -> <=, U+21D2 -> =>, U+21D4 -> <=>), box drawing (U+2500 -> -, U+2502 -> |, U+250C -> +-, U+2510 -> -+, U+2514 -> +-, U+2518 -> -+, U+251C -> |-, U+2524 -> -|), espace inse cable U+00A0 -> espace simple.
2. Les 2 outils consommateurs en profitent automatiquement : bump 0.2.1-py -> 0.2.2-py (py+sh+md des 2 outils) + ligne historique + doc section caracteres couverts elargie.

**Lecons** :
1. SCAN PAR OCTETS VS SCAN DECODE : compter les octets > 127 est trompeur (les octets 0x80-0x9F sont des artefacts, 0xC2/0xC3/0xE2 des prefixes UTF-8) - toujours DECODER en UTF-8 puis compter les caracteres, sinon on liste des fantomes.
2. PIEGE CHEMINS WINDOWS : l exclusion de dossier par sous-chaine (ex: exemples/) ECHOUE si les chemins contiennent des backslashes - normaliser en forward slashes (replace backslash) avant le test d exclusion, sinon exemples/ (zone volontairement polluee) fausse le scan.
3. LE PROJET EST 100% PROPRE hors exemples/ et hors dictionnaire : le scan propre confirme que les seuls fichiers non-ASCII sont le dictionnaire (exception volontaire) et exemples/ (zone de test). L ajout de symboles est donc PREVENTIF : couvrir les familles qui pourraient apparaitre (schemas box drawing, fleches verticales, NBSP sournois).
4. COHERENCE DES REMPLACEMENTS : suivre les conventions existantes (U+2192 -> ->, U+2190 -> <-) : fleches verticales -> ^ et v, double sens -> <->, doubles -> <= => <=>, box drawing transcrits en traits/coins ASCII (+- -+ |- -|), NBSP -> espace simple. Verifier l absence de doublon/conflit AVANT d inserer (script avec controle).
5. REGLE DES 5 FICHIERS : apres bump de version, verifier py, sh, md des 2 outils + ligne historique + doc mention - ici 6 fichiers outils + 1 dictionnaire = 7, ASCII 0 (sauf dictionnaire), LF pur, nommage 0 erreur.
6. TESTS SEQUENTIELS : jamais 2 outils de correction en parallele sur le meme fichier (fausse les compteurs) - un fichier neuf par test, dossier neutre .zz-xxx (les noms .tmp/test- sont exclus par defaut).
## [LECON] 2026-08-09 -- ALIGNER UN TEST SUR LA REALITE (2 KO PREEXISTANTS)

**Mission** : mettre a jour test-005-generateurs-commande pour les 2 KO preexistants
(point 17 : version parcours-atlas attendue 0.1.5 vs reelle 0.1.10 ; point 18 : le test
exigeait 0 commande en dur alors que la case c30 porte une commande TEMPLATE connue
cartographier-parcours.py {parcours}).

**Lecons** :
1. QUAND UNE DONNEE EVOLUE, UN TEST OBSOLETE EST UNE DETTE : le .md documentait deja le
   residu (tableau : "1 commande restante c30") mais le .py exigeait encore 0 -> le test
   et sa doc ne racontaient pas la meme histoire. Toujours aligner .py ET .md ensemble.
2. NE PAS GELLER UNE DEFAILLANCE SANS GARDE-FOU : le point 18 ne doit pas devenir
   "toujours passer" - il doit tolerer EXACTEMENT le residu connu (n_commande == 1 ET
   case == c30) pour que TOUTE commande supplementaire soit un KO (detection de regression).
3. BALAYER TOUTES LES REFS DE VERSION : apres un changement de version attendue, grep
   complet sur les 2 fichiers (docstring, en-tete, titre, commentaires de section dans le
   CODE) - la ref v0.1.5 a ete trouvee 9 fois, dont 1 dans un commentaire de section
   (ligne 173) facile a oublier.
4. DECALAGE DOCUMENTAIRE A CORRIGER AU PASSAGE : le .md ligne 14 disait catalogue 0.2.0
   alors que le .py verifie 0.2.3 - profiter d une mise a jour de test pour resynchroniser
   la doc avec le code (regle des 5 fichiers appliquee au test lui-meme).
5. VALIDATION = RE-EXECUTION COMPLETE : 26/26 OK apres correction, ASCII 0, LF pur,
   py_compile OK, 0 residu. Un test mis a jour doit re-passer A L IDENTIQUE avant clore.
## [LECON] 2026-08-09 -- GARDE-FOU CLES DUPLIQUEES DANS LE REGENERATEUR DE CATALOGUE

**Mission** : ajouter un garde-fou a generateurs-regenerer-catalogue pour detecter les cles
dupliquees dans parametres lors des regenerations (lecon inserer-contenu-fichier : cle fichier
en double = collision de placeholder = meme valeur generee 2 fois).

**Lecons** :
1. LA DEDUPLICATION DE parser_aide NE COUVRE QUE LES NOUVELLES ENTREES : le mode sync
   PRESERVE l existant tel quel - un doublon preexistant passait sans controle. Le garde-fou
   doit valider le catalogue FINAL (existant + nouvelles + speciales + originales) AVANT
   ecriture, jamais seulement ce qui est genere.
2. GARDE-FOU = REFUS D ECRITURE + EXIT NON NUL : ne pas se contenter d un avertissement -
   si doublon detecte, ne PAS ecrire et lister les entrees fautives (nom + cles). En dry-run,
   rapport sans ecriture (outil de controle avant application).
3. TESTABILITE = OPTION --catalogue <chemin> : tester le garde-fou (positif et negatif) SANS
   toucher au catalogue reel - cibler une copie temporaire. Positif = doublon injecte -> refus
   + fichier inchange ; negatif = copie saine -> ecriture OK.
4. DEFAILLANCE LATENTE CRLF DECOUVERTE : l outil ecrivait en CRLF alors que le standard projet
   est LF (.gitattributes eol=lf + protocole-outils) - toute regeneration wet aurait corrompu
   le catalogue (conflit LF/CRLF). Corrige : ecriture LF pur + docstring/docs/spec mis a jour.
5. REGLE DES 5 FICHIERS APPLIQUEE : bump 1.0.0 -> 1.1.0 sur py (VERSION) + md (Version +
   historique) + spec (3 refs : frontmatter, champ version, titre) - le .sh est un simple
   wrapper exec (parite --version automatique, aucune version a dupliquer - verifier avant de
   chercher).
6. VALIDATION NON-REGRESSION : test-005 26/26 apres modification du regenerateur - le catalogue
   reel ne doit JAMAIS etre modifie par les tests du regenerateur (option --catalogue).
## [LECON] 2026-08-09 -- CORRECTION POINT MINEUR AUDIT : COMMENTAIRE STALE LIGNE 318

**Mission** : corriger le commentaire stale de generateurs-regenerer-catalogue.py (ligne 318)
'puis reecrire CRLF' -> 'puis ecrire en LF pur (standard projet)' - point mineur signale par
l audit Themis de conformite d execution (rapport garde-fou regenerateur).
**Lecons** :
1. UN COMMENTAIRE QUI DECRIT UN ANCIEN COMPORTEMENT EST UN ECART : quand on supprime une
   logique (resultat_crlf), le commentaire inline qui la decrivait devient trompeur - le
   corriger dans la MEME mission (ne pas laisser le docstring seul a jour).
2. CORRECTION DE COMMENTAIRE = PAS DE BUMP DE VERSION : la recommandation de l audit etait
   explicite (1 ligne, sans bump) - la version v1.1.0 reste inchangee, parite py/sh intacte.
3. VALIDATION LEGERE MAIS COMPLETE : py_compile + bash -n + parite --version + ASCII 0 +
   LF pur + grep de non-regression ('reecrire CRLF' absent) - une correction de commentaire
   ne necessite pas la batterie complete des tests fonctionnels.
## [LECON] 2026-08-09 -- GENERATEURS-AMELIORATION CREE (v1.0.0)

**Mission** : creer le generateur d'amelioration et d'optimisation (checklist
de questions par theme, format JSON) + theme ameliorer-outil + inscription
index-tools/catalogue.

**Livrables** :
- `generateurs-amelioration.py` v1.0.0 (py) + `.sh` (wrapper pur) + `.md` + `spec/`
- `themes-amelioration.json` : theme `ameliorer-outil` (10 questions avec raison)
- index-tools.md : ligne + total bump (108 -> 109)
- catalogue-commandes.json : entree triee (position 45), total 111 -> 112
- Interface : `--theme <nom>` / `--reponses 'q1=...;q2=...'` / `--liste` / `--aide` / `--version`

**Validations** : parite py/sh --version OK · interrogation 10/10 non-interactive
OK · theme inconnu -> erreur OK · py_compile/bash -n OK · nommage OK · ASCII 0 ·
LF pur · detecter-decalages-catalogue : 111 conformes / 0 decalage · test-005
26/26 OK.

**Lecons** :
1. Le mecanisme de questions de `generateurs-commande` (poser_question +
   parametres question/raison) est le modele naturel : reutilise pour la
   checklist, pas de reimplementation (code reuse).
2. L'option `--aide` est OBLIGATOIRE pour tout outil reference au catalogue :
   `detecter-decalages-catalogue` classe en "NON TESTABLE" tout outil sans
   aide reconnue (decouvert : mon outil etait le 1 non testable, corrige).
3. Checklist interrogee = reflexion deplacee HORS des cartes de decision
   (philosophie : alleger = decomposer, une place pour chaque chose).
4. Catalogue : toute nouvelle entree est inseree en position TRIEE (verifier
   le tri apres insertion) avec modele --theme {theme} et parametre obligatoire.
5. Hors perimetre (pre-existant, a ne pas corriger sans mission) :
   `test-001-evaluer-agents-coherence` reste "NON TESTABLE" (script de test
   sans --aide reference au catalogue).
6. Regle des 5 fichiers respectee (py, sh, md, spec) + enregistrements
   (index-tools, catalogue) + themes JSON = 6e fichier du dossier.
## [LECON] 2026-08-09 -- VALIDER-CASE CREE (v1.0.0, etape 2 de la refonte)

**Mission** : creer l outil qui valide et allege les cartes de decision
(etape 2 de la spec-refonte-cartes-decision v0.1.1, contrat section 6), avec
la CHAINE OBLIGATOIRE : apres la creation, activer Morpheus (tests) puis Janus
(controle) - la lecon de la conformite manquee sur generateurs-amelioration.

**Livrables** :
- `valider/valider-case/valider-case.py` v1.0.0 + `.sh` (wrapper pur) + `.md` + `spec/`
- index-tools.md : ligne + total bump (109 -> 110)
- catalogue-commandes.json : entree triee (position 94), total 112 -> 113
- Interface : <parcours.json> + --case / --surcharge / --modele / --references
  / --dry-run / --rapport / --version / --aide

**Fonctionnement** : verdict CONFORME / A ALLEGER / NON CONFORME + rapport md.
- STRUCTURE : types valides (question/controle/indice/action/fin), case_depart,
  fins joignables (BFS)
- MODELE : branches min 2 pour decisions ; indice/action = suivant requis ;
  boucle directe = erreur SAUF pattern de re-essai (controle NON -> soi-meme,
  volontaire, = avertissement) ; deviation sans rejoint = avertissement
- ALLEGEMENT : > 3 indices OU texte > 160 car. = signale avec proposition
- REFERENCES : ref resolvable (pattern-N -> spec-guider ; chemin -> fichier ;
  protocole-/regle- -> regles-immuables)
- NORMES : nommage c<numero>[a-z]?, titre, ASCII

**Resultat revelateur** : parcours-cerberus = A ALLEGER (0 erreur, 15
surcharges, 1 avertissement) - la preuve objective de la degradation des
cartes que la refonte doit corriger.

**Validations** : parite py/sh --version v1.0.0 OK · py_compile/bash -n OK ·
nommage 0 erreur (apres renommage validateur-case -> valider-case, voir lecons)
· ASCII 0 · LF pur · detecter-decalages-catalogue 112 conformes / 0 decalage ·
test-005 26/26 · 0 residu.

**Lecons** :
1. LE NOMMAGE PRIME SUR LE CONCEPT : l outil s appelait validateur-case (concept
   de la spec) mais le dossier valider/ exige le prefixe valider- -> renomme en
   valider-case AVANT le chainage (le concept reste dans les descriptions).
   TOUJOURS lancer valider-nommage AVANT de brancher quoi que ce soit.
2. Le pattern de re-essai (controle NON -> soi-meme) est VOLONTAIRE dans les
   cartes (c5 cerberus, c8 vulcain) : le validateur le traite en avertissement,
   pas en erreur - croiser la realite des cartes avant de figer une regle.
3. La preuve de la degradation est maintenant AUTOMATISEE : valider-case sur un
   parcours donne le compte exact de surcharges (15 sur cerberus) - la refonte
   des generateurs (etapes 3-4) pourra mesurer sa propre efficacite.
4. CHAINE EXECUTEE : cette fois je n ai PAS reactive Cerberus - j ai active
   Morpheus (case c8) pour les tests formels test-009-valider-case, puis la
   carte de Morpheus enchainera sur Janus. La conformite devient le defaut.

## [LECON] 2026-08-09 -- ETAPE 3 TERMINEE : generateurs-case v0.3.0 (modele compose complet + --ref)

**Mission** : refondre generateurs-case selon la spec-refonte-cartes-decision section 7.1 (etape 3).

**Actions realisees** :
1. `ajouter-bloc` generalise en MODELE COMPOSE COMPLET : decision + branches min 2 (OUI/NON + `--branche <rep>:<vers>` repetable) + deviation + rejoint.
2. Indices deviation/rejoint transformes en REFERENCES (`--ref-deviation`/`--ref-rejoint`, defaut `pattern-7`) : `{"type": "ref", "ref": "pattern-7"}` au lieu des textes inline longs -> valider-case ne signale plus de surcharge (verifie : bloc cree = 0 a alleger, verdict CONFORME).
3. Option `--ref <ref>` (repetable) ajoutee a `ajouter` et `editer` : pose des indices de type reference (cle `ref`, alignee sur `valider-case --references`).
4. Validation auto enrichie : appel interne `valider-case <parcours> --modele --dry-run` apres chaque modification (spec-refonte 7.1) - un verdict NON CONFORME bloque l'operation.
5. Regle des 5 fichiers : py + sh + md a jour (0.2.2 -> 0.3.0), SPEC CREE (spec-generateurs-case.001.01.ebauche.md, manquait - regle des 5 fichiers), index-tools ligne mise a jour.
6. 1 caractere non-ASCII introduit pendant la refonte ("clé" dans un docstring) -> corrige immediatement (lecon : verifier ASCII des docstrings apres toute edition).

**Lecons** :
1. Les indices de type REFERENCE (cle `ref`) sont le moyen d'alleger les cartes : un bloc compose genere par ajouter-bloc v0.3.0 ne produit AUCUNE surcharge (0 a alleger) alors que v0.2.2 en produisait 2 (textes inline > 160 car).
2. Le format de ref doit etre aligne sur la detection de valider-case --references : `pattern-<N>`, `protocole-<x>`/`regle-<x>`, chemin relatif. Lire l'outil de validation AVANT de choisir le format.
3. La spec de l'outil generateurs-case n'existait pas (regle des 5 fichiers incomplete) - creee avec la refonte.
4. Le testeur existant (tester-generateurs-case.sh) a 3 echecs PREEXISTANTS (PT5/PT6b attendent 21 cases dans parcours-vulcain, la carte en a 32 ; PT8b recablage c7->c20, c20 n'existe plus) : compteurs obsoletes, INDEPENDANTS de la refonte (PT6/PT9/PT15 passent). A corriger par Morpheus dans le test formel.

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.3.0, ASCII 0 (4 fichiers + spec), LF pur 0 CRLF, nommage 0 erreur, detecter-decalages 112 conformes / 0 decalage, test-005 26/26 OK.

**Conformite** : apres creation, j'active Morpheus (tests formels test-010) conformement a ma carte c8 - la chaine bout-en-bout continue.

## [LECON] 2026-08-09 -- ETAPE 4 TERMINEE : generateurs-carte v0.3.0 (squelette allege + delegation validateur-case)

**Mission** : refondre generateurs-carte selon la spec-refonte-cartes-decision section 7.2 (etape 4).

**Actions realisees** :
1. `creer` : squelette ALLEGE - les 8 textes de regles inline longs (> 160 car) des cases
   c0/c0b/c0c/c1/c2/c2b remplaces par des REFERENCES resolvables :
   - `protocole-activation` (relecture c0, action obligatoire c0b - resolu par recherche dans regles-immuables)
   - `pattern-6` (contexte temps reel c0c), `pattern-10` (une carte = un role c1),
   - `pattern-3`, `pattern-7`, `pattern-2` (rappels c2),
   - `cerveau-projet/agents/regles-immuables/general/rvav-workflow.md` (RVAV c2b, chemin relatif).
   Une carte neuve nait CONFORME (erreurs 0, a alleger 0) - LA PREUVE de l allegement a la creation.
2. `detecter` : delegation au validateur-case v1.0.0 (`--modele --surcharge --references`) en
   complement des anomalies structurelles locales - source unique de verite (spec 7.2).
3. `dupliquer-chemin` : les references sont CONSERVEES telles quelles dans les copies
   (teste : dc1 porte la ref pattern-10, aucun texte inline duplique).
4. `valider_auto` : ajout de l appel `valider-case --modele --references --dry-run` apres chaque ecriture.
5. Regle des 5 fichiers : py + sh + md a jour (0.2.0 -> 0.3.0, parite), SPEC CREE (spec-generateurs-carte.001.01.ebauche.md),
   index-tools ligne maj, catalogue choix action corrige (creer/analyser/detecter/dupliquer-chemin - manquait detecter).

**Lecons** :
1. La carte neuve nait ALLEGEE : squelette v0.3.0 = CONFORME des la creation (0 surcharge),
   alors que v0.2.2 generait des textes inline longs detectes par valider-case.
2. Les references `pattern-N`/`protocole-x`/chemins sont resolues par valider-case --references
   (pattern-N = "### Pattern N" dans spec-guider-parcours ; protocole-x/regle-x = recherche par nom
   dans regles-immuables ; chemin = fichier existant). Voir resoudre_reference avant de choisir.
3. --version seul echouait (action requise par argparse) -> interception dans main() comme --aide
   (lecon repetee de l etape 3 : tester --aide/--version sur les outils a sous-commandes).
4. Le catalogue portait un choix obsolet (["creer","analyser","dupliquer"]) - detecter manquait
   et le nom exact est dupliquer-chemin : verifier le catalogue apres toute modification de sous-commandes.
5. Attention ASCII strict dans les scripts temporaires (2 fois "nait/cle" corriges).

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.3.0, ASCII 0 (4 fichiers + spec),
LF pur 0 CRLF, nommage 0 erreur, detecter-decalages 112 conformes / 0 decalage, test-005 26/26 OK.

**Conformite** : apres creation, j'active Morpheus (tests formels test-011) conformement a ma carte c8.

## [LECON] 2026-08-09 -- ETAPE 5 TERMINEE : guider-parcours v0.4.0 (resolution des references + type action)

**Mission** : consolider guider-parcours selon la spec-refonte-cartes-decision etape 5 (resolution des
references d indices + ordre d execution obligatoire + IMPLEMENTER LE TYPE action, critere 7).

**Actions realisees** :
1. RESOLUTION DES REFERENCES dans afficher_indices (nouvelle fonction resoudre_reference) :
   - pattern-<N> : affiche [REFERENCE] X puis le TITRE + 3 premieres lignes du Pattern N extraites
     de la spec-guider-parcours (format '### Pattern N -- Titre') ;
   - protocole-<x>/regle-<x> : chemin du fichier/dossier trouve par recherche dans regles-immuables ;
   - chemin relatif : affiche le chemin + (fichier existant)/(reference non resolvable).
   Une case du squelette v0.3.0 affiche desormais le CONTENU resolu des refs (pattern-3/7/2, rvav) -
   la regle vit a UN endroit et l agent la voit resoudre a la navigation.
2. IMPLEMENTATION DU TYPE action dans naviguer (spec critere 7) : une case action avec 'suivant'
   s execute SANS question et enchaine automatiquement (teste : c8 action -> c9 fin -> PARCOURS TERMINE).
   Ajout du type action dans les tableaux de la spec-guider-parcours (version 0.4.0) et du .md.
3. generateurs-case v0.3.1 : type action ajoute aux choix de ajouter/editer + construire_case pose le
   'suivant' pour action comme pour indice (bug detecte : le suivant n etait pose que pour indice).
4. valider-case v1.0.0 acceptait DEJA le type action (TYPES_VALIDES prepare a l etape 2) - aucune
   modification necessaire de ce cote.

**Lecons** :
1. L'integration d'un nouveau type de case est TRANSVERSALE : guider-parcours (navigation) +
   generateurs-case (creation/edition) + valider-case (validation) + spec + .md. Verifier CHACUN
   (valider-case l avait deja, generateurs-case ne l avait pas - corrige).
2. Le bug 'suivant non pose pour action' etait silencieux : la case etait creee mais sans suivant,
   le validateur le signalait (--modele) et la navigation echouait. Le test formel (test-010 mis a jour
   avec 2 points action) couvre maintenant ce cas.
3. Apres bump de version d'un outil, les tests formels existants qui verifient la version (test-010
   attendait v0.3.0) doivent etre mis a jour : 1 KO detecte, corrige (v0.3.1 + 2 nouveaux points).
4. Resoudre une reference pattern-N : le titre est '### Pattern N -- Titre', le corps suit jusqu'a la
   prochaine '### '. Afficher 3 lignes suffit (l agent va lire la source pour le detail).

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.4.0 (gp) / v0.3.1 (gc),
ASCII 0 (7 fichiers), LF pur 0 CRLF, nommage 0, detecter-decalages 112 conformes / 0 decalage,
test-001-guider-parcours 14/14, test-005 26/26, test-010 25/25 (maj), test-011 19/19.

**Conformite** : apres creation, j'active Morpheus (tests formels test-012) conformement a ma carte c8.
## [LECON] 2026-08-09 -- CORRECTIF valider-case v1.0.1 : garde-fou anti-pollution du rapport

**Mission** : corriger le defaut de valider-case qui ecrivait son rapport par defaut dans le repertoire courant (lecon : rapport a la racine cree a 19:13 par Buffy).
**Resultat** : v1.0.1, aucun fichier cree sans --rapport <fichier> explicite.
**Lecons** :
1. Le defaut : quand --rapport absent ET --dry-run absent, valider-case ecrivait rapport-valider-case-<date>.md dans le CWD relatif au repertoire de lancement -- un agent lançant depuis la racine pollue la racine
2. Le correctif : sans --rapport <fichier> explicite, AUCUN fichier n'est cree (message clair 'AUCUN RAPPORT ECRIT : utilise --rapport <fichier>') ; --rapport <fichier> ecrit exactement au chemin fourni ; --dry-run conserve la simulation
3. Regle des 5 fichiers respectee : py (v1.0.1) + sh (Version 1.0.1) + md (historique + section rapport obsolete corrigee) + spec (Version + Historique) + test-009 (version + nouveau point 11b garde-fou)
4. Le test-009 passe de 19 a 20 points : le point 11b verifie qu'une commande sans options ne cree aucun fichier dans le repertoire courant
5. Aucun test existant ne dependait de l'ecriture par defaut (tous utilisaient --dry-run ou --rapport explicite) : la regression est nulle
6. Normes : ASCII strict + LF pur sur les 5 fichiers

**Preuve** : test-009 20/20, parite py/sh v1.0.1, commande sans options depuis /tmp = 0 fichier cree.

## [LECON] 2026-08-09 -- OUTIL generateurs-ligne cree (v0.1.0, categorie generateurs/)

**Mission** : creer generateurs-ligne (decision utilisateur) -- maillon du milieu de la suite des generateurs de cartes de decision (carte -> ligne -> case). Ligne = chemin de bout en bout ; configs = gabarits de groupes de cases ; carte Atlas a jour (existence + mtime) ; dry/wet.
**Livrables** : generateurs-ligne.py + .sh (wrapper pur exec python3) + .md + spec/ + entree catalogue-commandes.json (113 -> 114) + index-tools.md (103 -> 104).

**Lecons** :
1. La suite des generateurs est maintenant : generateurs-carte (carte COMPLETE) -> generateurs-ligne (LIGNE = groupe de cases en un bloc) -> generateurs-case (UNE case). Le maillon du milieu prepare un bloc conforme (decision + branches + deviation + rejoint) sans connaitre le metier : l'edition fine reste a l'agent habilite via SA carte.
2. LA CONVENTION DE NOMMAGE DES IDS DE CASES EST STRICTE : c<numero>[a-z]? (PAS DE POINT). Mon premier jet generait c42.1/c42.2 -> valider-case a refuse (NOMMAGE) a la validation auto. Corrige : c42, c42a, c42b... (suffixes lettres, jamais de point).
3. La case REJOINT d'un bloc doit pointer vers la cible EXTERNE fournie (--rejoint), pas vers elle-meme : un gabarit "REJOINT -> REJOINT" cree une boucle. Distinguer le suivant de la case REJOINT (externe) des suivants des cases AVANT (vers la case REJOINT du bloc).
4. Verification carte Atlas avant edition : cartographie-<agent>.md doit exister ET avoir un mtime > parcours JSON. Si absente/perimee -> BLOCAGE + invite a activer Atlas (case c31 Cartographier de SA carte) pour regenerer, puis revenir. --force passe outre (decision explicite).
5. Cablage du point d'attache : question/controle -> ajouter une BRANCHE (--reponse) ; action/indice -> recabler le suivant vers la premiere case (l'ancien suivant devient le rejoint par defaut). Une question/controle SANS suivant exige --rejoint explicite.
6. Parite py/sh (--version identiques) : le .sh est un wrapper pur exec python3 avec gestion --version avant l'exec.
7. detecter-impacts a signale 3 faux positifs de DATE (fichiers plus anciens sans aucune reference a generateurs-ligne) : verifier par grep que 0 reference -> justifie le NON MIS A JOUR sans modification.
8. Le catalogue attend le champ modele "{action} {parcours}" avec des parametres interpoleables (choix/texte) -- l'utilisateur compose la commande exacte via generateurs-commande.

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.1.0, ASCII 0 (4 fichiers), LF pur 0 CRLF, nommage 0, catalogue 114 trie, index-tools 104, bout en bout via generateurs-commande OK, ajout reel config defaut/config-1/config-3 -> valider-case CONFORME 0 erreur.

**Conformite** : apres creation, j'active Morpheus (test-017-generateurs-ligne) conformement a ma carte c8.
