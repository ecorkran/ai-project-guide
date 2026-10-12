// Required ESLint rules as a block to add to an existing flat config
// (ai-project-guide rules/typescript.md). Use this when the project already has
// an ESLint config, e.g. Next.js; a project with no config uses
// eslint.config.mjs instead.
//
// Add to the project's eslint.config.mjs:
//   import requiredRules from "./required-rules.mjs";
//   ...requiredRules,   // last entry of the exported config array
//
// Needs the typescript-eslint plugin and parser already registered by the
// existing config (next/typescript and tseslint.configs.* both do). Expect new
// lint errors once these rules are on; they are real findings.
//
// Keep the rules in step with eslint.config.mjs and the `required` list.
export default [
  {
    files: ["**/*.{ts,tsx,mts,cts}"],
    languageOptions: {
      parserOptions: { projectService: true },
    },
    rules: {
      // Exception handling (general.md): no swallowed errors.
      "no-empty": ["error", { allowEmptyCatch: false }],
      "@typescript-eslint/only-throw-error": "error",
      // Async: every promise is awaited or explicitly handled.
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
    },
  },
];
