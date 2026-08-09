# Test 005 -- generateurs-commande v0.2.1 + parcours-atlas v0.1.2

**Testeur** : Morpheus (testeur dedie)
**Date** : 2026-08-09
**Objet** : test formel du generateur de commande v0.2.1 (fiabilisation des flags
optionnels) et du parcours Atlas v0.1.2 (pilote strict, commandes en dur retirees)

---

## Contexte

Buffy a corrige un BUG MAJEUR dans `generateurs-commande` avant la generalisation
aux 10 autres parcours :

| Fichier | Avant | Apres |
|---|---|---|
| generateurs-commande.py | v0.2.0 (condition de retrait INVERSEE) | v0.2.1 (flags vides retires) |
| generateurs-commande.sh | v0.2.0 (logique absente) | v0.2.1 (logique portee, parite) |
| catalogue-commandes.json | v0.1.0-beta (9 flags booleens en dur) | v0.2.0 (placeholders {cle}) |
| parcours-atlas.json | v0.1.1 (24 commandes en dur) | v0.1.2 (pilote strict : 0 commande) |

**Bug corrige** : `composer_commande` retirait le flag optionnel uniquement quand
le parametre n'avait PAS de champ `flag` (condition inversee) -> les commandes
composees contenaient `--debut --fin --lignes` sans valeur -> argparse code 2.

**Flags booleens corriges** : `--inverse`, `--forcer`, `--backup`, `--unique`,
`--liste`, `--lister`, `--resume`, `--compter`, `--json` : le flag en dur du
modele est devenu un placeholder `{cle}` -> reponse `oui` = flag present,
reponse `non` = flag absent.

## Points couverts (26)

### Generateur v0.2.1
1. `--version` py = v0.2.1
2. `--version` sh = v0.2.1
3. py_compile OK
4. bash -n OK
5. `lire-fichier` (fichier=AGENTS.md;lignes=3) : SANS `--debut`/`--fin` vides, `--lignes 3` present
6. commande composee `lire-fichier` : EXECUTABLE (code 0)
7. `lire-activite-recente` (fichier;nombre=2) : SANS `--longueur` vide
8. commande composee `lire-activite-recente` : EXECUTABLE (code 0)
9. flag booleen `analyser-dependances` inverse=oui : `--inverse` PRESENT
10. flag booleen inverse=non : `--inverse` ABSENT
11. flag booleen `ecrire-fichier` backup=non : `--backup` ABSENT (py)
12. parite py/sh : commande composee identique (CRLF normalise)
13. catalogue JSON valide
14. catalogue version = 0.2.0
15. flag optionnel renseigne conserve : `lister-fichiers --extension md` PRESENT
16. non-regression : `creer-fichier` compose correctement

### Parcours Atlas v0.1.2
17. json.load valide + version 0.1.2
18. 0 champ `commande` restant dans les indices outil avec catalogue
19. navigation `OUI|explorer` : PARCOURS TERMINE
20. navigation `OUI|autre|OUI` (delegation) : PARCOURS TERMINE
21. `valider-cartes-decision --agent atlas` : CONFORME
22. case c3 : `PASSE PAR LE GENERATEUR` + `catalogue: lister-fichiers` sans commande en dur

### ASCII
23. ASCII 0 : generateurs-commande.py
24. ASCII 0 : generateurs-commande.sh
25. ASCII 0 : catalogue-commandes.json
26. ASCII 0 : parcours-atlas.json

## Protections

- Test realise dans le workspace (`RACINE` derive du chemin du test) : aucun
  fichier hors workspace, aucun fichier cree dans le projet.
- Commandes en lecture seule (lire-fichier, lire-activite-recente) : aucune
  modification de fichier.
- Fichiers temporaires : uniquement ceux de Python (`tempfile`/pycache) geres
  par le systeme.
- REGLE ABSOLUE : jamais de test sans protections.

## Verdict

**VALIDE** si 26/26 OK.
