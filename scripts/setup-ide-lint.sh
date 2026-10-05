# Lint config check for setup-ide. Sourced by setup-ide, not run directly.
#
# For each language detected in the project, checks that the linter config the
# language rules require is present and contains the rules listed in
# project-guides/lint/<language>/required. It only reports, unless WRITE_LINT
# is true: then it writes a config that is missing. It never edits a config
# that exists. The one layered case is ruff: when pyproject.toml has a
# [tool.ruff] section without the required rules, it adds a ruff.toml that
# extends that section, so the project's own settings stay in force.
#
# Reads the project from PROJECT_ROOT and writes to TARGET_ROOT, so a dry run
# (which points TARGET_ROOT at a sandbox) still checks the real project.
#
# Written configs belong to the project from then on: they are not recorded in
# the install manifest and never pruned.

# Root-level files this check may write. Dry run copies them into its sandbox.
LINT_WRITE_PATHS="ruff.toml analysis_options.yaml eslint.config.mjs .editorconfig Directory.Build.props"

# Print the first alternative of each requirement in required_file that has no
# match in the text on stdin. Requirement lines hold alternatives separated by |.
# Args: required_file
lint_missing_requirements() {
    local required=$1
    local text line alt found
    text=$(cat)
    while IFS= read -r line; do
        case "$line" in ''|'#'*) continue ;; esac
        found=false
        local old_ifs=$IFS
        IFS='|'
        for alt in $line; do
            if printf '%s' "$text" | grep -qF -- "$alt"; then
                found=true
                break
            fi
        done
        IFS=$old_ifs
        [ "$found" = true ] || printf '%s\n' "${line%%|*}"
    done < "$required"
}

# Args: language, description of the config checked, missing requirements
lint_report() {
    local lang=$1 what=$2 missing=$3
    if [ -z "$missing" ]; then
        print_status $GREEN "✅ Lint ($lang): $what has the required rules"
    else
        print_status $YELLOW "⚠️  Lint ($lang): $what is missing required rules: $(printf '%s' "$missing" | tr '\n' ' ')"
    fi
}

# Write a missing config when WRITE_LINT is set, otherwise say how to.
# Args: language, path relative to the project root, source file
lint_write_or_suggest() {
    local lang=$1 rel=$2 src=$3
    if [ "$WRITE_LINT" = true ]; then
        cat "$src" > "$TARGET_ROOT/$rel"
        print_status $GREEN "✅ Lint ($lang): wrote $rel"
    else
        print_status $YELLOW "⚠️  Lint ($lang): no $rel — run setup-ide with --write-lint to add it"
    fi
}

# The [tool.ruff...] sections of pyproject.toml, with quotes normalized to ".
pyproject_ruff_sections() {
    [ -f "$PROJECT_ROOT/pyproject.toml" ] || return 0
    awk '/^[[:space:]]*\[/ { in_ruff = ($0 ~ /^[[:space:]]*\[+tool\.ruff/) } in_ruff' \
        "$PROJECT_ROOT/pyproject.toml" | tr "'" '"'
}

lint_check_python() {
    local root=$PROJECT_ROOT
    local required="$LINT_SOURCE_DIR/python/required"
    [ -f "$root/pyproject.toml" ] || [ -f "$root/setup.py" ] \
        || compgen -G "$root/requirements*.txt" > /dev/null || return 0

    # Same precedence as ruff: .ruff.toml, then ruff.toml, then pyproject.toml.
    local cfg=""
    [ -f "$root/ruff.toml" ] && cfg="ruff.toml"
    [ -f "$root/.ruff.toml" ] && cfg=".ruff.toml"

    local missing
    if [ -n "$cfg" ]; then
        missing=$({
            tr "'" '"' < "$root/$cfg"
            if grep -qE '^[[:space:]]*extend[[:space:]]*=[[:space:]]*["'"'"']pyproject\.toml' "$root/$cfg"; then
                pyproject_ruff_sections
            fi
        } | lint_missing_requirements "$required")
        lint_report python "$cfg" "$missing"
        return 0
    fi

    local sections
    sections=$(pyproject_ruff_sections)
    if [ -z "$sections" ]; then
        lint_write_or_suggest python ruff.toml "$LINT_SOURCE_DIR/python/ruff.toml"
        return 0
    fi

    missing=$(printf '%s' "$sections" | lint_missing_requirements "$required")
    if [ -z "$missing" ]; then
        lint_report python "[tool.ruff] in pyproject.toml" ""
        return 0
    fi

    if [ "$WRITE_LINT" != true ]; then
        lint_report python "[tool.ruff] in pyproject.toml" "$missing"
        print_status $YELLOW "   Run setup-ide with --write-lint to add a ruff.toml that extends it with them"
        return 0
    fi

    # ruff.toml outranks pyproject.toml, so it extends that config rather than
    # replacing it. extend-select from this file applies on top of the
    # project's own select and ignore.
    {
        echo "# Adds the rules required by ai-project-guide rules/python.md on top of"
        echo "# [tool.ruff] in pyproject.toml, which stays the main ruff config."
        echo 'extend = "pyproject.toml"'
        echo ""
        echo "[lint]"
        echo "extend-select = [$(printf '%s' "$missing" | paste -sd ',' - | sed 's/,/, /g')]"
    } > "$TARGET_ROOT/ruff.toml"
    print_status $GREEN "✅ Lint (python): wrote ruff.toml extending [tool.ruff] in pyproject.toml"
}

lint_check_dart() {
    local pubspec="$PROJECT_ROOT/pubspec.yaml"
    [ -f "$pubspec" ] || return 0

    local lang="dart"
    grep -qE 'sdk:[[:space:]]*flutter' "$pubspec" && lang="flutter"

    if [ -f "$PROJECT_ROOT/analysis_options.yaml" ]; then
        lint_report "$lang" analysis_options.yaml \
            "$(lint_missing_requirements "$LINT_SOURCE_DIR/dart/required" < "$PROJECT_ROOT/analysis_options.yaml")"
        return 0
    fi

    local staged
    staged=$(mktemp)
    if [ "$lang" = flutter ]; then
        sed 's|^include: package:lints/recommended.yaml$|include: package:flutter_lints/flutter.yaml|' \
            "$LINT_SOURCE_DIR/dart/analysis_options.yaml" > "$staged"
    else
        cat "$LINT_SOURCE_DIR/dart/analysis_options.yaml" > "$staged"
    fi
    lint_write_or_suggest "$lang" analysis_options.yaml "$staged"
    rm -f "$staged"
}

lint_check_typescript() {
    [ -f "$PROJECT_ROOT/tsconfig.json" ] || [ -f "$PROJECT_ROOT/tsconfig.base.json" ] || return 0

    local f cfg=""
    for f in eslint.config.js eslint.config.mjs eslint.config.cjs eslint.config.ts \
             eslint.config.mts eslint.config.cts .eslintrc .eslintrc.js .eslintrc.cjs \
             .eslintrc.json .eslintrc.yml .eslintrc.yaml; do
        if [ -f "$PROJECT_ROOT/$f" ]; then
            cfg=$f
            break
        fi
    done

    if [ -n "$cfg" ]; then
        lint_report typescript "$cfg" \
            "$(lint_missing_requirements "$LINT_SOURCE_DIR/typescript/required" < "$PROJECT_ROOT/$cfg")"
        return 0
    fi

    lint_write_or_suggest typescript eslint.config.mjs "$LINT_SOURCE_DIR/typescript/eslint.config.mjs"
    if [ "$WRITE_LINT" = true ]; then
        print_status $BLUE "   Install: npm i -D eslint @eslint/js typescript-eslint, and add a \"lint\": \"eslint .\" script"
    fi
}

lint_check_csharp() {
    local projects
    projects=$(find "$PROJECT_ROOT" -maxdepth 3 \
        \( -name .git -o -name node_modules -o -name project-documents -o -name bin -o -name obj \) -prune \
        -o \( -name '*.csproj' -o -name '*.sln' \) -print)
    [ -n "$projects" ] || return 0

    # The requirements span three kinds of file, so check them together.
    local missing
    missing=$({
        local f
        for f in .editorconfig Directory.Build.props; do
            [ -f "$PROJECT_ROOT/$f" ] && cat "$PROJECT_ROOT/$f"
        done
        printf '%s\n' "$projects" | grep '\.csproj$' | while IFS= read -r f; do cat "$f"; done
    } | lint_missing_requirements "$LINT_SOURCE_DIR/csharp/required")

    if [ -z "$missing" ]; then
        lint_report csharp "analyzer and build settings" ""
        return 0
    fi

    lint_report csharp "analyzer and build settings" "$missing"
    local f
    for f in .editorconfig Directory.Build.props; do
        [ -f "$PROJECT_ROOT/$f" ] || lint_write_or_suggest csharp "$f" "$LINT_SOURCE_DIR/csharp/$f"
    done
}

# Run every language check. A language whose rules file is excluded through
# rules.exclude is skipped, since the project has opted out of those rules.
check_lint_configs() {
    if [ ! -d "$LINT_SOURCE_DIR" ]; then
        print_status $RED "❌ Lint config directory not found: $LINT_SOURCE_DIR"
        return 1
    fi

    local lang
    for lang in python dart typescript csharp; do
        rule_is_excluded "$lang.md" && continue
        "lint_check_$lang"
    done
}
