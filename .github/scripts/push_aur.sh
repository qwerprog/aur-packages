#!/usr/bin/env bash
set -euo pipefail

PKG_DIR="${1:?Usage: push_aur.sh <pkg_dir>}"

if [ -z "${AUR_SSH_PRIVATE_KEY:-}" ]; then
  echo "Error: AUR_SSH_PRIVATE_KEY secret is not set in GitHub Secrets!" >&2
  exit 1
fi

mkdir -p ~/.ssh
chmod 700 ~/.ssh
printf '%s\n' "${AUR_SSH_PRIVATE_KEY}" > ~/.ssh/aur
chmod 600 ~/.ssh/aur
ssh-keyscan -t ed25519,rsa aur.archlinux.org >> ~/.ssh/known_hosts 2>/dev/null

AUR_DIR="/tmp/aur-${PKG_DIR}"
rm -rf "${AUR_DIR}"

export GIT_SSH_COMMAND="ssh -i ~/.ssh/aur -o StrictHostKeyChecking=accept-new"

for attempt in 1 2 3; do
  if git clone "ssh://aur@aur.archlinux.org/${PKG_DIR}.git" "${AUR_DIR}"; then
    break
  fi
  if [ "${attempt}" -eq 3 ]; then
    echo "Error: Failed to clone AUR repository for ${PKG_DIR}." >&2
    exit 1
  fi
  rm -rf "${AUR_DIR}"
  sleep $((attempt * 3))
done

# Replace non-.git contents with tracked package files from monorepo
find "${AUR_DIR}" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

REPO_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
while IFS= read -r -d '' rel_path; do
  sub_path="${rel_path#${PKG_DIR}/}"
  dest_path="${AUR_DIR}/${sub_path}"
  mkdir -p "$(dirname "${dest_path}")"
  cp -pf "${REPO_ROOT}/${rel_path}" "${dest_path}"
done < <(git -C "${REPO_ROOT}" ls-files -z "${PKG_DIR}/")

cd "${AUR_DIR}"
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

git add -A
if [ -z "$(git status --porcelain)" ]; then
  echo "AUR ${PKG_DIR} is already in sync; nothing to push."
  exit 0
fi

git commit -m "Update ${PKG_DIR}"
git push -u origin master
echo "Successfully pushed ${PKG_DIR} to AUR."
