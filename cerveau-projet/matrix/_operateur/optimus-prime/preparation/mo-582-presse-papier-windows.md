---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# MO-582 -- PRESSE-PAPIER WINDOWS : OUI, MESURE ET PROUVE

Question du createur (EO-507, deposee le 2026-09-30). Reponse courte :
**oui, et ca marche sans rien installer** -- mais il y a un piege qui
trompe tout le monde.

## 1. LA REPONSE

Oui. Deux facon, et il faut choisir la deuxieme.

**Par `tkinter`** : disponible ici (Tk 8.6). Mais il faut creer une
`Tk()` racine, ce qui ouvre une fenetre, ce qui est lourd et fragile dans
un outil de la Matrice. A ecarter.

**Par l API native `ctypes` (RECOMMANDE)** : `user32` + `kernel32`, deja
presents dans Python, zero dependance, zero fenetre. C est la voie.

## 2. LA PREUVE, EXECUTEE SUR CETTE MACHINE

```
contenu AVANT  : "Les jours sans vent, par calme plat sur l eau, Jeremie s en..."
ecrit          : 'MO-582 preuve presse-papier -- accents : ...'
relu           : 'MO-582 preuve presse-papier -- accents : ...'
ALLER-RETOUR   : OK
ACCENTS INTACTS: OK
restaure       : "Les jours sans vent, par calme plat sur l eau, Jeremie s en..."
```

Le contenu de l operateur est **restaure** apres le test : la preuve ne vole
pas son presse-papier. Les accents font l aller-retour sans degradation.

## 3. LE PIEGE, MESURE ET PAYE

Mon premier cobaye a leve `OSError: access violation writing 0x0`.

Un `HANDLE` Windows fait **64 bits** sur un Python 64 bits. Or `ctypes`
declare `restype = c_int`, soit **32 bits** : le handle est tronque,
`GlobalLock` renvoie 0, et le `memmove` ecrit vers le vide.

Il faut declarer les signatures, sinon le presse-papier n'est pas
"impossible" mais "piege au premier essai" :

```python
k32.GlobalAlloc.restype = wintypes.HGLOBAL
k32.GlobalLock.restype  = ctypes.c_void_p
u32.GetClipboardData.restype = wintypes.HANDLE
u32.SetClipboardData.restype = wintypes.HANDLE
```

## 4. DEUX CONTRAINTES REELLES, NON NEGOCIABLES

- **`OpenClipboard` est EXCLUSIF** : un autre processus le tient -> il faut
  reessayer, pas abandonner au premier echec.
- **`EmptyClipboard` detruit l historique** (Ctrl+V) de l operateur. Pour
  un outil, on ecrit dans le presse-papier a la demande, jamais en
  tache de fond. Mon cobaye sauvegarde puis restaure ; un outil de
  production doit faire pareil.

## 5. CE QUI A ETE FAIT ET CE QUI NE L A PAS ETE

Aucune brique de production creee : la demande est une question, pas une
fonctionnalite. Le cobaye est dans la zone jetable, purgee a la cloture.

Si le createur veut une porte lue dans le parc, la forme est : une fonction
`lire()` / `ecrire(texte)` de 20 lignes pres de `matrice/data/commun/`,
avec les signatures declarees et la restauration. Une porte qui lit le
presse-papier ferait aussi bien le pont entre l'agent et l'editeur du
createur (sortir un chemin de fichier, coller une commande).

## 6. MOYEN DE PREUVE

`.tmp-582/cobaye-clipboard.py` : `ctypes.windll.user32.OpenClipboard` -> 1,
`IsClipboardFormatAvailable(13)` -> 1, aller-retour ecrit/lu identique
accents compris.
