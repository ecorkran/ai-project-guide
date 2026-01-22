---
docType: guide
layer: framework-guide
framework: nextjs
subject: app-router-metadata
audience: [human, ai]
description: Managing metadata in Next.js App Router applications
---

# Developer Guide: Using Metadata in Next.js Apps with the App Router

This guide provides a concise, technical overview of managing metadata in Next.js applications using the App Router, focusing on best practices and implementation patterns. For official documentation and further details, refer to: https://nextjs.org/docs/app/getting-started/metadata-and-og-images#best-practices

## **Overview**

Next.js offers a robust Metadata API for defining SEO-related tags (e.g., `<meta>`, `<link>`) in your app's HTML head. This API is tightly integrated into the App Router, supporting both static and dynamic metadata at the page and layout level[1][2][3][13].

## **Metadata Implementation Patterns**

### **1. Static Metadata**

For routes where metadata does not depend on runtime data, export a static `metadata` object from your `layout.js` or `page.js` file:

```js
// app/page.js
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Next.js App',
  description: 'A concise description for SEO.',
  openGraph: {
    title: 'My Next.js App',
    description: 'A concise description for SEO.',
    images: ['/og-image.png'],
  },
};
```
This approach is simple and preferred for static content[13][10].

### **2. Dynamic Metadata**

For routes where metadata depends on route parameters, fetched data, or needs to extend parent metadata, export an async `generateMetadata` function:

```js
// app/posts/[id]/page.js
import type { Metadata, ResolvingMetadata } from 'next';
import { getPostData } from '@/lib/posts';

export async function generateMetadata({ params }, parent: ResolvingMetadata): Promise<Metadata> {
  const post = await getPostData(params.id);
  const previousImages = (await parent).openGraph?.images || [];
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: ['/dynamic-og-image.jpg', ...previousImages],
    },
  };
}
```
Use this pattern for dynamic pages, such as blogs or product details[6][13].

### **3. Metadata Inheritance and Composition**

- Metadata defined in a layout is inherited by nested pages.
- Child routes can extend or override parent metadata.
- Use the `parent` parameter in `generateMetadata` to access and build upon parent metadata[13].

### **4. Metadata Fields and Best Practices**

- **Common fields:** `title`, `description`, `keywords`, `openGraph`, `twitter`, `robots`, `viewport`, `appleWebApp`, etc.
- **Comprehensive coverage:** Combine multiple metadata fields for SEO and social sharing.
- **Consistency:** Define shared metadata at the root layout for global consistency[10].
- **Relevance:** Tailor metadata to each page for better search and share previews[10].
- **Avoid duplicates:** Ensure no conflicting or duplicate keys across nested metadata objects[10].

### **5. Absolute URLs and `metadataBase`**

For any metadata fields requiring absolute URLs (e.g., Open Graph images), set a `metadataBase` in your root layout:

```js
// app/layout.js
export const metadata = {
  metadataBase: new URL('https://yourdomain.com'),
  // ...other fields
};
```
This ensures all relative URLs are resolved correctly[13][8].

### **6. Custom Meta Tags**

To add custom meta tags (e.g., `<meta property="product:brand" ...>`), use the `other` field in the metadata object. Note: Next.js will render these as `<meta name="...">` by default; for specialized needs, consider contributing to the framework or using a custom Head component if absolutely necessary[11].

## **SEO and Performance Considerations**

- **Streaming Metadata:** Next.js streams metadata for bots that can execute JavaScript, improving crawl efficiency. For HTML-limited bots, metadata blocks rendering until ready. You can customize bot detection via `htmlLimitedBots` in `next.config.js`[13].
- **Static vs. Dynamic:** Prefer static metadata for performance unless dynamic data is required[8].
- **OG Images:** Generate and cache Open Graph images for social sharing previews[2].

## **Best Practices Summary**

> - Use static metadata where possible for simplicity and performance.
> - Use `generateMetadata` for dynamic or parameterized routes.
> - Define `metadataBase` for consistent absolute URLs.
> - Combine multiple metadata fields for SEO and social sharing.
> - Avoid duplicate or conflicting metadata keys.
> - Place shared metadata in the top-most layout to propagate to nested routes.
> - Refer to the official guide for more: https://nextjs.org/docs/app/getting-started/metadata-and-og-images#best-practices

## **References**

- [Next.js Metadata and OG Images Best Practices](https://nextjs.org/docs/app/getting-started/metadata-and-og-images#best-practices)
- [Next.js Metadata API Reference][13]
- [Dynamic Metadata Example][6]
- [SEO Optimization with Metadata][4][5]

---

This guide is designed for developers building modern Next.js applications with the App Router, enabling robust, maintainable, and SEO-friendly metadata management.

Sources
[1] Optimizing: Metadata | Next.js https://nextjs.org/docs/app/building-your-application/optimizing/metadata
[2] Getting Started: Metadata and OG images - Next.js https://nextjs.org/docs/app/getting-started/metadata-and-og-images
[3] Adding Metadata - App Router - Next.js https://nextjs.org/learn/dashboard-app/adding-metadata
[4] Maximizing SEO with Meta Data in Next.js 15 - DEV Community https://dev.to/joodi/maximizing-seo-with-meta-data-in-nextjs-15-a-comprehensive-guide-4pa7
[5] Practical Guide to Implementing Functional SEO in NextJS App Router https://dev.to/cre8stevedev/practical-guide-to-implementing-functional-seo-in-nextjs-app-router-static-dynamic-metadata-4ae2
[6] Creating Dynamic Metadata with Next.js - StaticMania https://staticmania.com/blog/creating-dynamic-metadata-with-nextjs
[7] Next.js 14 - SEO & Metadata Tutorial (Complete Guide) - YouTube https://www.youtube.com/watch?v=a2ovCcxXqNo
[8] Managing Metadata in Next.js 14 for Enhanced SEO and User ... https://devarshi.dev/blog/managing-metadata-in-nextjs14-for-seo
[9] The New Metadata API in NextJs 13 - YouTube https://www.youtube.com/watch?v=cacys-rrQN8
[10] Mastering Next.js Metadata for Enhanced Web Visibility - DhiWise https://www.dhiwise.com/post/mastering-nextjs-metadata-for-enhanced-web-visibility
[11] How to add new custom meta property in nextjs app router? https://stackoverflow.com/questions/77959830/how-to-add-new-custom-meta-property-in-nextjs-app-router
[12] How to create dynamic title and meta data using next 13.2.3 pages ... https://www.reddit.com/r/nextjs/comments/14zd3y0/how_to_create_dynamic_title_and_meta_data_using/
[13] Functions: generateMetadata - Next.js https://nextjs.org/docs/app/api-reference/functions/generate-metadata
[14] Dynamic routing and metadata generation in Next.js app router https://stackoverflow.com/questions/76548863/dynamic-routing-and-metadata-generation-in-next-js-app-router
[15] Next.js metadata vs React 19 title and meta components #75054 https://github.com/vercel/next.js/discussions/75054
[16] New Metadata support and "use client" : r/nextjs - Reddit https://www.reddit.com/r/nextjs/comments/11fjnpq/new_metadata_support_and_use_client/
