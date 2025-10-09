#!/bin/bash
#
# AI Project Guide - Bootstrap Script
#
# Quick setup for any project using ai-project-guide.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.sh | bash
#
# Or download and run:
#   curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.sh -o bootstrap.sh
#   chmod +x bootstrap.sh
#   ./bootstrap.sh

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

# Check prerequisites
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir &> /dev/null; then
    print_error "Not in a git repository"
    echo ""
    echo "Please run this from your project root and ensure it's a git repository:"
    echo "  cd /path/to/your/project"
    echo "  git init"
    echo "  bash scripts/setup-guides.sh"
    exit 1
fi

# Navigate to git repository root
GIT_ROOT=$(git rev-parse --show-toplevel)
if [ "$(pwd)" != "$GIT_ROOT" ]; then
    print_info "Navigating to git repository root..." "$BLUE"
    cd "$GIT_ROOT"
    print_success "Working directory: $GIT_ROOT"
fi

print_info "Setting up AI Project Guide..." "$BLUE"
echo ""

# Check if already set up
if [ -d "project-documents/ai-project-guide" ]; then
    print_warning "AI Project Guide submodule already exists!"
    echo ""
    print_info "To update, run:" "$BLUE"
    echo "  git submodule update --remote project-documents/ai-project-guide"
    echo ""
    print_info "Or if you have the Python script:" "$BLUE"
    echo "  python3 project-documents/ai-project-guide/scripts/setup-project-guides.py --update"
    exit 0
fi

# Create directory structure
print_info "Creating directory structure..." "$BLUE"
mkdir -p project-documents/user/{analysis,architecture,features,project-guides,reviews,slices,tasks}

# Create .gitkeep
echo "# Keep user/ in version control" > project-documents/user/.gitkeep

print_success "Created project-documents/user/ subdirectories"
echo ""

# Check for external guides
if [ -n "$EXTERNAL_PROJECT_DOC_URL" ]; then
    print_info "Importing external guides from: $EXTERNAL_PROJECT_DOC_URL" "$BLUE"

    # Clone to temp directory
    if git clone "$EXTERNAL_PROJECT_DOC_URL" /tmp/external-guides-$$ 2>/dev/null; then
        # Copy contents into user/ (overlay)
        cp -r /tmp/external-guides-$$/* project-documents/user/ 2>/dev/null || true

        # Clean up
        rm -rf /tmp/external-guides-$$

        print_success "External guides imported into project-documents/user/"
        echo ""
    else
        print_warning "Failed to clone external guides (skipping)"
        print_info "Check that EXTERNAL_PROJECT_DOC_URL is accessible" "$BLUE"
        echo ""
    fi
fi

# Add git submodule
print_info "Adding ai-project-guide as git submodule..." "$BLUE"

if git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide 2>/dev/null; then
    print_success "Submodule added successfully!"
    echo ""

    # Setup update script based on project type
    if [ -f "package.json" ]; then
        print_info "Detected package.json - adding update-guides script..." "$BLUE"

        # Check if node is available for JSON manipulation
        if command -v node &> /dev/null; then
            node -e "
                const fs = require('fs');
                const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
                pkg.scripts = pkg.scripts || {};
                pkg.scripts['update-guides'] = 'bash project-documents/ai-project-guide/scripts/template-stubs/update-guides.sh';
                fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2) + '\n');
            "
            print_success "Added 'update-guides' to package.json scripts"
        else
            print_warning "Node.js not found - please manually add to package.json:"
            echo '  "update-guides": "bash project-documents/ai-project-guide/scripts/template-stubs/update-guides.sh"'
        fi
        echo ""
    else
        print_info "Creating update-guides wrapper script..." "$BLUE"
        mkdir -p scripts
        cat > scripts/update-guides << 'EOF'
#!/bin/bash
# Update guides wrapper - calls the template stub from ai-project-guide
exec project-documents/ai-project-guide/scripts/template-stubs/update-guides.sh "$@"
EOF
        chmod +x scripts/update-guides
        print_success "Created scripts/update-guides wrapper"
        echo ""
    fi

    print_success "🎉 Setup complete!" "$GREEN"
    echo ""

    print_info "Next steps:" "$BLUE"
    echo "  1. Commit the changes:"
    echo "       git add ."
    echo "       git commit -m 'Add ai-project-guide'"
    echo ""
    echo "  2. To update guides later:"
    if [ -f "package.json" ]; then
        echo "       pnpm update-guides  (or npm run update-guides)"
    else
        echo "       bash scripts/update-guides"
    fi
    echo ""
    echo "  3. Start using the framework:"
    echo "       • Review: project-documents/ai-project-guide/readme.md"
    echo "       • Process: project-documents/ai-project-guide/project-guides/guide.ai-project.000-process.md"
    echo "       • Your work goes in: project-documents/user/"
    echo ""
else
    print_error "Failed to add submodule. This might happen if:"
    echo "  • You don't have internet connection"
    echo "  • GitHub is unreachable"
    echo "  • The submodule already exists"
    echo ""
    print_info "Try manual setup:" "$BLUE"
    echo "  git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide"
    exit 1
fi
