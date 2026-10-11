#!/usr/bin/env python3
"""Verify ordered parts and reconstruct an unchanged native source archive.

Apache License 2.0; see recipes/LICENSE. This does not extract or build sources.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def reconstruct(manifest_path, component, output=None):
    manifest_path = manifest_path.resolve()
    manifest = json.loads(manifest_path.read_text())
    item = next((entry for entry in manifest["components"] if entry["id"] == component), None)
    if item is None or "archive" not in item:
        raise ValueError("Component has no prepared source archive")
    output = output.resolve() if output else None
    if output and output.exists():
        raise ValueError("Preserve existing files; choose a new output path")
    combined, total = hashlib.sha256(), 0
    stream = output.open("xb") if output else None
    try:
        for part in item["archive"]["parts"]:
            relative = PurePosixPath(part["file"])
            if relative.is_absolute() or ".." in relative.parts or "\\" in part["file"]:
                raise ValueError("Unsafe part path")
            path = manifest_path.parent.joinpath(*relative.parts).resolve()
            if not path.is_relative_to(manifest_path.parent) or not path.is_file():
                raise ValueError("Part path escapes the material directory or is missing")
            part_hash, part_bytes = hashlib.sha256(), 0
            with path.open("rb") as source:
                while chunk := source.read(1024 * 1024):
                    part_hash.update(chunk)
                    combined.update(chunk)
                    part_bytes += len(chunk)
                    total += len(chunk)
                    if stream:
                        stream.write(chunk)
            if part_bytes != part["bytes"] or part_hash.hexdigest() != part["sha256"]:
                raise ValueError("Part bytes/hash mismatch: " + part["file"])
        if total != item["archive"]["bytes"] or combined.hexdigest() != item["archive"]["sha256"]:
            raise ValueError("Combined archive differs from attested source bytes")
    finally:
        if stream:
            stream.close()
    return {"component": component, "bytes": total, "sha256": combined.hexdigest(),
            "state": "archive_reassembled_verified_not_extracted_or_built" if output else "ordered_parts_combined_hash_verified_not_built"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("manifest.json"))
    parser.add_argument("--component", required=True)
    parser.add_argument("--output", type=Path, help="Omit to verify parts/combined bytes without writing an archive")
    args = parser.parse_args()
    print(json.dumps(reconstruct(args.manifest, args.component, args.output), indent=2))
