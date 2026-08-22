---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# hades-contexte-git

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** git
**Chemin :** `agents/tools/git/hades-contexte-git/`
**Proprietaire :** Hades (agent dedie au git)

## Description

Caisse a outils git de Hades (M8b) : retourne en JSON le contexte complet du
depot - identite (user.name/email), projet, branche, remote origin, dernier
commit (sha/date/sujet), AGE EN MINUTES du dernier commit avec VERDICT
RECENT/PERIME (garde-fou de la regle d anciennete), nombre de fichiers modifies.

## Utilisation

```
python3 hades-contexte-git.py [--version]
```

## Regle d anciennete (decision utilisateur 2026-08-22)

- Seuil : 30 minutes.
- `checkout.autorise` = true seulement si age <= seuil.
- Au-dela : checkout INTERDIT - reparation dans le present par l agent
  habilite (flux INTER-ROUND, protocole-fin-mission v0.2.0).

## Preuve reelle (2026-08-22)

Commit vieux de 913.8 minutes -> verdict PERIME, checkout.autorise false,
80 fichiers modifies non commits : le garde-fou aurait bloque le checkout
dangereux du jour.
