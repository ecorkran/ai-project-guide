#!/bin/bash
# AI Project Guide Update - Template Stub
# Updates the ai-project-guide submodule and external guides (if configured)

# Update submodule and ensure it's on main branch (not detached HEAD)
git submodule update --remote --merge project-documents/ai-project-guide

# Ensure submodule is on main branch
cd project-documents/ai-project-guide
git checkout main
git pull origin main
cd ../..

# Update external guides if configured
if [ -n "$EXTERNAL_PROJECT_DOC_URL" ]; then
    echo "Updating external guides from: $EXTERNAL_PROJECT_DOC_URL"

    TEMP_DIR="/tmp/external-guides-update-$$"
    if git clone "$EXTERNAL_PROJECT_DOC_URL" "$TEMP_DIR" 2>/dev/null; then
        cp -r "$TEMP_DIR"/* project-documents/user/ 2>/dev/null || true
        rm -rf "$TEMP_DIR"
        echo "✓ External guides updated"
    else
        echo "⚠ Warning: Failed to update external guides"
    fi
else
    echo "ℹ No external guides configured (EXTERNAL_PROJECT_DOC_URL not set)"
fi
