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
| **[openai-chatgpt](./openai-chatgpt)** | ![AUR version](https://img.shields.io/aur/version/openai-chatgpt?color=blue&logo=archlinux) | [AUR](https://aur.archlinux.org/packages/openai-chatgpt) | • Official native Arch Linux binary packaging by OpenAI<br>• Safely removes invasive upstream post-install scripts that tamper with `/etc/pacman.conf`<br>• Standardized official desktop entry and `/usr/bin/chatgpt` executable |

---

## Installation

Install using your preferred AUR helper (e.g., `paru` or `yay`):

```bash
# Tencent WeChat
paru -S tencent-wechat
# or
yay -S tencent-wechat

# Tencent QQ
paru -S tencent-qq
# or
yay -S tencent-qq

# OpenAI ChatGPT
paru -S openai-chatgpt
# or
yay -S openai-chatgpt
```

---

## Repository Layout

```text
aur-packages/
├── .github/workflows/
│   ├── sync-tencent-wechat.yml   # Daily upstream check & auto-sync to AUR for WeChat
│   ├── sync-tencent-qq.yml       # Daily upstream check & auto-sync to AUR for QQ
│   └── sync-openai-chatgpt.yml   # Daily upstream check & auto-sync to AUR for ChatGPT
│
├── tencent-wechat/               # WeChat AUR package files
│   ├── PKGBUILD                  # Package build script
│   ├── .SRCINFO                  # AUR package metadata
│   ├── wechat.sh                 # Native Wayland & sandbox launcher
│   ├── wechat.desktop            # Desktop entry
│   └── LICENSE                   # License statement
│
├── tencent-qq/                   # QQ AUR package files
│   ├── PKGBUILD                  # Package build script
│   ├── .SRCINFO                  # AUR package metadata
│   ├── qq.sh                     # Native Wayland & sandbox launcher
│   ├── qq.desktop                # Desktop entry
│   └── LICENSE                   # License statement
│
└── openai-chatgpt/               # ChatGPT AUR package files
    ├── PKGBUILD                  # Package build script
    └── .SRCINFO                  # AUR package metadata
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

- The underlying software binaries (such as WeChat, QQ, ChatGPT, etc.) are proprietary products owned by their respective copyright holders (Tencent Technology, OpenAI, etc.). This repository provides only community packaging scripts and runtime wrappers for Arch Linux.
- Packaging scripts, wrapper scripts, and configuration files created in this repository are provided under open-source community-compatible terms.
