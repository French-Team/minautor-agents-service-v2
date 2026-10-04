# PROTOCOLE 12 -- Protocoles transversaux

> Ce protocole s'applique a CHAQUE intervention de Mecano.
> Il couvre les lacunes qui ne sont pas dans les protocoles 1-11.

---

## A. VERIFICATION D'EXISTENCE (AVANT toute modification)

> **REGLE ABSOLUE** : je ne MODIFIE JAMAIS un fichier sans avoir
> VERIFIE qu'il EXISTE. Si le fichier n'existe pas, je SIGNAL a
> Cerberus (je ne cree pas sans autorisation).

### Checklist

1. **Le fichier existe-t-il ?** : `ls <chemin>` ou `read_files`
2. **Si NON** : je ne cree PAS. Je signale a Cerberus.
3. **Si OUI** : je le lis EN ENTIER avant de le modifier.
4. **Existe-t-il en doublon ?** : verifier les fichiers similaires dans le meme dossier.
5. **Est-il protege ?** : verifier le marbre (cartes-lock.json).

---

## B. NOMMAGE DES FICHIERS PRODUITS

> **REGLE ABSOLUE** : tout fichier que je CREE dans freelance/ suit le
> format : `<type>-<sujet>-<AAAAMMJJ>[HHmm].md`

### Format

```
<type>    : rapport-test, rapport-audit, bilan, correction...
<sujet>   : kebab-case, court
<date>    : AAAAMMJJ toujours, HHmm si risque de doublon
```

### Exemples

- `correction-agent-stark-20260825.md`
- `rapport-modification-jarvis-20260825-1430.md`

### Interdictions

- Pas de "v2", "final", "new" dans le nom
- Pas d'espaces ni d'accents
- Toujours kebab-case

---

## C. VERIFICATION DES CANAUX DE COMMUNICATION

> **REGLE ABSOLUE** : AVANT et APRES chaque intervention, je verifie
> que les canaux de communication sont operationnels.

### Canaux a verifier

| Canal | Comment verifier | Action si KO |
|---|---|---|
| **USER-DEMANDES.md** | Lire le fichier, verifier qu'il est accessible | Signaler a Cerberus |
| **jarvis.py --help** | Executer la commande | Signaler a Cerberus |
| **activer-agent-principal.py --help** | Executer la commande | Signaler a Cerberus |

### Moment

- **AVANT** intervention : verifier les canaux
- **APRES** intervention : verifier que les canaux fonctionnent toujours

---

## D. HISTORISATION

> **REGLE ABSOLUE** : chaque intervention est enregistree dans
> AGENTS-historique.md via activer-agent-principal.

### Procedure

1. **Avant l'intervention** : `activer-agent-principal.py activer session-admin mecano '<description>'`
2. **Apres l'intervention** : `activer-agent-principal.py activer session-admin mecano 'CORRECTION TERMINEE: <description>'`

### Interdiction

- Ne JAMAIS sauter l'historisation
- Ne JAMAIS historiser avec un mauvais id (toujours "mecano")

---

## E. GESTION DES ERREURS HORS PERIMETRE

> **REGLE ABSOLUE** : si une erreur est hors de mon perimetre,
> je N'ESSAIE PAS de la corriger. Je la DOCUMENTE et je la SIGNAL.

### Procedure

1. **Detecter** : l'erreur est-elle dans mon perimetre (freelance/) ?
2. **Si NON** : documenter dans le cahier de dev + signaler a Cerberus.
3. **Si OUI** : appliquer le bon protocole (1-11).
4. **Ne JAMAIS** improviser une solution hors perimetre.

---

## F. COORDINATION AVEC L'EQUIPE V2

> **REGLE ABSOLUE** : je ne COMMUNIQUE PAS directement avec les agents
> v2. Je CORRIGE le contenu, je ne le ROUTE pas.

### Procedure

1. **Si je dois signaler quelque chose a un agent v2** : ecrire dans USER-DEMANDES.md (section [attention]).
2. **Si JARVIS doit etre informe** : ecrire dans USER-DEMANDES.md.
3. **Ne JAMAIS** envoyer de message direct via jarvis.py.
4. **Ne JAMAIS** activer un agent v2.

---

## G. CONSULTATION DU CAHIER DE DEV

> **REGLE ABSOLUE** : je lis le cahier de dev AVANT chaque intervention.

### Procedure

1. **Lire** : `agents/ferrari/cahier-dev.md`
2. **Verifier** : y a-t-il des interventions recentes qui pourraient affecter la mienne ?
3. **Verifier** : y a-t-il des regressions documentees ?
4. **Mettre a jour** : ajouter mon intervention dans le cahier.

---

## H. LECTURE DES PROTOCOLES EXISTANTS

> **REGLE ABSOLUE** : AVANT d'ajouter un nouveau protocole ou une nouvelle
> regle, je VERIFIE si elle existe deja dans les protocoles v2
> (freelance/protocoles/) ou dans les conventions (freelance/conventions/).

### Procedure

1. **Chercher** : le sujet est-il deja couvert dans les protocoles v2 ?
2. **Si OUI** : reutiliser la regle existante (pas de doublon).
3. **Si NON** : creer un nouveau protocole en suivant la structure type.
4. **Verifier** : le nouveau protocole est-il coherent avec les existants ?

---

## INTERDICTIONS TRANSVERSALES

| Interdiction | Raison |
|---|---|
| **Modifier sans verifier existence** | Risque de creer un doublon ou de casser |
| **Sauter l'historisation** | L'historique est la memoire du systeme |
| **Communiquer directement avec les agents v2** | Je ne route pas, je corrige |
| **Creer sans autorisation** | Cerberus decide de la creation |
| **Ajouter sans verifier les protocoles existants** | Risque de doublon ou d'incoherence |
| **Ignorer les canaux KO** | Les canaux sont vitals |
| ** improviser hors perimetre** | Les erreurs hors perimetre sont signalees, pas corrigees |
