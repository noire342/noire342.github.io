#!/usr/bin/env python3
"""Prepare a fresh Linux source tree and preserve archive baselines; no build.

Supplemental delivery helper under Apache License 2.0 (see LICENSE).
Original archives and archived recipes are never rewritten.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import tarfile

EXPECTED = {
    "player-r28c-arm64": "2628b2c47998d50f3a43a22cce13775f4320dfa3f6cd26ab57c0ef83666d6d89",
    "image-decoder-arm64": "e8b3077effe962bfab4da4e937bda9039cf66cbd480624b5fc33b71b65a70c72",
    "sqlite-arm64": "12244b35453860694e94f490a7e30c834e926d072833cbed219af9651a82fa1f",
}
def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def safe(name):
    path = PurePosixPath(name)
    if not path.parts or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError("Unsafe archive path: " + name)
    return path


def prepare(archive, component, root):
    if os.name != "posix":
        raise ValueError("Extract for rebuilding on a Linux filesystem")
    root = root.resolve()
    if root == Path("/") or root.is_relative_to(Path("/mnt")) or root.exists():
        raise ValueError("Choose a new dedicated Linux directory outside /mnt; preserve previous attempts")
    actual = digest(archive)
    if actual != EXPECTED[component]:
        raise ValueError("Archive SHA-256 differs from the delivery record")
    root.mkdir(parents=True)
    proof = root / "recipient-baseline"
    proof.mkdir()
    records, names, links, retained_hashes = [], set(), [], {}
    compiled = re.compile(r"\.(?:o|a|lo|la|so(?:\.\d+)*)$")
    with tarfile.open(archive, "r|gz") as tar:
        for member in tar:
            relative = safe(member.name)
            name = relative.as_posix()
            if name in names:
                raise ValueError("Duplicate archive path: " + name)
            names.add(name)
            if relative.parts[0] == "recipient-baseline":
                raise ValueError("Archive collides with recipient proof directory")
            old_metadata = (relative.parts[0] == "verified-config" or
                            relative.name.startswith("native-verification-") and relative.suffix == ".json" or
                            name in {"build-attempt.json", "build-result.json"})
            old_output = compiled.search(relative.name) or any(part in {".libs", ".deps"} for part in relative.parts)
            target = root.joinpath(*relative.parts)
            kind = "directory" if member.isdir() else "file" if member.isfile() else "symlink" if member.issym() else "hardlink" if member.islnk() else "unsupported"
            row = {"path": name, "kind": kind, "bytes": member.size}
            if member.isdir():
                target = proof / "archived-metadata" / name if old_metadata else target
                target.mkdir(parents=True, exist_ok=True)
            elif member.issym() or member.islnk():
                linked = safe(member.linkname) if member.islnk() else PurePosixPath(member.linkname)
                resolved = posixpath.normpath(posixpath.join(str(relative.parent), member.linkname) if member.issym() else member.linkname)
                if linked.is_absolute() or "\\" in member.linkname or safe(resolved).parts[0] != relative.parts[0]:
                    raise ValueError("Source link escapes its source tree")
                links.append((member, relative, resolved))
                row["linkTarget"] = member.linkname
            elif member.isfile():
                with tar.extractfile(member) as source:
                    first = source.read(4)
                    # ELF executables without suffix are old generated outputs too.
                    old_output = bool(old_output or first == b"\x7fELF")
                    if old_output:
                        target = proof / "archived-generated" / name
                        row["preservedAs"] = target.relative_to(root).as_posix()
                    elif old_metadata:
                        target = proof / "archived-metadata" / name
                        row["preservedAs"] = target.relative_to(root).as_posix()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    hashed = hashlib.sha256()
                    with target.open("xb") as output:
                        output.write(first)
                        hashed.update(first)
                        while chunk := source.read(1024 * 1024):
                            output.write(chunk)
                            hashed.update(chunk)
                    row["sha256"] = hashed.hexdigest()
                target.chmod(member.mode & 0o777)
                if not old_output and not old_metadata:
                    retained_hashes[name] = row["sha256"]
                if name in {"provenance.json", "sources.lock.json", "dav1d-android-cross.ini"}:
                    copied = proof / "archived-metadata" / name
                    copied.parent.mkdir(parents=True, exist_ok=True)
                    copied.write_bytes(target.read_bytes())
            else:
                raise ValueError("Unsupported archive entry: " + name)
            records.append(row)
    link_names = {relative.as_posix() for _, relative, _ in links}
    if any(any(parent.as_posix() in link_names for parent in PurePosixPath(name).parents) for name in names):
        raise ValueError("Archive path descends through a link")
    for member, relative, resolved in links:
        target = root.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        source = root.joinpath(*PurePosixPath(resolved).parts)
        if not target.parent.resolve().is_relative_to(root) or not source.resolve().is_relative_to(root):
            raise ValueError("Link resolution escapes recipient directory")
        if member.issym():
            target.symlink_to(member.linkname)
        elif source.is_file():
            os.link(source, target)
        else:
            raise ValueError("Missing source hardlink target")
    if component == "player-r28c-arm64":
        provenance = json.loads((root / "provenance.json").read_text())
        if digest(root / "sources.lock.json") != provenance["lockSha256"]:
            raise ValueError("Archived source-lock hash differs")
        for name, expected in provenance["recipeHashes"].items():
            if digest(root / "rebuild-recipe" / name) != expected:
                raise ValueError("Archived build recipe differs: " + name)
    if component == "image-decoder-arm64":
        source_files = {path.relative_to(root).as_posix(): digest(path)
                        for name in ("decoder", "deps") for path in (root / name).rglob("*") if path.is_file()}
        baseline = {"schemaVersion": 1, "state": "archive_extracted_not_rebuilt", "archiveSha256": actual,
                    "sourceLockSha256": digest(root / "sources.lock.json"), "files": source_files}
        (root / "recipient-source-baseline.json").write_text(json.dumps(baseline, indent=2) + "\n")
        (proof / "recipient-source-baseline.json").write_text(json.dumps(baseline, indent=2) + "\n")
    report = {"component": component, "state": "source_tree_prepared_not_built", "archiveSha256": actual,
              "archiveEntries": len(records), "originalEntries": records, "workingFileHashesBeforeBuild": retained_hashes,
              "preservedOldOutputs": sum("archived-generated/" in item.get("preservedAs", "") for item in records),
              "metadataPreservedBeforeBuild": True, "archivedRecipesModified": False}
    (proof / "archive-preparation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key not in {"originalEntries", "workingFileHashesBeforeBuild"}}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component", choices=EXPECTED, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.archive.resolve(), args.component, args.root)
