#!/usr/bin/env python3
"""Create and verify a local ZIP backup with a SHA-256 manifest.

This educational utility is not encrypted, cloud-backed, immutable, or intended
to replace a managed enterprise backup product. It never removes old archives
unless --apply-retention is explicitly supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
import sys
import tempfile
import zipfile

EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", "backups"}
MANIFEST_NAME = "MANIFEST.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def collect_files(source: Path) -> list[tuple[Path, str]]:
    if source.is_file():
        if source.is_symlink():
            raise ValueError("No se respaldan enlaces simbólicos.")
        return [(source, source.name)]
    files: list[tuple[Path, str]] = []
    for current, dirs, names in os.walk(source, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name for name in dirs
            if name not in EXCLUDED_DIRS and not (current_path / name).is_symlink()
        ]
        for name in names:
            path = current_path / name
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(source).as_posix()
            files.append((path, relative))
    return sorted(files, key=lambda item: item[1].casefold())


def create_backup(source: Path, destination: Path) -> Path:
    source = source.resolve(strict=True)
    destination = destination.resolve()
    if not source.is_file() and not source.is_dir():
        raise ValueError("La fuente debe ser un archivo o directorio existente.")
    if source.is_dir() and destination == source:
        raise ValueError("La carpeta destino no puede ser la fuente.")
    if source.is_dir() and source in destination.parents:
        raise ValueError("La carpeta destino no puede estar dentro de la fuente.")
    files = collect_files(source)
    if not files:
        raise ValueError("No hay archivos regulares para respaldar.")
    destination.mkdir(parents=True, exist_ok=True)

    created = datetime.now(timezone.utc)
    stamp = created.strftime("%Y%m%d-%H%M%S")
    archive_path = destination / f"backup-{stamp}.zip"
    if archive_path.exists():
        raise FileExistsError(f"Ya existe el respaldo: {archive_path}")
    manifest = {
        "format": 1,
        "created_utc": created.isoformat(timespec="seconds"),
        "source_name": source.name,
        "files": [
            {"path": relative, "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path, relative in files
        ],
    }

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=".backup-", suffix=".tmp", dir=destination, delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path, relative in files:
                archive.write(path, arcname=relative)
            archive.writestr(MANIFEST_NAME, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        os.replace(temporary_path, archive_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    return archive_path


def verify_backup(archive_path: Path) -> tuple[int, int]:
    with zipfile.ZipFile(archive_path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"CRC inválido en el miembro: {bad_member}")
        names = archive.namelist()
        if names.count(MANIFEST_NAME) != 1:
            raise ValueError("El archivo debe incluir exactamente un MANIFEST.json.")
        manifest = json.loads(archive.read(MANIFEST_NAME))
        items = manifest.get("files")
        if not isinstance(items, list):
            raise ValueError("El manifiesto no contiene una lista 'files'.")
        verified = 0
        total_bytes = 0
        for item in items:
            relative = item.get("path", "")
            posix_path = PurePosixPath(relative)
            if not relative or posix_path.is_absolute() or ".." in posix_path.parts:
                raise ValueError(f"Ruta insegura o vacía en el manifiesto: {relative!r}")
            if relative not in names:
                raise ValueError(f"Falta un archivo del manifiesto: {relative}")
            payload = archive.read(relative)
            digest = hashlib.sha256(payload).hexdigest()
            if digest != item.get("sha256"):
                raise ValueError(f"Hash incorrecto: {relative}")
            if len(payload) != item.get("size_bytes"):
                raise ValueError(f"Tamaño incorrecto: {relative}")
            verified += 1
            total_bytes += len(payload)
        return verified, total_bytes


def apply_retention(destination: Path, days: int, now: datetime) -> list[Path]:
    if days < 1:
        raise ValueError("Los días de retención deben ser al menos 1.")
    cutoff = now - timedelta(days=days)
    removed = []
    for candidate in destination.glob("backup-*.zip"):
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc) < cutoff:
            candidate.unlink()
            removed.append(candidate)
    return removed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Archivo o carpeta fuente")
    parser.add_argument("--destination", type=Path, help="Carpeta donde se guardará el ZIP")
    parser.add_argument("--verify", type=Path, help="Verificar un ZIP ya creado")
    parser.add_argument("--retention-days", type=int, help="Edad mínima para eliminar ZIP antiguos")
    parser.add_argument(
        "--apply-retention", action="store_true",
        help="Aplicar borrado de backup-*.zip antiguos (acción destructiva explícita)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.verify:
            if args.source or args.destination or args.apply_retention:
                raise ValueError("--verify no se combina con creación o retención.")
            count, total = verify_backup(args.verify)
            print(f"VERIFICADO: {count} archivo(s), {total} bytes; {args.verify}")
            return 0
        if not args.source or not args.destination:
            raise ValueError("Indique --source y --destination, o utilice --verify.")
        if args.apply_retention and args.retention_days is None:
            raise ValueError("--apply-retention requiere --retention-days.")
        archive = create_backup(args.source, args.destination)
        print(f"CREADO: {archive}")
        count, total = verify_backup(archive)
        print(f"VERIFICADO: {count} archivo(s), {total} bytes")
        if args.retention_days is not None:
            if args.apply_retention:
                removed = apply_retention(args.destination.resolve(), args.retention_days, datetime.now(timezone.utc))
                print(f"RETENCIÓN APLICADA: {len(removed)} respaldo(s) eliminado(s)")
            else:
                cutoff = datetime.now(timezone.utc) - timedelta(days=args.retention_days)
                pending = [p for p in args.destination.glob("backup-*.zip") if p.stat().st_mtime < cutoff.timestamp()]
                print(f"SIMULACIÓN: {len(pending)} respaldo(s) superarían {args.retention_days} días; no se eliminó ninguno.")
                for path in pending:
                    print(f"  candidato: {path}")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
