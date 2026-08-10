---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole d Audit du Travail de Buffy

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-10
**Agent** : Themis (evaluatrice croisee)

---

## Objectif

Definir comment Themis audite la conformite du travail de Buffy, developpeur
principal des fichiers du cerveau-projet (protocoles, conventions, fiches,
lecons, index, parcours JSON, liens).

**Pourquoi ce protocole ?**
- Themis audite en global (audit des 11 parcours, audit de conformite) mais sans
  protocole dedie a la verification du travail documentaire de Buffy
- Le travail de Buffy est specifique : documents du cerveau, pas de code outil -
  les criteres d audit doivent couvrir la qualite documentaire ET la conformite
  d execution de SA carte
- Ce protocole s appuie sur les procedures d audit deja eprouvees (4i, criteres
  22-25, Pattern 14) et les applique au cas particulier de Buffy

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Mission de Buffy terminee (ou chaine passee par Janus) | Les fichiers ont ete modifies, lecons ajoutees |
| 2 | Activation par Cerberus ou par un agent (branche audit-agent) | Je n audite jamais de ma propre initiative |
| 3 | Relecture de ma fiche et de mes corrections | Garde-fou relecture avant de commencer |
| 4 | Contexte de la demande | La mission confiee a Buffy, sa carte (parcours-buffy.json) et le deroulement reel |
| 5 | Outils de controle | detecter-impacts, valider-cartes-decision, evaluer-coherence, detecter-divergences-version |

---

## Etapes

```
DEMANDE -> CROISEMENT MISSION/CARTE/DEROULEMENT -> CONFORMITE EXECUTION
   1                    2                               3
-> VERIFICATION IMPACT -> FIN SUIT SA CARTE -> REACTIVER -> QUALITE DOC
        4                     5                  6            7
-> PARCOURS/FICHES -> RAPPORT
       8                9
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Croiser mission / carte / deroulement reel | La mission de Buffy a-t-elle suivi SA carte case par case ? Relever les cases non citees (zones grises) | parcours-buffy.json, AGENTS-historique |
| E2 | Conformite d execution (c8b) | Relecture obligatoire respectee, outils de la carte utilises (pas de contournement systeme), les fins de Buffy activent Janus (c8/c22/c27 - REGLE IMMUABLE JANUS meme sans code) | AGENTS-historique, lecons Buffy |
| E3 | Verification d impact (Pattern 14, c8c) | detecter-impacts sur un echantillon des fichiers modifies : TOUS les fichiers impactes sont a jour ? | detecter-impacts |
| E4 | La fin suit SA carte (Pattern 13, c8d) | Buffy active Janus selon sa carte, elle ne reactive pas Cerberus directement | parcours-buffy.json, AGENTS-historique |
| E5 | Critere reactiver R1-R5 | Si Themis a ete activee par un agent (branche c25/c25b) : l agent a-t-il reactiver correctement l agent precedent avec son rapport ? | AGENTS-historique, AGENTS.md, classeur-variables |
| E6 | Qualite documentaire | ASCII strict, LF pur, liens internes (toutes formes : markdown + backticks), tableaux, conventions (en-tete + 7 sections) | valider-conformite-ascii, valider-liens, evaluer-coherence, valider-tableaux |
| E7 | Parcours et fiches | Versions coherentes (Pattern 14), cartes de decision valides, pas de divergence spec/py | valider-cartes-decision --tous, detecter-divergences-version |
| E8 | Piege lecons | Les lecons de Buffy ne contiennent pas d exemple de syntaxe de lien litteral (motif parasite) | evaluer-coherence, lecture |
| E9 | Rapport | Rapport dans themis/rapports/ au format de la fiche (Contexte, Resultats, Synthese, Recommandations) | - |

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| [R]echercher | Rassembler mission, carte, deroulement reel, fichiers modifies, outils de controle |
| [V]erifier | Appliquer E1 a E8 : checklist de conformite complete |
| [A]nalyser | Distinguer les VRAIS ecarts des zones grises (cases de la carte non tracees dans les lecons) et des faux positifs |
| [V]alider | Verdict CONFORME / NON CONFORME et rediger le rapport |

> **REGLE ABSOLUE** : Je ne donne JAMAIS de verdict sans avoir verifie la boucle
> RVAV complete. Je ne modifie jamais rien : j evalue, je croise, je synthetise
> et je rapporte.

---

## Exemples

### Exemple 1 : audit de conformite d execution (mission P14)

```
Mission : Vulcain met a jour l identification de vulcain.md (Pattern 14)
Audit Themis :
  E1 : croisement mission/carte -> c14 non execute (lacune de carte)
  E2 : c8b -> le point c14 manquant est une lacune de la CARTE, pas une
       defaillance de l agent
  E5 : critere reactiver R1-R5 -> 5/5 conforme
  E9 : verdict CONFORME avec recommandation (ajouter la case Documentation
       au parcours-vulcain)
```

### Exemple 2 : audit de verification d impact

```
Mission : Buffy corrige 15 liens casses
Audit Themis :
  E3 : detecter-impacts -> 4 fichiers NON MIS A JOUR detectes, analyses :
       citations sans version (lecons historiques, rapport date, fiche) ->
       aucun impact oublie reel
  E6 : evaluer-coherence -> 0 lien casse apres correction
  E9 : verdict CONFORME, observation hors perimetre (liens preexistants)
```

---

## Pieges courants

| Piege | Consequence | Parade |
|---|---|---|
| **Zones grises de la carte** | Des cases combos de la carte non citees dans la lecon de l agent | Les relever et verifier si elles ont ete executees (trace AGENTS-historique) avant de conclure |
| **Lacune de carte vs defaillance d execution** | Confondre un manque de la carte avec une erreur de l agent | Distinguer : si la carte ne demandait pas l etape, c est une lacune de carte a recommander |
| **Faux positifs de detecter-impacts** | Fichiers qui CITENT l outil sans version | Verifier si la mention porte une version a mettre a jour : non = pas un impact |
| **Motif parasite dans les lecons** | Un exemple de syntaxe de lien dans une lecon casse evaluer-coherence | Decrire la syntaxe en toutes lettres ou bloc fenced - verifier avec evaluer-coherence |
| **Sortie reactiver non conservee** | La sortie reelle de la commande reactiver n est pas dans un fichier | R1/R4/R5 verifiables directement (trace, bloc, profil) ; R2/R3 deduits |

---

## Liens

| Reference | Usage |
|---|---|
| [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md) | Structure des protocoles (en-tete + 7 sections) |
| [protocole-controle-buffy](../protocole-controle-buffy/) | Protocole de Janus (controle croise du travail de Buffy) |
| [spec-guider-parcours](../../../tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md) | Patterns 13/14, procedure 4i, criteres |
| [rvav-workflow](../rvav-workflow.md) | Boucle obligatoire avant verdict |
| [regles-veracite](../regles-veracite.md) | Ne jamais mentir ou inventer |
| [regles-emojis-ascii](../regles-emojis-ascii.md) | ASCII strict |
| [combo-audit-themis](../../../tools/combos/combo-audit-themis/) | Suite d audit croise (case c3 du parcours themis) |
