---
identite:
  type: combo
  appartient_a: commun
  commun: true
---
# combo-nettoyage-hygie

**Version :** 0.1.1
**Statut :** ebauche
**Categorie :** combos
**Chemin :** `agents/tools/combos/combo-nettoyage-hygie/`
**Proprietaire :** Hygie (outil partage)

---

## Objectif

Cycle de nettoyage de Hygie, encapsule en un combo (Pattern 3) :

1. **Snapshot** (`snapshot-nettoyage creer`) : preuve de tracabilite de
   l etat du workspace AVANT toute suppression
2. **Detection FICHIERS** (`detecter-residus --zone tous --detail`) : scan
   compartimente par zone (cerveau-projet / workspace)
3. **Detection PROCESSUS** (`detecter-processus-residuels --detail`) : scan
   des processus orphelins (parent mort) ou referencant le projet
4. **Verdict** : workspace propre OU residus a supprimer

La suppression reste executee par **Hygie** (seul agent habilite a supprimer
sans demande prealable) : `supprimer-fichier` / `supprimer-dossier` pour les
fichiers, `nettoyer-processus-residuels` (exclusif Hygie) pour les processus,
puis rapport et rotation 7 jours des snapshots.

---

## Utilisation

```bash
python3 combos-moteur.py cerveau-projet/agents/tools/combos/combo-nettoyage-hygie/definition-combo.json
```

---

## Deroulement

| Case | Action |
|---|---|
| c1-c2 | Generer + executer `snapshot-nettoyage creer` (preuve) |
| c3-c4 | Generer + executer `detecter-residus --zone tous --detail` |
| c4b-c4c | Generer + executer `detecter-processus-residuels --detail` |
| c5 | Controle : des residus detectes (fichiers OU processus) ? |
| c6 | FIN : Hygie supprime les fichiers (supprimer-fichier/dossier) + termine les processus (nettoyer-processus-residuels), verifie la disparition, redige le rapport, rotation 7 jours |
| c7 | FIN : workspace propre |

---

## Dependances

- `snapshot-nettoyage` (nettoyer/)
- `detecter-residus` (detecter/)
- `detecter-processus-residuels` (detecter/)
- `nettoyer-processus-residuels` (nettoyer/, exclusif Hygie)
- `combos-moteur` (combos/)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-13 | Creation initiale (mission Hygie, demande utilisateur) |

---
