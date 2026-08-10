# Rapport d'audit -- POURQUOI LES CASES INDIUISENT ENCORE LES AGENTS EN ERREUR (reactiver/activer)

**Date** : 2026-08-10
**Auditrice** : Themis (evaluatrice croisee)
**Contexte** : l utilisateur a signale que la philosophie a change (l agent
ACTIVE l agent suivant dans SA carte, sans repasser par Cerberus entre les
maillons - Pattern 13), mais des cases et mentions induisent encore les agents
en erreur. Incident declencheur : dans la chaine testee en reel, Themis et
Morpheus ont utilise la commande reactiver qui les a ramenes DIRECTEMENT a
Cerberus au lieu de revenir a l agent precedent.

---

## Contexte

- Incident : reactiver de Themis et de Morpheus -> Cerberus (au lieu de
  l agent precedent)
- Scan : 11 parcours + protocoles + 11 fiches
- Question : pourquoi les agents sont-ils encore induits en erreur malgre le
  changement de philosophie ?

---

## Resultats

### 1. L outil : reactiver ramene TOUJOURS a Cerberus

| Fait | Detail |
|---|---|
| Fonction | `reactiver_cerberus(session, raison, agent_precedent)` (ligne 637) |
| Aide | `reactiver <session> <raison> <agent_precedent> - Reactiver Cerberus dans sa session` |
| Conclusion | La commande reactiver NE PEUT PAS ramener a un agent autre que Cerberus - c est sa conception |

### 2. Les 2 cases FAUSSES qui induisent en erreur (cause directe)

| Parcours | Case | Titre | Probleme |
|---|---|---|---|
| atlas | c31b | FIN - Reactiver l agent precedent avec sa carte | La case donne la commande `reactiver session-llm-1 <raison> <agent_precedent>` qui ramene a CERBERUS, pas a l agent precedent |
| themis | c25b | FIN - Reactiver l agent precedent avec son rapport | Idem : la commande reactiver ramene a Cerberus |

**La bonne commande pour revenir a l agent precedent est `activer <session> <agent_precedent> <raison>`** (l action activer accepte n importe quel agent).

### 3. Les 37 fins mentionnant Cerberus : verdict

| Verdict | Nombre | Detail |
|---|---|---|
| CONFORME | ~30 | Fins legitimes : "FIN - Reactiver Cerberus" (quand active par Cerberus directement), "Signaler le besoin a Cerberus", "FIN - Delegation (ou reactive Cerberus si active directement par lui)" |
| A CORRIGER | 2 | atlas c31b + themis c25b : donnent la MAUVAISE commande (reactiver au lieu d activer) pour revenir a l agent precedent |
| A VERIFIER | ~5 | Les fins "FIN - Activer Janus" (buffy c8/c22/c27, morpheus c10, vulcain c9/c15) : le message dit "Janus controle puis REACTIVE Cerberus" - correct seulement si Janus a ete active par Cerberus |

### 4. Le protocole-activation : cycle obsolete

| Element | Etat | Probleme |
|---|---|---|
| Cycle (etape 6) | `REACTIVER -> Cerberus` | Decrit uniquement le retour a Cerberus, pas les maillons de chaine |
| Pattern 13 (spec) | `activation directe = reactiver Cerberus, maillon de chaine = activer le suivant, dernier maillon = reactiver Cerberus avec bilan` | La regle existe dans la spec mais n est PAS propagee dans le protocole-activation |

### 5. La regle de decision (ce qui manque)

| Situation | Action correcte | Commande |
|---|---|---|
| J ai ete active par Cerberus directement | Fin : reactiver Cerberus | `reactiver <session> <raison> <agent>` |
| J ai ete active par un agent (maillon de chaine) | Fin : activer l agent suivant OU revenir a l agent precedent | `activer <session> <agent> <raison>` |
| Je suis le dernier maillon de la chaine | Fin : reactiver Cerberus avec bilan consolide | `reactiver <session> <raison> <agent>` |

---

## Synthese

**Pourquoi les agents sont encore induits en erreur ?**

1. **La commande reactiver est ambigue** : elle s appelle reactiver mais ne
   ramene QU a Cerberus. Les cartes qui disent "reactiver l agent precedent"
   donnent la commande reactiver - c est une INCOHERENCE directe entre le
   texte (reactiver l agent precedent) et la commande (reactiver Cerberus).

2. **La regle Pattern 13 n est pas propagee** : elle est documentee dans la
   spec-guider-parcours mais le protocole-activation (source de verite de
   l activation) decrit encore le cycle simple CERBERUS -> AGENT -> CERBERUS
   sans les maillons de chaine.

3. **Les cartes de fin n ont pas la regle de decision** : une fin devrait
   porter la condition (qui m a active ?) pour choisir entre reactiver et
   activer.

## Recommandations

| # | Recommandation | Cible | Priorite |
|---|---|---|---|
| 1 | CORRIGER les 2 cases fausses : atlas c31b et themis c25b - remplacer la commande reactiver par `activer <session> <agent_precedent> <raison>` et reformuler "REACTIVE L AGENT PRECEDENT" en "ACTIVE L AGENT PRECEDENT (maillon de chaine)" | atlas, themis (Buffy) | HAUTE |
| 2 | METTRE A JOUR protocole-activation : integrer le Pattern 13 (3 cas : active par Cerberus / maillon de chaine / dernier maillon) avec la regle de decision et les commandes exactes | protocole-activation (Buffy) | HAUTE |
| 3 | AJOUTER la regle de decision dans les fins de parcours : chaque fin "Reactiver Cerberus" doit preciser "si j ai ete active par Cerberus" et chaque fin de maillon de chaine doit preciser "activer <agent>" | 11 parcours (Buffy) | MOYENNE |
| 4 | VERIFIER les fiches agents (section UTILISATION / Pour terminer ma mission) : les 11 fiches mentionnent "reactiver Cerberus" - ajouter la distinction selon le mode d activation | 11 fiches (Buffy) | MOYENNE |
| 5 | DOCUMENTER la lecon : la commande reactiver ramene TOUJOURS a Cerberus (conception) - pour revenir a un agent precedent, utiliser activer <agent> | corrections agents | BASSE |

---

## Annexe : inventaire complet des 37 fins mentionnant Cerberus

Voir le scan dans l historique : athena (c10/c20/c21), atlas (c11/c28/c29),
buffy (c13d/c22/c27/c35/c36/c8), cerberus (c20), clio (c12/c15/c16), janus
(c10/c29/c30), minerve (c10/c20/c21), morpheus (c10/c14/c16/c17), promethee
(c10/c20/c21), themis (c13/c23/c24/c8d), vulcain (c15/c16d/c18/c19/c9).
Seules 2 sont fausses (atlas c31b, themis c25b) - le reste est conforme ou a
verifier selon le mode d activation.
