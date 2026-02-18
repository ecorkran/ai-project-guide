---
layer: rules
scope: ui-development
audience: [human, ai]
description: Guidelines for handling UI/UX tasks in task breakdowns and implementation.
dateCreated: 20260218
dateUpdated: 20260218
---

#### UI Development Task Rules

When creating or expanding tasks that involve UI/UX work, follow these guidelines in addition to the standard task breakdown process defined in `guide.ai-project.005-task-breakdown`.

##### Mockups
Mockups should be provided to cover all UI tasks. Interpret mockups as layout and design guides:
- Ensure that controls or placeholders are present in 1:1 correspondence with the UI specification.
- Placeholders are only acceptable if specifically indicated and for the specific elements referenced.
- UI elements should be laid out and positioned as specified by the mockup.

If mockups are not provided for a UI task, stop and request them from the Project Manager before proceeding.

##### Theming and Style
- If requested, generate a color scheme from a base color and a description, and apply this theme to the UI.
- If requested to use a specific layout style (e.g., bento cards, dashboard grid), adhere to that layout throughout the relevant components.
- If you do not have enough information or knowledge of the requested style, request information and do not proceed until satisfied you have what you need.

##### Accessibility
- UI components should follow basic accessibility practices: semantic HTML, appropriate ARIA attributes, keyboard navigation support, and sufficient color contrast.
- Include accessibility checks in success criteria for UI tasks where applicable.