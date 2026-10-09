#!/usr/bin/env bash
#
# Launcher script for tencent-meeting (腾讯会议 / WeMeet)
# Provides Wayland / XWayland compatibility, Qt dark mode text fixes,
# OpenSSL 3 / PulseAudio wrapping, and secure Bubblewrap sandboxing.
#

set -e

WEMEET_BIN="/opt/wemeet/bin/wemeetapp"

# 1. Qt Appearance & Scalability
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_STYLE_OVERRIDE=fusion
export IBUS_USE_PORTAL=1
export LD_LIBRARY_PATH="/usr/lib/wemeet:${LD_LIBRARY_PATH:-/usr/lib}"

# 2. Paths & State Setup
USER_RUN_DIR="/run/user/$(id -u)"
CONFIG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}"
FONTCONFIG_DIR="${CONFIG_DIR}/fontconfig"
KDE_GLOBALS_FILE="${CONFIG_DIR}/kdeglobals"
KDE_ICON_CACHE_FILE="${XDG_CACHE_HOME:-${HOME}/.cache}/icon-cache.kcache"
WEMEET_APP_DIR="${XDG_DATA_HOME:-${HOME}/.local/share}/wemeetapp"
LD_PRELOAD_WRAP="${LD_PRELOAD:-}:/usr/lib/wemeet/libwemeetwrap.so"

# Ensure fontconfig directory exists to avoid LoadCustomFont() crash
mkdir -p "${FONTCONFIG_DIR}"
mkdir -p "${WEMEET_APP_DIR}"

# 3. Display Platform Configuration
BIN_NAME="$(basename "$0")"
if [[ "${BIN_NAME}" == *"-x11" ]]; then
    export XDG_SESSION_TYPE=x11
    export EGL_PLATFORM=x11
    export QT_QPA_PLATFORM=xcb
    unset WAYLAND_DISPLAY
elif [[ "${XDG_SESSION_TYPE}" == "wayland" ]]; then
    export QT_QPA_PLATFORM=xcb
    export XDG_SESSION_TYPE=x11
    unset WAYLAND_DISPLAY
    export WEMEET_XWAYLAND=1
fi

# 4. User Custom Flags (~/.config/tencent-meeting-flags.conf or wemeet-flags.conf)
USER_FLAGS=()
for flags_file in "${CONFIG_DIR}/tencent-meeting-flags.conf" "${CONFIG_DIR}/wemeet-flags.conf"; do
    if [[ -f "${flags_file}" ]]; then
        while IFS= read -r line || [[ -n "${line}" ]]; do
            line="$(echo "${line}" | sed 's/#.*//;s/^[[:space:]]*//;s/[[:space:]]*$//')"
            [[ -n "${line}" ]] && USER_FLAGS+=("${line}")
        done < "${flags_file}"
        break
    fi
done

# 5. Lightweight Privacy Sandbox via Bubblewrap (if installed)
if command -v bwrap >/dev/null 2>&1; then
    BWRAP_ARGS=(
        --new-session
        --unshare-user-try --unshare-pid --unshare-uts --unshare-cgroup-try
        --proc /proc
        --ro-bind / /
        --dev-bind /dev /dev
        --dev-bind-try /dev/dri /dev/dri
        --dev-bind-try /dev/snd /dev/snd
        --tmpfs /dev/shm
        --bind /tmp /tmp
        --ro-bind-try /sys /sys
        --ro-bind /dev/null /proc/cpuinfo
        --bind "${USER_RUN_DIR}" "${USER_RUN_DIR}"
        --bind "${HOME}" "${HOME}"
        --tmpfs "${HOME}/.ssh"
        --tmpfs "${HOME}/.gnupg"
        --tmpfs "${CONFIG_DIR}"
        --ro-bind-try "${FONTCONFIG_DIR}" "${FONTCONFIG_DIR}"
        --ro-bind-try "${KDE_GLOBALS_FILE}" "${KDE_GLOBALS_FILE}"
        --bind-try "${KDE_ICON_CACHE_FILE}" "${KDE_ICON_CACHE_FILE}"
        --bind "${WEMEET_APP_DIR}" "${WEMEET_APP_DIR}"
        --setenv LD_PRELOAD "${LD_PRELOAD_WRAP}"
    )

    for dev_node in /dev/video*; do
        [[ -e "${dev_node}" ]] && BWRAP_ARGS+=(--dev-bind "${dev_node}" "${dev_node}")
    done

    exec bwrap "${BWRAP_ARGS[@]}" "${WEMEET_BIN}" "${USER_FLAGS[@]}" "$@"
else
    export LD_PRELOAD="${LD_PRELOAD_WRAP}"
    exec "${WEMEET_BIN}" "${USER_FLAGS[@]}" "$@"
fi
