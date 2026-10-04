# PROTOCOLE 9 -- Harnais de securite (COMING SOON)

> Ce protocole decrit le SYSTEME DE HARNAIS qui sera mis en place
> dans la v2. Il n'est PAS ENCORE OPERATIONNEL. Ce document sert de
> SPECIFICATION pour la future implementation.

---

## QU'EST-CE QU'UN HARNAIS ?

Un harnais est un ENVELOPPE DE SECURITE qui entoure une action
sensible (edition, test, modification). Quand un agent lance un
combo via un harnais, il est GUIDE a travers une procedure securisee.

**Analogie** : le harnais est comme un equipement de protection que
le chirurgien met avant d'operer. Il isole la zone, protege les
organes sains, et donne des signaux si quelque chose tourne mal.

---

## PRINCIPE FONCTIONNEL

```
AGENT lance COMBO
    |
    v
HARNAIS s'active
    |
    +---> Phase 1 : ISOLATION
    |     - Copie le fichier cible dans une zone securisee
    |     - Verifie l'integrite (hash, backup)
    |     - Active les signaux d'alerte
    |
    +---> Phase 2 : ECRITURE
    |     - L'agent travaille dans le harnais
    |     - Chaque ecriture est LOGGEE
    |     - Les signaux surveillent les anomalies
    |
    +---> Phase 3 : VALIDATION
    |     - Verifie l'integrite du resultat
    |     - Compare avant/apres
    |     - Demande confirmation si anomalie
    |
    +---> Phase 4 : APPLICATION
          - Applique le changement au fichier reel
          - Met a jour l'historique
          - Libere le harnais
```

---

## TYPES DE HARNAIS + COMBOS

> Les combos sont definis dans [combos-harnais.json](combos-harnais.json).
> Chaque combo correspond a un harnais et contient les etapes exactes.

| Harnais | Combo | Usage | Protections |
|---|---|---|---|
| **harnais-test** | combo-harnais-test | Ecrire et lancer des tests | Isolation, signaux d'echec, rollback auto |
| **harnais-edition** | combo-harnais-edition | Editer des fichiers sensibles | Backup, comparaison avant/apres, confirmation |
| **harnais-modification** | combo-harnais-modification | Modifier des outils/protocoles | Validation syntaxique, non-regression |
| **harnais-creation** | combo-harnais-creation | Creer de nouveaux fichiers | Template, validation structure, nommage |

---

## COMBOS AVEC HARNAIS

> Les combos sont definis en JSON dans [combos-harnais.json](combos-harnais.json).
> Chaque combo contient : phases, etapes, signaux, rollback.
> Mecano lit le combo AVANT de commencer et le suit etape par etape.

---

## SIGNAUX DU HARNAIS

| Signal | Signification | Action |
|---|---|---|
| **SIG OK** | Tout va bien | Continuer |
| **SIG WARN** | Anomalie mineure | Alerter, continuer |
| **SIG ERR** | Erreur detectee | Stopper, rollback |
| **SIG CRIT** | Probleme critique | Stopper immEDIATEMENT, tout restaurer |

---

## AVANTAGES

| Avantage | Description |
|---|---|
| **Isolation** | L'agent travaille dans un espace securise |
| **Rollback** | Si echec, tout est restaure |
| **Tracabilite** | Chaque action est loggee |
| **Validation** | Chaque modification est verifyee |
| **Confirmation** | L'utilisateur valide avant application |

---

## IMPLEMENTATION FUTURE

| Phase | Action |
|---|---|
| **Phase 1** | Creer la structure de base (harnais-test) |
| **Phase 2** | Ajouter harnais-edition |
| **Phase 3** | Integrer les combos |
| **Phase 4** | Ajouter les signaux et alertes |

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Travailler sans harnais** | Toute action sensible doit passer par un harnais |
| **Desactiver les signaux** | Les signaux sont la pour proteger |
| **Rollback manuel** | Le rollback est automatique |
| **Ignorer un SIG ERR** | Arreter et diagnostiquer |
