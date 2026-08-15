# Liste Centrale des Protections (deploiement dynamique)

**Version** : 0.2.0
**Proprietaire** : Morpheus (outil partage)
**Reference** : `cerveau-projet/agents/tools/tester/tester-protections/tester-protections.py`
**Regle** : regle immuable PROTECTIONS + OPTIONS + CHRONO (template-test.md v0.3.0)

---

## Principe (demande utilisateur 2026-08-15)

L'ajout des protections est **DYNAMIQUE** : les protections vivent dans cette
**liste centrale unique**. Le template-test.md agit comme un **CONSTRUCTEUR** :
il importe la liste et DEPLOIE les protections automatiquement en amont et en
aval du test. Consequence : une fois le template corrige, **TOUT nouveau test
ou script temporaire est directement protege** par les nouvelles protections
ajoutees a la liste - sans modification du code du test.

```
LISTE (cette liste)  --import-->  tester-protections.py (point d entree unique)
        |                                        |
        |                                PROTECTIONS = charger_protections()
        v                                        v
   ajouter une protection        deploiement AUTOMATIQUE dans chaque test
   ici = protege tout            (amont : avant les points / aval : en fin)
```

---

## La liste (source de verite)

| # | Protection | Type | Deploiement | Description |
|---|---|---|---|---|
| 1 | `boucles-infinies` | stop | amont | Depassement de delai : arret force de l arbre (timeout) |
| 2 | `erreurs-silencieuses` | signal | aval | stderr non vide / mots-cles d erreur : signalement (le test juge) |
| 3 | `blocage` | stop | amont | Pas de reponse pendant X sec : arret force + STOP |
| 4 | `stop` | stop | aval | Point critique en echec : arret immediat du test (fail-fast) |
| 5 | `chrono` | chrono | amont+aval | Mesure des durees par etape (`point_actif` / `chrono_etape` / `bilan_chrono`) + option `--no-chrono` |
| 6 | `options-on-off` | outil | amont | `--isoler N` / `--desactiver 1,3,5` : isoler un test ou desactiver des points sans toucher au code |

La liste vivante se consulte via la commande :
`python3 cerveau-projet/agents/tools/tester/tester-protections/tester-protections.py --liste`

---

## Deploiement amont (debut du test, dans le canevas du template)

1. Import du point d entree unique : `PROTECTIONS = charger_protections()`
2. Options on/off : parsing de `sys.argv` (`CHRONO_ACTIF`, `ISOLE`,
   `DESACTIVES`) - protection `options-on-off`
3. Chrono : `T_START = time.monotonic()` - protection `chrono`
4. Executions : `PROTECTIONS.lancer_protege(cmd, timeout)` au lieu de
   `subprocess.run` brut - protections `boucles-infinies` + `blocage`

## Deploiement aval (fin du test, dans le canevas du template)

1. `bilan_chrono()` : affiche la duree totale + la duree par etape
   (alimente les outils de suivi futurs) - protection `chrono`
2. `verifier_critique(...)` sur les points CRITIQUES : leve
   `ArretProtection` -> le test s arrete immediatement - protections
   `stop` + `erreurs-silencieuses`
3. `=== RESULTAT : N OK / M KO ===` puis retour `0 si NB_KO == 0 sinon 1`

---

## Ajouter une protection (procedure)

1. Ajouter l entree dans `LISTE_PROTECTIONS` (tester-protections.py)
2. La deployer dans le canevas du template-test.md (amont et/ou aval)
3. Bumper la version du module + documenter dans le changelog
4. Lancer la non-regression (les tests existants heritent automatiquement
   de la nouvelle protection via l import unique)

## Verification (garde-fou)

- test-030 : chaque test-0XX importe les protections (bloc standard)
- test-044 : le template impose le triplet (protections + options + chrono)
