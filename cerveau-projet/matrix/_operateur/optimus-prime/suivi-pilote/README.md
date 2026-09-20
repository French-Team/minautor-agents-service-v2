---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# SUIVI DU PILOTE -- le domicile du suivi (chaine PB-003 / SP-003 / TD-003, EO-273)

Ce dossier est INVISIBLE : il vit sous _operateur/optimus-prime/, jamais dans la zone visible.
Un moule ou une vue d ici ne sert donc QUE de l invisible (L-016 : le cameleon ne lit pas cette
zone).

- pannes-declarees.json : LA LISTE FERMEE des pannes du pilote (T1). Pour chaque panne : le fait
  ATTENDU, la source qui le porte, le seuil de silence, la gravite, qui la voit, et la porte qui
  repare. Qui la LIT : la porte du suivi (T2) et son controle permanent (T4). Qui l ECRIT :
  l auditeur du pilote, par la porte d ecriture.
- suivi-pilote.md et suivi-pilote.jsonl (T2, a venir) : la vue DERIVEE et le journal des VERDICTS.
  Aucun fait n y est recopie -- la vue se recalcule depuis les sources : outbox.jsonl,
  suivi-optimus.jsonl, file-missions-optimus.json, entonnoir-files-optimus.json,
  defcon-historique.jsonl et le journal du marbre.

REGLE : une panne qui n est pas declaree dans pannes-declarees.json n existe PAS pour la porte.
La liste est fermee, et elle se modifie par la porte, jamais a la main.
