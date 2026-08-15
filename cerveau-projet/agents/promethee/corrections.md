---
identite:
  type: corrections
  appartient_a: promethee
  commun: false
# Corrections et Surcharges -- Promethee
# Agent dedie aux specs

agent:
  nom-agent: "promethee"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-06"

---

# Corrections et Surcharges

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **Pense-bete source obligatoire** | Je ne cree pas de spec sans un pense-bete source |
| **Template obligatoire** | Chaque spec utilise le spec-template, jamais un format libre |
| **Activer Minerve** | A la fin de ma mission, j'active Minerve pour le todo |
| **Index mis a jour** | Apres creation, la spec est ajoutee dans index-spec.md |

---

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

| Philosophie | Description |
|---|---|
| **La spec est la source de verite** | Elle est la reference technique de tout le projet |
| **Exigences claires** | Chaque exigence a un critere d'acceptation mesurable |
| **Ne pas inventer** | Je travaille uniquement a partir du pense-bete source |

---

## LECONS -- Lecons apprises

| Date | Lecon | Philosophie liee |
|---|---|---|
| 2026-08-06 | Creation de l'agent -- premieres lecons a venir | La spec est la source de verite |

---

## CONFIG -- Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Complet"
  style_reponse: "Technique"
```

### Outils et methodes

| Outil/Method | Usage |
|---|---|
| `generateurs-squelette-spec` | Generer le squelette de la spec |
| `creer-remplir-spec` | Remplir les sections sans ouvrir le fichier |
| `valider-spec` | Valider l'integrite de la spec |
| `activer-agent-principal` | Activer Minerve en fin de mission |

---

## CONNEXIONS -- Connexions

| Fichier | Role |
|---|---|
| `promethee.md` | Fiche principale de l'agent |
| `AGENTS.md` | Fichier dynamique de l'agent principal |
| `../index-agents.md` | Index des agents |
| `../../pense-betes/specs/index-spec.md` | Index des specs |
| `../../pense-betes/specs/spec-template.md` | Gabarit des specs |
| `../../agents/regles-immuables/general/regles-emojis-ascii.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/regles-veracite.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/rvav-workflow.md` | **OBLIGATOIRE** |
## [LECON] 2026-08-09 -- Pattern 12 CREATION LIMITEE documente dans la spec-guider-parcours (v0.2.21 -> v0.2.22)

**Mission** : generaliser le garde-fou CREATION LIMITEE (une carte = un role applique aux cases de creation) comme pattern standard dans la spec-guider-parcours, suite a l'incident Atlas (l'explorateur a ecrit un OUTIL dans explorations/ au lieu de signaler le besoin).

**Lecons** :
1. Une ancre de remplacement doit etre verifiee sur le fichier REEL avant insertion : la premiere ancre (rapports de l'agent audite.) etait scindee sur 2 lignes dans le fichier (et les rapports de / l'agent audite.) - l'insertion a echoue 2 fois avant de passer par un append en fin de fichier
2. Un script d'edition doit compter le nb d'occurrences de chaque ancre (1 attendu) et signaler clairement si l'ancre est absente ou multiple - jamais appliquer un remplacement aveugle
3. Le Pattern 12 s'articule en 3 endroits de la spec : la section pattern (definition), la procedure d'audit 4j (verification) et le critere 23 (audit themis) - les 3 doivent etre coherents (version v0.2.22 partout)
4. detecter-impacts signale les fiches agents comme NON MIS A JOUR (reference) : faux positifs (les fiches referencent la spec par CHEMIN, jamais par version) - verifier par un grep de version avant de corriger quoi que ce soit
5. Le garde-fou generalise : toute case de creation porte un indice regle CREATION LIMITEE (perimetre + roles exclus outil->Vulcain, test->Morpheus, case->Buffy) + une case Signaler le besoin renvoie vers l'agent habilite, jamais vers une action directe
## [LECON] 2026-08-09 -- PATTERN 13 DOCUMENTE (v0.2.23, spec-guider-parcours)

**Mission** : documenter le Pattern 13 (LA FIN SUIT SA CARTE - generalisation de la regle de retour) dans la spec-guider-parcours, avec le piege du double CRLF comme lecon technique.

**Livrables** :
1. Section `### Pattern 13 -- LA FIN SUIT SA CARTE (v0.2.23)` (lignes 1031-1086) : regles 1-4 (activation directe -> reactiver Cerberus ; maillon de chaine -> activer le suivant selon SA carte ; dernier maillon -> reactiver Cerberus avec bilan consolide ; la chaine ne retombe JAMAIS sur Cerberus au milieu), lien avec le Pattern 8, exemple JSON (fin activation directe vs fin delegation), piege technique CRLF
2. Procedure d'audit `### 4k. Pattern 13` (verification de la fin attendue par la carte + coherence avec le type d'activation)
3. Critere 24 (LA FIN SUIT SA CARTE) pour les audits Themis
4. Mises a jour de coherence : titre de section "Procedure d'audit des 13 patterns", liste "Patterns valides en production" + v0.2.23, bloc Agent + v0.2.23, Historique + v0.2.23
5. Spec passee de v0.2.22 a v0.2.23 (8 occurrences verifiees)

**Validations** : ASCII 0 / LF pur preserve (1484 lignes, 0 CRLF) / 13 modifications appliquees / structure coherente (Pattern 13 entre Pattern 12 et Procedure).

**Lecons** :
1. Le Pattern 13 s'articule en 4 endroits : bloc Agent + Historique (coherence versionnelle), section pattern (definition), procedure 4k (verification), critere 24 (audit Themis) - tous coherents en v0.2.23
2. Le piege du double/triple CRLF (lecon Buffy) est maintenant FIGE DANS LA SPEC comme lecon technique : lire/ecrire avec newline='' (aucune conversion), reparer avec re.sub(r'\r+\n', '\r\n', txt)
3. Meme un script d'edition temporaire doit respecter la regle ASCII stricte : un accent dans un commentaire (ex: "inchange") suffit a casser l'execution (SyntaxError: encoding problem: ascii)
4. La regle "la fin suit SA carte" remplace definitivement "toujours reactiver Cerberus" : verifier desormais que les audits (procedures 4i/4k) verifient la COHERENCE entre la case de fin et le type d'activation, pas seulement la presence d'une fin
## [LECON] 2026-08-09 -- PATTERN 14 DOCUMENTE (v0.2.24, spec-guider-parcours)

**Mission** : documenter le Pattern 14 (VERIFICATION D IMPACT GENERALISEE - la verification d impact detecter-impacts devient un pas OBLIGATOIRE de TOUTE procedure d audit Themis) dans la spec-guider-parcours, sur decision utilisateur 2026-08-09.

**Livrables** :
1. Section `### Pattern 14 -- VERIFICATION D IMPACT GENERALISEE (v0.2.24)` (apres le Pattern 13) : regles 1-5 (identifier les fichiers modifies, lancer detecter-impacts sur un echantillon representatif, verifier que TOUS les fichiers impactes sont mis a jour, tout impact NON mis a jour = NON CONFORME, outil de reference avec son .md), lien avec le Pattern 11 (processus vs livrables), rappel du piege CRLF
2. Procedure d'audit `### 4l. Pattern 14` (5 etapes, inseree entre 4k et la section 5 Cas particuliers)
3. Critere 25 (VERIFICATION D IMPACT GENERALISEE) ajoute apres le critere 24
4. Mises a jour de coherence : titre "Procedure d'audit des 14 patterns", liste "Patterns valides en production" + v0.2.24, bloc Agent + v0.2.24, Historique + v0.2.24
5. Spec passee de v0.2.23 a v0.2.24 (7 occurrences verifiees)

**Validations** : ASCII 0 / LF pur preserve (1543 lignes, 0 CRLF) / 7/7 modifications / structure coherente (Pattern 14 entre Pattern 13 et Procedure, 4l entre 4k et section 5, critere 25 en fin de fichier) / coquille corrodent corrigee.

**Lecons** :
1. Le Pattern 14 s'articule en 4 endroits : bloc Agent + Historique (coherence versionnelle), section pattern (definition), procedure 4l (verification), critere 25 (audit Themis) - tous coherents en v0.2.24
2. Un PATTERN D'AUDIT (procedure) se distingue d'un pattern de carte : il ne change pas la structure des parcours, il enrichit la grille d'audit que Themis applique a CHAQUE mission - le documenter dans la section Procedure est aussi important que la section pattern
3. detecter-impacts etait deja branche ponctuellement (parcours themis c8b, rapport-audit-janus) mais SANS procedure generalisee : la lecon "un outil existe mais n est pas branche = invisible" s'applique - la generalisation passe par la PROCEDURE d audit, pas par les cas
4. Rappel du piege double/triple CRLF confirme : lire/ecrire avec newline='' (aucune conversion) - la spec est restee en LF pur (1543 lignes, 0 CRLF)
5. Meme un script d'edition temporaire doit respecter ASCII strict (lecon deja apprise au Pattern 13 - cette fois aucun accent dans le script)
## [LECON] 2026-08-09 -- RE-AUDIT COMPLET GENERALISE A 14 PATTERNS (v0.2.25, spec-guider-parcours)

**Mission** : generaliser la procedure 4c (RE-AUDIT COMPLET) a TOUS les patterns (14 maintenant), suite logique du Pattern 14 - decision utilisateur (lecon Themis : rejouer TOUTES les procedures, jamais seulement la nouvelle).

**Livrables** :
1. Procedure 4c reecrite : titre RE-AUDIT COMPLET DES 14 PATTERNS (v0.2.25), point 1 liste TOUTES les procedures 1-4l dans l ordre (1, 2, 3, 4, 4b, 4c, 4d, 4e, 4f, 4g, 4h, 4i, 4j, 4k, 4l), point 2 nb procedures 11 -> 14 + lecon (la liste doit etre re-verifiee a chaque ajout de pattern), point 4 TOUS les criteres 1 a 25, point 5 la procedure 4l est un pas OBLIGATOIRE du re-audit
2. Ligne 361 : Les 13 patterns suivants -> Les 14 patterns suivants
3. Critere 14 : RE-AUDIT COMPLET DES 12 PATTERNS -> DES 14 PATTERNS + liste complete 1-4l + criteres 1 a 25
4. Coherences : bloc Agent + v0.2.25, Historique + v0.2.25
5. Spec passee de v0.2.24 a v0.2.25 (4 occurrences verifiees)

**Validations** : ASCII 0 / LF pur preserve (1554 lignes, 0 CRLF) / 5/5 modifications / 0 occurrence restante de 12 PATTERNS / 13 patterns (hors historique) / structure coherente.

**Lecons** :
1. Le re-audit complet (procedure 4c) avait VIEILLI : il listait 12 patterns pendant que 4i (Pattern 11), 4k (Pattern 13) et 4l (Pattern 14) s ajoutaient - la liste des procedures doit etre RE-VERIFIEE a chaque ajout de pattern, sinon le re-audit lui-meme devient incomplet (meta-lecon : le garde-fou vieillit si on ne le re-audite pas)
2. La generalisation s articule en 3 endroits : procedure 4c (le processus), ligne des patterns valides (le compte), critere 14 (la grille d audit) - tous coherents en 14
3. Le critere 14 doit couvrir TOUS les criteres 1 a 25 (pas seulement ceux lies au pattern recent) : la conformite d un parcours = TOUS les criteres
4. Le piege CRLF confirme encore : lire/ecrire avec newline='' (aucune conversion) - la spec est restee en LF pur (1554 lignes, 0 CRLF)
5. Un caractere non-ASCII dans la raison d activation (COEUR -> ecrit OEU) fait REFUSER l activation par l outil : la regle ASCII s applique aussi aux messages d activation, pas seulement aux fichiers
## [LECON] 2026-08-09 -- SPEC REFONTE CARTES DE DECISION REDIGEE (v0.1.0)

**Mission** : rediger la spec de refonte du concept des cartes de decision et
des cases (decision utilisateur : spec d abord - valider le concept AVANT de
coder), suite au diagnostic des 2 problemes : cartes cablees mais NON
EXECUTEES (conformite Morpheus/Janus manquee sur generateurs-amelioration) +
degradation conceptuelle (buffy 49 cases/45 Ko, 15 patterns, indices empiles).

**Livrables** :
- `pense-betes/specs/spec-refonte-cartes-decision.001.01.ebauche.md` (v0.1.0,
  10 sections : objectif, contexte+vision verbatim, probleme, modele case
  composee, principe case fournie a la demande, contrat validateur-case,
  evolution generateurs, plan 7 etapes, criteres 6, emplacement)
- `pense-betes/specs/index-spec.md` : ligne 001 ajoutee (remplace la ligne vide)

**Le concept de la spec (vision utilisateur)** :
1. CASE FOURNIE A LA DEMANDE : l'agent recoit UNE case, l'execute, valide --
   le SYSTEME fournit la suivante (principe catalogue). L'agent ne lit jamais
   la carte en entier.
2. CATALOGUES ALLEGES : les indices portent des REFERENCES (pattern-12,
   regle-ascii, protocole-tests) au lieu des textes inline > 160 caracteres.
3. VALIDATEUR-CASE (outil a creer) : valide structure + modele compose
   (branches min 2, deviation = rejoint) + surcharge + references mortes.
4. MODELE COMPOSE : decision + branches min 2 + deviation + rejoint genere en
   UNE commande par generateurs-case (generaliser ajouter-bloc Pattern 7).

**Validations** : ASCII 0 (2 recits corriges -> 0) - LF pur - frontmatter
(type: spec) OK - 10 sections - index-spec a jour ASCII 0 - 0 residu.

**Lecons** :
1. Spec d abord = le concept est valide AVANT de coder (aucune ligne de code
   n a ete ecrite pour cette etape) - c est le rempart contre la degradation.
2. La regle immuable ASCII s applique AUSSI aux specs : 2 accents (recit)
   echappaient - verifier systematiquement apres redaction.
3. Une spec de refonte doit CITER la vision utilisateur verbatim + le
   diagnostic factuel (tailles, chiffres) : c est la source de verite pour
   toutes les missions d implementation ulterieures.
4. Le plan d implementation reprend la chaine OBLIGATOIRE (Vulcain -> Morpheus
   tests -> Janus controle) pour chaque outil cree/modifie - la lecon de la
   conformite manquee est integree dans la spec (criteres 5).
## [LECON] 2026-08-09 -- SPEC-REFONTE v0.1.1 : TYPE action DECLARE NOUVEAU

**Mission** : clarifier le point mineur de l audit Themis (rapport-audit-spec-refonte) :
le type action etait presente comme "inchange" alors qu il n existe pas dans le
modele actuel (guider-parcours ne gere que fin/indice/question-controle ; aucun
des 11 parcours ne contient de case action). Decision utilisateur : DECLARER
action comme NOUVEAU type du modele cible.

**Modifications** (spec-refonte-cartes-decision.001.01.ebauche.md, v0.1.0 -> v0.1.1) :
1. Version 0.1.1 + ligne d historique (clarification, audit Themis)
2. Tableau 4.1 : ligne action marquee *(NOUVEAU - modele cible, a implementer
   a l etape 5 dans guider-parcours)*
3. Titre 4.1 : "Types de cases (existants + 1 NOUVEAU)" au lieu de "(inchange)"
4. Plan etape 5 : ajout "IMPLEMENTER LE TYPE action (nouveau, aujourd hui non
   gere : seul fin/indice/question-controle)"
5. Critere 7 : le type action implemente dans guider-parcours (comportement
   identique a indice sans indices)

**Validations** : ASCII 0 - LF pur - 10 sections intactes - index-spec inchange.

**Lecons** :
1. Un point mineur d audit se clarifie DANS la spec (source de verite) avant
   de lancer l implementation - jamais en cours de route.
2. Declarer un type NOUVEAU implique de mettre a jour TOUTES ses occurrences
   dans la spec (tableau, titre, plan, criteres) : coherence interne.
3. La spec v0.1.1 est la reference pour l etape 2 (validateur-case) : le type
   action y est explicite comme hors perimetre des etapes 2-4 (etape 5).
## [LECON] 2026-08-09 -- ETAPE 7 : spec-guider-parcours v0.5.0 (patterns REFERENCES, pas dupliques)

**Mission** : mettre a jour la spec-guider-parcours pour que les patterns soient des REFERENCES (source de verite) et non des textes dupliques dans les cases.
**Resultat** : spec v0.5.0 (1633 -> 1654 lignes), principe UNE PLACE POUR CHAQUE CHOSE documente, 4 exemples inline transformes en refs.
**Lecons** :
1. Le principe UNE PLACE POUR CHAQUE CHOSE est maintenant ecrit dans la spec : les patterns de la spec sont LA source de verite, une case POINTE (ref pattern-N) au lieu de copier. Consequences : modifier = 1 fichier, pas N cases ; une case ne derive jamais ; valider-case signale tout texte > 160 ou ref morte
2. 4 exemples inline transformes : exemple minimal c2 (verifier avant d'agir -> pattern-9 + type action), Pattern 5 c9a (RELAIS -> pattern-5), Pattern 10 c2 (je n execute JAMAIS -> pattern-10), Pattern 11 c8b (PATTERN 11 -> pattern-11)
3. Incoherence de version corrigee : titre ligne 7 (v0.2.27) vs Version ligne 9 (0.4.0) -> unifiees a 0.5.0 (v0.2.27 etait la version des patterns, 0.4.0 celle de la spec -- la spec avait evolue sans le titre)
4. References documentaires mises a jour : guider-parcours.md (Spec v0.2.27 -> v0.5.0) et vulcain.md (Spec du format v0.2.27 -> v0.5.0) -- detecter-impacts a confirme les impacts
5. Un exemple de case dans la spec doit etre la VITRINE du nouveau format : type action + indices ref, pas un exemple obsolette
6. Normes : ASCII strict + LF pur sur les 3 fichiers modifies (spec, .md, vulcain.md)
7. Non-regression : test-012 18/18 (resolution refs), test-013 22/22 (migration cerberus), detecter-decalages 112 conformes / 0 decalage

**Preuve** : spec v0.5.0 avec principe documente + 4 refs transformees + 0 inline > 160 ; test-012/013 OK.

## [LECON] 2026-08-10 -- PATTERN 16 ALLEGEMENT DOCUMENTE (spec-guider-parcours v0.6.0) (Promethee)

**Mission** : documenter le Pattern 16 (ALLEGEMENT des cases surchargees,
references resolues + combos, anti-doublon) dans la spec-guider-parcours,
apres validation du concept par l'utilisateur (avant les migrations).

**Modification** (spec-guider-parcours v0.5.0 -> v0.6.0) :
- Nouveau "### Pattern 16 -- ALLEGEMENT DES CASES SURCHARGEES (v0.2.28)"
  insere apres le Pattern 15, avec 6 etapes :
  1. DETECTER (valider-case A ALLEGER : > 3 indices ou texte > 160 car.) ;
  2. TRIER (regle/protocole longue -> reference resolue ; sequence d'outils
     -> combo Pattern 3) ;
  3. ANTI-DOUBLON OBLIGATOIRE (rechercher-texte dans les sources candidates :
     deja present -> referencer l'existante, partiel -> enrichir, absent ->
     creer) -- exigence utilisateur ;
  4. DEPLACER jamais supprimer (zero perte) ;
  5. PRISE EN COMPTE OBLIGATOIRE (guider-parcours resout et affiche) ;
  6. VERIFIER (valider-case CONFORME + resolvabilite + navigation).
- En-tete "Patterns valides en production" + "Procedure d'audit des 16
  patterns" mis a jour (v0.2.28 ajoute).
- Exemple reel documente (janus c8 -> protocole-controle-buffy ; c11/c18 ->
  combo partage).

**Lecons** :
- Une spec d'outil se met a jour comme une spec : appliquer la meme rigueur
  (structure, version, historique) que pour une creation.
- Le Pattern 16 est le modele a appliquer PENDANT les migrations des parcours
  v0.2.0 : allegement en cours de migration, pas apres.
- Anti-doublon = etape 3 obligatoire : la regle ne vit qu'a UN endroit.

**Outils utilises** : lire-fichier, editer-fichier, valider-conformite-ascii,
valider-liens, activer-agent-principal.
## [LECON] 2026-08-11 -- SPEC-REFONTE v0.1.2 : CONVENTION ETENDUE cT* ALIGNEE (Promethee, ecart detecte par detecter-convention-nommage)

**Contexte** : le nouvel outil detecter-convention-nommage v0.1.0 a detecte 1 ecart reel dans ma spec-refonte-cartes-decision (ligne 175 : "nommage des cases (c<numero>[a-z]?)" sans l'extension cT*). C'etait le SEUL fichier restant du cerveau-projet a citer l'ancienne convention.

**Lecon** :
1. Une spec de reference du cerveau doit citer la convention ETENDUE c[<prefixe-alpha-maj>]<numero>[a-z]? (cas normal + prefixe majuscule cT1..cT10, valider-case v1.0.2, spec-guider-parcours v0.6.2 regle 11) -- pas seulement la forme courte c<numero>[a-z]?.
2. Le garde-fou automatique detecter-convention-nommage couvre TOUT le cerveau-projet (pas seulement les outils) : il a trouve cet ecart dans docs-dev-cerveau-projet/ que l'audit Themis cible (famille generateurs-ligne) n'avait pas couvert.
3. Bump de version coherent : v0.1.1 -> v0.1.2 (titre ligne 9 + historique ligne 13) avec mention de l'alignement et de l'outil qui l'a detecte.
4. Verification en reel : re-scan detecter-convention-nommage -> 0 ecart sur cerveau-projet (VERDICT CONFORME, code 0) ; normes 0 non-ASCII / 0 CRLF.

## [LECON] 2026-08-11 -- SPEC-REFONTE v0.1.3 : BUDGET PONDERE DOCUMENTE (Promethee)

**Mission** : documenter le budget pondere des indices dans la spec-refonte-cartes-decision (spec de reference des outils de cases).
**Resultat** : spec v0.1.3, 3 endroits de l'ancienne regle alignes + mention dans la section 7.1 + version/historique.
**Lecons** :
1. La spec-refonte (spec de reference des outils de cases) doit refleter le modele implante dans valider-case/generateurs-case : court <= 100 car. = 0,5 unite, long > 100 car. = 1 unite, budget 3,0 unites par case, plafond absolu 160 car. inchange.
2. Quand une regle evolue dans les outils, scanner la spec de reference pour trouver TOUTES les mentions de l'ancienne regle (usage, verifications, criteres d acceptation, section generateurs) -- ici 3 endroits + 1 bonus.
3. Une version stale (valider-case v1.0.2 -> v1.1.0) peut subsister dans une section adjacente (bloc Normes convention ETENDUE) : la corriger pour la coherence avec la version implantee.
4. Le diff vs HEAD peut inclure des changements non commites anterieurs (v0.1.2 convention cT*) : verifier uniquement que MES modifications sont minimales et coherentes, sans reformatage.
5. Les lignes d'historique de version deviennent longues (> 120 car) : acceptable pour une ligne d'historique, mais verifier que les lignes de contenu restent raisonnables.

## [LECON] 2026-08-11 -- SCAN VERSIONS STALE DANS LES SPECS (Promethee)

**Mission** : scanner les specs pour detecter les versions "actuel" stale (classe section 7.1 spec-refonte) et les corriger.
**Resultat** : 8 specs corrigees, 0 ancienne version restante, detecter-divergences-version passe de 4 a 1 DIVERGENT (guider-parcours = cas inverse, observation).
**Lecons** :
1. Les versions "actuel" dans les titres de sections des specs (ex: "generateurs-case (v0.2.2 actuel)") se periment quand l'outil est bumpe : verifier systematiquement avec la VERSION reelle du .py.
2. L'outil detecter-divergences-version est le scan automatique de reference (spec en-tete vs py) : il a revele 3 specs non bumpees (combos-moteur 0.2.1->0.3.0, detecter-decalages 0.1.0->0.1.1, generateurs-case 0.4.0->0.4.2) - la spec est le fichier le plus souvent oublie lors d'un bump d'outil.
3. Le cas INVERSE existe : guider-parcours spec 0.6.2 vs py 0.5.0 (le py est en retard) - ce n'est PAS une spec stale, c'est un bump de code a traiter par Vulcain.
4. Attention aux references historiques legitimes : "spec-combos-moteur v0.2.1" dans le py = la version de la SPEC qui a etabli la regle (KO test-003), PAS la version du catalogue (0.2.9). Ne pas confondre.
5. Les mentions de versions dans le CORPS des specs (ex: "valider-case v1.0.2" dans les conventions de nommage) sont aussi des sources de stale : spec-valider-case (3x spec-refonte v0.1.1), detecter-convention-nommage, generateurs-ligne (4x), guider-parcours (2x).
6. CRITIQUE : corriger une version dans une spec peut CASSER un test formel qui verifie le texte exact (test-014 verifie litteralement "valider-case v1.0.2" in spec -> KO apres ma correction en v1.1.0). Toujours lancer la non-regression ciblee apres correction de spec ET signaler le KO a Morpheus (seul habilite pour les tests).

## [LECON] 2026-08-11 -- PATTERN 16 ALLEGEMENT ALIGNE SUR LE BUDGET PONDERE (spec-guider-parcours) (Promethee)

**Mission** : verifier la coherence budget pondere entre spec-refonte, spec-valider-case et spec-guider-parcours.
**Resultat** : spec-valider-case et spec-guider-parcours (PRINCIPE UNE PLACE) etaient deja coherents ; le Pattern 16 (ALLEGEMENT) de spec-guider-parcours decrivait encore l'ANCIENNE regle a 3 endroits -> corrige, bump v0.2.28 -> v0.2.29.
**Lecons** :
1. Une meme regle peut etre documentee a PLUSIEURS endroits dans une meme spec : le Pattern 16 (methode d'allegement) utilisait encore "plus de 3 indices" alors que le PRINCIPE UNE PLACE (meme spec, lignes ~140) documentait deja le budget pondere. Toujours scanner la spec COMPLETE pour toutes les occurrences de l'ancienne regle.
2. La verification de coherence (demande utilisateur) a revele l'ecart : spec-valider-case et spec-refonte etaient correctes, mais le Pattern 16 etait reste sur l'ancien modele. La verif croisee spec <-> spec est un controle utile (pas seulement spec <-> outil).
3. Le bump de version d'un pattern (v0.2.28 -> v0.2.29) doit etre coheren t sur TOUTES ses occurrences : titre du pattern (l.1224) + liste "Patterns valides en production" (l.409) + liste "Procedure d'audit" (l.1339).
4. Le test-014 ne verifie pas le texte du Pattern 16 (0 mention) : aucun risque de casser le test. Verifier AVANT de modifier qu'aucun test formel ne depend du texte change.
5. Le diff vs HEAD peut inclure des changements non commites anterieurs (v0.6.2 convention cT* + budget pondere deja documente) : verifier que MES modifications sont minimales et coherentes.

## [LECON] 2026-08-11 -- PROTOCOLE CREATION-SCRIPTS-TEMPORAIRES CREE (Promethee)

**Contexte** : mission anti-scripts-temporaires (3 outils + cartes renforcees + garde-fou test-024). Creation du protocole qui encadre l'usage des scripts temporaires.

**Protocole cree** : regles-immuables/general/protocole-creation-scripts-temporaires/ v0.1.0 ebauche, format 7 sections (Objectif, Prerequis, Etapes, RVAV, Exemples, Pieges courants, Liens).

**Cycle encadre (CREER/DECLARER/SUPPRIMER/PROMOUVOIR/DETECTER)** :
1. BESOIN ponctuel non couvert -> VERIFIER le catalogue d'abord
2. CREER via generateurs-outil-temporaire (jamais de script a la racine)
3. DECLARER au registre : enregistrer-usage-outil --mode script-temporaire
4. UTILISER puis SUPPRIMER (0 residu, test-024 vert)
5. PROMOUVOIR : 2e utilisation -> outil durable (Vulcain)
6. CONTROLER : Janus/Themis lancent detecter-usage-scripts-temporaires

**Verifications** : ASCII 0, LF 0, 7 sections, referencement index-regles-general (1 ligne), valider-ebauche OK.

**LE CONS** :
1. Le format 7 sections est la convention des protocoles de regles-immuables/general (Objectif, Prerequis, Etapes, RVAV, Exemples, Pieges courants, Liens).
2. L'index-regles-general.md doit etre mis a jour (ligne alphab?tique) des la creation d'un protocole.
3. Le cycle ferme la boucle du diagnostic : chaque script temporaire a une declaration, un controleur peut croiser les sources (racine/git/lecons) avec le registre.

## [LECON] 2026-08-15 -- PROTOCOLE SCRIPTS-TEMP v0.2.10 (Promethee)

**Contexte** : demande utilisateur - renforcer la regle entonnoir dans le protocole-creation-scripts-temporaires. La regle jamais python3 direct existait deja (v0.2.5) mais n a pas ete respectee : des scripts de fin en python3 direct ont reintroduit des CRLF (lecon 2026-08-15). Renforce v0.2.10 : PROTECTION DE SORTIE LF de l entonnoir v0.1.1 documentee (re-scanne les fichiers modifies pendant la fenetre) + POURQUOI JAMAIS python3 DIRECT explicite (append io.open a sans newline traduit LF en CRLF sur Windows) comme anti-recurrence.
VERDICT : VALIDE - protocole v0.2.10 documente, normes 0/0, test-049 11/11, test-024 16/16.
