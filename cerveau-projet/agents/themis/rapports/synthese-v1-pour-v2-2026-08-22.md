---
identite:
  nom: synthese-v1-pour-v2
  version: 0.1.0
  cree: 2026-08-22
  type: rapport
  appartient_a: themis
  commun: false
  tags: synthese, v1, v2, audit, migration
  session: freelance
# Synthese v1 -> v2 : Ce qui merite d'etre recupere

**Agent** : Themis
**Date** : 2026-08-22
**Mission** : Identifier ce qui merite d'etre recupere de la v1 pour la v2

---

## SYNTHESE GENERALE

La v1 contient **beaucoup de materiel reutilisable**. Voici ce qui merite vraiment d'etre recupere, par priorite.

---

## PRIORITE HAUTE — Indispensable

### 1. Templates de fiches (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| `fiche-agent-template.md` | Modele de fiche d'agent | Deja adapte dans conventions.md (template v2) |
| `corrections-template.md` | Modele de corrections | Deja adapte dans conventions.md |
| `outil-template.md` | Modele d'outil | Deja adapte dans conventions.md (template outil v2) |
| `outil-template.py` | Script de base d'outil | A adapter avec FastMCP |

**Verdict** : Les templates v1 sont la BASE des templates v2. Deja integres.

### 2. Guider-parcours (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| `guider-parcours.py` | Outil qui guide l'agent dans sa carte | A recreer en tant que tool MCP dans JARVIS |
| `spec-guider-parcours.md` | Specification du format parcours | A reutiliser tel quel (format JSON) |

**Verdict** : Le parcours JSON est le MEILLEUR concept de la v1. A conserver. Le script doit devenir un tool MCP.

### 3. Valider-cartes-decision (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| `valider-cartes-decision.py` | Valide la structure des cartes JSON | A recreer en tant que tool MCP |
| Verifications : JSON valide, types, branches, versions | | A reutiliser les memes verifications |

**Verdict** : Indispensable pour la qualite. A migrer en tool MCP.

### 4. Regles immuables (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| `regles-immuables/general/` | Regles fondamentales (cycle, activation, lecons) | A adapter pour la v2 |
| `regles-immuables/marbre/` | Securite du code | A adapter pour JARVIS |
| `protocole-fin-mission.md` | Pattern 8, inter-round | Deja integre dans protocoles.md |

**Verdict** : Les regles fondamentales sont REUTILISABLES. Les protocoles sont deja migrés.

### 5. Lire-fichier (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| `lire-fichier.py` | Lit n'importe quel fichier | A recreer en tool MCP |
| Supporte JSON, Markdown, texte | | A garder |

**Verdict** : Outil de base, indispensable. A migrer en tool MCP.

---

## PRIORITE MOYENNE — Utile

### 6. Combos (v1)
| Combo | Description | Utilite v2 |
|---|---|---|
| `combo-activation` | Active un agent + met a jour AGENTS.md | Remplace par JARVIS activer_agent |
| `combo-creer-agent` | Cree un agent complet (fiche+corrections+parcours) | Utile pour Shuri |
| `combo-audit-themis` | Lance un audit complet | Utile pour les audits |
| `combo-corriger-fichier` | Corrige un fichier | Utile |
| `combo-nettoyage-hygie` | Nettoie le workspace | Utile |
| `catalogue-combos.json` | Liste des combos | A recreer pour la v2 |

**Verdict** : Les combos sont des ORCHESTRATEURS. Utiles mais a simplifier dans la v2 (JARVIS fait l'orchestration).

### 7. Enregistrer-lecon (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| `enregistrer-lecon.py` | Enregistre une lecon dans la BDD | A migrer en tool MCP |
| `consulter-lecons.py` | Consulte les lecons | A migrer en tool MCP |
| `lecons.db` | BDD SQLite des lecons | A reutiliser |

**Verdict** : Le systeme de lecons est EXCELLENT. A migrer tel quel.

### 8. Detecter-ecritures-hors-cycle (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Detecte les ecritures faites hors d'un round | Securite | A recreer en tool MCP |

**Verdict** : Utile pour la securite. A migrer.

### 9. Evaluer-processus (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Verifie qu'un agent respecte les regles | Controle qualite | A migrer en tool MCP |

**Verdict** : Utile pour les audits. A migrer.

### 10. Valider-conformite-ascii (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Verifie l'encodage des fichiers | Controle qualite | A adapter pour UTF-8/CRLF (v2) |

**Verdict** : Utile mais a adapter pour le standard v2 (UTF-8, pas ASCII).

---

## PRIORITE BASSE — Optionnel

### 11. Bumper versions (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Met a jour les versions dans les fichiers | Gestion de version | A migrer si besoin |

**Verdict** : Utile mais pas critique. A migrer plus tard.

### 12. Cartographier (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Genere une vue d'ensemble du cerveau | Cartographie | A migrer si besoin |

**Verdict** : Optionnel. A migrer plus tard.

### 13. Chronometrer (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Chronometre les actions | Metrique | A migrer si besoin |

**Verdict** : Optionnel.

### 14. Proteger/Marbre (v1)
| Element | Description | Adaptation v2 |
|---|---|---|
| Protege les fichiers critiques | Securite | A adapter pour JARVIS |

**Verdict** : Utile mais a repenser pour MCP.

---

## CE QUI NE MERITE PAS D'ETRE RECUPERE

| Element | Pourquoi |
|---|---|
| `activer-agent-principal.py` | Remplace par JARVIS activer_agent |
| `lire-activite-recente.py` | Remplace par JARVIS status_equipe |
| `nettoyer-sessions.py` | Trop specifique a la v1 |
| `convertir-carte-mermaid.py` | Pas utile pour la v2 |
| `valider-relecture.py` | Trop specifique a la v1 |
| `combos-analyse-projet` | Trop specifique a la v1 |
| `combos-audit-general` | Trop specifique a la v1 |

---

## TABLEAU DE MIGRATION

| Outil v1 | Outil v2 | Priorite | Statut |
|---|---|---|---|
| `guider-parcours.py` | JARVIS tool MCP | Haute | A faire |
| `valider-cartes-decision.py` | JARVIS tool MCP | Haute | A faire |
| `lire-fichier.py` | JARVIS tool MCP | Haute | A faire |
| `enregistrer-lecon.py` | JARVIS tool MCP | Moyenne | A faire |
| `consulter-lecons.py` | JARVIS tool MCP | Moyenne | A faire |
| `detecter-ecritures-hors-cycle.py` | JARVIS tool MCP | Moyenne | A faire |
| `evaluer-processus.py` | JARVIS tool MCP | Moyenne | A faire |
| `valider-conformite-ascii.py` | Adapter pour UTF-8 | Moyenne | A faire |
| `activer-agent-principal.py` | JARVIS activer_agent | Haute | FAIT |
| `lire-activite-recente.py` | JARVIS status_equipe | Haute | FAIT |
| `bumper-versions.py` | JARVIS tool MCP | Basse | Plus tard |
| `cartographier.py` | JARVIS tool MCP | Basse | Plus tard |

---

## RECOMMANDATION

**Migrer en priorite** : guider-parcours, valider-cartes, lire-fichier, lecons.
**Deja fait** : activer, status, alertes (JARVIS MCP).
**A repenser** : marbre/protection (adaptation MCP).
**A abandonner** : outils trop specifiques a la v1 (nettoyer-sessions, convertir-mermaid).
