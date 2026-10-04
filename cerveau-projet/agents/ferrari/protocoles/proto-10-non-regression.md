# PROTOCOLE 10 -- Non-regression

> Ce protocole s'applique a CHAQUE intervention de Mecano dans freelance/.
> C'est le protocole LE PLUS CRITIQUE : il empeche les regressions.

---

## REGLE ABSOLUE

> AVANT chaque modification, je VERIFIE l'etat actuel.
> APRES chaque modification, je VERIFIE qu'aucune regression n'a ete
> introduite. Si une regression est detectee, je ROLLBACK immediatement.

---

## SOURCES DE VERITE

> **ATTENTION** : pendant la periode de dev, TOUTE source peut etre
> devenue obsolete. Je ne fais JAMAIS confiance aveuglement a un document.
> Je VERIFIE toujours contre la realite du disque.

| Source | Fiabilite | Action |
|---|---|---|
| **Fichier sur le disque** | HAUTE | C'est la realite. Toujours relire avant de modifier. |
| **Fiche d'agent** | MOYENNE | Peut etre obsolete. Verifier contre le disque. |
| **Corrections** | MOYENNE | Les lecons peuvent etre depassees. Verifier. |
| **Protocoles** | HAUTE | Mais verifier qu'ils sont a jour. |
| **Conventions** | HAUTE | Mais verifier contre les fichiers reels. |
| **USER-DEMANDES.md** | FAIBLE | Canal de communication, pas de source technique. |
| **AGENTS.md** | HAUTE | Source officielle des sessions et agents. |

---

## CHECKLIST NON-REGRESSION (AVANT modification)

1. **Lire le fichier cible** : quel est son etat ACTUEL ?
2. **Verifier les dependances** : quels autres fichiers dependent de celui que je modifie ?
3. **Verifier les tests** : y a-t-il des tests qui pinent ce fichier ?
4. **Verifier le marbre** : le fichier est-il protege ?
5. **Verifier les liens** : d'autres fichiers reference-t-ils celui que je modifie ?
6. **Photographier** : noter l'etat AVANT (hash, contenu, version)

---

## CHECKLIST NON-REGRESSION (APRES modification)

1. **Relire le fichier modifie** : est-il coherent ?
2. **Verifier les dependances** : les fichiers qui en dependent fonctionnent-ils toujours ?
3. **Verifier les tests** : lancer les tests concernes (si applicable)
4. **Verifier l'encodage** : le fichier est-il toujours dans le bon format ?
5. **Verifier les liens** : les references vers ce fichier sont-elles toujours valides ?
6. **Comparer AVANT/APRES** : la modification est-elle conforme a l'objectif ?

---

## EN CAS DE REGRESSION

| gravite | Action |
|---|---|
| **MINEURE** | Corriger immediatement, documenter dans le cahier de dev |
| **MAJEURE** | ROLLBACK complet, documenter, signaler a Cerberus |
| **CRITIQUE** | ROLLBACK + ARRETER toute activite, signaler a Cerberus + Gardien |

---

## ROLLBACK

1. **Restaurer le fichier** a son etat AVANT modification
2. **Verifier** que le rollback a reussi
3. **Documenter** la regression dans le cahier de dev
4. **Signaler** a Cerberus si la regression est majeure ou critique

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Modifier sans checklist AVANT** | Risque de regression non detectee |
| **Modifier sans verification APRES** | Risque de regression non detectee |
| **Ignorer une regression** | La regression s'aggrave avec le temps |
| **Rollback partiel** | Soit complet, soit pas de rollback |
