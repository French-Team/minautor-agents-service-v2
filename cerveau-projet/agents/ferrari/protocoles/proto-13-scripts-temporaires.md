# PROTOCOLE 13 -- Scripts temporaires

> Ce protocole s'applique QUAND un agent (v1 ou v2) doit creer ou
> modifier un SCRIPT TEMPORAIRE dans freelance/.
> Les scripts temporaires sont des outils de dev utilises une fois
> puis supprimes. Ils doivent TOUJOURS passer par un harnais.

---

## REGLE ABSOLUE

> **TOUT script temporaire est cree et execute a travers un harnais.**
> Aucun script temporaire ne s'execute SANS harnais.
> Les agents v2 sont OBLIGES d'utiliser le combo-harnais-script-temporaire.

---

## QU'EST-CE QU'UN SCRIPT TEMPORAIRE ?

| Caracteristique | Description |
|---|---|
| **But** | Executer une tache ponctuelle (test, verification, migration) |
| **Duree** | Utilise UNE FOIS puis supprime |
| **Emplacement** | /tmp/mecano-<nom>/ ou freelance/scripts-temp/ |
| **Encodage** | UTF-8 + CRLF (comme tout fichier v2) |
| **Lifecycle** | CREER -> EXECUTER -> VERIFIER -> SUPPRIMER |

---

## TYPES DE SCRIPTS TEMPORAIRES

| Type | Exemple | Harnais requis |
|---|---|---|
| **Script de test** | Verifier qu'un outil fonctionne | harnais-test |
| **Script de migration** | Deplacer des fichiers | harnais-modification |
| **Script de verification** | Checker l'integrite | harnais-edition |
| **Script de nettoyage** | Supprimer des residus | harnais-creation (inverse) |

---

## PROCEDURE OBLIGATOIRE

### AVANT de creer un script temporaire

1. **Lire ce protocole** (proto-13)
2. **Verifier le combo** : `combos-harnais.json` -> `harnais-script-temporaire`
3. **Determiner le type** : test, migration, verification, nettoyage
4. **Choisir le harnais** selon le type

### CREER le script

1. **Isoler** : creer dans /tmp/mecano-<nom>/
2. **Nommer** : `<type>-<sujet>-<AAAAMMJJ>.py` (kebab-case + date)
3. **Ecrire** : code propre, commentaires, gestion d'erreurs
4. **Logger** : enregistrer dans le cahier de dev

### EXECUTER le script

1. **Lancer** : `python3 /tmp/mecano-<nom>/<script>.py`
2. **Capturer** : stdout + stderr
3. **Parser** : resultats (OK/FAIL)
4. **Verifier** : le script a-t-il fait ce qu'il devait faire ?

### VERIFIER le script

1. **Relire le code** : est-il correct ?
2. **Verifier les effets** : le script a-t-il modifie les bons fichiers ?
3. **Verifier l'encodage** : les fichiers modifies sont-ils en UTF-8 + CRLF ?
4. **Comparer AVANT/APRES** : les modifications sont-elles conformes ?

### SUPPRIMER le script

1. **Supprimer** : `rm -rf /tmp/mecano-<nom>/`
2. **Verifier** : le dossier a-t-il ete supprime ?
3. **Logger** : enregistrer la suppression dans le cahier de dev

---

## COMBO : harnais-script-temporaire

> Le combo est defini dans `combos-harnais.json`.
> Les agents v2 sont OBLIGES d'utiliser ce combo pour tout script temporaire.

### Phases du combo

| Phase | Etapes | Signaux |
|---|---|---|
| **ISOLATION** | Creer /tmp/mecano-<nom>/, verifier pas de doublon | SIG OK / SIG ERR |
| **ECRITURE** | Ecrire le script, logger, verifier syntaxe | SIG OK / SIG ERR |
| **LANCEMENT** | Executer, capturer sortie, parser resultats | SIG OK / SIG ERR / SIG CRIT |
| **VALIDATION** | Verifier effets, comparer AVANT/APRES | SIG OK / SIG ERR |
| **SUPPRESSION** | Supprimer /tmp/mecano-<nom>/, logger | SIG OK / SIG ERR |

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Script sans harnais** | Tout script passe par un harnais |
| **Script permanent** | Les scripts temporaires sont SUPPRIMES apres usage |
| **Script dans freelance/ racine** | Les scripts vont dans /tmp/ ou scripts-temp/ |
| **Script sans nom dated** | Toujours kebab-case + AAAAMMJJ |
| **Script sans logger** | Chaque script est trace dans le cahier de dev |
| **Agent v2 sans combo** | Les agents v2 UTILISENT le combo, pas de deviation |

---

## EXEMPLE

### Script de test (harnais-test)

```python
#!/usr/bin/env python3
"""Test rapide de jarvis.py --lister"""
import subprocess, sys

result = subprocess.run(
    ["python3", "cerveau-projet/freelance/tools-commun/jarvis/jarvis.py", "lister", "--agent", "stark"],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("PASS: jarvis.py --lister fonctionne")
    sys.exit(0)
else:
    print(f"FAIL: {result.stderr}")
    sys.exit(1)
```

### Script de migration (harnais-modification)

```python
#!/usr/bin/env python3
"""Migration : renommer un fichier avec backup"""
import shutil, os

src = "source.md"
dst = "destination.md"
backup = f"{src}.bak"

shutil.copy2(src, backup)
os.rename(src, dst)
print(f"Migre: {src} -> {dst} (backup: {backup})")
```

---

## VERIFICATION PAR MECANO

Quand Mecano detecte un script temporaire :
1. **Verifier** qu'il utilise un harnais
2. **Verifier** qu'il est dans le bon emplacement
3. **Verifier** qu'il a ete supprime apres usage
4. **Si non** : signaler a Cerberus (violation du protocole)
