#!/bin/bash

# Vercel Ignored Build Step
# Exit 0 = CANCEL/SKIP BUILD (Do not deploy, saves build quotas & deployment storage)
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

# 2. Skip automated database update bot commits and explicit skip flags
if echo "$COMMIT_MSG" | grep -qiE '\[skip vercel\]|\[vercel skip\]|\[skip ci\]|\[ci skip\]|Auto-update deals database|Auto-update state'; then
  echo ">>> Skip flag or automated database update commit detected. Skipping Vercel build."
  exit 0
fi

# 3. Skip if commit author is GitHub Actions bot
if echo "$COMMIT_AUTHOR" | grep -qiE 'github-actions|action@github\.com|GitHub Action'; then
  echo ">>> GitHub Actions bot author detected ($COMMIT_AUTHOR). Skipping Vercel build."
  exit 0
fi

# 4. Check changed files in the current commit
CURRENT_COMMIT_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null || git diff --name-only HEAD~1 HEAD 2>/dev/null)
echo "--- Changed Files in Current Commit ---"
echo "$CURRENT_COMMIT_FILES"

# If current commit does not touch web runtime files, skip build
if ! echo "$CURRENT_COMMIT_FILES" | grep -qE '^(api/|main\.py|vercel\.json|requirements\.txt|assets/logo)'; then
  echo ">>> No web application runtime files modified in current commit. Skipping Vercel build."
  exit 0
fi

# 5. If web application runtime files were modified by user, proceed
echo ">>> Web application changes detected. Proceeding with Vercel build."
exit 1
