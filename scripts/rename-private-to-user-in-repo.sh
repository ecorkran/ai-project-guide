#!/bin/bash
#
# Rename all references from private/ to user/ in ai-project-guide repository
# Also updates ORG_PRIVATE_GUIDES_URL to EXTERNAL_PROJECT_DOC_URL
#
# This script updates documentation and code in the ai-project-guide repo itself.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    local icon="$1"
    local message="$2"
    local color="${3:-$NC}"
    echo -e "${color}${icon} ${message}${NC}"
}

print_error() { print_status "❌" "$1" "$RED"; }
print_success() { print_status "✅" "$1" "$GREEN"; }
print_info() { print_status "💡" "$1" "$BLUE"; }
print_warning() { print_status "⚠️" "$1" "$YELLOW"; }

# Navigate to repo root
if ! git rev-parse --git-dir &> /dev/null; then
    print_error "Not in a git repository"
    exit 1
fi

GIT_ROOT=$(git rev-parse --show-toplevel)
cd "$GIT_ROOT"

print_info "Renaming private/ → user/ in ai-project-guide repo"
echo ""

# Confirm this is ai-project-guide repo
if [ ! -f "project-guides/guide.ai-project.000-process.md" ]; then
    print_error "This doesn't appear to be the ai-project-guide repository"
    print_info "This script is for updating the ai-project-guide repo itself"
    print_info "For user projects, use: scripts/migrate-private-to-user.sh"
    exit 1
fi

# Files to update (excluding .git, node_modules, etc.)
FILES_TO_UPDATE=(
    ".claude/agents/code-review-agent.md"
    "CHANGELOG.md"
    "CLAUDE.md"
    "directory-structure.md"
    "file-naming-conventions.md"
    "readme.md"
    "project-guides/agents/code-review-agent.md"
    "project-guides/guide.ai-project.000-process.md"
    "project-guides/guide.ai-project.001-concept.md"
    "project-guides/guide.ai-project.002-spec.md"
    "project-guides/guide.ai-project.003-slice-planning.md"
    "project-guides/guide.ai-project.004-slice-design.md"
    "project-guides/guide.ai-project.006-task-expansion.md"
    "project-guides/guide.ai-project.090-code-review.md"
    "project-guides/guide.ai-project.091-legacy-task-migration.md"
    "project-guides/guide.ui-development.ai.md"
    "project-guides/prompt.ai-project.system.md"
    "project-guides/rules/general.md"
    "project-guides/rules/review.md"
    "scripts/bootstrap.sh"
    "scripts/template-stubs/prompt.legacy-migration.md"
    "scripts/template-stubs/update-guides.sh"
    "snippets/npm-scripts.ai-support.json.md"
    "tool-guides/manta-templates/knowledge.md"
    "tool-guides/manta-templates/setup.md"
)

# Also update files in private/ directory itself
if [ -d "private" ]; then
    while IFS= read -r file; do
        FILES_TO_UPDATE+=("$file")
    done < <(find private -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" \) 2>/dev/null || true)
fi

print_info "Step 1: Updating file content"
echo ""

UPDATED_COUNT=0

for file in "${FILES_TO_UPDATE[@]}"; do
    if [ ! -f "$file" ]; then
        print_warning "Skipping missing file: $file"
        continue
    fi

    # Create backup
    cp "$file" "$file.bak"

    # Perform replacements
    sed -i.tmp \
        -e 's|project-documents/private/|project-documents/user/|g' \
        -e 's|`private/|`user/|g' \
        -e "s|'private/|'user/|g" \
        -e 's|"private/|"user/|g' \
        -e 's| private/| user/|g' \
        -e 's|/private/|/user/|g' \
        -e 's|^private/|user/|g' \
        -e 's|ORG_PRIVATE_GUIDES_URL|EXTERNAL_PROJECT_DOC_URL|g' \
        -e 's|ORG_PRIVATE_GUIDES|EXTERNAL_PROJECT_DOC|g' \
        "$file"

    # Remove temp file
    rm -f "$file.tmp"

    # Check if file actually changed
    if ! cmp -s "$file" "$file.bak"; then
        print_success "Updated: $file"
        ((UPDATED_COUNT++))
    fi

    # Remove backup
    rm -f "$file.bak"
done

echo ""
print_success "Updated $UPDATED_COUNT file(s)"
echo ""

# Step 2: Rename directory
if [ -d "private" ]; then
    print_info "Step 2: Renaming directory: private/ → user/"
    git mv private user
    print_success "Directory renamed"
    echo ""
else
    print_warning "Directory 'private/' not found (may already be renamed)"
    echo ""
fi

# Step 3: Summary
print_success "✨ Rename complete!"
echo ""

print_info "Summary of changes:"
echo "  • Updated $UPDATED_COUNT documentation/script files"
echo "  • Renamed directory: private/ → user/"
echo "  • Updated env var: ORG_PRIVATE_GUIDES_URL → EXTERNAL_PROJECT_DOC_URL"
echo ""

print_info "Next steps:"
echo "  1. Review changes: git diff --staged"
echo "  2. Check renamed directory: ls -la project-documents/user/ (if applicable)"
echo "  3. Test bootstrap: bash scripts/bootstrap.sh (in test project)"
echo "  4. Commit: git commit -m 'Rename private/ to user/, update env var naming'"
echo ""

print_warning "Don't forget to update:"
echo "  • Any external documentation referencing 'private/'"
echo "  • Your own environment variables (ORG_PRIVATE_GUIDES_URL → EXTERNAL_PROJECT_DOC_URL)"
echo "  • User migration guide (create if needed)"
