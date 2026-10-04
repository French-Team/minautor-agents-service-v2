# PROTOCOLE 15 -- Modifier les templates

> Ce protocole s'applique QUAND Mecano modifie un fichier
> dans cerveau-projet/freelance/templates/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## IDENTITE DU DOSSIER

| Champ | Valeur |
|---|---|
| **Chemin** | cerveau-projet/freelance/templates/ |
| **Proprietaire** | Shuri (creation) + Rogers (conventions) |
| **Type** | Templates de creation |
| **Encodage** | UTF-8 + CRLF |

---

## FICHIERS PRESENTS

| Fichier | Sert a creer | Utilise par |
|---|---|---|
| template-agent-v2.md | Fiche d'agent | Shuri, Mecano |
| template-corrections-v2.md | Corrections d'agent | Shuri, Mecano |
| template-arbre-v2.json | Arbre de decisions | Shuri |
| template-theme-v2.json | Theme d'arbre | Shuri |
| template-fins-v2.json | Fins d'arbre | Shuri |
| template-outil-v2.md | Mode d'emploi outil | Forge, Mecano |
| template-outil-v2.py | Script outil | Forge, Mecano |
| template-outil-v2-data.json | Donnees outil (D15) | Forge, Mecano |
| README.md | Documentation templates | Rogers |

---

## POURQUOI CE DOSSIER EST CRITIQUE

Les templates DEFINISSENT la structure de TOUT ce qui sera cree.
Si un template est casse, TOUS les futurs agents/outils seront casses.

---

## REGLE ABSOLUE

> JE NE MODIFIE JAMAIS un template sans avoir VERIFIE
> que les agents/outils EXISTANTS sont toujours conformes
> a la nouvelle structure. Si le template change,
> les creations passees doivent toujours fonctionner.

---

## AVANT de commencer

1. **Lire le template a modifier EN ENTIER**
2. **Identifier les agents/outils existants** qui utilisent ce template
3. **Verifier qu'ils sont conformes** au template ACTUEL
4. **Verifier que le changement est retrocompatible**
5. **Si NON retrocompatible** : je SIGNAL a Cerberus, je ne modifie pas

---

## APRES modification

1. **Verifier 1 agent existant** : est-il toujours conforme ?
2. **Verifier 1 outil existant** : est-il toujours conforme ?
3. **Mettre a jour le README.md** du dossier templates/
4. **Mettre a jour conventions.md** si le template change les conventions
5. **Mettre a jour le cahier de dev** : noter ce qui a change

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| Pas de changement retrocompatible non teste | Casse les creations futures |
| Pas de suppression de champs obligatoires | Les agents existants en dependent |
| Pas de changement de format (JSON, YAML) | Casse les parseurs |
| Pas de modification sans verification des existants | Risque de regression |
