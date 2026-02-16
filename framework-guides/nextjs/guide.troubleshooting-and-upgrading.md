---
docType: guide
layer: framework-guide
framework: nextjs
subject: troubleshooting
audience: [human, ai]
description: Troubleshooting common Next.js issues and upgrade problems
dateUpdated: 20260121
---

# Next.js Troubleshooting and Upgrading

If encountering errors or difficulties when working with Next.js, consult this guide and the primary references listed in the introduction.

### Broken Transitions
FOUND IT! The ArticleCard is inside a CardCarousel that has a Framer Motion motion.div wrapper with animate={{ x: translateX }}. Framer Motion is taking control of the transform property and overriding CSS transforms.

This is the classic "Framer Motion vs CSS transforms" conflict. When Framer Motion animates x, it sets transform: translateX(...) on the element, which blocks CSS transform: scale() from working properly on child elements.

Quick fix - tell Framer Motion to NOT control transforms on the carousel children by adding style={{ transform: 'none' }} to the motion.div or switching to a different property.

Looking at the CardCarousel code:
```jsx
<motion.div
  animate={{ x: translateX }}
  transition={{ duration: 0.3 }}
  transformTemplate={({ x }) => `translateX(${x})`} // Preserve child transforms
  // ...
```

To fix, either do not use FramerMotion on the container, or update to use Transform instead of x.


### Should be Awaited or Types of Property are Incompatible
If encountering errors similar to the following, consult this guide and the two primary references listed in this introduction.

```sh
Error: Route "/blog/[slug]" used `params.slug`. `params` should be awaited before using its properties. 

Error: Types of property 'params' are incompatible.
Type '{ slug: string; }' is missing the following properties from type 'Promise<any>': then, catch, finally, [Symbol.toStringTag]
```

#### General Issue
You are encountering this error because **Next.js 15 introduced a breaking change:**  
**Dynamic route parameters (`params`) are now passed as a `Promise`** instead of a plain object. This affects all dynamic routes in the App Router, including `[slug]` pages.

#### Primary References
Upgrade Guide: https://nextjs.org/docs/app/guides/upgrading/version-15
Dynamic APIs: https://nextjs.org/docs/messages/sync-dynamic-apis

### Codemod
A codemod is available to automatically fix many issues related to upgrade from NextJS 14 to NextJS 15.  
Codemod: https://nextjs.org/docs/app/guides/upgrading/codemods#150


---

## **How to Fix**

### **1. Update Your Page Component Props**

**Old (Next.js 14 and below):**
```tsx
export default async function Page({ params }: { params: { slug: string } }) {
  // ...
}
```

**New (Next.js 15):**
```tsx
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  // ...
}
```
- **Notice:** `params` is now a `Promise<{ slug: string }>` and must be awaited before use[1][3][4][5][6][7].

---

### **2. Why This Change?**

- Next.js 15 made `params` asynchronous to support more flexible and powerful data fetching and route resolution[3][4][6].
- If you try to use `params` as a plain object, TypeScript will throw the error you saw:  
  > Type '{ slug: string; }' is missing the following properties from type 'Promise<any>': then, catch, finally, [Symbol.toStringTag][1][2][5][6].

---

### **3. Example Fix**

```tsx
// src/app/blog/[slug]/page.tsx

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  // ...rest of your code
}
```

- If your slug is an array (e.g., `[slug: string[]]`), adjust the type accordingly.

---

### **4. Additional Notes**

- This change applies to **all dynamic routes** in the App Router (including API routes)[3][4][5][6].
- Make sure to update all affected files in your project.
- If you have a lot of routes, there are codemods and scripts available to help automate this update[7].

---

## **Summary Table**

| Next.js Version | `params` Type in Page Props         | How to Access                        |
|-----------------|-------------------------------------|--------------------------------------|
| ≤ 14            | `{ slug: string }`                  | `params.slug`                        |
| 15+             | `Promise<{ slug: string }>`         | `const { slug } = await params;`     |

---

**In summary:**  
Update your page (and route) component signatures so that `params` is typed as a `Promise`, and always `await` it before accessing its properties. This will resolve the build error in Next.js 15[1][3][4][5][6][7].

## Additional Related Error
Yes, this error is directly related to the Next.js 15 breaking change where `params` became a Promise. Here's how to fix it:

---

## **Error Explanation**
```
Error: Route "/blog/[slug]" used `params.slug`.
`params` should be awaited before using its properties.
```
- **Cause**: You're accessing `params.slug` directly without first resolving the `params` Promise.
- **Location**: Your code at `src/app/blog/[slug]/page.tsx:16:22` contains `params.slug`.

---

## **Fix for Your Code**

### **Original Problematic Code**
```tsx
export default async function Page({ params }: PageProps) {
  const slug = params.slug; // <-- Error here
  // ...
}
```

### **Corrected Code**
```tsx
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params; // <-- Await first
  // ...
}
```
- **Key Change**: `params` is now a `Promise<{ slug: string }>`. You must `await` it before accessing `.slug`.

---

## **Alternative Fixes**

### **1. Coerce with `String()` (Quick Workaround)**
```tsx
export default async function Page({ params }: { params: { slug: string } }) {
  const slug = String(params.slug); // Works but not future-proof
  // ...
}
```

### **2. Access via Props (No Destructuring)**
```tsx
export default async function Page(props: { params: Promise<{ slug: string }> }) {
  const { slug } = await props.params;
  // ...
}
```

---

## **Full Example for Your Code**
```tsx
// src/app/blog/[slug]/page.tsx
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  let post: PostData;
  try {
    post = await getPostBySlug(slug);
  } catch (error) {
    notFound();
  }

  // Render post...
}
```

---

## **Important Notes**
- **Metadata Functions**: If you use `generateMetadata`, apply the same fix there:
  ```tsx
  export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = await params;
    // ...
  }
  ```
- **Backward Compatibility**: Next.js 15 allows synchronous access to `params` for now, but this will be deprecated. Fix it now to avoid future issues.

---

**References:**  
[Next.js 15 Upgrade Guide](https://nextjs.org/docs/messages/sync-dynamic-apis) | [Dynamic Routes Documentation](https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes)

Sources
[1] PageProps Type Errors in Next.js · community · Discussion #142577 https://github.com/orgs/community/discussions/142577
[2] Type 'Props' does not satisfy the constraint 'PageProps' Next.js 15.1.3 https://stackoverflow.com/questions/79332924/type-props-does-not-satisfy-the-constraint-pageprops-next-js-15-1-3
[3] How to fix Next.js 15 route export type errors - Array of Sunshine https://arrayofsunshine.co.uk/articles/how-to-fix-next-js-15-route-export-type-errors
[4] Next.js TypeScript error: 'param_type.params' incompatible with ... https://stackoverflow.com/questions/79370923/next-js-typescript-error-param-type-params-incompatible-with-paramcheckrou
[5] Type Error in Next.js Route: "Type '{ params: { id: string; }; }' does not ... https://stackoverflow.com/questions/79124951/type-error-in-next-js-route-type-params-id-string-does-not-satis
[6] Next.js 15 Build Fails: 'params' type mismatch (Promise) on dynamic ... https://github.com/vercel/next.js/issues/77609
[7] Type 'Props' does not satisfy the constraint 'PageProps' Next.js 15.1.3 https://www.reddit.com/r/nextjs/comments/1hux2pd/type_props_does_not_satisfy_the_constraint/
[8] Resolving "app/ Static to Dynamic Error" in Next.js https://nextjs.org/docs/messages/app-static-to-dynamic-error
[9] Solution to the Asynchronous Parameter Type Error in Next.js 15 ... https://en.kelen.cc/faq/solution-to-the-asynchronous-parameter-type-error-in-next.js-15-routing
[10] Type 'Props' does not satisfy the constraint 'PageProps ... - GitHub https://github.com/vercel/next.js/discussions/71997
[11] Next.js 15 Type Error: Invalid "GET" Export in Dynamic Route Handler https://www.reddit.com/r/nextjs/comments/1gooddy/nextjs_15_type_error_invalid_get_export_in/
[12] How to fix Next.js “Type error: Type 'Props' does not satisfy the ... https://dev.to/rubymuibi/how-to-fix-nextjs-type-error-type-props-does-not-satisfy-the-constraint-layoutprops-2n5a
[13] Routing: Error Handling - Next.js https://nextjs.org/docs/app/building-your-application/routing/error-handling
[14] Next.js 15 Dynamic Route Params Type Issue | Dev Log https://www.jeffknowlesjr.com/dev-log/nextjs-15-dynamic-route-params
[15] Custom App - Routing - Next.js https://nextjs.org/docs/pages/building-your-application/routing/custom-app
[16] Fixing the params.id Error in Next.js Dynamic Routes - LinkedIn https://www.linkedin.com/pulse/fixing-paramsid-error-nextjs-dynamic-routes-complete-guide-alam-08pzc
[17] Configuration: TypeScript - Next.js https://nextjs.org/docs/app/api-reference/config/typescript
[18] Strange behaviour in NextJS API routing. params is undefined ... https://github.com/vercel/next.js/discussions/58995
[19] Does not satisfy the constraint 'PageProps' - Help - Vercel Community https://community.vercel.com/t/does-not-satisfy-the-constraint-pageprops/3665
[20] Next JS Build Error - Code with Mosh Forum https://forum.codewithmosh.com/t/next-js-build-error/29815
