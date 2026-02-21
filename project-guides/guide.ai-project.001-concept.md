---
layer: process
phase: 1
phaseName: concept
guideRole: primary
audience: [human, ai]
description: How to write a Phase 1 Concept document.
dependsOn: [guide.ai-project.000-process.md]
dateUpdated: 20260216
---
This guide will assist us in creating a project concept, allowing us to describe projects using a consistent format and increasing our chances of completing them successfully.  This Concept is Phase 1 in our guide.ai-project.000-process.  If you do not have access to that guide, stop now and request it from the Project Manager.

#### High-Level Project Concept
What are we making?  What makes it unique i.e. why are we making it?  Tell everyone why it's going to be great.  Where does it run?  Who uses it and how do they access it?  Are we creating the whole thing now, or does this concept apply to a particular component, layer, front-end/back-end, etc?

If application or project characteristics lend themselves to a bullet list, add it here.  For example: 
* *This is a NextJS application for an email management SaaS product*
* *Minimal but effective and attractive UI*
* *Subscription based, with 3 tiers the 1st being free.*

*In this sub-project we will create a base NextJS application into which we will add at least a main view and a subscription page, created from sketch mockups.*
*n the future.*

##### Target Users
Include information on the target users for the application?  Will this change as the product develops?

##### Proposed Technical Stack
Describe the technical stack as much is known.  What frameworks, languages, or platforms will we use to develop it?  Where does it run?  Does it need any 3rd-party components (ex: SciChart)?  Start by identifying the proposed platform.

##### Proposed Development Methodology
Also include proposed development methodology here.  TDD?  DDD?  Speed or ironclad reliability (rarely both)?  

When creating the concept document, include the following in proposed methodology:
```
In general, favor simplicity and avoid over-engineering.  Remember the cliche about premature optimization.  Use industry standard solutions where practical and available.  Avoid reinventing wheels.
```

##### Summary
The goal here is to create a high-level concept document tailored to the current project.

##### Output Location
Save the completed concept document as `001-concept.{project}.md` in the `user/project-guides/` directory, where `{project}` is your project name.
