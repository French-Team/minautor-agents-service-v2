# detecter-surcharge-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Detecter
**Chemin :** `agents/tools/detecter/detecter-surcharge-fichier/`

## Description

Detecter les fichiers qui depassent un seuil de taille (nombre de lignes).

**Pourquoi cet outil ?**
- Les fichiers trop gros sont difficiles a lire et a maintenir
- Un seuil de 250 lignes est recommande pour les fichiers markdown
- Cet outil permet de surveiller la taille des fichiers du cerveau-projet

## Utilisation

```bash
./detecter-surcharge-fichier.sh [DOSSIER] [SEUIL]
```

### Parametres

| Parametre | Defaut | Description |
|---|---|---|
| `DOSSIER` | `.` | Dossier a verifier |
| `SEUIL` | `250` | Seuil en nombre de lignes |

## Resultat

### Exemple de sortie

```
=== Detection de surcharge dans cerveau-projet ===
Seuil : 250 lignes

[ATTENTION] cerveau-projet/agents/buffy/buffy.md : 212 lignes
[ATTENTION] cerveau-projet/pense-betes/regles-immuables/general/protocole-carte-decision/protocole-carte-decision.001.01.ebauche.md : 227 lignes

=== Termine ===
```

## Seuils recommandes

| Seuil | Usage |
|---|---|
| **100 lignes** | Fichiers de configuration simples |
| **200 lignes** | Fichiers de contenu standard |
| **250 lignes** | Fichiers de contenu detaille (recommande) |
| **500 lignes** | Fichiers de documentation longue |

## Notes

- Le seuil par defaut est de 250 lignes
- Les fichiers depassant le seuil sont signales avec `[ATTENTION]`
- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- Utiliser `nettoyer-fichier` ou `condenser-fichier` pour reduire la taille

## Liens

- **Outil similaire** : `verifier-role-fichier` -- verifie le role d'un fichier
- **Outil de correction** : `nettoyer-fichier` -- purifie un fichier
- **Outil de correction** : `condenser-fichier` -- condense un fichier

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
