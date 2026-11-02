#!/usr/bin/env python3
"""Review educational JSON Lines access logs using simple, explainable rules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PRIVILEGED_ACTIONS = {"permission_change", "admin_login", "backup_delete", "user_create", "role_change"}


def findings_for(event: dict) -> list[str]:
    findings: list[str] = []
    result = str(event.get("result", "")).lower()
    action = str(event.get("action", "")).lower()
    if result in {"denied", "failure", "failed"}:
        findings.append("acceso_denegado")
    if action in PRIVILEGED_ACTIONS and not (event.get("ticket") or event.get("change_id")):
        findings.append("accion_privilegiada_sin_cambio")
    if action == "bulk_download" or event.get("bulk_download") is True:
        findings.append("descarga_masiva")
    if action == "backup_delete":
        findings.append("borrado_de_respaldo")
    return findings


def audit(path: Path) -> tuple[int, int, list[tuple[int, list[str]]]]:
    total = 0
    malformed = 0
    alerts: list[tuple[int, list[str]]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            total += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                alerts.append((line_number, ["json_invalido"]))
                continue
            if not isinstance(event, dict):
                malformed += 1
                alerts.append((line_number, ["evento_no_es_objeto"]))
                continue
            reasons = findings_for(event)
            if reasons:
                # Do not print raw events: they may carry personal or sensitive data.
                alerts.append((line_number, reasons))
    return total, malformed, alerts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="Archivo JSONL de eventos")
    args = parser.parse_args()
    try:
        total, malformed, alerts = audit(args.log)
    except OSError as error:
        print(f"ERROR: no se pudo leer el archivo: {error}", file=sys.stderr)
        return 2
    print(f"Eventos analizados: {total}; alertas: {len(alerts)}; líneas con formato inválido: {malformed}")
    for line_number, reasons in alerts:
        print(f"Línea {line_number}: {', '.join(reasons)}")
    print("Revisar alertas con el propietario del activo; las reglas no prueban por sí solas una intrusión.")
    return 2 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
