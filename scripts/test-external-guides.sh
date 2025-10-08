#!/bin/bash
# Test script for external guides functionality
# Creates test repos and validates the external guides import/update flow

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    exit 1
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Cleanup function
cleanup() {
    print_info "Cleaning up test directories..."
    rm -rf /tmp/test-external-guides
    rm -rf /tmp/test-external-guides-project
}

# Set trap to cleanup on exit
trap cleanup EXIT

print_test "Creating test external guides repository..."
mkdir -p /tmp/test-external-guides
cd /tmp/test-external-guides
git init -q

# Create sample external guides content
mkdir -p architecture slices tasks project-guides
cat > architecture/external-arch.md << 'EOF'
# External Architecture Guide
This is a test architecture document from external guides.
EOF

cat > slices/100-slice.external-feature.md << 'EOF'
# External Slice Example
This is a test slice from external guides.
EOF

cat > tasks/100-tasks.external.md << 'EOF'
# External Tasks
- [ ] Test task from external guides
EOF

cat > project-guides/external-notes.md << 'EOF'
# External Notes
Custom project guidance from external guides.
EOF

git add .
git commit -q -m "Initial external guides content"
print_pass "External guides repository created"

print_test "Creating test project..."
mkdir -p /tmp/test-external-guides-project
cd /tmp/test-external-guides-project
git init -q

# Export the env var for bootstrap script
export ORG_PRIVATE_GUIDES_URL="file:///tmp/test-external-guides"
print_info "Set ORG_PRIVATE_GUIDES_URL=$ORG_PRIVATE_GUIDES_URL"

print_test "Running bootstrap with external guides..."
# Run bootstrap script (assuming we're in ai-project-guide repo)
bash $OLDPWD/scripts/bootstrap.sh

# Verify external files were imported
print_test "Verifying external files were imported..."
if [ -f "project-documents/private/architecture/external-arch.md" ]; then
    print_pass "External architecture file imported"
else
    print_fail "External architecture file NOT found"
fi

if [ -f "project-documents/private/slices/100-slice.external-feature.md" ]; then
    print_pass "External slice file imported"
else
    print_fail "External slice file NOT found"
fi

if [ -f "project-documents/private/tasks/100-tasks.external.md" ]; then
    print_pass "External tasks file imported"
else
    print_fail "External tasks file NOT found"
fi

# Create a user file to test preservation
print_test "Creating user file to test preservation..."
cat > project-documents/private/architecture/user-arch.md << 'EOF'
# User Architecture
This is a user-created file that should be preserved.
EOF

# Modify external guides repo
print_test "Updating external guides repository..."
cd /tmp/test-external-guides
echo -e "\n## Updated Section" >> architecture/external-arch.md
cat > architecture/new-external-file.md << 'EOF'
# New External File
This file was added after initial setup.
EOF
git add .
git commit -q -m "Update external guides"

# Copy update script to test project
print_test "Setting up update script in test project..."
cd /tmp/test-external-guides-project
mkdir -p scripts
cp $OLDPWD/scripts/template-stubs/update-guides.sh scripts/
chmod +x scripts/update-guides.sh

# Run update
print_test "Running update-guides script..."
bash scripts/update-guides.sh

# Verify update worked
print_test "Verifying external guides were updated..."
if grep -q "Updated Section" project-documents/private/architecture/external-arch.md; then
    print_pass "External file was updated"
else
    print_fail "External file was NOT updated"
fi

if [ -f "project-documents/private/architecture/new-external-file.md" ]; then
    print_pass "New external file was added"
else
    print_fail "New external file was NOT added"
fi

# Verify user file was preserved
print_test "Verifying user files were preserved..."
if [ -f "project-documents/private/architecture/user-arch.md" ]; then
    if grep -q "user-created file" project-documents/private/architecture/user-arch.md; then
        print_pass "User file was preserved"
    else
        print_fail "User file was modified"
    fi
else
    print_fail "User file was deleted"
fi

# Test without ORG_PRIVATE_GUIDES_URL
print_test "Testing without ORG_PRIVATE_GUIDES_URL set..."
unset ORG_PRIVATE_GUIDES_URL
bash scripts/update-guides.sh 2>&1 | grep -q "No external guides configured" && \
    print_pass "Gracefully handles missing ORG_PRIVATE_GUIDES_URL" || \
    print_fail "Did not handle missing ORG_PRIVATE_GUIDES_URL gracefully"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ All tests passed!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
print_info "Test artifacts cleaned up automatically"
