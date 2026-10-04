# exec
> subprocess standardise : rc + captures + timeout (fini le quoting rate).
| Version | 0.1.0 | Proprietaire | Forge |
## Contrat : entry.py --timeout N commande [args...] (REMAINDER : les flags de la commande passent)
Retour JSON {rc, stdout, stderr, timeout}. Fonction : lancer(commande).
