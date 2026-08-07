# mettre-a-jour-agents-md

**Categorie** : Mettre a jour
**Version** : 0.2.0
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Modifier AGENTS.md de maniere fiable et structuree.

**Pourquoi cet outil ?**
- AGENTS.md est un fichier critique -- les erreurs cassent le cycle
- Cet outil est concu SPECIFIQUEMENT pour AGENTS.md
- Il gere la structure et les formats automatiquement
- Il est fiable et teste

---

## Utilisation

Version Python (recommandee) :

```bash
python3 mettre-a-jour-agents-md.py <action> [parametres]
```

Version bash equivalente : `mettre-a-jour-agents-md.sh` (meme logique).

---

## Actions disponibles

### 1. Activer un agent

```bash
python3 mettre-a-jour-agents-md.py activer Buffy "Corriger les fichiers" "Mettre a jour demarrer.md"
```

**Fait :**
1. Lit AGENTS.md
2. Met a jour la section "Agent Principal Actuel"
3. Ajoute l'entree dans l'historique
4. Ecrit le fichier

### 2. Reactiver Cerberus

```bash
python3 mettre-a-jour-agents-md.py reactiver "Mission terminee" Buffy
```

**Fait :**
1. Lit agents/cerberus/cerberus.md
2. Lit AGENTS.md
3. Met a jour avec "Nom: Cerberus"
4. Ajoute l'entree dans l'historique
5. Ecrit le fichier

---

## Format de sortie

### Section "Agent Principal Actuel"

```markdown
## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | [agent] |
| **Role** | [role de l'agent] |
| **Derniere mise a jour** | [date] |
| **Fiche** | [lien] |
| **Corrections** | [lien] |
| **Active par** | [agent precedent] |
| **Raison** | [raison] |
```

### Historique (AGENTS-historique.md)

```
| [date et heure] | [agent] | [raison] |
```

**Format de l'horodatage** : `YYYY-MM-DD HH:MM` (date + heure precise)

**Regles de l'historique** :
- **Heure incluse** : chaque entree porte la date ET l'heure (HH:MM) pour situer precisement les groupes d'interventions
- **Ordre decroissant** : les entrees les plus recentes sont en HAUT du tableau
- **Limite 150** : le fichier ne conserve que les 150 interventions les plus recentes (les plus anciennes sont retirees automatiquement)

---

## Ce que fait cet outil

| Capacite | Description |
|---|---|
| Specifique a AGENTS.md | Concu pour ce fichier critique |
| Gere le format | La structure est maintenue automatiquement |
| Lit cerberus.md | Lit le fichier de Cerberus pour la reactivation |
| Valide le resultat | Verifie que la modification est correcte |
| Fiable et teste | Fonctionne a chaque fois |
| Horodatage HH:MM | Date + heure precise dans l'historique |
| Ordre decroissant | Les plus recentes en haut |
| Limite 150 | Tronque automatiquement a 150 entrees |
| Verification ASCII | Refuse toute raison contenant un caractere non-ASCII (lecon permanente 2026-08-07) |

---

## Exemple complet

### Utilisation

```
1. Appeler mettre-a-jour-agents-md.py reactiver "Mission terminee" <agent>
2. L'outil lit cerberus/cerberus.md
3. L'outil met a jour AGENTS.md
4. C'est fait -- fiablement
```

---

## Dependances

- `AGENTS.md` -- fichier a modifier
- `agents/cerberus/cerberus.md` -- lu lors de la reactivation

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0-beta | 2026-08-06 | Historique : horodatage HH:MM + ordre decroissant + limite 150 |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels avec protections (activation, reactivation, limite 150, ordre decroissant), VERSION ajoutee au script, promotion prepare |
| 0.2.1 | 2026-08-07 | Lecon permanente ASCII : verifier_ascii() avant toute ecriture (raison non-ASCII REFUSEE) + verifier_fichier_ascii() post-ecriture (WARNING si corruption pre-existante). Cause racine : caractere U+00E9 corrompu trouve dans AGENTS-historique.md lors de l'audit general |
| 0.2.0-py | 2026-08-07 | Version Python creee (mettre-a-jour-agents-md.py), basee sur outil-template.py. Portage fidele : actions activer/reactiver, historique HH:MM decroissant limite 150, verification ASCII avant ecriture |
| Renommage | 2026-08-07 | Renommage de mettre-a-jour-modifier-agents-md vers mettre-a-jour-agents-md (le nom ne refletait pas la fonction reelle : l'outil met a jour le fichier AGENTS.md). 136 references mises a jour dans 30 fichiers + spec + boucle retro-action |

---

## Notes

- Cet outil est CRITIQUE -- il gere le fichier le plus important
- La reactivation lit cerberus.md (pas corrections.md sauf en cas d'erreur)
- Chaque erreur ici casse tout le cycle

---
