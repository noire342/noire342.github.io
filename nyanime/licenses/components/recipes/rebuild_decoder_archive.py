#!/usr/bin/env python3
"""Recipient rebuild of the already-patched decoder archive; no Git or app build.

This supplemental recipe deliberately does not change the original attested
recipe. Preparation checks the delivered archive, then permits source edits.
Successful compilation is not evidence of installation or licence compliance.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile

FORMATS = ('JPEG', 'PNG', 'WebP', 'HEIF', 'AVIF', 'JXL')
NDK_VERSION = '27.2.12479018'
SOURCE_PATHS = ('decoder', 'deps/lcms2', 'deps/libjpeg-turbo', 'deps/libpng',
                'deps/libwebp', 'deps/libheif', 'deps/libde265', 'deps/dav1d', 'deps/libjxl')


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def linux_root(root):
    root = root.resolve()
    if os.name != 'posix' or root == Path('/') or root.is_relative_to(Path('/mnt')):
        raise ValueError('Use a new dedicated Linux filesystem directory, outside /mnt')
    return root


def safe_member(name):
    path = PurePosixPath(name)
    if not path.parts or path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('Unsafe source archive path: ' + name)
    return path


def extract_sources(archive, root):
    """Extract regular files first; add only internal links after all file writes."""
    links, names = [], set()
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar:
            relative = safe_member(member.name)
            normalized = relative.as_posix()
            if normalized in names:
                raise ValueError('Duplicate source archive path: ' + normalized)
            names.add(normalized)
            target = root.joinpath(*relative.parts)
            if member.issym() or member.islnk():
                links.append(member)
            elif member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source, target.open('xb') as destination:
                    shutil.copyfileobj(source, destination)
                target.chmod(member.mode & 0o777)
            else:
                raise ValueError('Unsupported source archive entry: ' + member.name)
    for member in links:
        relative = safe_member(member.name)
        target = root.joinpath(*relative.parts)
        if '\\' in member.linkname or PurePosixPath(member.linkname).is_absolute():
            raise ValueError('Unsafe source archive link: ' + member.name)
        linked = (target.parent / member.linkname if member.issym()
                  else root / member.linkname).resolve()
        if not linked.is_relative_to(root.resolve()):
            raise ValueError('Source archive link escapes root: ' + member.name)
        # No link parent may itself redirect a later link outside the new tree.
        if not target.parent.resolve().is_relative_to(root.resolve()):
            raise ValueError('Unsafe link parent: ' + member.name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if member.issym():
            target.symlink_to(member.linkname)
        elif linked.is_file():
            os.link(linked, target)
        else:
            raise ValueError('Missing source hardlink target: ' + member.name)


def source_hashes(root):
    result = {}
    for name in SOURCE_PATHS:
        tree = root / name
        if not tree.is_dir():
            raise ValueError('Missing complete source tree: ' + name)
        for path in sorted(tree.rglob('*')):
            if path.is_file():
                if not path.resolve().is_relative_to(root.resolve()):
                    raise ValueError('Source link escapes root')
                result[path.relative_to(root).as_posix()] = digest(path)
    return result


def prepare(archive, expected_sha256, root):
    actual = digest(archive)
    if actual != expected_sha256.lower():
        raise ValueError('Delivered decoder archive SHA-256 differs from the release record')
    if root.exists():
        raise ValueError('Preserve existing attempts; choose a new extraction root')
    root.mkdir(parents=True)
    extract_sources(archive, root)
    spec = json.loads((root / 'sources.lock.json').read_text())
    if spec['ndkVersion'] != NDK_VERSION or spec['api'] != 21:
        raise ValueError('Unsupported decoder archive toolchain or Android API')
    if tuple(item['path'] for item in spec['sources']) != SOURCE_PATHS:
        raise ValueError('The archive does not contain the complete six-format decoder')
    baseline = {'schemaVersion': 1, 'state': 'archive_extracted_not_rebuilt',
                'archiveSha256': actual, 'sourceLockSha256': digest(root / 'sources.lock.json'),
                'files': source_hashes(root)}
    (root / 'recipient-source-baseline.json').write_text(json.dumps(baseline, indent=2) + '\n')
    return {key: value for key, value in baseline.items() if key != 'files'}


def changes(baseline, current):
    return {'changed': sorted(name for name in baseline.keys() & current.keys()
                              if baseline[name] != current[name]),
            'added': sorted(current.keys() - baseline.keys()),
            'removed': sorted(baseline.keys() - current.keys())}


def run(command, log):
    with log.open('a') as stream:
        stream.write(json.dumps(list(map(str, command))) + '\n')
        stream.flush()
        subprocess.run(list(map(str, command)), check=True, stdout=stream, stderr=subprocess.STDOUT)


def rebuild(root, ndk, jobs=2):
    root, ndk = linux_root(root), ndk.resolve()
    if not 1 <= jobs <= 4:
        raise ValueError('Use one to four workers')
    properties = (ndk / 'source.properties').read_text()
    if not any(line.strip() == 'Pkg.Revision = ' + NDK_VERSION for line in properties.splitlines()):
        raise ValueError('Use Linux NDK r27c, revision ' + NDK_VERSION)
    baseline = json.loads((root / 'recipient-source-baseline.json').read_text())
    if digest(root / 'sources.lock.json') != baseline['sourceLockSha256']:
        raise ValueError('Keep the baseline source lock; modify the library source trees instead')
    output = root / 'build-arm64'
    report_file = root / 'recipient-rebuild.json'
    if output.exists() or report_file.exists():
        raise ValueError('Preserve this attempt and prepare another extraction root')
    for executable in ('cmake', 'meson', 'ninja'):
        if shutil.which(executable) is None:
            raise ValueError('Missing build prerequisite: ' + executable)
    report = {'schemaVersion': 1, 'state': 'recipient_rebuild_started_not_approval',
              'archiveSha256': baseline['archiveSha256'], 'ndkVersion': NDK_VERSION,
              'abi': 'arm64-v8a', 'api': 21, 'formats': list(FORMATS),
              'sourceChanges': changes(baseline['files'], source_hashes(root)),
              'oldBuildAttemptIgnored': (root / 'build-attempt.json').exists(),
              'recipeSha256': digest(Path(__file__)), 'commands': []}
    log = root / 'recipient-rebuild.log'
    report_file.write_text(json.dumps(report, indent=2) + '\n')
    try:
        cpp = root / 'decoder/library/src/main/cpp'
        # Sources in this archive already contain LCMS, CMake directory and 16K
        # changes from the original successful build. Do not reapply any patch.
        toolchain = ndk / 'toolchains/llvm/prebuilt/linux-x86_64/bin'
        cross = root / 'recipient-dav1d-cross.ini'
        cross.write_text(f"""[binaries]
c = '{toolchain}/aarch64-linux-android21-clang'
cpp = '{toolchain}/aarch64-linux-android21-clang++'
ar = '{toolchain}/llvm-ar'
strip = '{toolchain}/llvm-strip'
[properties]
needs_exe_wrapper = true
[host_machine]
system = 'android'
cpu_family = 'aarch64'
cpu = 'aarch64'
endian = 'little'
""")
        dav1d = output / 'dav1d'
        archive = dav1d / 'src/libdav1d.a'
        # Replace the original builder's absolute paths with this extraction's
        # new source/output paths. All other archived source changes are retained.
        (cpp / 'libheif/dav1d.cmake').write_text(f"""set(DAV1D_FOUND 1)
set(DAV1D_LIBRARIES "{archive}")
set(DAV1D_INCLUDE_DIR "{dav1d}" "{dav1d}/include" "{dav1d}/include/dav1d" "{root}/deps/dav1d/include")
""")
        configure = ['cmake', '-S', str(cpp), '-B', str(output), '-G', 'Ninja',
                     f'-DCMAKE_TOOLCHAIN_FILE={ndk}/build/cmake/android.toolchain.cmake',
                     '-DANDROID_ABI=arm64-v8a', '-DANDROID_PLATFORM=android-21',
                     '-DANDROID_STL=c++_shared', '-DANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON',
                     '-DCMAKE_POSITION_INDEPENDENT_CODE=ON', '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON',
                     '-DCMAKE_SHARED_LINKER_FLAGS=-Wl,-z,max-page-size=16384 -Wl,-z,common-page-size=16384',
                     '-DFETCHCONTENT_FULLY_DISCONNECTED=ON']
        configure += [f'-DFETCHCONTENT_SOURCE_DIR_{Path(name).name.upper()}={root / name}'
                      for name in SOURCE_PATHS[1:]]
        configure += [f'-DWITH_{name.upper()}=ON' for name in FORMATS]
        commands = [
            ['meson', 'setup', str(dav1d), str(root / 'deps/dav1d'), '--cross-file', str(cross),
             '--buildtype=release', '--default-library=static', '-Denable_tools=false', '-Denable_tests=false'],
            ['ninja', '-C', str(dav1d), f'-j{jobs}'], configure,
            ['cmake', '--build', str(output), '--target', 'imagedecoder', '--parallel', str(jobs)],
        ]
        report['commands'] = commands
        for index, command in enumerate(commands):
            if index == 2 and not archive.is_file():
                raise ValueError('Freshly compiled dav1d archive missing')
            run(command, log)
        library = output / 'libimagedecoder.so'
        if not library.is_file():
            raise ValueError('Build did not produce the replacement decoder')
        report.update(state='recipient_decoder_built_pending_native_apk_and_device_checks',
                      library=str(library), librarySha256=digest(library),
                      sourceHashesAfterBuild=source_hashes(root))
    except Exception:
        report['state'] = 'recipient_rebuild_failed_preserved_attempt'
        raise
    finally:
        report_file.write_text(json.dumps(report, indent=2) + '\n')
    return {key: value for key, value in report.items() if key != 'sourceHashesAfterBuild'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    extraction = commands.add_parser('prepare', help='Verify and extract before modifying library sources')
    extraction.add_argument('--archive', type=Path, required=True)
    extraction.add_argument('--sha256', required=True)
    extraction.add_argument('--root', type=Path, required=True)
    compilation = commands.add_parser('build', help='Build the already-patched sources; permits recipient edits')
    compilation.add_argument('--root', type=Path, required=True)
    compilation.add_argument('--ndk', type=Path, required=True)
    compilation.add_argument('--jobs', type=int, default=2)
    arguments = parser.parse_args()
    if arguments.command == 'prepare':
        result = prepare(arguments.archive.resolve(), arguments.sha256, linux_root(arguments.root))
    else:
        result = rebuild(arguments.root, arguments.ndk, arguments.jobs)
    print(json.dumps(result, indent=2))
