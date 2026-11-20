#!/usr/bin/env python3
"""Check upstream .deb releases and update PKGBUILD + .SRCINFO if changed."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request

USER_AGENT = "curl/8.7.1"


def write_github_output(kv: dict[str, str]) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        for k, v in kv.items():
            print(f"[output] {k}={v}")
        return
    with open(out_path, "a", encoding="utf-8") as fh:
        for k, v in kv.items():
            if "\n" in v:
                raise ValueError(f"Unexpected newline in output {k}: {v!r}")
            fh.write(f"{k}={v}\n")


def download_file(url: str, dest: pathlib.Path) -> None:
    cmd = [
        "curl",
        "--http1.1",
        "-fsSL",
        "-C",
        "-",
        "--connect-timeout",
        "30",
        "--speed-limit",
        "10240",
        "--speed-time",
        "30",
        "--retry",
        "5",
        "--retry-delay",
        "5",
        "-A",
        USER_AGENT,
        url,
        "-o",
        str(dest),
    ]
    subprocess.run(cmd, check=True)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while chunk := fh.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def dpkg_deb_version(path: pathlib.Path) -> str:
    # First try pure-Python parsing from ar/tar header without external tools
    with open(path, "rb") as fh:
        header_data = fh.read(2 * 1024 * 1024)
    ver = extract_version_from_deb_prefix(header_data)
    if ver:
        return ver

    # Fallback to dpkg-deb if installed
    if shutil.which("dpkg-deb"):
        res = subprocess.run(
            ["dpkg-deb", "-f", str(path), "Version"],
            check=True,
            capture_output=True,
            text=True,
        )
        ver = res.stdout.strip()
        if ver:
            return ver

    raise RuntimeError(f"Could not determine deb version for {path}")


def extract_version_from_deb_prefix(data: bytes) -> str | None:
    """Parse Debian ar header from partial bytes to read Version without full download."""
    if not data.startswith(b"!<arch>\n"):
        return None
    pos = 8
    while pos + 60 <= len(data):
        header = data[pos : pos + 60]
        name = header[0:16].decode("ascii", "ignore").strip().rstrip("/")
        size_str = header[48:58].decode("ascii", "ignore").strip()
        if not size_str.isdigit():
            return None
        size = int(size_str)
        body_start = pos + 60
        body_end = body_start + size
        if name.startswith("control.tar"):
            if body_end > len(data):
                return None
            control_tar = data[body_start:body_end]
            try:
                with tarfile.open(fileobj=io.BytesIO(control_tar), mode="r:*") as tf:
                    for member in tf.getmembers():
                        if member.name in ("control", "./control"):
                            extracted = tf.extractfile(member)
                            if extracted is None:
                                return None
                            text = extracted.read().decode("utf-8", "ignore")
                            m = re.search(r"^Version:\s*(\S+)", text, re.M)
                            return m.group(1) if m else None
            except Exception:
                with tempfile.NamedTemporaryFile(suffix=f"_{name}") as tmp:
                    tmp.write(control_tar)
                    tmp.flush()
                    for member_name in ("./control", "control"):
                        proc = subprocess.run(
                            ["tar", "-xOf", tmp.name, member_name],
                            capture_output=True,
                            text=True,
                        )
                        if proc.returncode == 0 and proc.stdout:
                            m = re.search(r"^Version:\s*(\S+)", proc.stdout, re.M)
                            if m:
                                return m.group(1)
            return None
        pos = body_end + (size % 2)
    return None


def fetch_json(url: str, method: str = "GET", headers: dict[str, str] | None = None, body: bytes | None = None) -> dict:
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_pkgbuild_var(pkgbuild_text: str, var_name: str) -> str:
    m = re.search(rf"^{re.escape(var_name)}=['\"]?([^'\"\n]+)['\"]?$", pkgbuild_text, re.M)
    if not m:
        raise RuntimeError(f"Could not find {var_name}= in PKGBUILD")
    return m.group(1).strip()


def parse_pkgbuild_arch_sha256(pkgbuild_text: str, arch_key: str) -> str:
    m = re.search(
        rf"^{re.escape(arch_key)}=\(\s*'([a-f0-9]{{64}})'\s*\)",
        pkgbuild_text,
        re.M,
    )
    if not m:
        raise RuntimeError(f"Could not find {arch_key} in PKGBUILD")
    return m.group(1)


def update_single_deb_files(
    pkg_dir: pathlib.Path,
    new_ver: str,
    new_rel: str,
    new_sha256: str,
) -> None:
    pkg_name = pkg_dir.name
    pkgbuild_path = pkg_dir / "PKGBUILD"
    srcinfo_path = pkg_dir / ".SRCINFO"

    pkgbuild = pkgbuild_path.read_text(encoding="utf-8")
    srcinfo = srcinfo_path.read_text(encoding="utf-8")

    pkgbuild, n1 = re.subn(r"^pkgver=.*$", f"pkgver={new_ver}", pkgbuild, count=1, flags=re.M)
    pkgbuild, n2 = re.subn(r"^pkgrel=.*$", f"pkgrel={new_rel}", pkgbuild, count=1, flags=re.M)
    pkgbuild, n3 = re.subn(
        r"^(sha256sums_x86_64=\(\s*')[a-f0-9]{64}('\s*\))",
        rf"\g<1>{new_sha256}\g<2>",
        pkgbuild,
        count=1,
        flags=re.M,
    )
    if (n1, n2, n3) != (1, 1, 1):
        raise RuntimeError(f"Failed updating PKGBUILD fields for {pkg_name}: counts={(n1, n2, n3)}")

    srcinfo, s1 = re.subn(r"^\tpkgver = .*$", f"\tpkgver = {new_ver}", srcinfo, count=1, flags=re.M)
    srcinfo, s2 = re.subn(r"^\tpkgrel = .*$", f"\tpkgrel = {new_rel}", srcinfo, count=1, flags=re.M)
    srcinfo, s3 = re.subn(
        rf"\b{re.escape(pkg_name)}-[^\s:]+?((?:-x86_64)?\.deb)\b",
        rf"{pkg_name}-{new_ver}\1",
        srcinfo,
    )
    srcinfo, s4 = re.subn(
        r"^\tsha256sums_x86_64 = [a-f0-9]{64}$",
        f"\tsha256sums_x86_64 = {new_sha256}",
        srcinfo,
        count=1,
        flags=re.M,
    )
    if s1 != 1 or s2 != 1 or s3 < 2 or s4 != 1:
        raise RuntimeError(
            f"Failed updating .SRCINFO fields for {pkg_name}: counts={(s1, s2, s3, s4)}"
        )

    pkgbuild_path.write_text(pkgbuild, encoding="utf-8")
    srcinfo_path.write_text(srcinfo, encoding="utf-8")


def update_qq_files(
    pkg_dir: pathlib.Path,
    new_base_ver: str,
    new_pkgver: str,
    new_rel: str,
    new_url_prefix: str,
    sha_x64: str,
    sha_arm64: str,
    sha_loong64: str,
) -> None:
    pkg_name = pkg_dir.name
    pkgbuild_path = pkg_dir / "PKGBUILD"
    srcinfo_path = pkg_dir / ".SRCINFO"

    pkgbuild = pkgbuild_path.read_text(encoding="utf-8")
    srcinfo = srcinfo_path.read_text(encoding="utf-8")

    pkgbuild, n1 = re.subn(
        r"^_base_pkgver=.*$", f"_base_pkgver={new_base_ver}", pkgbuild, count=1, flags=re.M
    )
    pkgbuild, n2 = re.subn(r"^pkgver=.*$", f"pkgver={new_pkgver}", pkgbuild, count=1, flags=re.M)
    pkgbuild, n3 = re.subn(r"^pkgrel=.*$", f"pkgrel={new_rel}", pkgbuild, count=1, flags=re.M)
    pkgbuild, n4 = re.subn(
        r'^_url_prefix=".*"$', f'_url_prefix="{new_url_prefix}"', pkgbuild, count=1, flags=re.M
    )
    pkgbuild, n5 = re.subn(
        r"^(sha256sums_x86_64=\(\s*')[a-f0-9]{64}('\s*\))",
        rf"\g<1>{sha_x64}\g<2>",
        pkgbuild,
        count=1,
        flags=re.M,
    )
    pkgbuild, n6 = re.subn(
        r"^(sha256sums_aarch64=\(\s*')[a-f0-9]{64}('\s*\))",
        rf"\g<1>{sha_arm64}\g<2>",
        pkgbuild,
        count=1,
        flags=re.M,
    )
    pkgbuild, n7 = re.subn(
        r"^(sha256sums_loong64=\(\s*')[a-f0-9]{64}('\s*\))",
        rf"\g<1>{sha_loong64}\g<2>",
        pkgbuild,
        count=1,
        flags=re.M,
    )
    if (n1, n2, n3, n4, n5, n6, n7) != (1, 1, 1, 1, 1, 1, 1):
        raise RuntimeError(
            f"Failed updating QQ PKGBUILD fields: counts={(n1, n2, n3, n4, n5, n6, n7)}"
        )

    srcinfo, s1 = re.subn(r"^\tpkgver = .*$", f"\tpkgver = {new_pkgver}", srcinfo, count=1, flags=re.M)
    srcinfo, s2 = re.subn(r"^\tpkgrel = .*$", f"\tpkgrel = {new_rel}", srcinfo, count=1, flags=re.M)
    srcinfo, s3 = re.subn(
        rf"^\tnoextract = {re.escape(pkg_name)}-[^\s]+-(amd64|arm64|loongarch64)\.deb$",
        rf"\tnoextract = {pkg_name}-{new_pkgver}-\1.deb",
        srcinfo,
        flags=re.M,
    )
    srcinfo, s4 = re.subn(
        r"^\tsource_x86_64 = .*$",
        f"\tsource_x86_64 = {pkg_name}-{new_pkgver}-amd64.deb::{new_url_prefix}/linuxqq_{new_base_ver}_amd64.deb",
        srcinfo,
        count=1,
        flags=re.M,
    )
    srcinfo, s5 = re.subn(
        r"^\tsha256sums_x86_64 = [a-f0-9]{64}$",
        f"\tsha256sums_x86_64 = {sha_x64}",
        srcinfo,
        count=1,
        flags=re.M,
    )
    srcinfo, s6 = re.subn(
        r"^\tsource_aarch64 = .*$",
        f"\tsource_aarch64 = {pkg_name}-{new_pkgver}-arm64.deb::{new_url_prefix}/linuxqq_{new_base_ver}_arm64.deb",
        srcinfo,
        count=1,
        flags=re.M,
    )
    srcinfo, s7 = re.subn(
        r"^\tsha256sums_aarch64 = [a-f0-9]{64}$",
        f"\tsha256sums_aarch64 = {sha_arm64}",
        srcinfo,
        count=1,
        flags=re.M,
    )
    srcinfo, s8 = re.subn(
        r"^\tsource_loong64 = .*$",
        f"\tsource_loong64 = {pkg_name}-{new_pkgver}-loongarch64.deb::{new_url_prefix}/linuxqq_{new_base_ver}_loongarch64.deb",
        srcinfo,
        count=1,
        flags=re.M,
    )
    srcinfo, s9 = re.subn(
        r"^\tsha256sums_loong64 = [a-f0-9]{64}$",
        f"\tsha256sums_loong64 = {sha_loong64}",
        srcinfo,
        count=1,
        flags=re.M,
    )
    if (s1, s2, s3, s4, s5, s6, s7, s8, s9) != (1, 1, 3, 1, 1, 1, 1, 1, 1):
        raise RuntimeError(
            f"Failed updating QQ .SRCINFO fields: counts={(s1, s2, s3, s4, s5, s6, s7, s8, s9)}"
        )

    pkgbuild_path.write_text(pkgbuild, encoding="utf-8")
    srcinfo_path.write_text(srcinfo, encoding="utf-8")


def run_deb_mode(pkg_dir: pathlib.Path, deb_url: str, force: bool = False) -> None:
    pkg_name = pkg_dir.name
    pkgbuild_text = (pkg_dir / "PKGBUILD").read_text(encoding="utf-8")
    current_ver = parse_pkgbuild_var(pkgbuild_text, "pkgver")
    current_rel = parse_pkgbuild_var(pkgbuild_text, "pkgrel")
    current_sha256 = parse_pkgbuild_arch_sha256(pkgbuild_text, "sha256sums_x86_64")

    # Fast prefix check: fetch deb control archive header (first 256 KiB)
    prefix_ver = None
    try:
        req = urllib.request.Request(
            deb_url,
            headers={"User-Agent": USER_AGENT, "Range": "bytes=0-262143"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            prefix_bytes = resp.read(262144)
        raw_prefix_ver = extract_version_from_deb_prefix(prefix_bytes)
        if raw_prefix_ver:
            prefix_ver = raw_prefix_ver.replace("-", "_")
    except Exception as exc:
        print(f"[{pkg_name}] Prefix range check unavailable ({exc}); proceeding to full check.")

    if prefix_ver is not None:
        print(f"[{pkg_name}] Current:  {current_ver}-{current_rel} ({current_sha256})")
        print(f"[{pkg_name}] Upstream (from control): {prefix_ver}")
        if not force and prefix_ver == current_ver:
            print(f"[{pkg_name}] Already at latest upstream version ({current_ver}). Skipping full download.")
            write_github_output({"has_update": "false"})
            return

    print(f"[{pkg_name}] Downloading upstream package: {deb_url}")
    with tempfile.TemporaryDirectory() as tmpdir:
        deb_path = pathlib.Path(tmpdir) / "upstream.deb"
        download_file(deb_url, deb_path)
        if prefix_ver is not None:
            upstream_ver = prefix_ver
        else:
            raw_ver = dpkg_deb_version(deb_path)
            upstream_ver = raw_ver.replace("-", "_")
        upstream_sha256 = sha256_file(deb_path)

    if prefix_ver is None:
        print(f"[{pkg_name}] Current:  {current_ver}-{current_rel} ({current_sha256})")
        print(f"[{pkg_name}] Upstream: {upstream_ver} ({upstream_sha256})")

    if upstream_ver != current_ver:
        new_ver = upstream_ver
        new_rel = "1"
        commit_msg = f"chore(release): bump {pkg_name} to {new_ver}"
    elif upstream_sha256 != current_sha256:
        new_ver = current_ver
        new_rel = str(int(current_rel) + 1)
        commit_msg = f"fix({pkg_name}): update sha256 checksum for {new_ver}-{new_rel}"
    else:
        print(f"[{pkg_name}] Already at latest upstream version and checksum.")
        write_github_output({"has_update": "false"})
        return

    update_single_deb_files(pkg_dir, new_ver, new_rel, upstream_sha256)
    print(f"[{pkg_name}] Updated PKGBUILD and .SRCINFO -> {new_ver}-{new_rel}")
    write_github_output({"has_update": "true", "commit_msg": commit_msg})


def resolve_qq_upstream() -> tuple[str, str]:
    """Return (base_pkgver, url_prefix) for latest Linux QQ official release."""
    ts = int(time.time() * 1000)
    config_urls = [
        f"https://im.qq.com/proxy/domain/qq-web.cdn-go.cn/im.qq.com_new/latest/rainbow/pcConfig.json?t={ts}",
        f"https://qq-web.cdn-go.cn/im.qq.com_new/latest/rainbow/pcConfig.json?t={ts}",
    ]
    pc_config = None
    last_err = None
    for cu in config_urls:
        try:
            pc_config = fetch_json(cu)
            if pc_config and "Linux" in pc_config:
                break
        except Exception as exc:
            last_err = exc
    if not pc_config or "Linux" not in pc_config:
        raise RuntimeError(f"Failed fetching QQ pcConfig.json: {last_err}")

    x64_deb_url = pc_config["Linux"]["x64DownloadUrl"]["deb"]
    print(f"[tencent-qq] pcConfig x64 deb URL: {x64_deb_url}")

    # Legacy direct linuxqq_<ver>_amd64.deb format
    m_direct = re.match(r"^(https?://.+)/linuxqq_([^_]+)_amd64\.deb$", x64_deb_url)
    if m_direct:
        return m_direct.group(2), m_direct.group(1)

    # Current QQNTV2/<nt_ver>/release/<md5>/QQ_..._amd64_01.deb format
    m_v2 = re.search(r"/QQNTV2/([^/]+)/release/([^/]+)/", x64_deb_url)
    if not m_v2:
        raise RuntimeError(f"Unrecognized QQ x64 deb URL format: {x64_deb_url}")
    nt_ver, md5_prefix = m_v2.group(1), m_v2.group(2)

    sign_resp = fetch_json(
        "https://im.qq.com/http2rpc/gotrpc/noauth/trpc.qqntv2.urlsign.UrlSign/GetSign",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-oidb": json.dumps({"uint32_command": "0x9b8e", "uint32_service_type": 1}),
        },
        body=json.dumps({"url": x64_deb_url}).encode("utf-8"),
    )
    signed_url = (sign_resp.get("data") or {}).get("url")
    if not signed_url:
        raise RuntimeError(f"Failed obtaining signed QQ URL: {sign_resp}")

    # Read control header from first 256 KiB; fall back to full download if needed
    req = urllib.request.Request(
        signed_url,
        headers={"User-Agent": USER_AGENT, "Range": "bytes=0-262143"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        prefix_bytes = resp.read(262144)

    base_pkgver = extract_version_from_deb_prefix(prefix_bytes)
    if not base_pkgver:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_deb = pathlib.Path(tmpdir) / "qq_signed.deb"
            download_file(signed_url, tmp_deb)
            base_pkgver = dpkg_deb_version(tmp_deb)

    url_prefix = f"https://qqdl.gtimg.cn/qqfile/QQNT/{nt_ver}/beta/{md5_prefix}"
    return base_pkgver, url_prefix


def run_qq_mode(pkg_dir: pathlib.Path, force: bool = False) -> None:
    pkg_name = pkg_dir.name
    pkgbuild_text = (pkg_dir / "PKGBUILD").read_text(encoding="utf-8")
    current_ver = parse_pkgbuild_var(pkgbuild_text, "pkgver")
    current_rel = parse_pkgbuild_var(pkgbuild_text, "pkgrel")
    current_url_prefix = parse_pkgbuild_var(pkgbuild_text, "_url_prefix")
    current_sha_x64 = parse_pkgbuild_arch_sha256(pkgbuild_text, "sha256sums_x86_64")

    base_pkgver, url_prefix = resolve_qq_upstream()
    upstream_pkgver = base_pkgver.replace("-", "_")

    print(f"[{pkg_name}] Current:  {current_ver}-{current_rel} (_url_prefix={current_url_prefix})")
    print(f"[{pkg_name}] Upstream: {upstream_pkgver} (_url_prefix={url_prefix})")

    if (
        not force
        and upstream_pkgver == current_ver
        and url_prefix == current_url_prefix
    ):
        print(f"[{pkg_name}] Already at latest upstream version ({current_ver}) and url_prefix. Skipping downloads.")
        write_github_output({"has_update": "false"})
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = pathlib.Path(tmpdir)
        amd64_path = tmp / "amd64.deb"
        amd64_url = f"{url_prefix}/linuxqq_{base_pkgver}_amd64.deb"
        print(f"[{pkg_name}] Downloading amd64 package: {amd64_url}")
        download_file(amd64_url, amd64_path)
        if dpkg_deb_version(amd64_path) != base_pkgver:
            raise RuntimeError("Version mismatch in amd64.deb")
        sha_x64 = sha256_file(amd64_path)
        amd64_path.unlink()

        if (
            not force
            and upstream_pkgver == current_ver
            and url_prefix == current_url_prefix
            and sha_x64 == current_sha_x64
        ):
            print(f"[{pkg_name}] Already at latest upstream version and checksum.")
            write_github_output({"has_update": "false"})
            return

        arm64_path = tmp / "arm64.deb"
        arm64_url = f"{url_prefix}/linuxqq_{base_pkgver}_arm64.deb"
        print(f"[{pkg_name}] Downloading arm64 package: {arm64_url}")
        download_file(arm64_url, arm64_path)
        if dpkg_deb_version(arm64_path) != base_pkgver:
            raise RuntimeError("Version mismatch in arm64.deb")
        sha_arm64 = sha256_file(arm64_path)
        arm64_path.unlink()

        loong64_path = tmp / "loongarch64.deb"
        loong64_url = f"{url_prefix}/linuxqq_{base_pkgver}_loongarch64.deb"
        print(f"[{pkg_name}] Downloading loongarch64 package: {loong64_url}")
        download_file(loong64_url, loong64_path)
        if dpkg_deb_version(loong64_path) != base_pkgver:
            raise RuntimeError("Version mismatch in loongarch64.deb")
        sha_loong64 = sha256_file(loong64_path)
        loong64_path.unlink()

    if upstream_pkgver != current_ver:
        new_rel = "1"
        commit_msg = f"chore(release): bump {pkg_name} to {upstream_pkgver}"
    else:
        new_rel = str(int(current_rel) + 1)
        commit_msg = f"fix({pkg_name}): update sha256 checksums for {upstream_pkgver}-{new_rel}"

    update_qq_files(
        pkg_dir,
        base_pkgver,
        upstream_pkgver,
        new_rel,
        url_prefix,
        sha_x64,
        sha_arm64,
        sha_loong64,
    )
    print(f"[{pkg_name}] Updated PKGBUILD and .SRCINFO -> {upstream_pkgver}-{new_rel}")
    write_github_output({"has_update": "true", "commit_msg": commit_msg})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["deb", "qq"], default="deb")
    parser.add_argument("--pkg-dir", required=True, help="Package directory name")
    parser.add_argument("--deb-url", help="Upstream .deb URL (required for mode=deb)")
    parser.add_argument("--force", action="store_true", help="Force full download and check")
    args = parser.parse_args()

    force = args.force or os.environ.get("FORCE_SYNC", "").lower() in ("true", "1")

    pkg_dir = pathlib.Path(args.pkg_dir)
    if not (pkg_dir / "PKGBUILD").is_file() or not (pkg_dir / ".SRCINFO").is_file():
        print(f"Error: PKGBUILD or .SRCINFO missing in {pkg_dir}", file=sys.stderr)
        return 1

    if args.mode == "deb":
        if not args.deb_url:
            print("Error: --deb-url is required when --mode=deb", file=sys.stderr)
            return 1
        run_deb_mode(pkg_dir, args.deb_url, force=force)
    else:
        run_qq_mode(pkg_dir, force=force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
