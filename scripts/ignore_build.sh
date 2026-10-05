#!/bin/bash

# Vercel Ignored Build Step
# Exit 0 = CANCEL/SKIP BUILD (Do not deploy)
# Exit 1 = PROCEED WITH BUILD (Deploy)

echo "=== Vercel Ignore Build Check ==="
echo "Commit Message: $VERCEL_GIT_COMMIT_MESSAGE"
echo "Commit Ref: $VERCEL_GIT_COMMIT_REF"
echo "Commit Author: $VERCEL_GIT_COMMIT_AUTHOR_LOGIN"

# 1. Skip ONLY if it's the automated database update bot commit
if echo "$VERCEL_GIT_COMMIT_MESSAGE" | grep -qiE '\[skip vercel\]|\[vercel skip\]|Auto-update deals database'; then
  echo ">>> Bot/state update commit detected. Skipping Vercel build."
  exit 0
fi

if echo "$VERCEL_GIT_COMMIT_AUTHOR_LOGIN" | grep -qiE 'github-actions'; then
  echo ">>> GitHub Actions bot author detected. Skipping Vercel build."
  exit 0
fi

# Otherwise, ALWAYS proceed with build!
echo ">>> Valid deployment commit. Proceeding with Vercel build."
exit 1

