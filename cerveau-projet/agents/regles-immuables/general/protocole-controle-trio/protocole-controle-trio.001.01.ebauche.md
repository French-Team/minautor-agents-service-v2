---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Controle du Travail du Trio (athena, promethee, minerve)

**Version** : 0.2.0
**Statut** : Ebauche
**Date creation** : 2026-08-11
**Agent** : Janus (controleur croise)

---

## Objectif

Definir comment Janus effectue le second controle (controle croise) du travail
du TRIO de preparation de projet : **athena** (pense-betes), **promethee**
(specs) et **minerve** (todos).

**Pourquoi ce protocole ?**
- Le trio prepare les livrables qui seront utilises pour le developpement des
  applications futures : pense-bete -> spec -> todo. Leur travail est
  **DETERMINANT** : une spec incomplete ou un todo mal structure en amont se
  repercutent sur toute la chaine de production.
- Janus etait calibre pour le controle des OUTILS de Vulcain (combo-controle-
  outil) puis des DOCUMENTS de Buffy (protocole-controle-buffy). Le travail du
  trio est une **CHAINE DE PRODUCTION** : chaque maillon depend du precedent.
- Decision 2026-08-11 : chaque agent du trio active JANUS a sa fin (second
  controle) - le protocole materialise ce que Janus doit verifier a chaque
  maillon.
- Ce protocole capitalise les lecons des controles passes (liens, format,
  coherence des chaines, index).

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Mission d'un agent du trio terminee | Le pense-bete / la spec / le todo a ete cree ou complete et la lecon est ajoutee dans corrections.md |
| 2 | Activation par Cerberus ou par l'agent du trio | Je ne m active jamais moi-meme (independance du controle) |
| 3 | Relecture de ma fiche et de mes corrections | Garde-fou relecture avant de commencer |
| 4 | Contexte de la mission | Je connais le maillon de la chaine controle (athena, promethee ou minerve) et le livrable attendu |
| 5 | Etat git de reference | Le recoupement git status est l outil principal d identification |

---

## Etapes

```
MISSION DU TRIO -> IDENTIFIER LES LIVRABLES -> INTEGRITE -> DOCUMENTAIRE
      1                    2                       3           4
-> CHAINE -> FORMAT/TEMPLATES -> INDEX -> SECURITE -> VERDICT -> RAPPORT
    5            6               7         8          9         10
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Identifier les fichiers crees/modifies | Recouper la mission avec git status : seuls les fichiers attendus (pense-betes/, specs/, todos/) sont touches | git status, lister-fichiers |
| E2 | PREUVE D INTEGRITE | git status VIDE sur les fichiers NON concernes - preuve plus fiable qu un contenu attendu | git status |
| E3 | Verification documentaire | ASCII strict + LF pur + tableaux valides + liens internes sur TOUS les fichiers modifies | valider-conformite-ascii, valider-tableaux, valider-liens, evaluer-coherence |
| E4 | Coherence de la CHAINE | Le maillon controle s appuie sur le maillon precedent QUI EXISTE : spec creee depuis un pense-bete reference, todo cree depuis une spec referencee (chaine athena -> promethee -> minerve) | lister-fichiers, lecture, rechercher-texte |
| E5 | Format et templates | Le livrable respecte son template : pense-bete (Header : Statut/ID/Class/Cree/Theme + sections), spec (Header + sections), todo (phases 0 a 9 + titre) | lecture, valider-conformite-ascii |
| E6 | Index a jour | Le livrable est reference dans son index : index-pense-bete.md, index-spec.md, index-todo.md | lecture, verifier-role-fichier |
| E7 | Conventions respectees | convention-protocoles, convention-structures, convention-nommage (prefixe nom.001.01.statut.md) | lecture, verifier-separation-preoccupations |
| E8 | Securite du travail (Pattern 12) | Creation limitee aux dossiers du cerveau (pense-betes/, specs/, todos/) - aucun fichier hors perimetre | detecter-usage-outils-externes, valider-nommage |
| E9 | Cartes et parcours du trio | JSON des parcours valide, cartes CONFORMES, fin c10 = 'FIN - Activer Janus' avec la COMMANDE EXACTE (activer-agent-principal.py activer session-llm-1 janus), Pattern 14 dans la fiche | valider-cartes-decision --agent athena/promethee/minerve |
| E10 | Verdict + rapport | Verdict VALIDE / A REVOIR / REJETE, rapport documente dans janus/controles/ | - |

---

## Chaine de transmission et boucle de correction

> **Role de Janus (v0.2.0)** : Janus n est pas seulement un verificateur final, il
> est le **POSTE DE CONTROLE DE LA CHAINE** : chaque maillon du trio l active a
> sa fin, il valide, puis **transmet au maillon suivant** (sans repasser par
> Cerberus). En cas de non-conformite, il **renvoie le rapport a l agent
> concerne** qui corrige puis le reactive. Il ne transmet JAMAIS un livrable non
> conforme en aval : la qualite est garantee maillon par maillon.

```
athena (pense-bete) -> JANUS -> promethee (spec) -> JANUS -> minerve (todo)
     -> JANUS -> Cerberus (fin de chaine, rapport global)
```

### Deroulement de la ligne trio (dans la carte de Janus, branche 'trio')

| Etape | Qui | Action |
|---|---|---|
| 1 | athena | Termine son pense-bete puis ACTIVE Janus (c10, commande exacte) |
| 2 | Janus | cT1 : lit ce protocole ; cT2 : identifie le maillon ; cT3/cT4/cT5 : controle le livrable (E1 a E10) |
| 3a | Janus | Verdict OK sur athena -> cT6 : ACTIVE promethee avec le pense-bete valide (transmission, PAS reactiver) |
| 3b | Janus | Verdict KO sur athena -> cT8 : RENVOIE le rapport a athena (elle corrige puis reactivera Janus) |
| 4 | promethee | Termine sa spec puis ACTIVE Janus (c10) |
| 5 | Janus | cT4 : controle la spec -> OK : cT7 ACTIVE minerve / KO : cT9 renvoie le rapport a promethee |
| 6 | minerve | Termine son todo puis ACTIVE Janus (c10) |
| 7 | Janus | cT5 : controle le todo -> OK : c10 REACTIVE Cerberus (fin de chaine, rapport global) / KO : cT10 renvoie le rapport a minerve |
| 8 | agent du trio | Boucle KO : recoit le rapport, c9f (branche 'corriger' de SA carte) CORRIGE le livrable, puis re-ACTIVE Janus |

### Boucle de correction (KO)

```
JANUS (KO) -> active l agent concerne avec le rapport
   -> l agent : branche 'corriger' (c9f) -> modifie UNIQUEMENT le livrable
   -> l agent reactivera Janus -> JANUS revalide -> OK : transmission au suivant
```

> **REGLE D EXCELLENCE** : Janus insiste sur la QUALITE de chaque livrable - un
> pense-bete de reference, une spec complete, un todo structure. Le travail du
> trio prepare la future team de codeurs : un livrable passe en aval uniquement
> s il est EXCELLENT, pas seulement acceptable. En cas de doute, verdict A
> REVOIR et renvoi du rapport.

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| [R]echercher | Lister les fichiers du trio (git status) et les maillons amont de la chaine (pense-bete -> spec -> todo) |
| [V]erifier | Appliquer E1 a E9 : la checklist complete du travail de production |
| [A]nalyser | Distinguer les VRAIS ecarts des faux positifs (fichiers d exemples de doc, cibles fictives des templates) |
| [V]alider | Donner le verdict (VALIDE / A REVOIR / REJETE) et documenter le rapport |

> **REGLE ABSOLUE** : Je ne donne JAMAIS de verdict sans avoir verifie la boucle
> RVAV complete. Je ne CORRIGE pas, je SIGNALE. Le travail du trio est
> DETERMINANT : en cas de doute, le verdict penche vers A REVOIR plutot que
> VALIDE.

---

## Exemples

### Exemple 1 : controle d'une spec creee par promethee

```
Mission : promethee cree une spec depuis un pense-bete
Controle Janus :
  E1 : git status -> spec creer + index-spec.md modifie (attendus)
  E2 : git status sur pense-betes/ -> VIDE (integrite : le pense-bete n a pas
       ete touche)
  E4 : lecture -> la spec reference le pense-bete source qui existe -> OK
  E5 : format -> Header + sections conformes a spec-template.md -> OK
  E6 : index-spec.md contient bien la nouvelle spec -> OK
  E9 : valider-cartes-decision --agent promethee -> CONFORME + fin c10
       'FIN - Activer Janus' avec commande exacte -> OK
  E10 : VERDICT VALIDE
```

---

## Pieges courants

| Piege | Consequence | Parade |
|---|---|---|
| **Chaine cassee** | Une spec creee sans pense-bete amont, ou un todo sans spec : le maillon est orphelin | Verifier SYSTEMATIQUEMENT le maillon precedent (E4) : l agent ne peut pas produire en aval sans amont |
| **Fichiers d exemples de doc** | Les .md de doc des outils (valider-liens.md, etc.) et les templates du trio utilisent des cibles FICTIVES : un controle generique les signalerait a tort | Verifier LEUR motif caracteristique ; git status vide = intacts |
| **Index non mis a jour** | Le livrable existe mais n est pas reference dans son index : invisible pour la chaine de production | Toujours verifier E6 (index-pense-bete / index-spec / index-todo) |
| **Format de fin obsolete** | La fin c10 du trio doit etre 'FIN - Activer Janus' avec la commande exacte - une fin 'Reactiver Cerberus' (ancien modele) casse la chaine de controle | Verifier E9 avec valider-cartes-decision + lecture du message |
| **Correction au lieu de signalement** | Je ne suis pas habilite a corriger | Je documente uniquement les problemes, l agent du trio ou l agent habilite corrige |
| **Transmission d un livrable non conforme** | Transmettre en aval un pense-bete/spec/todo avec des ecarts : l erreur se propage dans toute la chaine | Renvoyer le rapport a l agent concerne (boucle KO) - JAMAIS de transmission sans verdict OK |
| **Retour a Cerberus au milieu de la chaine** | La fin de Janus (reactiver) n est legitime qu apres le dernier maillon (minerve OK), et seulement via le PILOTE | Les fins cT6/cT7 suivent le modele aero : reactiver-fin --cible oracle ; c est le pilote qui ramene a Cerberus en fin de round |

---

## Liens

| Reference | Usage |
|---|---|
| [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md) | Structure des protocoles (en-tete + 7 sections) |
| [protocole-controle-buffy](../protocole-controle-buffy/) | Protocole de Janus pour le controle du travail documentaire de Buffy (modele) |
| [protocole-audit-buffy](../protocole-audit-buffy/) | Protocole de Themis (audit de conformite du travail de Buffy) |
| [protocole-controle-statuts](../protocole-controle-statuts/) | Protocole historique de Janus (statuts) |
| [pense-bete-template](../../../../pense-betes/pense-bete-template.md) | Template des pense-betes (athena) |
| [spec-template](../../../../pense-betes/specs/spec-template.md) | Template des specs (promethee) |
| [todo-template](../../../../pense-betes/specs/todo/todo-template.md) | Template des todos (minerve) |
| [rvav-workflow](../rvav-workflow.md) | Boucle obligatoire avant verdict |
| [regles-validation-rigoureuse](../regles-validation-rigoureuse.md) | Validation rigoureuse |
| [arbre-janus](../../../../agents/janus/parcours/arbre-janus.json) | Ligne trio (branche 'trio') implementee dans l arbre de Janus |
