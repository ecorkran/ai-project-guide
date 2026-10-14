---
docType: snippet
format: json
purpose: npm-scripts-for-ai-project-guide-setup
audience: [human, ai]
---

# AI Project Guide npm Scripts

Add these scripts to your package.json for ai-project-guide integration.

```json
"scripts": {
    "setup-guides": "mkdir -p project-documents/user/{analysis,architecture,features,project-guides,reviews,slices,tasks} && git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide && echo '# Keep user/ in version control' > project-documents/user/.gitkeep || echo 'Submodule already exists—run npm run update-guides to update.'",
    "update-guides": "git submodule update --remote project-documents/ai-project-guide",
    "setup-cursor": "cf setup-ide cursor",
    "setup-copilot": "cf setup-ide copilot",
    "setup-agents": "cf setup-ide agents",
    "setup-claude": "cf setup-ide claude"
  }
```
