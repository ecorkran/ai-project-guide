#!/bin/bash
# AI Project Guide Update - Template Stub
# Updates the ai-project-guide submodule to latest version

# Update submodule and ensure it's on main branch (not detached HEAD)
git submodule update --remote --merge project-documents/ai-project-guide

# Ensure submodule is on main branch
cd project-documents/ai-project-guide
git checkout main
git pull origin main
cd ../..
