# Outil — Vérifier la Surcharge des Fichiers

**Catégorie** : Valider
**Version** : 0.1.0
**Statut** : stable
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Détecter les fichiers qui dépassent un seuil de taille (nombre de lignes).

**Pourquoi cet outil ?**
- Les fichiers trop gros sont difficiles à lire et à maintenir
- Un seuil de 250 lignes est recommandé pour les fichiers markdown
- Cet outil permet de surveiller la taille des fichiers du cerveau-projet

---

## Utilisation

```bash
./verifier-surcharge-fichier.sh [DOSSIER] [SEUIL]
```

### Paramètres

| Paramètre | Défaut | Description |
|---|---|---|
| `DOSSIER` | `.` | Dossier à vérifier |
| `SEUIL` | `250` | Seuil en nombre de lignes |

---

## Résultat

### Exemple de sortie

```
=== Vérification de surcharge dans cerveau-projet ===
Seuil : 250 lignes

[ATTENTION] cerveau-projet/agents/buffy/buffy.md : 212 lignes
[ATTENTION] cerveau-projet/pense-betes/regles-immuables/general/protocole-carte-decision/protocole-carte-decision.001.01.ebauche.md : 227 lignes

=== Terminé ===
```

---

## Seuils recommandés

| Seuil | Usage |
|---|---|
| **100 lignes** | Fichiers de configuration simples |
| **200 lignes** | Fichiers de contenu standard |
| **250 lignes** | Fichiers de contenu détaillé (recommandé) |
| **500 lignes** | Fichiers de documentation longue |

---

## Notes

- Le seuil par défaut est de 250 lignes
- Les fichiers dépassant le seuil sont signalés avec `[ATTENTION]`
- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- Utiliser `purifier-fichier` ou `condenseur` pour réduire la taille

---

## Liens

- **Outil similaire** : `verifier-role-fichier` — vérifie le rôle d'un fichier
- **Outil de correction** : `purifier-fichier` — purifie un fichier
- **Outil de correction** : `condenseur` — condense un fichier
