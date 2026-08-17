# detecter-recherches-obsoletes

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Detecter
**Proprietaire :** Atlas (explorateur)

## Pourquoi cet outil ?

La memoire factuelle des agents vit dans recherches-web/. Une recherche non
re-verifiee devient un souvenir perime : l agent decide a partir de donnees
fausses (ex : une API Next.js obsolete). Cet outil signale les recherches a
re-verifier pour que la memoire reste VRAIE et D ACTUALITE (demande
utilisateur 2026-08-16 : les souvenirs = les donnees qui constituent les
decisions des agents).

## Critere d obsolescence

Une recherche est a re-verifier si au moins un des cas s applique :

1. `statut: obsolete` dans son header (declaree obsolete) ;
2. `date_validite` depassee (champ YAML optionnel du template) ;
3. age > `--seuil` jours depuis `date` (defaut 30).

## Utilisation

```
# Scan complet (defaut : seuil 30 jours, hors deja-obsoletes)
python3 detecter-recherches-obsoletes.py

# Seuil personnalise (ex : tout ce qui a plus de 14 jours)
python3 detecter-recherches-obsoletes.py --seuil 14

# Inclure les deja-obsoletes + rapport
python3 detecter-recherches-obsoletes.py --tous --rapport tmp-atlas/rapport-obsoletes.md

# Exemple de champ date_validite dans une recherche :
#   recherche:
#     ...
#     date: "2026-08-16"
#     date_validite: "2026-09-15"
```

## Regles

- Lecture seule : l outil ne modifie JAMAIS recherches-web/ (la mise a jour
  d une recherche se fait via la re-verification documentee).
- A lancer avant chaque mission qui depend de donnees web (protocole-
  recherches-web, etape 2 : chercher dans le cerveau).
- Le retour est 0 si rien a re-verifier, 1 sinon (utilisable en garde-fou).
- ASCII strict + LF.

## Liens

- **Memoire** : [recherches-web](../../../../recherches-web/index-recherches-web.md)
- **Protocole** : [protocole-recherches-web](../../../regles-immuables/general/protocole-recherches-web/)
- **Acces web** : [rechercher-web](../../rechercher/rechercher-web/rechercher-web.md)
