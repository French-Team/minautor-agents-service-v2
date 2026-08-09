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