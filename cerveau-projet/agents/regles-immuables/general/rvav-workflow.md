---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Workflow RVAVP -- Rechercher -> Verifier -> Analyser -> Valider -> Purifier

## Principe fondamental

Chaque fichier de contenu (`[type]-[theme].[id].[class].[statut].md`) passe par
5 statuts. Le passage du statut N au statut N+1 **exige une boucle RVAVP complete**
sur le travail effectue dans le statut N.

**On ne peut jamais passer au statut superieur sans avoir passe la boucle de
controle du statut courant.** Une erreur declenche une regression + increment du `class`.

**Nouveau** : La purification est la derniere etape avant de considerer un fichier comme valide.

---

## Les 5 statuts

| Statut | Ordre | Travail attendu |
|---|---|---|
| `ebauche` | 1 | Idee brute, structure minimale, rien de valide |
| `prepare` | 2 | Structure complete, ready pour le developpement |
| `dev` | 3 | Contenu developpe (toutes les sections ecrites) |
| `test` | 4 | RVAV effectue, liens verifies, coherence validee |
| `valide` | 5 | Approuve, reference fiable pour le projet |

---

## Boucle RVAVP (a chaque transition)

### 1. [rechercher]
- Rassembler toutes les references externes liees au travail du statut courant
- Identifier les dependances (liens vers d'autres pense-betes, specs, conventions)
- Noter les exigences non couvertes par le travail effectue

### 2. [verifier]
Checklist stricte -- **aucun point ne peut rester ouvert** :
- [ ] Structure du nom respecte `convention-renommage.md` (id.class.statut)
- [ ] Tous les sous-fichiers attendus existent (spec, todo, liens si applicable)
- [ ] Tous les liens internes pointent vers des fichiers existants
- [ ] Le contenu du statut courant est complet (rien d'a moitie-ecrit)

### 3. [analyser]
- Relecture approfondie du travail effectue dans le statut courant
- Verifier la coherence interne (logique, terminologie, references croisees)
- Identifier les incoherences, manques ou erreurs

### 4. [valider]
Decision finale apres RVAV :
- **Avancer** -> statut += 1, class += 1, renommage du fichier
- **Rester** -> class += 1, statut identique, travail de correction
- **Reculer** -> statut -= 1, class += 1, retour au travail precedent

### 5. [purifier]
Nettoyer le fichier apres validation (mise a jour 2026-08-15, decision utilisateur :
le protocole avait ete abandonne et n etait plus a jour - besoins listes par Buffy) :

**Principe (anti-perte) : on ne supprime JAMAIS d information.** La purification
DEPLACE vers un fichier d historique a cote (archive), elle ne tronque pas.

**Quotas par type de fichier (detecter-surcharge-fichier, seuil 250)** :

| Type | Quota (lignes) | Action |
|---|---|---|
| `corrections.md` d agent | 1000 | archiver les lecons les plus anciennes dans `<agent>-historique.md` |
| `AGENTS-historique.md` | 800 | archiver les entrees les plus anciennes dans AGENTS-historique-archive.md |
| fiches agents | 320 | signaler seulement (structure template) |
| protocoles | 400 | signaler seulement (structure documentaire) |

**Procedure (outil dedie `purifier-rvav`, cree par Vulcain)** :
1. `purifier-rvav --tous --dry-run --rapport plan.md` : detecter les fichiers en
   surcharge, afficher le plan (lignes avant/apres, sections a archiver)
2. Relire le rapport, valider le plan
3. `purifier-rvav --tous --executer` : appliquer (deplacement vers l archive,
   jamais de suppression)
4. Verifier : fichier principal sous le quota, archive creee, aucune perte
   (somme des lignes conservee), LF pur + ASCII strict

**Pour les fichiers de contenu (pense-betes, specs, protocoles)** :
- [ ] Supprimer les blockquotes explicatifs inutiles
- [ ] Reduire les exemples au minimum
- [ ] Supprimer les notes historiques
- [ ] Simplifier les justifications
- [ ] Verifier que le fichier reste comprehensible
---

## Boucle de retroaction (erreur)

Si une erreur est detectee a l'etape 3 [analyser] ou 4 [valider] :

1. Le fichier **garde** son `id` (jamais modifie)
2. Le `class` est **incremente** (+1)
3. Le fichier est **renomme** avec le nouveau class + le statut ajuste
4. Le travail de **correction** commence -> nouveau cycle RVAV depuis [rechercher]
5. Aucune avancee de statut n'est possible tant que RVAV ne valide pas

---

## Exemple de cycle complet

```
protocole-composition.001.01.ebauche.md
  -> RVAV : recherche de liens, checklist, analyse de coherence -> ECHEC (manque contenu spec)
  -> class +1, reste en ebauche
protocole-composition.001.02.ebauche.md
  -> RVAV : recherche, verification, analyse -> SUCCES
  -> class +1, statut +1
protocole-composition.001.03.prepare.md
  -> RVAV -> ECHEC (liens casses)
protocole-composition.001.04.prepare.md
  -> RVAV -> SUCCES
  -> statut +1
protocole-composition.001.05.dev.md
  -> ... et ainsi de suite jusqu'a valide
```

---

## Exigibilite

Ce workflow est **contraignant par defaut**. Toute personne travaillant sur le cerveau
doit passer chaque fichier par ce cycle RVAVP entre chaque statut.

**Note** : La purification est obligatoire avant de considerer un fichier comme `valide`.
