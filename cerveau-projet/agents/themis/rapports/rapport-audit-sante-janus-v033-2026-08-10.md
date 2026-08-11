# Rapport d'audit -- Protocole sante E5 (fiche janus vs parcours v0.3.3)

- **Date** : 2026-08-10
- **Auditrice** : Themis
- **Contexte** : etape 3 de la verification complete du parcours janus allege (c8/c11/c18 -> v0.3.3, Pattern 16). Audit documentaire du protocole sante-fichiers-agents E5 (E5a/E5b/E5c + Pattern 14).
- **Objet** : cerveau-projet/agents/janus/janus.md vs cerveau-projet/agents/janus/parcours/parcours-janus.json (v0.3.3)

---

## Verdict : A REVOIR (2 points) -> VALIDE (corrige le 2026-08-10, re-audit 10/10)

| Critere | Statut | Detail |
|---|---|---|
| E5a (formule fin-suit-SA-carte) | OK -> OK | Ligne 190 : "La fin de mission suit SA carte (Pattern 13)" (numerotation alignee) |
| E5b (croisement fiche/parcours) | KO -> **OK** | Corrige : bloc FINS REELLES cX ajoute (c10/c29/c29d/c30/c32) - re-audit 10/10 |
| E5c (sens des fins) | OK | Ligne 191 : "Je suis le DERNIER maillon... je reactiver Cerberus avec le BILAN CONSOLIDE" + ligne 212 |
| Pattern 14 (version dans la fiche) | KO -> **OK** | Corrige : ligne 76 `PARCOURS (v0.3.3)` - re-audit 10/10 |

---

## Point 1 -- Pattern 14 : version divergente

- **Fichier** : cerveau-projet/agents/janus/janus.md, ligne 76
- **Constats** :
  - Fiche : `> **REGLE ABSOLUE -- PARCOURS (v0.3.2)**`
  - Carte reelle : `version: 0.3.3`
- **Correction attendue** : mettre a jour la fiche vers `PARCOURS (v0.3.3)`.
- **Gravite** : legere (version obsolete) mais regle du protocole sante E5 (Pattern 14) violee.

## Point 2 -- E5b : aucune fin citee avec identifiant cX reel

- **Fichier** : cerveau-projet/agents/janus/janus.md
- **Constats** : les fins reelles de la carte v0.3.3 sont :
  - `c10` | FIN - Reactiver Cerberus
  - `c29` | Signaler le besoin (fin - relais)
  - `c29d` | FIN - Outil temporaire
  - `c30` | FIN - Delegation
  - `c32` | FIN - Retour de Themis avec son rapport
  - La fiche en formule le SENS (reactiver Cerberus, dernier maillon) mais ne cite AUCUN identifiant cX.
- **Lecon du re-audit** (protocole sante v0.1.1, E5b) : "Une mention textuelle sans identifiant reel est INSUFFISANTE".
- **Correction attendue** : enrichir la section fin de la fiche pour citer les fins reelles avec leurs identifiants cX (ex : `c10 FIN - Reactiver Cerberus`) en coherence avec la carte v0.3.3.

---

## Points conformes

- E5a : la regle fin-suit-SA-carte est formulee (meme si numerotee Pattern 8 dans la fiche - recommandation : aligner la numerotation sur la spec-guider-parcours actuelle qui parle de Pattern 13).
- E5c : le sens est correct (janus = dernier maillon des chaines outil -> tests -> controle, reactiver Cerberus).
- valider-cartes-decision --agent janus : CONFORME (re-confirme en etape 3).
- Non-regression : test-019 11/11, test-009 20/20 (temoin artificiel).

---

## Recommandations

1. **Correction par Buffy** (responsable des fichiers du cerveau) : mettre a jour ligne 76 vers v0.3.3 + citer les fins cX reelles dans la fiche janus.
2. **Alignement de numerotation** : la fiche cite "Pattern 8" la ou la spec parle de "Pattern 13" - harmoniser (a traiter lors d'une prochaine passe sante, hors perimetre immediat).
3. Apres correction, re-auditer E5b (le croisement doit passer de KO a OK).
