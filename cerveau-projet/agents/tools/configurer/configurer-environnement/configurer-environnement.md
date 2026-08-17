# configurer-environnement

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** configurer
**Proprietaire :** Vulcain (outil partage)

## Pourquoi cet outil ?

Le lanceur de non-regression (`tester-lancer-non-regression`) avait le nombre
de workers **code en dur** (`min(os.cpu_count(), 16)`), sans aucune adaptation
aux ressources reelles de la machine (RAM disponible, disque libre, charge
CPU). Sur une machine peu dotee, 16 workers provoquent du swapping et
**ralentissent** la suite au lieu de l accelerer.

Cet outil mesure les ressources reelles et ecrit une configuration
(`config-environnement.json`) que le lanceur lit pour auto-regler workers et
timeouts. C est la **fondation des configurations adaptables** (demande
utilisateur 2026-08-17).

## Utilisation

```bash
# Generer (ou regenerer) la configuration a partir des ressources reelles
python3 configurer-environnement.py --generer

# Simuler sans ecrire (voir ce qui serait ecrit)
python3 configurer-environnement.py --generer --dry-run

# Afficher la configuration actuelle
python3 configurer-environnement.py --afficher

# Detail du calcul des workers
python3 configurer-environnement.py --generer --verbose
```

## Options

| Option | Usage |
|---|---|
| `--generer` | Mesure les ressources et ecrit config-environnement.json |
| `--afficher` | Affiche la config actuelle (ne modifie rien) |
| `--reappliquer` | Alias de --generer (mesure a nouveau + reecrit) |
| `--dry-run` | Simuler sans ecrire |
| `--verbose` | Detail du calcul des workers |
| `--version` | Affiche la version |
| `--aide, -h` | Afficher cette aide |

## Contenu de la configuration

`config-environnement.json` (dans le dossier du lanceur) :

| Champ | Signification |
|---|---|
| `cpu_count` | Nombre de coeurs detectes |
| `ram_totale_mo` | RAM totale (Mo) |
| `ram_disponible_mo` | RAM disponible (Mo) |
| `disque_libre_go` | Espace disque libre (Go) |
| `charge_cpu` | Charge CPU (%) |
| `workers_recommandes` | Nombre de workers recommande (paliers) |
| `timeout_test_recommande` | Timeout interne par test (s) |

## Calcul des workers (paliers)

| RAM disponible | Workers recommandes |
|---|---|
| < 2 Go | 2 (preserver la RAM) |
| < 8 Go | moitie des coeurs (plafonne a 8) |
| sinon | min(cpu_count, 16) |

Le timeout interne par test part de 120s et augmente de 15s par tranche de
4 workers (contention quand on parallellise fort).

## Notes

- `psutil` est une dependance douce : si absent, seule la RAM/charge est
  inconnue (les autres champs restent remplis, workers = min(cpu, 16)).
- ASCII strict + LF pur.
- Le lanceur lit cette config via sa fonction `lire_workers_config()` : si le
  fichier est absent, il retombe sur `min(cpu_count, 16)` (comportement
  historique).
