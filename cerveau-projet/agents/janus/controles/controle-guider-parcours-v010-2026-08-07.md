# Controle -- Guide-Parcours v0.1.0 (jeu de piste) (Vulcain) 2026-08-07

**Outil concerne** : guider-parcours (v0.1.0) + parcours-vulcain.json + fiche vulcain allegee
**Mission controlee** : creation de l'outil de navigation case par case (jeu de piste anti-oubli),
parcours prototype Vulcain, fiche allegee (parcours = source de verite)
**Agent auteur** : Vulcain
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Nommage : outil `guider-parcours` (prefixe categorie `guider-`), dossier + fichiers conformes | inspection |
| 2 | 5 modeles de cases presents dans le parcours : question, indice (outil/fichier/regle), controle, fin | inspection |
| 3 | Spec coherente : format JSON, types de cases, CLI, criteres d'acceptation | inspection |
| 4 | Parcours = source de verite : fiche vulcain allegee (guidage dans le parcours, pas dans la fiche) | inspection |
| 5 | index-tools : categorie Guider ajoutee, compteur 80, liens valides | inspection |
| 6 | Test Morpheus : test-001-guider-parcours 14/14 VALIDE | execution reelle |
| 7 | Parite py/sh : memes sorties sur les memes cas | execution reelle |
| 8 | Validation : branches -> bonne case, reponse inconnue -> erreur, --case, JSON invalide refuse | execution reelle |
| 9 | Conformite ASCII des fichiers modifies | valider-conformite-ascii |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

(rempli apres le controle)

- **Verdict** : **VALIDE**
- **Points valides** : 10/10
- **Problemes detectes** : aucun (2 bugs avaient deja ete detectes et corriges par le cycle Morpheus -> Vulcain avant ce controle : nommage guide-parcours -> guider-parcours, transmission $@ dans executer_python du .sh)

## Detail des points

| # | Point | Resultat |
|---|---|---|
| 1 | Nommage guider-parcours (prefixe categorie guider-) | OK (dossier + py + sh + test conformes) |
| 2 | 5 modeles de cases + indices | OK (question 4, indice 9, controle 3, fin 4 ; indices outil 13, regle 11, fichier 4) |
| 3 | Spec coherente | OK (8 sections : objectif, format, types, CLI, exemple, criteres) |
| 4 | Parcours = source de verite (fiche allegee) | OK (section PARCOURS (SOURCE DE VERITE) dans vulcain.md, 0 mission detaillee dans la fiche) |
| 5 | index-tools : categorie Guider + compteur 80 | OK (ligne guider-parcours, Guider 1, Total 80) |
| 6 | Test Morpheus 14/14 | OK (execution reelle, VERDICT VALIDE) |
| 7 | Parite py/sh | OK (diff vide sur --liste et navigation) |
| 8 | Validations navigation | OK (branche construire c1->c9 complete, reponse inconnue detectee, --case, JSON invalide refuse par le test) |
| 9 | ASCII | OK (0 non-conforme sur 9 fichiers) |
| 10 | Traces d'outil externe | OK (0 suspect sur guider/ + vulcain.md + parcours + index-tools) |

---

## Lecons

1. Le concept du jeu de piste est operationnel : la navigation c1->c9 affiche les indices (outil/fichier/regle) au bon moment, l'agent avance une case a la fois -- reponse directe au probleme des fiches 200+ lignes
2. Le cycle MORPHEUS -> VULCAIN a fonctionne : 2 bugs detectes par les tests puis corriges par l'auteur AVANT ce controle (le second controle valide, il ne corrige pas)
3. verifier_nommage du .sh exige le prefixe de la CATEGORIE (guider-) tandis que le .py verifie le dossier de l'outil -- a verifier a chaque creation d'outil dans une categorie multi-mots
4. Un .sh avec python embarque par heredoc DOIT transmettre les arguments : python3 - "$@" << 'PYEOF' sinon le python ignore la ligne de commande
5. detecter-usage-outils-externes ne prend qu'UNE cible a la fois (pas plusieurs fichiers en arguments) -- lancer --recursive sur un dossier ou une cible seule
