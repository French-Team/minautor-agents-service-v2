# PROTOCOLE 7 -- Modifier les regles-immuables (freelance/)

> Ce protocole s'applique QUAND Mecano modifie les regles dans
> freelance/regles/ ou freelance/regles-immuables/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## REGLE ABSOLUE

> Les regles-immuables sont des CONTRAINTES QUI NE CHANGENT PAS.
> Modifier une regle immmuable = changer les fondations du systeme.
> Toute modification doit etre JUSTIFIEE et DOCUMENTEE.

---

## AVANT de commencer

1. **Lire la regle cible EN ENTIER** : comprendre pourquoi elle existe
2. **Verifier si la regle est dans le marbre** :
   - OUI -> JE NE MODIFIE PAS (c'est le domaine du Gardien)
   - NON -> je peux la modifier avec justification
3. **Lire les regles liees** : verifier la coherence avec les autres regles
4. **Verifier la version** : la regle a-t-elle un numero de version ?

---

## ECRIRE la modification

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF |
| **Justification** | Chaque modification doit etre justifiee |
| **Coherence** | La regle doit etre coherence avec toutes les autres |
| **Version** | Bumper la version si modification structurelle |

---

## VERIFIER apres modification

1. **Coherence** : la regle est-elle coherence avec les autres ?
2. **Marbre** : la regle n'est-elle PAS dans le marbre ?
3. **Impact** : quel est l'impact de cette modification sur les agents ?
4. **Version** : la version a-t-elle ete bumpree ?

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Modifier une regle du marbre** | C'est le domaine du Gardien - SEUL habilite |
| **Supprimer une regle immmuable** | Les regles sont la pour rester |
| **Modifier sans justification** | Chaque changement doit etre documente |
| **Changer l'encodage** | UTF-8 + CRLF toujours |
