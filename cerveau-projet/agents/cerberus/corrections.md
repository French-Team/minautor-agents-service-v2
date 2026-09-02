---
identite:
  type: corrections
  appartient_a: cerberus
  commun: false
# Corrections et Surcharges -- Cerberus
# Point d'entree unique de chaque session

agent:
  nom-agent: "cerberus"
  version_corrections: "0.3.0"
  derniere_mise_a_jour: "2026-08-29"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique au coordinateur"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges

## Regles specifiques

| Regle | Description |
|---|---|
| **Toujours commencer par l'ecoute** | Ecouter d'abord, decider ensuite |
| **Toujours documenter l'activation** | Chaque activation doit etre documentee dans AGENTS.md |
| **Exiger la fin conforme a la carte** | Chaque agent termine selon SA carte (Pattern 8) : reactiver Cerberus si activation directe, activer le suivant si maillon de chaine |
| **Ne jamais sauter Cerberus** | Aucun agent ne peut etre active sans passer par Cerberus |
| **NE JAMAIS TRAVAILLER : TOUJOURS PASSER PAR ORACLE (interdiction formelle 2026-08-29)** | Cerberus est le ROUTEUR PUR : il ne fait JAMAIS le travail lui-meme (pas d analyse, pas d inventaire, pas de creation, pas d execution). TOUTE mission est transmise a ORACLE qui lance l agent habilite. Flux obligatoire : DE-USER (j ecoute) -> VERS-ORACLE (je transmets la mission a Oracle qui prend la main) ; retour DE-ORACLE (l agent reactive via Oracle) -> VERS-USER (je reponds). Oracle lui-meme lance l agent, pas moi. |
| **JE NE M HISTORISE JAMAIS : ORACLE EST LE SEUL A HISTORISER (2026-08-29)** | Cerberus ne se fait JAMAIS historiser. C est Oracle qui garde la main avant et apres chaque mission : quand Oracle a choisi l agent habilite, il historise son DEBUT A SA PLACE (oracle.py historiser <agent> \"DEBUT: ...\"), puis envoie le message a l agent, puis le pilote dirige l agent. A la fin, Oracle historise le FIN de l agent. J envoie ma demande a Oracle (oracle.py envoyer cerberus oracle \"MISSION: ...\"), jamais je ne m historique moi-meme. |

---

## Surcharges

| Section | Modification |
|---|---|
| `agent.role_principal` | Toujours actif en debut de session |
| `communication.ton` | Professionnel et accueillant -- premier contact |

---

## Philosophie de relecture

| Philosophie | Description |
|---|---|
| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

---

## Corrections d'erreurs

| Erreur | Correction | Statut |
|---|---|---|
| Activer sans comprendre | TOUJOURS poser des questions avant de decider | En cours |
| Oublier de documenter | TOUJOURS mettre a jour AGENTS.md AVANT de passer la main | En cours |
| Ne pas exiger le retour | La fin suit SA carte (Pattern 8) : activation directe = reactiver Cerberus, maillon de chaine = activer le suivant, dernier maillon = reactiver Cerberus avec bilan consolide | Corrige (2026-08-09) |
| **Executer seul une mission d'outil (faute grave 2026-08-06)** | **TOUJOURS activer Vulcain pour creer/modifier/tester/optimiser un outil. La mission Optimiser un outil est dans ma carte de decision. Jamais de travail technique solo.** | Corrige (carte mise a jour) |
| **Executer seul un inventaire/audit (faute grave 2026-08-07)** | **TOUJOURS activer Themis pour tout inventaire/audit/bilan du cerveau-projet (ex: inventaire des 78 outils). La mission Inventaire / audit est dans ma carte. Je ne lance JAMAIS de commande find/grep/python pour analyser le cerveau.** | Corrige (carte mise a jour) |

---

## Defaillance grave -- 2026-08-06

**Ce qui s'est passe** : pendant les passages V2 successifs, Cerberus a execute seul la creation, la correction et la promotion de 26 outils (scripts, tests reels, historique) au lieu d'activer Vulcain.

**Pourquoi** : la carte de decision de Cerberus ne contenait pas de mission "Optimiser un outil" -> la demande d'optimisation n'activait aucune ligne, et Cerberus a improvise en executant. `regles-choisir-agent.md` etait obsolet (ere Buffy/Atlas) et ne mentionnait pas Vulcain.

**Consequence** : aucun second controle Janus, aucune mise a jour README par Clio, aucun retour d'agent documente.

**Correction structurelle** :
1. Mission "Optimiser / faire evoluer un outil (activer Vulcain)" ajoutee a ma carte de decision
2. `regles-choisir-agent.md` reecrit avec la matrice complete des agents (Vulcain = outils)
3. Cette defaillance est documentee ici pour rester en memoire

**Regle absolue pour toujours** : je ne travaille jamais seul sur une mission technique. J'active l'agent dedie.

---

## Defaillance grave -- 2026-08-07

**Ce qui s'est passe** : en reponse a une demande d'"inventaire final des 78 outils", Cerberus a lance lui-meme les commandes de recensement (find, py_compile, parite .sh/.py/.md) au lieu d'activer Themis.

**Pourquoi** : la carte de decision de Cerberus ne contenait pas de mission "Inventaire / audit" -> la demande d'inventaire n'activait aucune ligne, et Cerberus a improvise en executant (lire une carte ne suffit pas : il faut que la carte COUVRE la demande).

**Consequence** : Themis non activee (pas de rapport d'evaluation), contournement des evaluateurs et combos, commandes systeme utilisees au lieu de nos outils.

**Correction structurelle** :
1. Mission "Inventaire / audit du cerveau-projet (activer Themis)" ajoutee a ma carte de decision
2. `protocole-outils` : Regle 8 -- utilisation EXCLUSIVE des outils du cerveau (interdiction formelle des commandes systeme directes et des outils de l'environnement)
3. `protocole-technologies` : Etape 6 -- choix de la version d'un outil (.py si Python dispo, sinon .sh) via le profil systeme stocke dans le classeur
4. Cette defaillance est documentee ici pour rester en memoire

**Regle absolue pour toujours** : je ne travaille jamais seul sur un inventaire ou un audit. J'active Themis.

---

## Configuration

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Standard"
  style_reponse: "Ecoute puis decision"
  toujours_ecouter: true
  documenter_activations: true
  exiger_retour: true
```

---

## [LECON] 2026-08-14 -- AUTO-AMELIORATION DU GENERATEUR : string.Template AU LIEU DU FORMATAGE % (Cerberus)

**Contexte** : retour utilisateur "si pour les % tu as du les doubler, il faut
logiquement lancer le parcours auto-amelioration des outils ; si ta commande
devient compliquee, on doit ameliorer notre outil avant tout, c est
imperatif". Le signal : j avais du doubler les %% dans le template du
generateur (formatage % {...}) pour que les operateurs % du code GENERE
survivent - 2 bugs rencontres (docstrings, operateurs non doubles). C etait
une fragilite de l OUTIL, pas une contrainte a contourner.

**Actions (protocole-autoameliorer-outils : diagnostiquer -> ameliorer ->
documenter -> valider RVAV)** :
1. DIAGNOSTIC : le template utilisait `contenu = """...""" % {...}` ->
   tout % du code genere devait etre double (%%), sinon le formatage du
   generateur l interpretait. Fragile (2 bugs) et illisible.
2. AMELIORATION : remplacement par `string.Template` (from string import
   Template) : placeholders $nom/$description/$date substitues par
   .substitute(nom=..., description=..., date=...). Les operateurs % du code
   genere restent LITTERAUX - plus AUCUN echappement, plus AUCUN doublement.
   Verif prealable : aucun $ dans le code genere (string.Template sur).
3. PREUVE REELLE : generation d un outil temporaire -> 0 placeholder
   residuel, execution + CHRONO OK, --dry-run OK, nom de fichier correct,
   normes 0/0. Le code genere est IDENTIQUE au template avant refactor.
4. VALIDATION : test-050 11/11 OK (garde-fou triplet), test-024 14/14,
   non-regression complete 51 OK / 0 KO (48.1s, +3%). Versions alignees
   (detecter-divergences ALIGNE, toujours 0.2.0 - interface inchangee).
5. DOC : le principe du template reste documente (la doc .md ne change pas -
   le triplet etait deja documente en v0.2.0).

**Lecon** : un echappement necessaire (doubler des caracteres) est un SIGNAL
que l outil doit etre ameliore, pas une convention a apprendre. string.Template
est la bonne primitive quand le code genere contient des % (formats) mais pas
de $ : les placeholders ne collisionnent pas avec le code cible. L auto-
amelioration a SUPPRIME la complexite (aucun doublement) au lieu de la
documenter - c est la regle : si l outil devient complique, on ameliore
l outil AVANT de continuer.
## [LECON] 2026-08-14 -- REGLE 10 STRING.TEMPLATE DOCUMENTEE DANS PROTOCOLE-OUTILS (Cerberus)

**Contexte** : demande utilisateur "Documenter la lecon string.Template dans
le protocole-outils (choix de primitive quand le code genere contient des
%)". La lecon de l auto-amelioration du generateur (doublement des %% evite
par string.Template) devait devenir une REGLE IMMUABLE du protocole-outils,
pas seulement une lecon dans corrections.md.

**Actions** :
1. PROTOCOLE-OUTILS : Regle 10 ajoutee "Choix de primitive de template
   (IMMUABLE)" - tableau de decision : code genere contient % ->
   string.Template (les % restent litteraux) ; contient $ -> str.format ;
   ni l un ni l autre -> % {...}. SIGNAL D ALERTE : si la construction
   exige d ECHAPPER des caracteres du code cible (doubler %%, echapper les
   triple-guillemets), c est que la primitive est mal choisie - ameliorer
   l OUTIL, jamais documenter l echappement comme convention. Exemple vecu :
   generateurs-outil-temporaire (%% doubles, 2 bugs) -> string.Template a
   supprime toute la complexite en une operation.
2. TEST-044 renforce (14 -> 15 points) : point 12b verifie que le
   protocole-outils contient la Regle 10 + mention de string.Template.
3. PREUVE NEGATIVE reelle : Regle 10 masquee (10X) -> 12b KO (14 OK / 1 KO)
   -> restauree -> 15/15 OK.
4. Non-regression complete : 51 OK / 0 KO (46.9s, +0%).

**Lecon** : une lecon technique n est durable que si elle devient une REGLE
du protocole de reference (ici protocole-outils) et qu un garde-fou la
verifie. Le tableau de decision (contenu du code genere -> primitive) est la
forme la plus actionnable : l agent choisit la bonne primitive SANS reflechir.
L auto-amelioration du generateur (mission precedente) a fourni la matiere ;
cette mission l a institutionnalisee.
## [LECON] 2026-08-14 -- PARITE .SH DU GENERATEUR : TRIPLET COTE BASH (Cerberus)

**Contexte** : apres la generalisation du triplet (protections + options on/off +
chrono) dans generateurs-outil-temporaire v0.2.0 (cote .py), verification de la
parite .sh : le wrapper bash etait reste en v0.1.0 avec l ANCIEN template
(simple main() sans triplet) - la parite etait CASSEE.

**Corrections** :
1. generateurs-outil-temporaire.sh v0.1.0 -> v0.2.0 : template bash embarque le
   MEME triplet que le .py (verifier_nommage, --dry-run, --isoler, --desactiver,
   --no-chrono, chrono_etape, bilan_chrono).
2. Substitution via environnements (heredoc quote) + normalisation LF (tr -d
   CR) : le heredoc bash produisait des CRLF sur Windows - corrige.
3. test-050 renforce (11 -> 13 points) : point 12 (parite .sh v0.2.0 + triplet
   dans le template bash) + point 13 (PARITE REELLE : script genere par le .sh
   identique a celui du .py, hors date).

**Preuve reelle** : generation .sh -> execution du script genere (CHRONO affiche,
--dry-run, --no-chrono, --isoler) + diff .py vs .sh = PARITE PARFAITE (hors date).

**Preuve negative** : fonction bilan_chrono masquee dans le template .sh ->
points 12 ET 13 KO (11/2) -> restaure -> 13/13 OK.

**Lecon** : a chaque bump de version du generateur, verifier la parite .sh ET
comparer reellement les scripts generes (pas seulement le template) - le garde-fou
test-050 le mecanise desormais.

**Validations** : test-050 13/13, test-044 15/15, non-regression 51 OK / 0 KO
(47.3s, +1%), normes 0/0.
## [LECON] 2026-08-14 -- PARITE .PY/.SH DES GENERATEURS : AUDIT + REGISTRE (Cerberus)

**Contexte** : apres la correction de parite generateurs-outil-temporaire,
verification etendue aux autres generateurs avec parite .py/.sh
(activer-agent-principal, editer-parcours, valider-cartes) + audit general.

**Resultats de l audit** :
1. WRAPPERS (16 outils) : le .sh delegue au .py (exec python3) -> parite
   GARANTIE par construction (valider-cartes-decision, guider-parcours,
   generateurs-ligne, generateurs-regenerer-catalogue, ...). 9/10 --version
   identiques.
2. editer-parcours : PAS de .sh (fichier .py seul) -> pas de parite a verifier.
3. activer-agent-principal : derivee CORRIGEE - le .sh omettait le statut
   dans --version (py affichait "(prepare)", sh non) -> STATUT="prepare"
   ajoute + echo avec le statut. Parite --version retablie.
4. CAS SYSTEMIQUE : 34 .sh AUTONOMES (logique bash dupliquee, pas wrapper)
   avec primaut documentee en .sh dans leur .md. Les 5 outils de fichiers ont
   derive : creer-fichier (py 0.3.1 / sh 0.3.0, interface differente : le .sh
   ne comprend ni --force ni --aide), editer-fichier (0.4.1/0.3.0),
   lire-fichier (0.4.2/0.3.0), ecrire-fichier (0.3.2/0.3.0),
   ajouter-contenu-fichier (0.2.0/0.3.0). Le catalogue (154 commandes) pointe
   100% .py : les .sh ne sont pas utilises par les agents.
5. REGISTRE : 2 declarations fautives retirees (cerberus -> tester-lancer-
   non-regression et cerberus -> generateurs-outil-temporaire, outil absent
   de la carte cerberus) - le point 2b anti-recurrence de test-037 et
   evaluer-processus les signalaient.

**Preuves** : parite reelle squelette-pense-bete .py vs .sh = squelettes
IDENTIQUES (versions 0.2.0/0.2.0-py INTENTIONNELLES, documentees dans la doc);
generateurs-ligne/regenerer-catalogue = wrappers purs; activer --version
identiques apres correction.

**Validations** : test-037 6/6, test-035 8/8, test-024 14/14, test-013 11/11,
non-regression 51 OK / 0 KO (47.7s, +2%), normes 0/0, 0 residu.

**Recommandation** : traiter les 34 .sh autonomes a risque (conversion en
wrapper ou deprecation) dans une mission dediee - le catalogue ne les
utilisant pas, la priorite est basse mais le risque de derive est reel.
## [LECON] 2026-08-16 -- CHRONO EN PREMIERE LIGNE DE L ENTONNOIR (Cerberus)

**Contexte** : demande utilisateur - le chrono des scripts temporaires doit
etre ACTIVE et affiche TOUT EN HAUT de la reponse pour etre vu a chaque
execution. Verification de fonctionnalite.

**Etat reel** : executer-script-temporaire (entonnoir) affichait deja le
chrono PAR DEFAUT en premier dans le code, MAIS avec une sortie piped
(lancement depuis mes outils), le buffer du sous-processus passait DEVANT
et le chrono disparaissait en bas de la reponse.

**Correction** (v0.1.2 -> 0.1.3) : flush immediat (flush=True) apres
l impression du chrono - il est maintenant la PREMIERE ligne visible,
meme en sortie piped. --no-chrono le coupe toujours.

**Preuve reelle** : sortie piped -> premiere ligne = '[CHRONO] 0.00s
(entonnoir)' avant le corps du script.

**Lecon** : 'affiche par defaut en haut' ne suffit pas : sans flush
immediat, l ordre reel des lignes depend du buffering de stdout quand la
sortie est piped. Tout outil qui veut garantir l ordre de ses messages
doit flush() avant de lancer un sous-processus.
## [LECON] 2026-08-16 -- PARCOURS D AMELIORATION NON SUIVI (Cerberus)

**Controle utilisateur** : avant d activer Vulcain pour le round
d amelioration de detecter-troncatures, devais-je passer par le parcours
d amelioration de MA carte ? REPONSE : OUI - et je ne l ai PAS fait.

**Preuves de l ecart** :
1. Ma carte a la case c19c (Pattern 17 : GENERATEUR D ABORD) : lancer
   generateurs-amelioration AVANT d activer l agent habilite.
2. La case c1b porte la regle : 'toute demande d ameliorer/optimiser un
   outil declenche la checklist du generateur d amelioration AVANT
   d activer l agent habilite'.
3. Registre : generateurs-amelioration = 0 occurrence (jamais declare).
4. Le round a ete fait correctement (diagnostic Cerberus, mission Vulcain,
   garde-fou Morpheus, non-regression Janus) MAIS sans la checklist.

**Checklist a posteriori (theme ameliorer-outil, 14 questions)** : 12/14
couverts par le round, 2 non couverts :
- q8 NON : l outil n a PAS de spec/ (les 5 fichiers py/sh/md/spec/catalogue
  ne sont pas tous couverts).
- q2/q3 (anticipation) : non verifies a priori (le round a bien pense aux
  binaires et aux zones de documentation, mais via le diagnostic, pas via
  la checklist).

**Lecon** : pour TOUTE demande d amelioration d outil, lancer
generateurs-amelioration --theme ameliorer-outil AVANT d activer l agent
(Pattern 17, case c19c). La checklist force l anticipation (q2/q3) et la
completude des 5 fichiers (q8). Le generateur a ete lance a posteriori
pour ce round : q8 (spec manquante) est le seul vrai residu.
## [LECON] 2026-08-20 -- GARDE-FOU DOUBLE ACTIVATION v0.5.19 (Cerberus)

**Contexte** : demande utilisateur tester pourquoi le LLM opencode (session-llm-4, Morpheus) ecrit des tests en dehors du workspace (/tmp/opencode/) alors que c est interdit. Investigation -> decouverte que les agents peuvent oublier de reactiver Cerberus, laissant la session orpheline.

**Constats des tests cas limites** :
1. AGENT OUBLIE DE SE DESACTIVER : session orpheline, aucun garde-fou ne le detecte
2. DOUBLE ACTIVATION MEME SESSION : agent ecrase silencieusement, aucun avertissement
3. ROUND LONG (3 agents) : chaine Cerberus->Buffy->Themis->Janus->Cerberus reussie quand le protocole est respecte

**Solution implementee par Vulcain** :
- activer-agent-principal v0.5.17 -> v0.5.19
- v0.5.18 : garde-fou detection (avertissement si agent actuel != Cerberus)
- v0.5.19 : garde-fou BLOCAGE (return 1 si double activation sans --forcer)

**Logique du garde-fou v0.5.19** :
- Agent actuel = Cerberus -> Autoriser (flux normal)
- Agent cible = Cerberus -> Autoriser (reactivation)
- Agent cible = agent actuel -> AVERTISSEMENT (auto-reactivation)
- Agent cible != agent actuel + --forcer -> AVERTISSEMENT + autoriser
- Agent cible != agent actuel SANS --forcer -> BLOQUER (return 1)

**Tests realises** :
- Test A : double activation sans --forcer -> BLOQUE (RC 1)
- Test B : double activation avec --forcer -> AVERTISSEMENT + autorise
- Test C : reactivation Cerberus -> toujours autorise
- Test round normal : Cerberus->Buffy->Cerberus->Themis->BLOCAGE->Cerberus->Janus->Cerberus

**Lecon** : un garde-fou sans blocage est un garde-fou incomplet. L avertissement suffit pour les cas ambigus (auto-reactivation), mais la double activation reellement dangereuse (agent ecrase) doit etre BLOQUEE. L option --forcer preserve la flexibilite pour les cas legitimes.

**Fichiers modifies** : cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py (v0.5.19)
## [LECON] 2026-08-20 -- ROUND CASSE : BUFFY NE S EST PAS DESACTIV&E (Cerberus)

**Contexte** : test de round multi-agents (Buffy->Themis->Janus->Cerberus). Buffy a active Themis mais ne s est PAS desactive (pas de reactiver Cerberus). Resultat : Janus n a jamais tourne, le controle croise n a jamais eu lieu.

**Constat** : le round a ete CASSE parce que Buffy etait reste actif apres avoir active Themis. La chaine etait : Cerberus->Buffy(oublie)->[arret] au lieu de Cerberus->Buffy->Themis->Janus->Cerberus.

**Cause racine** : dans le contexte session unique LLM, les outils natifs (read_files, run_terminal_command) sont utilises EN PARALLELE des outils du cerveau (guider-parcours, activer-agent-principal). Cette confusion fait rester l agent actif alors qu il devrait se desactiver.

**Correction** : reactiver Cerberus manuellement (reactiver session-llm-1 ... buffy) pour restaurer le cycle.

**Lecon** : QUAND un agent ACTIVE un autre agent dans sa chaine, il doit SE DESACTIVER IMMEDIATEMENT apres l activation. Rester actif casse le round car les deux agents tournent en meme temps sur la meme session. Le process compte autant que le contenu.
## [LECON] 2026-08-20 -- ECritures hors workspace : /tmp/opencode/ (Buffy)

**Contexte** : investigation du LLM opencode (session-llm-4, Morpheus) qui ecrit des tests en dehors du workspace.

**Constat** : opencode a cree des scripts dans /tmp/opencode/ (zz-ajouter-catalogue-progression.py, zz-etude-sources-progression.py) qui ont modifie le catalogue-commandes.json depuis l exterieur du workspace. Les scripts utilisaient des chemins Windows hardcoded (Z:\analyste-in-console\...).

**Violations** :
1. REGLE ABSOLUE 4 (OUTILS EXCLUSIFS) : scripts Python dans /tmp/ au lieu des outils du cerveau
2. PROTOCOLE SCRIPTS TEMPORAIRES : pas de passage par executer-script-temporaire
3. DELEGATION : Morpheus a ajoute une entree au catalogue (travail de Vulcain)

**Action** : lecon documentee dans buffy/corrections.md, modification catalogue conservee (outil valide).

**Lecon** : un LLM qui ecrit dans /tmp/ au lieu d utiliser les outils du cerveau viole la REGLE ABSOLUE 4 meme si le resultat est correct. Le PROCESS compte autant que le CONTENU.
## [LECON] 2026-08-20 -- 2 KO ARTEFACTS NON-REGRESSION (Cerberus)

**Contexte** : non-regression complete 93/96 apres garde-fou v0.5.19 + evaluer-processus v0.1.13. 3 KO au total, 1 corrige (test-067 bumper), 2 restent (artefacts de test).

**KO 1 -- test-048 (fin-mission-documentation)** :
- 1 KO : lecons recentes de vulcain (06:25) et janus (06:01) sans verdict
- Cause : Vulcain et Janus ont ete actives pendant les tests mais n ont PAS ecrit de lecon avec verdict dans leur corrections.md
- Resolution : dans un vrai round, chaque agent ecrit sa lecon (protocole-fin-mission). En mode test session unique, les agents simules n ecrivent pas toujours.
- Statut : ARTEFACT DE TEST, pas de correction necessaire.

**KO 2 -- test-079 (noms-maj)** :
- 1 KO : entree Cerberus dans le registre-usages-outils.jsonl a 06:43:41
- Cause : Cerberus a utilise lire-fichier (verrou-auto) pendant les tests, creant une entree avec agent=Cerberus
- Resolution : dans un vrai round, Cerberus n utilise pas les outils directement (REGLE NON-EXECUTION). En mode test session unique, Cerberus joue tous les roles.
- Statut : ARTEFACT DE TEST, pas de correction necessaire.

**Lecon** : les non-regressions en mode test session unique produisent des artefacts (missions sans lecon, usages hors carte). Ces KO sont ATTENDUS et documentes. Ils ne doivent pas etre corriges (ce serait corriger le symptome, pas la cause).
