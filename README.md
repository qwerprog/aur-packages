# aur-packages

[English](./README_EN.md)

个人维护的 Arch Linux AUR (Arch User Repository) 软件包合集，由 Chapman ([@qwerprog](https://github.com/qwerprog)) 维护。

本代码仓库采用 Monorepo 架构统一管理个人维护的 AUR 软件包构建脚本（PKGBUILD）与运行时适配器，支持每日自动化检测官方上游版本、原生 Wayland 深度体验优化以及 Bubblewrap 轻量安全沙盒隔离。

---

## 软件包列表

| 软件包名称 | 当前版本 | AUR 链接 | 核心特性与亮点 |
| :--- | :--- | :--- | :--- |
| **[tencent-wechat](./tencent-wechat)** | ![AUR version](https://img.shields.io/aur/version/tencent-wechat?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/tencent-wechat) | • 原生 Wayland 自动探测与 Fcitx5 `text-input-v3` 选词框跟随<br>• 真实宿主 `$HOME` 映射（彻底解决文件管理器拖拽发送失效问题）<br>• 敏感隐私目录遮蔽（使用空 tmpfs 隔离保护 `~/.ssh` 和 `~/.gnupg`）<br>• 历史聊天记录数据库防分化软链自动维护 |
| **[tencent-qq](./tencent-qq)** | ![AUR version](https://img.shields.io/aur/version/tencent-qq?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/tencent-qq) | • 原生 Ozone Wayland 自动探测与 `text-input-v3` 输入法光标跟随<br>• 轻量级 Bubblewrap 隐私沙盒隔离与敏感密钥遮蔽<br>• 自动清理官方包内置的易损组件 `libssh2.so.1`<br>• 标准化 `/usr/bin/qq` 与 `/usr/bin/tencent-qq` 指令 |
| **[eusoft-eudic](./eusoft-eudic)** | ![AUR version](https://img.shields.io/aur/version/eusoft-eudic?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-eudic) | • 欧路词典 Linux 官方客户端社区重打包与维护<br>• 移除过时捆绑库与冲突的 `libxkbcommon-x11`，彻底修复启动崩溃（SIGSEGV）<br>• 标准化 `/usr/bin/eudic` 与 `/usr/bin/eusoft-eudic` 快捷指令及桌面图标 |
| **[eusoft-frhelper](./eusoft-frhelper)** | ![AUR version](https://img.shields.io/aur/version/eusoft-frhelper?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-frhelper) | • 法语助手 Linux 官方客户端社区重打包与维护<br>• 修复过时系统库冲突与 Wayland 适配，杜绝启动段错误<br>• 标准化 `/usr/bin/frhelper` 与 `/usr/bin/eusoft-frhelper` 快捷指令及桌面图标 |
| **[eusoft-dehelper](./eusoft-dehelper)** | ![AUR version](https://img.shields.io/aur/version/eusoft-dehelper?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-dehelper) | • 德语助手 Linux 官方客户端社区重打包与维护<br>• 修复过时系统库冲突与 Wayland 适配，杜绝启动段错误<br>• 标准化 `/usr/bin/dehelper` 与 `/usr/bin/eusoft-dehelper` 快捷指令及桌面图标 |
| **[eusoft-eshelper](./eusoft-eshelper)** | ![AUR version](https://img.shields.io/aur/version/eusoft-eshelper?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-eshelper) | • 西语助手 Linux 官方客户端社区重打包与维护<br>• 修复过时系统库冲突与 Wayland 适配，杜绝启动段错误<br>• 标准化 `/usr/bin/eshelper` 与 `/usr/bin/eusoft-eshelper` 快捷指令及桌面图标 |
| **[eusoft-ting-en](./eusoft-ting-en)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-en?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-ting-en) | • 每日英语听力 Linux 官方客户端社区重打包与维护<br>• 原生 Ozone Wayland 自动探测与用户 flags 配置支持<br>• 标准化 `/usr/bin/ting-en` 与 `/usr/bin/eusoft-ting-en` 快捷指令及桌面图标 |
| **[eusoft-ting-fr](./eusoft-ting-fr)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-fr?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-ting-fr) | • 每日法语听力 Linux 官方客户端社区重打包与维护<br>• 原生 Ozone Wayland 自动探测与用户 flags 配置支持<br>• 标准化 `/usr/bin/ting-fr` 与 `/usr/bin/eusoft-ting-fr` 快捷指令及桌面图标 |
| **[eusoft-ting-de](./eusoft-ting-de)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-de?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-ting-de) | • 每日德语听力 Linux 官方客户端社区重打包与维护<br>• 原生 Ozone Wayland 自动探测与用户 flags 配置支持<br>• 标准化 `/usr/bin/ting-de` 与 `/usr/bin/eusoft-ting-de` 快捷指令及桌面图标 |
| **[eusoft-ting-es](./eusoft-ting-es)** | ![AUR version](https://img.shields.io/aur/version/eusoft-ting-es?color=blue&logo=archlinux) | [AUR 页面](https://aur.archlinux.org/packages/eusoft-ting-es) | • 每日西语听力 Linux 官方客户端社区重打包与维护<br>• 原生 Ozone Wayland 自动探测与用户 flags 配置支持<br>• 标准化 `/usr/bin/ting-es` 与 `/usr/bin/eusoft-ting-es` 快捷指令及桌面图标 |

---

## 安装方式

推荐使用 Arch Linux AUR 助手（例如 `paru` 或 `yay`）直接安装：

```bash
# 安装腾讯软件
paru -S tencent-wechat
paru -S tencent-qq

# 安装欧路词典全语种系列
paru -S eusoft-eudic      # 欧路词典 (英语/通用)
paru -S eusoft-frhelper   # 法语助手
paru -S eusoft-dehelper   # 德语助手
paru -S eusoft-eshelper   # 西语助手

# 安装欧路每日听力全语种系列
paru -S eusoft-ting-en    # 每日英语听力
paru -S eusoft-ting-fr    # 每日法语听力
paru -S eusoft-ting-de    # 每日德语听力
paru -S eusoft-ting-es    # 每日西语听力
```

---

## 仓库目录结构

```text
aur-packages/
├── .github/workflows/
│   ├── sync-tencent-wechat.yml   # 微信每日上游版本检测与 AUR 自动同步
│   ├── sync-tencent-qq.yml       # QQ 每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-eudic.yml     # 欧路词典每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-frhelper.yml  # 法语助手每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-dehelper.yml  # 德语助手每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-eshelper.yml  # 西语助手每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-ting-en.yml   # 每日英语听力每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-ting-fr.yml   # 每日法语听力每日上游版本检测与 AUR 自动同步
│   ├── sync-eusoft-ting-de.yml   # 每日德语听力每日上游版本检测与 AUR 自动同步
│   └── sync-eusoft-ting-es.yml   # 每日西语听力每日上游版本检测与 AUR 自动同步
│
├── tencent-wechat/               # 微信 AUR 软件包工程
├── tencent-qq/                   # QQ AUR 软件包工程
├── eusoft-eudic/                 # 欧路词典 (英语/综合) AUR 软件包工程
├── eusoft-frhelper/              # 法语助手 AUR 软件包工程
├── eusoft-dehelper/              # 德语助手 AUR 软件包工程
├── eusoft-eshelper/              # 西语助手 AUR 软件包工程
├── eusoft-ting-en/               # 每日英语听力 AUR 软件包工程
├── eusoft-ting-fr/               # 每日法语听力 AUR 软件包工程
├── eusoft-ting-de/               # 每日德语听力 AUR 软件包工程
└── eusoft-ting-es/               # 每日西语听力 AUR 软件包工程
```

---

## 持续集成与自动化流水线

每个软件包子目录独立维护，并通过 GitHub Actions 实现全自动化同步至对应的 AUR 官方 Git 仓库：

1. 每日定时运行检测工作流；
2. 自动拉取官方最新的 deb 安装包元数据与更新；
3. 比对若发现上游发布新版本，流水线将自动：
   - 提取新版本号与计算对应架构的 SHA-256 校验值；
   - 更新对应子目录中的 `PKGBUILD` 并重新生成 `.SRCINFO`；
   - 将版本变更提交回本 GitHub 仓库；
   - 使用配置好的 SSH 密钥直接推送至 AUR 官方服务器（`ssh://aur@aur.archlinux.org/<包名>.git`）。

---

## 免责声明与授权条款

- 本项目所打包的软件本体（如微信、QQ、欧路词典、每日听力等）均为原权利人（如腾讯科技、上海潜言信息科技等）享有著作权的专有软件。本仓库仅提供针对 Arch Linux 环境的社区安装脚本与运行时封装工具。
- 本仓库所编写的构建脚本、启动器包装脚本以及相关配置文件均在开源社区兼容协议下提供。
