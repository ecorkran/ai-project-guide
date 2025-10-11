#!/bin/bash
# AI Project Guide Update Script
# Updates the ai-project-guide submodule and external guides (if configured)
# Works for both regular projects and monorepo development

set -e

SUBMODULE_PATH="project-documents/ai-project-guide"

echo "🔄 Updating AI Project Guide..."
echo ""

# Check if submodule exists
if [ ! -d "$SUBMODULE_PATH/.git" ] && [ ! -f "$SUBMODULE_PATH/.git" ]; then
    echo "❌ Error: ai-project-guide submodule not found at $SUBMODULE_PATH"
    echo ""
    echo "💡 Run setup first:"
    echo "   pnpm setup-guides (for npm/pnpm projects)"
    echo "   or"
    echo "   bash scripts/bootstrap.sh (for other projects)"
    exit 1
fi

# Update submodule and ensure it's on main branch (not detached HEAD)
echo "📚 Updating submodule..."
git submodule update --remote --merge "$SUBMODULE_PATH"

# Ensure submodule is on main branch
cd "$SUBMODULE_PATH"
git checkout main
git pull origin main

# Get version info
LATEST_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "latest")
LATEST_COMMIT=$(git log -1 --format="%h - %s")
cd ../..

echo ""
echo "✅ Updated to: $LATEST_COMMIT"
echo ""

# Update external guides if configured
if [ -n "$EXTERNAL_PROJECT_DOC_URL" ]; then
    echo "📦 Updating external guides from: $EXTERNAL_PROJECT_DOC_URL"

    TEMP_DIR="/tmp/external-guides-update-$$"
    if git clone "$EXTERNAL_PROJECT_DOC_URL" "$TEMP_DIR" 2>/dev/null; then
        cp -r "$TEMP_DIR"/* project-documents/user/ 2>/dev/null || true
        rm -rf "$TEMP_DIR"
        echo "✅ External guides updated"
    else
        echo "⚠️  Warning: Failed to update external guides"
    fi
    echo ""
else
    echo "ℹ️  No external guides configured (EXTERNAL_PROJECT_DOC_URL not set)"
    echo ""
fi

# Auto-commit the update
echo "💾 Committing changes..."
git add "$SUBMODULE_PATH"

if [ -n "$EXTERNAL_PROJECT_DOC_URL" ]; then
    git add project-documents/user/
fi

if git diff --staged --quiet; then
    echo "✅ Already up to date - no changes to commit"
else
    git commit -m "Update ai-project-guide to ${LATEST_VERSION}"
    echo "✅ Committed: Update ai-project-guide to ${LATEST_VERSION}"
fi

echo ""
echo "🎉 AI Project Guide synchronized successfully"
