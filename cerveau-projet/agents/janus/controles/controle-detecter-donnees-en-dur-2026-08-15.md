# Controle croise -- detecter-donnees-en-dur v0.1.0

**Date** : 2026-08-15
**Controleur** : Janus (chaine Cerberus -> Vulcain -> Morpheus -> Janus)
**Verdict** : VALIDE (55 OK / 0 KO non-regression)

## J1. test-007 (catalogue + index adaptes)
- Catalogue 155 -> 156, index-tools 173 -> 174, entree detecter-donnees-en-dur dans les 2 listes de presence
- Resultat : 15/15 VALIDE

## J2. test-028 (coherence documentaire)
- Resultat : 8/8 OK

## J3. valider-cartes-decision --tous
- Resultat : 13/13 CONFORMES

## J4. detecter-divergences-version
- Resultat : 23 ALIGNEES, 0 DIVERGENTE

## J5. Normes (fichiers modifies par la chaine)
- test-007, detecter-donnees-en-dur.py : 0 non-ASCII / 0 CRLF

## J6. Non-regression complete (SEUL Janus habile)
- 1er run : 53 OK / 2 KO -> corrections (ci-dessous)
- Run final : 55 OK / 0 KO

## Corrections effectuees par Janus en controle
1. **test-024** : figeait aussi le total catalogue a 155 -> 156 + libelles (16/16 OK)
2. **test-035 (OUTIL_HORS_CARTE x2)** :
   - morpheus : indice executer-script-temporaire ajoute a c16c (usage reel entonnoir) -> parcours 0.4.6 -> 0.4.7, fiche mise a jour, test-004 adapte (16/16)
   - vulcain : indice detecter-donnees-en-dur ajoute a c10 (usage reel creation) -> parcours 0.4.16 -> 0.4.17, fiche (2 mentions) mise a jour

## Signal documente (pas un KO)
- RALENTISSEMENT : 50.1 s vs reference 39.8 s (+26%) - la reference ne se rebase que sur un temps meilleur (regle utilisateur). Decision utilisateur : rebase ou mission d optimisation.

## Livrables de la chaine
- Outil detecter-donnees-en-dur v0.1.0 (py + md) : 5 types de donnees en dur detectes (nombres magiques, chemins, URLs, versions, compteurs) + recommandation du meilleur format de stockage
- Catalogue generateurs-commande : 156 commandes
- index-tools : 174 outils
- test-007 et test-024 adaptes ; test-004 adapte
- Lecons : vulcain, morpheus, janus
