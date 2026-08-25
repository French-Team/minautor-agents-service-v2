# PROTOCOLE 11 -- Reordonnancement des fichiers par importance

> Ce protocole s'applique a CHAQUE fois qu'un fichier est modifie
> dans freelance/. APRES modification, verifier l'ordre des elements
> et reordonner si necessaire.

---

## REGLE ABSOLUE

> **DEBUT + FIN = ZONE D'IMPACT MAXIMUM**
> Un LLM lit le DEBUT et la FIN d'un fichier. Le MILIEU est moins lu.
> Les regles importantes doivent etre au DEBUT ou a la FIN, jamais au milieu.

---

## PRINCIPE

```
DEBUT DU FICHIER (10-20% du contenu)
  -> Ce qui est LE PLUS IMPORTANT
  -> Regles absolues
  -> Informations critiques

MILIEU DU FICHIER (60-80% du contenu)
  -> Detail, examples, documentation
  -> Moins critique

FIN DU FICHIER (10-20% du contenu)
  -> Ce qui doit etre RETENU
  -> Interdictions
  -> Lecon finale
```

---

## ORDRE DE PRIORITE (debut du fichier)

| Priorite | Contenu | Position |
|---|---|---|
| **1 - CRITIQUE** | Regles absolues, interdictions | DEBUT (lignes 1-50) |
| **2 - IMPORTANT** | Perimetre, mode d'emploi | DEBUT (lignes 50-100) |
| **3 - UTILE** | Details, exemples | MILIEU |
| **4 - REFERENCE** | Tables, annexes | MILIEU-FIN |
| **5 - RETENIR** | Philosophie, citations | FIN |

---

## CHECKLIST REORDONNANCEMENT (APRES chaque modification)

1. **Lire le fichier modifie EN ENTIER**
2. **Identifier les regles importantes** : sont-elles au debut ?
3. **Identifier les elements critiques** : sont-ils au debut ou a la fin ?
4. **Verifier le milieu** : y a-t-il des regles importantes enfouies ?
5. **Si oui** : deplacer les regles importantes vers le debut ou la fin
6. **Verifier la coherence** : l'ordre est-il logique apres reordonnancement ?

---

## EXEMPLE AVANT / APRES

### AVANT (desordonne)
```markdown
# Titre
## Exemples (pas important)
... 50 lignes d'exemples ...
## Regle ABSOLUE (IMPORTANT, mais au milieu !)
... une regle critique ...
## Details
... 100 lignes de details ...
## Philosophie
```

### APRES (reordonne)
```markdown
# Titre
## Regle ABSOLUE (DEBUT - priorite 1)
## Perimetre (DEBUT - priorite 2)
## Mode d'emploi
## Exemples (MILIEU - priorite 3)
## Details (MILIEU - priorite 3)
## Philosophie (FIN - priorite 5)
## Interdictions (FIN - priorite 5)
```

---

## CAS SPECIFIQUES

| Type de fichier | Debut du fichier | Fin du fichier |
|---|---|---|
| **Fiche agent** | Vue d'ensemble, role, regles absolues | Citation, limites |
| **Corrections** | Contexte, regles specifiques | Lecons |
| **Protocole** | Regle absolue, quand l'utiliser | Interdictions |
| **Conventions** | Regles critiques, format | Exemples |
| **Arbre JSON** | Regles (D1, D5, D6, D3) | Fins centralisees |

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Mettre des exemples au debut** | Les exemples ne sont pas des regles |
| **Enfouir des regles absolues** | Elles doivent etre au debut |
| **Mettre des interdictions au milieu** | Elles doivent etre a la fin |
| **Garder un fichier desordonne** | Chaque modification = reordonnancement |
