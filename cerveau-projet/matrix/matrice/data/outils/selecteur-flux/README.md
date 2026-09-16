# Selecteur de Flux Matrice

## Description

Le selecteur de flux est le mecanisme central qui determine quel flux est actif dans la Matrice :
- **Flux 1 (Cameleon)** : Mode COMMUNICATION - La Matrice GUIDE le cameleon
- **Flux 2 (Optimus)** : Mode MAINTENANCE - La Matrice SURVEILLE Optimus

## Utilisation

### Consulter le flux actuel
```bash
python3 cerveau-projet/matrix/matrice/data/outils/selecteur-flux/main.py actuel
```

### Basculer vers un flux
```bash
python3 cerveau-projet/matrix/matrice/data/outils/selecteur-flux/main.py basculer <flux> --par <qui> --raison <texte>
```

### Afficher l'historique
```bash
python3 cerveau-projet/matrix/matrice/data/outils/selecteur-flux/main.py historique --derniers <n>
```

## Integration avec le demarrage

Le fichier `demarrer.md` contient un ORDRE 0 qui verifie le selecteur avant tout demarrage :
1. Si FLUX1 -> demarrer-cameleon.md
2. Si FLUX2 -> demarrer-optimus-prime.md
3. Si AUCUN -> l'utilisateur doit choisir

## Routine de verification

La routine `verifier-selecteur.py` verifie la coherence entre le selecteur et les processus en cours :
```bash
python3 cerveau-projet/matrix/matrice/routines/selecteur-flux/verifier-selecteur.py --verbose
```

## Fichier de configuration

Le selecteur est stocke dans : `cerveau-projet/matrix/matrice/data/selecteur-flux.json`

## Securite

- Un seul flux peut etre actif a la fois
- Les changements sont historises
- Les routines verifient la coherence
