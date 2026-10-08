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

---

## 安装方式

推荐使用 Arch Linux AUR 助手（例如 `paru` 或 `yay`）直接安装：

```bash
# 安装腾讯微信 Linux 原生优化版
paru -S tencent-wechat
# 或
yay -S tencent-wechat

# 安装腾讯 QQ Linux 原生优化版
paru -S tencent-qq
# 或
yay -S tencent-qq

# 安装欧路词典 Linux 社区版
paru -S eusoft-eudic
# 或
yay -S eusoft-eudic
```

---

## 仓库目录结构

```text
aur-packages/
├── .github/workflows/
│   ├── sync-tencent-wechat.yml   # 微信每日上游版本检测与 AUR 自动同步
│   ├── sync-tencent-qq.yml       # QQ 每日上游版本检测与 AUR 自动同步
│   └── sync-eusoft-eudic.yml     # 欧路词典每日上游版本检测与 AUR 自动同步
│
├── tencent-wechat/               # 微信 AUR 软件包工程
│   ├── PKGBUILD                  # 构建脚本
│   ├── .SRCINFO                  # AUR 索引元数据
│   ├── wechat.sh                 # 原生 Wayland 与沙盒启动器
│   ├── wechat.desktop            # 桌面快捷方式
│   └── LICENSE                   # 授权声明
│
├── tencent-qq/                   # QQ AUR 软件包工程
│   ├── PKGBUILD                  # 构建脚本
│   ├── .SRCINFO                  # AUR 索引元数据
│   ├── qq.sh                     # 原生 Wayland 与沙盒启动器
│   ├── qq.desktop                # 桌面快捷方式
│   └── LICENSE                   # 授权声明
│
└── eusoft-eudic/                 # 欧路词典 AUR 软件包工程
    ├── PKGBUILD                  # 构建脚本
    ├── .SRCINFO                  # AUR 索引元数据
    ├── eudic.sh                  # 平台适配与启动包装器
    ├── eusoft-eudic.desktop      # 桌面快捷方式
    └── LICENSE                   # 授权声明
```

---

## 持续集成与自动化流水线

每个软件包子目录独立维护，并通过 GitHub Actions 实现全自动化同步至对应的 AUR 官方 Git 仓库：

1. 每日定时（UTC 02:00 / 北京时间 10:00）运行检测工作流；
2. 自动拉取腾讯官方最新的 deb 安装包元数据；
3. 比对若发现上游发布新版本，流水线将自动：
   - 提取新版本号与计算对应架构的 SHA-256 校验值；
   - 更新对应子目录中的 `PKGBUILD` 并重新生成 `.SRCINFO`；
   - 将版本变更提交回本 GitHub 仓库；
   - 使用配置好的 SSH 密钥直接推送至 AUR 官方服务器（`ssh://aur@aur.archlinux.org/<包名>.git`）。

---

## 免责声明与授权条款

- 本项目所打包的软件本体（如微信、QQ、ChatGPT 等）均为原权利人（如腾讯科技、OpenAI 等）享有著作权的专有软件。本仓库仅提供针对 Arch Linux 环境的社区安装脚本与运行时封装工具。
- 本仓库所编写的构建脚本、启动器包装脚本以及相关配置文件均在开源社区兼容协议下提供。
