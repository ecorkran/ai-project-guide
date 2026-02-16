---
layer: process
phase: 0          # onboarding applies before Phase 1 begins
phaseName: meta
guideRole: onboarding   # new role distinct from primary/support
audience: [human]       # adjust if AI agents will parse it too
description: What a new contributor should read & set up before Phase 1.
dependsOn: [guide.ai-project.000-process.md]
dateUpdated: 20250930
---
Collection of notes I found useful as a human working with AIs.  AIs are free to read this too.

#### Placement In Roles
AIs such as ChatGPT o3 (deep research) may produce expressive and potentially verbose code, can be too much for things like detailed tasks list.  Asking them to keep the tasks concise may help.

Concept Document: Cascade w/Claude 3.7 Sonnet
Spec: o3-mini-high or gemini-2.5 (Cascade not tried yet)
Task Breakdown: gemini-2.5 Cascade (o3 mini-high is good too)

#### Protocol: Create App
1. Write your concept -- what are you trying to make?  If it has a UI include that, and if so only that, because you need to keep stuff split up.  Give this concept to your AI Technical Fellow.
   
2. Then you and either a Technical Fellow AI or potentially a Senior AI use the Spec Guide with the Concept and create the Spec.
   
3. Next work with a Senior AI good with logic (o3-mini-high, Cascade with Gemini 2.5) and turn the Spec into a Detailed Task Breakdown
   
4. From there work with a Senior AI to determine which can be implemented from Task Breakdown and which need further expansion and enhancement.  Implement tasks, expanding as needed.

#### Protocol: Feature Request
* create task lists for {feature} and write to file.
* run task implementation prompt
* confirm or verify anything needed.
* ensure detailed tasks are checked off
* write concise overview to .windsurf-updates.md in checked form
* make git commit

##### Apps to Create
* ShadCN base (or feature add to ai-lab-nextjs)
* Improved Blog Site
* SciChart specific code
* Angle dashboard

#### Roles
Some phases don't have enough testing yet.

* Cascade w/3.7 Sonnet Thinking did well analyzing a codebase.  Same when used with Gemini 2.5.  Using a model with an agent like Cascade will often produce different results then using without the agent.
  
* AIs like o3-mini-high do very well at creating specific tasks lists, and detailed list items in general.  Cascade with Gemini 2.5 excels at many things, and this is one.

* Very deep thinking AIs like o3 (ChatGPT deep research) produce lists that are too verbose and generally go into too much description.
