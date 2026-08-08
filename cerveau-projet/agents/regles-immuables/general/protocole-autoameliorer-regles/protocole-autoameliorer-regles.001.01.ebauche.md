---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- Auto-Ameliorer les Regles Immuables
---

## Objectif

Permettre aux regles immuables de s'ameliorer en continu, en les adaptant aux besoins du projet.

---

## Prerequis

- Lire `regles-immuables/index-regles-immuables.md` pour connaitre les regles
- Identifier les besoins non couverts
- Lire `convention-autoamelioration.md` pour les principes

---

## Etapes

### Etape 1 -- Diagnostiquer l'etat des regles

```
1. Lire regles-immuables/index-regles-immuables.md
2. Pour chaque regle :
   a. Verifier si elle est a jour
   b. Verifier si elle est respectee
   c. Identifier les ameliorations necessaires
3. Identifier les regles manquantes
```

### Etape 2 -- Ameliorer les regles existantes

```
Pour chaque regle :
1. Analyser les retours d'utilisation
2. Identifier les ameliorations possibles
3. Appliquer les ameliorations
4. Mettre a jour la documentation
5. Valider par RVAV
```

### Etape 3 -- Creer de nouvelles regles

```
Pour chaque besoin non couvert :
1. Creer un pense-bete
2. Creer une spec
3. Creer un todo
4. Developper la regle
5. Tester la regle
6. Documenter la regle
7. Integrer la regle
```

### Etape 4 -- Archiver les regles obsoletes

```
Pour chaque regle obsolete :
1. Verifier qu'elle n'est plus utilisee
2. La deplacer dans un dossier d'archive
3. Mettre a jour la documentation
4. Signaler l'archivage
```

### Etape 5 -- Valider la coherence

```
1. Verifier que toutes les regles sont a jour
2. Verifier que la documentation est complete
3. Verifier que les regles sont coherentes
4. Valider par RVAV
```

---

## RVAV

Appliquer le cycle complet a chaque etape critique :
- [rechercher] -- verifier les impacts
- [verifier] -- confirmer la coherence
- [analyser] -- valider les consequences
- [valider] -- approuver l'amelioration

---

## Liens

- [convention-autoamelioration.md](../../../conventions/protocoles/convention-autoamelioration.md)
- [regles-immuables/index-regles-immuables.md](../../../regles-immuables/index-regles-immuables.md)

---

*Protocole conforme aux conventions du cerveau-projet*
