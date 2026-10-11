#!/usr/bin/env python3
"""Rebuild SQLite JNI from a prepared archive tree; no Git, Gradle or app build.

Supplemental recipe under Apache License 2.0; see LICENSE. Recipient-invoked
native compilation requires the external pinned Linux NDK. No runtime claim.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


def digest(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def rebuild(root, ndk):
    root, ndk = root.resolve(), ndk.resolve()
    if os.name != "posix" or root == Path("/") or root.is_relative_to(Path("/mnt")):
        raise ValueError("Use a prepared dedicated Linux source directory")
    proof = root / "recipient-baseline"
    baseline = json.loads((proof / "archive-preparation.json").read_text())
    if baseline["component"] != "sqlite-arm64" or baseline["state"] != "source_tree_prepared_not_built":
        raise ValueError("Prepare the attested SQLite archive first")
    provenance = proof / "archived-metadata/provenance.json"
    if digest(root / "provenance.json") != digest(provenance):
        raise ValueError("Preserve original provenance; make edits to library source instead")
    if not any(line.strip() == "Pkg.Revision = 28.2.13676358" for line in (ndk / "source.properties").read_text().splitlines()):
        raise ValueError("Use the pinned Linux NDK r28c")
    native = root / "source/sqlite-android/src/main/jni"
    if "NDK_APP_LIBS_OUT=../jniLibs" in (native / "Application.mk").read_text():
        raise ValueError("The archive lacks the attested upstream output-path change")
    output = root / "recipient-build"
    if output.exists():
        raise ValueError("Preserve previous builds; prepare another source tree")
    output.mkdir()
    command = [str(ndk / "ndk-build"), "-C", str(native), "-j1", "APP_ABI=arm64-v8a",
               "APP_PLATFORM=android-21", "APP_STL=none", "APP_SUPPORT_FLEXIBLE_PAGE_SIZES=true",
               "APP_LDFLAGS=-Wl,-z,max-page-size=16384 -Wl,-z,common-page-size=16384",
               "NDK_OUT=" + str(output / "obj"), "NDK_LIBS_OUT=" + str(output / "libs")]
    current = {path.relative_to(root).as_posix(): digest(path) for path in (root / "source").rglob("*") if path.is_file()}
    original = {name: value for name, value in baseline["workingFileHashesBeforeBuild"].items() if name.startswith("source/")}
    report = {"state": "recipient_sqlite_build_started_not_approval", "archiveSha256": baseline["archiveSha256"],
              "ndkVersion": "28.2.13676358", "abi": "arm64-v8a", "api": 21, "workers": 1,
              "sourceChangesBeforeBuild": {"changed": sorted(name for name in original.keys() & current.keys() if original[name] != current[name]),
                                           "added": sorted(current.keys() - original.keys()), "removed": sorted(original.keys() - current.keys())},
              "command": command, "supplementalRecipeSha256": digest(__file__)}
    result_file = output / "recipient-build.json"
    result_file.write_text(json.dumps(report, indent=2) + "\n")
    try:
        with (output / "build.log").open("w") as log:
            subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
        library = output / "libs/arm64-v8a/libsqlite3x.so"
        report.update(state="recipient_sqlite_built_pending_native_package_and_device_checks", librarySha256=digest(library))
    except Exception:
        report["state"] = "recipient_sqlite_build_failed_preserved_attempt"
        raise
    finally:
        result_file.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--ndk", type=Path, required=True)
    args = parser.parse_args()
    rebuild(args.root, args.ndk)
