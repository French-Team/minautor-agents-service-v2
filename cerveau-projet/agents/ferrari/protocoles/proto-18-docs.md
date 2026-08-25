# PROTOCOLE 18 -- Modifier la documentation (freelance/docs/)

> Ce protocole s'applique QUAND Mecano modifie un fichier
> dans cerveau-projet/freelance/docs/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## IDENTITE DU DOSSIER

| Champ | Valeur |
|---|---|
| **Chemin** | cerveau-projet/freelance/docs/ |
| **Proprietaire** | Rogers (conventions) + Redacteur-v2 (redaction) |
| **Type** | Documentation technique |
| **Encodage** | UTF-8 + CRLF |

---

## FICHIERS PRESENTS

| Fichier | Contenu | Proprietaire |
|---|---|---|
| mcp-reference.md | Reference complete du protocole MCP | Rogers |

---

## POURQUOI CE DOSSIER EST IMPORTANT

La documentation est la MEMOIRE de la v2.
Si elle est fausse ou obsolete, les agents prennent des mauvaises decisions.

---

## REGLE ABSOLUE

> JE NE MODIFIE JAMAIS un fichier de documentation sans avoir VERIFIE
> que le contenu est toujours CORRECT par rapport au code.
> La documentation suit le code, jamais l'inverse.

---

## AVANT de commencer

1. **Lire le fichier a modifier EN ENTIER**
2. **Verifier le code concerne** : la documentation est-elle toujours exacte ?
3. **Verifier la date** : le fichier est-il obsolete ?
4. **Verifier le frontmatter** : version, date, proprietaire

---

## APRES modification

1. **Relire la modification** : est-ce clair et exact ?
2. **Verifier 1 exemple** : fonctionne-t-il encore ?
3. **Mettre a jour la version** dans le frontmatter
4. **Mettre a jour le cahier de dev**

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| Pas de documentation sans verification du code | Risque de desinformation |
| Pas de suppression de sections entieres | Les agents en dependent |
| Pas de changement de format (Markdown) | Casserait la lisibilite |
