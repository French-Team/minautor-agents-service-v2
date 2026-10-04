# Diagnostic -- Generaliser l'utilisation du generateur de commande

> Date : 2026-08-09
> Agent : Buffy (mission de diagnostic -- aucune modification effectuee)
> Methode : sous-protocole-diagnostic

---

## Symptomes

- **Probleme** : le generateur de commande (generateurs-commande) est "jamais utilise" par les agents alors qu'il doit garantir des commandes sans erreur. L'utilisateur demande sa generalisation en outil "systematique".
- **Quand** : constate lors des missions recentes (diagnostic initial du 08-08, confirme le 09-08).
- **Changements** : le catalogue a ete enrichi (106 commandes, couvre 91/92 outils reels) mais les parcours continuent de fournir des commandes python3 en dur copiees-collees.
- **Impact** : moyen-eleve -- risque d'erreurs de frappe/chemin/flag, et le generateur (outil phare du cerveau) reste un outil orphelin.

---

## Causes possibles

1. **Les parcours fournissent des commandes en dur** : l'agent n'a aucune raison d'utiliser le generateur si la commande exacte est deja dans la case.
2. **Les indices "passe par le generateur" sont trop rares** : seulement ~2 par parcours (morpheus : 0, demarrage : 0), donc pas systematique.
3. **Le generateur n'est pas un reflexe** : aucune regle immuable ne l'impose comme passage obligatoire avant de lancer une commande.
4. **Certaines commandes sont hors catalogue** : les verifications composites (parite py/sh --version avec diff) ne peuvent pas etre generees.

---

## Tests effectues

| # | Test | Resultat |
|---|---|---|
| 1 | Couverture du catalogue vs outils reels (.py hors tests) | **91/92 couverts** (seul regenerer-catalogue manque = normal, auto-genere) |
| 2 | Scan des 11 parcours + demarrage : commandes python3 en dur | **187 commandes en dur** |
| 3 | Outils distincts references en dur | **53 outils** -- **53/53 couverts par le catalogue** |
| 4 | Typologie des 187 commandes | 185 appels outils simples (COUVERTS) + 2 verifications composites (parite py/sh --version, HORS catalogue) |
| 5 | Indices "passe par le generateur" par parcours | ~2 en moyenne (morpheus 0, demarrage 0) |

### Repartition detaillee des commandes en dur par parcours

| Parcours | Commandes en dur | Outils distincts |
|---|---|---|
| athena | 14 | 10 |
| atlas | 23 | 15 |
| buffy | 27 | 15 |
| cerberus | 14 | 4 |
| clio | 12 | 6 |
| janus | 19 | 12 |
| minerve | 16 | 10 |
| morpheus | 8 | 5 |
| promethee | 15 | 10 |
| themis | 17 | 13 |
| vulcain | 16 | 9 |
| demarrage | 6 | 4 |
| **TOTAL** | **187** | **53** |

---

## Cause racine identifiee

**Cause** : les parcours fournissent les commandes exactes en dur (187), donc le generateur n'apporte aucune valeur ajoutee visible pour l'agent -- il n'est ni impose (regle) ni systematique (indices rares). Le catalogue est pret (53/53 outils couverts), mais les parcours ne pointent pas vers lui.

**Confiance** : Haute
**Impact** : Eleve (outil phare sous-utilise, risque d'erreurs de commande persistant)

---

## Solutions proposees

| # | Solution | Complexite | Impact |
|---|---|---|---|
| 1 | Convertir les 185 commandes en dur en cases "passe par le generateur" (avec le nom de la commande du catalogue) dans les 11 parcours + demarrage | Moyenne | Positif (systematique) |
| 2 | Ajouter une regle immuable : "toute commande d'outil passe par le generateur" (avec exception documentee pour les commandes composites) | Faible | Positif (normatif) |
| 3 | Enrichir l'indice generateur dans les cases (Pattern 9 procedure 4g existante) : nom de commande + parametres a renseigner | Moyenne | Positif (digeste pour l'agent) |
| 4 | Documenter dans le catalogue une commande "generateurs-commande --liste" d'auto-decouverte pour que l'agent trouve la bonne commande | Faible | Positif |
| 5 | Ne rien faire (statut quo) | Nulle | Neutre (l'outil reste orphelin) |

---

## Recommandation

**Solution recommandee** : combinaison des solutions 1 + 2 (conversion des 185 commandes + regle immuable), avec la solution 3 comme element de qualite.

**Justification** :
- La conversion (S1) est **faible risque** : 53/53 outils deja couverts par le catalogue, il s'agit de remplacer un texte par une reference au catalogue (les commandes generees sont identiques ou meilleures).
- La regle (S2) fige la philosophie : le generateur devient le reflexe obligatoire, comme RVAV ou ASCII.
- Les 2 commandes composites (parite py/sh) restent en dur par necessite -- a documenter comme exception.

**Decision utilisateur attendue** : valider la cible (S1+S2, S3 en option) avant toute modification -- conformement au choix "Diagnostic d'abord, decision ensuite".

---

## Validation

- [x] Les symptomes sont decrits
- [x] Les causes sont identifiees
- [x] Les tests sont effectues (scan complet des 12 parcours)
- [x] La cause racine est identifiee
- [x] Les solutions sont proposees
- [x] Aucune modification effectuee (mode diagnostic respecte)

---

*Diagnostic conforme au sous-protocole-diagnostic -- rapport depose par Buffy*
