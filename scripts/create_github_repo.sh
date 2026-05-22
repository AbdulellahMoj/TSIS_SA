#!/bin/bash
# Helper: create a GitHub repository from this local folder and push.
# Requires GitHub CLI (`gh`) and git configured with your account.

set -euo pipefail

REPO_NAME=${1:-student-internship-strategist}
VISIBILITY=${2:-public} # public or private

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: GitHub CLI (gh) is required. Install from https://github.com/cli/cli"
  exit 1
fi

echo "Creating repository '$REPO_NAME' (visibility=$VISIBILITY) on your GitHub account..."

# Create repo and push current directory
gh repo create "$REPO_NAME" --${VISIBILITY} --source . --remote origin --push

echo "Repository created and pushed. Remote origin set to 'origin'."
echo "Visit: https://github.com/$(gh auth status --show-token 2>/dev/null || true)"

echo "Done."
