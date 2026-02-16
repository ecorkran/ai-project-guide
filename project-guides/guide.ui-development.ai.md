---
layer: process
phase: 5
phaseName: execution
guideRole: support
audience:
  - human
  - ai
description: UI-specific playbook for Phases 4-5 (component naming, states, tests).
dependsOn:
  - guide.ai-project.002-spec.md
dateUpdated: 20251008
---
This document provides specialized knowledge and techniques useful in completion of UI/UX tasks.
##### Mockups and Wireframes
All tasks involving new views, forms, or pages, as well as any task requiring sophisticated layout should include a mockup or reference image.  Mockup may be wireframe or rendered UI elements.  Mockups should be present in the directory `user/ui` and `user/ui/screenshots` in the `{project-root}/project-documents/user/` folder.

*Example UI Mockup*
![[Pasted image 20250425124903.png]]

The notes in orange are for you to better understand how to convert one of these mockups into a real UI.  The mockup above provides layout, context notes (dashed callouts) and numerous UI elements.  UI color scheme should not be inferred from mockup.  From the sketch above (and supplemented by orange notes) you can see:
* The header is on top, and is full width
* The button bar is on the right, below the header, and fills remaining height.
* The historical data panel is to the right of the chart, full height.
* Panel controls are left aligned
* Padding and margins are present.

In general:
* Items should maintain reasonable padding, margins, and spacing at different sizes.
* Containers should fill space.  If buttons or controls form a group, the group relationship and proportions should be maintained on resize.  Use some judgement we don't need any full-screen-width buttons :) . 
* Items should be in same relative positions up/down/left/right as they are in the mockup.
* Do not, for example, put the data panel on the left if you were implementing the above design.
* Don't place buttons of different heights in the same row. 
* If percentages or ratios are specified, attempt to respect them, and maintain them on resize.

Based on above which you should infer from your analysis, the following renderings would be incorrect (I am showing mockup, but these would be real UI in actual project)

![[Pasted image 20250425124955.png]]

##### Colors and Styles
Colors should not be inferred from wireframe or sketch mockups.  If requested to create a color scheme based on a color or colors, attempt to work with shades of those colors.  For example, a dark scheme based on a deep teal (ideally you will be provided with RGB) as one of its darker colors should use that color, not grey with that color as accent, unless that is what is requested.  

Expect styles and schemes to be modified and iterated, and to work with your Project Manager or designer to lay them out and apply consistently.

##### Summary
This should help when working on UI tasks.  As always, if you do not have sufficient information to complete the task with a high probability of success, obtain confirmation from the project manager before proceeding.
