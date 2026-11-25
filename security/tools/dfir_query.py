#!/usr/bin/env python3
"""Fast local DFIR queries for Race-mode Windows disk evidence.

The hot path is intentionally small and lazy-loaded:
- the CLI can run under an unprepared Python and report missing capabilities;
- EWF logical streams that are already NTFS volumes mount directly;
- ordinary partitioned images fall back to dissect.volume disk discovery;
- deleted-file recovery, Registry, EVTX, SQLite, JumpList/raw artifact extraction
  and bounded streaming searches are exposed without requiring a full Target load.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import sqlite3
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Callable, Iterable


PINNED_DISSECT_TARGET = "3.20"
PINNED_DISSECT_ESEDB = "3.18"
DEFAULT_CHUNK_SIZE = 8 * 1024 * 1024
NTFS_OEM_ID = b"NTFS    "
DISSECT_TARGET = "dissect.target"
DISSECT_ESEDB = "dissect.esedb"
# Artifact extractors that need no separate parser once files are reachable.
RAW_ARTIFACT_CAPABILITIES = (
    "jumplist_extract",
    "prefetch_extract",
    "lnk_extract",
    "browser_artifact_extract",
)


class BackendUnavailable(RuntimeError):
    """Raised when the pinned local forensic backend cannot be imported."""


@dataclass
class Backend:
    copen: Callable[..., Any]
    ntfs_filesystem: Callable[..., Any]
    registry_hive: Callable[..., Any]
    evtx: Callable[..., Any]
    disk: Callable[..., Any]
    target_version: str


@dataclass
class ImageContext:
    image: Path
    container: BinaryIO
    fs: object
    layout: str
    partition_index: int | None = None
    physical_size: int | None = None
    container_logical_size: int | None = None


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "missing"


def load_backend() -> Backend:
    try:
        from dissect.eventlog.evtx import Evtx
        from dissect.regf.regf import RegistryHive
        from dissect.target.container import open as copen
        from dissect.target.filesystems.ntfs import NtfsFilesystem
        from dissect.volume.disk import Disk
    except Exception as exc:  # ImportError is not enough for the known Python 3.14 _Globber failure.
        raise BackendUnavailable(f"{type(exc).__name__}: {exc}") from exc
    return Backend(
        copen=copen,
        ntfs_filesystem=NtfsFilesystem,
        registry_hive=RegistryHive,
        evtx=Evtx,
        disk=Disk,
        target_version=_package_version(DISSECT_TARGET),
    )


def load_ese_backend() -> str:
    try:
        import dissect.esedb  # noqa: F401
    except Exception as exc:
        raise BackendUnavailable(
            f"ESE backend import failed: {type(exc).__name__}: {exc}"
        ) from exc
    return _package_version(DISSECT_ESEDB)


def _read_ntfs_signature(handle: BinaryIO) -> bytes:
    handle.seek(0)
    prefix = handle.read(11)
    handle.seek(0)
    return prefix[3:11] if len(prefix) >= 11 else b""


def _stream_size(handle: BinaryIO) -> int | None:
    try:
        current = handle.tell()
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        handle.seek(current)
        return int(size)
    except Exception:
        return None


def open_ntfs_image(image: str | Path, backend: Backend | None = None) -> ImageContext:
    backend = backend or load_backend()
    image_path = Path(image).expanduser().resolve()
    if not image_path.is_file():
        raise ValueError(f"image does not exist: {image_path}")
    container = backend.copen(str(image_path))
    physical_size = image_path.stat().st_size
    logical_size = _stream_size(container)

    if _read_ntfs_signature(container) == NTFS_OEM_ID:
        return ImageContext(
            image=image_path,
            container=container,
            fs=backend.ntfs_filesystem(container),
            layout="direct_ntfs",
            physical_size=physical_size,
            container_logical_size=logical_size,
        )

    try:
        disk = backend.disk(container)
        partitions = list(getattr(disk, "partitions", []) or [])
    except Exception as exc:
        raise ValueError(
            "image is not direct NTFS and volume-system discovery failed: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    for index, partition in enumerate(partitions):
        try:
            stream = partition.open()
            if _read_ntfs_signature(stream) != NTFS_OEM_ID:
                continue
            return ImageContext(
                image=image_path,
                container=container,
                fs=backend.ntfs_filesystem(stream),
                layout="partitioned_ntfs",
                partition_index=index,
                physical_size=physical_size,
                container_logical_size=logical_size,
            )
        except Exception:
            continue
    raise ValueError("no NTFS filesystem was found in the image")


def _jsonable(value):
    if isinstance(value, bytes):
        return value.hex()
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    try:
        return int(value)
    except Exception:
        return str(value)


def _print_json(payload) -> None:
    print(json.dumps(_jsonable(payload), ensure_ascii=False, indent=2))


def sha256_stream(handle: BinaryIO, chunk_size: int = DEFAULT_CHUNK_SIZE) -> str:
    digest = hashlib.sha256()
    while True:
        chunk = handle.read(chunk_size)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def copy_stream(handle: BinaryIO, output: Path, chunk_size: int = DEFAULT_CHUNK_SIZE) -> dict:
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise ValueError(f"refusing to overwrite existing output: {output}")
    digest = hashlib.sha256()
    total = 0
    with output.open("wb") as dst:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)
            digest.update(chunk)
            total += len(chunk)
    return {"output": str(output), "size": total, "sha256": digest.hexdigest()}


def _collect_needle_hits(
    data: bytes,
    base: int,
    label: str,
    needle: bytes,
    hits: list[dict],
    seen: set[tuple[str, int]],
    max_hits: int,
) -> None:
    """Append unseen occurrences of needle in data to hits, up to max_hits."""
    start = 0
    while len(hits) < max_hits:
        idx = data.find(needle, start)
        if idx < 0:
            break
        offset = base + idx
        key = (label, offset)
        if key not in seen:
            seen.add(key)
            hits.append({"encoding": label, "offset": offset})
        start = idx + 1


def stream_search(
    handle: BinaryIO,
    needles: Iterable[tuple[str, bytes]],
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_hits: int = 100,
) -> list[dict]:
    compiled = [(label, needle) for label, needle in needles if needle]
    if not compiled:
        raise ValueError("at least one non-empty search needle is required")
    if max_hits <= 0:
        raise ValueError("max_hits must be positive")
    overlap = max(len(needle) for _, needle in compiled) - 1
    handle.seek(0)
    absolute_read = 0
    tail = b""
    hits: list[dict] = []
    seen: set[tuple[str, int]] = set()
    while len(hits) < max_hits:
        chunk = handle.read(chunk_size)
        if not chunk:
            break
        data = tail + chunk
        base = absolute_read - len(tail)
        for label, needle in compiled:
            _collect_needle_hits(data, base, label, needle, hits, seen, max_hits)
        absolute_read += len(chunk)
        tail = data[-overlap:] if overlap > 0 else b""
    return sorted(hits, key=lambda row: (row["offset"], row["encoding"]))


def _mft_record_size(fs) -> int:
    raw = int(fs.ntfs.boot_sector.ClustersPerFileRecordSegment)
    if raw < 0:
        return 1 << (-raw)
    return raw * int(fs.ntfs.cluster_size)


def _record_summary(record) -> dict:
    size = None
    try:
        size = int(record.size())
    except Exception:
        pass
    path = None
    try:
        path = record.full_path()
    except Exception:
        pass
    return {
        "record": int(record.segment),
        "offset": int(getattr(record, "offset", 0)),
        "filename": str(getattr(record, "filename", "") or ""),
        "full_path": path,
        "size": size,
        "flags": int(getattr(getattr(record, "header", None), "Flags", 0)),
        "deleted": int(getattr(getattr(record, "header", None), "Flags", 0)) == 0,
    }


def find_mft_filename(fs, name: str, *, max_hits: int = 50) -> list[dict]:
    encoded = name.encode("utf-16le")
    record_size = _mft_record_size(fs)
    raw_hits = stream_search(
        fs.ntfs.mft.fh,
        [("utf16le", encoded)],
        max_hits=max_hits,
    )
    rows: list[dict] = []
    for hit in raw_hits:
        record_number = int(hit["offset"]) // record_size
        row = {
            "mft_byte_offset": int(hit["offset"]),
            "candidate_record": record_number,
            "record_size": record_size,
        }
        try:
            row.update(_record_summary(fs.ntfs.mft.get(record_number)))
        except Exception as exc:
            row["record_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


REGISTRY_HIVE_NAMES = {"SYSTEM", "SOFTWARE", "SAM", "SECURITY", "DEFAULT", "NTUSER.DAT", "USRCLASS.DAT"}


def _count_artifact_signals(signals: dict[str, int], upper_name: str, suffix: str) -> None:
    """Increment the artifact signal counters matched by one file."""
    if upper_name in REGISTRY_HIVE_NAMES:
        signals["registry_hives"] += 1
    if suffix == ".evtx":
        signals["evtx"] += 1
    if suffix == ".lnk":
        signals["lnk"] += 1
    if upper_name.endswith((".AUTOMATICDESTINATIONS-MS", ".CUSTOMDESTINATIONS-MS")):
        signals["jumplist"] += 1
    if suffix == ".pf":
        signals["prefetch"] += 1
    if upper_name == "SRUDB.DAT":
        signals["srum"] += 1
    if upper_name == "WINDOWS.EDB":
        signals["windows_search"] += 1
    if suffix in {".sqlite", ".sqlite3", ".db"}:
        signals["sqlite"] += 1


def _inventory_evidence_root(root: Path) -> dict:
    if not root.is_dir():
        raise ValueError(f"evidence root does not exist or is not a directory: {root}")
    suffix_counts: dict[str, int] = {}
    basename_counts: dict[str, int] = {}
    total_size = 0
    file_count = 0
    signals = {
        "registry_hives": 0,
        "evtx": 0,
        "lnk": 0,
        "jumplist": 0,
        "prefetch": 0,
        "srum": 0,
        "windows_search": 0,
        "sqlite": 0,
    }
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        file_count += 1
        try:
            total_size += path.stat().st_size
        except OSError:
            pass
        suffix = path.suffix.casefold() or "<none>"
        suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1
        upper_name = path.name.upper()
        basename_counts[upper_name] = basename_counts.get(upper_name, 0) + 1
        _count_artifact_signals(signals, upper_name, suffix)
    return {
        "path": str(root),
        "file_count": file_count,
        "total_size": total_size,
        "suffix_counts": dict(sorted(suffix_counts.items())),
        "artifact_signals": signals,
        "stage_required": False,
    }


def _probe_image(result: dict, image: str | Path, backend: Backend) -> None:
    """Open the image and record its layout and capabilities into result."""
    try:
        ctx = open_ntfs_image(image, backend)
        result["image"] = {
            "path": str(ctx.image),
            "container": type(ctx.container).__name__,
            "layout": ctx.layout,
            "partition_index": ctx.partition_index,
            "physical_size": ctx.physical_size,
            "container_logical_size": ctx.container_logical_size,
            "stage_required": False,
        }
        result["capabilities"]["ewf_open"] = True
        result["capabilities"]["ntfs"] = True
        result["capabilities"]["deleted_mft"] = hasattr(ctx.fs.ntfs, "mft")
        # These artifact types need no separate mount/parser to be immediately
        # extracted or stream-searched once NTFS is available.
        for key in RAW_ARTIFACT_CAPABILITIES:
            result["capabilities"][key] = True
        try:
            result["image"]["root_entries_sample"] = list(ctx.fs.listdir("/"))[:20]
        except Exception as exc:
            result["errors"].append(f"NTFS root listing failed: {type(exc).__name__}: {exc}")
        result["image"]["artifact_signals"] = _image_ese_signals(ctx)
    except Exception as exc:
        result["errors"].append(f"image open failed: {type(exc).__name__}: {exc}")


def _image_ese_signals(ctx: ImageContext) -> dict[str, int]:
    """Report which ESE-backed artifacts exist inside the mounted image."""
    image_signals = {"srum": 0, "windows_search": 0}
    for signal, artifact_path in (
        ("srum", "/Windows/System32/SRU/SRUDB.dat"),
        (
            "windows_search",
            "/ProgramData/Microsoft/Search/Data/Applications/Windows/Windows.edb",
        ),
    ):
        try:
            ctx.fs.stat(artifact_path)
            image_signals[signal] = 1
        except Exception:
            pass
    return image_signals


def _probe_evidence_root(result: dict, evidence_root: str | Path) -> None:
    """Inventory an extracted evidence directory into result."""
    try:
        root = Path(evidence_root).expanduser().resolve()
        result["evidence_root"] = _inventory_evidence_root(root)
        for key in RAW_ARTIFACT_CAPABILITIES:
            result["capabilities"][key] = True
    except Exception as exc:
        result["errors"].append(
            f"evidence root inventory failed: {type(exc).__name__}: {exc}"
        )


def _required_capabilities(
    result: dict,
    image: str | Path | None,
    evidence_root: str | Path | None,
) -> tuple[list[str], bool]:
    """Return the capabilities the run needs and whether ESE parsing is needed."""
    required = [
        "registry",
        "evtx",
        "sqlite",
        "stream_search",
    ]
    if image is not None:
        required.extend(["ewf_open", "ntfs", "deleted_mft", *RAW_ARTIFACT_CAPABILITIES])
        signals = result.get("image", {}).get("artifact_signals", {})
    elif evidence_root is not None:
        required.extend(RAW_ARTIFACT_CAPABILITIES)
        signals = result.get("evidence_root", {}).get("artifact_signals", {})
    else:
        return required, False
    return required, bool(signals.get("srum") or signals.get("windows_search"))


def _check_ese(result: dict, ese_version: str, ese_error: str) -> None:
    """Record an error when the needed ESE parser is missing or unpinned."""
    if not result["capabilities"]["ese"]:
        result["errors"].append(
            "ESE parser required by SRUM/Windows Search artifacts but unavailable: "
            + (ese_error or "unknown import failure")
        )
    elif ese_version != PINNED_DISSECT_ESEDB:
        result["errors"].append(
            f"dissect.esedb version {ese_version!r} is not pinned known-good "
            f"{PINNED_DISSECT_ESEDB!r}"
        )


def preflight(
    image: str | Path | None = None,
    evidence_root: str | Path | None = None,
) -> dict:
    if image is not None and evidence_root is not None:
        raise ValueError("preflight accepts either image or evidence_root, not both")
    started = time.perf_counter()
    result = {
        "ready": False,
        "python": sys.version.split()[0],
        "requirements": {
            DISSECT_TARGET: _package_version(DISSECT_TARGET),
            DISSECT_ESEDB: _package_version(DISSECT_ESEDB),
            "colorama": _package_version("colorama"),
            "sqlite3": sqlite3.sqlite_version,
        },
        "capabilities": {
            "ewf_open": False,
            "ntfs": False,
            "deleted_mft": False,
            "registry": False,
            "evtx": False,
            "ese": False,
            "sqlite": True,
            "stream_search": True,
            "jumplist_extract": False,
            "prefetch_extract": False,
            "lnk_extract": False,
            "browser_artifact_extract": False,
        },
        "errors": [],
    }
    try:
        backend = load_backend()
        result["requirements"][DISSECT_TARGET] = backend.target_version
        result["capabilities"]["registry"] = True
        result["capabilities"]["evtx"] = True
    except BackendUnavailable as exc:
        result["errors"].append(f"backend import failed: {exc}")
        result["elapsed_seconds"] = time.perf_counter() - started
        return result

    if backend.target_version != PINNED_DISSECT_TARGET:
        result["errors"].append(
            f"dissect.target version {backend.target_version!r} is not pinned known-good "
            f"{PINNED_DISSECT_TARGET!r}"
        )

    ese_error = ""
    try:
        ese_version = load_ese_backend()
        result["requirements"][DISSECT_ESEDB] = ese_version
        result["capabilities"]["ese"] = True
    except BackendUnavailable as exc:
        ese_version = "missing"
        ese_error = str(exc)

    if image is not None:
        _probe_image(result, image, backend)
    elif evidence_root is not None:
        _probe_evidence_root(result, evidence_root)

    required, ese_needed = _required_capabilities(result, image, evidence_root)
    if ese_needed:
        required.append("ese")
        _check_ese(result, ese_version, ese_error)
    result["ready"] = (
        not result["errors"]
        and all(bool(result["capabilities"].get(name)) for name in required)
    )
    result["elapsed_seconds"] = time.perf_counter() - started
    return result


def _ctx(args) -> ImageContext:
    return open_ntfs_image(args.image)


def command_preflight(args: argparse.Namespace) -> int:
    result = preflight(
        getattr(args, "image", None),
        getattr(args, "evidence_root", None),
    )
    _print_json(result)
    return 0 if result["ready"] else 2


def command_info(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    payload = {
        "image": str(ctx.image),
        "container": type(ctx.container).__name__,
        "layout": ctx.layout,
        "partition_index": ctx.partition_index,
        "physical_size": ctx.physical_size,
        "container_logical_size": ctx.container_logical_size,
        "volume_name": _jsonable(getattr(ctx.fs.ntfs, "volume_name", None)),
        "cluster_size": int(ctx.fs.ntfs.cluster_size),
        "sector_size": int(ctx.fs.ntfs.sector_size),
        "mft_record_size": _mft_record_size(ctx.fs),
    }
    _print_json(payload)
    return 0


def command_list(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    _print_json({"path": args.path, "entries": list(ctx.fs.listdir(args.path))})
    return 0


def command_glob(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    rows = []
    for entry in ctx.fs.glob(args.pattern):
        rows.append(str(entry))
        if len(rows) >= args.max_results:
            break
    _print_json({"pattern": args.pattern, "matches": rows})
    return 0


def command_stat(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    stat = ctx.fs.stat(args.path)
    payload = {
        "path": args.path,
        "size": int(stat.st_size),
        "inode": int(stat.st_ino),
        "mode": int(stat.st_mode),
        "mtime_ns": int(stat.st_mtime_ns),
        "ctime_ns": int(stat.st_ctime_ns),
        "birthtime_ns": int(getattr(stat, "st_birthtime_ns", 0)),
    }
    _print_json(payload)
    return 0


def command_extract(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    with ctx.fs.open(args.path) as handle:
        result = copy_stream(handle, Path(args.output))
    result["source"] = args.path
    _print_json(result)
    return 0


def command_find_mft(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    _print_json({
        "name": args.name,
        "matches": find_mft_filename(ctx.fs, args.name, max_hits=args.max_hits),
    })
    return 0


def command_recover_mft(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    record = ctx.fs.ntfs.mft.get(args.record)
    summary = _record_summary(record)
    try:
        handle = record.open()
    except Exception as exc:
        raise ValueError(
            f"MFT record {args.record} has no recoverable unnamed DATA stream: "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    with handle:
        result = copy_stream(handle, Path(args.output))
    _print_json({**summary, **result})
    return 0


def command_search_file(args: argparse.Namespace) -> int:
    ctx = _ctx(args)
    encodings = []
    if args.encoding in {"ascii", "both"}:
        encodings.append(("ascii", args.needle.encode("utf-8")))
    if args.encoding in {"utf16le", "both"}:
        encodings.append(("utf16le", args.needle.encode("utf-16le")))
    started = time.perf_counter()
    with ctx.fs.open(args.path) as handle:
        hits = stream_search(
            handle,
            encodings,
            chunk_size=args.chunk_size_mib * 1024 * 1024,
            max_hits=args.max_hits,
        )
    _print_json({
        "path": args.path,
        "needle": args.needle,
        "hits": hits,
        "hit_count": len(hits),
        "elapsed_seconds": time.perf_counter() - started,
    })
    return 0


def command_registry_get(args: argparse.Namespace) -> int:
    backend = load_backend()
    ctx = open_ntfs_image(args.image, backend)
    with ctx.fs.open(args.hive) as handle:
        hive = backend.registry_hive(handle)
        key = hive.open(args.key)
        if args.value:
            value = key.value(args.value)
            payload = {
                "hive": args.hive,
                "key": args.key,
                "name": args.value,
                "type": _jsonable(value.type),
                "value": _jsonable(value.value),
            }
        else:
            payload = {
                "hive": args.hive,
                "key": args.key,
                "values": [
                    {
                        "name": str(value.name),
                        "type": _jsonable(value.type),
                        "value": _jsonable(value.value),
                    }
                    for value in key.values()
                ],
            }
    _print_json(payload)
    return 0


def _event_to_dict(event) -> dict:
    return {str(key): _jsonable(value) for key, value in event.items()}


def _evtx_row_matches(row: dict, record_id: int | None, needle: str) -> bool:
    """Apply the --record-id and --needle filters to one decoded event."""
    if record_id is not None:
        try:
            if int(row.get("EventRecordID", -1)) != record_id:
                return False
        except Exception:
            return False
    if needle:
        searchable = json.dumps(row, ensure_ascii=False, default=str).casefold()
        if needle not in searchable:
            return False
    return True


def command_evtx(args: argparse.Namespace) -> int:
    backend = load_backend()
    ctx = open_ntfs_image(args.image, backend)
    needle = (args.needle or "").casefold()
    rows = []
    with ctx.fs.open(args.path) as handle:
        for event in backend.evtx(handle):
            row = _event_to_dict(event)
            if not _evtx_row_matches(row, args.record_id, needle):
                continue
            rows.append(row)
            if len(rows) >= args.max_events:
                break
    _print_json({"path": args.path, "events": rows, "count": len(rows)})
    return 0


def command_sqlite(args: argparse.Namespace) -> int:
    database = Path(args.database).expanduser().resolve()
    if not database.is_file():
        raise ValueError(f"SQLite file does not exist: {database}")
    uri = f"file:{database.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        cursor = connection.execute(args.sql)
        columns = [item[0] for item in (cursor.description or [])]
        rows = cursor.fetchmany(args.max_rows)
    _print_json({"database": str(database), "columns": columns, "rows": rows})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fast Race-mode Windows DFIR evidence queries")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("preflight", help="Fail-fast capability check before the Race clock starts")
    source = p.add_mutually_exclusive_group()
    source.add_argument("--image")
    source.add_argument("--evidence-root")
    p.set_defaults(func=command_preflight)

    def image_cmd(name: str, help_text: str):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("--image", required=True)
        return cmd

    p = image_cmd("info", "Show image/container/NTFS facts")
    p.set_defaults(func=command_info)
    p = image_cmd("list", "List one NTFS directory")
    p.add_argument("--path", required=True)
    p.set_defaults(func=command_list)
    p = image_cmd("glob", "Glob NTFS paths")
    p.add_argument("--pattern", required=True)
    p.add_argument("--max-results", type=int, default=200)
    p.set_defaults(func=command_glob)
    p = image_cmd("stat", "Stat one NTFS path")
    p.add_argument("--path", required=True)
    p.set_defaults(func=command_stat)
    p = image_cmd("extract", "Extract one live NTFS path and hash it")
    p.add_argument("--path", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_extract)
    p = image_cmd("find-mft", "Find UTF-16 filename occurrences in raw $MFT")
    p.add_argument("--name", required=True)
    p.add_argument("--max-hits", type=int, default=50)
    p.set_defaults(func=command_find_mft)
    p = image_cmd("recover-mft", "Recover the unnamed DATA stream from an MFT segment")
    p.add_argument("--record", required=True, type=int)
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_recover_mft)
    p = image_cmd("search-file", "Bounded streaming ASCII/UTF-16LE search inside one artifact")
    p.add_argument("--path", required=True)
    p.add_argument("--needle", required=True)
    p.add_argument("--encoding", choices=["ascii", "utf16le", "both"], default="both")
    p.add_argument("--max-hits", type=int, default=100)
    p.add_argument("--chunk-size-mib", type=int, default=8)
    p.set_defaults(func=command_search_file)
    p = image_cmd("registry-get", "Read a key/value directly from a Registry hive in the image")
    p.add_argument("--hive", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--value", default="")
    p.set_defaults(func=command_registry_get)
    p = image_cmd("evtx", "Search or select events directly from an EVTX in the image")
    p.add_argument("--path", required=True)
    p.add_argument("--needle", default="")
    p.add_argument("--record-id", type=int)
    p.add_argument("--max-events", type=int, default=20)
    p.set_defaults(func=command_evtx)

    p = sub.add_parser("sqlite", help="Run a bounded read-only query against a recovered SQLite file")
    p.add_argument("--database", required=True)
    p.add_argument("--sql", required=True)
    p.add_argument("--max-rows", type=int, default=100)
    p.set_defaults(func=command_sqlite)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (BackendUnavailable, OSError, ValueError, sqlite3.Error) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
