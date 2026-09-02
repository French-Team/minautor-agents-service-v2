---
identite:
  type: corrections
  appartient_a: clio
  commun: false
# Corrections et Surcharges -- Clio
# Agent dedie a la mise a jour du README

agent:
  nom-agent: "clio"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-06"

---

# Corrections et Surcharges

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **Outil unique** | Je n'edite JAMAIS le README directement -- seul `mettre-a-jour-readme` le modifie |
| **Sources de verite** | Je verifie AGENTS-historique.md, agents/ et tools/ avant de modifier |
| **Apres chaque mission** | Je suis active par Cerberus apres chaque retour d'agent, pas a la demande |
| **README uniquement** | Je ne touche pas aux autres fichiers du cerveau |
| **Le README est le livre** | Je CORRIGE le texte existant -- jamais de chronologie, jamais de lignes d'interventions ajoutees |

---

## [LECON] 2026-08-16 -- MISE A JOUR README PUBLIC + DEV (Clio)

**Contexte** : demande utilisateur (mise a jour des readmes). Mission confiee
par Cerberus (case c17) apres un diagnostic des compteurs.

**Travail realise** :
1. readme-dev.md : tableau des outils resynchronise sur la realite
   (combos-analyse-projet = source de verite). Les compteurs Analyser 5->6,
   Corriger 6->7, Detecter 15->17, Nettoyer 3->4 etaient perimes. Les
   exemples de colonnes Corriger/Nettoyer/Evaluer etaient incomplets.
2. README public : ligne Argus du tableau des agents re-formatee (elle etait
   sortie du tableau, avec une 3e colonne inexistante, collant au titre suivant).

**Verification** : combos-analyse-projet verdict "README A JOUR (0 ecart)",
test-038 7/7 (badge 149 == 149), normes 0 non-ascii / 0 CRLF sur les 2 fichiers.

**Lecon** :
- La source de verite des compteurs d outils est combos-analyse-projet
  (compter_outils = dossiers reels), pas l index-tools (qui compte aussi
  protections/tests/templates -> 187 avec une convention differente).
- Toujours verifier le format des tableaux markdown apres un ajout de ligne
  (ligne Argus mal formatee : colonnes manquantes + titre colle).
## [LECON] 2026-08-16 -- BADGE 150 + MIGRER DANS README-DEV (Clio)

**Contexte** : migration relecture obligatoire (Vulcain) -> nouvel outil
migrer-cases-relecture -> compte reel d outils 149 -> 150. test-038 KO
(badge affiche 149, reel 150).

**Travail realise** :
1. Badge README 149 -> 150 (2 occurrences : affichage ET href du header).
   Lecons du passage : editer-fichier n a remplace que la PREMIERE
   occurrence de la ligne ; le href (2e occurrence) est reste a 149 ->
   verification grep des 2 occurrences + test-038 7/7.
2. readme-dev.md : categorie Migrer 1 -> 2 (migrer-identite +
   migrer-cases-relecture) dans le tableau de la section 6.
3. combos-analyse-projet : README A JOUR (0 ecart), normes 0/0.

**Lecon** :
- Un nouvel outil = +1 au compte reel = badge ET tableau readme-dev a
  synchroniser dans la meme mission. Le badge a 2 occurrences (affichage +
  href) : toujours verifier les 2 (grep Outils-<n> et test-038).
- combos-analyse-projet est la source de verite : il liste les ecarts
  categorie par categorie (il a detecte Migrer 1 vs 2).
## [LECON] 2026-08-16 -- BADGE OUTILS README 150 -> 152 (Clio)

**Contexte** : KO test-038 (badge-readme-synchronise) detecte par Janus en
barriere KO. Vulcain a cree 2 outils web (rechercher-web +
detecter-recherches-obsoletes) : le compte reel des outils est passe de 150
a 152 mais le badge en dur du README affichait encore 150 (affichage + href).

**Fait** :
- Badge en dur ligne 9 du README : affichage (Outils-152) PUIS href
  (Outils-152) - 2 occurrences distinctes (editer-fichier 150 -> 152 x2).
- test-038 : 7/7 OK (affichage == compte reel == href).

**Lecons** :
- Le badge README a DEUX occurrences du nombre (affichage + href) : corriger
  les deux, sinon test-038 reste KO (verifie les deux separement).
- editer-fichier remplace la PREMIERE occurrence : pour un badge en dur avec
  2 memes valeurs, relancer avec un motif plus precis (badge/Outils-150...)
  pour la 2e. Toujours verifier avec grep -o | sort | uniq -c apres.
- Le KO a ete detecte par la barriere serie KO de Janus (nouveau workflow) :
  le cycle KO -> agent habilite (Clio) -> revalidation est fluide.
## [LECON] 2026-08-17 -- BADGE OUTILS + TABLE README-DEV (Clio)

**Contexte** : KO non-regression test-038 (badge 157 vs compte reel 159) apres le round BDD des lecons (2 nouveaux outils : enregistrer-lecon, consulter-lecons).

**Cause** : le badge du README et la table de readme-dev ne sont pas synchronises automatiquement avec la source de verite (compter_outils de combos-analyse-projet). Chaque nouvel outil cree doit etre repere : badge README ligne 9 (affichage + href), totaux readme-dev (lignes 28, 57, 218) ET table des categories.

**Actions** : badge Outils-157 -> 159 (affichage + href), readme-dev 149 outils/35 categories -> 159/38, table maj (Enregistrer 1->2, ajout Consulter 1 + Configurer 1, Analyser 6->9, Detecter 17->19, Rechercher 10->11).

**Lecon** : verifier la synchronisation des compteurs a CHAQUE creation d outil ; la source de verite est compter_outils (combos-analyse-projet), jamais un comptage a la main.
## [LECON] 2026-08-20 -- NOUVELLES REGLES (ton 1ere personne, dry-run, badges dynamiques)

**Contexte** : l'utilisateur veut des README parlants qui creent un premier contact avec les utilisateurs lambda.

**Nouvelles regles ajoutees a la fiche Clio v0.2.2** :
1. **Ton 1ere personne** : le README parle "je suis..." au lieu de "Le cerveau-projet est..."
2. **Dry-run obligatoire** : montrer le AVANT/APRES avant d'ecrire
3. **Badges dynamiques** : compter les agents, protocoles, conventions, regles AVANT de mettre a jour les badges

**Lecon** : le README n'est pas qu'un document technique -- c'est le premier contact avec les utilisateurs. Le ton doit etre accueillant et explicatif, pas froid et documentaire.
## [LECON] 2026-08-20 -- REECRITURE COMPLETE README (ton 1ere personne + badges dynamiques)

**Contexte** : l'utilisateur veut des README parlants qui creent un premier contact avec les utilisateurs lambda.

**Travail realise** :
1. README.md : reecriture complete en ton 1ere personne (je suis...), badges dynamiques (16 agents, 164 outils, 97 tests, 36 protocoles, 75 regles)
2. README-dev.md : reecriture en ton 1ere personne, compteurs mis a jour (164 outils, 39 categories, 16 parcours, 97 tests)
3. Compteurs reels verifies via combos-analyse-projet : 16 agents, 164 outils

**Lecon** : le README n'est pas qu'un document technique -- c'est le premier contact avec les utilisateurs. Le ton doit etre accueillant et explicatif, pas froid et documentaire. Les badges dynamiques donnent une vision immediate de la puissance du systeme.

**Verdict** : ASCII 0/0 sur les 2 fichiers, compteurs alignes sur la realite.
## [LECON] 2026-08-22 -- CORRECTION ECART E1 README PUBLIC + DEV (Clio)

**Contexte** : audit Themis creation Redacteur-v2 - E1 MAJEUR : compteurs 16 agents
vs 18 reels, Socrate et Redacteur-v2 absents des tables.
**Travail realise** : README.md (16->18 x2, + lignes Socrate et Redacteur-v2 dans la
table Mes agents) ET readme-dev.md (compteur Agents 16->18, + 2 lignes section 4,
liste parcours 16->18 avec argus/chiron/gardien/socrate/redacteur-v2 ajoutes).
**Verification** : combos-analyse-projet VERDICT README A JOUR (badge 164 == 164,
0 ecart), ASCII 0, LF pur sur les 2 fichiers.
**Verdict** : VALIDE.
**Lecon** : l'audit avait declare readme-dev a jour a tort - les 2 documents doivent
TOUJOURS etre verifies ensemble (grep cible sur chaque nom d'agent dans CHACUN des
2 readmes). Le compteur de texte libre (16 agents) n'est pas detecte par --verifier :
les compteurs narratifs se corrigent a la main apres verification --agents.
## [LECON] 2026-08-23 -- REGISTRE INCOMPLET : 3 OUTILS DE DEMARRAGE NON DECLARES (Clio, inter-round Janus D1)

**Contexte** : lors de ma mission verifier (README doit-il refleter la reparation), j ai declare au registre seulement consulter-lecons + mettre-a-jour-readme. Janus a signale D1 (VERDICT A REVOIR) : guider-parcours, lire-fichier, lire-activite-recente MANQUANTS (non auto-journalises).

**Lecon** : la case c19 de ma carte ordonne "un appel a enregistrer-usage-outil PAR OUTIL" - TOUS les outils utilises dans la mission, y compris ceux de demarrage (guider-parcours, lire-fichier, lire-activite-recente), doivent etre declares au registre en mode direct (convention des autres agents). Un registre incomplet declenche une boucle KO de Janus.

**Corrige** : 3 entrees ajoutees (22:09:19). Rapport : janus/controles/controle-clio-verifier-readme-reparation-2026-08-23.md.
## [LECON] 2026-08-24 -- MISSION P1 README-DEV : CATEGORIE GIT AJOUTEE (DEVIATION)

**Contexte** : deviation Pattern 7 (bilan consolide) - P1 : readme-dev incoherence interne, tableau section 6 somme 164 vs total reel 165 (categorie Git manquante, outil hades-contexte-git). Detecte par mettre-a-jour-readme --verifier [ECART SOMME].

**Deroulement** : j'ai confirme P1 (verifier + combo-maj-readme), mais editer-fichier est VERROUILLE pour clio (habilites : buffy, hermes, minerve, promethee, redacteur-v2) -> redirection verrou vers buffy (habilitee) qui a insere la ligne '| Git | 1 | hades-contexte-git |' entre Gerer et Guider. Verifier final : [OK] 40 categories, somme 165 = total reel 165.

**Lecons** :
1. JE N'AI PAS D'OUTIL D'EDITION DIRECTE VERROUILLE : editer-fichier n'est pas dans mes habilitations -> pour une correction ciblee hors mettre-a-jour-readme, je passe par l'agent habilite (buffy) via la redirection verrou (jamais de contournement).
2. MEME EN MISSION DE DIAGNOSTIC SANS CORRECTION EFFECTIVE, JE DECLARE MES USAGES D'OUTILS (guider-parcours, lire-fichier, combos-moteur...) - lecon deja apprise en D1 (23/08), reaffirmee ici.
3. LE VERIFIER EST MA SOURCE DE VERITE : [OK] somme = total = le tableau readme-dev est coherent.

**Preuves** : verifier [OK] 165=165, rapport janus/controles/controle-deviation-3-lots-2026-08-24.md.
## [LECON] 2026-08-24 -- README-V2.MD REDIGE (EXCEPTION REDACTION V2)

**Contexte** : mission de rediger cerveau-projet/README-v2.md (grand
public v2, equipe freelance) avec l EXCEPTION REDACTION V2 (decision
utilisateur 2026-08-24).

**Verdict** : fichier cree (190 lignes, ASCII 0/0, frontmatter YAML FERME
ligne 8, ton 1ere personne, badges dynamiques : 10 agents (9 MARVEL +
Hades), 20 protocoles, M1-M7, 11 modules tools-commun, ~600 messages
JARVIS, JARVIS v0.9.x). Dry-run AVANT/APRES presente et VALIDE par
l utilisateur avant ecriture.

**Lecons** :
1. L EXCEPTION REDACTION V2 fonctionne : un agent lie a un fichier unique
   peut rediger un NOUVEAU document si la fiche + la carte sont preparees
   (lecon Chiron respectee : la pedagogie precede l activation).
2. Le dry-run AVANT/APRES + validation utilisateur sont LA garantie avant
   toute ecriture.
3. Les badges dynamiques se comptent sur les sources reelles (agents,
   modules, protocoles), pas sur des suppositions.

**Preuves** : README-v2.md (190 lignes, ASCII 0/0, frontmatter ferme) ;
sources verifiees (conventions, M1-M7, protocoles, tools-commun 11
modules, jarvis v0.9.x) ; validation utilisateur du dry-run ; lecon BDD.
