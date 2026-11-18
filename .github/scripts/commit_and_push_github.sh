#!/usr/bin/env bash
set -euo pipefail

PKG_DIR="${1:?Usage: commit_and_push_github.sh <pkg_dir> <commit_msg>}"
COMMIT_MSG="${2:?Usage: commit_and_push_github.sh <pkg_dir> <commit_msg>}"

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

git add "${PKG_DIR}/PKGBUILD" "${PKG_DIR}/.SRCINFO"
if git diff --cached --quiet; then
  echo "No staged changes for ${PKG_DIR}."
  exit 0
fi

git commit -m "${COMMIT_MSG}"

for attempt in 1 2 3 4 5; do
  if git pull --rebase --autostash origin main && git push origin main; then
    echo "Successfully pushed ${PKG_DIR} update to GitHub main."
    exit 0
  fi
  echo "Push attempt ${attempt} failed (concurrent push?), retrying..."
  sleep $((attempt * 2 + RANDOM % 3))
done

echo "Error: Failed to push to origin main after 5 attempts." >&2
exit 1
