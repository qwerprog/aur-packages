# aur-packages

[简体中文](./README.md)

Personal Arch User Repository (AUR) packages collection maintained by Chapman ([@qwerprog](https://github.com/qwerprog)).

This monorepo manages PKGBUILDs and runtime wrappers for packages maintained on the Arch User Repository, featuring automated upstream version checking, native Wayland optimization, and lightweight Bubblewrap security sandboxing.

---

## Packages Overview

| Package | Version | AUR Link | Features & Highlights |
| :--- | :--- | :--- | :--- |
| **[tencent-wechat](./tencent-wechat)** | ![AUR version](https://img.shields.io/aur/version/tencent-wechat?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/tencent-wechat) | • Native Wayland auto-detection & Fcitx5 `text-input-v3` candidate box tracking<br>• Real host `$HOME` bind (resolves file manager drag-and-drop sending issues)<br>• Sensitive directory masking (empty tmpfs isolation for `~/.ssh` and `~/.gnupg`)<br>• Automatic symlink maintenance to prevent chat history database fragmentation |
| **[tencent-qq](./tencent-qq)** | ![AUR version](https://img.shields.io/aur/version/tencent-qq?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/tencent-qq) | • Native Ozone Wayland auto-detection & `text-input-v3` IME cursor tracking<br>• Lightweight Bubblewrap privacy sandbox with key masking<br>• Automated cleanup of vulnerable bundled `libssh2.so.1`<br>• Standardized `/usr/bin/qq` and `/usr/bin/tencent-qq` commands |
| **[eusoft-eudic](./eusoft-eudic)** | ![AUR version](https://img.shields.io/aur/version/eusoft-eudic?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-eudic) | • Official Eudic Linux client community repackage & maintenance<br>• Cleaned up obsolete bundled libraries and conflicting `libxkbcommon-x11` (fixing SIGSEGV crash on startup)<br>• Standardized `/usr/bin/eudic` & `/usr/bin/eusoft-eudic` commands and desktop icons |
| **[eusoft-frhelper](./eusoft-frhelper)** | ![AUR version](https://img.shields.io/aur/version/eusoft-frhelper?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-frhelper) | • Official Frhelper Linux client community repackage & maintenance<br>• Cleaned up obsolete bundled libraries and conflicting `libxkbcommon-x11` (fixing SIGSEGV crash on startup)<br>• Standardized `/usr/bin/frhelper` & `/usr/bin/eusoft-frhelper` commands and desktop icons |
| **[eusoft-dehelper](./eusoft-dehelper)** | ![AUR version](https://img.shields.io/aur/version/eusoft-dehelper?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-dehelper) | • Official Dehelper Linux client community repackage & maintenance<br>• Cleaned up obsolete bundled libraries and conflicting `libxkbcommon-x11` (fixing SIGSEGV crash on startup)<br>• Standardized `/usr/bin/dehelper` & `/usr/bin/eusoft-dehelper` commands and desktop icons |
| **[eusoft-eshelper](./eusoft-eshelper)** | ![AUR version](https://img.shields.io/aur/version/eusoft-eshelper?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-eshelper) | • Official Eshelper Linux client community repackage & maintenance<br>• Cleaned up obsolete bundled libraries and conflicting `libxkbcommon-x11` (fixing SIGSEGV crash on startup)<br>• Standardized `/usr/bin/eshelper` & `/usr/bin/eusoft-eshelper` commands and desktop icons |
| **[eusoft-ting-en](./eusoft-ting-en)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-en?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-ting-en) | • Official Daily English Listening Linux client community repackage & maintenance<br>• Native Ozone Wayland auto-detection & custom user flags loading<br>• Standardized `/usr/bin/ting-en` & `/usr/bin/eusoft-ting-en` commands and desktop icons |
| **[eusoft-ting-fr](./eusoft-ting-fr)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-fr?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-ting-fr) | • Official Daily French Listening Linux client community repackage & maintenance<br>• Native Ozone Wayland auto-detection & custom user flags loading<br>• Standardized `/usr/bin/ting-fr` & `/usr/bin/eusoft-ting-fr` commands and desktop icons |
| **[eusoft-ting-de](./eusoft-ting-de)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-de?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-ting-de) | • Official Daily German Listening Linux client community repackage & maintenance<br>• Native Ozone Wayland auto-detection & custom user flags loading<br>• Standardized `/usr/bin/ting-de` & `/usr/bin/eusoft-ting-de` commands and desktop icons |
| **[eusoft-ting-es](./eusoft-ting-es)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-es?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/eusoft-ting-es) | • Official Daily Spanish Listening Linux client community repackage & maintenance<br>• Native Ozone Wayland auto-detection & custom user flags loading<br>• Standardized `/usr/bin/ting-es` & `/usr/bin/eusoft-ting-es` commands and desktop icons |

---

## Installation

Install using your preferred AUR helper (e.g., `paru` or `yay`):

```bash
# Tencent applications
paru -S tencent-wechat
paru -S tencent-qq

# Eusoft dictionaries
paru -S eusoft-eudic      # Eudic (English / Comprehensive)
paru -S eusoft-frhelper   # Frhelper (French)
paru -S eusoft-dehelper   # Dehelper (German)
paru -S eusoft-eshelper   # Eshelper (Spanish)

# Eusoft listening suites
paru -S eusoft-ting-en    # Daily English Listening
paru -S eusoft-ting-fr    # Daily French Listening
paru -S eusoft-ting-de    # Daily German Listening
paru -S eusoft-ting-es    # Daily Spanish Listening
```

---

## Repository Layout

```text
aur-packages/
├── .github/workflows/
│   ├── sync-tencent-wechat.yml   # Daily upstream check & auto-sync to AUR for WeChat
│   ├── sync-tencent-qq.yml       # Daily upstream check & auto-sync to AUR for QQ
│   ├── sync-eusoft-eudic.yml     # Daily upstream check & auto-sync to AUR for Eudic
│   ├── sync-eusoft-frhelper.yml  # Daily upstream check & auto-sync to AUR for Frhelper
│   ├── sync-eusoft-dehelper.yml  # Daily upstream check & auto-sync to AUR for Dehelper
│   ├── sync-eusoft-eshelper.yml  # Daily upstream check & auto-sync to AUR for Eshelper
│   ├── sync-eusoft-ting-en.yml   # Daily upstream check & auto-sync to AUR for Daily English Listening
│   ├── sync-eusoft-ting-fr.yml   # Daily upstream check & auto-sync to AUR for Daily French Listening
│   ├── sync-eusoft-ting-de.yml   # Daily upstream check & auto-sync to AUR for Daily German Listening
│   └── sync-eusoft-ting-es.yml   # Daily upstream check & auto-sync to AUR for Daily Spanish Listening
│
├── tencent-wechat/               # WeChat AUR package files
├── tencent-qq/                   # QQ AUR package files
├── eusoft-eudic/                 # Eudic AUR package files
├── eusoft-frhelper/              # Frhelper AUR package files
├── eusoft-dehelper/              # Dehelper AUR package files
├── eusoft-eshelper/              # Eshelper AUR package files
├── eusoft-ting-en/               # Daily English Listening AUR package files
├── eusoft-ting-fr/               # Daily French Listening AUR package files
├── eusoft-ting-de/               # Daily German Listening AUR package files
└── eusoft-ting-es/               # Daily Spanish Listening AUR package files
```

---

## Continuous Integration & Automation

Each package directory is independently maintained and synchronized with the official AUR Git repository via GitHub Actions:

1. The detection workflows run on schedule or trigger manually;
2. Automatically retrieves metadata from official upstream release packages;
3. If an upstream update is detected, the workflow automatically:
   - Extracts the new version and computes SHA-256 checksums;
   - Updates `PKGBUILD` and regenerates `.SRCINFO` in the corresponding directory;
   - Commits the updated metadata back to this GitHub repository;
   - Authenticates and pushes directly to the official AUR Git server (`ssh://aur@aur.archlinux.org/<pkgname>.git`).

---

## Disclaimer & License

- The underlying software binaries (such as WeChat, QQ, Eudic, Ting, etc.) are proprietary products owned by their respective copyright holders (Tencent Technology, Shanghai Qianyan Information Technology, etc.). This repository provides only community packaging scripts and runtime wrappers for Arch Linux.
- Packaging scripts, wrapper scripts, and configuration files created in this repository are provided under open-source community-compatible terms.
