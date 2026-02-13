---
layer: process
phase: 6
phaseName: task-expansion
guideRole: primary
audience: [human, ai]
description: Phase 6 playbook for turning slice task breakdowns into atomic subtasks.
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.002-spec.md
  - guide.ai-project.003-slice-planning.md
dateCreated: 20250101
dateUpdated: 20260121
---
#### Summary
This guide provides instructions and methodology for expanding and enhancing slice task breakdowns in order to create manageable lists to give to an (AI) working as a developer. This assignment is Phase 6 in `guide.ai-projects.00-process`, and will not be received (and cannot be started) until confirmation that the Slice Task Breakdown (Phase 5 Output) is available and approved by the Project Manager.

#### Inputs and Outputs
The inputs to this task are as follows:
* guide.ai-project.000-process
* guide.ai-project.006-task-expansion (this document)
* {project} - spec (phase 2 output)
* {project} - high-level design (phase 3 output)
* {slice} - slice design (phase 4 output)
* {slice} - slice task breakdown (phase 5 output)
* rules/ - directory containing specific coding rules and guidelines organized by platform/technology.

If any inputs are missing, insufficient, or you have questions, stop and resolve these with the Project Manager before proceeding.

The output should be the updated slice task file with expanded and enhanced tasks. Ensure that every task in the input is accounted for.

#### Output Formatting
For this job we'll work in raw markdown code. It's easy for all of us to read and write, and the raw code more easily pastes into other applications and documents.

We will continue to follow the checkbox list format that we have for our main tasks document. L1 items have checkbox, L2 items underneath them, indented and also with checkboxes. The Success condition remains in the L2 list not the L1. Subtasks beyond L2 are considered L3, and should be numbered.

Code blocks should use the multi-line code block syntax tagged with their language:
```{language}
{code block here}
```

Very simple code statements (ex: npm run dev) can use inline: `npm run dev` (etc).

Document may begin with a 1-line title in H1 format. No other H1 should be present. In general, start at H3 or H3 and prefer H3, H4, H5. Avoid any emoji in this document. This is designed to be efficient, streamlined, and fast -- no distractions.

#### Specific Instructions
Our job is to examine the slice task breakdown and expand or enhance the tasks where this additional granularity would improve our AI developer's chances of completing the task successfully.

For any additional context, how and where we fit into the project or the overall plan, consult the additional documentation provided with the input. While we are mostly not writing code, the rules/ directory will provide guidelines for writing any minimal required code as well as potential usefulness in structuring the tasks.

Phases 1-5 are completed and approved. We are going to work on Phase 6, Task enhancement and expansion for the current slice. We will work with the slice task file created in Phase 5: `user/tasks/nnn-tasks.{slice-name}.md`.

###### Procedure
* Identify and review all required inputs and confirm any questions, omissions, or inconsistencies.
* Work with the existing slice task file `user/tasks/nnn-tasks.{slice-name}.md`.
* For each task in the slice, examine it. Can a relatively junior developer complete it as described? If we could improve the odds of that by making the task more granular, adding detail, potentially splitting into subtasks, let's do it.
* Preserve the YAML front matter and context summary - these are crucial for context management.
* Make sure we cover all the tasks.
* If a task cannot effectively be improved, add it to our output verbatim.
* Update the `lastUpdated` field in the YAML front matter.

##### Example of Input Task (from Phase 5)
Note: do use the markdown multiline codeblocks as we described. I couldn't embed them all in here due to formatting concerns and have indicated them in the input and output examples.

```markdown
---
slice: user-authentication
project: trading-app
lld: user/slices/01-slice.user-authentication.md
dependencies: [foundation-setup]
projectState: foundation complete, database schema defined
dateCreated: 20250115
dateUpdated: 20250115
---

## Context Summary
- Working on user authentication slice
- Foundation work (Next.js app, database) is complete
- This slice provides login/logout/registration functionality
- Next slice: trading-dashboard (depends on this)

### User Registration & Login Setup
- [ ] Set up NextAuth.js authentication system  
  - [ ] Install and configure NextAuth.js with TypeScript support
  - [ ] Configure providers (email/password for MVP)
  - [ ] Set up database adapter for user sessions
  - [ ] Success: Users can register and login successfully
```

##### Example of Expansion (Phase 6)
This is provided as an example of expansion. Use this in addition to the additional information in this document to guide your evaluation and expansion.

```markdown
---
slice: user-authentication
project: trading-app
lld: user/slices/01-slice.user-authentication.md
dependencies: [foundation-setup]
projectState: foundation complete, database schema defined
dateCreated: 20250115
dateUpdated: 20250116
---

## Context Summary
- Working on user authentication slice
- Foundation work (Next.js app, database) is complete
- This slice provides login/logout/registration functionality
- Next slice: trading-dashboard (depends on this)

### User Registration & Login Setup

#### Install and Configure NextAuth.js
- [ ] Install NextAuth.js dependencies
  - [ ] Install core NextAuth.js packages
    1. Run:
       (multi-line code block)
       npm install next-auth @next-auth/prisma-adapter
       npm install -D @types/next-auth
       
  - [ ] Verify TypeScript support is properly configured
  - [ ] Success: NextAuth packages installed without conflicts

#### Configure Authentication Providers
- [ ] Set up email/password authentication
  - [ ] Create NextAuth configuration file at `pages/api/auth/[...nextauth].ts`
  - [ ] Configure credentials provider for email/password
    (multi-line code block)typescript
    import NextAuth from 'next-auth'
    import CredentialsProvider from 'next-auth/providers/credentials'
    
    export default NextAuth({
      providers: [
        CredentialsProvider({
          name: 'credentials',
          credentials: {
            email: { label: 'Email', type: 'email' },
            password: { label: 'Password', type: 'password' }
          },
          // Configuration continues...
        })
      ]
    })
    
  - [ ] Add environment variables for NextAuth configuration
    1. Add to `.env.local`:
       (multi-line code block)
       NEXTAUTH_URL=http://localhost:3000
       NEXTAUTH_SECRET=your-secret-key-here
       
  - [ ] Success: Basic email/password authentication configured

#### Set Up Database Integration
- [ ] Configure Prisma adapter for NextAuth
  - [ ] Install Prisma adapter: `npm install @next-auth/prisma-adapter`
  - [ ] Update NextAuth config to use Prisma adapter
  - [ ] Add NextAuth schema to Prisma schema file
    (multi-line code block)prisma
    model Account {
      id                String  @id @default(cuid())
      userId            String
      type              String
      provider          String
      providerAccountId String
      // Additional NextAuth fields...
    }
    
  - [ ] Run database migration: `npx prisma migrate dev --name add-auth`
  - [ ] Success: Database tables created for authentication

#### Create Authentication UI Components
- [ ] Build login form component
  - [ ] Create `src/components/auth/LoginForm.tsx`
  - [ ] Include email and password fields with validation
  - [ ] Add login button that calls NextAuth signIn
  - [ ] Handle loading states and error messages
  - [ ] Success: Functional login form renders and submits

- [ ] Build registration form component
  - [ ] Create `src/components/auth/RegisterForm.tsx`
  - [ ] Include email, password, and confirm password fields
  - [ ] Add client-side validation for password strength
  - [ ] Handle user creation and automatic login after registration
  - [ ] Success: Users can create accounts through the form

#### Final Integration Testing
- [ ] Test complete authentication flow
  - [ ] Verify user registration creates database records
  - [ ] Verify login works with created credentials
  - [ ] Verify logout clears session properly
  - [ ] Test invalid credentials handling
  - [ ] Success: End-to-end authentication flow works correctly
```

Tasks expansions continue with similar levels of details, and should conclude with something such as the following:
```markdown
#### Final Verification
- [ ] Confirm slice completion criteria:
  - [ ] All authentication functionality working
  - [ ] Database integration tested
  - [ ] UI components responsive and accessible
  - [ ] Error handling implemented
  - [ ] Ready for integration with next slice (trading-dashboard)
```

##### Additional Rules for UI Tasks
When working with UI/UX tasks, always consult the AI Development Guide - UI (`guide.ui-development.ai`).
Mockups should be provided to cover all UI tasks. Mockups should be interpreted as layout and design guides. Ensure that controls or placeholders are present, in 1:1 correspondence with the UI. Placeholders are only acceptable if specifically indicated and for the specific elements referenced. UI elements should be laid out and positioned as specified by the mockup.

If requested, generate a color scheme from a base color and a description, and apply this theme to the UI.

If requested to draw elements in a certain general style (ex: bento cards), adhere to this layout and use it to guide any design. If you do not have enough information or knowledge of the style, request information and don't proceed until satisfied you have the information you need.

##### Context Preservation
This phase is crucial for maintaining context across development sessions. The expanded tasks should include enough detail that:
- A fresh AI agent can understand what needs to be done
- The slice can be resumed after context loss or agent restart
- Dependencies on other slices are clearly documented
- Current project state is preserved

##### Summary
Phase 6 transforms slice task breakdowns into detailed, implementable work items that our AI developers can execute with confidence. The focus is on granularity, clarity, and context preservation to ensure successful slice completion.