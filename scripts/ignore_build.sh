#!/bin/bash

# Vercel Ignored Build Step
# Exit 0 = CANCEL/SKIP BUILD (Do not deploy, save storage & build quotas)
# Exit 1 = PROCEED WITH BUILD (Deploy)

echo "=== Vercel Ignore Build Check ==="
echo "Commit Message: $VERCEL_GIT_COMMIT_MESSAGE"
echo "Commit Ref:     $VERCEL_GIT_COMMIT_REF"
echo "Commit Author:  $VERCEL_GIT_COMMIT_AUTHOR_LOGIN"
echo "Commit SHA:     $VERCEL_GIT_COMMIT_SHA"

# 1. Force deploy keyword overrides all skip rules
if echo "$VERCEL_GIT_COMMIT_MESSAGE" | grep -qiE '\[force deploy\]|\[deploy\]'; then
  echo ">>> [force deploy] keyword detected. Proceeding with Vercel build."
  exit 1
fi

# 2. Skip automated database update bot commits and explicit skip flags
if echo "$VERCEL_GIT_COMMIT_MESSAGE" | grep -qiE '\[skip vercel\]|\[vercel skip\]|\[skip ci\]|\[ci skip\]|Auto-update deals database'; then
  echo ">>> Skip flag or automated database update commit detected. Skipping Vercel build."
  exit 0
fi

# 3. Skip if commit author is GitHub Actions bot
COMMIT_AUTHOR="${VERCEL_GIT_COMMIT_AUTHOR_LOGIN:-$(git log -1 --pretty=format:'%an %ae' 2>/dev/null)}"
if echo "$COMMIT_AUTHOR" | grep -qiE 'github-actions|action@github\.com|GitHub Action'; then
  echo ">>> GitHub Actions bot author detected ($COMMIT_AUTHOR). Skipping Vercel build."
  exit 0
fi

# 4. Check changed files between deployments
if [ -n "$VERCEL_GIT_PREVIOUS_SHA" ] && [ -n "$VERCEL_GIT_COMMIT_SHA" ]; then
  CHANGED_FILES=$(git diff --name-only "$VERCEL_GIT_PREVIOUS_SHA" "$VERCEL_GIT_COMMIT_SHA" 2>/dev/null)
else
  CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null || git diff --name-only HEAD^ HEAD 2>/dev/null)
fi

if [ -n "$CHANGED_FILES" ]; then
  echo "--- Evaluated Changed Files ---"
  echo "$CHANGED_FILES"
  # Only trigger build if files affecting web app runtime were modified
  if ! echo "$CHANGED_FILES" | grep -qE '^(api/|app/|main\.py|vercel\.json|requirements\.txt|assets/logo)'; then
    echo ">>> No website-related files modified in this commit. Skipping Vercel build."
    exit 0
  fi
fi

# Otherwise, valid web changes detected -> proceed
echo ">>> Web application changes detected. Proceeding with Vercel build."
exit 1
