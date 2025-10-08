#!/bin/bash
#
# Migrate project-documents/private/ to project-documents/user/
#
# This script renames the directory and updates all internal references.
# Safe to run multiple times (idempotent).

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    local icon="$1"
    local message="$2"
    local color="${3:-$NC}"
    echo -e "${color}${icon} ${message}${NC}"
}

print_error() {
    print_status "❌" "$1" "$RED"
}

print_success() {
    print_status "✅" "$1" "$GREEN"
}

print_info() {
    print_status "💡" "$1" "$BLUE"
}

print_warning() {
    print_status "⚠️" "$1" "$YELLOW"
}

# Navigate to git repository root
if ! git rev-parse --git-dir &> /dev/null; then
    print_error "Not in a git repository"
    exit 1
fi

GIT_ROOT=$(git rev-parse --show-toplevel)
cd "$GIT_ROOT"

print_info "Migrating private/ → user/ in: $GIT_ROOT"
echo ""

# Check current state
PRIVATE_EXISTS=false
USER_EXISTS=false

if [ -d "project-documents/private" ]; then
    PRIVATE_EXISTS=true
fi

if [ -d "project-documents/user" ]; then
    USER_EXISTS=true
fi

# Determine what to do
if [ "$PRIVATE_EXISTS" = true ] && [ "$USER_EXISTS" = true ]; then
    print_error "Both project-documents/private/ and project-documents/user/ exist!"
    echo ""
    print_info "Please resolve manually:"
    echo "  1. Merge content if needed"
    echo "  2. Remove project-documents/private/"
    echo "  3. Re-run this script"
    exit 1
fi

if [ "$PRIVATE_EXISTS" = false ] && [ "$USER_EXISTS" = false ]; then
    print_warning "Neither project-documents/private/ nor project-documents/user/ exists"
    print_info "Nothing to migrate. Exiting."
    exit 0
fi

if [ "$USER_EXISTS" = true ]; then
    print_success "Already migrated to project-documents/user/"
    print_info "Checking for any remaining 'private/' references..."
    echo ""
fi

# Step 1: Rename directory if needed
if [ "$PRIVATE_EXISTS" = true ]; then
    print_info "Renaming directory: private/ → user/"

    git mv project-documents/private project-documents/user

    print_success "Directory renamed"
    echo ""
fi

# Step 2: Update references in user/ directory files
print_info "Scanning user/ directory for internal 'private/' references..."
echo ""

UPDATED_FILES=()

# Find all text files in user/ directory
while IFS= read -r file; do
    # Skip binary files
    if file "$file" | grep -q text; then
        # Check if file contains "private/"
        if grep -q "private/" "$file" 2>/dev/null; then
            # Create backup
            cp "$file" "$file.bak"

            # Replace private/ with user/
            sed -i.tmp 's|project-documents/private/|project-documents/user/|g' "$file"
            sed -i.tmp 's|`private/|`user/|g' "$file"
            sed -i.tmp 's|/private/|/user/|g' "$file"

            # Remove temp file
            rm -f "$file.tmp"

            # Check if file actually changed
            if ! cmp -s "$file" "$file.bak"; then
                UPDATED_FILES+=("$file")
                print_success "Updated: $file"
            fi

            # Remove backup
            rm -f "$file.bak"
        fi
    fi
done < <(find project-documents/user -type f 2>/dev/null || true)

echo ""

# Step 3: Report results
if [ ${#UPDATED_FILES[@]} -eq 0 ]; then
    print_success "No internal references to update"
else
    print_success "Updated ${#UPDATED_FILES[@]} file(s)"
    echo ""
    print_info "Updated files:"
    for file in "${UPDATED_FILES[@]}"; do
        echo "  - $file"
    done
fi

echo ""
print_success "Migration complete!"
echo ""

print_info "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Test your project"
echo "  3. Commit changes: git add . && git commit -m 'Migrate private/ to user/'"
echo ""
print_warning "Note: Update your CLAUDE.md or prompts if they reference 'private/' directly"
