# Controle - Capture de D9 (historique par agent + tokens-historique.md)

**Agent controleur** : Janus
**Mission controlee** : Redaction de la decision D9 dans proposition-v2.md
**Fichier concerne** : cerveau-projet/freelance/proposition-v2.md
**Date** : 2026-08-21

---

## VERDICT : VALIDE

Non-regression complete : **97/97 OK (0 KO)**, rating test **98.9 EXCELLENT**.
Aucun defaut signale.

---

## 1. Contenu de la mission (CONFORME)

D9 est capturee dans proposition-v2.md :

| Point D9 | Localisation | Verifie |
|---|---|---|
| Journal D9 (section 0) | Ligne 35 | OUI |
| Section 1 probleme historique corrige | Ligne 59 | OUI |
| Arborescence historique/ (3 sous-zones : historique-agents/, registre-usages/, tokens-historique.md) | Lignes 117-122 | OUI |
| Regle Auto-enregistrement (D9) section 6 | Ligne 286 | OUI |
| Sous-section Tokens et activites (D9) | Lignes 288-317 | OUI |

Points cles :
- PAS de trace unique : l'historique.jsonl a disparu de l'arborescence.
- Historique PAR AGENT (comme AGENTS-historique.md en v1).
- Les outils s'enregistrent EUX-MEMES (auto-journalisation des usages).
- tokens-historique.md : activites recentes + tokens consommes/envoyes/recus/en cache.

## 2. Coherence (CONFORME)

- Repond au probleme v1 des 3 sources desynchronisees SANS fusion en une
  trace unique (refus utilisateur respecte) : chaque source a UN role unique.
- L'auto-enregistrement est coherent avec D3 (transparence) : l'agent ne
  declare plus ses usages, l'outil le fait a sa place.
- 0 reference a "1 seule source" ; la seule mention "historique.jsonl" est
  l'explication de la decision (l'utilisateur le refuse).
- Aucune inversion session-admin / session-freelance.

## 3. Validations

| Verification | Resultat |
|---|---|
| Non-regression complete | **97/97 OK (0 KO)** |
| Rating test | **98.9/100 EXCELLENT** |
| Marbre (--tous) | exit 0, 0 divergence |
| evaluer-processus global | 0 probleme |
| ASCII/LF proposition-v2.md | 0 non-ASCII, 0 CRLF |
| Coherence encart/corps AGENTS-historique | 10/10 (aucune heure absente) |
| Audit Themis | CONFORME 0 defaut |
| Structure | Journal D9 + arborescence + regle + sous-section tokens |

## 4. Conclusion

La mission de redaction de D9 est VALIDE : l'historique par agent est
conserve (comme v1), la trace unique est supprimee, les outils s'auto-
enregistrent, et tokens-historique.md suit les activites et les tokens.
La non-regression est verte (97/97). La chaine est bouclee : Cerberus est
reactive avec le bilan consolide.
