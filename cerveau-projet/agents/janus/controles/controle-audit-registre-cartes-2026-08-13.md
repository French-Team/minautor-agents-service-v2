# Controle croise : audit registre vs cartes

**Date** : 2026-08-13
**Verificateur** : Janus
**Verdict** : VALIDE (J1-J5 verts)

## Contexte

Demande utilisateur : verifier que tous les outils reellement utilises par
les agents sont assignes aux cartes. Themis a audite le registre des usages
(courant 21 lignes + historique 75 lignes) et produit le rapport
`themis/rapports/audit-registre-cartes-2026-08-13.md`.

## Verifications (J1-J5)

### J1 : Rapport existant et exact
- Fichier present (4416 octets), 0 non-ASCII, 0 CRLF.

### J2 : Reference morte confirmee
- `verifier-cartes-decision` : INTROUVABLE dans tools/ -> typo confirmee
  pour `valider-cartes-decision` (outil reel present).

### J3 : Echantillon des lacunes confirme
- `valider-case` : 0 occurrence dans la carte janus -> hors carte confirme.

### J4 : Cerberus - derives non re-assignees (etat voulu)
- test-034 (cerberus-sans-outils-tests) : 6 OK / 0 KO (garde-fou en vigueur).
- Carte cerberus : 0 reference a tester-lancer -> les derives historiques
  ne sont PAS re-assignees. Etat voulu confirme.

### J5 : Liste des corrections de cartes a faire

| Agent | Case | Outils a ajouter |
|---|---|---|
| janus | c4 (Verifier les tests) | valider-case, detecter-decalages-catalogue, detecter-divergences-version, generateurs-regenerer-catalogue |
| janus | registre (historique) | corriger la typo verifier-cartes-decision -> valider-cartes-decision |
| morpheus | c11/c12 | detecter-divergences-version, generateurs-regenerer-catalogue, valider-cartes-decision |
| morpheus | c12 | corriger le wildcard tester-protection-* -> tester-protections |
| vulcain | c10/c6/c12 | detecter-divergences-version, detecter-usage-scripts-temporaires, generateurs-carte, generateurs-case, generateurs-regenerer-catalogue, guider-parcours |

## Lecon Janus

L audit manuel complet (courant + historique) est plus fiable que le scan
automatique (courant seul) : la non-regression archive les declarations dans
l historique, et les derives corrigees y restent. Un audit qui ne lit que le
registre courant sous-estime les usages. Et la distinction derive-corrigee
vs lacune-reelle est decisive : corriger les unes sans re-introduire les
autres demande de lire le contexte de chaque declaration.
