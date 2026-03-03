---
docType: migration
scope: project-wide
description: Migration instructions to v0.13.x
targetVersion: "0.13.0"
dateCreated: 20260302
dateUpdated: 20260302
---

# v0.13.x Migration Guide

## Overview
This version makes numerous changes and streamlines the project structure and flow significantly.

### Roles Update
Technical Fellow is renamed to Architect

### Feature Component Removed
"feature" as a project component is removed.  Previously a feature was standalone functionality, not substantial enough to be a slice, but too much to be a task.  This concept was removed.  Any files in `user/features/` should be moved to `/user/archive`.

### Phase Renames and Remaps
Phases are as follows:
1. Concept
2. Architecture
3. Slice Plan
4. Slice Design
5. Task Breakdown
6. Implementation
7. Integration

The following phases are removed, consolidated, or renamed:
2. Spec replaced with 2. Architecture.  Project-wide spec is only created on explicit request now
2.5. HLD is now handled at architectural component level.
3.5. Architural component is moved to 2. Architecture
5. Explicit Follow version is now an optional supplement to 5. Task Breakdown
6. Task Expansion is now an optional variant to 5. Task Breakdown
7. Implementation is now 6. Implementation

### Project Structure and Flow
The dual path of project vs architecture level planning and overview documents is now streamlined into one path that all project follow.  Additionally, project-level specs and HLD are generally not created.

All projects now use the following organization:
Concept -> Architectural Component -> Slice Plan -> Slices -> Tasks

Most projects will have multiple architectural components.  Small projects will only have one.