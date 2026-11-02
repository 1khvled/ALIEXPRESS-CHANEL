#!/bin/bash

# Vercel Ignored Build Step
# Exit 0 = CANCEL/SKIP BUILD (Do not deploy, save storage & build quotas)
# Exit 1 = PROCEED WITH BUILD (Deploy)

COMMIT_MSG="${VERCEL_GIT_COMMIT_MESSAGE:-$(git log -1 --pretty=format:'%B' 2>/dev/null)}"
COMMIT_AUTHOR="${VERCEL_GIT_COMMIT_AUTHOR_LOGIN:-$(git log -1 --pretty=format:'%an %ae' 2>/dev/null)}"
COMMIT_SHA="${VERCEL_GIT_COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null)}"

echo "=== Vercel Ignore Build Check ==="
echo "Commit Message: $COMMIT_MSG"
echo "Commit Author:  $COMMIT_AUTHOR"
echo "Commit SHA:     $COMMIT_SHA"
echo "Previous SHA:   $VERCEL_GIT_PREVIOUS_SHA"

# 1. Force deploy keyword overrides all skip rules
if echo "$COMMIT_MSG" | grep -qiE '\[force deploy\]|\[deploy\]'; then
  echo ">>> [force deploy] keyword detected. Proceeding with Vercel build."
  exit 1
fi

# 2. Check changed files between deployments
if [ -n "$VERCEL_GIT_PREVIOUS_SHA" ] && [ -n "$COMMIT_SHA" ]; then
  CHANGED_FILES=$(git diff --name-only "$VERCEL_GIT_PREVIOUS_SHA" "$COMMIT_SHA" 2>/dev/null)
else
  CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null || git diff --name-only HEAD^ HEAD 2>/dev/null)
fi

echo "--- Evaluated Changed Files ---"
echo "$CHANGED_FILES"

# If web application runtime files were modified, build and deploy
if echo "$CHANGED_FILES" | grep -qE '^(api/|app/|main\.py|vercel\.json|requirements\.txt|scripts/ignore_build\.sh|assets/logo)'; then
  echo ">>> Web application changes detected in commit range. Proceeding with Vercel build."
  exit 1
fi

# Otherwise (e.g. only storage/state/ or deals.db modified), skip build
echo ">>> Only database/storage files modified. Skipping Vercel build."
exit 0
