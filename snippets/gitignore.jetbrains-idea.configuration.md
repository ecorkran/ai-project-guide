---
docType: snippet
format: gitignore
purpose: jetbrains-ide-configuration
audience: [human, ai]
---

# JetBrains IDE .gitignore Configuration

Contains `.gitignore` entries for JetBrains IDEs. This information should be in every `.gitignore`.

### JetBrains IDEs 
```
.idea/*
!.idea/modules.xml
!.idea/vcs.xml
!.idea/*.iml
!.idea/encodings.xml
!.idea/codeStyles/**
!.idea/inspectionProfiles/**
!.idea/runConfigurations/**
```
### Explicitly ignore user-specific noise
```
.idea/workspace.xml
.idea/usage.statistics.xml
.idea/shelf/
```
