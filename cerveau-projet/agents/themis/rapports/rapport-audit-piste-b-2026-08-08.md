# Rapport d'audit -- Piste B : indices PASSE PAR LE GENERATEUR

**Date** : 2026-08-08
**Auditrice** : Themis (evaluatrice croisee)
**Contexte** : la piste B (indices generateurs-commande dans les 11 parcours) avait ete perdue par un git checkout de restauration pendant la piste C volet 2. Buffy l a reparse a l identique (trace AGENTS-historique lignes 21-22). Audit de conformite demande par l utilisateur (REPARER PUIS AUDITER).

## Verdict global : CONFORME

## Criteres d'audit

| # | Critere | Resultat |
|---|---|---|
| C1 | Exactement 1 regle PASSE PAR LE GENERATEUR + 1 indice outil generateurs-commande (avec catalogue: generateurs-commande) par parcours | CONFORME -- 11/11 (1+1 par parcours) |
| C2 | Indice en TETE des indices de la case la plus pertinente (celle qui lance une suite d outils) | CONFORME -- regle pos=0, indice pos=1 dans les 11 parcours |
| C3 | Commande d exemple cite un NOM VALIDE du catalogue et CIBLEE sur l outil de la case | CONFORME -- tous les --commande cites existent au catalogue (ex: generateurs-squelette-pense-bete, verifier-systeme, evaluer-structure, analyser-structure, activer-agent-principal, creer-fichier, valider-nommage, mettre-a-jour-readme, valider-ebauche, generateurs-squelette-todo, generateurs-squelette-spec) |
| C4 | Pattern 9 intact : LIRE AVANT USAGE affiche pour l indice generateurs-commande | CONFORME -- verifie sur athena c4 et themis c16 : catalogue + PASSE PAR LE GENERATEUR + LIRE AVANT USAGE (generateurs-commande.md) |
| C5 | Navigation --reponses PARCOURS TERMINE 11/11 avec affichage de l indice | CONFORME -- 11/11 PARCOURS TERMINE |
| C6 | json.load 11/11, ASCII 0/11, valider-cartes --tous 11/11 CONFORME | CONFORME -- json OK, ASCII 0, valider-cartes 11/11 |
| C7 | Piste C intacte (champs catalogue) | CONFORME -- 188 champs = 177 (piste C) + 11 (piste B, chacun avec catalogue: generateurs-commande), aucune suppression |

## Tableau par agent

| Agent | Regle | Indice | Position | Commande exemple | Catalogue |
|---|---|---|---|---|---|
| athena | 1 | 1 | tete (0/1) | generateurs-squelette-pense-bete | OK |
| atlas | 1 | 1 | tete (0/1) | analyser-structure | OK |
| buffy | 1 | 1 | tete (0/1) | valider-nommage | OK |
| cerberus | 1 | 1 | tete (0/1) | activer-agent-principal | OK |
| clio | 1 | 1 | tete (0/1) | mettre-a-jour-readme | OK |
| janus | 1 | 1 | tete (0/1) | valider-ebauche | OK |
| minerve | 1 | 1 | tete (0/1) | generateurs-squelette-todo | OK |
| morpheus | 1 | 1 | tete (0/1) | creer-fichier | OK |
| promethee | 1 | 1 | tete (0/1) | generateurs-squelette-spec | OK |
| themis | 1 | 1 | tete (0/1) | evaluer-structure | OK |
| vulcain | 1 | 1 | tete (0/1) | verifier-systeme | OK |

## Verifications independantes realisees (aucune confiance dans les validations Buffy)

1. Comptage + position via script de croisement sur les 11 fichiers JSON
2. Verification des noms --commande contre le catalogue (json.load catalogue)
3. Navigation reelle guider-parcours --reponses (11 chemins connus)
4. Affichage controle : guider-parcours sur athena + themis (grep catalogue + LIRE AVANT USAGE)
5. valider-conformite-ascii 11 fichiers
6. valider-cartes-decision --tous

## Lecons

1. La reparation a l identique est validee : la trace AGENTS-historique (lignes 21-22) + la lecon Buffy (corrections lignes 513-524) ont permis de reconstruire la piste B sans ecart.
2. Le champ catalogue (v0.2.20) est bien porte par les 11 indices generateurs-commande : 188 champs au total (177 piste C + 11 piste B) -- coherence parfaite, pas de doublon.
3. L ajustement morpheus (c4 creer-fichier au lieu de c6 tester-protection-*) est CONFORME : le pseudo-outil tester-protection-* n a pas d entree catalogue exploitable, la commande d exemple doit citer un nom executable.
4. Aucun ecart detecte : la piste B reparee est conforme a la spec (Pattern 3 generateur + Pattern 9 LIRE AVANT USAGE) et cohabite avec la piste C.
