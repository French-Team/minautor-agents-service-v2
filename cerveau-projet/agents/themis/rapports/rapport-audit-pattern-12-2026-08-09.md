# Rapport d'audit -- Pattern 12 CREATION LIMITEE (procedure 4j)

**Date** : 2026-08-09
**Evaluatrice** : Themis (procedure 4j, spec-guider-parcours v0.2.22)
**Objet** : verifier que le Pattern 12 (CREATION LIMITEE, garde-fou une carte = un role) est applique dans les 11 parcours -- toutes les cases de creation portent-elles l'indice regle ?
**Question utilisateur** : toutes les cases de creation portent-elles l'indice regle CREATION LIMITEE ?

---

## 1. Procedure appliquee (4j de la spec v0.2.22)

1. Identifier les cases de creation/documentation (indices avec creer-fichier, ecrire-fichier, editer-fichier, ajouter-contenu-fichier OU titre evoquant creation/redaction/documentation)
2. Verifier la presence d'un indice `regle` CREATION LIMITEE en tete des indices (perimetre + roles exclus)
3. Verifier qu'aucune case ne demande de creer un outil/test/case soi-meme
4. Verifier que la case `Signaler le besoin` ne contient PAS la mention "documenter une nouvelle case dans le parcours"

---

## 2. VERDICT GLOBAL : NON CONFORME (1/11 parcours conforme)

Le Pattern 12 vient d'etre documente dans la spec (v0.2.22, mission Promethee du jour). **Seul le parcours pilote atlas v0.1.3 est conforme** (corrige par Buffy apres l'incident du jour). Les **10 autres parcours** presentent des ecarts : cases de creation SANS l'indice regle CREATION LIMITEE complet (perimetre + roles exclus) et/ou case Signaler le besoin avec la mention fautive.

Note d'equite : ce resultat est ATTENDU -- le Pattern 12 a ete formalise aujourd'hui ; les autres parcours ne l'ont pas encore integre. L'audit sert de liste de travail pour la generalisation (lecon : un nouveau pattern s'applique d'abord en pilote, puis se generalise).

---

## 3. Tableau parcours par parcours

| Parcours (version) | Cases de creation identifiees | Garde-fou CREATION LIMITEE | Case Signaler (mention fautive) | Conformite |
|---|---|---|---|---|
| atlas (v0.1.3) | c9, c18, c19, c25 (+ c10 lecons) | OUI en tete (c9/c18/c19/c25) | c29 corrigee : signaler a Cerberus (outil -> Vulcain, test -> Morpheus, case -> Buffy), je ne cree rien | CONFORME |
| athena (v0.1.1) | c4 (squelette), c9 (lecons) | NON (REGLE IMMUABLE ASCII en tete) | c20 : OUI fautive | ECART |
| buffy (v0.2.3) | c5, c7, c11, c15, c20, c25 | NON (REGLE WORKSPACE en tete) | c35 : OUI fautive | ECART |
| cerberus (v0.2.2) | AUCUNE | NA | c23 : OUI fautive | ECART (point 4) |
| clio (v0.1.1) | c8 (editer-fichier) | NON (REGLE IMMUABLE ASCII en tete) | c15 : OUI fautive | ECART |
| janus (v0.2.1) | c2, c11, c18 (creer-fichier), c3 (lecture) | NON (REGLE WORKSPACE en tete) | c29 : OUI fautive | ECART |
| minerve (v0.1.1) | c4 (squelette), c8 (index-todo), c9 (lecons) | NON (REGLE WORKSPACE/ASCII en tete) | c20 : OUI fautive | ECART |
| morpheus (v0.1.2) | c8 (lecons) | NON (REGLE WORKSPACE en tete) | c16 : OUI fautive | ECART |
| promethee (v0.1.1) | c4 (squelette), c8 (index-spec), c9 (lecons) | NON (REGLE WORKSPACE/ASCII en tete) | c20 : OUI fautive | ECART |
| themis (v0.2.1) | c9 (rapport), c12 (lecons) | NON (REGLE WORKSPACE/ASCII en tete) | c23 : OUI fautive | ECART |
| vulcain (v0.2.4) | c12 (modifier l'outil) | NON (REGLE WORKSPACE en tete) | c18 : OUI fautive | ECART |

**Total cases de creation** : 25 cases identifiees (atlas 4 conformes ; 21 cases sans garde-fou complet).
**Cases Signaler fautives** : 10 (toutes sauf atlas c29).

---

## 4. Liste des ecarts (parcours | case | probleme)

### Ecart A -- Case de creation SANS indice regle CREATION LIMITEE (point 2)
Les cases suivantes utilisent un outil de creation/ecriture (creer-fichier, ecrire-fichier, editer-fichier, ajouter-contenu-fichier) mais portent en tete une REGLE WORKSPACE ou REGLE IMMUABLE ASCII (garde-fou partiel : perimetre workspace, mais SANS les roles exclus outil -> Vulcain, test -> Morpheus, case -> Buffy ni le renvoi vers la case Signaler) :

| Parcours | Cases | Outil |
|---|---|---|
| athena | c9 | ajouter-contenu-fichier (lecons) |
| buffy | c5, c7, c11, c15, c20, c25 | creer-fichier, editer-fichier, ajouter-contenu-fichier, copier-fichier |
| clio | c8 | editer-fichier (index) |
| janus | c2, c11, c18 | creer-fichier (missions de controle) |
| minerve | c8, c9 | editer-fichier (index-todo), ajouter-contenu-fichier (lecons) |
| morpheus | c8 | ajouter-contenu-fichier (lecons) |
| promethee | c8, c9 | editer-fichier (index-spec), ajouter-contenu-fichier (lecons) |
| themis | c9, c12 | creer-fichier (rapport), ajouter-contenu-fichier (lecons) |
| vulcain | c12 | editer-fichier (modifier l'outil) |

### Ecart B -- Case Signaler le besoin avec mention fautive (point 4)
Les cases suivantes contiennent "documenter une nouvelle case dans le parcours" (creation de case = role de Buffy, l'agent audite ne doit jamais creer sa propre case) :

| Parcours | Case |
|---|---|
| athena | c20 |
| buffy | c35 |
| cerberus | c23 |
| clio | c15 |
| janus | c29 |
| minerve | c20 |
| morpheus | c16 |
| promethee | c20 |
| themis | c23 |
| vulcain | c18 |

---

## 5. Points conformes

- **Point 3** : AUCUNE case (hors cases Signaler) ne demande a l'agent de creer un outil, un test ou une case de parcours lui-meme -- recherche negative sur les mentions "creer un outil", "ecrire un test", "creer une case", "nouvelle case" dans les messages/indices : 0 resultat hors cases Signaler
- **Atlas v0.1.3** : modele de reference complet (garde-fou en tete des 4 cases de creation + case Signaler corrigee) -- a dupliquer
- **Base existante** : 9 parcours portent deja une REGLE WORKSPACE ou REGLE IMMUABLE ASCII en tete de leurs cases de creation -- le Pattern 12 est une EXTENSION de ces regles (ajout des roles exclus), pas un changement de fond

---

## 6. Recommandations

1. **Generaliser le Pattern 12** : activer Buffy (concepteur des parcours) pour ajouter l'indice regle CREATION LIMITEE en tete des 21 cases de creation identifiees (tableau Ecart A), sur le modele exact d'atlas c9/c18/c19/c25 (perimetre du role + roles exclus + renvoi Signaler)
2. **Corriger les 10 cases Signaler** : remplacer "documenter une nouvelle case dans le parcours" par "signaler a Cerberus (outil -> Vulcain, test -> Morpheus, nouvelle case -> Buffy), je ne cree rien moi-meme" -- modele atlas c29
3. **Re-audit 4j** apres correction : relancer cette meme procedure (script de scan reutilisable : detecter les cases de creation + verifier la mention fautive) pour confirmer 11/11 CONFORME
4. **Parcours cerberus** : n'a aucune case de creation (point 2 NA) mais doit corriger sa case c23 (Ecart B) -- le garde-fou ne concerne pas ses actions (il active uniquement) mais sa case Signaler reste fautive
5. **Vulcain c12** : cas particulier a traiter avec soin -- modifier l'outil est SON role (le perimetre du garde-fou doit l'autoriser : outils = role Vulcain, mais interdire tests et cases)

---

## 7. Traces

- Spec source : cerveau-projet/agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md (v0.2.22, section ### 4j. Pattern 12)
- 11 parcours scannes : cerveau-projet/agents/*/parcours/parcours-*.json
- Methode : scan JSON (outils de creation dans indices + titre evocateur) + verification croisee de la mention fautive
- Outils utilises : lire-fichier, lister-fichiers, valider-conformite-ascii, detecter-usage-outils-externes
