# PROTOCOLE 6 -- Modifier les protocoles (freelance/)

> Ce protocole s'applique QUAND Mecano modifie un PROTOCOLE dans
> freelance/protocoles/. LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## REGLE ABSOLUE

> Les protocoles sont des INSTRUCTIONS DE COMPORTEMENT. Modifier un
> protocole = modifier la facon dont les agents freelance travaillent.
> Un protocole mal ecrit peut provoquer des erreurs en cascade.

---

## AVANT de commencer

1. **Lire le protocole cible EN ENTIER** : comprendre sa structure et son but
2. **Lire l index des protocoles** : verifier la coherence avec les autres
3. **Verifier les references** : le protocole reference-t-il d'autres fichiers ?
   Si oui, verifier que ces fichiers existent
4. **Verifier la version** : le protocole a-t-il un numero de version ?

---

## STRUCTURE TYPE d'un protocole v2

```
# PROTOCOLE N -- Titre

> Ce protocole s'applique QUAND ...
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## REGLE ABSOLUE
> ...

## AVANT de commencer
1. ...
2. ...

## ECRIRE la modification
| Element | Regle |
|---|---|

## VERIFIER apres modification
1. ...

## INTERDICTIONS
| Interdiction | Raison |
|---|---|
```

---

## ECRIRE la modification

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF |
| **Structure** | Garder la structure type (REGLE ABSOLUE, AVANT, ECRIRE, VERIFIER, INTERDICTIONS) |
| **References** | Tous les liens doivent pointer vers des fichiers existants |
| **Clarte** | Chaque instruction doit etre UNIQUEMENT comprehensible |

---

## VERIFIER apres modification

1. **Coherence** : le protocole est-il coherent avec les autres ?
2. **References** : tous les liens fonctionnent ?
3. **Clarte** : un agent qui lit ce protocole sait-il exactement quoi faire ?
4. **Version** : a-t-il ete mis a jour ?

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Supprimer un protocole existant** | Les agents en dependent |
| **Modifier le protocole-marbre** | C'est le domaine du Gardien |
| **Ajouter des regles contradictoires** | Verifier la coherence avec les autres |
| **Changer l'encodage** | UTF-8 + CRLF toujours |
