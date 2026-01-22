---
docType: guide
layer: framework-guide
framework: nextjs
subject: markdown-rendering
audience: [human, ai]
description: Simplified guide to using markdown in Next.js without MDX complexity
---

# Markdown in Next.js

Simplified guide to using markdown in Next.js. Simple markdown, no unnecessary MDX or React in Markdown noise.

## How It Works

- **gray-matter** parses frontmatter metadata from your `.md` files.
- **remark** (with `remark-html`) converts markdown content into HTML.
- You render the HTML in your React components using `dangerouslySetInnerHTML`.

This approach is widely recommended, including in the official Next.js documentation and popular tutorials[1][5][3].

## Minimal Setup Steps

1. **Install dependencies:**
   ```bash
   npm install gray-matter remark remark-html
   ```

2. **Organize your markdown files:**
   - Place your `.md` files in a directory like `/posts` or `/data/blog`.
   - Each file starts with YAML frontmatter:
     ```
     ---
     title: My First Post
     date: 2025-05-09
     tags:
       - nextjs
       - markdown
     ---
     This is the content of my post.
     ```
   - You can define any frontmatter fields you want[1].

3. **Read and parse markdown in your data fetching function:**
   ```js
   import fs from 'fs'
   import path from 'path'
   import matter from 'gray-matter'
   import { remark } from 'remark'
   import html from 'remark-html'

   export async function getPostData(slug) {
     const fullPath = path.join('posts', `${slug}.md`)
     const fileContents = fs.readFileSync(fullPath, 'utf8')
     const matterResult = matter(fileContents)
     const processedContent = await remark().use(html).process(matterResult.content)
     const contentHtml = processedContent.toString()
     return {
       slug,
       contentHtml,
       ...matterResult.data,
     }
   }
   ```
   - This extracts both your frontmatter and the HTML content[5].

4. **Render your post:**
   ```jsx
   export default function Post({ postData }) {
     return (
       <article>
         <h1>{postData.title}</h1>
         <div dangerouslySetInnerHTML={{ __html: postData.contentHtml }} />
       </article>
     )
   }
   ```

## Why This Approach Is Great

- **No extra complexity:** No need for MDX, ContentLayer, or remote loaders.
- **Fast builds:** All parsing happens at build time, not in the client[2].
- **Flexible:** Easily supports any frontmatter fields you want.
- **Simple migration:** Feels very similar to Astro’s markdown content flow.

## References
- [Bionic Julia: Next.js Markdown Blog Setup][1]
- [Next.js Official Tutorial: Render Markdown][5]
- [TinaCMS: Simple Markdown Blog in Next.js][3]
- [CSS-Tricks: Responsible Markdown in Next.js][2]

**Bottom line:**  
If you just want markdown to drive content and don’t need JSX in your posts, gray-matter + remark is the best, simplest solution for Next.js.

### Important
NextJS will not apply any styles to your markdown by default (Astro does).  You will need to add them yourself.  The easiest way is to 



---[1] https://bionicjulia.com/blog/setting-up-nextjs-markdown-blog-with-typescript[2] https://css-tricks.com/responsible-markdown-in-next-js/[3] https://tina.io/blog/simple-markdown-blog-nextjs[5] https://nextjs.org/learn/pages-router/dynamic-routes-render-markdown

Sources
[1] Setting up a NextJS Markdown Blog with Typescript - Bionic Julia https://bionicjulia.com/blog/setting-up-nextjs-markdown-blog-with-typescript
[2] Responsible Markdown in Next.js - CSS-Tricks https://css-tricks.com/responsible-markdown-in-next-js/
[3] How To Create a Markdown Blog With Next.js - TinaCMS https://tina.io/blog/simple-markdown-blog-nextjs
[4] Guides: MDX - Next.js https://nextjs.org/docs/app/guides/mdx
[5] Render Markdown - Pages Router - Next.js https://nextjs.org/learn/pages-router/dynamic-routes-render-markdown
[6] Using Remark to Create an Interactive Table of Contents in a Next.js ... https://illacloud.com/blog/react-markdown
[7] How to get dynamic content without using Remark/Grey Matter https://stackoverflow.com/questions/70713346/how-to-get-dynamic-content-without-using-remark-grey-matter
[8] My Favorite Way to Use Markdown in NextJS - YouTube https://www.youtube.com/watch?v=YC6LqIYVHxI
[9] Building a Markdown blog using Next.js and Tailwind Typography https://dev.to/albac/building-a-markdown-blog-using-nextjs-and-tailwind-typography-41mf
[10] gray-matter and images for a next.js blog : r/nextjs - Reddit https://www.reddit.com/r/nextjs/comments/o5cjri/graymatter_and_images_for_a_nextjs_blog/
[11] How to add new element inside react-markdown content in nextjs ... https://stackoverflow.com/questions/76848688/how-to-add-new-element-inside-react-markdown-content-in-nextjs-without-using-jsx
[12] Simple blog with Next.js 13 + app router — MDX or otherwise https://stackoverflow.com/questions/76807144/simple-blog-with-next-js-13-app-router-mdx-or-otherwise
[13] A Powerful Combination of Markdown and MDX in Next.js for CMS https://staticmania.com/blog/markdown-and-mdx-in-next.js-a-powerful-combination-for-content-management
[14] In nextjs why use markdown for blog contents? : r/reactjs - Reddit https://www.reddit.com/r/reactjs/comments/16w23nw/in_nextjs_why_use_markdown_for_blog_contents/
[15] Blog Starter Kit - Vercel https://vercel.com/templates/next.js/blog-starter-kit
[16] How to use markdown rather than code to create pages in a Next.js ... https://dev.to/jameswallis/combining-markdown-and-dynamic-routes-to-make-a-more-maintainable-next-js-website-3ogl
[17] remarkjs/react-markdown: Markdown component for React - GitHub https://github.com/remarkjs/react-markdown
[18] Blending Markdown and React components in NextJS - Ed Spencer https://edspencer.net/2024/8/28/using-markdown-with-nextjs
[19] Example using Prism / Markdown with Next.js including ... - GitHub https://github.com/leerob/nextjs-prism-markdown
[20] Parse a Markdown Document With gray-matter - Egghead.io https://egghead.io/lessons/next-js-parse-a-markdown-document-with-gray-matter
