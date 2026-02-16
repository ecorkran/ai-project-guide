---
docType: guide
layer: tool-guide
tool: tailwindcss
subject: syntax-highlighting
audience: [human, ai]
description: Using Shiki and rehype-shiki for syntax highlighting in Tailwind v4 apps
dateUpdated: 20260121
---

# Syntax Highlighting in Tailwind CSS v4

Should you use Shiki and rehype-shiki for syntax highlighting in a Tailwind v4 app?

**Shiki** and **rehype-shiki** are excellent choices for syntax highlighting in modern web apps, including those using Tailwind CSS v4. Here's a breakdown of how they work, their advantages, and alternatives you might consider.

---

### **What Are Shiki and rehype-shiki?**

- **Shiki** is a syntax highlighter that uses the same TextMate grammars and themes as VS Code, producing highly accurate and visually appealing code blocks. It outputs HTML with semantic classes, making it easy to style with CSS or Tailwind utilities[1][5][6].
- **rehype-shiki** is a plugin for the rehype ecosystem (often used in Markdown/MDX pipelines) that integrates Shiki for automatic code block highlighting during Markdown processing[4][6].

---

### **How Do They Work in a Tailwind v4 App?**

- **Integration**: Use rehype-shiki as a plugin in your Markdown/MDX processing pipeline (e.g., with Next.js, Astro, SvelteKit, or custom setups). It will process code blocks and output HTML with Shiki’s syntax highlighting[4][5][6][7].
- **Styling**: The output is unstyled by default. You add your own styles-Tailwind makes this easy. For example, you can target Shiki’s classes or use arbitrary selectors to apply colors, padding, scrollbars, etc.[4][5].
- **Dark/Light Themes**: Shiki supports multiple themes and can switch between them using CSS variables, making it easy to match your site’s color mode[4].

---

### **Advantages of Shiki/rehype-shiki**

- **VS Code-quality highlighting**: Looks exactly like your editor[1][5].
- **Customizable themes**: Use any VS Code theme or your own[1][4][5].
- **Performance**: Shiki runs at build time (or server-side), so there’s no client-side JS payload for highlighting[5][7].
- **Tailwind-friendly**: Output is plain HTML, so you can style it with Tailwind classes or custom CSS[4][5].

---

### **Alternatives**

- **react-syntax-highlighter**: A popular React component for client-side highlighting. Easier for dynamic content but larger JS bundle and less accurate highlighting compared to Shiki[3].
- **Prism.js**: Another widely used highlighter, but less accurate than Shiki for some languages and themes.
- **rehype-pretty**: A wrapper plugin around Shiki for easier integration with rehype/MDX pipelines[4].
- **rehype-pretty-code**: Wrapper plugin around Shiki for rehype/MD (not MDX)

---

### **Best Practice Recommendation**

**For static or server-rendered code blocks (e.g., blogs, documentation):**
- **Use Shiki (via rehype-shiki or rehype-pretty-code)**. This gives you the best-looking, most accurate highlighting, with minimal runtime cost and full control over styling[4][5][6][7].

**For dynamic, client-side code editing or interactive code blocks:**
- Consider client-side libraries like react-syntax-highlighter, but only if you need runtime highlighting[3].

---

### **Example: Using rehype-shiki with Tailwind v4**

1. **Install dependencies:**
   ```bash
   npm install shiki rehype-shiki
   ```

2. **Configure your Markdown/MDX pipeline:**
   ```js
   import rehypeShiki from 'rehype-shiki';

   // Example for Next.js or similar frameworks
   const mdxOptions = {
     rehypePlugins: [
       [rehypeShiki, { theme: 'github-dark', themes: { dark: 'github-dark', light: 'github-light' } }]
     ]
   }
   ```

3. **Style the output with Tailwind:**
   - Target Shiki’s classes in your CSS or use Tailwind’s arbitrary selectors to apply styles[4][5].

---
## rehype-pretty-code for Markdown Syntax Highlighting (No MDX)?

**rehype-pretty-code** is an excellent choice for syntax highlighting in a Tailwind v4 app that processes plain Markdown (not MDX). It is specifically designed to work with Markdown or MDX, and leverages the Shiki (or Shikiji) syntax highlighter to provide accurate, editor-grade highlighting-matching the look and feel of VS Code[1][3][4][5].

### **Key Features**

- **VS Code-quality themes:** You can use any VS Code theme for your code blocks, ensuring your site matches the familiar appearance of the editor[1][4][5].
- **Static highlighting:** All highlighting is done at build time (server-side), so there’s no client-side JavaScript overhead[1][4][5].
- **Advanced features:** Supports line numbers, line highlighting, word highlighting, and even ANSI highlighting for terminal output[1][4][5].
- **Customizable styling:** The plugin outputs semantic HTML, which you can style using Tailwind classes or custom CSS[2].

### **How to Use rehype-pretty-code (with Markdown, not MDX)**

1. **Install Dependencies**
   ```bash
   npm install rehype-pretty-code shiki
   ```

2. **Set Up Your Markdown Pipeline**
   Use `unified`, `remark-parse`, `remark-rehype`, and `rehype-stringify` to process Markdown, and add `rehype-pretty-code` as a plugin:
   ```js
   import { unified } from 'unified';
   import remarkParse from 'remark-parse';
   import remarkRehype from 'remark-rehype';
   import rehypeStringify from 'rehype-stringify';
   import rehypePrettyCode from 'rehype-pretty-code';

   const file = await unified()
     .use(remarkParse)
     .use(remarkRehype)
     .use(rehypePrettyCode, {
       // Options: theme, line numbers, etc.
       theme: 'vscode-dark-plus'
     })
     .use(rehypeStringify)
     .process(markdownString);
   ```

3. **Style the Output with Tailwind**
   The plugin adds data attributes like `[data-rehype-pretty-code-figure]` to the output. You can use Tailwind’s `@apply` directive in your CSS to style these elements:
   ```css
   [data-rehype-pretty-code-figure] pre {
     @apply px-0;
   }
   [data-rehype-pretty-code-figure] code {
     @apply text-sm leading-loose md:text-base;
   }
   [data-rehype-pretty-code-figure] [data-line] {
     @apply border-l-2 border-l-transparent px-3;
   }
   [data-rehype-pretty-code-figure] [data-highlighted-line] {
     background: rgba(200, 200, 255, 0.1);
     @apply border-l-blue-400;
   }
   ```
   You have full control to make the code blocks look exactly like VS Code[2].

### Official Guide
https://rehype-pretty.pages.dev/

### **Should You Use It?**

- **Yes, rehype-pretty-code is highly recommended** for your use case:
  - It works seamlessly with plain Markdown (no MDX required)[1][3][5].
  - It produces beautiful, VS Code-style code blocks.
  - It is easy to style with Tailwind CSS[2].
  - It supports advanced features like line/word highlighting if you need them[1][4].

### **Alternatives**

- **rehype-shiki**: Also works well, but rehype-pretty-code offers more advanced features (like line/word highlighting and easier theme switching)[2].
- **rehype-highlight**: Simpler, but less accurate and less customizable than Shiki-based plugins[2].

---

### **Conclusion**

**Shiki and rehype-shiki are the best-in-class solution for code syntax highlighting in Tailwind v4 apps that render Markdown or MDX.** They produce accurate, beautiful, and customizable code blocks, and integrate seamlessly with Tailwind’s utility-first styling approach. For most static or server-rendered use cases, you should use Shiki (via rehype-shiki or rehype-pretty or rehype-prtty-code) over client-side alternatives[1][4][5][6][7].

**rehype-pretty-code:**  
If you want your code blocks to look like VS Code and you’re processing plain Markdown, rehype-pretty-code is the best choice. It’s designed for exactly this scenario and is easy to style with Tailwind v4[1][2][4][5].

Sources
[1] Rehype Pretty Code | Rehype Pretty https://rehype-pretty.pages.dev
[2] Code Highlighting - shikijs/rehype - Velite https://velite.js.org/guide/code-highlighting
[3] rehype-pretty/rehype-pretty-code: Beautiful code blocks for ... - GitHub https://github.com/rehype-pretty/rehype-pretty-code
[4] Lets see what we can do with rehype pretty code - JollyBlog https://my-first-blog-dusky.vercel.app/blog/code-blocks
[5] test: Rehype pretty code - David Wells https://davidwells.io/typography/_rehype-pretty-code
[6] Syntax highlighting for MDX - Bruno https://itsbruno.dev/blog/syntax-highlighting-for-mdx
[7] Which library is used for code syntax highlighting in sdk.vercel.ai? https://www.reddit.com/r/nextjs/comments/1as3155/which_library_is_used_for_code_syntax/
[8] Code highlighting plugin - Tutorial - Chris.lu https://chris.lu/web_development/tutorials/next-js-static-mdx-blog/code-highlighting-plugin
[9] Remark and rehype dont convert mdx correctly in nextjs in app router https://stackoverflow.com/questions/78375327/remark-and-rehype-dont-convert-mdx-correctly-in-nextjs-in-app-router
[10] Transforming Markdown with Remark & Rehype - ryanfiller.com https://www.ryanfiller.com/blog/remark-and-rehype-plugins
[11] How you guys using mdx-remote with rehype-pretty-code? : r/nextjs https://www.reddit.com/r/nextjs/comments/155mc7w/how_you_guys_using_mdxremote_with_rehypeprettycode/
[12] Trying to figure out why my formatting breaks with rehype-code-titles ... https://www.reddit.com/r/neovim/comments/1iqxr70/trying_to_figure_out_why_my_formatting_breaks/
[13] How to use Rehype Pretty Code with Nuxt3 markdown https://stackoverflow.com/questions/76588933/how-to-use-rehype-pretty-code-with-nuxt3-markdown
[14] `@shikijs/rehype`: support for inline code · Issue #660 - GitHub https://github.com/shikijs/shiki/issues/660
[15] onVisitHighlightedLine cannot push classname using Rehype Pretty ... https://stackoverflow.com/questions/76549262/onvisithighlightedline-cannot-push-classname-using-rehype-pretty-code
[16] Possibility to pass additional props to MDX custom components ... https://github.com/atomiks/rehype-pretty-code/issues/69
[17] How to use light and dark mode with Rehype Pretty Code https://stackoverflow.com/questions/73003034/how-to-use-light-and-dark-mode-with-rehype-pretty-code
[18] How I Used Unified, Remark, and Rehype to Build a ... - Ondrej Sevcik https://ondrejsevcik.com/blog/building-perfect-markdown-processor-for-my-blog
[19] rehypejs/rehype-highlight: plugin to highlight code blocks - GitHub https://github.com/rehypejs/rehype-highlight
[20] Markdown is not perfectly rendered in remix vite #2522 - GitHub https://github.com/orgs/mdx-js/discussions/2522
