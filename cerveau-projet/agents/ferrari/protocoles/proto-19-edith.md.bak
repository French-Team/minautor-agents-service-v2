# PROTOCOLE 19 -- Modifier EDITH (agent dormant special)

> Ce protocole s'applique QUAND Mecano modifie un fichier
> dans cerveau-projet/freelance/edith/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## IDENTITE DE L'AGENT

| Champ | Valeur |
|---|---|
| **Chemin** | cerveau-projet/freelance/edith/ |
| **Proprietaire** | EDITH (auto-observatrice) |
| **Type** | Agent dormant + serveur H24 |
| **Statut** | dormante (reveil par son serveur ou sur demande) |
| **Encodage** | UTF-8 + CRLF |

---

## POURQUOI EDITH EST SPECIALE

EDITH n'est PAS un agent normal. Elle a 3 particularites :

| Particularite | Description | Impact |
|---|---|---|
| **DORMANTE** | Elle dort jusqu'a son reveil | Pas dans les rounds normaux |
| **SERVEUR H24** | Son serveur de routines vit en continu | Collecte des donnees 24h/24 |
| **LECTURE SEULE** | Elle observe, elle ne modifie jamais | Zero ecriture sauf rapports |

---

## STRUCTURE

```
edith/
├── edith.md              <- fiche (dormante, silver, notation 85)
├── corrections.md        <- fenetre glissante
├── parcours/
│   ├── arbre-edith.json  <- arbre de decisions (PAS une carte)
│   ├── fins.json         <- fins centralisees
│   ├── theme-lire.json   <- theme lecture
│   ├── theme-observer.json <- theme observation
│   └── theme-rapporter.json <- theme rapport
└── rapports/             <- rapports de suivi de score
    ├── suivi-stark-*.md
    └── suivi-vision-*.md
```

---

## REGLES ABSOLUES EDITH

| Regle | Description |
|---|---|
| **LECTURE SEULE** | EDITH ne modifie JAMAIS de fichiers (sauf ses propres rapports) |
| **PAS DE ROUND** | EDITH n'est JAMAIS dans un round (pas d'activation par Cerberus en round) |
| **SERVEUR INDEPENDANT** | Son serveur vit hors des rounds, collecte en continu |
| **REVEIL CONDITIONNEL** | EDITH ne se reveille que sur signal (serveur ou demande utilisateur) |
| **4 W** | Qui, Quoi, Comment, Quand -- ses rapportent toujours ces 4 elements |

---

## AVANT de commencer

1. **Lire edith.md EN ENTIER** : comprendre son statut dormant
2. **Lire arbre-edith.json** : comprendre ses 3 themes (lire, observer, rapporter)
3. **Verifier le statut** : est-elle encore dormante ?
4. **Verifier les rapports** : sont-ils a jour ?

---

## CAS PARTICULIERS

| Situation | Action |
|---|---|
| Modifier edith.md | Proto 1 (agent v2) + Proto 19 (regles EDITH) |
| Modifier arbre-edith.json | Proto 4 (arbre) + Proto 19 |
| Ajouter un rapport | Proto 19 UNIQUEMENT (pas de proto specifique) |
| Modifier le serveur | NE PAS TOUCHER (c'est dans tools-commun/routines/) |

---

## APRES modification

1. **Verifier le statut** : EDITH est-elle toujours dormante ?
2. **Verifier les rapports** : sont-ils toujours lisibles ?
3. **Mettre a jour le cahier de dev**
4. **Signaler a Cerberus** : si le statut a change

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| Pas d'activation en round | EDITH est hors-round |
| Pas de modification de fichiers autres que les siens | LECTURE SEULE |
| Pas de modification de son serveur | Independance operationnelle |
| Pas de changement de statut sans autorisation | Dormant = pas deranger |
