#!/bin/bash

# Vercel Ignored Build Step
# Exit 0 = CANCEL/SKIP BUILD (Do not deploy)
# Exit 1 = PROCEED WITH BUILD (Deploy)

echo "=== Vercel Ignore Build Check ==="
echo "Commit Message: $VERCEL_GIT_COMMIT_MESSAGE"
echo "Commit Ref: $VERCEL_GIT_COMMIT_REF"
echo "Commit Author: $VERCEL_GIT_COMMIT_AUTHOR_LOGIN"

# 0. Allow force deploy flags
if [[ "$VERCEL_GIT_COMMIT_MESSAGE" == *"[force vercel]"* ]] || \
   [[ "$VERCEL_GIT_COMMIT_MESSAGE" == *"[deploy]"* ]]; then
  echo ">>> Explicit deploy flag detected. Proceeding with Vercel deployment."
  exit 1
fi

# 1. Skip if automated state / bot commit or explicit skip tags
if [[ "$VERCEL_GIT_COMMIT_MESSAGE" == *"[skip vercel]"* ]] || \
   [[ "$VERCEL_GIT_COMMIT_MESSAGE" == *"[vercel skip]"* ]] || \
   [[ "$VERCEL_GIT_COMMIT_MESSAGE" == *"[skip ci]"* ]] || \
   [[ "$VERCEL_GIT_COMMIT_MESSAGE" == *"Auto-update deals database"* ]] || \
   [[ "$VERCEL_GIT_COMMIT_AUTHOR_LOGIN" == *"github-actions"* ]] || \
   [[ "$VERCEL_GIT_COMMIT_AUTHOR_NAME" == *"GitHub Action"* ]]; then
  echo ">>> Automated bot/state commit detected. Skipping Vercel build."
  exit 0
fi

# 2. Check if deployment-critical files changed (api/, vercel.json, requirements.txt, templates/)
# If only storage/state/, deals.db, scripts/, tests/, README changed, do NOT redeploy Vercel!
if git rev-parse HEAD^ >/dev/null 2>&1; then
  DIFF=$(git diff --name-only HEAD^ HEAD)
  echo "Changed files in this commit:"
  echo "$DIFF"

  RELEVANT=$(echo "$DIFF" | grep -E '^(api/|templates/|vercel\.json|requirements\.txt)')
  if [ -z "$RELEVANT" ]; then
    echo ">>> No changes to api/, templates/, vercel.json, or requirements.txt. Skipping build."
    exit 0
  fi
fi

echo ">>> Relevant API/app changes detected. Proceeding with Vercel deployment."
exit 1
