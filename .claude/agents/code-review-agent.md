---
description: Automated code review agent configuration for comprehensive project codebase analysis
globs: ["**/*"]
alwaysApply: false
---

# Automated Code Review Agent

## Agent Purpose
This agent automatically performs comprehensive code reviews across the entire project codebase, generating review documents and task lists according to the guidelines in `.cursor/rules/review.md`.

## Agent Configuration

### Detection & Scope
- **Project Type Detection**: Automatically identify project type from file structure and configuration files
- **File Type Mapping**: Map project types to relevant source file extensions
- **Scope**: Full project crawl (not just changed files)
- **Frequency**: On-demand execution (not continuous monitoring)

### Project Type Detection Logic

#### NextJS Projects
- **Indicators**: `next.config.js/ts`, `package.json` with Next.js dependency, `app/` or `src/app/` directory
- **File Extensions**: `.tsx`, `.ts`, `.jsx`, `.js`, `.css`, `.scss`, `.mdx`
- **Key Directories**: `src/`, `app/`, `components/`, `lib/`, `types/`

#### Python Projects
- **Indicators**: `requirements.txt`, `pyproject.toml`, `setup.py`, `__init__.py` files
- **File Extensions**: `.py`, `.pyx`, `.pyi`
- **Key Directories**: `src/`, `app/`, `tests/`, `migrations/`

#### C++ Projects
- **Indicators**: `CMakeLists.txt`, `Makefile`, `*.vcxproj`, `*.sln`
- **File Extensions**: `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`, `.hxx`
- **Key Directories**: `src/`, `include/`, `lib/`, `tests/`

#### Rust Projects
- **Indicators**: `Cargo.toml`, `Cargo.lock`
- **File Extensions**: `.rs`
- **Key Directories**: `src/`, `tests/`, `examples/`

#### Generic/Unknown Projects
- **Fallback**: Review all common source files
- **File Extensions**: `.js`, `.ts`, `.jsx`, `.tsx`, `.py`, `.cpp`, `.h`, `.rs`, `.go`, `.java`

## Review Process

### Step 1: Project Analysis
1. **Detect Project Type**: Analyze project structure and configuration files
2. **Identify Source Files**: Map relevant file extensions and directories
3. **Generate File List**: Create comprehensive list of files to review
4. **Load Review Guidelines**: Read and parse `.cursor/rules/review.md`

### Step 2: File-by-File Review
For each source file:
1. **Read File Content**: Load and parse file content
2. **Apply Review Questionnaire**: Systematically evaluate against all 12 review criteria
3. **Generate Findings**: Document issues, improvements, and observations
4. **Categorize Issues**: Group by Critical Issues, Code Quality, Best Practices, etc.

### Step 3: Document Generation
1. **Create Review Documents**: Generate `review.{filename}.MMDD.md` files
2. **Create Task Lists**: Generate `tasks.code-review.{filename}.MMDD.md` files
3. **Organize by Priority**: P0 (Critical) → P1 (Quality) → P2 (Best Practices) → P3 (Enhancements)
4. **Add YAML Headers**: Include proper metadata for all generated files

### Step 4: Summary Report
1. **Generate Overview**: Create summary of all findings across the project
2. **Prioritize Actions**: Identify highest-impact improvements
3. **Create Index**: Generate master index of all review documents

## File Organization

### Output Structure
```
project-documents/
└── user/
    └── reviews/
        ├── review-docs/
        │   ├── review.component.tsx.0101.md
        │   ├── review.utils.ts.0101.md
        │   └── ...
        ├── tasks/
        │   ├── tasks.code-review.component.tsx.0101.md
        │   ├── tasks.code-review.utils.ts.0101.md
        │   └── ...
        ├── summary/
        │   ├── review-summary.0101.md
        │   └── priority-actions.0101.md
        └── index/
            └── review-index.0101.md
```

### YAML Headers
All generated files include:
```yaml
---
layer: project
docType: review
projectType: nextjs
reviewDate: 2025-01-01
reviewer: automated-agent
priority: P0|P1|P2|P3
---
```

## Review Criteria Application

### Platform-Specific Reviews
- **NextJS**: Focus on Sections 8, 11, 12 (Performance, Accessibility, React/TypeScript/NextJS)
- **Python**: Focus on Sections 1-7, 9-10 (Bugs, Code Quality, Security, Testing)
- **C++**: Focus on Sections 1-7, 9-10 (Bugs, Code Quality, Security, Testing)
- **Rust**: Focus on Sections 1-7, 9-10 (Bugs, Code Quality, Security, Testing)

### File Type Specifics
- **Component Files**: Emphasize Sections 5, 11, 12 (Component Structure, Accessibility, React patterns)
- **Utility Files**: Emphasize Sections 4, 6, 7 (Code Duplication, Patterns, Documentation)
- **Configuration Files**: Emphasize Sections 2, 6 (Hard-coded Elements, Best Practices)
- **Test Files**: Emphasize Sections 10, 7 (Testing Coverage, Documentation)

## Automation Triggers

### Manual Execution
- **Command**: `npm run code-review` or `pnpm code-review`
- **Scope**: Full project review
- **Output**: Complete review document set

### Scheduled Execution
- **Frequency**: Weekly automated reviews
- **Scope**: Changed files since last review
- **Output**: Incremental review updates

### CI/CD Integration
- **Trigger**: On pull requests
- **Scope**: Changed files in PR
- **Output**: PR-specific review comments

## Configuration Options

### Review Depth
- **Quick**: Surface-level review (5-10 minutes per file)
- **Standard**: Comprehensive review (15-30 minutes per file)
- **Deep**: In-depth analysis (30-60 minutes per file)

### Output Format
- **Markdown**: Standard markdown files
- **JSON**: Machine-readable format
- **HTML**: Web-viewable reports
- **PDF**: Printable reports

### Filtering Options
- **File Size**: Skip files larger than threshold
- **File Type**: Review only specific file types
- **Directory**: Limit to specific directories
- **Complexity**: Focus on high-complexity files

## Quality Assurance

### Review Validation
- **Consistency Check**: Ensure consistent application of guidelines
- **Coverage Verification**: Confirm all relevant files were reviewed
- **Priority Validation**: Verify appropriate priority assignments
- **Documentation Completeness**: Check for missing required sections

### Performance Optimization
- **Parallel Processing**: Review multiple files concurrently
- **Caching**: Cache file content and analysis results
- **Incremental Reviews**: Only review changed files when possible
- **Resource Limits**: Set memory and time limits per file

## Integration Points

### Existing Tools
- **Git Integration**: Use git for file discovery and change tracking
- **Linting Integration**: Incorporate existing linting results
- **Type Checking**: Include TypeScript/other type checker results
- **Build System**: Consider build warnings and errors

### External Services
- **Code Quality Tools**: Integrate with SonarQube, CodeClimate, etc.
- **Security Scanners**: Include security analysis results
- **Performance Tools**: Incorporate performance metrics
- **Documentation Generators**: Link to existing documentation

## Success Metrics

### Review Quality
- **Coverage**: Percentage of source files reviewed
- **Issues Found**: Number and severity of issues identified
- **Actionability**: Percentage of findings converted to tasks
- **Accuracy**: False positive rate of identified issues

### Process Efficiency
- **Review Speed**: Time per file reviewed
- **Output Quality**: Completeness and clarity of generated documents
- **Maintenance Overhead**: Time required to maintain and update agent
- **User Adoption**: Frequency of agent usage by team

## Maintenance

### Regular Updates
- **Guideline Updates**: Sync with changes to `.cursor/rules/review.md`
- **Project Type Detection**: Add support for new project types
- **File Type Mapping**: Update for new file extensions
- **Review Criteria**: Refine based on team feedback

### Performance Monitoring
- **Execution Time**: Track review duration
- **Resource Usage**: Monitor memory and CPU consumption
- **Error Rates**: Track failed reviews and analysis errors
- **User Feedback**: Collect and incorporate team input

---

## Usage Instructions

### Quick Start
1. Ensure `.cursor/rules/review.md` is up to date
2. Run: `npm run code-review` or `pnpm code-review`
3. Review generated documents in `project-documents/user/code-reviews/`
4. Prioritize and implement tasks from generated task lists

### Customization
1. Modify project type detection logic for your specific needs
2. Adjust file type mappings for your project structure
3. Customize review criteria application based on your guidelines
4. Configure output formats and organization preferences

### Integration
1. Add to CI/CD pipeline for automated PR reviews
2. Schedule regular full-project reviews
3. Integrate with existing code quality tools
4. Connect to project management systems for task tracking 