# Nyanime native component source materials

Prepared 11 October 2026 for inspection before publication. These are third-party native source bundles, their original modifications/build recipes and matching notices. This folder is not an application release. It does not provide private Nyanime application source, a content-source catalogue or an app installer.

The immutable original source archives were matched to the local selected-input records. Each archive is delivered as ordered raw binary parts of **at most 48 MiB (50,331,648 bytes)**. Concatenation recreates the original gzip archive exactly; no member, licence, timestamp, test fixture or archived report is rewritten. `manifest.json` gives full and per-part SHA-256 values, byte counts and public upstream revisions. `indexes/` preserves a complete path/type/size/hash index of archive members. `SHA256SUMS.txt` covers the prepared files.

| Component | Original archive bytes | Parts | Original SHA-256 |
| --- | --- | --- | --- |
| Player, arm64, NDK r28c | 130,362,260 | 3 | `2628b2c47998d50f3a43a22cce13775f4320dfa3f6cd26ab57c0ef83666d6d89` |
| Image decoder, arm64, original NDK r27c build | 157,979,172 | 4 | `e8b3077effe962bfab4da4e937bda9039cf66cbd480624b5fc33b71b65a70c72` |
| SQLite Android JNI, arm64, NDK r28c | 5,450,902 | 1 | `12244b35453860694e94f490a7e30c834e926d072833cbed219af9651a82fa1f` |

Individual source trees have their own licences. Broad upstream repositories can contain optional tools or test code under terms different from the code built into the selected native library. Delivery of those source trees is not a claim that every file was compiled into the application or shares one blanket licence.

## Reconstruct the exact source archive

Download this folder's `manifest.json`, `reassemble.py`, and every part of the selected component, preserving the relative `parts/<component>/` directories. Run with Python 3.11 or later:

```sh
python3 reassemble.py --component player-r28c-arm64 --output /tmp/player-r28c-sources.tar.gz
python3 reassemble.py --component image-decoder-arm64 --output /tmp/decoder-sources.tar.gz
python3 reassemble.py --component sqlite-arm64 --output /tmp/sqlite-sources.tar.gz
```

The output directory must exist, and each output filename must be new. The helper checks every part's byte count/hash and the final archive's byte count/hash. On failure, an incomplete output is preserved for diagnosis; do not extract it. Omitting `--output` verifies ordered combined bytes without writing an archive. File concatenation alone does not perform any native compilation or install an application.

## Preserve the source baseline before a rebuild

Use a **new dedicated Linux filesystem directory outside `/mnt`** for each attempt. Existing directories and old reports are preserved. The archived READMEs describe earlier preparation/build stages; the original decoder/SQLite preparation commands are not standalone archive-rebuild instructions. In particular, they can require Git repositories, try to fetch fresh sources, reject already-patched trees or collide with old build records.

The supplemental `recipes/prepare_source_tree.py` verifies the complete archive SHA before extraction. It preserves original provenance, source locks, verification metadata, original build records and previous generated native files under `recipient-baseline/` **before any build**. It records hashes of the initial working sources. Generated ELF programs/objects/libraries are placed in `recipient-baseline/archived-generated/`; they are not offered to the new build as source-tree outputs. Player `verified-config/` and the previous native report are archived separately, preventing the original verifier from colliding with or overwriting them. Source recipes inside the original archive remain unchanged.

The exact player source archive contains public upstream Mbed TLS cryptographic test fixtures and some previously generated files. These are retained in the delivery and identified in the member index. They are not user private keys. Flagged original source/test files were matched byte for byte to Mbed TLS revision `107ea89daaefb9867ea9121002fbbdf926780e98` and its framework submodule revision `94599c0e3b5036e086446a51a3f79640f70f22f6`. The regenerated test header has different complete-file bytes; its 12 PEM key payloads match public fixtures. The recorded diff's encoded data lines match those same public fixtures. Never use these test keys as real credentials.

### Player: archived recipe, NDK r28c

```sh
python3 recipes/prepare_source_tree.py --component player-r28c-arm64 \
  --archive /tmp/player-r28c-sources.tar.gz --root /opt/recipient-player-new
bash /opt/recipient-player-new/rebuild-recipe/build-linux.sh \
  /opt/recipient-player-new /opt/android-ndk-r28c arm64-v8a 1
```

Required NDK revision: `28.2.13676358`. The external Linux host requires Python 3, pkg-config, Meson, Ninja, CMake, make, autoconf/automake/libtool, NASM, gperf and the tools required by the upstream recipes. The locked recipe hashes are verified against the original archived provenance; source edits may be made after preparing the baseline. Do not run `prepare_sources.py` over an extracted/modified source tree. Keep the original baseline evidence when evaluating the new output.

### Decoder: supplemental recipe for already-patched source trees

```sh
python3 recipes/prepare_source_tree.py --component image-decoder-arm64 \
  --archive /tmp/decoder-sources.tar.gz --root /opt/recipient-decoder-new
python3 recipes/rebuild_decoder_archive.py build \
  --root /opt/recipient-decoder-new --ndk /opt/android-ndk-r27c --jobs 1
```

Required NDK revision: `27.2.12479018`; Linux CMake, Meson and Ninja are external prerequisites. The copied supplemental helper is identified and hashed in `manifest.json`; it is outside the immutable original archive. It builds the already-patched six-format sources without Git or fetching dependencies and relocates the original absolute dav1d paths to the new extraction directory. LCMS/CMake/page-size patches are not applied again. The native wrapper is MPL-covered and includes statically linked LGPL-covered libraries; their preferred sources, covered modifications and usable replacement route remain relevant obligations.

### SQLite: optional rebuild of the delivered JNI source

```sh
python3 recipes/prepare_source_tree.py --component sqlite-arm64 \
  --archive /tmp/sqlite-sources.tar.gz --root /opt/recipient-sqlite-new
python3 recipes/rebuild_sqlite_archive.py \
  --root /opt/recipient-sqlite-new --ndk /opt/android-ndk-r28c
```

The supplemental SQLite helper rebases the native command recorded in the original build provenance to the new source/output directories. It keeps the same ABI, API, STL and page-size flags, uses one worker, and preserves a separate attempt report. It uses the delivered SQLite 3.45.0 and already-modified JNI tree rather than re-fetching or reapplying them. SQLite is public-domain software and the Android wrapper is Apache-licensed; this optional source/rebuild offer is not a statement that these permissive licences require an independent rebuild before distribution.

## Libarchive and permissive notices

Libarchive Android 1.1.6 is a selected permissive component. The matched wrapper/native-dependency notice copies are in `notices/libarchive-1.1.6/`. The [official wrapper source revision](https://github.com/zhanghai/libarchive-android/tree/d3ee9c472173fcaf28e737f59dd34ef6cf3d1c88) is provided as an upstream reference. **No local corresponding-source archive is claimed for libarchive.** Native build provenance/submodule-chain checks are separate from retaining its applicable permissive copyright, licence and disclaimer texts. A missing optional source archive is not presented as an LGPL blocker for this component.

The matching notices for the selected NDK r28c C++ runtime are included separately under `notices/cpp-runtime-r28c/`. The original decoder source build used r27c; source bundles and the runtime selected by final application packaging must not be conflated.

## Delivery boundary and checks still pending

This preparation verified immutable source-archive hashes, full member indexes, privacy/source boundaries, notice-copy hashes and part reconstruction. It did not run Gradle, a native build, Android installation or runtime tests. The supplemental extraction/rebuild procedures have been reviewed against the archived scripts; supplying them alone is not proof of a successful new source rebuild.

These bundles contain the native preferred sources and relevant upstream wrapper trees. **Final LGPL Java/DEX replacement materials, donor packaging and application recomposition tooling are still being prepared.** The existence of original Java files in a source tree is not proof that a specific optimized application's Java boundary can be replaced. This page provides no usable-release or completed-relink claim and no substitute for the required covered-library source/object/install materials. A future release record must tie the materials to its exact shipped artefact, notices and replacement procedure.

Supplemental delivery scripts use the existing project Apache License 2.0 copied in `recipes/LICENSE`; the copied decoder helper's origin/hash is retained. No third-party source or library is relicensed by this document. Earlier licences and grants remain applicable.
