# Rapport d'audit -- RE-AUDIT COMPLET DES 14 PATTERNS (11 parcours)

**Date** : 2026-08-09
**Auditrice** : Themis (session-llm-1)
**Procedure** : 4c de la spec-guider-parcours v0.2.25 (re-audit integral 1 a 4l)
**Perimetre** : les 11 parcours (athena, atlas, buffy, cerberus, clio, janus,
minerve, morpheus, promethee, themis, vulcain)

---

## 1. Synthese globale

| Verdict | Parcours |
|---|---|
| **CONFORME** | cerberus (0 ecart) |
| **ECARTS P2/P12** | athena, atlas, buffy, clio, janus, minerve, morpheus, promethee, themis, vulcain |

**Verdict global : NON CONFORME a 100 %** -- 10 parcours sur 11 portent des
ecarts structurels sur 2 patterns : P2 (rappel ASCII position 1) et P12
(creation limitee). Le pattern le plus regressif : P2, dont la regle a ete
deplacee de la position 1 par les ajouts recents (piste B, workspace).

---

## 2. Resultats par pattern

### Conformes (11/11 parcours)

| Pattern | Verification | Resultat |
|---|---|---|
| P1 multi-missions | case Mission c1 + Mission hors perimetre dans chaque parcours | CONFORME |
| P3 combos | indices combo references (valider-cartes-decision 11/11) | CONFORME |
| P4 question honnete | c0 question + c0b RELIRE + case_depart=c0 | CONFORME |
| P5 delegation active | 0 formulation passive (grep te reactive / j attends / attend le retour) | CONFORME |
| P6 contexte temps reel | c0c CONTEXTE + lire-activite-recente sur les 11 | CONFORME |
| P7 modele compose | 0 decision a branche unique (min 2 branches) | CONFORME |
| P8 chaine bout-en-bout | fins actives, retour par la carte | CONFORME |
| P9 lire le .md avant usage | guider-parcours v0.3.1 (>= v0.3.0) ; verifier-documents-manquants : 0 vrai manquant (4 .md de combos = faux positifs connus, ce sont des combos pas des outils) | CONFORME |
| P10 une carte = un role | valider-cartes-decision --agent : 11/11 CONFORME | CONFORME |
| P11 conformite d execution | case c8b presente dans parcours-themis ; executions recentes conformes | CONFORME |
| P13 la fin suit SA carte | case c8d presente ; fins actives conformes | CONFORME |
| ASCII / LF | 0 non-ASCII, 0 CRLF sur les 11 parcours | CONFORME |

### Ecarts (Pattern 2 -- position 1 ASCII) : 28 ecarts sur 10 parcours

La procedure 2 exige que le PREMIER element des indices de chaque case
d'ecriture soit `REGLE IMMUABLE ASCII`. Les ajouts recents (piste B
"PASSE PAR LE GENERATEUR", "REGLE WORKSPACE", "CREATION LIMITEE") ont ete
inseres en position 1, repoussant la regle ASCII en position 2+.

| Parcours | Nb | Cases |
|---|---|---|
| athena | 2 | c4 (PASSE PAR LE GENERATEUR), c5 (REGLE WORKSPACE) |
| atlas | 4 | c9, c18, c19, c25 (CREATION LIMITEE en position 1) |
| buffy | 9 | c5, c7, c11, c15, c19, c20, c24, c25, c10c (REGLE WORKSPACE) |
| janus | 4 | c2, c11, c18 (WORKSPACE), c9 (REGLE IMMUABLE RVAV) |
| minerve | 3 | c4 (GENERATEUR), c5, c8 (WORKSPACE) |
| morpheus | 1 | c8 (WORKSPACE) |
| promethee | 3 | c4 (GENERATEUR), c5, c8 (WORKSPACE) |
| themis | 1 | c9 (WORKSPACE) |
| vulcain | 1 | c12 (WORKSPACE) |

**Cause racine** : les corrections recentes (piste B indice generateur,
regle workspace) ont ete inserees en tete des indices sans respecter la
position 1 ASCII -- la regle ASCII existe mais n est plus en position 1.

### Ecarts (Pattern 12 -- CREATION LIMITEE) : 37 ecarts sur 10 parcours

La procedure 4j exige que toute case de creation/documentation porte un
indice regle CREATION LIMITEE precisant le perimetre et les roles exclus.

| Parcours | Nb | Exemples de cases |
|---|---|---|
| athena | 4 | c4, c5, c9 (Lecons), c14 |
| atlas | 2 | c10 (Lecons), c14 (Documenter la source) -- note : c9/c18/c19/c25 ont DEJA le garde-fou |
| buffy | 9 | c5, c7, c11, c15, c19, c20, c24, c25, c10c |
| clio | 2 | c8, c10 (Lecons) |
| janus | 4 | c2, c9, c11, c18 |
| minerve | 5 | c4, c5, c8, c9, c14 |
| morpheus | 1 | c8 |
| promethee | 5 | c4, c5, c8, c9, c14 |
| themis | 2 | c9, c12 (Lecons) |
| vulcain | 3 | c4, c6, c12 |

**Note** : les cases "Lecons et retour" (retour dans corrections.md) sont
comptees comme cases de creation/documentation par la procedure 4j -- elles
doivent porter le garde-fou au meme titre que les autres.

### Ecart (Pattern 14 -- verification d impact) : 1 fichier

| Fichier | Statut |
|---|---|
| cerveau-projet/agents/vulcain/vulcain.md | NON MIS A JOUR (mtime 11:02 vs parcours-vulcain.json 12:28) |

detecter-impacts sur parcours-vulcain.json : la fiche vulcain.md est plus
ancienne que le parcours -- l identification (version du parcours) n a pas
ete mise a jour lors des dernieres modifications.

---

## 3. Criteres d'acceptation appliques (1 a 25)

- Criteres 1-12, 14-21, 23, 25 : CONFORMES (structure, navigation, ASCII,
  contexte temps reel, modele compose, outils de reference)
- Critere 13 (fin passive) : CONFORME (0 formulation passive)
- Critere 22 (conformite d execution) : CONFORME
- Critere 24 (la fin suit SA carte) : CONFORME

## 4. Methodes utilisees

- guider-parcours (navigation, mode agent non-bloquant)
- valider-cartes-decision --agent (11/11 CONFORME)
- valider-conformite-ascii (0 non-ASCII sur les 11)
- verifier-documents-manquants (P9 : 0 vrai manquant)
- detecter-impacts (P14 : 1 ecart vulcain.md)
- Scripts d'audit structurel (positions des indices, branches, fins)
  -- supprimes apres usage (0 fichier residuel)

## 5. Actions recommandees

1. **P2 (28)** : deplacer la regle `REGLE IMMUABLE ASCII` en position 1 des
   indices de chaque case d'ecriture ecartee (les regles PASSE PAR LE
   GENERATEUR, WORKSPACE, CREATION LIMITEE passent en position 2+) -- via
   generateurs-case (outil de reference, critere 17).
2. **P12 (37)** : ajouter l'indice regle CREATION LIMITEE (perimetre +
   roles exclus) sur les cases de creation/documentation ecartees -- la
   carte atlas c9/c18/c19/c25 sert de modele de reference.
3. **P14** : mettre a jour l identification (version du parcours) dans
   vulcain.md.
4. Re-audit 4c complet apres corrections.
