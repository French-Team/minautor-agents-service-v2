---
# Mission de controle -- parcours-atlas + fiche atlas.md
# Second controle (Buffy) -- serie jeu de piste, 11e parcours

agent:
  nom: "janus"
  type_controle: "second-controle"
  date: "2026-08-07"
  cible:
    - "cerveau-projet/agents/atlas/parcours/parcours-atlas.json"
    - "cerveau-projet/agents/atlas/atlas.md"
---

# Mission de controle -- Parcours Atlas (jeu de piste)

**Origine** : Buffy (mission terminee) -- creation du parcours Atlas (11e) + fiche allegee v0.2.0.

## Verdict attendu

1. **Case Mission** : 5 branches (explorer, web, documenter, analyser, autre)
2. **Chemin explorer** : 8 etapes completes (lister-dossiers, lister-fichiers, lister-fonctions, lister-appels, lire-fichier, rechercher-texte, valider-relecture, documenter les decouvertes) -> lecons -> FIN reactiver Cerberus
3. **Chemin web** : 3 etapes (formuler requete protocole-recherches-web, executer, documenter source) -> lecons -> FIN
4. **Chemin documenter** : 6 etapes (public cible, lister-fichiers, analyser-structure + decomposer-fichier, creer-fichier, ecrire-fichier, RVAV) -> lecons -> FIN
5. **Chemin analyser** : 5 etapes (lister-fichiers, lire-fichier, analyser-structure, analyser-dependances, creer cartographie) -> lecons -> FIN
6. **REGLE VALIDER AVANT DE MODIFIER** : x5 en indices des cases d'ecriture (signature d'Atlas)
7. **Rappel ASCII** : x6 (Pattern 2) dans les cases d'ecriture
8. **REACTIVER CERBERUS** : dans la case FIN (Atlas ne delegue pas)
9. **Navigation** : --reponses des 5 chemins -> PARCOURS TERMINE, --liste OK (32 lignes)
10. **Fiche allegee** : 0 mission detaillee, PARCOURS (SOURCE DE VERITE) present, ASCII 0 non-conforme sur les 2 fichiers

---

## RESULTAT DU CONTROLE

**VERDICT : VALIDE (10/10)**

| Point | Verification | Resultat |
|---|---|---|
| 1 | Case Mission : 5 branches | explorer c2 / web c12 / documenter c15 / analyser c21 / autre c26 | OK |
| 2 | Chemin explorer : 8 etapes | lister-dossiers -> lister-fichiers -> lister-fonctions -> lister-appels -> lire-fichier -> rechercher-texte -> valider-relecture -> documenter decouvertes -> lecons -> FIN | OK |
| 3 | Chemin web : 3 etapes + protocole | formuler requete (protocole-recherches-web) -> executer -> documenter source -> lecons -> FIN | OK |
| 4 | Chemin documenter : 6 etapes | public cible -> lister-fichiers -> analyser-structure + decomposer-fichier -> creer-fichier -> ecrire-fichier -> RVAV -> lecons -> FIN | OK |
| 5 | Chemin analyser : 5 etapes | lister-fichiers -> lire-fichier -> analyser-structure -> analyser-dependances -> creer cartographie -> lecons -> FIN | OK |
| 6 | REGLE VALIDER AVANT DE MODIFIER | 5 occurrences dans les cases d'ecriture (signature d'Atlas) | OK |
| 7 | Rappel ASCII (Pattern 2) | 6 occurrences dans les cases d'ecriture | OK |
| 8 | REACTIVER CERBERUS | present dans la case FIN c11 (Atlas ne delegue pas) | OK |
| 9 | Navigation + --liste | 5 chemins -> PARCOURS TERMINE, --liste 32 lignes | OK |
| 10 | Fiche allegee + ASCII | 0 mission detaillee, PARCOURS present, ASCII 0 non-conforme + traces 0 | OK |

**Outils utilises pour le controle** : activer-agent-principal, guider-parcours, valider-conformite-ascii, detecter-usage-outils-externes, lire-fichier
