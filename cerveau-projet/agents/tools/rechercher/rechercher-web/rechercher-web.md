# rechercher-web

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Rechercher
**Proprietaire :** Atlas (explorateur)

## Pourquoi cet outil ?

Les agents du cerveau travaillent avec leurs donnees et leur memoire
(recherches-web/ = leur memoire FACTUELLE, les souvenirs qui alimentent leurs
decisions). Un souvenir perime produit des decisions fausses (ex : coder un
projet Next.js avec une version obsolete de l API). Cet outil donne aux
agents un acces web REEL : chercher et lire, puis documenter dans
recherches-web/ pour que la memoire reste vraie et a jour (demande
utilisateur 2026-08-16).

## Fonctionnement

1. L agent appelle avec `--agent <nom>` (obligatoire) :
   - recherche : `rechercher-web.py --agent atlas "version stable de Next.js"`
   - lecture :   `rechercher-web.py --agent atlas --url https://nextjs.org/`
2. Le verrou d habilitation verifie que l outil est dans la carte de l agent
   (source de verite : parcours-*.json) et journalise l usage
   (registre-usages-outils.jsonl, mode verrou-auto).
3. L outil interroge le web (DuckDuckGo Lite pour la recherche, lecture
   directe pour --url), avec un timeout reseau INTERNE (protection - jamais
   de timeout exterieur).
4. L agent documente ensuite les informations dans recherches-web/
   (protocole-recherches-web, template recherche-template.md).

## Utilisation

```
# Recherche (titres + URLs + extraits)
python3 rechercher-web.py --agent atlas "documentation React Server Components"

# Lecture d une page (titre + texte lisible)
python3 rechercher-web.py --agent atlas --url https://nextjs.org/docs

# Rapport markdown (a deposer dans recherches-web/[theme]/)
python3 rechercher-web.py --agent atlas "etat actuel de Next.js" --rapport tmp-atlas/recherche-nextjs.md
```

## Regles

- Sources fiables d abord : documentation officielle, GitHub officiel, puis
  blogs reconnus (protocole-recherches-web).
- Toujours documenter la recherche dans recherches-web/ avant de l utiliser
  comme preuve.
- Verifier la fraicheur avant usage : une recherche de plus de 30 jours doit
  etre re-verifiee (voir detecter-recherches-obsoletes).
- Ne jamais inventer une source : si la page n est pas accessible, le dire.
- ASCII strict + LF (comme tout l outillage).

## Liens

- **Protocole** : [protocole-recherches-web](../../../regles-immuables/general/protocole-recherches-web/)
- **Memoire** : [recherches-web](../../../../recherches-web/index-recherches-web.md)
- **Template** : [recherche-template.md](../../../../recherches-web/templates/recherche-template.md)
- **Fraicheur** : [detecter-recherches-obsoletes](../../detecter/detecter-recherches-obsoletes/detecter-recherches-obsoletes.md)
- **Verrou** : [proteger-verrou-habilitation](../../proteger/proteger-verrou-habilitation/proteger-verrou-habilitation.md)
