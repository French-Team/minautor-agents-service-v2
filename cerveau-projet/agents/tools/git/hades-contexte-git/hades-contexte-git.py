#!/usr/bin/env python3
# -*- coding: ascii -*-
# hades-contexte-git v0.1.0 - caisse a outils git de Hades (Vulcain, M8b)
# Retourne le contexte complet du depot + verdict d anciennete.
import json
import os
import subprocess
import sys

VERSION = "0.1.0"
STATUT = "prepare"
SEUIL_MINUTES = 30  # au-dela : PERIME (regle d anciennete, decision 2026-08-22)


def git(args):
    r = subprocess.run(["git"] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return (r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip())


def main():
    if "--version" in sys.argv:
        print("hades-contexte-git v%s (%s)" % (VERSION, STATUT))
        return 0
    ctx = {}
    code, nom, _ = git(["config", "user.name"])
    ctx["user.name"] = nom if code == 0 else ""
    code, mail, _ = git(["config", "user.email"])
    ctx["user.email"] = mail if code == 0 else ""
    ctx["projet"] = os.path.basename(os.getcwd())
    code, branche, _ = git(["rev-parse", "--abbrev-ref", "HEAD"])
    ctx["branche"] = branche if code == 0 else ""
    code, remote, _ = git(["remote", "get-url", "origin"])
    ctx["remote.origin"] = remote if code == 0 else ""
    code, sha_date_msg, _ = git(
        ["log", "-1", "--pretty=format:%h|%cI|%s"])
    if code == 0 and sha_date_msg:
        sha, date_iso, sujet = sha_date_msg.split("|", 2)
        ctx["dernier.commit.sha"] = sha
        ctx["dernier.commit.date"] = date_iso
        ctx["dernier.commit.sujet"] = sujet
        from datetime import datetime, timezone
        try:
            dt = datetime.fromisoformat(date_iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - dt).total_seconds() / 60.0
            ctx["dernier.commit.age.minutes"] = round(age, 1)
            ctx["anciennete.verdict"] = "RECENT" if age <= SEUIL_MINUTES else "PERIME"
            ctx["anciennete.seuil.minutes"] = SEUIL_MINUTES
            ctx["checkout.autorise"] = (age <= SEUIL_MINUTES)
        except Exception as e:
            ctx["anciennete.verdict"] = "INCONNU (%s)" % e
    else:
        ctx["dernier.commit.sha"] = ""
    code, status_out, _ = git(["status", "--porcelain"])
    lignes = [l for l in status_out.split("\n") if l.strip()] if code == 0 else []
    ctx["fichiers.modifies"] = len(lignes)
    print(json.dumps(ctx, indent=1, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
