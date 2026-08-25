# PROTOCOLE 1 -- Modifier un agent v2 (freelance/)

> Ce protocole s'applique QUAND Mecano modifie un FICHIER D'AGENT dans
> freelance/ (fiche .md, corrections.md, arbre de decisions, etc.).
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## REGLE ABSOLUE

> Je suis un agent v1 (ASCII + LF) qui modifie des fichiers v2
> (UTF-8 + CRLF). JE NE MELANGE JAMAIS les deux encodages.

---

## AVANT de commencer

1. **Lire le fichier cible EN ENTIER** (comprendre l'agent, son role, ses regles)
2. **Verifier le frontmatter** : le fichier a-t-il un frontmatter D17 ?
   - OUI : verifier que je conserve TOUS les champs (nom, version, cree, statut, grade, medaille, notation, mot-cles, type, appartient_a, commun, tags, session, theme)
   - NON : c'est un fichier v1 deroute, NE PAS ajouter de frontmatter D17 (je corrige le contenu, pas la structure)
3. **Verifier l'encodage actuel** du fichier cible :
   - UTF-8 + CRLF = standard v2 : je continue en v2
   - ASCII + LF = standard v1 : je continue en v1 (fichier rare dans freelance/)
4. **Verifier les mots-cles** : minimum 5 mots-cles dans le frontmatter

---

## ECRIRE le fichier modifie

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF (comme le fichier original dans freelance/) |
| **Frontmatter** | Conserver intact (pas de modification sauf si demande expresse) |
| **Contenu** | Appliquer la correction demandee |
| **Mots-cles** | Minimum 5 dans le frontmatter |
| **Emojis** | Autorises (v2) |
| **Nommage** | Si nouveau fichier : kebab-case + date AAAAMMJJ |

---

## VERIFIER apres modification

1. **Relire le fichier modifie** : le frontmatter est-il coherent ?
2. **Verifier l'encodage** : le fichier est-il toujours UTF-8 + CRLF ?
3. **Verifier les mots-cles** : au minimum 5 ?
4. **Verifier la coherence** : le fichier est-il toujours lisible et coherent ?

---

## EXEMPLE de modification

**Avant** (fichier stark.md dans freelance/) :
```yaml
---
identite:
  nom: Stark
  version: 0.3.0
  ...
  session: freelance
  theme: MARVEL
---
```

**Modification demandee** : ajouter une regle dans les REGLES ABSOLUES

**Apres** : meme frontmatter, meme encodage (UTF-8 + CRLF), regle ajoutee
dans le corps du fichier. PAS de changement de version (c'est a l'agent
de decider ou a Cerberus).

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Modifier le frontmatter D17** | Sauf demande expresse de l'agent ou de Cerberus |
| **Changer l'encodage** | Le fichier reste UTF-8 + CRLF |
| **Supprimer des mots-cles** | Minimum 5 toujours |
| **Ajouter un parcours lineaire** | Les agents v2 ont des ARBRES, pas des parcours |
| **Modifier les regles immuables freelance** | Regle dans regles-immuables/freelance/ |
