# Guia 1

Build a fullscreen hero landing page for a creative agency called "VANGUARD" using React, Tailwind CSS, and Vite. The page should be a single viewport-height section with a looping background video and all content overlaid on top.

\*\*Background video:\*\*  
Use this exact CloudFront URL as a fullscreen \`\<video\>\` element with \`autoPlay\`, \`muted\`, \`loop\`, and \`playsInline\` attributes, set to \`object-cover\` to fill the entire viewport:  
\`\`\`  
https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260606\_154941\_df1a96e1-a06f-450c-bd02-d863414cc1a0.mp4  
\`\`\`

\*\*Fonts (loaded in index.html):\*\*  
1\. "FSP DEMO \- PODIUM Sharp 4.11" from \`https://db.onlinewebfonts.com/c/8b75d9dcff6a48c35a46656192adf019?family=FSP+DEMO+-+PODIUM+Sharp+4.11\` \-- used for the brand name and main heading. Create a \`.font-podium\` utility class for it and register it in tailwind.config.js as \`fontFamily.podium\`.  
2\. "Inter" from Google Fonts (weights 400, 500, 600, 700\) \-- used for body text, nav links, stats, and CTAs. Register it in tailwind.config.js as \`fontFamily.inter\`.

\*\*Icons:\*\* Use \`lucide-react\` for all icons: \`ArrowUpRight\`, \`Award\`, \`Crown\`, and \`X\`.

\*\*Navbar:\*\*  
\- Horizontal bar at the top with responsive padding (\`px-6 sm:px-10 lg:px-16\`, \`py-5 lg:py-7\`).  
\- Left: brand name "VANGUARD" in \`font-podium\`, white, bold, uppercase, \`text-2xl sm:text-3xl\`, \`tracking-wider\`.  
\- Center (hidden below \`md\`): four nav links \-- "Projects", "Studio", "Offerings", "Inquire" \-- in \`font-inter\`, \`text-sm\`, \`text-white/80\`, \`tracking-widest\`, uppercase, with \`hover:text-white\` transition.  
\- Right (hidden below \`md\`): a "GET IN TOUCH" link with an \`ArrowUpRight\` icon, styled as a bordered button (\`border border-white/30 hover:border-white/60\`, \`px-6 py-3\`, \`text-xs\`, \`tracking-widest\`, uppercase, \`hover:bg-white/10\`).  
\- Right (visible below \`md\`): a hamburger button made of three white \`div\` bars (\`w-6 h-0.5\`, \`w-6 h-0.5\`, \`w-4 h-0.5\` with \`space-y-1.5\`).

\*\*Mobile Menu Overlay (below \`md\` only):\*\*  
\- Fixed fullscreen overlay (\`fixed inset-0 z-50\`) with \`bg-black/95 backdrop-blur-sm\`.  
\- Toggles visibility via React \`useState\` \-- when open: \`opacity-100 visible\`, when closed: \`opacity-0 invisible\`, with \`transition-all duration-500\`.  
\- Header row matches the navbar: brand name on left, \`X\` close icon on right.  
\- Centered vertically: each of the 4 nav links rendered in \`font-podium\`, \`text-4xl sm:text-5xl\`, white, uppercase, with staggered entrance animations using inline \`style\` \-- each item gets \`transitionDelay: i \* 80 \+ 100ms\`, \`opacity\` and \`translateY(20px)\` transitions based on the open state.  
\- Below the links: a "GET IN TOUCH" bordered button with the same staggered animation pattern.  
\- All links call \`setMenuOpen(false)\` on click.

\*\*Hero Content (vertically centered, left-aligned):\*\*  
All hero elements use staggered \`animate-fade-up\` animations (defined in CSS as \`@keyframes fade-up\` translating from \`translateY(30px), opacity:0\` to \`translateY(0), opacity:1\` over \`0.8s ease-out\`). Each successive element has an additional \`0.2s\` delay. Elements start with \`opacity: 0\` and use \`animation-fill-mode: forwards\`.

1\. \*\*Tagline:\*\* A \`Crown\` icon (lucide, \`w-4 h-4\`, \`text-white/70\`) followed by "World-Class Digital Collective" in \`text-white/70\`, \`text-xs sm:text-sm\`, \`font-inter\`, \`tracking-\[0.3em\]\`, uppercase. Uses \`animate-fade-up\` (no delay). Has \`mb-6 lg:mb-8\`.

2\. \*\*Main Heading:\*\* Three lines in \`font-podium\`, white, uppercase, \`leading-\[0.92\]\`, \`tracking-tight\`, each using \`text-\[clamp(2.8rem,8vw,7rem)\]\`:  
   \- "Design."  
   \- "Disrupt."  
   \- "Conquer."  
   Uses \`animate-fade-up-delay-1\` (0.2s delay).

3\. \*\*Subtext:\*\* "We build fierce brand identities" (line break) "that don't just turn heads \--" then bold white "they lead." in \`text-white/70\`, \`text-sm sm:text-base\`, \`font-inter\`, \`leading-relaxed\`, \`max-w-md\`. Uses \`animate-fade-up-delay-2\` (0.4s delay). \`mt-6 lg:mt-8\`.

4\. \*\*CTA Row:\*\* Uses \`animate-fade-up-delay-3\` (0.6s delay), \`mt-8 lg:mt-10\`, \`flex flex-wrap items-center gap-4 sm:gap-6\`.  
   \- Black button "SEE OUR WORK" with \`ArrowUpRight\` icon. \`bg-black hover:bg-neutral-900\`, \`px-5 sm:px-7 py-3 sm:py-4\`, \`text-\[11px\] sm:text-xs\`, \`tracking-widest\`, uppercase. Arrow has \`group-hover:translate-x-0.5 group-hover:-translate-y-0.5\` transition.  
   \- Beside it (hidden on mobile, \`hidden sm:flex\`): an \`Award\` icon (\`w-8 h-8\`, \`text-white/50\`) with two lines of text: "Top-Rated" / "Brand Studio" in \`text-white/60\`, \`text-xs\`, \`tracking-wider\`, uppercase.

5\. \*\*Stats Row:\*\* Uses \`animate-fade-up-delay-4\` (0.8s delay), \`mt-8 sm:mt-10 lg:mt-14\`, \`flex flex-wrap gap-6 sm:gap-12 lg:gap-16\`. Three stats:  
   \- "250+" / "Brands Transformed"  
   \- "95%" / "Client Retention"  
   \- "10+" / "Years in the Game"  
   Values in \`font-inter\`, white, \`text-2xl sm:text-4xl lg:text-5xl\`, bold, \`tracking-tight\`. Labels in \`text-white/50\`, \`text-\[9px\] sm:text-xs\`, \`tracking-widest\`, uppercase, \`mt-1\`.

\*\*CSS Animations (defined in index.css under \`@layer utilities\`):\*\*  
\`\`\`css  
@keyframes fade-up {  
  from { opacity: 0; transform: translateY(30px); }  
  to { opacity: 1; transform: translateY(0); }  
}  
@keyframes fade-in {  
  from { opacity: 0; }  
  to { opacity: 1; }  
}  
@keyframes scale-in {  
  from { opacity: 0; transform: scale(0.9); }  
  to { opacity: 1; transform: scale(1); }  
}  
\`\`\`  
With classes: \`.animate-fade-up\` (0s delay), \`.animate-fade-up-delay-1\` through \`.animate-fade-up-delay-4\` (0.2s increments, starting \`opacity: 0\`), \`.animate-fade-in\`, \`.animate-fade-in-delay\`.

\*\*Responsive behavior:\*\*  
\- Full layout is mobile-first with breakpoints at \`sm\` (640px), \`md\` (768px), and \`lg\` (1024px).  
\- Nav links and "GET IN TOUCH" button show at \`md\`+; hamburger shows below \`md\`.  
\- Award badge hides on mobile (\`hidden sm:flex\`).  
\- All text sizes, paddings, gaps, and margins scale up through \`sm:\` and \`lg:\` prefixes.  
\- Stats and CTA row use \`flex-wrap\` to prevent overflow on small screens.

Make everything fully mobile responsive. Use a single \`App.tsx\` component with \`useState\` for the menu toggle. No routing needed.

# Guia 2

Build a full-screen, dark-themed hero section for a geology brand called \*\*Lithos\*\*, using \*\*React 18 \+ TypeScript \+ Vite \+ Tailwind CSS\*\* and \*\*lucide-react\*\* for icons. The signature feature is a \*\*cursor-following spotlight that reveals a second image\*\* through a soft circular mask on top of a base image. Match every detail below exactly.

\#\#\# Fonts  
Add this to the top of \`src/index.css\`, then \`@tailwind base/components/utilities\`:  
\`\`\`css  
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700\&family=Playfair+Display:ital,wght@1,400;1,500;1,600\&display=swap');  
\* { font-family: 'Inter', sans-serif; }  
.font-playfair { font-family: 'Playfair Display', serif; }  
\`\`\`  
\- Body/UI font: \*\*Inter\*\*.  
\- Display/wordmark accent: \*\*Playfair Display, italic\*\*.

\#\#\# Asset URLs (use these exactly)  
\- Base image (\`BG\_IMAGE\_1\`):  
  \`https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260609\_195923\_b0ba8ace-1d1d-4f2c-9a28-1ab84b330680.png\&w=1280\&q=85\`  
\- Reveal image (\`BG\_IMAGE\_2\`):  
  \`https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260609\_201152\_bba90a12-bf12-459f-91f0-51f237dbaf3b.png\&w=1280\&q=85\`

\#\#\# Layout & structure  
Root wrapper: \`min-h-screen bg-white tracking-\[-0.02em\]\`, inline \`fontFamily: "'Inter', sans-serif"\`.

\*\*Section\*\* (\`\<section\>\`): \`relative w-full overflow-hidden h-screen bg-black\`, inline \`style={{ height: '100dvh' }}\`. Layers, by z-index:  
1\. \*\*Base image\*\* (\`z-10\`): \`absolute inset-0 bg-center bg-cover bg-no-repeat\`, background \= \`BG\_IMAGE\_1\`.  
2\. \*\*Reveal layer\*\* (\`z-30\`): a \`RevealLayer\` component (see below) showing \`BG\_IMAGE\_2\`.  
3\. \*\*Heading\*\* (\`z-50\`): \`absolute top-\[14%\] left-0 right-0 flex flex-col items-center text-center px-5 pointer-events-none\`. An \`\<h1\>\` with \`text-white leading-\[0.95\]\` containing two block spans:  
   \- Line 1: \`block font-playfair italic font-normal text-5xl sm:text-7xl md:text-8xl\`, inline \`letterSpacing: '-0.05em'\`, text \*\*"Layers hold"\*\*.  
   \- Line 2: \`block font-normal text-5xl sm:text-7xl md:text-8xl \-mt-1\`, inline \`letterSpacing: '-0.08em'\`, text \*\*"tales of time"\*\*.  
4\. \*\*Bottom-left paragraph\*\* (\`z-50\`): \`hidden sm:block absolute bottom-14 left-10 md:left-14 max-w-\[260px\]\`. \`\<p className="text-sm text-white/80 leading-relaxed"\>\` — "Every layer of sediment records a chapter of our planet, from ancient seabeds to drifting ash, layered across millions of years beneath us."  
5\. \*\*Bottom-right block\*\* (\`z-50\`): \`absolute bottom-10 sm:bottom-24 left-5 right-5 sm:left-auto sm:right-10 md:right-14 max-w-full sm:max-w-\[260px\] flex flex-col items-start gap-4 sm:gap-5\`. Contains a \`\<p className="text-xs sm:text-sm text-white/80 leading-relaxed"\>\` — "Our interactive maps let you peel back the crust to trace how stones, fossils, and deep time combine to shape the ground beneath your feet." — and a \*\*Start Digging\*\* button: \`bg-\[\#e8702a\] hover:bg-\[\#d2611f\] text-white text-sm font-medium px-7 py-3 rounded-full transition-all hover:scale-\[1.03\] active:scale-95 hover:shadow-lg hover:shadow-\[\#e8702a\]/30\`.

\#\#\# The cursor spotlight reveal (core mechanic)  
In the parent, define \`const SPOTLIGHT\_R \= 260;\` and track the mouse with smoothing:  
\- Refs: \`mouse\` (raw), \`smooth\` (eased), \`rafRef\`; state \`cursorPos\` (init \`{x:-999,y:-999}\`).  
\- \`mousemove\` listener stores raw \`e.clientX/clientY\`.  
\- A \`requestAnimationFrame\` loop lerps: \`smooth.x \+= (mouse.x \- smooth.x) \* 0.1\` (same for y), then \`setCursorPos\`. Clean up listener \+ cancel RAF on unmount.

\`RevealLayer({ image, cursorX, cursorY })\`:  
\- Holds a hidden \`\<canvas\>\` (\`absolute inset-0 pointer-events-none\`, \`style={{display:'none'}}\`) sized to \`window.innerWidth/Height\` on mount \+ resize.  
\- A reveal \`\<div\>\` (\`absolute inset-0 bg-center bg-cover bg-no-repeat z-30 pointer-events-none\`) with the reveal image as background.  
\- On every render: clear canvas, build a \*\*radial gradient\*\* at \`(cursorX, cursorY)\` from radius 0 → \`SPOTLIGHT\_R\` with stops:  
  \`0 → rgba(255,255,255,1)\`, \`0.4 → 1\`, \`0.6 → 0.75\`, \`0.75 → 0.4\`, \`0.88 → 0.12\`, \`1 → 0\`.  
  Fill an arc of radius \`SPOTLIGHT\_R\` with it. Then \`canvas.toDataURL()\` and apply it as \`maskImage\`/\`webkitMaskImage\` on the reveal div with \`maskSize: '100% 100%'\`. This makes the second image visible only inside the soft glowing circle that trails the cursor.

\#\#\# Navigation (fixed, over hero)  
\`\<nav className="fixed top-0 left-0 right-0 z-\[100\] flex items-center justify-between p-4 sm:p-5"\>\`:  
\- \*\*Left\*\*: an inline SVG logo (26×26, viewBox \`0 0 256 256\`, \`fill="\#ffffff"\`, path \`M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z\`) \+ wordmark \`\<span className="text-white text-2xl font-playfair italic"\>Lithos\</span\>\`.  
\- \*\*Center pill\*\* (\`hidden md:flex absolute left-1/2 \-translate-x-1/2 bg-white/20 backdrop-blur-md border border-white/30 rounded-full px-2 py-2 items-center gap-1\`): buttons \*\*Course\*\* (active: full white text), then \*\*Field Guides, Geology, Plans, Live Tour\*\* (\`text-white/80 ... hover:bg-white/20 hover:text-white transition-colors\`, \`px-4 py-1.5 rounded-full text-sm font-medium\`).  
\- \*\*Right (desktop)\*\*: \`hidden md:block bg-white text-gray-900 text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-gray-100\` — \*\*Sign Up\*\*.

\#\#\# Animations (premium, on load)  
Add to \`index.css\`:  
\`\`\`css  
@keyframes heroReveal { 0%{opacity:0;transform:translateY(28px);filter:blur(12px)} 100%{opacity:1;transform:translateY(0);filter:blur(0)} }  
@keyframes heroFadeUp { 0%{opacity:0;transform:translateY(20px)} 100%{opacity:1;transform:translateY(0)} }  
@keyframes heroZoom { 0%{transform:scale(1.12)} 100%{transform:scale(1)} }  
.hero-anim { opacity:0; animation-fill-mode:forwards; animation-timing-function:cubic-bezier(0.16,1,0.3,1); }  
.hero-reveal { animation-name:heroReveal; animation-duration:1.1s; }  
.hero-fade { animation-name:heroFadeUp; animation-duration:1s; }  
.hero-zoom { animation:heroZoom 1.8s cubic-bezier(0.16,1,0.3,1) forwards; }  
@media (prefers-reduced-motion: reduce){ .hero-anim,.hero-zoom{ animation:none; opacity:1; } }  
\`\`\`  
Apply:  
\- Base image div → add \`hero-zoom\` (slow Ken Burns zoom-out).  
\- Heading line 1 → \`hero-anim hero-reveal\`, inline \`animationDelay: '0.25s'\`; line 2 → same with \`'0.42s'\` (blur-rise, staggered).  
\- Bottom-left paragraph wrapper → \`hero-anim hero-fade\`, \`animationDelay: '0.7s'\`.  
\- Bottom-right wrapper → \`hero-anim hero-fade\`, \`animationDelay: '0.85s'\`.

\#\#\# Responsiveness  
\- Heading scales \`text-5xl\` → \`sm:text-7xl\` → \`md:text-8xl\`.  
\- Center nav pill and desktop Sign Up are \`hidden\` below \`md\`; the mobile hamburger is \`md:hidden\`.  
\- Bottom-left paragraph is \`hidden sm:block\`; bottom-right block is full-width on mobile (\`left-5 right-5\`) and right-anchored from \`sm\`.  
\- Use \`100dvh\` so mobile browser chrome doesn't clip the section.

# Guia 3

Build a full-screen, dark-themed hero section for a geology brand called \*\*Lithos\*\*, using \*\*React 18 \+ TypeScript \+ Vite \+ Tailwind CSS\*\* and \*\*lucide-react\*\* for icons. The signature feature is a \*\*cursor-following spotlight that reveals a second image\*\* through a soft circular mask on top of a base image. Match every detail below exactly.

\#\#\# Fonts  
Add this to the top of \`src/index.css\`, then \`@tailwind base/components/utilities\`:  
\`\`\`css  
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700\&family=Playfair+Display:ital,wght@1,400;1,500;1,600\&display=swap');  
\* { font-family: 'Inter', sans-serif; }  
.font-playfair { font-family: 'Playfair Display', serif; }  
\`\`\`  
\- Body/UI font: \*\*Inter\*\*.  
\- Display/wordmark accent: \*\*Playfair Display, italic\*\*.

\#\#\# Asset URLs (use these exactly)  
\- Base image (\`BG\_IMAGE\_1\`):  
  \`https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260609\_195923\_b0ba8ace-1d1d-4f2c-9a28-1ab84b330680.png\&w=1280\&q=85\`  
\- Reveal image (\`BG\_IMAGE\_2\`):  
  \`https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260609\_201152\_bba90a12-bf12-459f-91f0-51f237dbaf3b.png\&w=1280\&q=85\`

\#\#\# Layout & structure  
Root wrapper: \`min-h-screen bg-white tracking-\[-0.02em\]\`, inline \`fontFamily: "'Inter', sans-serif"\`.

\*\*Section\*\* (\`\<section\>\`): \`relative w-full overflow-hidden h-screen bg-black\`, inline \`style={{ height: '100dvh' }}\`. Layers, by z-index:  
1\. \*\*Base image\*\* (\`z-10\`): \`absolute inset-0 bg-center bg-cover bg-no-repeat\`, background \= \`BG\_IMAGE\_1\`.  
2\. \*\*Reveal layer\*\* (\`z-30\`): a \`RevealLayer\` component (see below) showing \`BG\_IMAGE\_2\`.  
3\. \*\*Heading\*\* (\`z-50\`): \`absolute top-\[14%\] left-0 right-0 flex flex-col items-center text-center px-5 pointer-events-none\`. An \`\<h1\>\` with \`text-white leading-\[0.95\]\` containing two block spans:  
   \- Line 1: \`block font-playfair italic font-normal text-5xl sm:text-7xl md:text-8xl\`, inline \`letterSpacing: '-0.05em'\`, text \*\*"Layers hold"\*\*.  
   \- Line 2: \`block font-normal text-5xl sm:text-7xl md:text-8xl \-mt-1\`, inline \`letterSpacing: '-0.08em'\`, text \*\*"tales of time"\*\*.  
4\. \*\*Bottom-left paragraph\*\* (\`z-50\`): \`hidden sm:block absolute bottom-14 left-10 md:left-14 max-w-\[260px\]\`. \`\<p className="text-sm text-white/80 leading-relaxed"\>\` — "Every layer of sediment records a chapter of our planet, from ancient seabeds to drifting ash, layered across millions of years beneath us."  
5\. \*\*Bottom-right block\*\* (\`z-50\`): \`absolute bottom-10 sm:bottom-24 left-5 right-5 sm:left-auto sm:right-10 md:right-14 max-w-full sm:max-w-\[260px\] flex flex-col items-start gap-4 sm:gap-5\`. Contains a \`\<p className="text-xs sm:text-sm text-white/80 leading-relaxed"\>\` — "Our interactive maps let you peel back the crust to trace how stones, fossils, and deep time combine to shape the ground beneath your feet." — and a \*\*Start Digging\*\* button: \`bg-\[\#e8702a\] hover:bg-\[\#d2611f\] text-white text-sm font-medium px-7 py-3 rounded-full transition-all hover:scale-\[1.03\] active:scale-95 hover:shadow-lg hover:shadow-\[\#e8702a\]/30\`.

\#\#\# The cursor spotlight reveal (core mechanic)  
In the parent, define \`const SPOTLIGHT\_R \= 260;\` and track the mouse with smoothing:  
\- Refs: \`mouse\` (raw), \`smooth\` (eased), \`rafRef\`; state \`cursorPos\` (init \`{x:-999,y:-999}\`).  
\- \`mousemove\` listener stores raw \`e.clientX/clientY\`.  
\- A \`requestAnimationFrame\` loop lerps: \`smooth.x \+= (mouse.x \- smooth.x) \* 0.1\` (same for y), then \`setCursorPos\`. Clean up listener \+ cancel RAF on unmount.

\`RevealLayer({ image, cursorX, cursorY })\`:  
\- Holds a hidden \`\<canvas\>\` (\`absolute inset-0 pointer-events-none\`, \`style={{display:'none'}}\`) sized to \`window.innerWidth/Height\` on mount \+ resize.  
\- A reveal \`\<div\>\` (\`absolute inset-0 bg-center bg-cover bg-no-repeat z-30 pointer-events-none\`) with the reveal image as background.  
\- On every render: clear canvas, build a \*\*radial gradient\*\* at \`(cursorX, cursorY)\` from radius 0 → \`SPOTLIGHT\_R\` with stops:  
  \`0 → rgba(255,255,255,1)\`, \`0.4 → 1\`, \`0.6 → 0.75\`, \`0.75 → 0.4\`, \`0.88 → 0.12\`, \`1 → 0\`.  
  Fill an arc of radius \`SPOTLIGHT\_R\` with it. Then \`canvas.toDataURL()\` and apply it as \`maskImage\`/\`webkitMaskImage\` on the reveal div with \`maskSize: '100% 100%'\`. This makes the second image visible only inside the soft glowing circle that trails the cursor.

\#\#\# Navigation (fixed, over hero)  
\`\<nav className="fixed top-0 left-0 right-0 z-\[100\] flex items-center justify-between p-4 sm:p-5"\>\`:  
\- \*\*Left\*\*: an inline SVG logo (26×26, viewBox \`0 0 256 256\`, \`fill="\#ffffff"\`, path \`M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z\`) \+ wordmark \`\<span className="text-white text-2xl font-playfair italic"\>Lithos\</span\>\`.  
\- \*\*Center pill\*\* (\`hidden md:flex absolute left-1/2 \-translate-x-1/2 bg-white/20 backdrop-blur-md border border-white/30 rounded-full px-2 py-2 items-center gap-1\`): buttons \*\*Course\*\* (active: full white text), then \*\*Field Guides, Geology, Plans, Live Tour\*\* (\`text-white/80 ... hover:bg-white/20 hover:text-white transition-colors\`, \`px-4 py-1.5 rounded-full text-sm font-medium\`).  
\- \*\*Right (desktop)\*\*: \`hidden md:block bg-white text-gray-900 text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-gray-100\` — \*\*Sign Up\*\*.

\#\#\# Animations (premium, on load)  
Add to \`index.css\`:  
\`\`\`css  
@keyframes heroReveal { 0%{opacity:0;transform:translateY(28px);filter:blur(12px)} 100%{opacity:1;transform:translateY(0);filter:blur(0)} }  
@keyframes heroFadeUp { 0%{opacity:0;transform:translateY(20px)} 100%{opacity:1;transform:translateY(0)} }  
@keyframes heroZoom { 0%{transform:scale(1.12)} 100%{transform:scale(1)} }  
.hero-anim { opacity:0; animation-fill-mode:forwards; animation-timing-function:cubic-bezier(0.16,1,0.3,1); }  
.hero-reveal { animation-name:heroReveal; animation-duration:1.1s; }  
.hero-fade { animation-name:heroFadeUp; animation-duration:1s; }  
.hero-zoom { animation:heroZoom 1.8s cubic-bezier(0.16,1,0.3,1) forwards; }  
@media (prefers-reduced-motion: reduce){ .hero-anim,.hero-zoom{ animation:none; opacity:1; } }  
\`\`\`  
Apply:  
\- Base image div → add \`hero-zoom\` (slow Ken Burns zoom-out).  
\- Heading line 1 → \`hero-anim hero-reveal\`, inline \`animationDelay: '0.25s'\`; line 2 → same with \`'0.42s'\` (blur-rise, staggered).  
\- Bottom-left paragraph wrapper → \`hero-anim hero-fade\`, \`animationDelay: '0.7s'\`.  
\- Bottom-right wrapper → \`hero-anim hero-fade\`, \`animationDelay: '0.85s'\`.

\#\#\# Responsiveness  
\- Heading scales \`text-5xl\` → \`sm:text-7xl\` → \`md:text-8xl\`.  
\- Center nav pill and desktop Sign Up are \`hidden\` below \`md\`; the mobile hamburger is \`md:hidden\`.  
\- Bottom-left paragraph is \`hidden sm:block\`; bottom-right block is full-width on mobile (\`left-5 right-5\`) and right-anchored from \`sm\`.  
\- Use \`100dvh\` so mobile browser chrome doesn't clip the section.

# Guia 4

Build a 3D Creator portfolio landing page for "Jack" using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React. The page has a dark theme (\#0C0C0C background) with the font Kanit (Google Fonts, weights 300-900). The page title is "Jack \-- 3D Creator".

GLOBAL STYLES  
Background: \#0C0C0C on html, body, \#root, and the main wrapper  
Font family: 'Kanit', sans-serif  
Global reset: box-sizing border-box, margin 0, padding 0  
CSS class .hero-heading: gradient text using background: linear-gradient(180deg, \#646973 0%, \#BBCCD7 100%) with \-webkit-background-clip: text and \-webkit-text-fill-color: transparent  
Main wrapper has overflowX: 'clip'  
SECTION ORDER  
HeroSection  
MarqueeSection  
AboutSection  
ServicesSection  
ProjectsSection  
1\. HERO SECTION  
Full viewport height (h-screen), flex column layout with overflowX: clip.

Navbar: Horizontal nav bar with 4 links \-- "About", "Price", "Projects", "Contact" \-- evenly spaced with justify-between. Text color \#D7E2EA, font-medium, uppercase, tracking-wider. Sizes: text-sm md:text-lg lg:text-\[1.4rem\]. Padding: px-6 md:px-10 pt-6 md:pt-8. Hover: opacity 70% with 200ms transition.

Hero Heading: Massive h1 with text "Hi, i'm jack" (lowercase "i", curly apostrophe via \&apos;). Uses the .hero-heading gradient text class. Font-black, uppercase, tracking-tight, leading-none, whitespace-nowrap, w-full. Font sizes: text-\[14vw\] sm:text-\[15vw\] md:text-\[16vw\] lg:text-\[17.5vw\]. Margin top: mt-6 sm:mt-4 md:-mt-5. Wrapped in overflow-hidden container.

Bottom bar: Flexbox justify-between items-end with pb-7 sm:pb-8 md:pb-10:

Left: paragraph text "a 3d creator driven by crafting striking and unforgettable projects", color \#D7E2EA, font-light, uppercase, tracking-wide, leading-snug. Font size: clamp(0.75rem, 1.4vw, 1.5rem). Max-width: max-w-\[160px\] sm:max-w-\[220px\] md:max-w-\[260px\].  
Right: ContactButton component (see below)  
Hero Portrait: Centered absolutely. Uses a Magnet component (mouse-following magnetic effect) wrapping an image. Image URL: https://shrug-person-78902957.figma.site/\_components/v2/d24c01ad3a56fc65e942a1f501eb73db42d7cf9a/Rectangle\_40443.81459862.png. Magnet settings: padding 150, strength 3, activeTransition "transform 0.3s ease-out", inactiveTransition "transform 0.6s ease-in-out". Positioning: absolute left-1/2 \-translate-x-1/2 z-10. Width: w-\[280px\] sm:w-\[360px\] md:w-\[440px\] lg:w-\[520px\]. On mobile: top-1/2 \-translate-y-1/2. On sm+: sm:top-auto sm:translate-y-0 sm:bottom-0.

FadeIn animations: Navbar fades in with delay 0, y \-20. Heading: delay 0.15, y 40\. Left text: delay 0.35, y 20\. Contact button: delay 0.5, y 20\. Portrait: delay 0.6, y 30\.

2\. MARQUEE SECTION  
Two rows of images that scroll horizontally based on page scroll position. Background \#0C0C0C. Padding: pt-24 sm:pt-32 md:pt-40 pb-10.

21 GIF images from motionsites.ai (exact URLs):

https://motionsites.ai/assets/hero-space-voyage-preview-eECLH3Yc.gif  
https://motionsites.ai/assets/hero-codenest-preview-Cgppc2qV.gif  
https://motionsites.ai/assets/hero-vex-ventures-preview-BczMFIiw.gif  
https://motionsites.ai/assets/hero-stellar-ai-v2-preview-DjvxjG3C.gif  
https://motionsites.ai/assets/hero-asme-preview-B\_nGDnTP.gif  
https://motionsites.ai/assets/hero-transform-data-preview-Cx5OU29N.gif  
https://motionsites.ai/assets/hero-vitara-preview-Cjz2QYyU.gif  
https://motionsites.ai/assets/hero-terra-preview-BFjrCr7T.gif  
https://motionsites.ai/assets/hero-skyelite-preview-DHaZIgUv.gif  
https://motionsites.ai/assets/hero-aethera-preview-DknSlcTa.gif  
https://motionsites.ai/assets/hero-designpro-preview-D8c5\_een.gif  
https://motionsites.ai/assets/hero-stellar-ai-preview-D3HL6bw1.gif  
https://motionsites.ai/assets/hero-xportfolio-preview-D4A8maiC.gif  
https://motionsites.ai/assets/hero-orbit-web3-preview-BXt4OttD.gif  
https://motionsites.ai/assets/hero-nexora-preview-cx5HmUgo.gif  
https://motionsites.ai/assets/hero-evr-ventures-preview-DZxeVFEX.gif  
https://motionsites.ai/assets/hero-planet-orbit-preview-DWAP8Z1P.gif  
https://motionsites.ai/assets/hero-new-era-preview-CocuDUm9.gif  
https://motionsites.ai/assets/hero-wealth-preview-B70idl\_u.gif  
https://motionsites.ai/assets/hero-luminex-preview-CxOP7ce6.gif  
https://motionsites.ai/assets/hero-celestia-preview-0yO3jXO8.gif  
Row 1: first 11 images, tripled for seamless scrolling. Moves RIGHT on scroll (translateX(offset \- 200)).  
Row 2: remaining 10 images, tripled. Moves LEFT on scroll (translateX(-(offset \- 200))).  
Scroll offset calculated as: (window.scrollY \- sectionTop \+ window.innerHeight) \* 0.3  
Each image tile: 420px x 270px, rounded-2xl, object-cover, lazy loaded.  
Gap between tiles: gap-3. Gap between rows: gap-3.  
Uses willChange: 'transform' for performance. Scroll listener is passive.  
3\. ABOUT SECTION  
Full-height centered section with min-h-screen, padding px-5 sm:px-8 md:px-10 py-20.

Four decorative 3D images positioned absolutely in corners:

Top-left: Moon icon \-- https://shrug-person-78902957.figma.site/\_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/moon\_icon.11395d36.png \-- w-\[120px\] sm:w-\[160px\] md:w-\[210px\], positioned top-\[4%\] left-\[1%\] sm:left-\[2%\] md:left-\[4%\]. FadeIn: delay 0.1, x \-80, y 0, duration 0.9.  
Bottom-left: 3D object \-- https://shrug-person-78902957.figma.site/\_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/p59\_1.4659672e.png \-- w-\[100px\] sm:w-\[140px\] md:w-\[180px\], positioned bottom-\[8%\] left-\[3%\] sm:left-\[6%\] md:left-\[10%\]. FadeIn: delay 0.25, x \-80, y 0, duration 0.9.  
Top-right: Lego icon \-- https://shrug-person-78902957.figma.site/\_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/lego\_icon-1.703bb594.png \-- w-\[120px\] sm:w-\[160px\] md:w-\[210px\], positioned top-\[4%\] right-\[1%\] sm:right-\[2%\] md:right-\[4%\]. FadeIn: delay 0.15, x 80, y 0, duration 0.9.  
Bottom-right: 3D group \-- https://shrug-person-78902957.figma.site/\_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/Group\_134-1.2e04f3ce.png \-- w-\[130px\] sm:w-\[170px\] md:w-\[220px\], positioned bottom-\[8%\] right-\[3%\] sm:right-\[6%\] md:right-\[10%\]. FadeIn: delay 0.3, x 80, y 0, duration 0.9.  
Heading: "About me" using .hero-heading gradient text, font-black, uppercase, leading-none, tracking-tight, centered. Font size: clamp(3rem, 12vw, 160px). FadeIn: delay 0, y 40\.

Animated paragraph: Uses a character-by-character scroll-driven opacity animation. Text: "With more than five years of experience in design, i focus on branding, web design, and user experience, i truly enjoy working with businesses that aim to stand out and present their best image. Let's build something incredible together\!" \-- color \#D7E2EA, font-medium, centered, leading-relaxed, max-w-\[560px\], font size clamp(1rem, 2vw, 1.35rem). Each character animates from opacity 0.2 to 1 based on scroll progress, with scroll offset \['start 0.8', 'end 0.2'\].

Contact button below the text block. Gap between heading/text: gap-10 sm:gap-14 md:gap-16. Gap between text block and button: gap-16 sm:gap-20 md:gap-24.

4\. SERVICES SECTION  
White background (\#FFFFFF), with rounded-t-\[40px\] sm:rounded-t-\[50px\] md:rounded-t-\[60px\] top corners. Padding: px-5 sm:px-8 md:px-10 py-20 sm:py-24 md:py-32.

Heading: "Services" in \#0C0C0C, font-black, uppercase, centered, font size clamp(3rem, 12vw, 160px). Margin bottom: mb-16 sm:mb-20 md:mb-28.

5 service items in a vertical list, max-w-5xl, centered:

01 \- 3D Modeling: "Creation of detailed objects, characters, or environments tailored to specific client needs, ideal for games, products, and visualizations."  
02 \- Rendering: "High-quality, photorealistic renders that showcase designs with custom lighting, textures, and materials to bring concepts to life."  
03 \- Motion Design: "Dynamic animations and motion graphics that add energy and storytelling to brands, products, and digital experiences."  
04 \- Branding: "Crafting cohesive visual identities \-- from logos to full brand systems \-- that communicate a clear and memorable presence."  
05 \- Web Design: "Designing clean, modern, and conversion-focused websites with attention to layout, typography, and user experience."  
Each item: horizontal layout with number (font-black, font size clamp(3rem, 10vw, 140px), color \#0C0C0C) on the left and name \+ description stacked vertically on the right. Name: font-medium, uppercase, font size clamp(1rem, 2.2vw, 2.1rem). Description: font-light, leading-relaxed, max-w-2xl, font size clamp(0.85rem, 1.6vw, 1.25rem), opacity 0.6. Items separated by 1px borders (rgba(12, 12, 12, 0.15)). Padding: py-8 sm:py-10 md:py-12. Staggered FadeIn: each item delays by i \* 0.1.

5\. PROJECTS SECTION  
Dark background (\#0C0C0C), rounded top corners rounded-t-\[40px\] sm:rounded-t-\[50px\] md:rounded-t-\[60px\], pulled up with \-mt-10 sm:-mt-12 md:-mt-14, z-10.

Heading: "Project" (singular) using .hero-heading gradient, same styling as other headings.

3 sticky-stacking project cards that scale down as you scroll past them (card stacking effect using Framer Motion useScroll and useTransform). Each card is sticky top-24 md:top-32 inside an h-\[85vh\] container.

Scale calculation: targetScale \= 1 \- (totalCards \- 1 \- index) \* 0.03. Each card offset by top: ${index \* 28}px.

Each card has: rounded-\[40px\] sm:rounded-\[50px\] md:rounded-\[60px\], border-2 border-\[\#D7E2EA\], background \#0C0C0C, padding p-4 sm:p-6 md:p-8.

Card layout:

Top row: Number (huge, same style as services), category label, project name, and a "Live Project" ghost button (rounded-full, border-2 \#D7E2EA, uppercase, tracking-widest).  
Bottom row: Two-column image grid \-- left column (40% width) has 2 stacked images, right column (60%) has 1 tall image. All images have heavy border radius rounded-\[40px\] sm:rounded-\[50px\] md:rounded-\[60px\]. Left top image height: clamp(130px, 16vw, 230px). Left bottom image height: clamp(160px, 22vw, 340px).  
Project data with CloudFront image URLs:

Project 01 \- "Nextlevel Studio" (Client):

Col1 image 1: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055344\_5eff02e0-87a5-41ce-b64f-eb08da8f33db.png\&w=1280\&q=85  
Col1 image 2: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055431\_11d841fd-8b41-46a5-82e4-b04f2407a7d8.png\&w=1280\&q=85  
Col2 image: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055451\_e317bf2d-28d4-48cc-86b0-6f72f25b6327.png\&w=1280\&q=85  
Project 02 \- "Aura Brand Identity" (Personal):

Col1 image 1: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055654\_911201c5-36d9-4bc6-bac7-331adfce159f.png\&w=1280\&q=85  
Col1 image 2: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055723\_5ceda0b8-d9c2-4665-b2e3-83ba19ba76d1.png\&w=1280\&q=85  
Col2 image: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055753\_adc5dcbd-a8e6-49c0-b43a-9b030d835cea.png\&w=1280\&q=85  
Project 03 \- "Solaris Digital" (Client):

Col1 image 1: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055759\_963cfb0b-4bd1-4b0f-9d0a-09bd6cf95b2f.png\&w=1280\&q=85  
Col1 image 2: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_060108\_438f781a-9846-4dcc-89ab-c4e6cb830f5b.png\&w=1280\&q=85  
Col2 image: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260412\_055818\_9d062121-ad7e-46b9-999a-1a6a692ef1ee.png\&w=1280\&q=85  
REUSABLE COMPONENTS  
ContactButton: Rounded-full pill button with gradient background linear-gradient(123deg, \#18011F 7%, \#B600A8 37%, \#7621B0 72%, \#BE4C00 100%), inner box-shadow 0px 4px 4px rgba(181, 1, 167, 0.25), 4px 4px 12px \#7721B1 inset, white 2px outline with \-3px offset. Text: white, font-medium, uppercase, tracking-widest. Sizes: px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4, text text-xs sm:text-sm md:text-base. Label: "Contact Me".

LiveProjectButton: Ghost/outline pill button. Rounded-full, border-2 border-\[\#D7E2EA\], text color \#D7E2EA, font-medium, uppercase, tracking-widest. Sizes: px-8 py-3 sm:px-10 sm:py-3.5, text text-sm sm:text-base. Hover: bg-\[\#D7E2EA\]/10. Label: "Live Project".

FadeIn: Framer Motion wrapper using whileInView with viewport={{ once: true, margin: "50px", amount: 0 }}. Accepts delay, duration (default 0.7), x (default 0), y (default 30). Easing: \[0.25, 0.1, 0.25, 1\]. Uses motion.create() for dynamic element types.

Magnet: Mouse-following magnetic hover effect. Tracks mouse position relative to element center, applies translate3d transform divided by strength factor. Activates when cursor is within padding distance of element edge. Smooth transition in (0.3s ease-out) and out (0.6s ease-in-out). Uses willChange: 'transform'.

AnimatedText: Character-by-character scroll-reveal text animation. Each character goes from opacity 0.2 to 1 based on its position in the text relative to scroll progress. Uses Framer Motion useScroll targeting the paragraph element with offset \['start 0.8', 'end 0.2'\]. Each character uses invisible placeholder \+ absolute positioned animated span.

KEY DEPENDENCIES  
react, react-dom (^18.3.1)  
framer-motion (^12.38.0)  
lucide-react (^0.344.0)  
tailwindcss (^3.4.1)  
vite, typescript  
RESPONSIVE BREAKPOINTS  
All sections use Tailwind's default breakpoints (sm: 640px, md: 768px, lg: 1024px) with mobile-first approach. Heavy use of clamp() for fluid typography. The entire design scales gracefully from mobile to ultra-wide screens.

# Guia 5

Build a single full-viewport hero section in React \+ TypeScript \+ Vite \+ Tailwind CSS, using \`lucide-react\` for icons. The component is a character-figurine carousel called "TOONHUB".

\*\*Fonts (load in \`index.html\` head):\*\*  
\`\`\`html  
\<link rel="preconnect" href="https://fonts.googleapis.com" /\>  
\<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /\>  
\<link href="https://fonts.googleapis.com/css2?family=Anton\&family=Inter:wght@400;500;600;700\&display=swap" rel="stylesheet" /\>  
\`\`\`  
Body font: \`'Inter', sans-serif\`. Display font (huge ghost text \+ bottom-right link): \`'Anton', sans-serif\`.

\*\*Image data (4 items, exact URLs and colors):\*\*  
\`\`\`ts  
const IMAGES \= \[  
  { src: 'https://fifth-gentle-45902158.figma.site/\_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/1.02464a56.png', bg: '\#F4845F', panel: '\#F79B7F' },  
  { src: 'https://fifth-gentle-45902158.figma.site/\_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/2.b977faab.png', bg: '\#6BBF7A', panel: '\#85CC92' },  
  { src: 'https://fifth-gentle-45902158.figma.site/\_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/3.4df853b4.png', bg: '\#E882B4', panel: '\#ED9DC4' },  
  { src: 'https://fifth-gentle-45902158.figma.site/\_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/4.4457fbce.png', bg: '\#6EB5FF', panel: '\#8DC4FF' },  
\];  
\`\`\`  
Preload all 4 images on mount via \`new Image()\`.

\*\*State & logic:\*\*  
\- \`activeIndex\` (0–3), \`isAnimating\` boolean lock, \`isMobile\` (\`window.innerWidth \< 640\`, updated on resize).  
\- \`navigate('next' | 'prev')\`: ignore if animating; set \`isAnimating=true\`; bump \`activeIndex\` \`(prev+1)%4\` or \`(prev+3)%4\`; release lock after \`650ms\`.  
\- Roles derived from activeIndex: \`center=activeIndex\`, \`left=(activeIndex+3)%4\`, \`right=(activeIndex+1)%4\`, \`back=(activeIndex+2)%4\`.

\*\*Layout structure:\*\*  
Outer \`\<div\>\` has \`backgroundColor: IMAGES\[activeIndex\].bg\`, transition \`background-color 650ms cubic-bezier(0.4,0,0.2,1)\`, \`fontFamily: 'Inter, sans-serif'\`, \`relative w-full overflow-hidden\`. Inside, a \`relative w-full\` div with \`height: 100vh; overflow: hidden\`.

1\. \*\*Grain overlay\*\* (\`absolute inset-0 pointer-events-none\`, zIndex 50): SVG fractalNoise data URI, \`baseFrequency=0.9\`, \`numOctaves=4\`, opacity 0.08 inside SVG, container \`opacity: 0.4\`, \`backgroundSize: 200px 200px\`, repeat.

2\. \*\*Giant ghost text "3D SHAPE"\*\* (\`absolute inset-x-0 flex items-center justify-center pointer-events-none select-none\`, zIndex 2, \`top: 18%\`): font Anton, \`fontSize: clamp(90px, 28vw, 380px)\`, weight 900, color white, opacity 1, lineHeight 1, uppercase, letterSpacing \`-0.02em\`, whiteSpace nowrap.

3\. \*\*Top-left brand label "TOONHUB"\*\* (\`absolute top-6 left-4 sm:left-8\`, zIndex 60): \`text-xs font-semibold uppercase\`, white, opacity 0.9, letterSpacing \`0.18em\`.

4\. \*\*Carousel\*\* (\`absolute inset-0\`, zIndex 3): map all 4 IMAGES; each item is \`position:absolute\`, \`aspectRatio: '0.6 / 1'\`, with role-based styles below. Inside, an \`\<img\>\` \`width:100%; height:100%; objectFit:contain; objectPosition:bottom center; draggable=false\`.

   Per-role style:  
   \- \*\*center\*\*: \`transform: translateX(-50%) scale(${isMobile?1.25:1.68})\`, no blur, opacity 1, zIndex 20, \`left:50%\`, \`height: isMobile?'60%':'92%'\`, \`bottom: isMobile?'22%':0\`.  
   \- \*\*left\*\*: \`translateX(-50%) scale(1)\`, blur 2px, opacity 0.85, zIndex 10, \`left: isMobile?'20%':'30%'\`, \`height: isMobile?'16%':'28%'\`, \`bottom: isMobile?'32%':'12%'\`.  
   \- \*\*right\*\*: same as left but \`left: isMobile?'80%':'70%'\`.  
   \- \*\*back\*\*: \`translateX(-50%) scale(1)\`, blur 4px, opacity 1, zIndex 5, \`left:50%\`, \`height: isMobile?'13%':'22%'\`, \`bottom: isMobile?'32%':'12%'\`.

   Transition on each item: \`transform 650ms cubic-bezier(0.4,0,0.2,1), filter 650ms ..., opacity 650ms ..., left 650ms ...\`. \`willChange: transform, filter, opacity\`.

5\. \*\*Bottom-left text \+ nav buttons\*\* (\`absolute bottom-6 left-4 sm:bottom-20 sm:left-24\`, zIndex 60, \`maxWidth:320px\`):  
   \- \`\<p\>\` "TOONHUB FIGURINES" — bold uppercase, tracking-widest, \`mb-2 sm:mb-3 text-base sm:text-\[22px\]\`, white, opacity 0.95, letterSpacing \`0.02em\`.  
   \- \`\<p\>\` (hidden on mobile, \`hidden sm:block\`): "The artwork is stunning, shipped fully prepared. The finish is a vision, the 3D craft is flawless. Many thanks\! Wishing you the win. Order now." — \`text-xs sm:text-sm\`, white, opacity 0.85, lineHeight 1.6, \`mb-4 sm:mb-5\`.  
   \- Two circular buttons (\`w-12 h-12 sm:w-16 sm:h-16\`, transparent bg, 2px white border, white icon): \`ArrowLeft\` and \`ArrowRight\` from lucide-react, size 26, strokeWidth 2.25. On hover: scale 1.08 \+ bg \`rgba(255,255,255,0.12)\`. Transition \`transform 150ms, background-color 150ms\`. Click triggers \`navigate('prev')\` / \`navigate('next')\`.

6\. \*\*Bottom-right link "DISCOVER IT"\*\* (\`absolute bottom-6 right-4 sm:bottom-20 sm:right-10\`, zIndex 60): \`\<a\>\` flex items-center, font Anton, \`fontSize: clamp(20px, 4vw, 56px)\`, weight 400, white, opacity 0.95→1 on hover (200ms), letterSpacing \`-0.02em\`, lineHeight 1, uppercase, no underline. Followed by \`ArrowRight\` (\`w-5 h-5 sm:w-8 sm:h-8\`, strokeWidth 2.25).

\*\*Behavior summary:\*\* clicking arrows rotates roles; background color, image positions, scales, blurs, and opacities all crossfade simultaneously over 650ms with \`cubic-bezier(0.4,0,0.2,1)\`. The character images sit at the bottom of the screen overlapping the giant "3D SHAPE" text behind them.

# Guia 6

Create a single-page hero section with a fullscreen looping background video, glassmorphic navigation, and cinematic typography. Use React \+ Vite \+ Tailwind CSS \+ TypeScript with shadcn/ui.

Video Background:

Fullscreen \<video\> element with autoPlay, loop, muted, playsInline  
Source URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260314\_131748\_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4  
Positioned absolute inset-0 w-full h-full object-cover z-0

Fonts:

Import from Google Fonts: Instrumental Serif (display) and Inter weights 400/500 (body)  
CSS variables: \--font-display: 'Instrument Serif', serif and \--font-body: 'Inter', sans-serif  
Body uses var(--font-body), headings use inline fontFamily: "'Instrument Serif', serif"

Color Theme (dark, HSL values for CSS variables):

\--background: 201 100% 13% (deep navy blue)  
\--foreground: 0 0% 100% (white)  
\--muted-foreground: 240 4% 66% (muted gray)  
\--primary: 0 0% 100%, \--primary-foreground: 0 0% 4%  
\--secondary: 0 0% 10%, \--muted: 0 0% 10%, \--accent: 0 0% 10%  
\--border: 0 0% 18%, \--input: 0 0% 18%

Navigation Bar:

relative z-10, flex row, justify-between, px-8 py-6, max-w-7xl mx-auto  
Logo: "Velorah®" (® as \<sup className="text-xs"\>), text-3xl tracking-tight, Instrument Serif font, text-foreground  
Nav links (hidden on mobile, md:flex): Home (active, text-foreground), Studio, About, Journal, Reach Us — all text-sm text-muted-foreground with hover:text-foreground transition-colors  
CTA button: "Begin Journey", liquid-glass rounded-full px-6 py-2.5 text-sm text-foreground, hover:scale-\[1.03\]

Hero Section:

relative z-10, flex column, centered, text-center, px-6 pt-32 pb-40 py-\[90px\]  
H1: "Where dreams rise through the silence." — text-5xl sm:text-7xl md:text-8xl, leading-\[0.95\], tracking-\[-2.46px\], max-w-7xl, font-normal, Instrument Serif. The words "dreams" and "through the silence." wrapped in \<em className="not-italic text-muted-foreground"\> for color contrast  
Subtext: text-muted-foreground text-base sm:text-lg max-w-2xl mt-8 leading-relaxed — "We're designing tools for deep thinkers, bold creators, and quiet rebels. Amid the chaos, we build digital spaces for sharp focus and inspired work."  
CTA button: "Begin Journey", liquid-glass rounded-full px-14 py-5 text-base text-foreground mt-12, hover:scale-\[1.03\] cursor-pointer

Liquid Glass Effect (CSS class .liquid-glass):

.liquid-glass {  
  background: rgba(255, 255, 255, 0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}

Animations (CSS keyframes \+ classes):

@keyframes fade-rise {  
  from { opacity: 0; transform: translateY(24px); }  
  to { opacity: 1; transform: translateY(0); }  
}  
.animate-fade-rise { animation: fade-rise 0.8s ease-out both; }  
.animate-fade-rise-delay { animation: fade-rise 0.8s ease-out 0.2s both; }  
.animate-fade-rise-delay-2 { animation: fade-rise 0.8s ease-out 0.4s both; }

H1 gets animate-fade-rise  
Subtext gets animate-fade-rise-delay  
Hero CTA button gets animate-fade-rise-delay-2

Layout: No decorative blobs, radial gradients, or overlays. Minimalist, cinematic, vertically centered hero. The video provides all visual depth.

# Guia 7

Prompt: Cinematic Hero Section with Looping Video Background

Create a fullscreen single-page hero section using React \+ Vite \+ Tailwind CSS \+ TypeScript with the following specifications:

Fonts:  
Display text (headings, logo): Instrument Serif  
Body text (navigation, descriptions): Inter  
Import both fonts in /src/styles/fonts.css

Video Background:  
URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260328\_083109\_283f3553-e28f-428b-a723-d639c617eb2b.mp4  
Position: top: '300px' with inset: 'auto 0 0 0'  
Implement custom fade-in/fade-out loop logic using React useEffect and useRef:  
Use requestAnimationFrame to continuously monitor currentTime and duration  
Fade in over 0.5s at the start (opacity 0 to 1\)  
Fade out over 0.5s before the end (opacity 1 to 0\)  
On ended event: set opacity to 0, wait 100ms, reset currentTime \= 0, then play() again  
This creates a seamless manual loop with smooth fade transitions  
Add gradient overlays: absolute inset-0 bg-gradient-to-b from-background via-transparent to-background positioned over the video

Navigation Bar:  
Logo: "Aethera®" (with registered trademark symbol as superscript)  
Logo styling: text-3xl, tracking-tight, Instrument Serif, color \#000000  
Menu items: Home (color \#000000), Studio, About, Journal, Reach Us (all others \#6F6F6F)  
Menu items: text-sm with transition-colors  
CTA button: "Begin Journey", rounded-full, px-6 py-2.5, text-sm, black background (\#000000), white text, hover scale 1.03  
Layout: flex justify-between, px-8 py-6, max-w-7xl mx-auto

Hero Section:  
Positioning: paddingTop: 'calc(8rem \- 75px)', pb-40  
Layout: centered (flex flex-col items-center justify-center text-center), px-6  
Headline:  
Text: "Beyond silence, we build the eternal."  
Styling: text-5xl sm:text-7xl md:text-8xl, max-w-7xl, font-normal  
Font: Instrument Serif  
Line height: 0.95  
Letter spacing: \-2.46px  
Color: \#000000 for main text, \#6F6F6F for italic emphasized words ("silence," and "the eternal.")  
Animation: animate-fade-rise

Description:  
Text: "Building platforms for brilliant minds, fearless makers, and thoughtful souls. Through the noise, we craft digital havens for deep work and pure flows."  
Styling: text-base sm:text-lg, max-w-2xl, mt-8, leading-relaxed  
Color: \#6F6F6F  
Animation: animate-fade-rise-delay

Hero CTA Button:  
Text: "Begin Journey"  
Styling: rounded-full, px-14 py-5, text-base, mt-12  
Colors: black background (\#000000), white text (\#FFFFFF)  
Hover: scale 1.03  
Animation: animate-fade-rise-delay-2

Colors:  
Background: white (\#FFFFFF)  
Headlines/logos/buttons: black (\#000000)  
Descriptions/menu items: gray (\#6F6F6F)  
Button text: white (\#FFFFFF)

Animations (in /src/styles/theme.css):  
fade-rise: opacity 0 to 1, translateY 20px to 0, duration 0.8s, ease-out  
fade-rise-delay: same as fade-rise but with 0.2s delay  
fade-rise-delay-2: same as fade-rise but with 0.4s delay

Layout Structure:  
Container: relative min-h-screen w-full overflow-hidden  
Background video layer (z-0)  
Gradient overlay on video  
Navigation bar (z-10)  
Hero section (z-10)  
All elements should be responsive and maintain the glassmorphic aesthetic with the specified padding, positioning, and smooth animations.

# Guia 8

Build Prompt: Cinematic Space-Travel Landing Page  
Build a single-page landing site with two full-height sections (Hero \+ Capabilities), both using looping background videos with custom JS crossfade, a shared liquid-glass design system, and Framer Motion entrance animations.

Tech stack (pinned, CDN-only)  
\<script src="https://cdn.tailwindcss.com"\>\</script\>  
\<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"\>\</script\>  
\<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"\>\</script\>  
\<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"\>\</script\>  
\<script src="https://unpkg.com/framer-motion@11.11.17/dist/framer-motion.js"\>\</script\>  
\<script\>window.Motion \= window.FramerMotion;\</script\>  
Body is bg: \#000. Page is a React app mounted on \#root, all components are \<script type="text/babel"\> files exporting via window.X \= X.

Fonts  
Google Fonts:

family=Instrument+Serif:ital@0;1\&family=Barlow:wght@300;400;500;600  
Tailwind config adds:

font-heading → 'Instrument Serif', serif (always italic in use)  
font-body → 'Barlow', sans-serif  
Default border radius override: DEFAULT: "9999px" (so bare rounded → pill).

Liquid-glass utilities (exact CSS, in a \<style\> block)  
Two variants — .liquid-glass (subtle, for nav/chips/cards) and .liquid-glass-strong (heavier blur, for primary CTA):

.liquid-glass {  
background: rgba(255,255,255,0.01);  
background-blend-mode: luminosity;  
backdrop-filter: blur(4px);  
\-webkit-backdrop-filter: blur(4px);  
border: none;  
box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);  
position: relative;  
overflow: hidden;  
}  
.liquid-glass::before {  
content: "";  
position: absolute; inset: 0;  
border-radius: inherit;  
padding: 1.4px;  
background: linear-gradient(180deg,  
rgba(255,255,255,0.45) 0%,  
rgba(255,255,255,0.15) 20%,  
rgba(255,255,255,0) 40%,  
rgba(255,255,255,0) 60%,  
rgba(255,255,255,0.15) 80%,  
rgba(255,255,255,0.45) 100%);  
\-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
\-webkit-mask-composite: xor;  
mask-composite: exclude;  
pointer-events: none;  
}  
.liquid-glass-strong { /\* same but: \*/  
backdrop-filter: blur(50px);  
box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);  
}  
.liquid-glass-strong::before { /\* same but 0.5 / 0.2 / 0 / 0 / 0.2 / 0.5 stops \*/ }  
FadingVideo component (custom JS crossfade, no CSS transitions)  
Wraps a \<video autoPlay muted playsInline preload="auto"\> starting at opacity: 0\. Behavior:

FADE\_MS \= 500, FADE\_OUT\_LEAD \= 0.55 seconds.  
fadeTo(target, duration) uses requestAnimationFrame; reads current opacity from http://video.style.opacity so each new fade resumes from wherever the last one left off. Each call calls cancelAnimationFrame on the previous rAF id before starting.  
On loadeddata: set opacity 0, play(), fadeTo(1).  
On timeupdate: if fadingOutRef not set and duration \- currentTime \<= 0.55 and \> 0, flip the ref and fadeTo(0).  
On ended: set opacity 0; after setTimeout(100ms) reset currentTime \= 0, play(), clear fadingOutRef, fadeTo(1).  
loop attribute is OFF (we implement looping manually via ended).  
Cleanup on unmount: cancel rAF, remove listeners.  
Section 1 — Hero (full viewport, black bg)  
Background video (120% width/height, top-aligned, centered horizontally — focal point is the top of frame):

src: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260418\_080021\_d598092b-c4c2-4e53-8e46-94cf9064cd50.mp4  
class: absolute left-1/2 top-0 \-translate-x-1/2 object-cover object-top z-0  
style: { width: "120%", height: "120%" }  
No overlay. z-10 layer holds: Navbar → Hero content (flex-1, centered) → Partners.

Navbar (fixed top-4, px-8 / lg:px-16, z-50)  
Left: 48×48 liquid-glass circle with italic serif lowercase "a" (Instrument Serif).  
Center (desktop only): liquid-glass pill, px-1.5 py-1.5, holding 5 text links — Home, Voyages, Worlds, Innovation, Plan Launch — each px-3 py-2 text-sm font-medium text-white/90 font-body. Followed by a white pill button Claim a Spot \+ ArrowUpRight icon (bg-white text-black, whitespace-nowrap).  
Right: 48×48 invisible spacer to balance logo.  
Hero content (centered, pt-24 px-4)  
All animated with Framer Motion, initial: {filter: blur(10px), opacity: 0, y: 20}, easeOut.

Badge (delay 0.4s): liquid-glass rounded-full pill. Contains white pill chip "New" (bg-white text-black px-3 py-1 text-xs font-semibold) \+ text "Maiden Crewed Voyage to Mars Arrives 2026" (text-sm text-white/90, pr-3).  
Headline — BlurText component (word-by-word animation, see below). Text: "Venture Past Our Sky Across the Universe". Classes: text-6xl md:text-7xl lg:text-\[5.5rem\] font-heading italic text-white leading-\[0.8\] max-w-2xl justify-center tracking-\[-4px\].  
Subheading (delay 0.8s, mt-4 text-sm md:text-base text-white max-w-2xl font-body font-light leading-tight): "Discover the universe in ways once unimaginable. Our pioneering vessels and breakthrough engineering bring deep-space exploration within reach—secure and extraordinary."  
CTAs (delay 1.1s, flex items-center gap-6 mt-6):  
Primary: liquid-glass-strong rounded-full px-5 py-2.5 text-sm font-medium text-white with "Start Your Voyage" \+ ArrowUpRight (h-5 w-5).  
Secondary: bare text link, "View Liftoff" \+ Play icon (h-4 w-4, filled).  
Stats row (delay 1.3s, flex items-stretch gap-4 mt-8): two liquid-glass cards, p-5 w-\[220px\] rounded-\[1.25rem\], each:  
Top: white 28×28 outline SVG icon (clock for card 1, globe for card 2).  
Bottom: large number in Instrument Serif italic white (text-4xl tracking-\[-1px\] leading-none): "34.5 Min" / "2.8B+". Label below (text-xs text-white font-body font-light mt-2): "Average Videos Watch Time" / "Users Across the Globe".  
Partners (bottom of hero, delay 1.4s)  
flex flex-col items-center gap-4 pb-8:

liquid-glass rounded-full chip (px-3.5 py-1 text-xs font-medium text-white): "Collaborating with top aerospace pioneers globally".  
Row of 5 names in Instrument Serif italic white, text-2xl md:text-3xl tracking-tight, gap-12/md:gap-16: Aeon · Vela · Apex · Orbit · Zeno.  
BlurText component (word-by-word blur-in)  
IntersectionObserver triggers on 10% visibility. Splits text by spaces. Each word is a motion.span with:

initial: {filter: 'blur(10px)', opacity: 0, y: 50}  
3-step keyframes to {filter: 'blur(5px)', opacity: 0.5, y: \-5} → {filter: 'blur(0px)', opacity: 1, y: 0}  
duration: 0.7 (stepDuration 0.35 × 2), times: \[0, 0.5, 1\], ease: easeOut  
Stagger: delay \= (i \* 100\) / 1000 seconds  
display: inline-block, marginRight: 0.28em (not non-breaking-space — letter-spacing \-4px eats nbsp).  
Parent \<p\> is display: flex; flexWrap: wrap; justifyContent: center; rowGap: 0.1em.  
Section 2 — Capabilities (min-h-screen, black bg)  
Background video (full-bleed, no 120% scale):

src: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260418\_094631\_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4  
class: absolute inset-0 w-full h-full object-cover z-0  
Same FadingVideo treatment. No overlay.

Content (relative z-10 px-8 md:px-16 lg:px-20 pt-24 pb-10 flex flex-col min-h-screen):

Header (mb-auto):

Kicker: text-sm font-body text-white/80 mb-6 → // Capabilities  
Heading: font-heading italic text-white text-6xl md:text-7xl lg:text-\[6rem\] leading-\[0.9\] tracking-\[-3px\]:  
Production  
evolved  
(two lines, \<br/\> between).  
Three cards (grid grid-cols-1 md:grid-cols-3 gap-6 mt-16): each is liquid-glass rounded-\[1.25rem\] p-6 min-h-\[360px\] flex flex-col.

Top row of each card (flex items-start justify-between gap-4):

Left: 44×44 nested liquid-glass square (rounded-\[0.75rem\]) with a white Material Icons SVG (fill currentColor, h-6 w-6 text-white). Use random Material icons — these three used:  
AI Scenery: image icon — path M5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.825 0 1.413.588T21 5v14q0 .825-.587 1.413T19 21H5Zm1-4h12l-3.75-5-3 4L9 13l-3 4Z  
Batch Production: movie icon — path M4 6.47 5.76 10H20v8H4V6.47M22 4h-4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.89-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4Z  
Smart Lighting: lightbulb icon — path M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1Zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7Z  
Right: flex flex-wrap justify-end gap-1.5 max-w-\[70%\] — 4 small liquid-glass pill tags (rounded-full px-3 py-1 text-\[11px\] text-white/90 font-body whitespace-nowrap):  
Card 1: Natural Context · Photo Realism · Infinite Settings · Eco-Vibe  
Card 2: Scale Fast · Visual Consistency · Time Saver · Ready to Post  
Card 3: Ray Tracing · Physical Shadows · Studio Quality · Sunlight Sync  
Middle: flex-1 spacer.

Bottom of each card (mt-6):

Title h3: font-heading italic text-white text-3xl md:text-4xl tracking-\[-1px\] leading-none — "AI Scenery" / "Batch Production" / "Smart Lighting"  
Body p (mt-3 text-sm text-white/90 font-body font-light leading-snug max-w-\[32ch\]):  
"AI analyzes your product to create indistinguishable natural environments — from Icelandic cliffs to misty forests."  
"Style your entire product line in minutes. Create a unified visual identity for catalogues and social media without weeks of retouching."  
"Automatic lighting and material adjustment. Achieve flawless integration with realistic shadows and sunlight."  
Icons (inline lucide-style SVGs, currentColor stroke)  
ArrowUpRight: 24×24, M7 17L17 7 \+ M7 7h10v10, strokeWidth 2, round caps.  
Play: 24×24 filled polygon 6 4 20 12 6 20 6 4\.  
Notes  
All text white; no green, no gradient backgrounds.  
No CSS transitions on the videos — fades must be rAF-driven per the FadingVideo spec.  
Videos are full-bleed with no dark overlay; contrast comes from the liquid-glass chrome.  
Framer Motion dev warnings about list keys can be suppressed with a console.error filter wrapper — they're benign.  
The detailed prompt above captures every element, style, animation, video URL, and font to recreate the landing page exactly.

# Guia 9

# Guia 10

Prompt:  
Build a modern React landing page using Vite, Tailwind CSS, and motion/react for elegant animations. The application must feature a highly polished, aesthetic hero section and a glassmorphic navigation bar.  
1\. Typography & Global CSS (src/index.css)  
Import the fonts "Inter" and "Outfit" from Google Fonts.  
Set \--font-sans to Inter and \--font-display to Outfit.  
Set \--color-brand-green to \#9fff00 and \--color-bg-base strictly to \#EDEEF5.  
Ensure the body uses @apply bg-bg-base text-zinc-900 font-sans antialiased; to carry the \#EDEEF5 background throughout the entire page.  
2\. Component Structure (src/App.tsx)  
Import Navbar and Hero.  
Return a div containing the \<Navbar /\> and \<main\>\<Hero /\>\</main\>.  
Set the wrapper container classes to min-h-screen bg-bg-base selection:bg-brand-green selection:text-black.  
3\. Navbar Component (src/components/Navbar.tsx)  
Give it fixed styling: fixed top-0 left-0 w-full z-50 py-6 md:py-10 bg-gradient-to-b from-\[\#f1f1f1\]/80 to-transparent backdrop-blur-\[2px\].  
Container layout: A 12-column grid (grid-cols-12 max-w-7xl mx-auto).  
Left (Cols 1-3): A geometric flower/clover SVG icon (fill: \#1a1a1a) beside the brand name "mėntality" using the display font.  
Center (Cols 4-9): Desktop-only hidden nav links: "service", "patient resources", "about us", "education center". Styled small and lowercase.  
Right (Cols 10-12): "find help" anchor link, a black rounded button reading "get started →", and an elegant animated hamburger toggle icon for mobile.  
Include an AnimatePresence and motion.div drawer that slides down for mobile with the navigation links.  
4\. Hero Component (src/components/Hero.tsx)  
Main styling: \<section className="relative min-h-\[110vh\] sm:min-h-\[140vh\] w-full flex flex-col items-center justify-start overflow-hidden bg-bg-base"\>  
Background Video Container:  
Absolute wrapper: \<div className="absolute top-\[15vh\] sm:top-\[20vh\] left-0 w-full h-\[95vh\] sm:h-\[120vh\] z-0 pointer-events-none"\>  
The video itself should be \<video autoPlay loop muted playsInline className="w-full h-full object-cover opacity-100" /\>  
Exact CloudFront URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260603\_132049\_036591b8-6e92-4760-b94c-a7ea6eef315c.mp4  
Gradient Mask: Below the video in the wrapper, add \<div className="absolute top-0 left-0 w-full h-24 sm:h-32 bg-gradient-to-b from-bg-base to-transparent"\>\</div\> to smoothly blend the video into the \#EDEEF5 background.  
Hero Content Alignment: Use \<div className="max-w-7xl w-full mx-auto px-8 md:px-16 lg:px-20 relative z-10 grid grid-cols-12 gap-x-4 md:gap-x-8"\>. Place the text in col-span-12 md:col-span-10 md:col-start-2.  
Hero Header (motion.h1): Needs a slide-up fade (initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}).  
Exact text formatting:  
\[\#1a1a1a\] Remix: Mentality offers  
\[\#8e8e8e\] information  
(line break)  
\[\#8e8e8e\] and resources to help you manage  
(line break)  
\[\#8e8e8e\] your \[Eye Icon Puipl UI Element\] mental wellbeing.  
For the Eye Icon Element between "your" and "mental", create an inline pill-shaped visual: w-\[16px\] md:w-\[42px\] lg:w-\[62px\] border-\[2px\] border-\[\#1a1a1a\] rounded-full inline-flex items-center justify-center containing a tiny solid black dot (w-2 h-2).  
Search Pill Component:  
Add a delayed slide-up animation (delay: 0.15) under the header text.  
Make a custom capsule \<div className="bg-white rounded-\[6px\] border border-black/\[0.05\] p-1 pl-4 flex items-center shadow-sm"\>.  
Include an \<input placeholder="Ask me anything..."\> with transparent background so it looks integrated.  
Trailing action button: \<button className="bg-\[\#1a1a1a\] text-white w-9 h-9 rounded-full relative"\> containing an SVG chevron/arrow icon.  
Architectural Edge Anchors:  
Absolute middle right edge: Create a glassmorphic pill button for language switching (pl — en).  
Absolute bottom left corner: Place "2024" in small neat text.  
Absolute bottom right corner: Place "mental health tools" in small neat text.  
Ensure there are no artificial margins/padding below the video to make sure the video takes exactly 100% of the Hero viewport, while allowing the \#EDEEF5 background base to anchor the entire page cleanly.

# Guia 11

Recreate this hero section exactly. Here are the complete specifications:

Video Background:

Full-screen background video, absolutely positioned, covering the entire viewport (object-cover)  
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260403\_050628\_c4e32401-fab4-4a27-b7a8-6e9291cd5959.mp4  
Autoplay, loop, muted, playsInline  
NO dark overlay, NO gradient overlay, NO semi-transparent layer on top of the video. The video plays raw with no dimming whatsoever.  
Typography (CRITICAL \- must be applied globally):

Import the Google Font Inter via a \<link\> tag in index.html:

\<link rel="preconnect" href="https://fonts.googleapis.com"\>  
\<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin\>  
\<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600\&display=swap" rel="stylesheet"\>  
Set the body font-family in CSS to: 'Inter', sans-serif  
Apply \-webkit-font-smoothing: antialiased and \-moz-osx-font-smoothing: grayscale on the body  
Also extend the Tailwind config to set fontFamily: { sans: \['Inter', 'sans-serif'\] } so all Tailwind font-sans usage picks up Inter automatically  
Navbar:

Wrapped in horizontal page padding: px-6 md:px-12 lg:px-16 with pt-6 top padding  
The navbar bar itself uses the .liquid-glass class and has rounded-xl, px-4 py-2, flex layout with items-center justify-between  
Left: Logo text "VEX" \- text-2xl font-semibold tracking-tight  
Center (hidden on mobile, visible md+): Links "Story", "Investing", "Building", "Advisory" \- text-sm, gap-8, hover transitions to gray-300  
Right: "Start a Chat" button \- bg-white text-black px-6 py-2 rounded-lg text-sm font-medium, hover to gray-100  
Hero Content (Bottom of viewport):

Container: same horizontal padding as navbar, flex column filling remaining height, content pushed to bottom with flex-1 flex flex-col justify-end, bottom padding pb-12 lg:pb-16  
On large screens: 2-column grid (lg:grid lg:grid-cols-2 lg:items-end)  
Left Column \- Main content:

Heading: "Shaping tomorrow\\nwith vision and action." (literal line break between "tomorrow" and "with")

Responsive sizes: text-4xl md:text-5xl lg:text-6xl xl:text-7xl  
font-normal, mb-4  
Inline style: letterSpacing: '-0.04em'  
Character-by-character entrance animation: Each character starts at opacity: 0 and translateX(-18px), then transitions to opacity: 1 and translateX(0). Each character gets a staggered delay calculated as: (lineIndex \* lineLength \* charDelay) \+ (charIndex \* charDelay) where charDelay \= 30ms. The whole animation starts after 200ms initial delay. Each character transition is 500ms.  
Spaces render as \\u00A0 (non-breaking space)  
Subheading: "We back visionaries and craft ventures that define what comes next."

text-base md:text-lg text-gray-300 mb-5  
Fade-in animation: starts at 800ms delay, 1000ms duration  
Buttons row: flex-wrap with gap-4

"Start a Chat" \- bg-white text-black px-8 py-3 rounded-lg font-medium  
"Explore Now" \- liquid-glass border border-white/20 text-white px-8 py-3 rounded-lg font-medium, hover transitions to white bg \+ black text  
Fade-in animation: starts at 1200ms delay, 1000ms duration  
Right Column \- Tag:

Aligned to bottom-right on large screens (flex items-end justify-start lg:justify-end)  
Glass card: liquid-glass border border-white/20 px-6 py-3 rounded-xl  
Text: "Investing. Building. Advisory." \- text-lg md:text-xl lg:text-2xl font-light  
Fade-in animation: starts at 1400ms delay, 1000ms duration  
Liquid Glass CSS (place in global CSS):

.liquid-glass {  
  background: rgba(0, 0, 0, 0.4);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.1) 80%, rgba(255,255,255,0.3) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}  
FadeIn component: A wrapper that starts with opacity: 0 and transitions to opacity: 1 after a configurable delay (ms) using a setTimeout \+ React state. Transition duration is also configurable. Uses inline transitionDuration style and Tailwind's transition-opacity class.

AnimatedHeading component: Splits text by \\n into lines, then each line into individual characters. Each character is an inline-block \<span\> with CSS transitions on opacity and transform (translateX). Animation triggers via React state after the initial delay.

Color scheme: Black background, white text, gray-300 for secondary text, white/20 for borders. No purple, no indigo.

Stack: React \+ TypeScript, Tailwind CSS, Vite. No extra UI libraries needed. Icons from lucide-react if needed (none currently used in the hero).

# Guia 12

Build a full-screen hero landing page for a creative agency called "Mainframe" using React, TypeScript, Vite, and Tailwind CSS. Here is every detail:

\---

FONTS

Load two fonts in \`index.html\` via these stylesheet links:  
\- Heading: \`https://db.onlinewebfonts.com/c/5ac3fe7c6abd2f62067f266d89671492?family=HelveticaNowDisplay-Medium\`  
\- Body: \`https://db.onlinewebfonts.com/c/1aa3377e489837a26d019bba501e779d?family=HelveticaNowDisplayW01-Rg\`

In \`index.css\`, define CSS variables:  
\`\`\`css  
:root {  
  \--font-heading: 'HelveticaNowDisplay-Medium', 'Helvetica Neue', Arial, sans-serif;  
  \--font-body: 'HelveticaNowDisplayW01-Rg', 'Helvetica Neue', Arial, sans-serif;  
}  
body {  
  font-family: var(--font-body);  
}  
\`\`\`

The entire page uses \`var(--font-body)\` except the logo text which uses \`var(--font-heading)\`.

\---

BACKGROUND VIDEO (mouse-scrub controlled)

\- A full-screen \`\` element is \`position: fixed; inset: 0; z-index: 0; object-fit: cover; object-position: 70% center;\`.  
\- Video source URL: \`https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260530\_042513\_df96a13b-6155-4f6e-8b93-c9dee66fba08.mp4\`  
\- The video is \`muted\`, \`playsInline\`, \`preload="auto"\`. It does NOT autoplay.  
\- The video scrubs forward/backward based on horizontal mouse movement. Use a \`mousemove\` event listener on \`window\`. Track \`prevX\`, compute \`delta \= currentX \- prevX\`, convert to a time offset: \`(delta / window.innerWidth)  SENSITIVITY  video.duration\` where \`SENSITIVITY \= 0.8\`. Clamp \`targetTime\` between 0 and \`video.duration\`. Use \`video.currentTime\` to seek, and an \`onSeeked\` handler to queue the next seek if \`targetTime\` has moved, preventing seek-flooding.

\---

\*\*NAVBAR (fixed, z-index: 10)\*\*

\- Fixed to top, full width. Padding: \`px-5 sm:px-8 py-4 sm:py-5\`. Flex row, \`justify-between\`, \`items-center\`.  
\- \*\*Logo (left):\*\* Flex row with \`gap-3\`. Text "Mainframe(R)" (use the registered trademark symbol) at \`text-\[21px\] sm:text-\[26px\]\`, \`tracking-tight\`, black, using \`var(--font-heading)\`. Beside it, a decorative asterisk character \`✳︎\` at \`text-\[25px\] sm:text-\[30px\]\`, black, \`select-none\`, \`letter-spacing: \-0.02em\`.  
\- \*\*Desktop nav links (center, hidden below md):\*\* Flex row, \`text-\[23px\]\`, black. Links: "Labs", "Studio", "Openings", "Shop" separated by commas rendered as \`, \`. Each link has \`hover:opacity-60 transition-opacity\`.  
\- \*\*Desktop CTA (right, hidden below md):\*\* An anchor "Get in touch" at \`text-\[23px\]\`, black, \`underline underline-offset-2\`, \`hover:opacity-60 transition-opacity\`.  
\- \*\*Mobile hamburger (visible below md):\*\* A button with 3 horizontal bars (each \`w-6 h-\[2px\] bg-black\`), spaced with \`gap-\[5px\]\`. On toggle, the top bar rotates 45deg and translates down 7px, middle bar fades to opacity 0, bottom bar rotates \-45deg and translates up 7px. All transitions are \`duration-300\`.  
\- \*\*Mobile overlay (z-index: 9):\*\* \`fixed inset-0 bg-white/95 backdrop-blur-sm\`, flex column, vertically centered, left-aligned with \`px-8 gap-8\`. Same links at \`text-\[32px\] font-medium\`, plus "Get in touch" underlined. Fades in/out with \`opacity\` and \`pointerEvents\` toggled. Hidden on md+.

\---

\*\*HERO SECTION (z-index: 1)\*\*

\- Full \`h-screen\`, flex column. On mobile: \`justify-end pb-12\`. On \`md:\`: \`justify-center pb-0\`. Horizontal padding: \`px-5 sm:px-8 md:px-10\`. \`overflow-hidden\`.  
\- Content container: \`max-w-xl\`, \`relative z-10\`.

\*\*1. Blurred intro label:\*\*  
\- \`pointer-events-none\`, \`select-none\`, \`mb-5 sm:mb-6\`.  
\- Font size: \`clamp(18px, 4vw, 26px)\`, \`line-height: 1.3\`, \`font-weight: 400\`, \`color: \#000\`, \`filter: blur(4px)\`.  
\- Two lines of text:  
  \- Line 1: "Hey there, meet A.R.I.A,"  
  \- Line 2: "Mainframe's Adaptive Response Interface Agent"  
\- Separated by a \`  
\`.

\*\*2. Typewriter text:\*\*  
\- Text: \`"Glad you stopped in. Good taste tends to find us. Now, what are we building?"\`  
\- Custom \`useTypewriter\` hook: takes \`text\`, \`speed\` (default 38ms per character), \`startDelay\` (default 600ms). After the delay, an interval reveals one character at a time. Returns \`{ displayed, done }\`.  
\- Rendered in a \`

\` tag, black, \`mb-5 sm:mb-6\`, font size \`clamp(18px, 4vw, 26px)\`, \`line-height: 1.35\`, \`font-weight: 400\`, \`min-height: 54px\`.  
\- While typing, show a blinking cursor: \`inline-block w-\[2px\] h-\[1.1em\] bg-black align-middle ml-\[2px\]\` with CSS animation \`blink 1s step-end infinite\` (\`opacity: 1 at 0%/100%, 0 at 50%\`). Cursor disappears when \`done\` is true.

\*\*3. Action pill buttons:\*\*  
\- Appear with a fade-in \+ slide-up animation (\`opacity 0-\>1\`, \`translateY(8px)-\>0\`, \`transition: opacity 0.4s ease, transform 0.4s ease\`). They become visible 400ms after page load, independent of the typewriter animation (do NOT wait for typing to finish).  
\- Container: \`flex flex-wrap gap-y-1\`.  
\- \*\*4 white pill buttons:\*\* Labels: "Pitch us an idea", "Come work here", "Send a brief hello", "See how we operate". Each is \`inline-flex items-center justify-center bg-white text-black border border-black/10 rounded-full text-\[13px\] sm:text-\[15px\] px-4 sm:px-5 py-\[0.3em\] mx-\[0.2em\] mb-\[0.4em\] white-space: nowrap\`. Hover: \`bg-black text-white\`, \`transition-colors duration-200\`.  
\- \*\*1 outline pill button:\*\* Text "Reach us: hello@mainframe.co" (email is underlined with \`underline-offset-1\`), followed by a small 12x12 copy icon (inline SVG of two overlapping rectangles). Styled: \`text-white bg-transparent border border-white rounded-full\`, same sizing as above, with \`gap-2 sm:gap-3\` between text and icon. Hover: \`bg-white text-black\`. On click, copies "hello@mainframe.co" to clipboard via \`navigator.clipboard.writeText()\`.

\---

DEPENDENCIES

Only React, ReactDOM, Tailwind CSS, and Vite. No other UI libraries. Lucide-react is available but not used in this component.

# Guia 13

Create a premium private jet landing page hero section with the following specifications:

Video Background:  
Use this exact CloudFront video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260328\_091828\_e240eb17-6edc-4129-ad9d-98678e3fd238.mp4  
Video should autoplay, be muted, loop continuously, and include playsInline attribute  
Video covers entire viewport (100vh) using object-cover

Navigation Bar:  
Brand name "SkyElite" on the left (text-2xl, font-semibold, text-gray-900)  
Desktop menu items (hidden on mobile, visible md:flex): Start, Story, Rates, Benefits, FAQ  
Navigation links in gray-900 with hover:text-gray-700 transition  
Mobile hamburger menu button using Lucide React icons (Menu/X)  
Mobile menu appears as dropdown with white/95 opacity background, backdrop blur, rounded corners, shadow  
Max width 7xl, centered with px-8 py-6

Hero Content (centered, \-mt-80 to pull up):  
Small uppercase label: "PRIVATE JETS" (text-sm, font-semibold, gray-600, tracking-wider, mb-4)  
Large two-line heading with overlapping effect:  
Line 1: "Premium." (text-6xl md:text-7xl lg:text-8xl, font-normal, text-gray-500, leading-none, tracking-tighter)  
Line 2: "Accessible." (same size, color: \#202A36, negative margin-top: \-12px for overlap)  
Subtitle: "Your dedication deserves recognition." (text-lg md:text-xl, gray-600, mb-6, max-w-2xl)  
Two call-to-action buttons (gap-4, centered):  
"Discover" button: px-4 py-2, rounded-full, bg-gray-300, text-gray-800, font-medium, hover:bg-gray-400  
"Book Now" button: px-4 py-2, rounded-full, white text, bg-color \#202A36, hover color \#1a2229 with smooth transitions

Typography:  
Use Inter font (import from Google Fonts: 400, 500, 600, 700 weights)  
Apply to entire body via CSS

Technical Setup:  
React with TypeScript  
Tailwind CSS for styling  
Lucide React for icons  
useState hook for mobile menu toggle  
Full screen height container (h-screen)  
Responsive breakpoints: mobile-first, md, lg  
All transitions use transition-colors class

Layout Structure:  
Outer container: min-h-screen, bg-gray-50  
Hero section: relative, h-screen, overflow-hidden  
Content wrapper: relative, h-full, flex flex-col  
Main content area: flex-1, flex items-center justify-center

Make it clean, modern, and premium-looking with smooth interactions.

# Guia 14

Build a single-page React \+ TypeScript \+ Vite \+ Tailwind site that is a full-screen video-background landing page with a contact form. Use \`lucide-react\` for icons.

\*\*Layout & Sizing\*\*  
\- Root: \`min-h-screen\` white background with padding \`p-3 sm:p-4 md:p-6\`.  
\- Inside the root, one large rounded card with \`rounded-2xl sm:rounded-3xl\`, \`overflow-hidden\`. Heights: \`min-h-\[calc(100vh-24px)\] sm:min-h-\[calc(100vh-32px)\] md:min-h-\[calc(100vh-48px)\] lg:h-\[calc(100vh-48px)\]\`. On desktop it locks to viewport; on tablet/mobile it expands to content.  
\- Background video fills the card (\`absolute inset-0 w-full h-full object-cover\`). The video element has \`autoPlay muted loop playsInline\`. Use this exact URL:  
  \`\`\`  
  https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260602\_150901\_c45b90ec-18d7-42ff-90e2-b95d7109e330.mp4  
  \`\`\`  
\- Content layer: \`relative z-10 flex flex-col\` with the same min-height ladder as the card and \`lg:h-full\`, padding \`p-4 sm:p-6 md:p-8\`, \`gap-6\`.

\*\*Fonts\*\*  
\- Import from Google Fonts in \`index.css\`: \`Inter\` (weights 300–700) and \`Instrument Serif\` (italic \+ regular).  
\- Set \`\* { font-family: 'Inter', sans-serif; }\` globally.  
\- Use \`Instrument Serif\` italic for one accent word inline (see headline below).

\*\*Navbar (top)\*\*  
\- Pill bar with \`bg-white/60 backdrop-blur-md rounded-2xl shadow-sm\`, padding \`pl-3 sm:pl-4 pr-2 py-2\`, \`w-full sm:w-auto\`, \`flex items-center gap-3 sm:gap-6\`.  
\- Logo: 32x32 inline SVG (\`viewBox="0 0 256 256"\`) with two black filled paths forming a stylized "M":  
  \`M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z\`.  
\- Links (hidden on mobile, shown \`sm:flex\`): \`Our story\`, \`Expertise\`, \`Our work\`, \`Journal\` — class \`text-gray-800 text-sm font-medium hover:opacity-60 transition-opacity whitespace-nowrap\`.  
\- CTA button on the right: black pill \`bg-black text-white text-sm font-medium px-4 sm:px-5 py-2 rounded-xl hover:bg-gray-800\` with label \`Start a project\`. On mobile it floats right with \`ml-auto\`.

\*\*Spacer\*\*  
\- A \`\<div className="flex-1 min-h-\[2rem\]" /\>\` between nav and the bottom row.

\*\*Bottom row (headline \+ form)\*\*  
\- Container: \`flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6\`.

\*\*Headline (left)\*\*  
\- \`\<p\>\` with white text, \`text-3xl sm:text-4xl xl:text-5xl font-medium leading-tight drop-shadow-lg lg:max-w-lg xl:max-w-2xl shrink-0\`.  
\- Content (with \`\<br /\>\`):  
  \`We craft bold ideas\` / \`and ship them as \*products\*\`  
\- The word \`products\` is wrapped in a \`\<span\>\` with inline style: \`fontFamily: "'Instrument Serif', serif"\`, \`fontStyle: 'italic'\`, \`fontWeight: 400\`.

\*\*Contact form card (right)\*\*  
\- Outer: \`w-full lg:w-\[min(480px,45%)\] shrink-0\`.  
\- Card: \`bg-white rounded-2xl sm:rounded-3xl shadow-2xl overflow-hidden\`, inner padding \`p-4 sm:p-6\`, \`flex flex-col gap-4\`.

1\. \*\*Heading:\*\* \`Say hello\! 👋\` — \`text-xl sm:text-2xl font-semibold text-black tracking-tight\`.

2\. \*\*Email \+ socials row\*\* (always horizontal): \`flex flex-row items-center justify-between gap-3 bg-gray-50 rounded-2xl px-4 py-2.5\`.  
   \- Left: small grey label \`Drop us a line\`, then mailto link \`hello@forma.co\` in \`text-blue-600 font-semibold hover:underline truncate\`.  
   \- Right: four 32x32 rounded-xl buttons (\`w-8 h-8 rounded-xl flex items-center justify-center hover:opacity-80 transition-opacity\`) using lucide icons size 13:  
     \- Twitter — \`bg-gray-100 text-gray-800\`  
     \- Circle — \`bg-pink-100 text-pink-500\`  
     \- Instagram — \`bg-orange-100 text-orange-400\`  
     \- Linkedin — \`bg-blue-100 text-blue-600\`  
   \- Extract this into a small \`SocialBtn\` helper component.

3\. \*\*OR divider:\*\* horizontal lines on either side of the word \`OR\` (\`text-gray-400 font-medium text-sm\`, lines \`flex-1 h-px bg-gray-200\`).

4\. \*\*Form\*\* (\`flex flex-col gap-4\`):  
   \- Label \`Tell us about your vision\` (\`text-sm font-medium text-black\`).  
   \- Name \+ Email inputs side by side on \`sm:\` (\`flex flex-col sm:flex-row gap-2\`), placeholders \`Full name\` and \`Email\`. Input style: \`flex-1 min-w-0 text-sm px-3 py-2.5 rounded-xl border border-gray-200 bg-transparent placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition\`.  
   \- Textarea, 4 rows, placeholder \`What are you looking to build or improve...\`, same input style plus \`resize-none\`.  
   \- Service tags section: label \`I need help with...\`. Tags wrap (\`flex flex-wrap gap-1.5\`). Each tag is a button \`text-xs font-medium px-3 py-2 rounded-lg border transition-all\`. Inactive: \`bg-white text-gray-700 border-gray-200 hover:border-gray-400\`. Active (selected): \`bg-gray-100 text-black border-black\`. Multi-select toggle via state.  
     \- Services list (exact order): \`Website\`, \`Mobile App\`, \`Web App\`, \`E-Commerce\`, \`Visual Identity\`, \`3D & Motion\`, \`Digital Marketing\`, \`Growth & Consulting\`, \`Other\`.  
   \- Submit button: \`w-full bg-black text-white text-sm font-semibold py-3 rounded-2xl hover:bg-gray-800 transition-colors disabled:opacity-60\`. Label: \`Send my message\` (or \`Sending...\` while submitting).

5\. \*\*Submit behavior:\*\* On submit, set \`sending=true\`, await a 1-second fake delay (\`new Promise(r \=\> setTimeout(r, 1000))\`), then show a success state in place of the form: centered column with \`py-6 gap-3\`, a 48x48 green check pill (\`w-12 h-12 rounded-full bg-green-50 flex items-center justify-center text-xl\` containing \`✓\`), heading \`You're all set\!\` (\`text-base font-semibold text-gray-900\`), and subtext \`Expect a reply within 24 hours.\` (\`text-sm text-gray-500\`).

\*\*State (useState)\*\*  
\- \`selected: string\[\]\` (toggled service chips)  
\- \`name\`, \`email\`, \`message\`: strings  
\- \`sending\`, \`sent\`: booleans

\*\*Transitions/animations\*\*  
\- All interactive elements use Tailwind \`transition-\*\` utilities (opacity, colors, all).  
\- No external animation library; rely on Tailwind hover/focus transitions and \`backdrop-blur-md\` on the navbar.

\*\*Constants at the top of the file\*\*  
\- \`VIDEO\_URL\` (the CloudFront URL above) and \`SERVICES\` array.

\*\*Files\*\*  
\- \`src/App.tsx\` — entire component plus \`SocialBtn\` helper.  
\- \`src/index.css\` — Google Fonts import \+ Tailwind directives \+ global \`\* { font-family: 'Inter', sans-serif; }\`.  
\- Standard Vite \+ Tailwind config (\`tailwind.config.js\` scanning \`./index.html\` and \`./src/\*\*/\*.{ts,tsx}\`).

# Guia 15

Build a React \+ Vite \+ Tailwind CSS landing page for "Axion Studio" \- a design agency site. Use the \`shaders\` package (npm: \`shaders\`) for the hero background, \`lucide-react\` for icons. The page has 3 sections. Match every detail exactly:

\---

\#\# SECTION 1: HERO (Full viewport height)

\*\*Background:\*\* Light gray \`\#EFEFEF\` with a full-screen animated shader overlay (positioned absolute, inset-0, z-10, pointer-events-none). The shader stack uses components from \`shaders/react\`:  
\- \`Swirl\` \- colorA: \`\#ffffff\`, colorB: \`\#f0f0f0\`, detail: 1.7  
\- \`ChromaFlow\` \- baseColor: \`\#ffffff\`, downColor/leftColor/rightColor/upColor: \`\#ff5f03\`, momentum: 13, radius: 3.5  
\- \`FlutedGlass\` \- aberration: 0.61, angle: 31, frequency: 8, highlight: 0.12, highlightSoftness: 0, lightAngle: \-90, refraction: 4, shape: "rounded", softness: 1, speed: 0.15  
\- \`FilmGrain\` \- strength: 0.05

\*\*Navigation (z-20, relative):\*\* A pill-shaped white navbar (\`bg-white rounded-full\`) with 5px padding, inside a max-w-\[1440px\] container with p-2 sm:p-3.

\- LEFT: Dark circle logo (w-9 h-9 sm:w-10 sm:h-10, bg-gray-900, rounded-full) with white text "AX" (10px/11px, font-bold, tracking-tight). Next to it (hidden on mobile, shown md+): nav links "Projects", "Studio", "Journal", "Connect" \- 14px, text-gray-900, hover:text-gray-500, transition-colors duration-300, gap-6.

\- RIGHT (hidden on mobile, shown md+):   
  \- Text "Taking on projects for Q1 2026" (13px, text-gray-600, hidden below lg)  
  \- Clock icon (lucide, size 14\) \+ live London time "{HH:MM} in London" (13px, text-gray-600)  
  \- CTA button: bg-gray-900, text-white, 13px font-medium, rounded-full, pl-5 pr-2 py-2. Text "Book a strategy call" with a HOVER TEXT ROLL animation: the text is duplicated inside a flex-col container with overflow-hidden h-\[20px\], on group-hover it translates \-50% vertically (duration-500, ease cubic-bezier(0.25,0.1,0.25,1)). Arrow icon in a white circle (w-6 h-6) that rotates \-45deg on hover (same easing).

\- MOBILE: A "Menu"/"Close" toggle button (md:hidden), bg-gray-900, rounded-full, with Menu/X icons from lucide-react.

\*\*Mobile Menu Overlay:\*\* Fixed inset-0, z-50. Black/60 backdrop. A white bottom sheet (rounded-2xl, mx-3 mb-3) that slides up (translate-y-full to translate-y-0, duration-500, ease cubic-bezier(0.32,0.72,0,1)). Contains: time badge, nav links (28px/32px font-medium), and a "Start a project" button with arrow.

\*\*Hero Content (z-20):\*\* Positioned at the bottom of the viewport using flexbox (flex-1 spacer above). Max-w-\[1440px\], px-5 sm:px-8 lg:px-12, pb-14 sm:pb-16 lg:pb-20.

\- Small label: "Axion Studio" (13px/14px, text-gray-900, tracking-wide, mb-5 sm:mb-8)  
\- Headline h1: "We craft digital experiences / for brands ready to dominate / their category online." \- clamp(1.75rem,7vw,4.2rem) on mobile, clamp(2.5rem,5vw,4.2rem) on sm+. font-medium, leading-\[1.08\], tracking-\[-0.03em\], text-gray-900. Line breaks hidden on mobile (uses \`\<br className="hidden sm:block" /\>\` with \`\<span className="sm:hidden"\> \</span\>\` fallback spaces).  
\- CTA row (mt-8 sm:mt-12, flex-col sm:flex-row, gap-4 sm:gap-5):  
  \- Orange button: bg-\[\#F26522\], hover:bg-\[\#e05a1a\], text-white, 13px/14px, rounded-full, pl-5 sm:pl-6 pr-2 py-2. Same text-roll hover animation for "Start a project". White circle (w-7 h-7 sm:w-8 sm:h-8) with orange ArrowRight that rotates \-45deg on hover.  
  \- Partner badge: White pill with subtle shadow (0\_2px\_8px\_rgba(0,0,0,0.08)), hover shadow (0\_4px\_16px\_rgba(0,0,0,0.12)), rounded-\[4px\]. Contains an inline SVG icon (the starburst/compass shape below, w-5 h-5 sm:w-6 sm:h-6, fill-current text-\[\#E8704E\]), text "Certified Partner" (13px/14px font-medium), and a dark badge "Featured" (10px/11px, bg-gray-900, text-white, px-1.5 sm:px-2 py-0.5, rounded).

\*\*SVG Icon for partner badge:\*\*  
\`\`\`svg  
\<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"\>\<path d="m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z"/\>\</svg\>  
\`\`\`

\---

\#\# SECTION 2: ABOUT (White background)

\`bg-white\`, pt-16 sm:pt-20 lg:pt-32, pb-12 sm:pb-16 lg:pb-24, overflow-hidden. Max-w-\[1440px\] container.

\*\*Badge row:\*\* px-5 sm:px-8 lg:px-12, flex items-center gap-3, mb-6 sm:mb-8.  
\- Numbered circle: w-6 h-6 sm:w-7 sm:h-7, rounded-full, bg-gray-900, text-white, 11px/12px font-semibold. Shows "1".  
\- Pill label: "Introducing Axion" \- 12px/13px, font-medium, border border-gray-200, rounded-full, px-3 sm:px-4 py-1 sm:py-1.5.

\*\*Heading h2:\*\* "Strategy-led creatives, delivering / results in digital and beyond." \- clamp(1.5rem,4vw,3.2rem), font-medium, leading-\[1.12\], tracking-\[-0.02em\], text-gray-900, mb-12 sm:mb-16 lg:mb-28.

\*\*Content area (responsive):\*\*

\- MOBILE/TABLET (lg:hidden): Stacked \- paragraph \+ button, then images.  
  \- Paragraph: "Through research, creative thinking and iteration we help growing brands realize their digital full potential." \- 15px/17px, leading-\[1.6\], font-medium, text-gray-900.  
  \- Button: "About our studio" \- orange (\#F26522), same text-roll animation, white arrow circle rotates \-45deg.  
  \- Two images: flex-col sm:flex-row, gap-4 sm:gap-5. First: sm:w-\[45%\] aspect-\[438/346\]. Second: sm:w-\[55%\] aspect-\[900/600\]. Both rounded-xl sm:rounded-2xl, object-cover.

\- DESKTOP (hidden lg:grid): \`grid-cols-\[26%\_1fr\_48%\] items-end gap-6 xl:gap-8\`.  
  \- Left column (self-end): Small image, aspect-\[438/346\], rounded-2xl.  
  \- Center column (self-start, flex justify-end): Paragraph (16px/18px, leading-\[1.65\], whitespace-nowrap, with \`\<br/\>\` between lines) \+ orange button.  
  \- Right column (self-end): Large image, aspect-\[3/2\], rounded-2xl.

\*\*Image URLs:\*\*  
\- Small image: \`https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260516\_090123\_74be96d4-9c1b-40cf-932a-96f4f4babed3.png\&w=1280\&q=85\`  
\- Large image: \`https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260516\_090133\_c157d30b-a99a-4477-bec1-a446149ec3f2.png\&w=1280\&q=85\`

\---

\#\# SECTION 3: CASE STUDIES (Light gray background)

\`bg-\[\#F5F5F5\]\`, pt-16 sm:pt-20 lg:pt-28, pb-16 sm:pb-20 lg:pb-28. Max-w-\[1440px\] container.

\*\*Badge row:\*\* Same pattern as Section 2, but number is "2", label is "Featured client work", border-gray-300.

\*\*Heading h2:\*\* "Our projects" \- same clamp sizing as hero headline (clamp(1.75rem,7vw,4.2rem) / clamp(2.5rem,5vw,4.2rem)), font-medium, leading-\[1.08\], tracking-\[-0.03em\], mb-10 sm:mb-14 lg:mb-16.

\*\*Cards Grid:\*\* \`grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6 lg:gap-7\`, px-5 sm:px-8 lg:px-12.

\*\*Card 1 (Narrativ):\*\*  
\- Video container: aspect-\[329/246\], rounded-2xl, overflow-hidden, bg-\[\#1a1d2e\], group, cursor-pointer.  
\- Video: \`src="https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260516\_122702\_390f5305-8719-41d5-ae80-d23ab3796c28.mp4"\`, autoPlay, muted, loop, playsInline, w-full h-full object-cover.  
\- Hover button (absolute bottom-4 left-4): A white circle (h-9 w-9) that expands to w-\[148px\] on group-hover (transition-all duration-300 ease-in-out). Contains "Learn more" text (13px, font-medium, opacity-0 to opacity-100 on hover with delay-100) and a link/chain SVG icon (14x14, \-rotate-45 to rotate-0 on hover). The SVG is the lucide "link" icon drawn manually with two arc paths.  
\- Description: "Winner of Site of the Month 2025 \- an interactive 3D showcase driving record engagement" \- 13px/14px, text-gray-600, mt-4, leading-relaxed.  
\- Title: "Narrativ" \- 14px/15px, font-semibold, text-gray-900, mt-1.

\*\*Card 2 (Luminar):\*\*  
\- Video container: aspect-square, rounded-2xl, overflow-hidden, bg-\[\#6b6b6b\], group, cursor-pointer.  
\- Video: \`src="https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260516\_123323\_f909c2b8-ff6c-4edf-882b-8ebcdbe389b5.mp4"\`, autoPlay, muted, loop, playsInline, w-full h-full object-cover.  
\- Hover button (absolute bottom-4 left-4): A DARK circle (bg-gray-900, h-9 w-9) that expands to w-\[168px\] on group-hover. Contains "View case study" text (13px, font-medium, text-white) and a white ArrowRight icon (size 14\) that transitions from \-rotate-45 to rotate-0 on hover.  
\- Description: "Transforming a dated platform into a conversion-focused brand experience" \- 13px/14px, text-gray-600, mt-4, leading-relaxed.  
\- Title: "Luminar" \- 14px/15px, font-semibold, text-gray-900, mt-1.

\---

\#\# GLOBAL STYLES (index.css):

Standard Tailwind directives plus two utility classes (not actively used in current layout but defined):  
\- \`.liquid-glass\`: rgba(255,255,255,0.01) bg, backdrop-filter blur(4px), inset box-shadow, pseudo-element gradient border using mask-composite.  
\- \`.liquid-glass-strong\`: Same but blur(50px), no pseudo-element.

\---

\#\# TECHNICAL DETAILS:  
\- \*\*Framework:\*\* React 18 \+ TypeScript \+ Vite  
\- \*\*Styling:\*\* Tailwind CSS 3.4 (default config, no custom theme extensions)  
\- \*\*Packages:\*\* \`shaders\` (for Shader, ChromaFlow, FilmGrain, FlutedGlass, Swirl from \`shaders/react\`), \`lucide-react\` (ArrowRight, Clock, Menu, X)  
\- \*\*Font:\*\* System default (no custom font loaded)  
\- \*\*All animations use:\*\* \`duration-500 ease-\[cubic-bezier(0.25,0.1,0.25,1)\]\` unless noted otherwise  
\- \*\*Max content width:\*\* 1440px, centered with mx-auto  
\- \*\*Responsive breakpoints:\*\* Default Tailwind (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)  
\- \*\*Live clock:\*\* Updates every second, shows London timezone in HH:MM format

# Guia 16

Build a modern, interactive hero section using React, Tailwind CSS, and Framer Motion (motion/react). Ensure you follow these precise architecture and styling instructions:  
1\. Fonts & Global Animations  
Import the Inter font from Google Fonts.  
In your CSS setup, configure Tailwind to use it by default (--font-sans: 'Inter', ...).  
Create a keyframe animation in CSS named blink for the typewriter cursor:  
code  
CSS  
@keyframes blink {  
  0%, 100% { opacity: 1; }  
  50% { opacity: 0; }  
}  
.animate-blink { animation: blink 1s step-end infinite; }  
2\. General Page Structure  
Wrap the entire application in a container div with the following classes: relative bg-white text-neutral-900 font-sans selection:bg-\[\#EAECE9\] selection:text-\[\#1C2E1E\] antialiased overflow-x-hidden flex flex-col lg:block lg:min-h-screen.  
3\. Background Video Component (with Native Scrubbing)  
Container element: Add a div containing the background video with classes: order-last lg:order-none relative lg:absolute lg:inset-0 lg:z-0 overflow-hidden pointer-events-none w-full aspect-square md:aspect-video lg:aspect-auto lg:h-full bg-neutral-50 lg:bg-transparent.  
Video element: Use \<video\> with muted, playsInline, preload="auto".  
Video Source URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260601\_110537\_3a579fa0-7bbc-4d94-9d25-0e816c7840f5.mp4  
Classes: w-full h-full object-cover object-right lg:object-right-bottom.  
Scrubbing/Playback Logic via useEffect hooks:  
Desktop Mouse Scrubbing Hook: Listen to the window mousemove event. If window.innerWidth \< 1024, ignore (disable scrubbing). Store the mouse 'previous X' coordinate to calculate the delta against 'current X'. Update the target scrub time based on (delta / window.innerWidth) \* 0.8 \* video.duration. Clamp the time between 0 and duration. Set video.currentTime \= targetTime. Bind a seeked event listener to ensure smooth tracking frame to frame.  
Mobile Autoplay Hook: Because scrubbing is disabled on mobile frames, trigger normal playback for screens \< 1024 width: video.autoplay \= true and video.play().  
4\. Interactive Navbar  
Header wrapper: Wrap the Navbar in \<header className="fixed top-0 inset-x-0 z-10 px-5 sm:px-8 py-4 sm:py-5 flex flex-row justify-between items-center bg-transparent"\>  
Logo (Left side): Flex row with gap-3.  
Text: Mainframe\&reg; (using the ® symbol). Classes: text-\[21px\] sm:text-\[26px\] tracking-tight text-black font-medium select-none.  
Icon block right beside it: An asterisk &\#10033;. Classes: text-\[25px\] sm:text-\[30px\] text-black select-none tracking-\[-0.02em\] font-medium leading-none mb-1.  
Desktop Nav Links (Center): Flex row, hidden md:flex, text-\[23px\] text-black. Links are "Labs", "Studio", "Openings", "Shop" separated by \<span className="opacity-40"\>,\&nbsp;\</span\> dividers. Hover states should use hover:opacity-60 transition-opacity.  
Desktop CTA (Right): Hidden on mobile. A link reading "Get in touch" mapped with text-\[23px\] text-black underline underline-offset-2 hover:opacity-60 transition-opacity.  
Mobile Menu Logic:  
Hamburger \<button\> visible below md. Has three w-6 h-\[2px\] bg-black spans.  
Hook it to a local state isMobileMenuOpen. When open, animate the burger into an 'X' (top bar rotate-45 translate-y-\[7px\], middle bar opacity-0, bottom bar \-rotate-45 \-translate-y-\[7px\]). All spans need transition-all duration-300.  
Create a full screen Mobile Navigation Overlay div hidden on Desktop. Fixed inset-0 z-\[9\] with bg-white/95 backdrop-blur-sm. Apply opacity-100 pointer-events-auto when isMobileMenuOpen is true; otherwise, opacity-0 pointer-events-none.  
5\. Content Layout Container  
Below the background video and relative to it, add a content grouping layer: \<div className="relative z-10 flex flex-col order-first lg:order-none w-full bg-white lg:bg-transparent pb-8 lg:pb-0 lg:min-h-screen"\>  
Inside that, the overarching layout engine: \<main id="spade-hero" className="w-full max-w-7xl mx-auto px-6 py-12 flex-1 flex flex-col justify-center"\>  
6\. Typewriter Hook and Headline  
Implement a custom useTypewriter(text, speed \= 38, startDelay \= 600\) React hook. It uses setTimeout and setInterval to iteratively build a string slice by slice. It must return an object: { displayed: string, done: boolean }.  
Run the hook with the string "we'd love to\\nhear from you\!".  
Wrap the headline securely in a motion.div configured to drop-in (initial: opacity: 0, y: 20, animate: opacity: 1, y: 0, transition duration 0.6).  
Render your hook text inside \<h1 className="text-5xl md:text-6xl lg:text-\[76px\] font-normal tracking-tight text-black leading-\[1.08\] mb-8 select-none w-full whitespace-pre-wrap"\>.  
While typing (\!done), output a \<span className="inline-block w-\[2px\] h-\[1.1em\] bg-black align-middle ml-\[2px\] animate-blink" /\> cursor at the end of the displayed text string.  
7\. Secondary Description Text  
Another motion.div (delay 0.1s from the headline).  
Content: \<p\> tag that reads: Whether you have questions, feedback, \<br /\> drop us a message and we'll get back to you as soon as possible.  
Classes: text-lg md:text-xl text-\[\#5A635A\] leading-relaxed font-normal mb-14 max-w-2xl.  
8\. Interactive Multi-Select Service Pills  
Using setServices track an array \["Brand", "Digital", "Campaign", "Other"\].  
The prompt Title: "What sort of service?" (text-2xl font-medium tracking-tight mb-2). Subtitle: "Select all that apply" (opacity-85 text-\[\#738273\] mb-8).  
Iterate over the options natively outputting motion.button wrapper tags allowing multiple selections inside a flex wrap container.  
Pill active traits classes: bg-\[\#1C2E1E\] text-white shadow-md shadow-emerald-950/5 transform. Show a check icon (lucide-react) dropping in using type: "spring", stiffness: 300, damping: 20\.  
Pill inactive traits classes: bg-white text-\[\#1C2E1E\] border border-\[\#F1F3F1\] hover:bg-\[\#F1F3F1\]/55.  
Contingent Feedback Status Banner: Underneath your service pills, write an \<AnimatePresence mode="wait"\> that tracks user state array length:  
Empty: Show a generic placeholder indicating "Please click to select services above." at fifty percent opacity (opacity: 0.5, italic, text-xs).  
Active Selection: Swap cleanly into a container \<motion.div\> that springs height gracefully (height: "auto"). Inside, display an acknowledgment banner reading "Ready to inquire about: \[array.join(", ")\]" combined with an arrow call-to-action button "Let's Go" (text-\[\#4D6D47\] uppercase text-xs). Style the banner with bg-\[\#FAFBF9\] border rounded-2xl.

# Guia 17

Build a modern, interactive hero section using React, Tailwind CSS, and Framer Motion (motion/react). Ensure you follow these precise architecture and styling instructions:  
1\. Fonts & Global Animations  
Import the Inter font from Google Fonts.  
In your CSS setup, configure Tailwind to use it by default (--font-sans: 'Inter', ...).  
Create a keyframe animation in CSS named blink for the typewriter cursor:  
code  
CSS  
@keyframes blink {  
  0%, 100% { opacity: 1; }  
  50% { opacity: 0; }  
}  
.animate-blink { animation: blink 1s step-end infinite; }  
2\. General Page Structure  
Wrap the entire application in a container div with the following classes: relative bg-white text-neutral-900 font-sans selection:bg-\[\#EAECE9\] selection:text-\[\#1C2E1E\] antialiased overflow-x-hidden flex flex-col lg:block lg:min-h-screen.  
3\. Background Video Component (with Native Scrubbing)  
Container element: Add a div containing the background video with classes: order-last lg:order-none relative lg:absolute lg:inset-0 lg:z-0 overflow-hidden pointer-events-none w-full aspect-square md:aspect-video lg:aspect-auto lg:h-full bg-neutral-50 lg:bg-transparent.  
Video element: Use \<video\> with muted, playsInline, preload="auto".  
Video Source URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260601\_110537\_3a579fa0-7bbc-4d94-9d25-0e816c7840f5.mp4  
Classes: w-full h-full object-cover object-right lg:object-right-bottom.  
Scrubbing/Playback Logic via useEffect hooks:  
Desktop Mouse Scrubbing Hook: Listen to the window mousemove event. If window.innerWidth \< 1024, ignore (disable scrubbing). Store the mouse 'previous X' coordinate to calculate the delta against 'current X'. Update the target scrub time based on (delta / window.innerWidth) \* 0.8 \* video.duration. Clamp the time between 0 and duration. Set video.currentTime \= targetTime. Bind a seeked event listener to ensure smooth tracking frame to frame.  
Mobile Autoplay Hook: Because scrubbing is disabled on mobile frames, trigger normal playback for screens \< 1024 width: video.autoplay \= true and video.play().  
4\. Interactive Navbar  
Header wrapper: Wrap the Navbar in \<header className="fixed top-0 inset-x-0 z-10 px-5 sm:px-8 py-4 sm:py-5 flex flex-row justify-between items-center bg-transparent"\>  
Logo (Left side): Flex row with gap-3.  
Text: Mainframe\&reg; (using the ® symbol). Classes: text-\[21px\] sm:text-\[26px\] tracking-tight text-black font-medium select-none.  
Icon block right beside it: An asterisk &\#10033;. Classes: text-\[25px\] sm:text-\[30px\] text-black select-none tracking-\[-0.02em\] font-medium leading-none mb-1.  
Desktop Nav Links (Center): Flex row, hidden md:flex, text-\[23px\] text-black. Links are "Labs", "Studio", "Openings", "Shop" separated by \<span className="opacity-40"\>,\&nbsp;\</span\> dividers. Hover states should use hover:opacity-60 transition-opacity.  
Desktop CTA (Right): Hidden on mobile. A link reading "Get in touch" mapped with text-\[23px\] text-black underline underline-offset-2 hover:opacity-60 transition-opacity.  
Mobile Menu Logic:  
Hamburger \<button\> visible below md. Has three w-6 h-\[2px\] bg-black spans.  
Hook it to a local state isMobileMenuOpen. When open, animate the burger into an 'X' (top bar rotate-45 translate-y-\[7px\], middle bar opacity-0, bottom bar \-rotate-45 \-translate-y-\[7px\]). All spans need transition-all duration-300.  
Create a full screen Mobile Navigation Overlay div hidden on Desktop. Fixed inset-0 z-\[9\] with bg-white/95 backdrop-blur-sm. Apply opacity-100 pointer-events-auto when isMobileMenuOpen is true; otherwise, opacity-0 pointer-events-none.  
5\. Content Layout Container  
Below the background video and relative to it, add a content grouping layer: \<div className="relative z-10 flex flex-col order-first lg:order-none w-full bg-white lg:bg-transparent pb-8 lg:pb-0 lg:min-h-screen"\>  
Inside that, the overarching layout engine: \<main id="spade-hero" className="w-full max-w-7xl mx-auto px-6 py-12 flex-1 flex flex-col justify-center"\>  
6\. Typewriter Hook and Headline  
Implement a custom useTypewriter(text, speed \= 38, startDelay \= 600\) React hook. It uses setTimeout and setInterval to iteratively build a string slice by slice. It must return an object: { displayed: string, done: boolean }.  
Run the hook with the string "we'd love to\\nhear from you\!".  
Wrap the headline securely in a motion.div configured to drop-in (initial: opacity: 0, y: 20, animate: opacity: 1, y: 0, transition duration 0.6).  
Render your hook text inside \<h1 className="text-5xl md:text-6xl lg:text-\[76px\] font-normal tracking-tight text-black leading-\[1.08\] mb-8 select-none w-full whitespace-pre-wrap"\>.  
While typing (\!done), output a \<span className="inline-block w-\[2px\] h-\[1.1em\] bg-black align-middle ml-\[2px\] animate-blink" /\> cursor at the end of the displayed text string.  
7\. Secondary Description Text  
Another motion.div (delay 0.1s from the headline).  
Content: \<p\> tag that reads: Whether you have questions, feedback, \<br /\> drop us a message and we'll get back to you as soon as possible.  
Classes: text-lg md:text-xl text-\[\#5A635A\] leading-relaxed font-normal mb-14 max-w-2xl.  
8\. Interactive Multi-Select Service Pills  
Using setServices track an array \["Brand", "Digital", "Campaign", "Other"\].  
The prompt Title: "What sort of service?" (text-2xl font-medium tracking-tight mb-2). Subtitle: "Select all that apply" (opacity-85 text-\[\#738273\] mb-8).  
Iterate over the options natively outputting motion.button wrapper tags allowing multiple selections inside a flex wrap container.  
Pill active traits classes: bg-\[\#1C2E1E\] text-white shadow-md shadow-emerald-950/5 transform. Show a check icon (lucide-react) dropping in using type: "spring", stiffness: 300, damping: 20\.  
Pill inactive traits classes: bg-white text-\[\#1C2E1E\] border border-\[\#F1F3F1\] hover:bg-\[\#F1F3F1\]/55.  
Contingent Feedback Status Banner: Underneath your service pills, write an \<AnimatePresence mode="wait"\> that tracks user state array length:  
Empty: Show a generic placeholder indicating "Please click to select services above." at fifty percent opacity (opacity: 0.5, italic, text-xs).  
Active Selection: Swap cleanly into a container \<motion.div\> that springs height gracefully (height: "auto"). Inside, display an acknowledgment banner reading "Ready to inquire about: \[array.join(", ")\]" combined with an arrow call-to-action button "Let's Go" (text-\[\#4D6D47\] uppercase text-xs). Style the banner with bg-\[\#FAFBF9\] border rounded-2xl.

# Guia 18

Build a full-screen dark hero section landing page in React \+ Vite \+ Tailwind CSS v4 \+ Motion (framer-motion) \+ Lucide React icons \+ hls.js. The page should be a single screen (100vh, no scroll) with a black background, a fullscreen background video, a glassmorphism navbar, and a centered hero with an email capture CTA.  
\>  
\> \*\*Dependencies:\*\* \`react\`, \`react-dom\`, \`motion\`, \`hls.js\`, \`lucide-react\`, \`tailwindcss\` v4 with \`@tailwindcss/vite\`, \`@vitejs/plugin-react\`  
\>  
\> \*\*Fonts:\*\* Import Google Fonts:  
\> \- \`Inter\` (weights 300, 400, 500, 600\) \-- used as the base sans-serif font  
\> \- \`Instrument Serif\` (regular and italic) \-- used for the hero heading  
\>  
\> \*\*CSS (\`index.css\`):\*\*  
\> \- Import both Google Font URLs, then \`@import "tailwindcss";\`  
\> \- Set \`@theme { \--font-sans: "Inter", ui-sans-serif, system-ui, sans-serif; }\`  
\> \- \`:root\` variables: \`--background: \#000000; \--foreground: \#ffffff;\`  
\> \- \`body\`: background-color var(--background), color var(--foreground), font-family var(--font-sans), \`-webkit-font-smoothing: antialiased\`, \`letter-spacing: \-0.01em\`  
\> \- \`.liquid-glass\` class: \`background: rgba(255,255,255,0.01)\`, \`background-blend-mode: luminosity\`, \`backdrop-filter: blur(4px)\`, \`-webkit-backdrop-filter: blur(4px)\`, \`border: none\`, \`box-shadow: inset 0 1px 1px rgba(255,255,255,0.1)\`, \`position: relative\`, \`overflow: hidden\`. It has a \`::before\` pseudo-element for a gradient border effect: \`padding: 1.4px\`, \`background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)\`, masked with \`-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0)\` and \`-webkit-mask-composite: xor; mask-composite: exclude;\`  
\> \- \`.glass-pill\` class: \`background: rgba(255,255,255,0.04)\`, \`backdrop-filter: blur(16px) saturate(180%)\`, \`border-radius: 9999px\`, \`box-shadow: none \!important\`  
\>  
\> \*\*Background Video component:\*\*  
\> \- Renders an absolutely positioned \`\<div\>\` covering the full parent (\`absolute inset-0 overflow-hidden pointer-events-none\`)  
\> \- Contains a \`\<video\>\` element: \`autoPlay\`, \`muted\`, \`loop\`, \`playsInline\`, classes \`w-full h-full object-cover opacity-100\`  
\> \- Video source URL: \`https://stream.mux.com/kimF2ha9zLrX64H00UgLGPflCzNtl1T0215MlAmeOztv8.m3u8\` (this is an HLS stream from Mux, NOT CloudFront)  
\> \- Uses \`hls.js\`: if the browser natively supports HLS (\`video.canPlayType("application/vnd.apple.mpegurl")\`), set \`video.src\` directly; otherwise instantiate \`new Hls()\`, \`loadSource\`, \`attachMedia\`  
\>  
\> \*\*Navbar component:\*\*  
\> \- Animates in with \`motion.nav\`: \`initial={{ y: \-20, opacity: 0 }}\`, \`animate={{ y: 0, opacity: 1 }}\`  
\> \- Classes: \`relative z-20 px-6 py-6 w-full\`  
\> \- Inner container: \`liquid-glass rounded-full px-6 py-3 flex items-center justify-between max-w-5xl mx-auto\`  
\> \- Left side (\`flex items-center gap-8\`):  
\>   \- Logo: \`Globe\` icon from lucide-react (w-6 h-6 text-white) \+ "Asme" text (\`text-white font-semibold text-lg\`), in a \`flex items-center gap-2\` wrapper  
\>   \- Nav links: "Features", "Pricing", "About" \-- hidden on mobile (\`hidden md:flex\`), \`items-center gap-8 text-white/80 text-sm font-medium\`, each link has \`hover:text-white transition-colors duration-300\`  
\> \- Right side (\`flex items-center gap-4\`):  
\>   \- "Sign Up" plain text button: \`text-white hover:text-white/80 transition-colors text-sm font-medium cursor-pointer\`  
\>   \- "Login" glassmorphism button: \`liquid-glass rounded-full px-6 py-2 text-sm font-medium text-white hover:opacity-90 transition-opacity cursor-pointer\`  
\>  
\> \*\*Hero component:\*\*  
\> \- \`\<section\>\` with \`relative flex-1 flex flex-col items-center justify-center px-6\`  
\> \- Content wrapper: \`relative z-10 text-center max-w-5xl mx-auto flex flex-col items-center justify-center w-full gap-12\`  
\> \- \*\*Tagline\*\* (motion.p): text "BUILD A NO-CODE AI APP IN MINUTES", \`text-white/80 text-\[10px\] md:text-\[11px\] font-medium tracking-\[0.2em\] uppercase mb-4\`, animates \`initial={{ opacity: 0, y: 10 }}\`, \`animate={{ opacity: 1, y: 0 }}\`, \`transition={{ delay: 0.1 }}\`  
\> \- \*\*Heading\*\* (motion.h1): text "A new way to think and create with computers" (with \`\<br className="hidden md:block" /\>\` after "create"), \`fontFamily: "'Instrument Serif', serif"\` set via inline style, classes \`text-4xl md:text-\[64px\] font-medium tracking-\[-0.01em\] leading-\[1.1\] mb-6 bg-gradient-to-b from-white via-white/95 to-white/70 bg-clip-text text-transparent max-w-4xl\`, animates \`initial={{ opacity: 0, y: 20 }}\`, \`animate={{ opacity: 1, y: 0 }}\`, \`transition={{ duration: 1, ease: \[0.16, 1, 0.3, 1\] }}\`  
\> \- \*\*CTA area\*\* (motion.div): \`min-h-\[50px\] mt-2\`, animates with \`delay: 0.4\`. Uses \`AnimatePresence mode="wait"\` to toggle between:  
\>   \- \*\*Button state\*\*: "Get early access" \-- \`px-10 py-3 text-\[14px\] font-medium border border-white/10 rounded-full hover:border-white/30 hover:bg-white/\[0.02\] transition-all duration-300 text-white/90 backdrop-blur-sm cursor-pointer\`. On click, switches to email form.  
\>   \- \*\*Email form state\*\*: a \`\<form\>\` with \`flex items-center gap-2 pl-5 pr-1.5 py-1.5 text-\[14px\] font-medium border border-white/20 rounded-full bg-white/\[0.02\] backdrop-blur-sm w-full max-w-\[320px\] focus-within:border-white/40 transition-colors duration-300\`. Contains an email \`\<input\>\` (transparent background, white text, \`placeholder-white/45\`, \`autoFocus\`) and a submit button with either \`ArrowRight\` icon (default) or \`Check\` icon (after submit). Both states animate scale 0.95 to 1 with 0.2s duration.  
\>   \- \*\*Typewriter placeholder\*\*: when the email form opens, the placeholder text "Enter Your Email Here For Early Access" types in character by character at 60ms intervals. After submission, it types "You Will Receive Notifications By Email" instead. After 4 seconds, it resets back to the button state.  
\> \- \*\*"Play Video Demo"\*\* link below (motion.div with \`delay: 0.8\` fade-in): \`text-white/80 hover:text-white/40 transition-colors duration-300 text-\[13px\] font-medium tracking-wide\`  
\>  
\> \*\*App root layout:\*\*  
\> \- \`\<main\>\` with \`relative bg-black h-screen w-screen flex flex-col overflow-hidden selection:bg-white selection:text-black shrink-0\`  
\> \- Render order: \`BackgroundVideo\`, \`Navbar\`, \`Hero\`  
\> \- Text selection is styled white bg with black text

\---

Key clarification: The video URL is \*\*not\*\* from CloudFront. It is an HLS stream hosted on \*\*Mux\*\*: \`https://stream.mux.com/kimF2ha9zLrX64H00UgLGPflCzNtl1T0215MlAmeOztv8.m3u8\`. The \`.m3u8\` format requires hls.js for non-Safari browsers.

# Guia 19

Build a single-page hero section with a full-screen looping background video, liquid glass UI elements, and a dark cinematic aesthetic. Use React, TypeScript, Tailwind CSS, and Lucide React icons. Here are the exact specifications:

Background Video:

Full-screen muted autoplaying video covering the entire viewport, positioned absolutely with object-cover  
Video source URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260328\_115001\_bcdaa3b4-03de-47e7-ad63-ae3e392c32d4.mp4  
The video is shifted down by 17% (translate-y-\[17%\]) so the top portion of the video is cropped \-- the interesting content is in the lower portion of the frame  
The video loops seamlessly with a custom JavaScript fade system (no CSS transitions): 500ms requestAnimationFrame-based fade-in on load/loop start, 500ms fade-out when 0.55 seconds remain before the video ends. A fadingOutRef boolean prevents re-triggering the fade-out from repeated timeUpdate events. On ended, opacity is set to 0, then after 100ms the video resets to currentTime \= 0, plays, and fades back in. Each new fade cancels any running animation frame to prevent competing animations. Fades resume from the current opacity rather than snapping.  
The outer container is min-h-screen bg-black with overflow-hidden

Font:

Import Google Font "Instrument Serif" (both regular and italic) via CSS @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1\&display=swap')  
The heading uses fontFamily: "'Instrument Serif', serif" applied via inline style

Liquid Glass CSS (.liquid-glass class):

background: rgba(255, 255, 255, 0.01) with background-blend-mode: luminosity  
backdrop-filter: blur(4px) and \-webkit-backdrop-filter: blur(4px)  
border: none  
box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1)  
position: relative; overflow: hidden  
A ::before pseudo-element creates the glass border effect:  
position: absolute; inset: 0; border-radius: inherit; padding: 1.4px  
background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)  
Mask trick for border-only rendering: \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0); \-webkit-mask-composite: xor; mask-composite: exclude  
pointer-events: none

Layout (all inside one full-screen flex column):

Navigation bar (relative z-20, padding pl-6 pr-6 py-6):  
Inner container: rounded-full px-6 py-3 flex items-center justify-between max-w-5xl mx-auto  
Left side: Logo area with a Globe icon (size 24\) and text "Asme" in white, font-semibold text-lg, with gap-2  
Next to the logo (with gap-8): three nav links ("Features", "Pricing", "About") \-- hidden on mobile, shown on md: \-- styled text-white/80 hover:text-white transition-colors text-sm font-medium  
Right side (gap-4): "Sign Up" as plain white text button, "Login" as a liquid-glass rounded-full px-6 py-2 button

Hero content area (relative z-10 flex-1 flex flex-col items-center justify-center px-6 py-12 text-center \-translate-y-\[20%\]):  
Heading: "Built for the curious" \-- text-5xl md:text-6xl lg:text-7xl text-white mb-8 tracking-tight whitespace-nowrap with Instrument Serif font  
Below the heading, a max-w-xl w-full space-y-4 container:  
Email input bar: liquid-glass rounded-full pl-6 pr-2 py-2 flex items-center gap-3. Inside: a transparent email input (placeholder: "Enter your email", text-white placeholder:text-white/40 text-base) and a white circular submit button (bg-white rounded-full p-3 text-black) containing an ArrowRight icon (size 20\)  
Subtitle text: text-white text-sm leading-relaxed px-4 \-- "Stay updated with the latest news and insights. Subscribe to our newsletter today and never miss out on exciting updates."  
Manifesto button: centered, liquid-glass rounded-full px-8 py-3 text-white text-sm font-medium hover:bg-white/5 transition-colors

Social icons footer (relative z-10 flex justify-center gap-4 pb-12):  
Three circular icon buttons, each liquid-glass rounded-full p-4 text-white/80 hover:text-white hover:bg-white/5 transition-all  
Icons: Instagram, Twitter, Globe (all size 20\) from lucide-react  
Each has an aria-label

Tech stack: Vite \+ React 18 \+ TypeScript, Tailwind CSS 3, lucide-react for all icons. Default Tailwind config with no extensions. No other UI libraries.

# Guia 20

Build a password manager landing page hero section using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React icons. Here is every specification:

\---

\#\#\# Fonts

\- \*\*Heading font:\*\* "Helvetica Now Display Bold" \-- load via this stylesheet in \`index.html\`:  
  \`\`\`  
  \<link href="https://db.onlinewebfonts.com/c/04e6981992c0e2e7642af2074ebe3901?family=Helvetica+Now+Display+Bold" rel="stylesheet"\>  
  \`\`\`  
\- \*\*Body font:\*\* "Inter" (weights 300-900) \-- load via Google Fonts in \`index.css\`:  
  \`\`\`  
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900\&display=swap');  
  \`\`\`

\#\#\# CSS Variables (defined in \`:root\` in \`index.css\`)

\`\`\`  
\--font-heading: 'Helvetica Now Display Bold', sans-serif;  
\--font-body: 'Inter', sans-serif;  
\--color-text: \#192837;  
\--color-accent: \#7342E2;  
\--color-login-bg: \#F2F2EE;  
\`\`\`

Global reset: \`\* { box-sizing: border-box; }\`, body uses \`var(--font-body)\`, \`var(--color-text)\`, margin/padding 0\.

\---

\#\#\# Background

Full-viewport looping background video, absolutely positioned, covering the entire page with \`object-cover\`. URL:

\`\`\`  
https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260606\_131516\_eca35265-ea66-4fbd-8d52-22aae6e1a503.mp4  
\`\`\`

Attributes: \`autoPlay\`, \`muted\`, \`loop\`, \`playsInline\`. Classes: \`absolute inset-0 z-0 w-full h-full object-cover\`.

\---

\#\#\# Logo (inline SVG component)

A custom geometric SVG logo, 32x32, viewBox \`0 0 256 256\`, fill \`\#192837\`:

\`\`\`  
M 64 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 L 128 64 L 128 64.5 L 161 32 L 192 0 L 256 0 L 256 64 L 192 128 L 128 128 L 128 192 L 96 223 L 63.5 256 L 0 256 L 0 192 Z M 256 192 L 224 223 L 191.5 256 L 128 256 L 128 192 L 192 128 L 256 128 Z  
\`\`\`

\---

\#\#\# Navbar

\- Max-width \`1280px\`, centered with \`margin: 0 auto\`.  
\- Padding: \`px-5 sm:px-8 py-4 sm:py-5\`.  
\- \`relative z-10\`, flexbox with \`justify-between\`, \`items-center\`.  
\- \*\*Left:\*\* Logo component.  
\- \*\*Center (desktop, hidden on mobile \`md:flex\`):\*\* 5 nav links \-- "Vault", "Plans", "Install", "News", "Help". Each is \`text-sm font-medium\`, color \`var(--color-text)\`, \`transition-opacity hover:opacity-70\`, gap-8.  
\- \*\*Right (desktop, hidden on mobile \`md:flex\`):\*\* Two pill buttons with \`gap-3\`:  
  \- "Start For Free": background \`\#7342E2\`, white text, \`text-sm font-semibold px-5 py-2.5 rounded-full\`, hover shadow, active scale-95.  
  \- "Sign In": background \`\#F2F2EE\`, text \`var(--color-text)\`, same sizing/rounding.  
\- \*\*Mobile (\`md:hidden\`):\*\* Hamburger button using Lucide \`Menu\` icon (24px). Toggles to \`X\` icon when open.

\---

\#\#\# Mobile Menu (slide-in sheet)

Uses Framer Motion \`AnimatePresence\`. Two layers:

1\. \*\*Backdrop:\*\* Fixed overlay, \`rgba(25,40,55,0.35)\` background, \`backdrop-blur(4px)\`. Fades in/out over 0.3s. Clicking dismisses the menu.

2\. \*\*Sheet:\*\* Fixed, right-aligned, \`width: min(88vw, 360px)\`, \`height: 100dvh\`, background \`\#CFC8C5\`, box-shadow \`-12px 0 48px rgba(25,40,55,0.18)\`. Slides in from right with custom cubic bezier \`\[0.22, 1, 0.36, 1\]\` over 0.45s; exits with \`\[0.55, 0, 1, 0.45\]\` over 0.35s.

   Contents:  
   \- \*\*Header:\*\* Logo \+ circular close button (40x40, background \`rgba(25,40,55,0.1)\`, X icon 20px), with \`whileTap={{ scale: 0.9 }}\`.  
   \- \*\*Divider:\*\* 1px line, \`rgba(25,40,55,0.12)\`, margin \`0 24px\`.  
   \- \*\*Nav links:\*\* Each link staggers in from right (x: 24 to 0, delay \`0.18 \+ i \* 0.07\`, duration 0.4s). Font size \`1.1rem\`, rounded-xl, hover \`bg-black/10\`.  
   \- \*\*CTA buttons:\*\* Same "Start For Free" (\`\#7342E2\`) and "Sign In" (\`\#F2F2EE\`) as desktop, full-width, \`py-3.5 rounded-full\`, font size \`0.95rem\`.

\---

\#\#\# Hero Content

\- Centered container, max-width \`1280px\`, \`relative z-10\`.  
\- Padding top: \`clamp(40px, 8vw, 72px)\`, bottom \`48px\`.  
\- Inner content wrapper: max-width \`660px\`, centered.

\*\*Heading (\`\<h1\>\`):\*\*  
\- Font: \`var(--font-heading)\`.  
\- Size: \`clamp(1.65rem, 5vw, 3rem)\`.  
\- Line-height: \`1.05\`, letter-spacing: \`-0.01em\`.  
\- Color: \`var(--color-text)\`.  
\- Text-align: center.  
\- Two lines:  
  \- Line 1 (nowrap): \`Lock\` \[Zap icon 24px\] \`Down Your\` \[LockKeyhole icon 24px\] \`Passwords\`  
  \- Line 2: \`with Ironclad Security\` \[Fingerprint icon 24px\]  
\- All inline icons: color \`\#192837\`, \`display: inline\`, \`verticalAlign: middle\`, \`position: relative\`, \`top: \-2px\`, margin \`0 4px\` (Fingerprint has \`marginLeft: 6px\` only).  
\- Animates: fade-up from \`y: 28\`, \`opacity: 0\`, duration 0.6s, ease \`\[0.22, 1, 0.36, 1\]\`, delay \`0 \* 0.15\`.

\*\*Subtext (\`\<p\>\`):\*\*  
\- Font: \`var(--font-body)\`.  
\- Size: \`clamp(0.9rem, 2.5vw, 1.1rem)\`.  
\- Color: \`var(--color-text)\` at \`opacity: 0.8\`.  
\- Max-width: \`560px\`, line-height \`1.65\`, text-align center.  
\- Copy: "Zero stress, total control. Unbreakable storage, one-tap access, and pro-grade tools for your non-stop world."  
\- Animates: same fade-up, delay \`1 \* 0.15\`.

\*\*CTA Button:\*\*  
\- Pill button (\`borderRadius: 50px\`), background \`\#7342E2\`, white text.  
\- Size: \`clamp(0.9rem, 2vw, 1rem)\`, padding \`17px 24px\`, min-width \`210px\`.  
\- Box-shadow: \`0 4px 24px rgba(115,66,226,0.28)\`.  
\- Flexbox with \`justify-between\`, gap \`32px\`.  
\- Label: "Get It Free" with \`ArrowRightCircle\` icon (20px) on right.  
\- Hover: \`scale: 1.04, brightness(1.1)\`. Tap: \`scale: 0.96\`.  
\- Animates: same fade-up, delay \`2 \* 0.15\`.

\---

\#\#\# Animation System (Framer Motion variants)

All hero elements use a shared \`fadeUp\` variant:  
\`\`\`  
hidden: { opacity: 0, y: 28 }  
visible: (i) \=\> ({ opacity: 1, y: 0, transition: { delay: i \* 0.15, duration: 0.6, ease: \[0.22, 1, 0.36, 1\] } })  
\`\`\`

\---

\#\#\# Dependencies

\- \`react\`, \`react-dom\` (v18)  
\- \`framer-motion\`  
\- \`lucide-react\` (icons: ArrowRightCircle, Zap, LockKeyhole, Fingerprint, Menu, X)  
\- Tailwind CSS 3 with default config, no custom theme extensions  
\- Vite \+ TypeScript

# Guia 21

RECREATION PROMPT

Build a single-page landing site using React \+ TypeScript \+ Vite \+ Tailwind CSS \+ framer-motion \+ lucide-react. The entire page has a bg-black background. The font loaded via Google Fonts is Instrument Serif (italic and regular). Import it in index.css:

@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1\&display=swap');  
LIQUID GLASS CSS (in index.css, inside @layer components)  
Create a reusable .liquid-glass class used on every glass element:

.liquid-glass {  
  background: rgba(255, 255, 255, 0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}

.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(  
    180deg,  
    rgba(255, 255, 255, 0.45) 0%,  
    rgba(255, 255, 255, 0.15) 20%,  
    rgba(255, 255, 255, 0\) 40%,  
    rgba(255, 255, 255, 0\) 60%,  
    rgba(255, 255, 255, 0.15) 80%,  
    rgba(255, 255, 255, 0.45) 100%  
  );  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}  
SECTION 1 \-- HERO (full-viewport, in Index.tsx)  
Full-screen (min-h-screen) container with overflow-hidden relative flex flex-col.

Background video: absolute, covers the entire viewport (absolute inset-0 w-full h-full object-cover object-bottom). URL:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260405\_074625\_a81f018a-956b-43fb-9aee-4d1508e30e6a.mp4  
Attributes: muted, autoPlay, playsInline, preload="auto". Starts at opacity: 0\.

Video fade logic (vanilla JS via refs, no CSS transitions):

On canplay: play the video, then animate opacity from 0 to 1 over 500ms using requestAnimationFrame.  
On timeupdate: when remaining time \<= 0.55s, animate opacity from current to 0 over 500ms.  
On ended: set opacity to 0, wait 100ms, reset currentTime to 0, play again, fade back to 1 over 500ms.  
This creates a seamless loop with smooth crossfade to black between plays.  
Navbar (relative z-20, px-6 py-6):

A liquid-glass rounded-full pill, max-w-5xl mx-auto, px-6 py-3, flex between left/right.  
Left: Globe icon (24px, white) \+ "Asme" text (white, font-semibold, text-lg). Hidden on mobile: nav links "Features", "Pricing", "About" (text-white/80 hover:text-white text-sm font-medium, gap-8 ml-8).  
Right: "Sign Up" text button (white, text-sm, font-medium) \+ "Login" button (liquid-glass rounded-full px-6 py-2, white text-sm font-medium).  
Hero content (relative z-10, flex-1 flex flex-col items-center justify-center, px-6 py-12 text-center, \-translate-y-\[20%\]):

Heading: text-7xl md:text-8xl lg:text-9xl, white, tracking-tight whitespace-nowrap, font-family 'Instrument Serif', serif. Text: Know it then \<em className="italic"\>all\</em\>.  
Email input: max-w-xl w-full. A liquid-glass rounded-full pill with pl-6 pr-2 py-2 flex items-center gap-3. Inside: transparent \<input\> with placeholder "Enter your email" (text-white placeholder:text-white/40). A white circular submit button (bg-white rounded-full p-3 text-black) containing ArrowRight icon (20px).  
Subtitle: text-white text-sm leading-relaxed px-4. Text: "Stay updated with the latest news and insights. Subscribe to our newsletter today and never miss out on exciting updates."  
Manifesto button: liquid-glass rounded-full px-8 py-3 text-white text-sm font-medium hover:bg-white/5 transition-colors.  
Social icons footer (relative z-10, flex justify-center gap-4 pb-12):

Three liquid-glass rounded-full p-4 buttons for Instagram, Twitter, Globe icons (20px). text-white/80 hover:text-white hover:bg-white/5 transition-all.  
SECTION 2 \-- ABOUT SECTION (separate component AboutSection.tsx)  
Uses framer-motion useInView (ref, { once: true, margin: "-100px" }).  
bg-black pt-32 md:pt-44 pb-10 md:pb-14 px-6 overflow-hidden.  
Subtle radial gradient overlay: bg-\[radial-gradient(ellipse\_at\_top,\_rgba(255,255,255,0.03)\_0%,\_transparent\_70%)\].  
Label: "About Us" \-- text-white/40 text-sm tracking-widest uppercase. Animates: opacity: 0, y: 20 \-\> opacity: 1, y: 0, duration 0.6.  
Heading: text-4xl md:text-6xl lg:text-7xl text-white leading-\[1.1\] tracking-tight. Animates: opacity: 0, y: 40 \-\> opacity: 1, y: 0, duration 0.8, delay 0.1. Text structure:  
Pioneering then ideas (Instrument Serif italic, text-white/60) for  
Line break (hidden on mobile)  
minds that then create, build, and inspire. (all Instrument Serif italic, text-white/60)  
SECTION 3 \-- FEATURED VIDEO (separate component FeaturedVideoSection.tsx)  
bg-black pt-6 md:pt-10 pb-20 md:pb-32 px-6 overflow-hidden. Max-w-6xl.  
A rounded-3xl overflow-hidden aspect-video container that animates opacity: 0, y: 60 \-\> opacity: 1, y: 0, duration 0.9.  
Video: w-full h-full object-cover, muted, autoPlay, loop, playsInline, preload="auto". URL:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260402\_054547\_9875cfc5-155a-4229-8ec8-b7ba7125cbf8.mp4  
Gradient overlay on video: bg-gradient-to-t from-black/60 via-transparent to-transparent.  
Bottom overlay content (absolute bottom-0 left-0 right-0 p-6 md:p-10):  
Flex row on desktop, column on mobile.  
Left: a liquid-glass rounded-2xl p-6 md:p-8 max-w-md card. Label "Our Approach" (text-white/50 text-xs tracking-widest uppercase mb-3). Body text (text-white text-sm md:text-base leading-relaxed): "We believe in the power of curiosity-driven exploration. Every project starts with a question, and every answer opens a new door to innovation."  
Right: "Explore more" button (liquid-glass rounded-full px-8 py-3, white text-sm font-medium) with whileHover={{ scale: 1.05 }} and whileTap={{ scale: 0.95 }}.  
SECTION 4 \-- PHILOSOPHY / INNOVATION x VISION (separate component PhilosophySection.tsx)  
bg-black py-28 md:py-40 px-6 overflow-hidden. Max-w-6xl.  
Heading: text-5xl md:text-7xl lg:text-8xl text-white tracking-tight mb-16 md:mb-24. Animates opacity: 0, y: 40 \-\> opacity: 1, y: 0, duration 0.8. Text: Innovation then x in Instrument Serif italic text-white/40, then Vision.  
Two-column grid (grid-cols-1 md:grid-cols-2 gap-8 md:gap-12):  
Left: Video in rounded-3xl overflow-hidden aspect-\[4/3\]. Animates from opacity: 0, x: \-40. URL:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260307\_083826\_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4  
muted, autoPlay, loop, playsInline, preload="auto".  
Right: Animates from opacity: 0, x: 40\. Two text blocks separated by a w-full h-px bg-white/10 divider.  
Block 1: Label "Choose your space" (text-white/40 text-xs tracking-widest uppercase mb-4). Body (text-white/70 text-base md:text-lg leading-relaxed): "Every meaningful breakthrough begins at the intersection of disciplined strategy and remarkable creative vision. We operate at that crossroads, turning bold thinking into tangible outcomes that move people and reshape industries."  
Block 2: Label "Shape the future". Body: "We believe that the best work emerges when curiosity meets conviction. Our process is designed to uncover hidden opportunities and translate them into experiences that resonate long after the first impression."  
SECTION 5 \-- SERVICES / WHAT WE DO (separate component ServicesSection.tsx)  
bg-black py-28 md:py-40 px-6 overflow-hidden. Max-w-6xl.  
Subtle radial gradient: bg-\[radial-gradient(ellipse\_at\_center,\_rgba(255,255,255,0.02)\_0%,\_transparent\_60%)\].  
Header row: flex between "What we do" (text-3xl md:text-5xl text-white tracking-tight) and "Our services" label (text-white/40 text-sm, hidden on mobile). Animates opacity: 0, y: 30 \-\> visible, duration 0.7.  
Two-card grid (grid-cols-1 md:grid-cols-2 gap-6 md:gap-8):  
Each card: liquid-glass rounded-3xl overflow-hidden with group class. Animates opacity: 0, y: 50 \-\> visible, duration 0.8, staggered by 0.15s.  
Card video area: aspect-video, object-cover, transition-transform duration-700 group-hover:scale-105. Gradient overlay: bg-gradient-to-t from-black/40 to-transparent.  
Card body (p-6 md:p-8): tag label (uppercase, tracking-widest, text-white/40 text-xs), ArrowUpRight icon in a liquid-glass rounded-full p-2 circle, title (text-white text-xl md:text-2xl mb-3 tracking-tight), description (text-white/50 text-sm leading-relaxed).  
Card 1: Video URL:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260314\_131748\_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4  
Tag: "Strategy". Title: "Research & Insight". Description: "We dig deep into data, culture, and human behavior to surface the insights that drive meaningful, lasting change."  
Card 2: Video URL:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260324\_151826\_c7218672-6e92-402c-9e45-f1e0f454bdc4.mp4  
Tag: "Craft". Title: "Design & Execution". Description: "From concept to launch, we obsess over every detail to deliver experiences that feel effortless and look extraordinary."

# Guia 22

Create an NFT landing page called "Orbis.Nft" with 4 sections, using a dark space theme. The page uses video backgrounds served from CloudFront, a liquid glass UI effect, and a specific color/font system. Recreate it exactly as described below.

FONTS (Google Fonts)

Anton \- Used for all headings and navigation text (aliased as font-grotesk in Tailwind)

Condiment \- A cursive script used for accent/overlay text (aliased as font-condiment in Tailwind)

System monospace font (font-mono) \- Used for body/description paragraphs

Load via Google Fonts in index.html:

https://fonts.googleapis.com/css2?family=Anton\&family=Condiment\&display=swap

COLOR SYSTEM (Tailwind config)

Background: \#010828 (deep dark navy blue)

cream: \#EFF4FF (off-white, used for all text)

neon: \#6FFF00 (bright green, used for accent cursive text and underline bars)

LIQUID GLASS CSS EFFECT

Applied via a .liquid-glass class. This is used on the navbar, social icon buttons, NFT cards, and card overlays:

.liquid-glass {  
  background: rgba(255, 255, 255, 0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}

TEXTURE OVERLAY

A full-screen fixed texture overlay sits on top of everything (z-50, pointer-events-none). It uses a /texture.png image with mix-blend-mode: lighten at opacity: 0.6, covering the entire viewport with background-size: cover.

SECTION 1: HERO (Full viewport)

Background: Full-bleed looping muted autoplaying video covering the entire section with object-cover

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_045634\_e1c98c76-1265-4f5c-882a-4276f2080894.mp4

Container: max-w-\[1831px\] centered with responsive horizontal padding

Section has rounded-b-\[32px\] bottom corners, clipping the video

Header:

Left: "Orbis.Nft" logo text in Anton, 16px, uppercase

Center: Navigation bar with liquid-glass effect, rounded-\[28px\], px-\[52px\] py-\[24px\]. Contains 5 links: Homepage, Gallery, Buy NFT, FAQ, Contact. Each link is Anton 13px uppercase. Links have hover:text-neon transition. Nav is hidden on mobile (hidden lg:block).

Hero Content:

Large heading in Anton font, responsive sizing: 40px mobile / 60px sm / 75px md / 90px lg. Uppercase. leading-\[1.05\] mobile, leading-\[1\] tablet+. Max width 780px on desktop, offset with lg:ml-32.

Text reads:

Beyond earth  
and ( its ) familiar boundaries

Overlaid cursive accent text "Nft collection" in Condiment font (24px-48px responsive), positioned absolute to the right side of the heading, slightly rotated (-rotate-1), in neon green (text-neon), with mix-blend-exclusion and opacity-90.

Social Icons (Desktop):

3 square buttons (56x56px) stacked vertically in top-right corner, each with liquid-glass and rounded-\[1rem\]. Icons: Mail, Twitter, Github from lucide-react (20x20px). hover:bg-white/10 transition.

Social Icons (Mobile):

Same 3 buttons but centered horizontally below the heading, shown only below lg breakpoint.

SECTION 2: ABOUT / INTRO (Full viewport)

Background: Full-bleed looping muted autoplaying video with object-cover

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_151551\_992053d1-3d3e-4b8c-abac-45f22158f411.mp4

Container: Same max-w-\[1831px\] centered, with generous vertical padding (64px-96px responsive)

Top Row (flex row on desktop, column on mobile):

Left: Heading in Anton, responsive 32px-60px, uppercase:

Hello\!  
I'm orbis

With an overlaid "Orbis" in Condiment cursive, neon green, mix-blend-exclusion, 36px-68px responsive, positioned absolute at bottom-right of heading, slightly rotated.

Right: Short paragraph in monospace 14px-16px, uppercase, cream color, max-width 266px: "A digital object fixed beyond time and place. An exploration of distance, form, and silence in space"

Bottom Row (flex row, space-between):

Two columns (left and right), each containing 2 identical paragraphs. Same monospace text as above but at opacity-10 (nearly invisible, decorative). Right column hidden below lg. On mobile, text uses text-\[\#010828\] (dark) so it's effectively invisible against the video.

SECTION 3: NFT COLLECTION GRID

Background: Solid \#010828 (no video)

Container: Same max-w-\[1831px\] centered

Header Row:

Left: Heading in Anton, 32px-60px responsive, uppercase:

Collection of  
  \[indented\] Space objects

Where "Space" is in Condiment cursive neon green, and "objects" is in Anton. The second line is indented with ml-12 / ml-24 / ml-32 responsive.

Right: A "SEE ALL CREATORS" button. "SEE" is large (32px-60px), "ALL" and "CREATORS" are stacked smaller (20px-36px) next to it. Below the text is a neon green bar (bg-neon, height 6px-10px responsive, full width of button).

NFT Card Grid:

3-column grid on desktop (lg:grid-cols-3), 2 on tablet, 1 on mobile. Gap 24px.

Each card: liquid-glass container with rounded-\[32px\], padding 18px, hover:bg-white/10 transition.

Inside each card: a square video container (pb-\[100%\] aspect ratio trick) with rounded-\[24px\] overflow hidden.

Video URLs:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_053923\_22c0a6a5-313c-474c-85ff-3b50d25e944a.mp4 (Score: 8.7/10)

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_054411\_511c1b7a-fb2f-42ef-bf6c-32c0b1a06e79.mp4 (Score: 9/10)

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_055427\_ac7035b5-9f3b-4289-86fc-941b2432317d.mp4 (Score: 8.2/10)

Each card has an overlay bar at the bottom: a liquid-glass bar with rounded-\[20px\], px-5 py-4, showing "RARITY SCORE:" label (11px, cream/70% opacity) and score value (16px). On the right side of the bar is a circular purple gradient button (48x48px, bg-gradient-to-br from-\[\#b724ff\] to-\[\#7c3aed\]) with a right-arrow chevron SVG inside, with shadow-lg shadow-purple-500/50 and hover:scale-110 transition.

SECTION 4: CTA / FINAL SECTION

Background: Full-width video (NOT object-cover, instead w-full h-auto block so it displays at native aspect ratio)

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_055729\_72d66327-b59e-4ae9-bb70-de6ccb5ecdb0.mp4

Text Content (positioned absolute over the video):

Right-aligned block, offset with lg:pr-\[20%\] lg:pl-\[15%\]

Small "Go beyond" text in Condiment cursive, neon green, mix-blend-exclusion, positioned absolute at top-left of the heading block. Sizes: 17px-68px responsive.

Heading in Anton, responsive 16px-60px, uppercase:

JOIN US.  
REVEAL WHAT'S HIDDEN.  
DEFINE WHAT'S NEXT.  
FOLLOW THE SIGNAL.

"JOIN US." has extra bottom margin (mb-4 to mb-12 responsive) before the remaining lines.

Social Icons (Bottom-left, absolute positioned):

Positioned at left-\[8%\], bottom-\[12%\] to bottom-\[20%\] with responsive breakpoints.

A vertical liquid-glass container with rounded-\[0.5rem\] to rounded-\[1.25rem\] responsive, containing 3 stacked icon buttons (Mail, Twitter, Github).

Buttons have responsive widths using viewport units and rem values (e.g., w-\[14vw\] sm:w-\[14.375rem\] md:w-\[10.78125rem\] lg:w-\[16.77rem\]) and similar responsive heights.

Buttons are separated by border-b border-white/10 dividers (except the last one).

KEY TECHNICAL DETAILS

Framework: React \+ TypeScript \+ Vite \+ Tailwind CSS

Icons: lucide-react (Mail, Twitter, Github)

No additional packages needed beyond what Vite \+ React \+ Tailwind provides

All videos: autoPlay loop muted playsInline attributes

Responsive: Mobile-first with sm:, md:, lg: breakpoints throughout

Max content width: 1831px across all sections

All text is uppercase except the Condiment cursive accents which are normal-case

# Guia 23

Prompt to recreate this landing page:

Build a single-page dark portfolio landing page using React \+ Vite \+ Tailwind CSS \+ TypeScript \+ GSAP \+ Framer Motion \+ hls.js.

\---

\#\# Global Design System

\#\#\# Fonts  
Google Fonts import: Inter (300–700) and Instrument Serif (italic, 400).  
\- \--font-body: 'Inter', sans-serif → Tailwind font-body  
\- \--font-display: 'Instrument Serif', serif → Tailwind font-display

\#\#\# CSS Custom Properties (HSL, no hsl() wrapper — Tailwind adds it)  
\--bg: 0 0% 4%;  
\--surface: 0 0% 8%;  
\--text: 0 0% 96%;  
\--muted: 0 0% 53%;  
\--stroke: 0 0% 12%;  
\--accent: 0 0% 96%;

\#\#\# Tailwind Custom Colors  
bg: "hsl(var(--bg))",  
surface: "hsl(var(--surface))",  
"text-primary": "hsl(var(--text))",  
muted: "hsl(var(--muted))",  
stroke: "hsl(var(--stroke))",

\#\#\# Accent Gradient  
linear-gradient(90deg, \#89AACC 0%, \#4E85BF 100%) — used on logo ring, hover borders, progress bars. CSS utility class .accent-gradient.

\#\#\# Custom Animations (in index.css)  
\- @keyframes scroll-down — translateY(-100%) → translateY(200%), 1.5s ease-in-out infinite  
\- @keyframes role-fade-in — opacity 0 \+ translateY(8px) → opacity 1 \+ translateY(0), 0.4s ease-out  
\- @keyframes gradient-shift — background-position 0% 50% → 100% 50% → 0% 50%, 6s ease infinite (for animated gradient borders)

\#\#\# Forced dark theme — no light mode toggle. body gets bg-bg text-text-primary.

\---

\#\# Page Structure (Index.tsx)

{isLoading && \<LoadingScreen onComplete={() \=\> setIsLoading(false)} /\>}

\---

\#\# Section 1: Loading Screen

Full-screen overlay (fixed inset-0 z-\[9999\] bg-bg). Uses requestAnimationFrame counter from 000→100 over 2700ms.

\- Top-left: "Portfolio" label — text-xs text-muted uppercase tracking-\[0.3em\]. Animates y:-20→0, opacity 0→1.  
\- Center: Rotating words \["Design", "Create", "Inspire"\] cycling every 900ms. AnimatePresence mode="wait" with y:20→0→-20 transitions. text-4xl md:text-6xl lg:text-7xl font-display italic text-text-primary/80.  
\- Bottom-right: Counter display — text-6xl md:text-8xl lg:text-9xl font-display text-text-primary tabular-nums. Shows String(count).padStart(3, "0").  
\- Bottom progress bar: h-\[3px\] bg-stroke/50, inner div with .accent-gradient, scaleX(count/100) transform, box-shadow: 0 0 8px rgba(137, 170, 204, 0.35).  
\- On complete (count reaches 100): 400ms delay then calls onComplete.

\---

\#\# Section 2: Hero

Full-viewport section with background HLS video and centered content.

\#\#\# Background Video  
\- HLS source: https://stream.mux.com/Aa02T7oM1wH5Mk5EEVDYhbZ1ChcdhRsS2m1NYyx4Ua1g.m3u8  
\- Uses hls.js — if Hls.isSupported(), create HLS instance; else if native HLS support, set video.src directly.  
\- Video: autoPlay muted loop playsInline, absolutely positioned and centered with min-w-full min-h-full object-cover \-translate-x-1/2 \-translate-y-1/2.  
\- Dark overlay: bg-black/20  
\- Bottom fade: h-48 bg-gradient-to-t from-bg to-transparent

\#\#\# Navbar (fixed, floats at top center)  
fixed top-0 left-0 right-0 z-50 flex justify-center pt-4 md:pt-6 px-4.

Inner pill: inline-flex items-center rounded-full backdrop-blur-md border border-white/10 bg-surface px-2 py-2. Gets shadow-md shadow-black/10 when scrollY \> 100\.

Contents (left to right):  
1\. Logo: 9×9 circle with accent gradient border (reverses direction on hover). Inner bg-bg circle with "JA" in font-display italic text-\[13px\]. Scales 110% on hover.  
2\. Divider: w-px h-5 bg-stroke mx-1 (hidden on mobile)  
3\. Nav links: \["Home", "Work", "Resume"\] — text-xs sm:text-sm rounded-full px-3 sm:px-4 py-1.5 sm:py-2. Active: text-text-primary bg-stroke/50. Inactive: text-muted hover:text-text-primary hover:bg-stroke/50.  
4\. Divider  
5\. "Say hi" button: Same size as nav links. On hover, shows accent gradient border behind (using absolute span with inset: \-2px). Inner content wrapped in bg-surface rounded-full backdrop-blur-md. Includes "↗" arrow.

\#\#\# Hero Content (centered, z-10)  
\- Eyebrow: text-xs text-muted uppercase tracking-\[0.3em\] mb-8 — "COLLECTION '26". Class blur-in.  
\- Name: text-6xl md:text-8xl lg:text-9xl font-display italic leading-\[0.9\] tracking-tight text-text-primary mb-6 — "Michael Smith". Class name-reveal.  
\- Role line: "A {role} lives in Chicago." — roles cycle every 2s through \["Creative", "Fullstack", "Founder", "Scholar"\]. Role word uses font-display italic text-text-primary animate-role-fade-in inline-block with key={roleIndex} for re-triggering animation.  
\- Description: text-sm md:text-base text-muted max-w-md mb-12 — "Designing seamless digital interactions by focusing on the unique nuances which bring systems to life."  
\- CTA Buttons (inline-flex gap-4):  
  \- "See Works": Solid button. Default: bg-text-primary text-bg. Hover: bg-bg text-text-primary with accent gradient border ring.  
  \- "Reach out...": Outlined button. Default: border-2 border-stroke bg-bg text-text-primary. Hover: border-transparent with accent gradient border ring.  
  \- Both: rounded-full text-sm px-7 py-3.5 hover:scale-105.

\#\#\# GSAP Entrance  
Timeline with ease: "power3.out":  
\- .name-reveal: opacity 0→1, y 50→0, duration 1.2s, delay 0.1s  
\- .blur-in: opacity 0→1, filter blur(10px)→blur(0px), y 20→0, duration 1s, stagger 0.1, delay 0.3s

\#\#\# Scroll Indicator  
Bottom-center, text-xs text-muted uppercase tracking-\[0.2em\] "SCROLL" label above a w-px h-10 bg-stroke line with animated highlight using .animate-scroll-down.

\---

\#\# Section 3: Selected Works

bg-bg py-12 md:py-16. Inner: max-w-\[1200px\] mx-auto px-6 md:px-10 lg:px-16.

\#\#\# Header  
Framer Motion whileInView — opacity 0→1, y 30→0, duration 1s, ease \[0.25,0.1,0.25,1\], viewport once margin "-100px".  
\- Eyebrow: w-8 h-px bg-stroke \+ "Selected Work" text-xs text-muted uppercase tracking-\[0.3em\]  
\- Heading: "Featured \*projects\*" — italic word in font-display italic  
\- Subtext: "A selection of projects I've worked on, from concept to launch."  
\- "View all work" button (desktop only, hidden md:inline-flex) — rounded-full with gradient hover border ring \+ right arrow

\#\#\# Bento Grid  
grid grid-cols-1 md:grid-cols-12 gap-5 md:gap-6. Column spans alternate: 7/5/5/7.

4 project cards with titles: Automotive Motion, Urban Architecture, Human Perspective, Brand Identity.

Each card: bg-surface border border-stroke rounded-3xl with aspect ratios. Contains:  
\- Background image with object-cover group-hover:scale-105  
\- Halftone overlay: radial-gradient(circle, \#000 1px, transparent 1px) at 4×4px, opacity-20 mix-blend-multiply  
\- Hover: bg-bg/70 opacity-0→1 \+ backdrop-blur-lg  
\- Hover label: pill with animated gradient border, white bg, "View — \*Title\*" (title in font-display italic)

\---

\#\# Section 4: Journal

bg-bg py-16 md:py-24. Same header pattern (eyebrow \+ "Recent \*thoughts\*" \+ subtext \+ "View all" button).

4 journal entries displayed as horizontal pills (rounded-\[40px\] sm:rounded-full) with titles, images, read times, and dates.

Each entry: flex items-center gap-6 p-4 bg-surface/30 hover:bg-surface border border-stroke.

\---

\#\# Section 5: Explorations (Parallax Gallery)

min-h-\[300vh\] section for scroll-driven parallax.

\#\#\# Layer 1: Pinned Center (z-10)  
h-screen div pinned with GSAP ScrollTrigger.create({ pin: contentRef, pinSpacing: false }).  
\- Eyebrow: "Explorations"  
\- Heading: "Visual \*playground\*"  
\- Subtext \+ Dribbble button

\#\#\# Layer 2: Parallax Columns (z-20, absolute)  
grid grid-cols-2 gap-12 md:gap-40 inside max-w-\[1400px\].

6 items split into 2 columns with GSAP scroll-driven parallax movement.  
Cards: aspect-square max-w-\[320px\], with rotation and lightbox on click.

\---

\#\# Section 6: Stats

bg-bg py-16 md:py-24. 3-column grid with stats: 20+ Years Experience, 95+ Projects Done, 200% Satisfied Clients.

\---

\#\# Section 7: Contact / Footer

bg-bg pt-16 md:pt-20 pb-8 md:pb-12 overflow-hidden.

\#\#\# Background Video  
Same HLS source as hero, but flipped vertically (scale-y-\[-1\]). Heavier overlay: bg-black/60.

\#\#\# GSAP Marquee  
"BUILDING THE FUTURE • " repeated 10×. GSAP xPercent: \-50, duration 40, ease "none", repeat \-1.

\#\#\# CTA  
Email button: mailto:hello@michaelsmith.com with gradient hover border ring.

\#\#\# Footer Bar  
Social links \[Twitter, LinkedIn, Dribbble, GitHub\] \+ Green pulsing dot \+ "Available for projects"

\---

\#\# Dependencies  
gsap, framer-motion, hls.js, react-router-dom, tailwindcss-animate

Add smooth scroll nav and page transitions.

# Guia 24

Create a fullscreen hero section for a password manager app called "VaultShield" using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React icons.

\---

\#\# Fonts

\- \*\*Heading font:\*\* \`Helvetica Now Display Bold\` loaded from \`https://db.onlinewebfonts.com/c/04e6981992c0e2e7642af2074ebe3901?family=Helvetica+Now+Display+Bold\` (add as a \`\<link\>\` in \`index.html\`)  
\- \*\*Body font:\*\* \`Inter\` (weights 300-900) loaded from Google Fonts: \`https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900\&display=swap\` (imported in CSS)

\#\# CSS Variables

\`\`\`css  
:root {  
  \--font-heading: 'Helvetica Now Display Bold', sans-serif;  
  \--font-body: 'Inter', sans-serif;  
  \--color-text: \#192837;  
  \--color-accent: \#7342E2;  
  \--color-login-bg: \#F2F2EE;  
}  
\`\`\`

\#\# Background Video

Full-screen background video covering the entire viewport (\`absolute inset-0, object-cover\`):

\`\`\`  
https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260518\_003132\_8b7edcb6-c64d-4a52-a9ca-879942e122ad.mp4  
\`\`\`

Attributes: \`autoPlay\`, \`muted\`, \`loop\`, \`playsInline\`

\#\# Layout Structure

1\. \*\*Container:\*\* \`relative w-full min-h-screen\`, font-family from \`--font-body\`, color from \`--color-text\`  
2\. \*\*Navbar:\*\* max-width 1280px, centered, z-10, \`px-5 sm:px-8 py-4 sm:py-5\`, flex with items centered and space-between  
3\. \*\*Hero content:\*\* max-width 1280px centered container with \`paddingTop: clamp(40px, 8vw, 72px)\`, content block capped at \`max-width: 560px\`

\#\# Logo (SVG)

Custom SVG logo, 32x32, fill \`\#192837\`, geometric angular shape:

\`\`\`svg  
\<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" overflow="visible" viewBox="0 0 256 256"\>  
  \<path d="M 64 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 L 128 64 L 128 64.5 L 161 32 L 192 0 L 256 0 L 256 64 L 192 128 L 128 128 L 128 192 L 96 223 L 63.5 256 L 0 256 L 0 192 Z M 256 192 L 224 223 L 191.5 256 L 128 256 L 128 192 L 192 128 L 256 128 Z" fill="\#192837"/\>  
\</svg\>  
\`\`\`

\#\# Navbar Elements

\- \*\*Left:\*\* Logo  
\- \*\*Center (desktop only, \`hidden md:flex\`):\*\* 5 links — \`\['Vault', 'Plans', 'Install', 'News', 'Help'\]\`, text-sm font-medium, opacity hover effect  
\- \*\*Right (desktop only):\*\*  
  \- "Start For Free" button — \`background: \#7342E2\`, white text, rounded-full, \`px-5 py-2.5\`  
  \- "Sign In" button — \`background: \#F2F2EE\`, dark text, rounded-full, \`px-5 py-2.5\`  
\- \*\*Mobile:\*\* Hamburger icon (Menu/X from lucide-react), opens a right-side slide-in sheet

\#\# Mobile Menu Sheet (AnimatePresence \+ Framer Motion)

\- \*\*Backdrop:\*\* fixed inset-0, \`rgba(25,40,55,0.35)\` background with \`blur(4px)\` backdrop-filter  
\- \*\*Sheet:\*\* fixed right-0 top-0, width \`min(88vw, 360px)\`, height \`100dvh\`, background \`\#CFC8C5\`, box-shadow \`-12px 0 48px rgba(25,40,55,0.18)\`  
\- \*\*Sheet animation:\*\* slides from \`x: '100%'\` to \`x: 0\`, ease \`\[0.22, 1, 0.36, 1\]\`, duration 0.45s  
\- \*\*Sheet content:\*\* Logo \+ close button header, 1px divider, staggered nav links (delay \`0.18 \+ i \* 0.07\`), bottom CTA buttons matching desktop style

\#\# Hero Heading

\- Font: \`var(--font-heading)\`  
\- Size: \`clamp(1.65rem, 5vw, 3rem)\`  
\- Line-height: \`1.05\`  
\- Letter-spacing: \`-0.01em\`  
\- Color: \`\#192837\`  
\- Margin-bottom: \`24px\`  
\- Contains inline Lucide icons (Zap, LockKeyhole, Fingerprint) at 24px, color \`\#192837\`, vertically aligned middle, positioned \`top: \-2px\`  
\- Text: "Lock Down Your Passwords with Ironclad Security"  
  \- Zap icon before "Lock"  
  \- LockKeyhole icon between "Passwords" and "with"  
  \- Fingerprint icon after "Security"

\#\# Hero Subtext

\- Font: \`var(--font-body)\`  
\- Size: \`clamp(0.9rem, 2.5vw, 1.1rem)\`  
\- Line-height: \`1.65\`  
\- Opacity: \`0.8\`  
\- Max-width: \`560px\`  
\- Text: "Zero stress, total control. VaultShield keeps you covered with unbreakable storage, one-tap access, and pro-grade tools for your non-stop world."

\#\# CTA Button

\- Background: \`\#7342E2\`  
\- Color: white  
\- Border-radius: \`50px\`  
\- Padding: \`17px 24px\`  
\- Font: \`var(--font-body)\`, font-weight semibold  
\- Size: \`clamp(0.9rem, 2vw, 1rem)\`  
\- Box-shadow: \`0 4px 24px rgba(115,66,226,0.28)\`  
\- Min-width: \`210px\`  
\- Flex with space-between, gap \`32px\`  
\- Text: "Get It Free" with ArrowRightCircle icon (20px) on the right  
\- Hover: \`scale(1.04)\` \+ \`brightness(1.1)\`  
\- Tap: \`scale(0.96)\`

\#\# Animations (Framer Motion)

\*\*fadeUp variant\*\* applied to heading (delay 0), subtext (delay 0.15s), and CTA button (delay 0.30s):

\`\`\`js  
hidden: { opacity: 0, y: 28 }  
visible: { opacity: 1, y: 0, transition: { delay: i \* 0.15, duration: 0.6, ease: \[0.22, 1, 0.36, 1\] } }  
\`\`\`

\#\# Dependencies

\- \`react\`, \`react-dom\`  
\- \`framer-motion\`  
\- \`lucide-react\` (icons: ArrowRightCircle, Zap, LockKeyhole, Fingerprint, Menu, X)  
\- Tailwind CSS

\---

That is every detail needed to reproduce the hero section exactly as built.

# Guia 25

Create an NFT landing page called "Orbis.Nft" with 4 sections, using a dark space theme. The page uses video backgrounds served from CloudFront, a liquid glass UI effect, and a specific color/font system. Recreate it exactly as described below.

FONTS (Google Fonts)

Anton \- Used for all headings and navigation text (aliased as font-grotesk in Tailwind)

Condiment \- A cursive script used for accent/overlay text (aliased as font-condiment in Tailwind)

System monospace font (font-mono) \- Used for body/description paragraphs

Load via Google Fonts in index.html:

https://fonts.googleapis.com/css2?family=Anton\&family=Condiment\&display=swap

COLOR SYSTEM (Tailwind config)

Background: \#010828 (deep dark navy blue)

cream: \#EFF4FF (off-white, used for all text)

neon: \#6FFF00 (bright green, used for accent cursive text and underline bars)

LIQUID GLASS CSS EFFECT

Applied via a .liquid-glass class. This is used on the navbar, social icon buttons, NFT cards, and card overlays:

.liquid-glass {  
  background: rgba(255, 255, 255, 0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}

TEXTURE OVERLAY

A full-screen fixed texture overlay sits on top of everything (z-50, pointer-events-none). It uses a /texture.png image with mix-blend-mode: lighten at opacity: 0.6, covering the entire viewport with background-size: cover.

SECTION 1: HERO (Full viewport)

Background: Full-bleed looping muted autoplaying video covering the entire section with object-cover

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_045634\_e1c98c76-1265-4f5c-882a-4276f2080894.mp4

Container: max-w-\[1831px\] centered with responsive horizontal padding

Section has rounded-b-\[32px\] bottom corners, clipping the video

Header:

Left: "Orbis.Nft" logo text in Anton, 16px, uppercase

Center: Navigation bar with liquid-glass effect, rounded-\[28px\], px-\[52px\] py-\[24px\]. Contains 5 links: Homepage, Gallery, Buy NFT, FAQ, Contact. Each link is Anton 13px uppercase. Links have hover:text-neon transition. Nav is hidden on mobile (hidden lg:block).

Hero Content:

Large heading in Anton font, responsive sizing: 40px mobile / 60px sm / 75px md / 90px lg. Uppercase. leading-\[1.05\] mobile, leading-\[1\] tablet+. Max width 780px on desktop, offset with lg:ml-32.

Text reads:

Beyond earth  
and ( its ) familiar boundaries

Overlaid cursive accent text "Nft collection" in Condiment font (24px-48px responsive), positioned absolute to the right side of the heading, slightly rotated (-rotate-1), in neon green (text-neon), with mix-blend-exclusion and opacity-90.

Social Icons (Desktop):

3 square buttons (56x56px) stacked vertically in top-right corner, each with liquid-glass and rounded-\[1rem\]. Icons: Mail, Twitter, Github from lucide-react (20x20px). hover:bg-white/10 transition.

Social Icons (Mobile):

Same 3 buttons but centered horizontally below the heading, shown only below lg breakpoint.

SECTION 2: ABOUT / INTRO (Full viewport)

Background: Full-bleed looping muted autoplaying video with object-cover

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_151551\_992053d1-3d3e-4b8c-abac-45f22158f411.mp4

Container: Same max-w-\[1831px\] centered, with generous vertical padding (64px-96px responsive)

Top Row (flex row on desktop, column on mobile):

Left: Heading in Anton, responsive 32px-60px, uppercase:

Hello\!  
I'm orbis

With an overlaid "Orbis" in Condiment cursive, neon green, mix-blend-exclusion, 36px-68px responsive, positioned absolute at bottom-right of heading, slightly rotated.

Right: Short paragraph in monospace 14px-16px, uppercase, cream color, max-width 266px: "A digital object fixed beyond time and place. An exploration of distance, form, and silence in space"

Bottom Row (flex row, space-between):

Two columns (left and right), each containing 2 identical paragraphs. Same monospace text as above but at opacity-10 (nearly invisible, decorative). Right column hidden below lg. On mobile, text uses text-\[\#010828\] (dark) so it's effectively invisible against the video.

SECTION 3: NFT COLLECTION GRID

Background: Solid \#010828 (no video)

Container: Same max-w-\[1831px\] centered

Header Row:

Left: Heading in Anton, 32px-60px responsive, uppercase:

Collection of  
  \[indented\] Space objects

Where "Space" is in Condiment cursive neon green, and "objects" is in Anton. The second line is indented with ml-12 / ml-24 / ml-32 responsive.

Right: A "SEE ALL CREATORS" button. "SEE" is large (32px-60px), "ALL" and "CREATORS" are stacked smaller (20px-36px) next to it. Below the text is a neon green bar (bg-neon, height 6px-10px responsive, full width of button).

NFT Card Grid:

3-column grid on desktop (lg:grid-cols-3), 2 on tablet, 1 on mobile. Gap 24px.

Each card: liquid-glass container with rounded-\[32px\], padding 18px, hover:bg-white/10 transition.

Inside each card: a square video container (pb-\[100%\] aspect ratio trick) with rounded-\[24px\] overflow hidden.

Video URLs:

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_053923\_22c0a6a5-313c-474c-85ff-3b50d25e944a.mp4 (Score: 8.7/10)

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_054411\_511c1b7a-fb2f-42ef-bf6c-32c0b1a06e79.mp4 (Score: 9/10)

https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_055427\_ac7035b5-9f3b-4289-86fc-941b2432317d.mp4 (Score: 8.2/10)

Each card has an overlay bar at the bottom: a liquid-glass bar with rounded-\[20px\], px-5 py-4, showing "RARITY SCORE:" label (11px, cream/70% opacity) and score value (16px). On the right side of the bar is a circular purple gradient button (48x48px, bg-gradient-to-br from-\[\#b724ff\] to-\[\#7c3aed\]) with a right-arrow chevron SVG inside, with shadow-lg shadow-purple-500/50 and hover:scale-110 transition.

SECTION 4: CTA / FINAL SECTION

Background: Full-width video (NOT object-cover, instead w-full h-auto block so it displays at native aspect ratio)

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260331\_055729\_72d66327-b59e-4ae9-bb70-de6ccb5ecdb0.mp4

Text Content (positioned absolute over the video):

Right-aligned block, offset with lg:pr-\[20%\] lg:pl-\[15%\]

Small "Go beyond" text in Condiment cursive, neon green, mix-blend-exclusion, positioned absolute at top-left of the heading block. Sizes: 17px-68px responsive.

Heading in Anton, responsive 16px-60px, uppercase:

JOIN US.  
REVEAL WHAT'S HIDDEN.  
DEFINE WHAT'S NEXT.  
FOLLOW THE SIGNAL.

"JOIN US." has extra bottom margin (mb-4 to mb-12 responsive) before the remaining lines.

Social Icons (Bottom-left, absolute positioned):

Positioned at left-\[8%\], bottom-\[12%\] to bottom-\[20%\] with responsive breakpoints.

A vertical liquid-glass container with rounded-\[0.5rem\] to rounded-\[1.25rem\] responsive, containing 3 stacked icon buttons (Mail, Twitter, Github).

Buttons have responsive widths using viewport units and rem values (e.g., w-\[14vw\] sm:w-\[14.375rem\] md:w-\[10.78125rem\] lg:w-\[16.77rem\]) and similar responsive heights.

Buttons are separated by border-b border-white/10 dividers (except the last one).

KEY TECHNICAL DETAILS

Framework: React \+ TypeScript \+ Vite \+ Tailwind CSS

Icons: lucide-react (Mail, Twitter, Github)

No additional packages needed beyond what Vite \+ React \+ Tailwind provides

All videos: autoPlay loop muted playsInline attributes

Responsive: Mobile-first with sm:, md:, lg: breakpoints throughout

Max content width: 1831px across all sections

All text is uppercase except the Condiment cursive accents which are normal-case

# Guia 26

Build a full-screen hero section for a data-security SaaS landing page called "securify" using React \+ TypeScript \+ Tailwind CSS, with a looping fullscreen background video, a floating pill-shaped navbar, and large staggered typography.

Fonts & Global Styles

Load Google font "Readex Pro" weights 300, 400, 500, 600, 700\.  
Set body font-family: 'Readex Pro', system-ui, \-apple-system, sans-serif;, background \#000, color \#fff, antialiased.  
Make html, body, \#root height 100%.  
Add a .hero-title class with letter-spacing: \-0.04em; line-height: 0.95;.  
Section container

A \<section\> with classes: relative h-screen w-full overflow-hidden bg-black.  
Background video

\<video\> with className="absolute inset-0 w-full h-full object-cover", autoPlay loop muted playsInline, and src="https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260418\_063509\_7d167302-4fd4-480b-8260-18ab572333d4.mp4".  
Navbar (absolute, z-20, px-6 md:px-10 pt-6, top-0 left-0 right-0)

A \<nav\> with flex items-center justify-between gap-4.  
Left pill: flex items-center gap-2 bg-neutral-900/90 backdrop-blur rounded-full pl-4 pr-6 py-3 containing:  
A custom white SVG logo (viewBox 0 0 256 256, class h-5 w-5) with path: M 128 192 L 128 256 L 64.5 256 L 32 223 L 0 192 L 0 128 L 64 128 Z M 256 192 L 256 256 L 192.5 256 L 160 223 L 128 192 L 128 128 L 192 128 Z M 128 64 L 128 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 Z M 256 64 L 256 128 L 192.5 128 L 160 95 L 128 64 L 128 0 L 192 0 Z filled \#ffffff.  
Brand text "securify" (text-white text-sm font-normal tracking-tight).  
Center pill (hidden on mobile): hidden md:flex items-center gap-1 bg-neutral-900/90 backdrop-blur rounded-full px-3 py-2 with four anchor links: "platform", "solutions", "company", "support" — each text-neutral-300 hover:text-white transition-colors text-sm px-5 py-2 rounded-full.  
Right button: "get started" — bg-white text-black text-sm font-normal rounded-full px-6 py-3 hover:bg-neutral-200 transition-colors.  
Foreground content wrapper: relative h-full w-full (rendered after Navbar, above the video).

Three giant staggered headline words (each an \<h1\> with class hero-title absolute text-white font-medium text-\[14vw\] md:text-\[13vw\]):

"protect" — left-4 md:left-10 top-\[18%\]  
"your" — right-4 md:right-10 top-\[38%\]  
"data" — left-\[18%\] md:left-\[28%\] top-\[58%\]  
All lowercase.

Description paragraph (absolute, left-6 md:left-10 top-\[46%\], max-w-\[240px\] text-\[15px\] leading-snug text-white/90):

"we can guarding your data with utmost care, empowering you with privacy everywhere"

Stat block — top-right (absolute right-6 md:right-24 top-\[14%\]):

Row: flex items-center gap-3 justify-end — a diagonal divider (hidden md:block h-px w-24 bg-white/40 rotate-\[20deg\]) then number "+65k" (text-4xl md:text-5xl font-medium tracking-tight).  
Sublabel: "startups use" (text-xs md:text-sm text-white/70 mt-1 text-right).  
Bottom gradient overlay: pointer-events-none absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-b from-transparent to-black.

Stat block — bottom-left (absolute left-6 md:left-20 bottom-20 md:bottom-24):

Row: number "+1.5b" then divider hidden md:block h-px w-24 bg-white/40 rotate-\[-20deg\].  
Sublabel: "gb data was protected" (text-xs md:text-sm text-white/70 mt-1).  
Stat block — bottom-right (absolute right-6 md:right-20 bottom-16 md:bottom-20):

Row: diagonal divider rotate-\[-20deg\] then "+300k".  
Sublabel: "downloads" (right-aligned, text-white/70).  
Notes

All text is lowercase.  
Navbar pills use bg-neutral-900/90 backdrop-blur.  
Only transitions: hover:text-white on nav links, hover:bg-neutral-200 on the button.  
No purple/indigo anywhere; palette is pure black, white, neutral-900, and white opacity variants (white/40, white/70, white/90).  
Responsive: mobile hides nav links and diagonal dividers; typography scales via vw units.

# Guia 27

\#\#\# Stack

\- \*\*Vite\*\* \+ \*\*React 18\*\* \+ \*\*TypeScript\*\*  
\- \*\*Tailwind CSS 3.4\*\*  
\- \*\*lucide-react\*\* for icons (\`LogIn\`, \`UserPlus\`, \`Play\`, \`Sparkles\`, \`Menu\`, \`X\`)  
\- No Framer Motion \-- all animations are CSS \`transition-\*\` classes

\---

\#\#\# Fonts (loaded in \`index.html\`)

\`\`\`html  
\<link rel="preconnect" href="https://fonts.googleapis.com" /\>  
\<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /\>  
\<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700\&display=swap" rel="stylesheet" /\>  
\<link href="https://db.onlinewebfonts.com/c/6e47ef470dd19698c911332a9b4d1cf4?family=Neue+Haas+Grotesk+Text+Pro" rel="stylesheet" /\>  
\<link href="https://db.onlinewebfonts.com/c/dec0d9b4e22ca588dc20e1e2e09a59b5?family=Neue+Haas+Grotesk+Display+Pro+55+Roman" rel="stylesheet" /\>  
\`\`\`

Body/root font stack (in \`index.css\`):

\`\`\`css  
html, body, \#root {  
  height: 100%;  
  margin: 0;  
  font-family: 'Neue Haas Grotesk Display Pro 55 Roman', 'Neue Haas Grotesk Text Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif;  
  \-webkit-font-smoothing: antialiased;  
}  
\`\`\`

\---

\#\#\# Video URL (CloudFront)

\`\`\`  
https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260511\_131941\_d136af49-e243-493a-be14-6ff3f24e09e6.mp4  
\`\`\`

\---

\#\#\# Color Palette

| Token | Hex |  
|-------|-----|  
| Dark green (text, buttons) | \`\#1f2a1d\` |  
| Medium dark green | \`\#2d3a2a\` |  
| Button hover | \`\#2a3827\` |  
| Body text green | \`\#4b5b47\` |  
| Heading primary | \`\#336443\` |  
| Heading accent | \`\#85AB8B\` |  
| Bottom-left text | \`\#3d5638\` |  
| Bottom-left button bg | \`\#3d5638\`, hover \`\#2d4228\` |

\---

\#\#\# Architecture

Two files:

1\. \*\*\`BoomerangVideoBg.tsx\`\*\* \-- captures video frames into canvas, then plays them forward/backward in a seamless boomerang loop at 30fps (960px max capture width).  
2\. \*\*\`App.tsx\`\*\* \-- the full hero section.

\---

\#\#\# \`BoomerangVideoBg.tsx\` (exact)

\`\`\`tsx  
import { useEffect, useRef, useState } from 'react';

type Props \= {  
  src: string;  
  className?: string;  
};

export default function BoomerangVideoBg({ src, className }: Props) {  
  const videoRef \= useRef\<HTMLVideoElement\>(null);  
  const displayCanvasRef \= useRef\<HTMLCanvasElement\>(null);  
  const \[framesReady, setFramesReady\] \= useState(false);  
  const framesRef \= useRef\<HTMLCanvasElement\[\]\>(\[\]);

  useEffect(() \=\> {  
    const video \= videoRef.current;  
    if (\!video) return;

    const frames: HTMLCanvasElement\[\] \= \[\];  
    let capturing \= true;  
    let lastTime \= \-1;  
    const MAX\_WIDTH \= 960;

    const captureFrame \= () \=\> {  
      if (\!capturing || video.readyState \< 2\) return;  
      if (video.currentTime \=== lastTime) return;  
      lastTime \= video.currentTime;

      const vw \= video.videoWidth;  
      const vh \= video.videoHeight;  
      if (\!vw || \!vh) return;

      const scale \= Math.min(1, MAX\_WIDTH / vw);  
      const w \= Math.round(vw \* scale);  
      const h \= Math.round(vh \* scale);

      const canvas \= document.createElement('canvas');  
      canvas.width \= w;  
      canvas.height \= h;  
      const ctx \= canvas.getContext('2d');  
      if (\!ctx) return;  
      ctx.drawImage(video, 0, 0, w, h);  
      frames.push(canvas);  
    };

    type VFCVideo \= HTMLVideoElement & {  
      requestVideoFrameCallback?: (cb: () \=\> void) \=\> number;  
    };  
    const vfcVideo \= video as VFCVideo;  
    const hasVFC \= typeof vfcVideo.requestVideoFrameCallback \=== 'function';

    let rafId \= 0;  
    const rafLoop \= () \=\> {  
      captureFrame();  
      if (capturing) rafId \= requestAnimationFrame(rafLoop);  
    };

    const vfcLoop \= () \=\> {  
      captureFrame();  
      if (capturing && vfcVideo.requestVideoFrameCallback) {  
        vfcVideo.requestVideoFrameCallback(vfcLoop);  
      }  
    };

    const onEnded \= () \=\> {  
      capturing \= false;  
      if (frames.length \> 0\) {  
        framesRef.current \= frames;  
        setFramesReady(true);  
      }  
    };

    const onLoaded \= () \=\> {  
      video.play().catch(() \=\> {});  
      if (hasVFC) {  
        vfcVideo.requestVideoFrameCallback\!(vfcLoop);  
      } else {  
        rafId \= requestAnimationFrame(rafLoop);  
      }  
    };

    video.addEventListener('loadedmetadata', onLoaded);  
    video.addEventListener('ended', onEnded);  
    if (video.readyState \>= 1\) onLoaded();

    return () \=\> {  
      capturing \= false;  
      cancelAnimationFrame(rafId);  
      video.removeEventListener('loadedmetadata', onLoaded);  
      video.removeEventListener('ended', onEnded);  
    };  
  }, \[src\]);

  useEffect(() \=\> {  
    if (\!framesReady) return;  
    const canvas \= displayCanvasRef.current;  
    if (\!canvas) return;  
    const ctx \= canvas.getContext('2d');  
    if (\!ctx) return;  
    const frames \= framesRef.current;  
    if (frames.length \=== 0\) return;

    const first \= frames\[0\];  
    canvas.width \= first.width;  
    canvas.height \= first.height;

    let index \= 0;  
    let direction \= 1;  
    let last \= performance.now();  
    const interval \= 1000 / 30;  
    let rafId \= 0;

    const render \= (now: number) \=\> {  
      if (now \- last \>= interval) {  
        last \= now;  
        ctx.drawImage(frames\[index\], 0, 0);  
        index \+= direction;  
        if (index \>= frames.length \- 1\) {  
          index \= frames.length \- 1;  
          direction \= \-1;  
        } else if (index \<= 0\) {  
          index \= 0;  
          direction \= 1;  
        }  
      }  
      rafId \= requestAnimationFrame(render);  
    };  
    rafId \= requestAnimationFrame(render);  
    return () \=\> cancelAnimationFrame(rafId);  
  }, \[framesReady\]);

  return (  
    \<div className={className ?? 'absolute inset-0 w-full h-full'}\>  
      \<video  
        ref={videoRef}  
        src={src}  
        className="w-full h-full object-cover"  
        style={{ display: framesReady ? 'none' : 'block' }}  
        muted  
        playsInline  
        preload="auto"  
        crossOrigin="anonymous"  
      /\>  
      \<canvas  
        ref={displayCanvasRef}  
        className="w-full h-full object-cover"  
        style={{ display: framesReady ? 'block' : 'none' }}  
      /\>  
    \</div\>  
  );  
}  
\`\`\`

\---

\#\#\# \`App.tsx\` (exact)

\`\`\`tsx  
import { useState, useEffect } from 'react';  
import { LogIn, UserPlus, Play, Sparkles, Menu, X } from 'lucide-react';  
import BoomerangVideoBg from './BoomerangVideoBg';

const BG\_VIDEO \=  
  'https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260511\_131941\_d136af49-e243-493a-be14-6ff3f24e09e6.mp4';

function App() {  
  const \[menuOpen, setMenuOpen\] \= useState(false);

  useEffect(() \=\> {  
    if (menuOpen) {  
      document.body.style.overflow \= 'hidden';  
    } else {  
      document.body.style.overflow \= '';  
    }  
    return () \=\> {  
      document.body.style.overflow \= '';  
    };  
  }, \[menuOpen\]);

  const navLinks \= \[  
    { href: '\#mission', label: 'Purpose' },  
    { href: '\#how', label: 'The Process' },  
    { href: '\#pricing', label: 'Tariffs' },  
  \];

  return (  
    \<section className="relative w-full min-h-screen sm:h-screen overflow-hidden"\>  
      \<BoomerangVideoBg src={BG\_VIDEO} className="absolute inset-0 w-full h-full" /\>  
      \<nav className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 sm:px-6 md:px-10 py-4 sm:py-6"\>  
        \<div className="flex items-center gap-2 text-\[\#2d3a2a\]"\>  
          \<span className="text-lg sm:text-xl md:text-2xl font-semibold tracking-tight"\>  
            LinkFlow\<sup className="text-\[10px\] sm:text-xs font-medium"\>TM\</sup\>  
          \</span\>  
        \</div\>

        \<div className="hidden lg:flex items-center gap-1 bg-white/70 backdrop-blur-md rounded-full pl-6 pr-1 py-1 shadow-sm border border-white/60"\>  
          {navLinks.map((link, i) \=\> (  
            \<a  
              key={link.href}  
              href={link.href}  
              className={\`text-sm px-3 py-2 transition-colors ${  
                i \=== 0 ? 'font-semibold text-\[\#1f2a1d\]' : 'font-medium text-\[\#4b5b47\] hover:text-\[\#1f2a1d\]'  
              }\`}  
            \>  
              {link.label}  
            \</a\>  
          ))}  
          \<button className="ml-2 bg-\[\#1f2a1d\] hover:bg-\[\#2a3827\] text-white text-sm font-medium px-5 py-2.5 rounded-full transition-colors"\>  
            Try it Live  
          \</button\>  
        \</div\>

        \<div className="flex items-center gap-3 sm:gap-6 text-\[\#2d3a2a\]"\>  
          \<a href="\#signup" className="hidden sm:flex items-center gap-2 text-sm font-medium hover:opacity-80 transition-opacity"\>  
            \<UserPlus className="w-4 h-4" /\>  
            Sign Me Up\!  
          \</a\>  
          \<a href="\#login" className="hidden sm:flex items-center gap-2 text-sm font-medium hover:opacity-80 transition-opacity"\>  
            \<LogIn className="w-4 h-4" /\>  
            Enter  
          \</a\>  
          \<button  
            onClick={() \=\> setMenuOpen((v) \=\> \!v)}  
            className="lg:hidden relative flex items-center justify-center w-10 h-10 rounded-full bg-white/70 backdrop-blur-md border border-white/60 text-\[\#1f2a1d\] transition-all duration-300 hover:bg-white/90"  
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}  
            aria-expanded={menuOpen}  
          \>  
            \<Menu  
              className={\`w-5 h-5 absolute transition-all duration-300 ${  
                menuOpen ? 'opacity-0 rotate-90 scale-50' : 'opacity-100 rotate-0 scale-100'  
              }\`}  
            /\>  
            \<X  
              className={\`w-5 h-5 absolute transition-all duration-300 ${  
                menuOpen ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 \-rotate-90 scale-50'  
              }\`}  
            /\>  
          \</button\>  
        \</div\>  
      \</nav\>

      {/\* Mobile menu overlay \*/}  
      \<div  
        className={\`lg:hidden fixed inset-0 z-20 transition-opacity duration-300 ${  
          menuOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'  
        }\`}  
        onClick={() \=\> setMenuOpen(false)}  
      \>  
        \<div className="absolute inset-0 bg-\[\#1f2a1d\]/40 backdrop-blur-sm" /\>  
      \</div\>

      {/\* Mobile menu drawer \*/}  
      \<div  
        className={\`lg:hidden fixed top-0 right-0 bottom-0 z-20 w-\[85%\] max-w-sm bg-white/95 backdrop-blur-xl shadow-2xl transition-transform duration-500 ease-\[cubic-bezier(0.22,1,0.36,1)\] ${  
          menuOpen ? 'translate-x-0' : 'translate-x-full'  
        }\`}  
      \>  
        \<div className="flex flex-col h-full pt-24 px-8 pb-8"\>  
          \<div className="flex flex-col gap-1"\>  
            {navLinks.map((link, i) \=\> (  
              \<a  
                key={link.href}  
                href={link.href}  
                onClick={() \=\> setMenuOpen(false)}  
                className={\`text-2xl font-semibold text-\[\#1f2a1d\] py-4 border-b border-\[\#1f2a1d\]/10 transition-all duration-500 ${  
                  menuOpen ? 'translate-x-0 opacity-100' : 'translate-x-8 opacity-0'  
                }\`}  
                style={{ transitionDelay: menuOpen ? \`${150 \+ i \* 70}ms\` : '0ms' }}  
              \>  
                {link.label}  
              \</a\>  
            ))}  
          \</div\>

          \<div  
            className={\`mt-8 flex flex-col gap-4 transition-all duration-500 ${  
              menuOpen ? 'translate-x-0 opacity-100' : 'translate-x-8 opacity-0'  
            }\`}  
            style={{ transitionDelay: menuOpen ? '400ms' : '0ms' }}  
          \>  
            \<a href="\#signup" className="flex items-center gap-2 text-sm font-medium text-\[\#2d3a2a\] sm:hidden"\>  
              \<UserPlus className="w-4 h-4" /\>  
              Sign Me Up\!  
            \</a\>  
            \<a href="\#login" className="flex items-center gap-2 text-sm font-medium text-\[\#2d3a2a\] sm:hidden"\>  
              \<LogIn className="w-4 h-4" /\>  
              Enter  
            \</a\>  
            \<button className="mt-2 bg-\[\#1f2a1d\] hover:bg-\[\#2a3827\] text-white text-sm font-semibold px-5 py-3 rounded-full transition-colors"\>  
              Try it Live  
            \</button\>  
          \</div\>  
        \</div\>  
      \</div\>

      {/\* Hero copy \*/}  
      \<div className="relative z-10 flex flex-col items-center text-center pt-24 sm:pt-28 md:pt-32 px-4 sm:px-6"\>  
        \<h1  
          className="font-normal leading-\[0.95\] text-\[\#336443\] text-\[2rem\] sm:text-4xl md:text-5xl lg:text-\[4.75rem\] xl:text-\[5.25rem\] max-w-5xl"  
          style={{ fontFamily: '"Neue Haas Grotesk Display Pro 55 Roman", "Neue Haas Grotesk Text Pro", "Helvetica Neue", Helvetica, Arial, sans-serif', letterSpacing: '-0.035em' }}  
        \>  
          Close the rift{' '}  
          \<span className="text-\[\#85AB8B\]"\>  
            linking  
            \<br className="hidden sm:block" /\> signals and action  
          \</span\>  
        \</h1\>  
        \<p className="mt-6 sm:mt-8 text-\[\#4b5b47\] text-sm sm:text-base md:text-lg leading-relaxed max-w-md px-2"\>  
          Shape scattered signals into meaningful outcomes via AI-driven workflows.  
        \</p\>  
      \</div\>

      {/\* Bottom-left CTA block \*/}  
      \<div className="absolute left-4 right-4 sm:right-auto sm:left-6 md:left-10 bottom-6 sm:bottom-8 md:bottom-10 z-10 max-w-sm"\>  
        \<div className="flex items-center gap-2 text-\[\#3d5638\] sm:text-white/95 mb-3"\>  
          \<Sparkles className="w-4 h-4" /\>  
          \<span className="text-sm font-semibold sm:font-medium"\>  
            FluxEngine\<sup className="text-\[10px\]"\>TM\</sup\>  
          \</span\>  
        \</div\>  
        \<p className="text-\[\#3d5638\]/90 sm:text-white/85 text-xs leading-relaxed mb-6 max-w-xs font-medium sm:font-normal"\>  
          LinkFlow smoothly unites your company systems, streamlining data paths between services without having to write custom scripts.  
        \</p\>  
        \<div className="flex items-center gap-4 flex-wrap"\>  
          \<button className="bg-\[\#3d5638\] sm:bg-white hover:bg-\[\#2d4228\] sm:hover:bg-white/90 text-white sm:text-\[\#1f2a1d\] text-sm font-semibold px-5 sm:px-6 py-2.5 sm:py-3 rounded-full transition-colors shadow-sm"\>  
            Try it Live  
          \</button\>  
          \<button className="text-\[\#3d5638\] sm:text-white text-sm font-semibold sm:font-medium hover:opacity-80 transition-opacity"\>  
            Know More.  
          \</button\>  
        \</div\>  
      \</div\>

      {/\* Bottom-right video link \*/}  
      \<div className="hidden sm:flex absolute right-6 md:right-10 bottom-8 md:bottom-10 z-10 items-center gap-2 text-white/90 text-sm"\>  
        \<button className="flex items-center justify-center w-6 h-6 rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/30 transition-colors"\>  
          \<Play className="w-3 h-3 fill-white text-white ml-0.5" /\>  
        \</button\>  
        \<span className="font-medium"\>How we build?\</span\>  
        \<span className="text-white/60"\>1:35\</span\>  
      \</div\>  
    \</section\>  
  );  
}

export default App;  
\`\`\`

\---

\#\#\# Animation Details (all CSS, no Framer Motion)

| Element | Property | Values |  
|---------|----------|--------|  
| Hamburger Menu/X icon swap | \`transition-all duration-300\` | Open: Menu gets \`opacity-0 rotate-90 scale-50\`, X gets \`opacity-100 rotate-0 scale-100\`. Closed: reverse. |  
| Mobile overlay backdrop | \`transition-opacity duration-300\` | Open: \`opacity-100 pointer-events-auto\`. Closed: \`opacity-0 pointer-events-none\`. |  
| Mobile drawer slide | \`transition-transform duration-500 ease-\[cubic-bezier(0.22,1,0.36,1)\]\` | Open: \`translate-x-0\`. Closed: \`translate-x-full\`. |  
| Mobile nav links stagger | \`transition-all duration-500\` | Open: \`translate-x-0 opacity-100\`, delay per item: \`150ms \+ i \* 70ms\`. Closed: \`translate-x-8 opacity-0\`, delay \`0ms\`. |  
| Mobile CTA group | \`transition-all duration-500\` | Open: \`translate-x-0 opacity-100\`, delay \`400ms\`. Closed: \`translate-x-8 opacity-0\`, delay \`0ms\`. |  
| Nav buttons | \`transition-colors\` | Default Tailwind duration (150ms). |  
| Opacity links | \`transition-opacity\` | \`hover:opacity-80\`. |

\---

\#\#\# Key Layout/Spacing Notes

\- Root section: \`relative w-full min-h-screen sm:h-screen overflow-hidden\`  
\- Navbar padding: \`px-4 sm:px-6 md:px-10 py-4 sm:py-6\`  
\- Desktop pill nav: \`bg-white/70 backdrop-blur-md rounded-full pl-6 pr-1 py-1 shadow-sm border border-white/60\`  
\- Hero heading: \`pt-24 sm:pt-28 md:pt-32\`, font sizes \`text-\[2rem\] sm:text-4xl md:text-5xl lg:text-\[4.75rem\] xl:text-\[5.25rem\]\`, \`leading-\[0.95\]\`, \`letterSpacing: '-0.035em'\`  
\- Bottom-left block: \`absolute left-4 right-4 sm:right-auto sm:left-6 md:left-10 bottom-6 sm:bottom-8 md:bottom-10\`  
\- Bottom-right video: \`absolute right-6 md:right-10 bottom-8 md:bottom-10\`

\---

\#\#\# Dependencies (package.json)

\`\`\`json  
{  
  "dependencies": {  
    "lucide-react": "^0.344.0",  
    "react": "^18.3.1",  
    "react-dom": "^18.3.1"  
  },  
  "devDependencies": {  
    "@vitejs/plugin-react": "^4.3.1",  
    "autoprefixer": "^10.4.18",  
    "postcss": "^8.4.35",  
    "tailwindcss": "^3.4.1",  
    "typescript": "^5.5.3",  
    "vite": "^5.4.2"  
  }  
}  
\`\`\`

# Guia 28

PROMPT:

Build a full-viewport cinematic movie/streaming hero section using React, Tailwind CSS, and Lucide React icons. Use the Inter font from Google Fonts. The entire page is a single full-height hero \-- no scrolling, no additional sections.

BACKGROUND VIDEO:

A full-screen background video plays on loop, muted, autoplaying, covering the entire viewport with object-cover. The video is fixed-positioned behind everything at z-index 0\.

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260406\_094145\_4a271a6c-3869-4f1c-8aa7-aeb0cb227994.mp4

BOTTOM BLUR OVERLAY (no gradient darkening):

Over the video, there is a single fixed, full-screen overlay div that applies a strong backdrop-blur-xl. This div uses a CSS mask so the blur only appears at the bottom and fades to transparent toward the middle of the screen. There is NO dark gradient overlay \-- only blur.

The mask: mask-image: linear-gradient(to top, black 0%, transparent 45%) (with the \-webkit- prefix too).

This overlay is pointer-events-none and sits at z-index 1\.

FONT:

Import Inter from Google Fonts (weights 300-700). Set font-family: 'Inter', sans-serif on the body.

LIQUID GLASS EFFECT (used on multiple buttons):

Create a reusable .liquid-glass CSS class with these exact properties:

background: rgba(255, 255, 255, 0.01) with background-blend-mode: luminosity  
backdrop-filter: blur(4px) (with \-webkit- prefix)  
border: none  
box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1)  
position: relative; overflow: hidden  
A ::before pseudo-element that creates a thin glowing border effect:  
position: absolute; inset: 0; border-radius: inherit; padding: 1.4px  
background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)  
Uses \-webkit-mask with linear-gradient(\#fff 0 0\) content-box and linear-gradient(\#fff 0 0\) combined with \-webkit-mask-composite: xor and mask-composite: exclude to create a border-only gradient stroke  
pointer-events: none  
BLUR-FADE-UP ANIMATION (used on every element with staggered delays):

Create a @keyframes blurFadeUp animation:

From: opacity: 0; filter: blur(20px); transform: translateY(40px)  
To: opacity: 1; filter: blur(0); transform: translateY(0)  
The .animate-blur-fade-up class applies this as animation: blurFadeUp 1s ease-out forwards with initial opacity: 0\. Each element on the page gets a staggered animationDelay via inline style.

NAVBAR (z-index 50, relative positioned):

A horizontal navbar with justify-between, padding px-4 sm:px-6 md:px-12 py-4 md:py-6.

Left: A text logo (e.g. your brand name like "CINEMATIC" or similar) styled as h-8 md:h-10, with blur-fade-up animation at delay 0ms.

Center (desktop only, hidden below lg): Navigation links \-- "Movies", "TV Series", "Editor's Pick", "Interviews", "User Reviews" \-- each as an anchor with text-sm, hover:text-gray-300 transition-colors, and staggered blur-fade-up delays from 100ms to 300ms (50ms increments).

Right: Two buttons visible on sm and up:

A "Search" button \-- rounded-full liquid-glass pill with the text "Search" and a Lucide Search icon (size 18), padding px-4 md:px-6 py-2, blur-fade-up at 350ms.  
A user/profile circle button \-- w-10 h-10 rounded-full liquid-glass with a Lucide User icon (size 18), blur-fade-up at 400ms.  
A hamburger menu button visible only below lg \-- w-10 h-10 rounded-full liquid-glass with animated icon transition between Lucide Menu and X icons. The transition uses rotate-180, opacity, and scale-50 with duration-500 ease-out. Blur-fade-up at 350ms.  
MOBILE MENU (below lg breakpoint):

An absolutely positioned dropdown below the navbar (top-\[72px\]), z-index 40\. It slides in with translate-y-0 opacity-100 when open, \-translate-y-4 opacity-0 pointer-events-none when closed, duration-500 ease-out.

Background: bg-gray-900/95 backdrop-blur-lg with border-t border-b border-gray-800 shadow-2xl.  
Contains the same 5 nav links, each in a column with py-3 px-3 rounded-lg, hover:bg-gray-800/50, and staggered slide-in animations (translate-x based, 50ms delay increments).  
Below sm, also shows Search and Profile buttons in a bordered section at the bottom.  
HERO CONTENT (bottom of viewport):

A flex container that grows to fill remaining space and aligns content to the bottom (flex-1 flex flex-col justify-end), with padding px-4 sm:px-6 md:px-12 pb-8 md:pb-16, z-index 10\.

Inside, a flex-col md:flex-row items-end gap-8 layout:

Left side (flex-1):

Metadata row \-- a horizontal flex-wrap row with gap-3 sm:gap-6 mb-6 md:mb-8 text-xs sm:text-sm, blur-fade-up at 300ms:

Star icon (size 16, fill-white, responsive to sm:w-5 sm:h-5) \+ "8.7/10 IMDB" (font-medium)  
Clock icon (size 16\) \+ "132 min"  
Calendar icon (size 16\) \+ "April, 2025"  
Title \-- text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-normal, letter-spacing \-0.04em, mb-4 md:mb-6, blur-fade-up at 400ms. Text: "Step Through. Work Smarter."

Description \-- text-base sm:text-lg md:text-xl text-gray-400 mb-6 md:mb-12 max-w-2xl, blur-fade-up at 500ms. Text: "A voyage through forgotten realms, where past and future intertwine."

CTA buttons \-- flex-wrap row with gap-3 sm:gap-4:

"Watch Now" \-- bg-white text-black rounded-full font-medium, px-6 sm:px-8 py-2.5 sm:py-3, with a Lucide Play icon (size 18, fill-black), hover:bg-gray-200, blur-fade-up at 600ms.  
"Learn More" \-- rounded-full font-medium liquid-glass, same padding, blur-fade-up at 700ms.  
Right side (navigation arrows):

A row of two pill buttons (md:w-auto, aligned right on desktop, left on mobile):

"Previous" button \-- rounded-full liquid-glass, px-4 sm:px-6 py-2.5 sm:py-3, with Lucide ChevronLeft icon, blur-fade-up at 800ms.  
"Next" button \-- same styling with Lucide ChevronRight icon, blur-fade-up at 900ms.  
COLOR PALETTE:

Background: pure black (bg-black)  
Text: white, with text-gray-400 for the subtitle  
All interactive glass elements use the .liquid-glass class (nearly transparent white with blur)  
The only solid-colored element is the "Watch Now" button (white background, black text)  
STAGGER TIMING SUMMARY:

Logo: 0ms  
Nav links: 100ms, 150ms, 200ms, 250ms, 300ms  
Search button: 350ms  
User button: 400ms  
Metadata row: 300ms  
Title: 400ms  
Description: 500ms  
Watch Now: 600ms  
Learn More: 700ms  
Previous: 800ms  
Next: 900ms  
RESPONSIVE BREAKPOINTS:

Below sm (\< 640px): Smaller text, tighter padding, Search/User buttons hidden (available in mobile menu)  
Below lg (\< 1024px): Nav links hidden, hamburger menu shown  
md and up: Side-by-side layout for hero content and navigation arrows  
lg and up: Full desktop navbar with all links visible

# Guia 29

Project Setup

Stack: React 19 \+ Vite 6 \+ Tailwind CSS 4 \+ Motion (Framer Motion) \+ Lucide React icons \+ TypeScript

package.json dependencies:  
\- \`react\`, \`react-dom\` ^19.0.1  
\- \`vite\` ^6.2.3  
\- \`@tailwindcss/vite\` ^4.1.14, \`tailwindcss\` ^4.1.14  
\- \`motion\` ^12.23.24  
\- \`lucide-react\` ^0.546.0  
\- \`@vitejs/plugin-react\` ^5.0.4  
\- \`typescript\` \~5.8.2

Fonts (loaded via Google Fonts in \`index.css\`):  
\- Sans: Inter (weights: 300, 400, 500, 600\)  
\- Mono: JetBrains Mono (weights: 400, 500\)

\`\`\`css  
/\* index.css \*/  
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600\&family=JetBrains+Mono:wght@400;500\&display=swap');  
@import "tailwindcss";

@theme {  
  \--font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;  
  \--font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, monospace;  
}

@layer utilities {  
  .text-mega {  
    font-size: 21vw;  
    line-height: 0.75;  
    letter-spacing: \-0.04em;  
  }  
}  
\`\`\`

Global styling: Background \`\#fcfcfc\`, text \`\#111\`, selection color \`bg-black text-white\`, \`overflow-x-hidden\`, \`font-sans\` (Inter).

\---

DATA

\`\`\`tsx  
const chaptersData \= \[  
  { name: "Age of Dinosaurs", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624247/01\_udnber.png" },  
  { name: "Fossils of Ancient Life", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624374/02\_pmvxxl.png" },  
  { name: "Reptiles of the Mesozoic", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624236/03\_hcp3jc.png" },  
  { name: "Marine Fossil Gallery", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624256/04\_get63z.png" },  
  { name: "Prehistoric Giants", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624251/05\_kz1tyu.png" }  
\];  
\`\`\`

\---

STATE

\`\`\`tsx  
const \[showVideo, setShowVideo\] \= useState(false);  
const \[activeChapter, setActiveChapter\] \= useState(2); // starts at "Reptiles of the Mesozoic"  
const \[isMobileMenuOpen, setIsMobileMenuOpen\] \= useState(false);  
\`\`\`

\- \`showVideo\` flips to \`true\` after a 2800ms delay (setTimeout)  
\- \`activeChapter\` auto-cycles every 3500ms via setInterval, wrapping \`(prev \+ 1\) % 5\`

\---

ANIMATION VARIANTS

\`\`\`tsx  
const fadeUp \= {  
  initial: { opacity: 0, y: 20 },  
  animate: { opacity: 1, y: 0 },  
};

const letterBlock \= {  
  initial: { y: 120, opacity: 0 },  
  animate: {   
    y: 0,   
    opacity: 1,   
    transition: { duration: 1.2, ease: \[0.16, 1, 0.3, 1\] }   
  }  
};  
\`\`\`

\---

SECTION 1: HERO (full viewport height)

Container: \`relative w-full min-h-screen flex flex-col overflow-hidden\`

1A. HEADER (NHM Logo)

\- \`motion.header\` with \`staggerChildren: 0.1, delayChildren: 0.1\`  
\- Padding: \`pt-6 px-6 md:px-16\`, \`z-20\`  
\- The "NHM" logo is a custom inline SVG with \`viewBox="0 0 840 100"\`, \`fill-\[\#111\]\`, full width  
\- The SVG is wrapped in \`motion.h1\` with \`variants\` that animate from \`scale: 1.03\` to \`scale: 1\` with \`staggerChildren: 0.06, delayChildren: 0.1\`  
\- Each polygon of each letter uses the \`letterBlock\` variant (slides up from \`y: 120\`)  
\- Letter N (translate 0,0): Three polygons \-- left vertical \`0,0 14,0 14,100 0,100\`, right vertical \`200,0 214,0 214,100 200,100\`, diagonal \`0,0 33,0 214,100 181,100\`  
\- Letter H (translate 280,0): Three polygons \-- left vertical \`0,0 14,0 14,100 0,100\`, right vertical \`200,0 214,0 214,100 200,100\`, crossbar \`14,43 200,43 200,57 14,57\`  
\- Letter M (translate 560,0): Four polygons \-- left vertical \`0,0 14,0 14,100 0,100\`, right vertical \`266,0 280,0 280,100 266,100\`, left diagonal \`0,0 26,0 153,100 127,100\`, right diagonal \`254,0 280,0 153,100 127,100\`

1B. SUB-NAV BAR

\- Below the SVG logo, \`flex justify-between items-start mt-8\`  
\- Font: \`text-\[10px\] md:text-\[11px\] font-mono tracking-\[0.2em\] uppercase\`  
\- Uses \`fadeUp\` variant with \`duration: 0.8, ease: "easeOut"\`

Left column (15% width): Three lines \-- "Natura" / "History" / "Museum"

Arrow separator (5% width, hidden on mobile): \`ArrowRight\` from lucide, size 14, strokeWidth 1, \`text-gray-400\`

Center column (flex-1 on mobile, 30% on desktop): "Exploring the story of life on earth through science, discovery and wonder." \-- Split differently on desktop (3 lines) vs mobile (4 lines). \`text-gray-800 leading-relaxed font-mono\`

Arrow separator (5% width, hidden on mobile): Same as above

Right column (15% width, hidden on mobile): Nav links list \-- Visit, Exhibitions, Discover, Learn, About. \`text-gray-800\`, \`hover:text-black hover:underline\`

Hamburger button (far right, z-60): Two horizontal lines (\`w-8 h-\[1.5px\] bg-black\`), \`gap-\[6px\]\`. Hover: first line shrinks to \`w-6\`, second expands to \`w-10\`. When open: first rotates 45deg \+ translateY, second rotates \-45deg \+ translateY (forming an X). Transition: \`duration-300\`.

1C. MOBILE MENU OVERLAY

\- \`AnimatePresence\` wrapping a \`motion.div\`  
\- Appears below the header, slides in from \`y: \-20\`, \`opacity: 0\` to \`y: 0, opacity: 1\`  
\- \`bg-\[\#fcfcfc\] border-b border-gray-200 shadow-xl\`, only visible on \`md:hidden\`  
\- Contains the same nav links as the desktop version, \`text-sm font-mono tracking-\[0.2em\] uppercase\`, \`space-y-6\`

1D. BACKGROUND VIDEO

\- Appears after 2800ms delay (controlled by \`showVideo\` state)  
\- \`absolute top-0 left-0 w-full h-full pointer-events-none z-0\`  
\- Video: \`autoPlay loop muted playsInline\`, \`w-full h-full object-cover\`  
\- Video URL: \`https://res.cloudinary.com/dsdxaxkiz/video/upload/v1779624998/magnific\_use-img-2-as-the-exact-ba\_Piu3X0W42C\_wnrc8f.mp4\`

1E. LEFT SIDEBAR CONTENT

\- \`motion.div\` with \`staggerChildren: 0.15, delayChildren: 0.6\`  
\- Position: \`px-10 md:px-16\`, \`mt-20 sm:mt-28 md:mt-32\`, \`w-\[320px\]\`, \`z-10\`

Section indicator: \`01\` \+ horizontal line (\`w-16 h-\[1.5px\] bg-black/20\`), \`text-xs font-mono\`

Headline: "TIMELESS WONDERS" \-- \`text-\[3.5rem\] md:text-\[5rem\] font-normal tracking-tight leading-\[1\]\`. Line break between "TIMELESS" and "WONDERS".

Description: "Step into the natural world and / discover the stories written / millions of years ago." \-- \`text-\[13px\] md:text-\[14px\] text-gray-700 w-\[240px\] leading-\[1.6\]\`

CTA Button ("Explore Now"):  
\- Container: \`bg-\[\#1a1a1a\] px-6 py-3.5 border border-\[\#1a1a1a\] rounded-md shadow-sm\`  
\- Hover: slides up 0.5px, adds \`shadow-\[3px\_3px\_0px\_rgba(17,17,17,0.5)\]\`  
\- Active: resets translate and shadow  
\- Has a sliding background panel: \`bg-\[\#fcfcfc\]\` that slides from \`-translate-x-\[101%\]\` to \`translate-x-0\` on hover, \`duration-700 ease-\[cubic-bezier(0.16,1,0.3,1)\]\`  
\- Icon: Custom SVG leaf/plant shape (4 paths forming a stylized leaf), white by default, turns \`\#111\` on hover with \`scale-110 \-rotate-12 \-translate-y-1\` transform  
\- Text: "Explore Now", \`text-\[15px\] font-medium\`, white turning to \`\#111\` on hover

1F. RIGHT SIDEBAR (hidden on mobile)

\- \`motion.div\` with \`staggerChildren: 0.15, delayChildren: 0.9\`  
\- Position: \`w-\[200px\] mt-12 md:mt-20\`, \`hidden md:flex\`

Specimen info: "Tyrannosaurus Rex" heading (\`text-\[10px\] font-bold font-mono tracking-widest uppercase\`), subtext "Late Cretaceous period / 68-66 million years ago" (\`text-\[12px\] text-gray-600 leading-\[1.6\]\`)

Stats: "Length" label \+ "12.3 m" value, "Height" label \+ "4.0 m" value. Labels: \`text-\[10px\] font-mono tracking-widest uppercase text-gray-500\`. Values: \`text-\[13px\] font-medium\`.

View Details button: Circle (\`w-10 h-10 rounded-full border border-gray-400\`) with \`Plus\` icon (size 16, strokeWidth 1.5), text "View Details" (\`text-\[10px\] font-mono uppercase tracking-widest font-bold\`). Hover: circle gets \`border-black bg-\[\#111\]\`, icon turns white.

1G. BOTTOM-LEFT "SCROLL TO EXPLORE"

\- \`absolute bottom-10 left-\[2.5rem\] md:left-\[4rem\]\`, \`hidden md:flex\`  
\- Fade up animation: \`delay: 1.2\`  
\- Circle (\`w-12 h-12 rounded-full border border-gray-300\`) containing two thin vertical lines (\`w-\[1px\] h-\[12px\] bg-gray-600\`, \`gap-\[4px\]\`) representing a pause icon  
\- Text: "Scroll to explore" \-- \`text-\[10px\] font-mono tracking-widest uppercase text-gray-500 font-semibold\`

\---

SECTION 2: "EXPLORE OUR WORLD"

Container: \`relative w-full min-h-\[75vh\] md:min-h-screen bg-\[\#fcfcfc\]\`, flex column centered, \`pt-24 md:pt-32 pb-0 z-20\`

2A. SECTION LABEL

\`\[ 02 \] Explore Our World\` \-- \`text-\[10px\] md:text-\[11px\] font-mono tracking-\[0.2em\]\`, \`mb-12\`. "02" in \`text-gray-500\`, "Explore Our World" in \`text-gray-900 font-bold uppercase\`.

2B. MAIN HEADING

"Unearth the stories of our planet's past through fossils, minerals, and ancient wonders." \-- \`text-\[2.2rem\] md:text-\[3.5rem\] lg:text-\[4.2rem\] leading-\[1.1\] font-medium tracking-tight text-\[\#111\]\`, max-width 1000px, text-center. Line break on desktop after "past". Animates with \`whileInView\` from \`y: 40, opacity: 0\` to \`y: 0, opacity: 1\`, \`once: true\`, margin \`-100px\`.

2C. ACTION PILLS

Five pill buttons in a flex-wrap row, \`gap-3 md:gap-4\`, \`mb-10 md:mb-24\`. Staggered reveal animation (\`staggerChildren: 0.1, delayChildren: 0.3\`). Each pill: \`rounded-full border border-gray-300 text-\[11px\] font-medium uppercase tracking-wider bg-white/50 backdrop-blur-sm text-gray-800\`. Hover: \`border-black bg-black text-white\`. Icons from lucide (size 14, strokeWidth 2):

1\. \`Bone\` \+ "Dinosaurs"  
2\. \`Dna\` \+ "Ancient Life"  
3\. \`Gem\` \+ "Minerals"  
4\. \`Leaf\` \+ "Fossils"  
5\. \`BookOpen\` \+ "Learn More"

2D. SPACER

\`min-h-\[220px\] md:min-h-\[450px\]\` \-- provides room for the pterodactyl image from Section 3 to overlap upward.

2E. BOTTOM TEXT

Absolute positioned at bottom, \`px-8 md:px-16 pb-8 md:pb-12\`, \`pointer-events-none\`. Two text elements at \`justify-between\`:  
\- Left: "WE DON'T JUST TELL STORIES."  
\- Right: "PALEONTOLOGY (C) 2026"  
\- Both: \`text-\[10px\] font-mono tracking-widest uppercase text-gray-500 font-medium\`, hidden on mobile.

\---

SECTION 3: "ANCIENT COLLECTION" (Dark Section)

Container: \`relative w-full bg-\[\#0a0a0a\] text-white flex flex-col z-30\`

3A. PTERODACTYL IMAGE (Overlapping)

\- Absolute positioned at top, centered horizontally (\`left-1/2 \-translate-x-1/2\`)  
\- Width: \`w-\[160vw\] md:w-\[1100px\]\`  
\- Image URL: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779625001/ChatGPT\_Image\_May\_23\_2026\_12\_24\_44\_PM\_1\_lv1dne.png\`  
\- Animates with \`whileInView\` from \`y: "-65%", opacity: 0\` to \`y: "-78%", opacity: 1\`, \`duration: 1.4, ease: "easeOut"\`, viewport margin \`100px\`  
\- \`pointer-events-none z-0\`, \`mix-blend\` not applied here

3B. HEADING AREA

\- Padding: \`px-8 md:px-16 pt-32 md:pt-48 mb-16\`, \`z-10\`  
\- Two-column layout on xl (\`flex-col xl:flex-row justify-between\`)

Left \-- Main heading: "Curated from millions of years of wonder \[3 circle icons\] & discovery." \-- \`text-\[1.8rem\] md:text-\[3rem\] lg:text-\[3.8rem\] xl:text-\[4rem\] leading-\[1.15\] font-medium tracking-tight text-white\`. The three circle icons are inline (\`inline-flex gap-2 md:gap-3 align-middle mx-2 md:mx-4 translate-y-\[-4px\]\`), each \`w-10 h-10 md:w-14 md:h-14 rounded-full border border-gray-600 bg-black text-gray-400\`. Hover: \`bg-white text-black border-white\`. Icons: \`Bone\`, \`Dna\`, \`Leaf\` (size 22).

Right \-- Tagline \+ pills:  
\- Tagline: "WE DON'T JUST DISPLAY FOSSILS / WE SHARE EARTH'S STORY" \-- \`text-\[9px\] md:text-\[10px\] font-mono tracking-widest text-gray-400 uppercase mb-6 leading-relaxed\`  
\- Three pills: "Educational", "Authentic", "Inspiring" \-- \`px-5 py-2 rounded-full border border-gray-600 text-\[9px\] font-mono tracking-widest uppercase text-gray-300\`. Hover: \`bg-white text-black border-white\`.

3C. TWO-COLUMN PANEL

Separated by \`h-\[1px\] bg-gray-800\` line. Flex row on desktop, column on mobile.

Left panel (35% width):  
\- \`border-r border-gray-800\` on desktop, \`border-b\` on mobile  
\- \`min-h-\[400px\] md:min-h-\[500px\]\`  
\- Top: \`\*\*\*\` text (\`text-gray-500 text-xl tracking-\[0.3em\]\`)  
\- Center: Chapter image using \`SandTransitionImage\` component (SVG filter-based sand/dissolve transition). Image: \`absolute inset-0 w-\[80%\] h-\[80%\] m-auto object-contain mix-blend-lighten\`. Uses \`AnimatePresence mode="wait"\`.  
\- Bottom: Chapter counter \`01 / 05\` style, with animated number (\`motion.div\` slides vertically). \`text-\[10px\] font-mono tracking-widest text-\[\#888\] uppercase\`. Counter numeral color \`\#888\`, divider \`text-\[\#333\]\`.

Right panel (65% width):  
\- Top bar: "Explore the past. Understand the present." \+ animated "Chapter 0X" label. \`border-b border-gray-800 p-8 text-\[10px\] font-mono text-gray-400 tracking-widest\`.  
\- Chapter list: 5 items, each \`border-b border-gray-800/80 py-8\`. Active: \`text-white\`, inactive: \`text-\[\#444\] hover:text-\[\#999\]\`. Chapter name: \`text-2xl md:text-\[2rem\] font-medium tracking-tight\`. Active item shows \`ArrowUpRight\` icon (size 22, strokeWidth 1, \`text-gray-400\`) that animates in/out.  
\- Clicking a chapter sets \`activeChapter\`.

3D. BOTTOM FOOTER

\- \`h-\[1px\] bg-gray-800\` divider  
\- Text: "DIGGING INTO OUR PLANET'S PAST" \-- \`px-8 py-8 text-\[10px\] font-mono tracking-widest text-gray-500 uppercase bg-\[\#0a0a0a\]\`

\---

SandTransitionImage COMPONENT

A custom component that creates a sand/particle dissolve effect using SVG filters:

\`\`\`tsx  
function SandTransitionImage({ src, alt, className }) {  
  // Uses usePresence() from motion/react for AnimatePresence awareness  
  // Unique filterId per instance via useRef  
  // requestAnimationFrame loop over 900ms  
  // Easing: entering \= quartic ease-out (1 \- Math.pow(1-t, 4)), exiting \= cubic (Math.pow(t, 3))  
  // SVG filter chain:  
  //   1\. feTurbulence: fractalNoise, baseFrequency 1.8, numOctaves 4  
  //   2\. feDisplacementMap: scale up to 150 based on progress  
  //   3\. feOffset: dy up to \-80 (enter) or 120 (exit), dx up to \-30/+30  
  //   4\. feGaussianBlur: up to 6px  
  //   5\. feColorMatrix: opacity fades (1 \- progress \* 1.2)  
  // Image has crossOrigin="anonymous" and referrerPolicy="no-referrer"  
}  
\`\`\`

\---

ALL EXTERNAL ASSET URLs

Video:  
\- \`https://res.cloudinary.com/dsdxaxkiz/video/upload/v1779624998/magnific\_use-img-2-as-the-exact-ba\_Piu3X0W42C\_wnrc8f.mp4\`

Images:  
\- Chapter 1: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624247/01\_udnber.png\`  
\- Chapter 2: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624374/02\_pmvxxl.png\`  
\- Chapter 3: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624236/03\_hcp3jc.png\`  
\- Chapter 4: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624256/04\_get63z.png\`  
\- Chapter 5: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624251/05\_kz1tyu.png\`  
\- Pterodactyl: \`https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779625001/ChatGPT\_Image\_May\_23\_2026\_12\_24\_44\_PM\_1\_lv1dne.png\`

(Note: these are Cloudinary URLs, not CloudFront. The project uses Cloudinary for all hosted media assets.)

\---

KEY DESIGN DETAILS

\- Color palette: \`\#fcfcfc\` (off-white bg), \`\#111\` / \`\#1a1a1a\` (near-black), \`\#0a0a0a\` (dark section bg). Gray scale via Tailwind: \`gray-300\` through \`gray-800\`.  
\- No purple/indigo anywhere. Strictly monochrome black/white/gray.  
\- Typography hierarchy: Large display headings (3.5-5rem), mono labels (10-11px), body text (13-14px).  
\- Spacing: 8px base system throughout.  
\- Transitions: Most hover transitions 300-700ms. Button slide effect uses \`cubic-bezier(0.16, 1, 0.3, 1)\`. Letter animations use same cubic bezier.  
\- The page is entirely a single \`App.tsx\` component plus the \`SandTransitionImage\` helper function in the same file.

# Guia 30

\*\*Build a fullscreen hero section in a Vite \+ React \+ TypeScript \+ Tailwind CSS project. Use \`gsap\` and \`lucide-react\`. No other UI libraries.\*\*

\#\#\# Fonts (in \`src/index.css\`)  
Import at the top of index.css BEFORE \`  
@tailwind  
\` directives:  
\`\`\`css  
@import  
 url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1\&family=Barlow:wght@300;400;500;600\&display=swap');

@font  
\-face {  
  font-family: 'Dirtyline';  
  src: url('https://fonts.cdnfonts.com/s/15011/Dirtyline36DaysofType.woff') format('woff');  
  font-weight: normal;  
  font-style: normal;  
  font-display: swap;  
}  
\`\`\`  
Body font: \`'Barlow', sans-serif\`, background \`\#000\`.

\#\#\# Tailwind config (\`tailwind.config.js\`)  
\`\`\`js  
theme: {  
  extend: {  
    fontFamily: {  
      heading: \['Instrument Serif', 'serif'\],  
      body: \['Barlow', 'sans-serif'\],  
      dirtyline: \['Dirtyline', 'sans-serif'\],  
    },  
    borderRadius: { DEFAULT: '9999px' },  
  },  
},  
\`\`\`

\#\#\# CSS (append to \`src/index.css\`)  
\`\`\`css  
.liquid-glass {  
  background: rgba(255,255,255,0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: "";  
  position: absolute; inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%,  
    rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0)    40%,  
    rgba(255,255,255,0)    60%,  
    rgba(255,255,255,0.15) 80%,  
    rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}

.liquid-glass-strong {  
  background: rgba(255,255,255,0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(50px);  
  \-webkit-backdrop-filter: blur(50px);  
  border: none;  
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass-strong::before {  
  content: "";  
  position: absolute; inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.5) 0%,  
    rgba(255,255,255,0.2) 20%,  
    rgba(255,255,255,0)   40%,  
    rgba(255,255,255,0)   60%,  
    rgba(255,255,255,0.2) 80%,  
    rgba(255,255,255,0.5) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}

.hero-title {  
  font-family: 'Instrument Serif', serif;  
  font-style: italic;  
  font-size: clamp(96px, 18vw, 280px);  
  line-height: 0.92;  
  letter-spacing: \-0.02em;  
  color: white;  
  text-align: center;  
}  
\`\`\`

\#\#\# Component (\`src/App.tsx\`)

\*\*Constants:\*\*  
\- \`NAV\_LINKS \= \['Gallery', 'Styles', 'API', 'Pricing', 'Blog'\]\`  
\- \`VIDEO\_SRC \= 'https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260511\_080827\_a9e5ad52-b6ee-4e79-b393-d936f179cfd7.mp4'\`

\*\*LogoMark\*\* — inline SVG, 44x26, viewBox \`0 0 44 26\`, three white rects at x=0/16/30, y=3, widths 14/12/14, height 20, rx=3.

\*\*State/refs:\*\*  
\- \`mounted\` (boolean, set true in a mount effect for fade-in).  
\- \`videoRef\` (HTMLVideoElement), \`videoBgRef\` (HTMLDivElement), \`displayCanvasRef\` (HTMLCanvasElement).  
\- \`framesReady\` boolean state, \`framesRef\` \= \`useRef\<HTMLCanvasElement\[\]\>(\[\])\`.

\*\*Effect 1 — Frame capture (boomerang setup):\*\*  
\- On mount, get \`videoRef.current\`. Set \`capturing \= true\`, \`lastTime \= \-1\`, \`MAX\_WIDTH \= 960\`, \`frames: HTMLCanvasElement\[\] \= \[\]\`.  
\- \`captureFrame()\`: bail if \`\!capturing\` or \`readyState \< 2\` or \`currentTime \=== lastTime\`. Update \`lastTime\`. Scale \= \`min(1, 960/videoWidth)\`. Create offscreen canvas at scaled w/h, \`ctx.drawImage(video, 0, 0, w, h)\`, push to frames.  
\- Use \`requestVideoFrameCallback\` when available, else \`requestAnimationFrame\` fallback.  
\- On \`loadedmetadata\`: call \`http://video.play().catch(()=\>{})\` then start the capture loop.  
\- On \`ended\`: set \`capturing \= false\`, store frames in \`framesRef.current\`, \`setFramesReady(true)\`.  
\- If \`readyState \>= 1\`, invoke \`onLoaded()\` immediately.  
\- Cleanup: cancel raf \+ remove listeners.

\*\*Effect 2 — Boomerang render:\*\*  
\- When \`framesReady\` true, grab \`displayCanvasRef\`, set its \`width/height\` from \`frames\[0\]\`.  
\- Variables: \`index \= 0\`, \`direction \= 1\`, \`last \= http://performance.now()\`, \`interval \= 1000/30\`.  
\- In an \`requestAnimationFrame(render)\` loop: if \`now \- last \>= interval\`, draw \`frames\[index\]\`, advance \`index \+= direction\`. When \`index \>= frames.length \- 1\`, clamp and flip to \`-1\`. When \`index \<= 0\`, clamp and flip to \`+1\`.  
\- Cleanup: cancelAnimationFrame.

\*\*Effect 3 — Parallax mouse tracking (gsap):\*\*  
\- \`strength \= 20\`. Track \`targetX/Y\`, smoothly lerp \`currentX/Y \+= (target \- current) \* 0.06\` each frame.  
\- On \`mousemove\`: \`targetX \= ((clientX \- cx)/cx) \* strength\` (same for Y).  
\- Each frame: \`gsap.set(videoBgRef.current, { x: currentX, y: currentY })\`.

\*\*JSX structure:\*\*  
Root: \`\<div className="min-h-screen bg-black text-white font-body overflow-x-hidden"\>\`

1\. \*\*Video background layer:\*\* \`\<div ref={videoBgRef} className="fixed top-0 left-0 w-full h-full z-0 scale-\[1.08\] origin-center"\>\` containing:  
   \- \`\<video\>\` with \`src={VIDEO\_SRC}\`, \`muted\`, \`playsInline\`, \`preload="auto"\`, \`crossOrigin="anonymous"\`, \`className="w-full h-full object-cover"\`, \`style={{ display: framesReady ? 'none' : 'block' }}\`.  
   \- \`\<canvas ref={displayCanvasRef} className="w-full h-full object-cover" style={{ display: framesReady ? 'block' : 'none' }}\>\`.

2\. \*\*Hero title:\*\* fixed div, \`left-0 right-0 z-20 w-full px-4\`, \`style={{ top: '126px' }}\`, fades in via \`transition-all duration-1000\` toggling \`opacity-100 translate-y-0\` vs \`opacity-0 translate-y-6\` based on \`mounted\`. Inside: \`\<h1 className="hero-title select-none"\>MicroVisuals\</h1\>\`.

3\. \*\*Nav:\*\* \`\<nav className="fixed top-5 left-1/2 \-translate-x-1/2 z-50 whitespace-nowrap"\>\` containing a \`liquid-glass flex items-center gap-6 rounded px-4 py-2.5\` pill:  
   \- \`\<LogoMark /\>\`  
   \- \`\<div className="flex items-center gap-5"\>\` of \`NAV\_LINKS\` as \`\<a\>\` with classes \`text-sm font-body font-light text-white/70 hover:text-white transition-colors duration-200\`.  
   \- Right cluster \`flex items-center gap-3 ml-4\`: "Sign in" link (same style), then "Try it free" with \`liquid-glass-strong text-sm font-body font-medium text-white rounded px-4 py-1.5 transition-all duration-200 hover:scale-\[1.04\] hover:shadow-\[0\_0\_16px\_2px\_rgba(255,255,255,0.12)\] active:scale-\[0.97\]\`.

4\. \*\*Bottom row:\*\* fixed, \`bottom-12 left-0 right-0 px-10 flex items-end justify-between z-20\`, fade-in with \`transition-all duration-1000 delay-300\`.  
   \- Left \`\<p\>\`: \`text-sm font-body font-light text-white/75 max-w-\[220px\] leading-relaxed\`, text: "Forma's AI understands context, composition, and style like a creative director would."  
   \- Center absolute \`left-1/2 \-translate-x-1/2 bottom-0 flex items-center gap-3\` with two buttons:  
     \- Primary: \`group relative bg-white text-black text-sm font-body font-medium rounded px-6 py-3 overflow-hidden active:scale-\[0.97\] transition-all duration-200 shadow-\[0\_0\_0\_0\_rgba(255,255,255,0)\] hover:shadow-\[0\_0\_24px\_4px\_rgba(255,255,255,0.25)\] hover:scale-\[1.03\]\`. Contents: \`\<span className="relative z-10"\>Start generating\</span\>\` \+ overlay \`\<span className="absolute inset-0 bg-gradient-to-b from-white to-white/85 opacity-0 group-hover:opacity-100 transition-opacity duration-200" /\>\`.  
     \- Secondary: \`liquid-glass group text-white text-sm font-body font-medium rounded px-6 py-3 active:scale-\[0.97\] transition-all duration-200 hover:scale-\[1.03\] hover:shadow-\[inset\_0\_1px\_1px\_rgba(255,255,255,0.2),0\_0\_20px\_2px\_rgba(255,255,255,0.07)\]\` — label "See templates".  
   \- Right \`\<p\>\`: same classes as left plus \`text-right\`, text: "Describe what you see in your head — get images that actually match."

\#\#\# Notes  
\- Tailwind default border-radius is overridden to \`9999px\` (full pill) — every \`rounded\` in the markup produces pill corners.  
\- Do NOT use \`video.currentTime\` to reverse — the boomerang uses the captured \`frames\[\]\` array only.  
\- The video element stays mounted (hidden once \`framesReady\`) so the canvas keeps drawing snapshots.

# Guia 31

Build a dark monochrome landing page called Mindloop — a newsletter/content platform. Use React \+ Vite \+ TypeScript \+ Tailwind CSS \+ shadcn/ui \+ Framer Motion. Fonts: Inter (sans) and Instrument Serif (serif, used for italic accent words). The entire theme is pure black (\#000) background with white foreground — no colors or gradients beyond monochrome. Install hls.js and framer-motion.

Design System (index.css)  
All CSS variables in HSL (no hsl() wrapper in the variable, just the values):

\--background: 0 0% 0%  
\--foreground: 0 0% 100%  
\--card: 0 0% 5%  
\--card-foreground: 0 0% 100%  
\--primary: 0 0% 100%  
\--primary-foreground: 0 0% 0%  
\--secondary: 0 0% 12%  
\--secondary-foreground: 0 0% 85%  
\--muted: 0 0% 15%  
\--muted-foreground: 0 0% 65%  
\--accent: 170 15% 45%  
\--accent-foreground: 0 0% 100%  
\--border: 0 0% 20%  
\--input: 0 0% 18%  
\--ring: 0 0% 40%  
\--hero-subtitle: 210 17% 95%  
Liquid Glass Effect (global CSS class .liquid-glass)

.liquid-glass {  
  background: rgba(255, 255, 255, 0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}  
Animation Pattern  
All sections use a reusable fadeUp helper with staggered delays:

const fadeUp \= (delay: number) \=\> ({  
  initial: { opacity: 0, y: 20 },  
  whileInView: { opacity: 1, y: 0 },  
  viewport: { once: true, margin: "-100px" },  
  transition: { duration: 0.6, delay, ease: "easeOut" },  
});

Page Structure (top to bottom)  
1\. Navbar (fixed, transparent)  
Left: Logo (concentric circles icon — outer w-7 h-7 with border-2 border-foreground/60, inner w-3 h-3 with border border-foreground/60) \+ "Mindloop" bold text.  
Center-left: Nav links \["Home", "How It Works", "Philosophy", "Use Cases"\] separated by • dots. Links are text-muted-foreground hover:text-foreground.  
Right: 3 social icons (Instagram, Linkedin, Twitter from lucide-react) in liquid-glass circular buttons (w-10 h-10 rounded-full).  
No background — fully transparent, fixed top-0 z-50, padding px-8 md:px-28 py-4.

2\. Hero Section (full viewport height)  
Background: autoplaying looping muted MP4 video covering the entire section.  
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260325\_120549\_0cd82c36-56b3-4dd9-b190-069cfc3a623f.mp4  
Bottom gradient: h-64 bg-gradient-to-t from-background to-transparent for smooth fade to black.  
Content (centered, z-10, pt-28 md:pt-32):  
Avatar row: 3 overlapping circular avatars (-space-x-2, w-8 h-8 rounded-full border-2 border-background) \+ "7,000+ people already subscribed" in text-muted-foreground text-sm.  
Heading: text-5xl md:text-7xl lg:text-8xl font-medium tracking-\[-2px\] — "Get Inspired with Us" where "Inspired" is font-serif italic font-normal.  
Subtitle: text-lg in hsl(var(--hero-subtitle)) color — "Join our feed for meaningful updates, news around technology and a shared journey toward depth and direction."  
Email form: liquid-glass rounded-full p-2 max-w-lg container with email input and a white bg-foreground text-background rounded-full px-8 py-3 "SUBSCRIBE" button with whileHover scale 1.03 and whileTap scale 0.98.

3\. "Search has changed" Section  
Top padding pt-52 md:pt-64, bottom padding pb-6 md:pb-9.  
Heading: text-5xl md:text-7xl lg:text-8xl — "Search has changed. Have you?" with "changed." in serif italic.  
Subtitle: text-muted-foreground text-lg max-w-2xl mx-auto mb-24.  
3 platform cards (grid md:grid-cols-3 gap-12 md:gap-8 mb-20): Each card has a 200x200 icon image centered, platform name (font-semibold text-base), and description (text-muted-foreground text-sm).  
ChatGPT icon: local asset icon-chatgpt.png  
Perplexity icon: local asset icon-perplexity.png  
Google AI icon: local asset icon-google.png  
Bottom tagline: "If you don't answer the questions, someone else will." in text-muted-foreground text-sm text-center.

4\. Mission Section  
Padding pt-0 pb-32 md:pb-44.  
Video: Large 800x800 looping autoplaying muted video centered.  
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260325\_132944\_a0d124bb-eaa1-4082-aa30-2310efb42b4b.mp4  
Scroll-driven word-by-word reveal using useScroll and useTransform from framer-motion:  
Paragraph 1 (text-2xl md:text-4xl lg:text-5xl font-medium tracking-\[-1px\]): "We're building a space where curiosity meets clarity — where readers find depth, writers find reach, and every newsletter becomes a conversation worth having." Words "curiosity", "meets", "clarity" are highlighted in \--foreground, rest in \--hero-subtitle.  
Paragraph 2 (text-xl md:text-2xl lg:text-3xl font-medium mt-10): "A platform where content, community, and insight flow together — with less noise, less friction, and more meaning for everyone involved."  
Each word transitions opacity from 0.15 to 1 based on scroll progress.

5\. Solution Section  
Padding py-32 md:py-44, border-t border-border/30.  
Label: "SOLUTION" in text-xs tracking-\[3px\] uppercase text-muted-foreground.  
Heading: text-4xl md:text-6xl — "The platform for meaningful content" (serif italic on "meaningful").  
Video: Rounded rounded-2xl, aspect-\[3/1\] object-cover.  
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260325\_125119\_8e5ae31c-0021-4396-bc08-f7aebeb877a2.mp4  
4-column feature grid (md:grid-cols-4 gap-8): Curated Feed, Writer Tools, Community, Distribution — each with title (font-semibold text-base) and description (text-muted-foreground text-sm).

6\. CTA Section  
Padding py-32 md:py-44, border-t border-border/30, overflow-hidden.  
Background video (HLS via hls.js): absolute inset-0 object-cover z-0.  
HLS URL: https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8  
Uses Hls.isSupported() check with fallback to native HLS for Safari.  
Overlay: absolute inset-0 bg-background/45 z-\[1\].  
Content (z-10, centered):  
Concentric circles logo icon (w-10 h-10 outer, w-5 h-5 inner).  
Heading: "Start Your Journey" (serif italic).  
Subtitle in text-muted-foreground.  
Two buttons: "Subscribe Now" (bg-foreground text-background rounded-lg px-8 py-3.5) and "Start Writing" (liquid-glass rounded-lg).

7\. Footer  
Simple py-12 px-8 md:px-28 footer.  
Left: "© 2026 Mindloop. All rights reserved." in text-muted-foreground text-sm.  
Right: Privacy, Terms, Contact links in text-muted-foreground text-sm hover:text-foreground.

Key Dependencies  
framer-motion for all animations  
hls.js for the CTA background video streaming  
@fontsource/inter (400, 500, 600, 700\)  
@fontsource/instrument-serif (400, 400-italic)  
lucide-react for icons  
tailwindcss-animate plugin

Assets Needed  
3 avatar images (avatar-1.png, avatar-2.png, avatar-3.png)  
3 platform icons (icon-chatgpt.png, icon-perplexity.png, icon-google.png)

# Guia 32

Create a single-page landing page for a creative design studio called "Viktor Oddy" using React, TypeScript, Vite, and Tailwind CSS. Use lucide-react for icons. The page has a white background throughout and uses two custom fonts: "PP Neue Montreal" (body text, loaded from Webflow CDN) and "PP Mondwest" (serif accent font, loaded from a local /PPMondwest-Regular.woff2 file). The body default font is PP Neue Montreal with system fallbacks.

The page consists of these sections in order:

1\. HERO SECTION (centered, narrow column max-w-\[440px\], px-6, pt-12 md:pt-16)

Logo text: "Viktor Oddy" in PP Mondwest serif font, text-\[32px\] md:text-\[40px\] lg:text-\[44px\], font-semibold, color \#051A24, tracking-tight, mb-4. Fades in with staggered animation (delay 0.1s).  
Tagline: "The creative studio of Viktor Oddy" in monospace font (font-mono), text-xs md:text-sm, color \#051A24, mb-2. Animation delay 0.2s.  
Main Heading: Two lines: "Build the next wave," and "the bold way." where "next wave" and "bold way." are in PP Mondwest serif. Text is text-\[32px\] md:text-\[40px\] lg:text-\[44px\], leading-\[1.1\], color \#0D212C, tracking-tight, whitespace-nowrap. Animation delay 0.3s.  
Description: Three paragraphs in a flex-col gap-6 container, text-sm md:text-base, color \#051A24, leading-relaxed, mt-5 md:mt-6. Animation delay 0.4s.  
Paragraph 1: "I spent seven years at Apple crafting products used by over a billion people. I founded Vortex Studio to bring that same level of thinking to innovators shaping what comes next."  
Paragraph 2: "The studio is deliberately small. I guide the creative vision on every project, backed by a veteran design crew that moves fast without cutting corners."  
Paragraph 3: "Projects start at $5,000 per month."  
Two buttons in flex-col sm:flex-row, gap-3 md:gap-4, mt-5 md:mt-6. Animation delay 0.5s:  
"Start a chat" (primary: bg-\[\#051A24\], text white, rounded-full, px-7 py-3, with a complex multi-layered box-shadow including an inset highlight)  
"View projects" (secondary: bg-white, text \#051A24, no border, with subtle shadow)  
2\. INFINITE MARQUEE (full width, mt-16 md:mt-20, mb-16)

Horizontally scrolling image strip. Uses 8 GIF images duplicated (total 16\) in a flex row with animate-marquee CSS animation (translateX(0) to translateX(-50%), 30s linear infinite on desktop, 10s on mobile). Images are h-\[280px\] md:h-\[500px\], object-cover, mx-3, rounded-2xl, shadow-lg.

Image URLs (all from motionsites.ai):

https://motionsites.ai/assets/hero-space-voyage-preview-eECLH3Yc.gif  
https://motionsites.ai/assets/hero-portfolio-cosmic-preview-BpvWJ3Nc.gif  
https://motionsites.ai/assets/hero-velorah-preview-CJNTtbpd.gif  
https://motionsites.ai/assets/hero-asme-preview-B\_nGDnTP.gif  
https://motionsites.ai/assets/hero-transform-data-preview-Cx5OU29N.gif  
https://motionsites.ai/assets/hero-aethera-preview-DknSlcTa.gif  
https://motionsites.ai/assets/hero-orbit-web3-preview-BXt4OttD.gif  
https://motionsites.ai/assets/hero-nexora-preview-cx5HmUgo.gif  
3\. TESTIMONIAL QUOTE SECTION (py-12, px-6, max-w-2xl, centered)

A quote icon (lucide-react Quote, w-6 h-6, text-slate-900). Animation delay 0.1s.  
Large quote text: 'I left Apple to build the studio I always wanted to work with' where "Apple" is in PP Mondwest serif. Text sizing: text-\[32px\] md:text-\[40px\] lg:text-\[44px\], leading-\[1.1\], color \#0D212C, tracking-tight. Animation delay 0.2s.  
Author: "Viktor Oddy" in italic, text-sm, color \#273C46. Animation delay 0.3s.  
Three company logo names displayed as text: "Apple" (80px wide, 24px font), "IDEO" (83px wide, 24px font), "Polygon" (110px wide, 24px font). Font-medium, text-slate-900. Animation delay 0.4s.  
Below logos: A parallax image (scrolls with a parallax effect based on viewport position, max offset 200px). The image URL is: https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260330\_103804\_7aa5494f-4d5b-432e-9dc7-20715275f143.png\&w=1280\&q=85. Alt text "Chris Halaska". w-full max-w-xs rounded-2xl shadow-lg. Animation delay 0.5s. The parallax uses IntersectionObserver \+ scroll listener with requestAnimationFrame.  
4\. PRICING SECTION (full width, py-12, px-6)

Two cards in a grid (grid-cols-1 md:grid-cols-2, gap-8), aligned right on desktop (md:justify-end, md:max-w-4xl). Each card has rounded-\[40px\], pl-10 pr-10 md:pr-24 pt-3 pb-10.

Card 1 (Dark): bg-\[\#051A24\], inset shadow. Text color \#F6FCFF / \#E0EBF0. Animation delay 0.1s.

Title: "Monthly Partnership" (text-\[22px\], font-medium)  
Description: "A dedicated creative design team. / You work directly with Viktor."  
Price: "$5,000" (text-2xl, color \#F6FCFF), "Monthly" below  
Two buttons: "Start a chat" (primary) \+ "How it works" (secondary), both linking to https://halaskastudio.com/./book  
Card 2 (Light): bg-white, shadow-\[0\_4px\_16px\_rgba(0,0,0,0.08)\]. Animation delay 0.2s.

Title: "Custom Project" (text-\[22px\], font-medium)  
Description: "Fixed scope, fixed timeline. / Same team, same standards."  
Price: "$5,000" (text-2xl, color \#0D212C), "Minimum" below  
One button: "Start a chat" (tertiary variant: white bg with combined shadow)  
5\. TESTIMONIAL CAROUSEL (full width, py-20)

Header row (md:max-w-4xl, md:ml-auto): Title "What builders say" (where "builders" is in PP Mondwest serif, same large heading size) on left. On the right: 5 filled black star icons (lucide-react Star, w-5 h-5, fill-black) \+ "Clutch 5/5" text.  
Auto-scrolling carousel (3s interval, pauses on hover) with prev/next circular buttons (w-12 h-12 rounded-full, border border-\[\#0D212C\]/20, lucide ChevronLeft/ChevronRight).  
Cards are 427.5px wide on desktop (full width minus 48px on mobile), gap-6, with exit animation (opacity fade \+ scale down). Each card: bg-white, rounded-\[32px\] md:rounded-\[40px\], shadow-\[0\_4px\_16px\_rgba(0,0,0,0.08)\], px-6 md:pl-10 md:pr-24 py-8.  
Card content: SVG quote mark icon (custom path), quote text (text-base, color \#0D212C, leading-relaxed), author row with circular avatar (w-12 h-12), name (font-semibold, text-sm), role/company with arrow prefix.  
Testimonials array uses Pexels avatar images. The testimonials are tripled for infinite scroll effect. Transform uses cubic-bezier(0.4, 0, 0.2, 1\) with 0.8s transition.  
5 testimonials:

Marcus Anderson, CEO, Data.storage \- "With very little guidance team delivered designs that were consistently spot on..."  
alexwu, Founder, Nexgate \- "Viktor led the creation of our best fundraising deck to date\!..."  
James Mitchell, VP Product, LaunchPad \- "Working with Viktor transformed our product vision..."  
Rachel Foster, Co-founder, Nexus Labs \- "The design quality exceeded our expectations..."  
David Zhang, Head of Design, Paradigm Labs \- "Incredible work from start to finish..."  
6\. PROJECTS SECTION (max-w-\[1200px\], px-6, py-12)

Vertical stack of 3 project items (gap-16 md:gap-20). Each has:

Text block offset left (ml-20 md:ml-28): Project name in PP Mondwest serif (text-2xl md:text-3xl, font-semibold, color \#051A24) \+ description (text-sm md:text-base, color \#051A24/70)  
Full-width image below (rounded-2xl, shadow-lg, object-cover)  
Each item independently triggers fade-in animation via IntersectionObserver.  
Projects:

"evr" \- "From idea to millions raised for a web3 AI product" \- https://motionsites.ai/assets/hero-evr-ventures-preview-DZxeVFEX.gif  
"Automation Machines" \- "Streamlining industrial automation processes" \- https://motionsites.ai/assets/hero-automation-machines-preview-DlTveRIN.gif  
"xPortfolio" \- "Modern portfolio management platform" \- https://motionsites.ai/assets/hero-xportfolio-preview-D4A8maiC.gif  
7\. PARTNER SECTION (full width, py-12, px-6)

Large white container (max-w-7xl, py-48, rounded-\[40px\], subtle shadow). On mouse hover, GIF thumbnails (from the marquee images array) spawn at cursor position with random rotation (-10 to \+10 deg), fade out over 1000ms with scale-down, spawning every 80ms minimum. Uses requestAnimationFrame-style cleanup.

Centered heading: "Partner with us" in PP Mondwest serif, text-\[48px\] md:text-\[64px\] lg:text-\[80px\], color \#0D212C, mb-12.  
CTA button: Dark pill with circular avatar image (Pexels photo 415829, w-10 h-10 rounded-full) \+ "Start chat with Viktor". Same primary button shadow style.  
8\. FOOTER (full width, py-12, px-6, max-w-\[1200px\])

Flex row (md:flex-row). Left side: "Start a chat" primary button. Right side: ArrowUpRight icon (lucide-react), then two columns of links:

Column 1: Services, Work, About (anchor links)  
Column 2: x.com, LinkedIn (external links, target \_blank)  
All links: text-base, color \#051A24, hover:opacity-70 transition.

9\. COPYRIGHT BAR (max-w-\[1200px\], px-6, py-4)

Flex row justify-between: "Vortex Studio Limited" on left, "Austin, USA" on right. Text-sm, color \#051A24.

10\. FIXED BOTTOM NAV (z-50, centered)

Floating pill fixed to bottom (bottom-6, centered via left-1/2 \-translate-x-1/2). White bg, rounded-full, px-8 py-2, complex layered shadow. Contains: "V" letter in PP Mondwest serif (text-2xl, font-semibold, color \#051A24) \+ "Start a chat" primary button.

ANIMATIONS:

All sections use a custom useInViewAnimation hook (IntersectionObserver with threshold 0.1, triggers once). Elements get class animate-fade-in-up when in view (otherwise opacity-0). The animation is defined in CSS:

@keyframes fadeInUp {  
  0% { opacity: 0; transform: translateY(30px); }  
  100% { opacity: 1; transform: translateY(0); }  
}  
.animate-fade-in-up {  
  animation: fadeInUp 0.8s ease-out forwards;  
  opacity: 0;  
}  
Each element within a section has staggered animationDelay values (0.1s, 0.2s, 0.3s, etc.).

COLOR PALETTE:

Primary dark: \#051A24  
Secondary dark: \#0D212C  
Light text on dark: \#F6FCFF, \#E0EBF0  
Body text: \#051A24  
Muted text: \#273C46  
Background: white throughout  
BUTTON SHADOWS (critical for the design feel):

Primary: 0\_1px\_2px\_0\_rgba(5,26,36,0.1), 0\_4px\_4px\_0\_rgba(5,26,36,0.09), 0\_9px\_6px\_0\_rgba(5,26,36,0.05), 0\_17px\_7px\_0\_rgba(5,26,36,0.01), 0\_26px\_7px\_0\_rgba(5,26,36,0), inset\_0\_2px\_8px\_0\_rgba(255,255,255,0.5)  
Secondary: 0\_0\_0\_0.5px\_rgba(0,0,0,0.05), 0\_4px\_30px\_rgba(0,0,0,0.08)  
FONTS (CSS):

@font-face {  
  font-family: 'PP Neue Montreal';  
  src: url('https://assets.website-files.com/6009ec8cda7f305645c9d91b/60176f9bb43e36419997ecfe\_PPNeueMontreal-Book.otf') format('opentype');  
  font-weight: 400;  
  font-display: swap;  
}  
@font-face {  
  font-family: 'PP Neue Montreal';  
  src: url('https://assets.website-files.com/6009ec8cda7f305645c9d91b/60176f9b39c5673e51a86f5a\_PPNeueMontreal-Medium.otf') format('opentype');  
  font-weight: 500;  
  font-display: swap;  
}  
@font-face {  
  font-family: 'PP Mondwest';  
  src: url('/PPMondwest-Regular.woff2') format('woff2');  
  font-weight: 400;  
  font-display: swap;  
}  
FILE STRUCTURE:

src/App.tsx \- Main layout with hero, marquee, and section composition  
src/components/Button.tsx \- Reusable button (primary/secondary/tertiary variants)  
src/components/TestimonialSection.tsx \- Quote with parallax image  
src/components/PricingSection.tsx \- Two pricing cards  
src/components/TestimonialCarousel.tsx \- Auto-scrolling testimonial cards  
src/components/ProjectsSection.tsx \- Project showcase items  
src/components/PartnerSection.tsx \- Interactive mouse-trail CTA section  
src/components/Footer.tsx \- Footer with links  
src/components/CopyrightBar.tsx \- Copyright line  
src/components/BottomNav.tsx \- Fixed floating bottom nav  
src/hooks/useInViewAnimation.ts \- IntersectionObserver scroll-trigger hook  
src/index.css \- Font faces, marquee animation, fade-in-up animation

# Guia 33

Build a full-screen hero section using React, Tailwind CSS, Framer Motion, and Lucide React icons. Use the Inter font. The page is fully mobile-responsive. Here are the exact specifications:

\---

\*\*BACKGROUND:\*\*  
\- A full-screen autoplaying, looping, muted video covering the entire viewport as a background.  
\- Video URL: \`https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260517\_222138\_3e3205be-3364-417b-a64a-bfe087acbec4.mp4\`  
\- The video is positioned absolute, inset-0, with \`object-cover\` to fill the viewport.

\---

\*\*COLOR:\*\*  
\- Accent color: \`\#5E0ED7\` (deep purple). Used for the logo dot, the "+" symbols in stats, and the CTA link text.  
\- All body text is black (\#000).

\---

\*\*FONT:\*\*  
\- Font family: \`'Inter', sans-serif\` applied to the root container.  
\- All text is uppercase with wide letter-spacing (\`tracking-widest\` or \`tracking-wide\`).  
\- Font weights: 600 (semibold) throughout.

\---

\*\*LAYOUT (flex column, min-h-screen):\*\*  
The page is a flex column with three vertical sections:  
1\. \*\*Nav\*\* (top, fixed height)  
2\. \*\*Stats row\*\* (flex-1, vertically centered, right-aligned)  
3\. \*\*Bottom content\*\* (pinned to bottom with padding)

\---

\*\*NAVIGATION BAR:\*\*  
\- Horizontal flex, items centered, justified between. Padding: \`px-5 sm:px-8 md:px-12 pt-5 md:pt-6\`.  
\- \*\*Left:\*\* A circular logo — 32px round div with 2px border in accent color, containing a 10px solid circle in accent color.  
\- \*\*Center (hidden on mobile, visible md+):\*\* Four nav links: "Story", "Expertise", "Studios", "Feedback". Text: 14px, font-semibold, tracking-widest, uppercase, black.  
\- \*\*Right:\*\* A 36px round black button with three horizontal white lines (hamburger icon — three \`span\` elements, each \`w-4 h-0.5 bg-white\` with \`gap-1\`). This opens the mobile menu on click.

\---

\*\*MOBILE MENU OVERLAY:\*\*  
\- Triggered by hamburger click. Fixed, full-screen, z-50, white background.  
\- Top row: same logo (left) and a 36px round black close button with an X icon (right).  
\- Below: vertical list of the 4 nav links at \`text-3xl\`, font-semibold, tracking-widest, uppercase, with \`gap-8\` and \`mt-16\`.  
\- Bottom (mt-auto): "Work With Us" CTA in accent color with ArrowUpRight icon, \`text-xl\`.

\---

\*\*STATS ROW (middle section):\*\*  
\- Container: \`flex-1 flex items-center justify-end\`, with same horizontal padding. \`py-8 md:py-0\`.  
\- Three stat items in a horizontal row with \`gap-5 sm:gap-8 md:gap-10\`, each right-aligned:  
  \- \*\*+300\*\* / CRAFTED BRANDS  
  \- \*\*+200\*\* / DIGITAL PRODUCTS  
  \- \*\*+100\*\* / VENTURES FUNDED  
\- Number styling: \`fontSize: clamp(1.5rem, 5vw, 3.5rem)\`, weight 600\. The "+" is rendered separately in accent color at 0.5em size. The number is black.  
\- Label: \`text-\[10px\] sm:text-xs md:text-sm\`, font-semibold, tracking-widest, uppercase, black, \`whitespace-pre-line leading-tight\` (each label has a line break between the two words).

\---

\*\*BOTTOM SECTION:\*\*  
\- Padding: \`px-5 sm:px-8 md:px-12 pb-8 md:pb-12\`. Flex column with \`gap-6 md:gap-12\`.

\*\*Row A (tagline \+ CTA):\*\*  
\- Flex row, items-center, justify-between, gap-4.  
\- \*\*Left:\*\* Small uppercase tagline paragraph: "Shaping Bold / Visions Into Power / For Your Tribe" (with \`\<br /\>\` line breaks). Text: \`text-\[10px\] sm:text-xs md:text-sm\`, font-semibold, tracking-widest, max-width \`130px sm:160px md:max-w-xs\`.  
\- \*\*Right:\*\* CTA link "Work With Us" with ArrowUpRight icon. Text: \`text-base sm:text-xl md:text-2xl\`, accent color, weight 600, \`whitespace-nowrap\`. Icon: 18px on mobile, 22px on sm+.

\*\*Row B (description \+ main heading):\*\*  
\- Flex row, \`items-end\`, justify-between, \`gap-3 sm:gap-4\`.  
\- \*\*Left:\*\* A fixed-width container (\`w-\[120px\] sm:w-\[180px\] md:w-\[280px\]\`, shrink-0) containing a paragraph: "Creative Studios Built Around Elevating Your Vision Into Striking Reality". Text: \`text-\[9px\] sm:text-xs md:text-sm\`, font-semibold, tracking-widest, uppercase, \`text-left md:text-right\`.  
\- \*\*Right:\*\* The main heading — three words stacked vertically: "Fearless", "Vision", "Delivered". Each word in its own \`overflow-hidden\` wrapper. Text: \`fontSize: clamp(2rem, 9vw, 9rem)\`, \`lineHeight: 0.88\`, weight 600, uppercase, black, text-right.

\---

\*\*ANIMATIONS (Framer Motion):\*\*

All animations fire on page load (initial \-\> animate).

1\. \*\*fadeDown variant\*\* (nav elements):  
   \- From: \`{ opacity: 0, y: \-20 }\`  
   \- To: \`{ opacity: 1, y: 0 }\`  
   \- Each element has a custom stagger index. Delay: \`index \* 0.1s\`. Duration: 0.5s. Ease: \`\[0.22, 1, 0.36, 1\]\`.  
   \- Applied to: logo (custom=0), each nav link (custom=1-4), hamburger (custom=5).

2\. \*\*fadeUp variant\*\* (stats \+ bottom content):  
   \- From: \`{ opacity: 0, y: 32 }\`  
   \- To: \`{ opacity: 1, y: 0 }\`  
   \- Delay: \`index \* 0.12s\`. Duration: 0.6s. Ease: \`\[0.22, 1, 0.36, 1\]\`.  
   \- Applied to: each stat card (custom=2,3,4), tagline paragraph (custom=5), CTA link (custom=6), description block (custom=7).

3\. \*\*Heading slide-up\*\* (main heading words):  
   \- Each word slides up from \`y: "110%"\` to \`y: 0\` within its overflow-hidden parent (clip reveal effect).  
   \- Delay: \`0.4 \+ wordIndex \* 0.14\` (so 0.4s, 0.54s, 0.68s). Duration: 0.7s. Ease: \`\[0.22, 1, 0.36, 1\]\`.

\---

\*\*RESPONSIVE BREAKPOINTS:\*\*  
\- Mobile-first. Three tiers: default (mobile), \`sm:\` (640px), \`md:\` (768px).  
\- Nav links hidden on mobile, shown md+.  
\- Spacing, font sizes, and widths scale up at each breakpoint.  
\- Mobile menu provides full navigation on small screens.

\---

\*\*DEPENDENCIES:\*\*  
\- React 18  
\- Tailwind CSS 3  
\- framer-motion  
\- lucide-react (ArrowUpRight, X icons)

# Guia 34

Build a Hero section for a DeFi dashboard named RIVR showcasing a sleek, glassmorphism aesthetic. Please mimic these exact specifications to ensure a premium UI.

Dependencies:   
\- Use \`lucide-react\` for icons.  
\- Use \`motion\` (imported from \`'motion/react'\`) for animations.

1\. Global Styles (\`src/index.css\`)  
Import the custom 'Helvetica Regular' font, set the Tailwind theme properly, and reset the body. Exact CSS to include:  
@import "tailwindcss";

@font-face {  
    font-family: "Helvetica Regular";  
    src: url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.eot");  
    src: url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.eot?\#iefix")format("embedded-opentype"),  
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.woff2")format("woff2"),  
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.woff")format("woff"),  
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.ttf")format("truetype"),  
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.svg\#Helvetica Regular")format("svg");  
}

@theme {  
  \--font-helvetica: "Helvetica Regular", ui-sans-serif, system-ui, sans-serif;  
}

:root {  
  font-family: var(--font-helvetica);  
}

body {  
  margin: 0;  
  overflow-x: hidden;  
  background-color: \#f0f0f0;  
}

2\. App Structure (\`src/App.tsx\`)  
Create a single \`\<main className="min-h-screen bg-\[\#f0f0f0\]"\>\` instance that returns the \`\<Hero /\>\` component.

3\. Hero Component (\`src/components/Hero.tsx\`)  
Outer wrapper: \`\<div className="w-full h-screen flex items-center justify-center p-3 md:p-5 bg-\[\#f0f0f0\]"\>\`.  
Inner container: \`\<section className="relative w-full max-w-\[1536px\] h-full rounded-\[1.5rem\] md:rounded-\[3rem\] overflow-hidden shadow-none flex flex-col items-center bg-white/10 group"\>\`  
Inside the \`\<section\>\`:  
\- The Video Background:   
  A \`\<video\>\` element with \`autoPlay muted loop playsInline\`.   
  Classes: \`absolute inset-0 w-full h-full object-cover object-\[65%\] lg:object-center z-0\`.   
  Source URL: \`https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260428\_193507\_4286c423-2fd9-4efd-92bd-91a939453fc1.mp4\` (Must use exactly this URL).  
\- The Content Layer:  
  A \`\<div className="relative z-10 w-full h-full flex flex-col items-center"\>\`.  
  Inside it, place: \`\<Navbar /\>\`, the text container, \`\<BottomLeftCard /\>\`, and \`\<BottomRightCorner /\>\`.  
\- Text Container:  
  \`\<div className="w-full flex flex-col items-center pt-8 px-6 text-center max-w-4xl"\>\`. Inside it:  
  \- \`\<HeroBadge /\>\`  
  \- A \`\<motion.h1\>\` with class: \`text-4xl sm:text-5xl md:text-6xl lg:text-\[80px\] font-normal text-\[\#5E6470\] mb-2 tracking-tight leading-\[1.05\]\`. Text: "Fluid Asset Streams". Animation: initial={{ opacity: 0, scale: 0.98 }}, animate={{ opacity: 1, scale: 1 }}, transition={{ duration: 0.8, delay: 0.2 }}.  
  \- A \`\<motion.p\>\` with class: \`text-sm sm:text-base md:text-lg text-\[\#5E6470\] opacity-80 leading-relaxed max-w-xl font-normal\`. Text: "Access Smart Vaults, stake RIVR, NFTs, transform rigid holdings into liquid cash instantly.". Animation: initial={{ opacity: 0 }}, animate={{ opacity: 1 }}, transition={{ duration: 0.8, delay: 0.4 }}.

4\. Navbar Component (\`src/components/Navbar.tsx\`)  
Wrapper: \`\<nav className="flex items-center justify-between py-6 px-6 md:px-10 w-full relative z-10"\>\`.  
\- Left Side (hidden spacer for centering): \`\<div className="flex-1 hidden md:block" /\>\`  
\- Center Menu: \`\<ul className="hidden md:flex items-center gap-8 text-\[rgb(45,45,45)\] font-normal text-sm"\>\`. Include items: Ecosystem, Economics (hasDropdown), Developers, Governance (hasDropdown). List items need: \`cursor-pointer hover:opacity-70 transition-opacity flex items-center gap-1 group\`. Append a \`ChevronRight\` icon (classes: \`w-4 h-4 transition-transform group-hover:translate-x-0.5\`) if hasDropdown is true.  
\- Mobile Logo: \`\<div className="md:hidden"\>\<span className="font-regular tracking-tighter text-xl text-\[rgba(30,50,90,0.9)\]"\>RIVR\</span\>\</div\>\`  
\- Right Button: \`\<div className="flex-1 flex justify-end"\>\` wrapping a \`\<motion.button\>\` (whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}).   
  Button classes: \`flex items-center bg-\[rgba(30,50,90,0.8)\] text-white rounded-full pl-2 pr-4 md:pr-6 py-1.5 md:py-2 gap-2 md:gap-3 hover:bg-\[rgba(30,50,90,1)\] transition-colors group\`. Inside button: Add an icon wrapper \`\<div className="bg-white/20 p-1 md:p-1.5 rounded-full flex items-center justify-center"\>\` containing \`ArrowUpRight\` (w-4 h-4 md:w-5 md:h-5 text-white), and a text node "Book Demo" (\`text-xs md:text-sm font-normal\`).

5\. HeroBadge Component (\`src/components/HeroBadge.tsx\`)  
Returns a \`\<motion.div\>\` (initial opacity 0, y 20; animate opacity 1, y 0; transition duration 0.6, ease "easeOut").  
Classes: \`flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 backdrop-blur-md border border-white/20 mx-auto mb-3 w-fit\`.  
Contents: \`\<Sparkles className="w-4 h-4 text-\[rgba(30,50,90,0.8)\]" /\>\` and text \`\<span className="text-\[14px\] font-normal text-\[rgba(30,50,90,0.9)\]"\>Fluid Staking\</span\>\`.

6\. BottomLeftCard Component (\`src/components/BottomLeftCard.tsx\`)  
Returns a \`\<motion.div\>\` (initial x: \-20, opacity: 0; animate x: 0, opacity: 1; transition: duration 0.8, delay 0.2).  
Position/Styling: \`absolute bottom-28 right-4 left-auto md:left-6 md:right-auto md:bottom-6 lg:bottom-10 lg:left-10 p-3 md:p-4 lg:p-5 rounded-\[1.2rem\] md:rounded-\[1.5rem\] lg:rounded-\[2.2rem\] bg-white/30 backdrop-blur-xl flex flex-col gap-2 lg:gap-3 min-w-\[140px\] md:min-w-\[150px\] lg:min-w-\[180px\] w-fit\`.  
\- Top text block: column with "5.2K" (classes: \`text-2xl md:text-3xl font-normal text-\[rgba(30,50,90,0.9)\] tracking-tight\`) and "Active Yielders" (classes: \`text-\[10px\] md:text-\[12px\] font-normal text-\[rgba(30,50,90,0.6)\] uppercase tracking-wider\`).  
\- Join Discord \`\<motion.button\>\` (hover/tap scale 1.02/0.98). Classes: \`flex items-center bg-white rounded-full pl-1.5 pr-5 py-1.5 gap-2 hover:bg-white/90 transition-colors self-start group\`. Inside: wrap \`ArrowUpRight\` in \`\<div className="bg-\[rgba(30,50,90,0.1)\] p-1 rounded-full ..."\>\` (using \`text-\[rgba(30,50,90,0.9)\]\` for icon) and append "Join Discord" text (\`text-\[14px\] font-normal text-\[rgba(30,50,90,0.9)\]\`).

7\. BottomRightCorner Component (\`src/components/BottomRightCorner.tsx\`)  
This requires a complex faux-cutout layout. Use a \`\<motion.div\>\` (initial y: 20, opacity: 0; animate y: 0, opacity: 1; duration: 0.8, delay: 0.4).  
Classes: \`absolute bottom-0 right-0 p-3 pt-5 pl-8 sm:p-4 sm:pt-6 sm:pl-10 md:p-6 md:pt-8 md:pl-14 bg-\[\#f0f0f0\] rounded-tl-\[1.5rem\] sm:rounded-tl-\[2rem\] md:rounded-tl-\[3.5rem\] flex items-center gap-3 sm:gap-4 md:gap-6\`.  
CRITICAL corner masks to include inside this container:  
\- Top intersection mask: \`\<div className="absolute \-top-\[1.5rem\] sm:-top-\[2rem\] md:-top-\[3.5rem\] right-0 w-\[1.5rem\] sm:w-\[2rem\] md:w-\[3.5rem\] h-\[1.5rem\] sm:h-\[2rem\] md:h-\[3.5rem\] pointer-events-none"\>\<svg width="100%" height="100%" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg"\>\<path d="M56 56V0C56 30.9279 30.9279 56 0 56H56Z" fill="\#f0f0f0"/\>\</svg\>\</div\>\`  
\- Left intersection mask: \`\<div className="absolute bottom-0 \-left-\[1.5rem\] sm:-left-\[2rem\] md:-left-\[3.5rem\] w-\[1.5rem\] sm:w-\[2rem\] md:w-\[3.5rem\] h-\[1.5rem\] sm:h-\[2rem\] md:h-\[3.5rem\] pointer-events-none"\>\<svg width="100%" height="100%" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg"\>\<path d="M56 56H0C30.9279 56 56 30.9279 56 0V56Z" fill="\#f0f0f0"/\>\</svg\>\</div\>\`  
Content:   
\- Circle Icon: A div with \`bg-\[rgba(30,50,90,0.05)\] w-10 h-10 md:w-14 md:h-14 rounded-full flex items-center justify-center border border-\[rgba(30,50,90,0.1)\]\` using \`ArrowUpRight\` (\`text-\[rgba(30,50,90,0.8)\]\`).  
\- Info column containing title "Documentation" (\`text-\[16px\] md:text-\[20px\] font-normal text-\[rgba(30,50,90,0.95)\]\`). Below it, a line containing text "Library" and a \`ChevronRight\` icon wrapped in \`\<div className="flex items-center gap-1 text-\[rgba(30,50,90,0.6)\] cursor-pointer hover:text-\[rgba(30,50,90,0.8)\] transition-colors"\>\<span className="text-\[12px\] md:text-\[15px\] font-normal"\>...\`

# Guia 35

Build a full-viewport cinematic hero section for a travel brand called "Wanderful" using React \+ TypeScript \+ Vite \+ Tailwind CSS. Use GSAP for animation and \`lucide-react\` for icons.

\*\*Fonts (load via Google Fonts in \`src/index.css\`):\*\*  
\`\`\`css  
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1\&family=Barlow:wght@300;400;500;600\&family=Inter:wght@300;400;500;600;700\&display=swap');  
\`\`\`  
Also load a custom display font:  
\`\`\`css  
@font-face {  
  font-family: 'Dirtyline';  
  src: url('https://fonts.cdnfonts.com/s/15011/Dirtyline36DaysofType.woff') format('woff');  
  font-weight: normal; font-style: normal; font-display: swap;  
}  
\`\`\`  
Body font: \`Barlow\`. Hero headings: \`Inter\`. Body background: \`\#000\`.

\*\*Video background (fixed, full screen, z-0):\*\*  
\- Use this exact CloudFront URL as the \`\<video\>\` src:  
  \`https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260510\_060007\_60275ce7-030c-4668-a160-8f364ec537d3.mp4\`  
\- Attributes: \`autoPlay muted loop playsInline\`, \`object-cover\`, wrapper scaled \`scale-\[1.08\]\` with \`origin-center\`.  
\- On \`onLoadedMetadata\`, set \`playbackRate \= 1.25\`.  
\- Add GSAP-driven mouse parallax: listen to \`mousemove\`, compute \`targetX/Y \= ((clientX \- cx)/cx) \* 20\`, lerp \`currentX/Y \+= (target \- current) \* 0.06\` inside \`requestAnimationFrame\`, and apply via \`gsap.set(videoBg, { x, y })\`.

\*\*Liquid-glass utility (add to \`index.css\`):\*\*  
\`\`\`css  
.liquid-glass {  
  background: rgba(255,255,255,0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: "";  
  position: absolute; inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%,  
    rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%,  
    rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%,  
    rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}  
\`\`\`

\*\*Header (fixed top, z-50, \`px-10 py-8\`, flex justify-between items-center):\*\*  
\- Left: wordmark \`Wanderful\` followed by \`\<sup\>TM\</sup\>\`, \`text-\[17px\] font-semibold tracking-tight\`.  
\- Center: \`\<nav\>\` using \`.liquid-glass rounded-full px-2 py-2 flex items-center gap-1\`. Links: \`JOURNEY\`, \`BENEFITS\`, \`JOURNAL\`, \`GUIDEBOOK\`. Each link: \`text-\[11px\] font-medium tracking-\[0.12em\] text-white/90 hover:text-white px-4 py-1.5 rounded-full transition-colors duration-200\`.  
\- Right: "GET ROAMING" anchor with same \`.liquid-glass rounded-full px-5 py-2.5 text-\[11px\] font-medium tracking-\[0.12em\] text-white/90 hover:text-white\`.

\*\*Hero headline (fixed, \`top: 120px\`, centered, z-20):\*\*  
Two lines, both centered, \`Inter\` 400, \`font-size: clamp(40px, 5.4vw, 72px)\`, \`line-height: 1.1\`, \`letter-spacing: \-0.02em\`:  
\- Line 1 (white): \`Venture without edges.\`  
\- Line 2 (\`rgba(255,255,255,0.55)\`): \`Uncover with keen instinct.\`

Fade-in on mount: \`opacity 0 → 100\` and \`translate-y-6 → 0\` with \`transition-all duration-1000\`.

\*\*Bottom block (fixed \`bottom-14\`, z-20, flex-col items-center gap-6), fade-in with \`delay-300\`:\*\*  
1\. Paragraph, \`max-w-\[620px\] text-\[15px\] leading-relaxed\` centered:  
   \- White: "Our smart itineraries shape around you — your rhythm, your vibe, your hunger for adventure."  
   \- \`text-white/55\`: " Each getaway is tailored, seamless, and wholly yours."  
2\. Button: white bg, black text, \`text-\[15px\] font-medium rounded-full px-8 py-3.5\`, hover \`scale-\[1.03\]\` \+ \`shadow-\[0\_0\_32px\_4px\_rgba(255,255,255,0.2)\]\`, active \`scale-\[0.97\]\`. Label: \`Plan my escape today\`.  
3\. Row: \`Lock\` icon from lucide-react (\`size={13} strokeWidth={1.5}\`) \+ \`text-\[11px\] font-medium tracking-\[0.14em\] text-white/70\`, text: \`SECURE BY DESIGN. ZERO DATA LEAKS.\`

\*\*Root container:\*\* \`min-h-screen bg-black text-white overflow-x-hidden\` with inline \`fontFamily: "'Inter', sans-serif"\`.

Dependencies: \`gsap\`, \`lucide-react\`, \`react\`, \`react-dom\`, tailwind configured with content globs \`./index.html\` and \`./src/\*\*/\*.{js,ts,jsx,tsx}\`.

# Guia 36

Create a high-end, dark-themed hero section for a coding education platform called 'CodeNest' using React and Tailwind CSS. The design must be responsive and follow these precise specifications:

1\. Background & Layout:

Background: Implement a full-screen background video using the HLS stream: https://stream.mux.com/tLkHO1qZoaaQOUeVWo8hEBeGQfySP02EPS02BmnNFyXys.m3u8. Use hls.js and set enableWorker: false to ensure stability in sandboxed environments.

Overlays: Set the video to 60% opacity. Add a dark linear gradient from the left (\#070b0a to transparent) and a bottom-up gradient for readability.

Grid System: Add three thin vertical grid lines (white/10 opacity) at the 25%, 50%, and 75% marks across the screen (visible on desktop).

Central Glow: Place a large horizontal SVG ellipse glow in the center-top area with a cyan/dark green hue, using a 25px Gaussian blur filter.

2\. The Liquid Glass Card:

Component: Create a 200x200px floating card positioned above the main headline, shifted exactly 50px upwards using translate-y-\[-50px\].

CSS Styling (Liquid Glass):

background: rgba(255, 255, 255, 0.01) with background-blend-mode: luminosity.

backdrop-filter: blur(4px).

box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1).

Border Effect: A ::before pseudo-element with inset: 0, padding: 1.4px, and a 180-degree white linear gradient. Use \-webkit-mask-composite: xor and mask-composite: exclude to create a sharp, high-end border frame.

Content: '\[ 2025 \]' tag (14px), 'Taught by Industry Professionals' headline (18px, using Instrument Serif italic for 'Industry'), and a small description (11px).

3\. Hero Content & Typography:

Eyebrow: 'Career-Ready Curriculum' in Plus Jakarta Sans, bold, 11px, color \#5ed29c.

Main Headline: 'LAUNCH YOUR CODING CAREER.' in Inter Extra Bold, uppercase, tracking-tight. Scale from 40px (mobile) to 72px (desktop). The final period must be green (\#5ed29c).

Description: 'Master in-demand coding skills...' in Inter, 14px, 70% white opacity, max-width 512px.

Primary CTA: 'Get Started' button with an ArrowRight icon. Rounded-full, background \#5ed29c, text \#070b0a, uppercase, bold.

4\. Global Navigation:

Header: Sticky/Absolute header with a white minimalist logo.

Desktop Menu: Links for 'PROJECTS', 'BLOG', 'ABOUT', 'RESUME' in Inter, 16px. Hover state: \#5ed29c.

Mobile Menu: A functional hamburger menu that toggles a full-screen dark overlay.

5\. Required Imports:

Fonts: Inter, Plus Jakarta Sans, and Instrument Serif (italic).

Icons: lucide-react (ArrowRight, Menu, X).

Library: hls.js for video streaming.

# Guia 37

Build a React \+ TypeScript \+ Tailwind CSS single-page hero section using Vite. The entire page lives in \`src/App.tsx\`. No extra libraries beyond \`react\`, \`react-dom\`, \`lucide-react\`, and Tailwind.

\*\*Background:\*\*  
\- A fullscreen autoplaying, muted, looping, \`playsInline\` background \`\<video\>\` element absolutely positioned \`inset-0 w-full h-full object-cover\`.  
\- Video URL (exact): \`https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260508\_215831\_c6a8989c-d716-4d8d-8745-e972a2eec711.mp4\`  
\- Root wrapper: \`relative min-h-screen overflow-hidden bg-\[\#f0f0ee\]\`.  
\- Foreground content wrapper: \`relative z-10 flex flex-col min-h-screen\`.

\*\*Logo (inline SVG component):\*\*  
\- \`width="18" height="18"\`, \`viewBox="0 0 256 256"\`, \`fill="none"\`.  
\- Single path with \`fill="rgb(84, 84, 84)"\` and \`d="M 160 88 L 194 34 L 216 0 L 256 0 L 256 40 L 221.5 93.5 L 200 128 L 256 128 L 256 256 L 96 256 L 96 168 L 64.246 220 L 40 256 L 0 256 L 0 216 L 34 162 L 56 128 L 0 128 L 0 0 L 160 0 Z"\`.

\*\*Navbar (centered, pill-style, two separate pills):\*\*  
\- \`\<nav\>\` classes: \`flex items-center justify-center pt-4 sm:pt-6 px-4 sm:px-8 gap-2 sm:gap-3\`.  
\- Left circular logo container: \`flex items-center justify-center rounded-full w-10 h-10 sm:w-11 sm:h-11 shrink-0\`, inline style \`backgroundColor: '\#EDEDED'\`, contains the Logo.  
\- Right pill container: \`flex items-center gap-4 sm:gap-10 rounded-xl px-4 sm:px-8 py-2.5 sm:py-3\`, inline style \`backgroundColor: '\#EDEDED'\`.  
\- Nav links array: \`\['Story', 'Products', 'Help', 'Support'\]\`. Each anchor: \`text-\[12px\] sm:text-\[14px\] font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200\`.

\*\*Hero content (bottom-left aligned):\*\*  
\- Outer: \`flex-1 flex items-end pb-10 sm:pb-16 lg:pb-20 px-6 sm:px-12 md:px-20 lg:px-28\`.  
\- Inner: \`max-w-xs\`. Four stacked elements, each with \`mb-3\`:

1\. Badge link: \`inline-flex items-center gap-1.5 text-\[11.5px\] font-medium text-blue-500 hover:text-blue-600 transition-colors mb-3 group\`. Text: \`Seen on Shark Tank in India\` followed by an arrow \`→\` in a span with \`inline-block transition-transform duration-200 group-hover:translate-x-0.5\`.

2\. Headline \`\<h1\>\`: \`text-\[1.5rem\] sm:text-\[1.75rem\] leading-\[1.15\] font-medium text-gray-900 tracking-tight mb-3\`. Text: \`Simple, smart prosthetics made for people who keep fighting.\`

3\. Subtext \`\<p\>\`: \`text-\[13px\] text-gray-400 font-normal mb-3\`. Text: \`Reclaim your movement now.\`

4\. CTA anchor: \`inline-flex items-center gap-2 text-\[13px\] font-medium text-blue-500 border border-blue-400 rounded-full px-5 py-2.5 hover:bg-blue-500 hover:text-white hover:border-blue-500 transition-all duration-200 group\`. Text: \`Try a free fitting\` plus arrow \`→\` in span with \`transition-transform duration-200 group-hover:translate-x-0.5\`.

\*\*Animations / micro-interactions:\*\*  
\- Arrow spans translate right by \`0.5\` on group hover (\`group-hover:translate-x-0.5\`).  
\- CTA fills blue on hover (bg \+ text \+ border transitions, 200ms).  
\- Nav links shift from gray-700 to gray-900 on hover.

\*\*Fonts:\*\* Default Tailwind sans-serif system font stack (no custom font). All sizes are exact pixel/rem values above (\`11.5px\`, \`12px\`, \`13px\`, \`14px\`, \`1.5rem\`, \`1.75rem\`).

\*\*Colors:\*\* Page background \`\#f0f0ee\`; pill backgrounds \`\#EDEDED\`; accent \`blue-500/600/400\`; text \`gray-900/700/400\`.

Do not add any other sections, no Supabase wiring, no routing. Only the single hero page as described.

# Guia 38

Create a full-screen dark hero section with a looping background video, navbar, headline, subtitle, CTA button, and a logo marquee at the bottom. Here are the exact specifications:

Theme & Colors (index.css CSS variables):  
Background: 260 87% 3% (deep dark blue-purple)  
Foreground: 40 6% 95% (off-white)  
Hero sub text: 40 6% 82%  
Body font: Geist Sans (via @fontsource/geist-sans)  
Headline font: General Sans (loaded from Fontshare: https://api.fontshare.com/v2/css?f\[\]=general-sans@400,500,600,700\&display=swap)

Background Video (Index page wrapper):  
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260328\_065045\_c44942da-53c6-4804-b734-f9e07fc22e08.mp4  
Positioned absolute inset-0 w-full h-full object-cover behind all content  
Starts with opacity: 0  
Custom JS-controlled fade loop: 0.5s fade-in at start, 0.5s fade-out at end, using requestAnimationFrame. On ended, opacity resets to 0, waits 100ms, then replays from 0  
No gradient overlays on the video  
The wrapper div has overflow-hidden, the hero content sits in a relative z-10 div above

Blurred overlay shape (centered behind content):  
w-\[984px\] h-\[527px\] opacity-90 bg-gray-950 blur-\[82px\]  
Absolutely positioned at top-1/2 left-1/2 \-translate-x-1/2 \-translate-y-1/2  
pointer-events-none  
The hero section has overflow-visible so the blur is not clipped

Navbar:  
Full width, py-5 px-8, flex row with justify-between  
Left: logo image (src/assets/logo.png, height 32px)  
Center: nav items — "Features" (with ChevronDown), "Solutions", "Plans", "Learning" (with ChevronDown). Each is a button with text-foreground/90 and hover transition  
Right: "Sign Up" button using heroSecondary variant, rounded-full px-4 py-2  
Below navbar: a 1px divider line with gradient from-transparent via-foreground/20 to-transparent, offset mt-\[3px\]

Hero content (vertically centered in remaining space via flex-1):  
Headline: "Power AI" at text-\[220px\], font-normal, leading-\[1.02\], tracking-\[-0.024em\], font-family General Sans  
"Power " is plain text-foreground  
"AI" uses bg-clip-text text-transparent with backgroundImage: linear-gradient(to left, \#6366f1, \#a855f7, \#fcd34d) (indigo → purple → amber)  
Subtitle: "The most powerful AI ever deployed / in talent acquisition" — text-hero-sub, text-lg, leading-8, max-w-md, mt-\[9px\], opacity-80  
CTA: "Schedule a Consult" button, heroSecondary variant, px-\[29px\] py-\[24px\], mt-\[25px\]

Logo marquee (pinned to bottom of hero, pb-10):  
Container: max-w-5xl mx-auto  
Left side: static text "Relied on by brands / across the globe" in text-foreground/50 text-sm  
Right side: infinite scrolling marquee with logos: Vortex, Nimbus, Prysma, Cirrus, Kynder, Halcyn (duplicated for seamless loop)  
Each logo: a liquid-glass 24x24 rounded-lg icon showing the first letter, plus the name in text-base font-semibold text-foreground  
Marquee animation: translateX(0%) → translateX(-50%), 20s linear infinite  
gap-16 between logos, gap-12 between text and marquee

Liquid glass utility class (in index.css):  
.liquid-glass { background: rgba(255, 255, 255, 0.01); background-blend-mode: luminosity; backdrop-filter: blur(4px); border: none; box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1); position: relative; overflow: hidden; }  
.liquid-glass::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1.4px; background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%); \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0); \-webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none; }

Section structure: min-h-screen flex flex-col — navbar at top, content centered via flex-1 flex items-center justify-center, marquee at bottom.

# Guia 39

Build a premium, AI-native email client landing page called "Aura" using \*\*React 18 \+ TypeScript \+ Vite \+ Tailwind CSS \+ motion/react (framer motion) \+ lucide-react\*\*. The aesthetic is dark (bg \`\#0c0c0c\`), cinematic, glassy, with a looping fullscreen background video, a shiny gradient headline, a macOS-style menu bar, a realistic inbox mockup, and a custom "liquid-glass" card treatment.

\#\# Stack / setup

\- \`package.json\` dependencies: \`react\`, \`react-dom\`, \`@supabase/supabase-js\`, \`motion\` (v12+, import from \`motion/react\`), \`lucide-react\`.  
\- Tailwind config extends colors with \`brand: '\#3D81E3'\` and fontFamily sans with \`\['Inter','system-ui','sans-serif'\]\`.  
\- Font: Google Fonts Inter weights 400, 500, 600, 700, 800, 900\. Import in \`index.css\` via \`@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900\&display=swap');\`.  
\- \`html,body { font-family: 'Inter', system-ui, sans-serif; \-webkit-font-smoothing: antialiased; }\`.  
\- Background color base \`\#0c0c0c\`, text white, selection \`bg-brand/30\`.

\#\# Global background video (fixed, behind everything)

Inside the root wrapper (\`relative min-h-screen overflow-x-hidden bg-\[\#0c0c0c\] text-white\`), render a fixed full-screen video:

\`\`\`  
\<div className="fixed inset-0 z-0 pointer-events-none"\>  
  \<video autoPlay loop muted playsInline  
    className="w-full h-full object-cover pointer-events-none"  
    src="https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260508\_064122\_c4750c0e-7476-4b44-94a2-a85a65c63bf2.mp4" /\>  
\</div\>  
\`\`\`

Also render two hidden-on-mobile fixed vertical guide lines at the 36rem container edges:  
\`\`\`  
\<div className="hidden md:block pointer-events-none fixed inset-y-0 left-1/2 \-translate-x-\[calc(50%+36rem)\] w-px bg-white/10 z-\[5\]" /\>  
\<div className="hidden md:block pointer-events-none fixed inset-y-0 left-1/2 translate-x-\[calc(-50%+36rem)\] w-px bg-white/10 z-\[5\]" /\>  
\`\`\`

\#\# Global SVG noise filters (two, both id \`c3-noise\`)

\- One at root level (subtle grain, multiply blend) for the shiny headline.  
\- One inside the pricing section (fractal noise, overlay blend) for the watermark.

Root filter:  
\`\`\`  
\<filter id="c3-noise"\>  
  \<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" /\>  
  \<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.35 0" /\>  
  \<feComposite in2="SourceGraphic" operator="in" result="noise" /\>  
  \<feBlend in="SourceGraphic" in2="noise" mode="multiply" /\>  
\</filter\>  
\`\`\`

Pricing filter:  
\`\`\`  
\<filter id="c3-noise"\>  
  \<feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="2" stitchTiles="stitch" /\>  
  \<feComponentTransfer\>\<feFuncA type="linear" slope="0.075" /\>\</feComponentTransfer\>  
  \<feComposite in2="SourceGraphic" operator="in" result="noise" /\>  
  \<feBlend in="SourceGraphic" in2="noise" mode="overlay" /\>  
\</filter\>  
\`\`\`

\#\# Shared primitives

\*\*AppleLogo\*\* — inline SVG Apple mark, \`viewBox="0 0 384 512"\`, \`fill="currentColor"\`, default \`w-4 h-4\`. Path:  
\`M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z\`.

\*\*LogoMark\*\* — abstract 4-quadrant curve mark, \`viewBox="0 0 256 256"\`, default \`w-8 h-8\`, white fill. Path:  
\`M 0 128 C 70.692 128 128 185.308 128 256 L 64 256 C 64 220.654 35.346 192 0 192 Z M 256 192 C 220.654 192 192 220.654 192 256 L 128 256 C 128 185.308 185.308 128 256 128 Z M 128 0 C 128 70.692 70.692 128 0 128 L 0 64 C 35.346 64 64 35.346 64 0 Z M 192 0 C 192 35.346 220.654 64 256 64 L 256 128 C 185.308 128 128 70.692 128 0 Z\`.

\*\*AppleButton\*\* — rounded-full white pill, Apple logo \+ "Download Aura" label \+ ChevronRight. Chevron translates \`+1px\` on group hover. Classes: \`group inline-flex items-center justify-center gap-2 rounded-full bg-white text-black font-medium text-sm px-5 py-3 transition-all hover:bg-white/90 active:scale-\[0.98\]\`. Accepts \`label\` and \`full\` props.

\*\*SectionEyebrow\*\* — \`\<span className="w-1.5 h-1.5 rounded-full bg-white" /\>\` \+ label, optional tag pill with \`px-2 py-0.5 rounded-full border border-white/10 text-white/50\`.

\*\*gradientStyle\*\* used on the headline word "Revitalized":  
\`\`\`  
backgroundImage: 'linear-gradient(to right, \#091020 0%, \#0B2551 12.5%, \#A4F4FD 32.5%, \#00d2ff 50%, \#0B2551 67.5%, \#091020 87.5%, \#091020 100%)'  
backgroundSize: '200% auto'  
WebkitBackgroundClip: 'text' (+ backgroundClip text)  
color: 'transparent'; WebkitTextFillColor: 'transparent'  
filter: 'url(\#c3-noise)'  
\`\`\`

Shiny animation (\`.animate-shiny\`): 6s linear infinite, keyframes shiny \`{0%: background-position: \-200% center; 100%: 200% center;}\`.

\#\# Liquid-glass utility (used across cards)

\`\`\`  
.liquid-glass {  
  background: rgba(255,255,255,0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);  
  position: relative; overflow: hidden;  
}  
.liquid-glass::before {  
  content: ''; position: absolute; inset: 0; border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor; mask-composite: exclude;  
  pointer-events: none;  
}  
\`\`\`

\#\# Section 1 — Navbar

Max-width \`max-w-6xl mx-auto px-6\`. Motion nav fades/slides down (opacity 0 \-\> 1, y \-10 \-\> 0, 0.6s easeOut). Left: just the \`LogoMark\` (NO "Aura" word). Center (\`hidden md:flex gap-8\`): links \`\['Solutions','Pricing','Blog','Documentation','Careers'\]\` each \`text-white/70 text-sm font-medium hover:text-white\` with staggered y animation (delay 0.1 \+ i\*0.05). Right desktop: \`\<AppleButton /\>\` default label "Download Aura". Mobile right: \`w-10 h-10 rounded-full border border-white/10 bg-white/5\` Menu icon button.

\#\# Section 2 — Hero

Centered section, \`pt-16 md:pt-28 pb-20 text-center flex flex-col items-center\`.  
Motion h1 (delay 0.3, 0.8s cubic-bezier(.22,1,.36,1)), classes \`text-4xl md:text-7xl font-semibold tracking-tight leading-\[0.9\]\`:  
\- Line 1: "Your email." (white)  
\- Line 2: "Revitalized" — apply \`animate-shiny\` and the \`gradientStyle\` inline.

Then motion paragraph (delay 0.5): \`mt-8 text-white/60 max-w-md text-base leading-\[1.5\]\`:  
\> "Aura is the premier inbox platform for the current era. It leverages powerful AI to organize, prioritize, and refine your messages into total clarity."

Then motion div (delay 0.7) with \`\<AppleButton /\>\` and \`text-xs text-white/40\` "Download for Intel / Apple Silicon".

\#\# Section 3 — macOS menu bar strip

Full-width bar \`h-10 bg-black/40 backdrop-blur-md border-t border-b border-white/10\`. Inside \`max-w-6xl mx-auto px-6 h-full flex items-center justify-between text-xs\`. Left: \`AppleLogo w-3.5 h-3.5\`, bold white "Aura", then menu items \`\['File','Edit','View','Go','Window','Help'\]\` (progressive hiding: index\>2 \`hidden sm:inline\`, index\>3 \`hidden md:inline\`). Right: \`Search w-3.5 h-3.5\` \+ "Wed May 6 1:09 PM". Enters with delay 0.9.

\#\# Section 4 — Inbox mockup

\`max-w-6xl mx-auto px-6 py-16 md:py-24\`. Outer container \`relative rounded-2xl overflow-hidden border border-white/10 bg-\[\#0e1014\]/90 backdrop-blur-2xl\`. Motion enters from y:40 at delay 1.1.

Title bar: three traffic lights \`\#ff5f57\`, \`\#febc2e\`, \`\#28c840\` (each \`w-3 h-3 rounded-full\`); center label "Aura — Inbox" \`text-xs text-white/50\`.

Body \`grid grid-cols-12 h-\[520px\]\`:

\*\*Sidebar (col-span-3, border-r, bg-black/30, p-4):\*\*  
\- White "Compose with Aura" button with \`Sparkles\` icon (\`rounded-lg bg-white text-black text-xs font-semibold px-3 py-2\`).  
\- Nav items (icon \+ label \+ optional count): Inbox (12, active), Starred (3), Sent, Drafts (2), Archive, Trash. Active uses \`bg-white/10 text-white\`, others \`text-white/60 hover:bg-white/5\`.  
\- Labels section: uppercase tracking "Labels" small title, then 4 color dots: Work \`\#00d2ff\`, Personal \`\#A4F4FD\`, Travel \`\#f59e0b\`, Finance \`\#10b981\`.

\*\*Message list (col-span-4, border-r):\*\*  
\- Search header: \`Search\` icon \+ placeholder "Search mail".  
\- 6 messages with name, subject, preview, time, unread/active flags:  
  \- Linear — "Weekly product digest" — "Your team shipped 23 issues this week..." — 9:41 AM — unread \+ active  
  \- Sophia Chen — "Re: Q3 roadmap review" — "Thanks for sending the deck over. I had a few thoughts..." — 8:12 AM — unread  
  \- Figma — "Marcus commented on your file" — "Love the new direction on the landing hero." — Yesterday  
  \- Stripe — "Payout of $12,480.00 sent" — "Your payout is on its way to your bank..." — Yesterday  
  \- Vercel — "Deployment ready for aura-web" — "Preview is live at aura-web-g3f.vercel.app" — Mon  
  \- GitHub — "\[aura/core\] PR \#482 approved" — "david-lim approved your pull request." — Mon

\*\*Reader (col-span-5):\*\*  
\- Toolbar with Reply, Forward, Archive, Trash2 icon buttons (each \`w-7 h-7 rounded-md hover:bg-white/5\`) and a MoreHorizontal on the right.  
\- Header: "Weekly product digest"; sender avatar gradient bubble \`w-7 h-7 rounded-full bg-gradient-to-br from-\[\#00d2ff\] to-\[\#0B2551\]\` with "L"; "Linear" \+ "to me · 9:41 AM"; "Work" pill.  
\- Body:  
  \- Card with \`Sparkles\` icon (color \`\#A4F4FD\`) labeled "Summary by Aura" and text "Your team closed 23 issues, merged 14 PRs, and shipped 2 features. Top contributor: Marcus. No action needed."  
  \- Paragraphs: "Hi team,", "Here is your weekly digest of everything happening across your projects. This was a strong week with significant progress on the Q3 roadmap.", "Twenty-three issues were closed, fourteen pull requests were merged, and two customer-facing features went out. The velocity trend continues to climb.", "Let me know if you would like a deeper breakdown by project or contributor.", "— The Linear team" (\`text-white/50\`).  
  \- Attachment pill with \`Paperclip\` icon: "digest-may-6.pdf".

\#\# Section 5 — FeatureTriage

\`max-w-6xl mx-auto px-6 py-20 md:py-28\`, two-column grid \`grid md:grid-cols-2 gap-10 md:gap-16 items-start\`.

Left column motion (y 20 \-\> 0, 0.7s): \`SectionEyebrow label="Triage" tag="AI-native"\`, h2 \`mt-5 text-3xl md:text-5xl font-semibold tracking-tight leading-\[1.02\]\`: "Clear your inbox" \<br/\> "in a single pass.". Paragraph \`mt-6 text-white/60 text-base leading-\[1.6\] max-w-md\`: "Aura reads every message, understands intent, and routes the noise away from the signal. Focus on what moves your day forward — the rest handles itself." Chips row (\`text-xs text-white/70 px-3 py-1.5 rounded-full border border-white/10 bg-white/\[0.03\]\`): "Auto-categorize", "Snooze for later", "Silent newsletters", "One-tap unsubscribe".

Right column: \`liquid-glass rounded-2xl p-5\` card. Eyebrow text: "Today · 42 messages triaged". Four sub-cards (each \`liquid-glass rounded-lg p-3\`):  
\- Priority (4) \`\#ffffff\` — items: "Sophia Chen — Q3 review", "David Lim — contract signoff"  
\- Follow-up (7) \`\#e5e5e5\` — items: "Marcus — design review", "Figma — comment thread"  
\- Updates (18) \`\#a3a3a3\` — items: "Vercel — deploy ready", "GitHub — PR \#482 merged"  
\- Archived (13) \`\#525252\` — items: "Stripe payout · Newsletter · Receipts"

\#\# Section 6 — LogoCloud

\`max-w-6xl mx-auto px-6 py-16 md:py-20\`. Centered kicker \`text-xs uppercase tracking-widest text-white/40\`: "Trusted by the world's most thoughtful teams". Grid \`mt-10 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-6\`, each logo name as \`text-sm font-semibold tracking-tight text-white/50 hover:text-white\`. Names: Linear, Vercel, Figma, Stripe, Ramp, Notion, Loom, Arc. Each fades in with stagger 0.05.

\#\# Section 7 — Testimonials

\`max-w-6xl mx-auto px-6 py-20 md:py-28 border-t border-white/10\`. 3-col grid of \`liquid-glass rounded-2xl p-6\` figures. Each: blockquote \`text-sm text-white/80 leading-\[1.6\]\` wrapped in quotes, \`figcaption mt-6 pt-5 border-t border-white/10\` with name \`text-sm font-semibold\`, role \`text-xs text-white/50\`, company uppercased \`text-xs text-white font-semibold tracking-wide\`.  
\- "Aura gave our leadership team four hours of their week back. It reads like email from the future." — Parker Wilf, Group Product Manager, MERCURY  
\- "The command palette alone has changed how I process messages. I can't imagine going back to a traditional client." — Andrew von Rosenbach, Senior Engineering Program Manager, COHERE  
\- "Triage that actually understands context. Our team stopped dreading Monday morning inboxes." — Mathies Christensen, Engineering Manager, LUNAR

\#\# Section 8 — Pricing

Uses custom CSS classes (not Tailwind) for cinematic typography.

Outer \`\<section className="c3-pricing-section"\>\` with its own \`\<svg\>\` defining the \`c3-noise\` pricing filter described earlier.

Watermark (giant hero headline as backdrop):  
\`\`\`  
\<div className="c3-watermark-container"\>  
  \<div className="c3-watermark-main"\>  
    \<span className="c3-watermark-line-1"\>Your email.\</span\>  
    \<span className="c3-watermark-line-2"\>Revitalized\</span\>  
  \</div\>  
\</div\>  
\`\`\`

State: \`yearly\` boolean toggle. Three plans:  
\- \*\*Free\*\* — "Free" — "For creators taking their first steps with Forma." — Up to 3 projects in the cloud / Image export up to 1080p / Basic editing tools / Free templates and icons / Access via web and mobile app.  
\- \*\*Standard\*\* — monthly "$9,99/m" yearly "$99,99/y" — "For freelancers and small teams who need more freedom and flexibility." — Up to 50 projects in the cloud / Export up to 4K / Advanced editing toolkit / Team collaboration (up to 5 members) / Access to premium template library.  
\- \*\*Pro\*\* (\`c3-card-pro\`) — monthly "$19,99/m" yearly "$199,99/y" — "For studios, agencies, and professional creators working with brands." — Unlimited projects / Export up to 8K \+ animations / AI-powered content generation tools / Unlimited team members / Brand customization.

Each card renders: \`c3-tier-small\` (tier), \`c3-tier-large\` (price), \`c3-desc\`, \`c3-list\` of checkmark rows (white circle \`c3-check\` with white SVG check), \`c3-btn\` "Choose Plan".

Below: \`c3-toggle-wrap\` with "Yearly" label and a pill toggle (white knob black when off; when \`.active\`, background \`rgba(255,255,255,0.2)\`, knob white, translated 24px).

Pricing CSS (key values, include exactly):  
\- \`.c3-pricing-section { position: relative; padding: 40px 20px 80px; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }\`  
\- \`.c3-watermark-container { position: relative; width: 100%; max-width: 1100px; text-align: center; margin-top: 40px; z-index: 2; }\`  
\- \`.c3-watermark-main { font-size: 9rem; font-weight: 800; line-height: 0.9; letter-spacing: \-0.05em; filter: url(\#c3-noise); display: flex; flex-direction: column; align-items: center; }\`  
\- \`.c3-watermark-line-1 { color: \#fff; }\`  
\- \`.c3-watermark-line-2 { background: linear-gradient(to right, \#091020 0%, \#0B2551 25%, \#A4F4FD 65%, \#00d2ff 100%); \-webkit-background-clip: text; background-clip: text; color: transparent; \-webkit-text-fill-color: transparent; }\`  
\- \`.c3-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; width: 100%; max-width: 1100px; margin-top: 60px; transform: translateX(20px); position: relative; z-index: 3; }\`  
\- \`.c3-card { background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.4)); backdrop-filter: blur(14px) brightness(0.91); border: 1px solid rgba(255,255,255,1); border-radius: 44px; padding: 50px 24px; min-height: 580px; display: flex; flex-direction: column; transition: all 0.6s cubic-bezier(.22,1,.36,1); overflow: hidden; position: relative; }\`  
\- \`.c3-card::before { content:''; position:absolute; inset:0; border-radius:inherit; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 50%); pointer-events:none; }\`  
\- \`.c3-card:hover { background: rgba(15,15,15,0.6); border-color: rgba(34,211,238,0.7); transform: translateY(-12px) scale(1.01); }\`  
\- \`.c3-card-pro { background: linear-gradient(135deg, rgba(0,0,0,0.85), rgba(0,0,0,0.55)); }\`  
\- \`.c3-tier-small { font-size: 1.1rem; font-weight: 400; color: rgba(255,255,255,0.6); }\`  
\- \`.c3-tier-large { font-size: 2.8rem; font-weight: 500; letter-spacing: \-0.02em; color: \#fff; margin-top: 8px; }\`  
\- \`.c3-desc { font-size: 0.88rem; color: rgba(255,255,255,0.45); min-height: 3.2em; margin-top: 16px; margin-bottom: 40px; line-height: 1.5; }\`  
\- \`.c3-list li { display:flex; align-items:flex-start; gap: 14px; font-size: 0.92rem; color: rgba(255,255,255,0.8); margin-bottom: 18px; line-height: 1.4; }\`  
\- \`.c3-check { width:28px; height:28px; border-radius:50%; background: rgba(255,255,255,0.15); display:inline-flex; align-items:center; justify-content:center; flex-shrink:0; }\`  
\- \`.c3-btn { background:\#fff; color:\#000; padding: 10px 32px; border-radius: 100px; font-weight:600; font-size: 0.88rem; margin-top:auto; border:none; cursor:pointer; align-self:center; transition: all 0.3s cubic-bezier(.22,1,.36,1); }\`  
\- \`.c3-btn:hover { background:\#f5f5f5; transform:scale(1.02); box-shadow: 0 8px 24px rgba(255,255,255,0.15); }\`  
\- \`.c3-toggle-wrap { display:flex; align-items:center; justify-content:flex-end; gap:12px; width:100%; max-width:1100px; margin-top:32px; padding-right:20px; }\`  
\- \`.c3-toggle { width:52px; height:28px; background:\#fff; border-radius:100px; position:relative; cursor:pointer; border:none; transition: background 0.3s cubic-bezier(.4,0,.2,1); padding:0; }\`  
\- \`.c3-toggle-knob { width:20px; height:20px; background:\#000; border-radius:50%; position:absolute; top:4px; left:4px; transition: all 0.3s cubic-bezier(.4,0,.2,1); }\`  
\- \`.c3-toggle.active { background: rgba(255,255,255,0.2); }\`  
\- \`.c3-toggle.active .c3-toggle-knob { transform: translateX(24px); background:\#fff; }\`  
\- Media query \`(max-width:1024px)\`: \`.c3-watermark-main { font-size: 3.5rem; filter:none; }\`, \`.c3-watermark-line-2 { background:none; \-webkit-text-fill-color:\#00d2ff; color:\#00d2ff; }\`, \`.c3-grid\` becomes horizontal scroll-snap flex (\`display:flex; overflow-x:auto; scroll-snap-type:x mandatory; transform:none; width:100vw; padding:0 20px; gap:16px; scrollbar-width:none\`), cards \`flex: 0 0 320px; scroll-snap-align:center\`, \`.c3-grid::-webkit-scrollbar{display:none}\`, \`.c3-toggle-wrap { justify-content:center; padding-right:0; }\`.

\#\# Section 9 — FinalCTA

\`max-w-6xl mx-auto px-6 py-20 md:py-32\`. Motion \`liquid-glass relative overflow-hidden rounded-3xl px-8 py-16 md:py-24 text-center\`. Radial glow overlay: \`radial-gradient(600px circle at 50% 0%, rgba(255,255,255,0.15), transparent 70%)\` at opacity 0.3.  
\- h2 \`text-4xl md:text-6xl font-semibold tracking-tight leading-\[1.02\]\`: "Close the tabs." / "Open your day.".  
\- Paragraph \`mt-6 text-white/60 max-w-md mx-auto text-sm leading-\[1.6\]\`: "Join thousands of builders, founders, and operators who treat email like a tool — not an obligation."  
\- Buttons: \`\<AppleButton label="Download Aura" /\>\` and \`rounded-full border border-white/15 text-white text-sm font-medium px-5 py-3 hover:bg-white/5\` "Talk to sales" \+ ChevronRight.

Reproduce exactly — fonts, gradient stops, noise filters, copy strings, animation delays, and the CloudFront video URL \`https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260508\_064122\_c4750c0e-7476-4b44-94a2-a85a65c63bf2.mp4\`.

# Guia 40

Create a full-screen hero landing page for "Bloom" — an AI-powered plant/floral design platform. The design uses a liquid glass morphism aesthetic over a looping video background.

Background  
Full-screen autoplaying, looping, muted video background: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260315\_073750\_51473149-4350-4920-ae24-c8214286f323.mp4  
Video covers entire viewport with object-cover, sits at z-0. All content floats above at z-10.

Fonts  
Display/Body: Poppins (Google Fonts) — used for headings and body text  
Serif accent: Source Serif 4 (Google Fonts) — used only for italic/emphasis text inside headings (e.g., \<em\>, \<i\>, .italic inside h1-h3)  
Headings use font-weight: 500

Color Palette  
Strict grayscale only — all CSS variables are 0 0% X% HSL values  
Text is text-white, text-white/80, text-white/60, text-white/50 for hierarchy  
No colored accents whatsoever

Liquid Glass CSS (two tiers)  
Define under @layer components:

.liquid-glass (light)  
background: rgba(255,255,255,0.01);  
background-blend-mode: luminosity;  
backdrop-filter: blur(4px);  
border: none;  
box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);  
position: relative; overflow: hidden;  
::before pseudo-element: gradient border using linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, transparent 40%, transparent 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%) with padding: 1.4px, masked via \-webkit-mask-composite: xor; mask-composite: exclude;

.liquid-glass-strong (heavy, for CTA/panels)  
Same structure but backdrop-filter: blur(50px), box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15), and ::before uses 0.5/0.2 alpha instead of 0.45/0.15.

Layout — Two-Panel Split  
Flex row, min-h-screen. Left panel w-\[52%\], right panel w-\[48%\] (hidden on mobile lg:flex).

Left Panel  
Has a liquid-glass-strong overlay (absolute inset-4 lg:inset-6 rounded-3xl)  
Nav: Logo image (/logo.png, 32×32) \+ "bloom" text (semibold, 2xl, tracking-tighter, white) on left. "Menu" button with Menu icon on right, liquid-glass pill.  
Hero center (flex-1, centered):  
Logo image again (80×80)  
h1: "Innovating the / spirit of bloom AI" — text-6xl lg:text-7xl, tracking-\[-0.05em\], white. The italic part uses font-serif text-white/80  
CTA button: "Explore Now" with Download icon in a w-7 h-7 rounded-full bg-white/15 circle. Button is liquid-glass-strong, rounded-full, hover:scale-105 active:scale-95  
Three pills: "Artistic Gallery", "AI Generation", "3D Structures" — liquid-glass, rounded-full, text-xs text-white/80  
Bottom quote:  
"VISIONARY DESIGN" label (text-xs tracking-widest uppercase text-white/50)  
Quote: "We imagined a realm with no ending." — mixed font-display/font-serif italic spans  
Author: "MARCUS AURELIO" with horizontal lines on each side

Right Panel (desktop only)  
Top bar: Social icons (Twitter, LinkedIn, Instagram) in a liquid-glass pill with ArrowRight. Account button with Sparkles icon button, both liquid-glass.  
Community card: Small liquid-glass card (w-56), "Enter our ecosystem" title \+ description  
Bottom feature section (mt-auto): Outer liquid-glass container with rounded-\[2.5rem\]  
Two side-by-side cards: "Processing" (Wand2 icon) and "Growth Archive" (BookOpen icon), each liquid-glass rounded-3xl  
Bottom card: flower image thumbnail (from @/assets/hero-flowers.png, 96×64), "Advanced Plant Sculpting" title \+ description, and a "+" button. All liquid-glass.

Icons  
All from lucide-react: Sparkles, Download, Wand2, BookOpen, ArrowRight, Twitter, Linkedin, Instagram, Menu

Key Details  
All interactive elements: hover:scale-105 transition-transform  
Social icon links: text-white hover:text-white/80 transition-colors  
Icon containers: w-8 h-8 rounded-full bg-white/10 flex items-center justify-center  
No border classes anywhere — glass effect handles all borders via ::before  
border-radius token: \--radius: 1rem

# Guia 41

Build a "Core Features" marketing section as a single centered component with three gradient cards. Use the Inter font family (weights 400, 500, 600\) loaded from Google Fonts: \`https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600\&display=swap\`.

\*\*Page shell:\*\*  
\- Body: white background \`\#ffffff\`, 80px top/bottom \+ 20px left/right padding, flex centered, Inter font.  
\- Global reset: \`\* { box-sizing: border-box; margin: 0; padding: 0; }\`.

\*\*Container (\`.c1-container\`):\*\* max-width 1100px, full width, text-align center.

\*\*Header block:\*\*  
\- Badge (\`.c1-badge\`): text "Core Features", 0.75rem, weight 600, uppercase, letter-spacing 1px, gradient text using \`linear-gradient(90deg, \#F5C344, \#F28482, \#B567C2)\` with \`-webkit-background-clip: text\` and transparent fill. 16px bottom margin.  
\- Title (\`.c1-title\`): "Built for Speed & Quality", font-size 2.75rem, weight 500, color \`\#0f172a\`, letter-spacing \-0.02em, 12px bottom margin.  
\- Subtitle (\`.c1-subtitle\`): "Everything you need to go" \+ \`\<br\>\` \+ "from idea to image", 1.125rem, color \`\#64748b\`, line-height 1.5, 50px bottom margin.

\*\*Grid (\`.c1-grid\`):\*\* 3 equal columns, 24px gap. Breakpoints: 2 columns under 900px, 1 column under 600px (title scales to 2.25rem).

\*\*Card base (\`.c1-card\`):\*\* 20px border-radius, height 340px, flex column justify-end, relative, overflow hidden, text-align left, background \`\#F4F8F9\`, shadow \`0 10px 30px \-10px rgba(0,0,0,0.1)\`. Titles inside (\`h3\`): 1.05rem, weight 600, color \`\#1e293b\`, padding 24px, z-index 2\.

\*\*Card 1 — Smart Prompt Suggestions (\`.c1-card-1\`):\*\*  
\- Background: \`radial-gradient(circle at 50% 0%, \#FFB347 0%, \#F9ED96 30%, \#F4F8F9 60%, \#F4F8F9 100%)\`.  
\- Prompt box (white, 12px radius, 16px padding, 0.8rem text, color \`\#475569\`, line-height 1.6, shadow \`0 8px 20px rgba(0,0,0,0.04)\`), absolutely positioned top:30px/left:24px/right:24px. Text: "A bright, high-resolution 3D illustration of a \*\*cheerful cartoon\*\* of a \*\*girl character\*\* \*\*centred against a\*\* smooth blue background" — bold phrases have class \`.c1-blur-text\` with gradient \`linear-gradient(90deg, \#FFB347, \#E5A1F5)\` as clipped text, weight 600\.  
\- "Add more details" pill button: absolute top:180px/left:40px, white background, 1px solid black border, 5px 14px padding, 20px radius, 0.75rem text, weight 600, color \`\#1e293b\`, shadow \`0 4px 15px rgba(0,0,0,0.08)\`, includes \`✦\` character styled \`color: \#a855f7; font-size: 1rem\` with 6px gap.  
\- Cursor SVG arrow: absolute top:205px/left:110px, 24x24, fill \`\#0f172a\`, white stroke 1px, drop-shadow \`0 4px 6px rgba(0,0,0,0.2)\`, z-index 10\. Path: \`M4 2L20 11L11 13L9 22L4 2Z\`.  
\- Heading: "Smart Prompt Suggestions".

\*\*Card 2 — API Access (\`.c1-card-2\`):\*\*  
\- Background: \`radial-gradient(circle at 50% 0%, \#E5A1F5 0%, \#F8ACA0 30%, \#F4F8F9 60%, \#F4F8F9 100%)\`.  
\- \`.c1-api-visual\` absolutely positioned top:0/left:0/right:0/bottom:70px, flex centered, 24px horizontal padding.  
\- Image (\`.c1-network-img\`): width 100%, height 180px, object-fit contain, margin-top 20px. Source: \`https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/viktor/network.svg\`.  
\- Heading: "API Access".

\*\*Card 3 — Project Library (\`.c1-card-3\`):\*\*  
\- Background: \`radial-gradient(circle at 50% 0%, \#F9ED96 0%, \#E5A1F5 30%, \#F4F8F9 60%, \#F4F8F9 100%)\`.  
\- Mesh overlay (\`.c1-mesh\`): absolute inset 0, background image \= two linear gradients of \`rgba(255,255,255,0.8) 1px, transparent 1px\` (horizontal and 90deg vertical), background-size 16px 16px, masked with \`radial-gradient(circle at center top, black 0%, transparent 80%)\` (include \`-webkit-mask-image\`).  
\- Folder image (\`.c1-folder\`): absolute top:50px, horizontally centered via \`left:50%; transform:translateX(-50%)\`, width 170px, drop-shadow \`0 15px 25px rgba(0,0,0,0.08)\`. Source: \`https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/viktor/library%20icon.svg\`.  
\- Search pill (\`.c1-search\`): absolute top:220px, centered, white background, 1px solid black, 6px 18px padding, 20px radius, 0.75rem text weight 500 color \`\#1e293b\`, shadow \`0 8px 20px rgba(0,0,0,0.06)\`, white-space nowrap, 8px gap. Contains a 14x14 lucide-style search SVG (circle cx=11 cy=11 r=8, line 21,21→16.65,16.65, stroke \`\#64748b\`, stroke-width 2, round caps/joins) followed by text "Search in library".  
\- Heading: "Project Library".

\*\*Note:\*\* No animations are defined in this component — it is purely static styling. No JavaScript behavior, no hover effects. Use Supabase if any data persistence is needed, though this section requires none.

# Guia 42

Create a full-screen dark hero landing page for a security company called "SENTINEL AI" using React, Vite, TypeScript, Tailwind CSS, shadcn/ui, and an embedded Spline 3D scene as the background. The tech stack uses @splinetool/react-spline and @splinetool/runtime for the 3D embed. Here is every detail:

FONT:  
Google Fonts "Sora" with weights 300, 400, 500, 600, 700\. Load it in index.html:

\<link rel="preconnect" href="https://fonts.googleapis.com"\>  
\<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin\>  
\<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700\&display=swap" rel="stylesheet"\>  
Set font-sora as the body font via Tailwind config: fontFamily: { sora: \["Sora", "sans-serif"\] } and apply font-sora antialiased on body.

COLOR THEME (all HSL CSS custom properties, dark only, no light mode):

\--background: 0 0% 10% (dark charcoal)  
\--foreground: 0 0% 96% (near-white)  
\--primary: 119 99% 46% (vivid green)  
\--primary-foreground: 0 0% 4% (near-black)  
\--secondary: 0 0% 18%  
\--secondary-foreground: 0 0% 96%  
\--muted: 0 0% 16%  
\--muted-foreground: 0 0% 60%  
\--accent: 119 99% 46% (same vivid green as primary)  
\--accent-foreground: 0 0% 4%  
\--destructive: 0 84% 60%  
\--border: 0 0% 20%  
\--input: 0 0% 20%  
\--ring: 119 99% 46%  
\--radius: 0.5rem  
\--nav-button: 0 0% 18%  
\--hero-bg: 0 0% 8% (the darkest background, nearly black)  
Map these in Tailwind config using hsl(var(--variable)) pattern. Add custom color tokens: nav-button and hero-bg.

CUSTOM ANIMATIONS (Tailwind config keyframes \+ animation):

fade-up keyframe:

0%: opacity: 0, transform: translateY(20px), filter: blur(4px)  
100%: opacity: 1, transform: translateY(0), filter: blur(0)  
Animation: fade-up 0.7s cubic-bezier(0.16, 1, 0.3, 1\) forwards  
fade-in keyframe:

0%: opacity: 0  
100%: opacity: 1  
Animation: fade-in 0.5s ease-out forwards  
NAVBAR (fixed, transparent, floating over the Spline scene):

fixed top-0 left-0 right-0 z-50, horizontal flex, justify-between, padding px-8 lg:px-16 py-5  
Left: Logo text "SENTINEL" \-- text-foreground text-xl font-semibold tracking-tight  
Center: Nav links array: \["Services", "About Us", "Projects", "Team", "Contacts"\] \-- each is text-sm text-muted-foreground hover:text-foreground transition-colors uppercase tracking-widest. Links use href={\#section-name}. Hidden on mobile (hidden md:flex), with gap-8.  
Right: "Get Quote" button using shadcn Button with a custom navCta variant: text-foreground bg-nav-button hover:bg-nav-button/80 active:scale-\[0.97\] transition-all. Size lg, with classes hidden md:inline-flex rounded-lg uppercase text-xs tracking-widest px-6.  
HERO SECTION (full-screen, content at bottom-left):

Structure:

Outer \<section\>: relative min-h-screen flex items-end bg-hero-bg overflow-hidden  
Spline 3D Background (absolute, full-size): Lazy-loaded via React.lazy(() \=\> import("@splinetool/react-spline")) wrapped in \<Suspense\> with a fallback \<div className="absolute inset-0 bg-hero-bg" /\>. The Spline component uses scene="https://prod.spline.design/Slk6b8kz3LRlKiyk/scene.splinecode" and className="w-full h-full". Placed inside \<div className="absolute inset-0"\>.  
Dark overlay: \<div className="absolute inset-0 bg-black/30 z-\[1\] pointer-events-none" /\>  
Content container: relative z-10 pointer-events-none w-full max-w-\[90%\] sm:max-w-md lg:max-w-2xl px-6 md:px-10 pb-10 md:pb-10 pt-32  
Content elements (all with staggered animate-fade-up, starting opacity-0):

Heading (delay 0.2s): \<h1\> with text "SENTINEL" in white \+ " AI" in primary green. Classes: text-\[clamp(3rem,8vw,6rem)\] font-bold leading-\[1.05\] tracking-\[-0.05em\] text-foreground mb-2 md:mb-4 uppercase. The "AI" part is wrapped in \<span className="text-primary"\>.

Subheading (delay 0.4s): \<p\> \-- "We implement security correctly." \-- text-foreground/80 text-\[clamp(1.125rem,2.5vw,1.875rem)\] font-light mb-3 md:mb-6

Description (delay 0.55s): \<p\> \-- "Enterprise security systems built in days. AI-powered surveillance deployed with zero-trust architecture. Smart access control set up for your entire facility. All of it done right, not just fast." \-- text-muted-foreground text-\[clamp(0.875rem,1.5vw,1.25rem)\] font-light mb-4 md:mb-8

Two CTA buttons (delay 0.7s): Wrapped in flex flex-wrap gap-3 font-bold. Both are plain \<button\> elements (not shadcn Button) with pointer-events-auto (to re-enable clicks since parent is pointer-events-none):

"Book a Call": bg-primary text-primary-foreground px-6 py-3 md:px-8 md:py-4 text-sm rounded-sm cursor-pointer hover:brightness-110 transition-all active:scale-\[0.97\]  
"Our Work": bg-white text-background px-6 py-3 md:px-8 md:py-4 text-sm rounded-sm cursor-pointer hover:brightness-90 transition-all active:scale-\[0.97\]  
Trust line (delay 0.85s): \<p\> \-- "Trusted security partner. Columbus, OH. 12 systems deployed." \-- text-muted-foreground/60 text-xs font-light mt-4 md:mt-6

All animated elements use style={{ animationDelay: "Xs" }} for the stagger, combined with the opacity-0 animate-fade-up classes.

PAGE WRAPPER (Index.tsx):  
Simple wrapper: \<div className="bg-hero-bg min-h-screen"\> containing \<Navbar /\> and \<HeroSection /\>.

KEY DEPENDENCIES:

@splinetool/react-spline and @splinetool/runtime for the 3D Spline embed  
tailwindcss-animate plugin  
shadcn/ui Button component with custom variants (navCta, hero, heroOutline)  
class-variance-authority for button variants  
IMPORTANT NOTES:

The Spline scene URL is https://prod.spline.design/Slk6b8kz3LRlKiyk/scene.splinecode \-- this is the exact 3D scene used  
The entire content area has pointer-events-none so clicks pass through to the Spline scene, but buttons re-enable with pointer-events-auto  
Responsive fluid typography uses clamp() for the heading, subheading, and description  
The content is anchored to the bottom-left of the viewport (flex items-end on the section \+ padding-bottom on the content)  
No hamburger menu on mobile \-- the nav links and CTA simply hide (hidden md:flex / hidden md:inline-flex)

# Guia 43

# Guia 44

Build a modern, high-performance landing page section using React, TypeScript, Tailwind CSS v4, and Motion. The application should match the following exact specifications:  
1\. Dependencies & Setup  
Libraries: Install lucide-react, motion, clsx, and tailwind-merge.  
Fonts & CSS: In index.css, import the Inter and Outfit fonts from Google Fonts: @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700\&family=Outfit:wght@400;500;600\&display=swap');  
Configure the Tailwind theme in your CSS to use Inter as \--font-sans and Outfit as \--font-display.  
The global body background should be \#f9fafb.  
2\. Main Hero Container & Video Background  
Create a hero section container with these exact classes: relative w-full max-w-\[1400px\] mx-auto rounded-\[48px\] bg-white border border-slate-200/50 shadow-\[0\_40px\_100px\_-20px\_rgba(0,0,0,0.03)\] overflow-hidden h-\[600px\] flex flex-col.  
Inside, add an absolutely positioned underlying layer (absolute inset-0 pointer-events-none z-0 overflow-hidden select-none) for the background video.  
The video tag must point to exactly this URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260505\_101331\_74f9b798-3f00-4e86-8a01-377aa16ffeaa.mp4. It must include autoPlay, loop, muted, and playsInline attributes, with the classes: w-full h-full object-cover scale-105 transition-transform duration-1000. No overlays.  
3\. Hero Text Content  
Create a content wrapper positioned relative (z-20 flex-1 px-8 md:px-16 pt-12 md:pt-16 flex flex-col items-start).  
Use motion.div from motion/react to animate the text layer in (fade in, slide up slightly).  
Headline: "Foundation of the\<br /\>new digital epoch". Should use the font-display font, sizes text-\[42px\] md:text-\[56px\], medium weight, tight tracking, color \#0a1b33.  
Subheadline: "Designing products, powering ecosystems and laying the foundation of a decentralized web for enterprises, builders and communities alike." Should use font-sans, sizes text-\[14px\] md:text-\[15px\], color \#64748b.  
Contact Button: Text "Contact Us", using a dark background (bg-\[\#0a152d\]), white text, rounded-full, with hover scale animations via motion.button.  
4\. Floating Bottom Navbar  
Create an absolutely positioned navbar wrapper at the bottom center of the hero: absolute bottom-10 left-1/2 \-translate-x-1/2 z-30.  
The nav element should use motion.nav to fade in and slide up (delayed after the text). It must have the classes: flex items-center bg-white/90 backdrop-blur-2xl px-1.5 py-1.5 rounded-full shadow-\[0\_12px\_40px\_rgba(0,0,0,0.08)\] border border-slate-200/40.  
Nav Elements:  
A small circular logo placeholder on the left (w-9 h-9 bg-white border-slate-100 shadow-sm) containing the star character "✦".  
Two standard text buttons: "Products" and "Docs" (text-\[12px\] font-semibold text-slate-500 hover:text-\[\#0a1b33\]).  
A "Get in touch" button on the right containing the text and a small ChevronRight (from lucide-react). Styled identically to the marquee cards: bg-white px-5 py-2 rounded-full text-\[12px\] font-semibold text-\[\#0a1b33\] border border-slate-200/60 shadow-sm hover:border-slate-300 transition-all.  
5\. Seamless Marquee Logo Scroller Component  
Below the hero container (mt-10), add a custom highly-performant Marquee Scroller component.  
The scroller must use a pure CSS @keyframes animation (transform: translateX(0) to translateX(-50%)) for infinite scrolling, pausing on hover. It needs a left/right masking gradient (maskImage linear-gradient fading to transparent on the edges). No title or description text above the scroller.  
The Logos List: Supply an array of 8 objects with src URLs from svgl.app, alt names, and hex gradient objects:  
Procure (procure.svg, blue gradient)  
Shopify (shopify.svg, yellow gradient)  
Blender (blender.svg, blue gradient)  
Figma (figma.svg, purple gradient)  
Spotify (spotify.svg, pink/red gradient)  
Lottielab (lottielab.svg, yellow/green)  
Google Cloud (google-cloud.svg, light blue)  
Bing (bing.svg, cyan/teal)  
Render the list twice inline to ensure a seamless loop.  
Card Design: Make each logo's container card exactly match the "Get in touch" navbar button's styling. The container classes must be exactly: group relative h-24 w-40 shrink-0 flex items-center justify-center rounded-full bg-white border border-slate-200/60 shadow-sm hover:border-slate-300 transition-all overflow-hidden.  
Inside the card, add an absolute div using the specific gradient colors, scaled at 1.5 and 0 opacity, which drops to scale 1 and opacity 100 on group-hover.  
The image tag should invert/turn black on hover (group-hover:brightness-0 group-hover:invert).

# Guia 45

Build a premium, fintech-style landing page for a stablecoin product called "Halo / USD Halo" using React \+ TypeScript \+ Vite \+ Tailwind CSS, with lucide-react for icons. No other UI libraries. Background color of the page is \#F5F5F5.

Global Setup  
Use TT Norms Pro as the primary font, loaded via @font-face from /fonts/tt-norms-pro-regular.woff2 (weight 400\) and /fonts/tt-norms-pro-semibold.woff2 (weight 600), with font-display: swap. Apply it to html, body, and inherit on \*.  
Tailwind base \+ components \+ utilities at the top of src/index.css.  
Page wrapper: flex flex-col bg-\[\#F5F5F5\]. The first section (Navbar \+ Hero) is wrapped in a h-screen flex flex-col overflow-hidden container.  
Inner content max width across sections: max-w-\[88rem\] mx-auto.  
Custom Logo Icon  
Create an SVG component LogoIcon using currentColor, viewBox 0 0 256 256, with this path (a stylized "halo" mark made of two interlocking rounded squares):

M 128.005 191.173 C 128.448 156.208 156.93 128 192 128 L 192 64 L 128 64 C 128 99.346 99.346 128 64 128 L 64 192 L 128 192 Z M 192 256 L 64 256 C 28.654 256 0 227.346 0 192 L 0 64 L 64 64 L 64 0 L 192 0 C 227.346 0 256 28.654 256 64 L 256 192 L 192 192 Z  
1\. Navbar (absolute, transparent over hero)  
nav is absolute top-0 left-0 right-0 z-20 px-6 py-5.  
Inner row: flex items-center justify-between.  
Left: LogoIcon (w-7 h-7, black) \+ word "Halo" (text-2xl font-medium tracking-tight text-black).  
Center (hidden below md): links Network · Ecosystem · Rewards · Help · News, gap-8, text-base text-gray-700 hover:text-black font-medium transition-colors duration-200.  
Right: black pill button "Open Wallet" — bg-black text-white text-base font-medium px-7 py-2.5 rounded-full hover:bg-gray-800 transition-colors duration-200.  
2\. Hero Section  
Outer: flex-1 px-6 pt-20 pb-6 flex items-end.  
Inner card: relative w-full rounded-2xl overflow-hidden, inline style height: calc(100vh \- 96px).  
Background video (autoplay, muted, loop, playsInline, object-cover absolute inset-0 w-full h-full):   
https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260423\_161253\_c72b1869-400f-45ed-ac0c-52f68c2ed5bd.mp4

Content overlay: relative z-10 flex flex-col items-start justify-start h-full p-12 pt-36.  
h1: "Your Wealth\\nWorks" (with \<br/\>) — text-black text-5xl md:text-6xl font-medium leading-tight max-w-xl mb-4, inline letterSpacing: '-0.04em'.  
p: "An automated, reward-powered digital dollar built for native passive earnings and effortless connection into DeFi." — text-black/70 text-base md:text-lg max-w-md mb-8 leading-relaxed, inline fontFamily: "'Inter', ui-sans-serif, system-ui, sans-serif".  
Pill button "Join us" with arrow circle: inline-flex items-center gap-3 bg-black text-white text-base md:text-lg font-medium pl-8 pr-2 py-2 rounded-full hover:bg-gray-800. Trailing arrow inside bg-white rounded-full p-2, using ArrowRight w-5 h-5 text-black from lucide-react.  
Followed by the Brand Marquee below.  
Brand Marquee (inside hero, below button)  
Container: mt-24 w-full max-w-md overflow-hidden.  
Inject scoped \<style\> with keyframes marquee translating 0 → \-50%, applied to .marquee-track { display:flex; width:max-content; animation: marquee 22s linear infinite; }.  
Render the brand list twice (so it loops seamlessly).  
Each item: mx-7 shrink-0 text-black/60 whitespace-nowrap with these inline styles:  
Stripe — Georgia serif, weight 700, letterSpacing \-0.02em, fontSize 15px  
Coinbase — Arial sans, weight 900, letterSpacing 0.08em, fontSize 13px, uppercase  
Uniswap — Trebuchet MS, weight 600, letterSpacing 0.01em, fontSize 15px, italic  
Aave — Courier New monospace, weight 700, letterSpacing 0.12em, fontSize 13px, uppercase  
Compound — Palatino, Book Antiqua, weight 400, letterSpacing \-0.01em, fontSize 16px  
MakerDAO — Impact, Arial Narrow, weight 400, letterSpacing 0.04em, fontSize 14px  
Chainlink — Verdana, weight 700, letterSpacing \-0.03em, fontSize 13px  
3\. Info Section ("Meet USD Halo.")  
section bg-\[\#F5F5F5\] px-6 py-24.  
Row 1: 2-col grid (grid-cols-1 md:grid-cols-2 gap-12 mb-16 items-start).  
Left: h2 "Meet USD Halo." — text-black text-4xl md:text-5xl font-medium leading-tight mb-8, letterSpacing \-0.03em. Below it, black pill "Discover it" button with white arrow circle (same pattern as "Join us" but text-base).  
Right: paragraph "USD Halo is a reward-earning dollar coin that lets your savings grow while remaining tied to the U.S. dollar." — text-black/70 text-2xl md:text-3xl leading-relaxed.  
Row 2 — 4-col card grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4):  
Card 1 (spans 2 cols on lg): rounded-2xl with background image:   
https://images.higgs.ai/?default=1\&output=webp\&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser\_38xzZboKViGWJOttwIXH07lWA1P%2Fhf\_20260423\_164207\_f243351d-ed59-48ec-83a0-a5e996bdbe3c.png\&w=1280\&q=85

 backgroundSize: cover; backgroundPosition: center. Inside: p-7 min-h-80 flex flex-col justify-between. Title (top): "Savings that bloom" — text-black text-2xl font-medium leading-snug letterSpacing \-0.02em. Body (bottom): "Gain steady returns as your dollar tokens are routed into top-performing DeFi strategies." — text-black/70 text-base max-w-xs.  
Card 2: solid \#2B2644, rounded-2xl, p-7, min-h-80, flex-col-justify-between. White heading "Always fluid,\\nalways pegged." text-2xl font-medium, body "Keep fully dollar-anchored with on-demand access to funds — no lockups or waits." text-white/60 text-base.  
Card 3: same \#2B2644 styling. Heading "Fully\\nautomated". Body "Skip the task of tuning positions yourself. USD Halo runs in the background for you."  
4\. Backed By Section (marquee row)  
section bg-\[\#F5F5F5\] px-6 with inner max-w-\[88rem\] mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 items-center.  
Left col (1/4): text-black/70 text-base leading-relaxed — "Funded by premier partners\\nand forward-thinking leaders."  
Right col (3/4): infinite marquee (same pattern as hero marquee but 30s linear infinite, class .backers-track, keyframes backers-marquee). Items use mx-10 shrink-0 text-black/50 whitespace-nowrap with these inline styles:  
Fundamental Labs — Times New Roman serif, 400, ls 0.02em, 14px  
KUCOIN — Arial Black, 900, ls 0.08em, 16px  
NGC — Impact, 700, ls 0.05em, 18px  
NxGen — Georgia, 600, ls \-0.02em, 17px  
Matter Labs — Helvetica, 700, ls \-0.01em, 15px  
DEXTools — Verdana, 700, ls 0.06em, 14px, uppercase  
NGRAVE — Courier New, 700, ls 0.18em, 14px  
Polychain — Palatino, 500, ls 0.03em, 15px  
Render brands twice for the loop.  
5\. Use Cases Section  
section bg-\[\#F5F5F5\] px-6 py-24. Inner: 2-col grid grid-cols-1 md:grid-cols-2 gap-8 items-start.  
Left column (md:pr-12 md:pt-2):  
Eyebrow: "USD Halo in Practice" — text-black/60 text-sm mb-2.  
h2 "Use modes" — text-5xl md:text-6xl font-medium leading-none mb-6, ls \-0.04em.  
Paragraph: "USD Halo powers a wide range of modes for builders, companies and treasuries wanting safe and rewarding stablecoin integrations plus more" — text-black/60 text-base leading-relaxed max-w-sm.  
Right column: large relative rounded-3xl overflow-hidden min-h-\[720px\] with background video (autoplay/muted/loop/playsInline, object-cover absolute inset-0):   
https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260423\_183428\_ab5e672a-f608-4dcb-b319-f3e040f02e2d.mp4

Overlay content relative z-10 p-10 md:p-12:  
h3 "Commerce" — text-4xl md:text-5xl font-medium leading-tight mb-5, ls \-0.03em.  
Paragraph: "Lift customer retention by offering USD Halo, a trusted dollar-backed stablecoin with strong yields, letting your patrons earn with zero effort on your platform." — text-black/70 text-base max-w-md mb-8.  
Inline-flex link "Know more" with leading circular icon: w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center group-hover:bg-white transition-colors containing ArrowRight w-4 h-4 text-black.  
Animations & Interactions  
Two CSS keyframe marquees (22s for hero brands, 30s for backers), both translating 0 → \-50% on a duplicated track for seamless looping.  
All buttons use transition-colors duration-200 with hover state hover:bg-gray-800 (or hover:bg-white for the white circle).  
Nav links transition on hover from text-gray-700 to text-black.  
Videos autoplay muted with playsInline for mobile compatibility.  
Composition  
App renders, in order:

h-screen overflow-hidden wrapper containing Navbar (absolute) \+ HeroSection.  
InfoSection  
BackedBySection  
UseCasesSection  
All section backgrounds are \#F5F5F5. All headings use negative letter-spacing for the tight, modern fintech feel. Use font-medium (600) as the heaviest weight throughout.

# Guia 46

Create a "Stellar.ai" landing page hero section using React, Tailwind CSS, and Lucide React icons. Use the Inter font (imported from Google Fonts). The page has a white background (bg-white), max-width max-w-7xl, and is centered with mx-auto.

Font: Import Inter (weights 400, 500, 600, 700\) from Google Fonts. Set font-family: 'Inter', sans-serif on the body.

Custom CSS animations (in index.css):

@keyframes fadeInUp \-- from opacity: 0; transform: translateY(30px) to opacity: 1; transform: translateY(0). Class .animate-fade-in-up uses this with 0.6s ease-out forwards.  
@keyframes fadeInOverlay \-- from opacity: 0 to opacity: 1\. Class .animate-fade-in-overlay uses this with 0.4s ease-out forwards.  
@keyframes fadeInDialog \-- from opacity: 0 to opacity: 1\. Class .animate-slide-up-overlay uses this with 0.5s ease-out forwards and has transform: translate(-50%, \-50%).  
Every major section uses .animate-fade-in-up with staggered animationDelay inline styles (starting at 0.1s and incrementing by 0.1s). Each element starts with opacity: 0 inline so the animation fills it to visible.

Tailwind config: Default config with no custom theme extensions. Uses standard content paths.

NAVIGATION (animationDelay: 0.1s):  
px-6 py-4 flex items-center justify-between max-w-7xl mx-auto  
Left: Lucide Star icon (w-5 h-5, fill-black) \+ "Stellar.ai" text (text-lg font-semibold)  
Center (hidden on mobile, hidden md:flex items-center gap-8): "Solutions" with ChevronDown, "For Teams" with ChevronDown, "About Us", "Learn Hub" \-- all text-sm text-gray-700 hover:text-black  
Right: "Login" link (text-sm text-gray-700) \+ "Get started free" button (bg-black text-white px-5 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors)

HERO SECTION (px-6 pt-24 pb-32 max-w-7xl mx-auto text-center):  
Reviews Badge (delay: 0.2s): inline-flex items-center gap-2 mb-8. Contains a bordered square (w-6 h-6 border border-gray-300 rounded) with a filled Star icon inside, plus "4.9 rating from 18.3K+ users" (text-sm font-medium text-black).

Main Heading (delay: 0.3s): text-6xl md:text-7xl lg:text-\[80px\] font-normal leading-\[1.1\] tracking-tight mb-5. First line: "Work Smarter. Move Faster." Second line: "AI Powers You Up." with gradient text (bg-gradient-to-r from-black via-gray-500 to-gray-400 bg-clip-text text-transparent).

Subheading (delay: 0.4s): text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto. Text: "Intelligent automation syncs with the tools you love to streamline tasks, boost output, and save time."

CTA Button (delay: 0.5s): bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors mb-12. Text: "Begin Free Trial".

Tab Bar (delay: 0.6s): Centered bg-gray-100 rounded-lg p-1 container.  
Mobile (md:hidden): 2x2 grid with 4 buttons: Analyse (BarChart3), Train (BookOpen), Testing (Users), Deploy (Rocket). Active: bg-white text-black shadow-sm. Inactive: text-gray-600.  
Desktop (hidden md:flex): Same 4 buttons in row with vertical dividers (w-px h-5 bg-gray-300).  
Tabs auto-cycle every 4s using setInterval. State: useState('analyse').

Video \+ Overlay Section (delay: 0.7s):  
Container: relative rounded-3xl overflow-hidden h-\[400px\] md:h-\[500px\]  
Video: src="https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260319\_165750\_358b1e72-c921-48b7-aaac-f200994f32fb.mp4", autoPlay, loop, muted, playsInline, w-full h-full object-cover.

4 Conditional Overlays per tab with animate-fade-in-overlay outer and animate-slide-up-overlay inner card:  
a. Analyse: "Set Up Your AI Workspace" wizard with purple progress bar at 25%, 4 steps  
b. Train: "AI Model Training" with orange progress at 67%, 4 metrics  
c. Testing: "Test Suite Results" with green success, 127/127 tests  
d. Deploy: "Deploy to Production" with 4 checklist items, Deploy Now button

Company Logos (delay: 0.8s): mt-24 flex with INTERSCOPE, SPOTIFY, Nexera (dot grid), M3 (serif italic), LAURA COLE (LC circle), vertex (dots)

# Guia 47

Create a dark landing page for "Neuralyn" — an analytics dashboard SaaS. Use React \+ Vite \+ Tailwind CSS \+ TypeScript \+ Framer Motion \+ shadcn/ui.

Fonts  
Inter (400, 500, 600, 700\) for body/UI via @fontsource/inter  
Instrument Serif (400, 400-italic) for the italic accent word via @fontsource/instrument-serif

Color Theme (all HSL, dark mode by default in :root)  
Background: 0 0% 0% (pure black)  
Foreground: 0 0% 100% (pure white)  
Muted foreground: 0 0% 65%  
Card: 0 0% 5%  
Border: 0 0% 20%  
Hero subtitle: 210 17% 95%

Page Structure  
Section 1: Hero (full viewport height, overflow-hidden)

Navbar — horizontal, padded px-8 md:px-28 py-4:

Left: Logo image \+ "Neuralyn" text (text-xl font-bold tracking-tight) \+ nav links (Home, Services with ChevronDown icon, Reviews, Contact us) — links hidden on mobile, gap-1 between links, gap-12 md:gap-20 between logo and links  
Right: "Sign In" button — solid white background (bg-foreground), black text (text-background), rounded-lg text-sm font-semibold, hover opacity transition

Hero Content — centered column, mt-16 md:mt-20 px-4:

Tag pill: A "liquid glass" styled pill (liquid-glass class) with inner "New" badge (white bg, black text, rounded-md text-sm font-medium px-2 py-0.5) \+ "Say Hello to Corewave v3.2" in text-sm font-medium text-muted-foreground. Pill has px-3 py-2 rounded-lg mb-6.  
Title: text-5xl md:text-7xl, tracking-\[-2px\], font-medium, leading-tight md:leading-\[1.15\] mb-3. Text: "Your Insights." / "One Clear Overview." — the word "Overview" is in Instrument Serif italic (font-serif italic font-normal)  
Subtitle: text-lg font-normal leading-6 opacity-90 mb-8, color uses CSS variable \--hero-subtitle. Text: "Neuralyn helps teams track metrics, goals, and progress with precision." with a \<br/\> after "goals,"  
CTA Button: "Get Started for Free" — solid white (bg-foreground text-background), rounded-full px-8 py-3.5 text-base font-medium, whileHover: scale 1.03, whileTap: scale 0.98

Dashboard \+ Video Area — full viewport width using w-screen with marginLeft: calc(-50vw \+ 50%) trick, aspect-ratio: 16/9, positioned relative:

Background video: \<video\>, absolutely positioned inset-0 w-full h-full object-cover. URL: https://d8j0ntlcm91z4.cloudfront.net/user\_38xzZboKViGWJOttwIXH07lWA1P/hf\_20260307\_083826\_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4  
Dashboard image: Absolutely positioned, centered, max-w-5xl w-\[90%\] rounded-2xl, mixBlendMode: "luminosity". Has parallax scroll (y: 0→-250).  
Bottom gradient fade: Absolutely positioned at bottom of section, h-40, gradient from background to transparent, z-30, pointer-events-none.

Parallax Scroll Effects (Framer Motion useScroll({ target: sectionRef, offset: \["start start", "end start"\] }) \+ useTransform):

Hero text content group: y: \[0, \-200\] and opacity: \[1, 0\] (fades over first 50% of scroll)  
Dashboard image: y: \[0, \-250\]

Entrance Animations: Staggered initial={{ opacity: 0, y }} / animate={{ opacity: 1, y: 0 }}:

Tag pill: y: 10, duration 0.5s, delay 0  
Title: y: 20, duration 0.6s, delay 0.1  
Subtitle: y: 20, duration 0.6s, delay 0.2  
CTA: y: 20, duration 0.6s, delay 0.3  
Dashboard area: y: 40, duration 0.8s, delay 0.4

Liquid Glass CSS

.liquid-glass {  
  background: rgba(255, 255, 255, 0.01);  
  background-blend-mode: luminosity;  
  backdrop-filter: blur(4px);  
  \-webkit-backdrop-filter: blur(4px);  
  border: none;  
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);  
  position: relative;  
  overflow: hidden;  
}  
.liquid-glass::before {  
  content: '';  
  position: absolute;  
  inset: 0;  
  border-radius: inherit;  
  padding: 1.4px;  
  background: linear-gradient(180deg,  
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,  
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,  
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);  
  \-webkit-mask: linear-gradient(\#fff 0 0\) content-box, linear-gradient(\#fff 0 0);  
  \-webkit-mask-composite: xor;  
  mask-composite: exclude;  
  pointer-events: none;  
}

Section 2: Testimonial (min-h-screen, centered, py-24 md:py-32 px-8 md:px-28)

Quote symbol image (w-14 h-10 object-contain)  
Testimonial text (text-4xl md:text-5xl font-medium leading-\[1.2\], wrapped in flex flex-wrap): "Neuralyn revolutionized how we handle financial insights using smart analytics. We are now driving better outcomes quicker than we ever imagined\! Neuralyn revolutionized how we handle financial insights using smart analytics."  
Scroll-driven word reveal: Each word is a \<motion.span\> with mr-\[0.3em\]. Uses useScroll({ target: containerRef, offset: \["start end", "end center"\] }). Each word maps to a sequential range \[i/total, (i+1)/total\] → opacity: \[0.2, 1\] and color: \["hsl(0 0% 35%)", "hsl(0 0% 100%)"\].  
Closing " quotation mark in text-muted-foreground ml-2  
Author row (flex items-center gap-4): Avatar image (w-14 h-14 rounded-full border-\[3px\] border-foreground object-cover) \+ name "Brooklyn Simmons" (text-base font-semibold leading-7 text-foreground) \+ role "Product Manager" (text-sm font-normal leading-5 text-muted-foreground)  
Layout: max-w-3xl mx-auto, content left-aligned (items-start), gap-10 between elements

Assets needed:  
logo.png — small logo icon  
hero-dashboard.png — dashboard screenshot  
quote-symbol.png — decorative quote mark  
testimonial-avatar.png — circular headshot

# Guia 48

Create a dark mode hero section for an AI website builder with the following exact specifications:

\#\# Technical Setup

\#\#\# Required Packages  
Install these packages:  
\- \`motion\` (version 12.23.24 or later) \- for animations  
\- \`hls.js\` (version 1.6.15 or later) \- for video streaming  
\- \`lucide-react\` (version 0.487.0 or later) \- for icons

\#\#\# Fonts  
Import these Google Fonts:  
\`\`\`css  
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700\&family=Instrument+Serif:ital@0;1\&display=swap');  
\`\`\`

\#\# Layout Structure

\#\#\# Navbar Component  
Create a fixed, transparent navbar with:

\*\*Position & Styling:\*\*  
\- Fixed to top, full width, z-index 50  
\- Background: fully transparent (bg-transparent)  
\- Padding: px-6 py-4  
\- Flexbox layout: items-center justify-between

\*\*Left Section:\*\*  
\- Sunburst icon (24x24px SVG) in white color

\*\*Center Section\*\* (hidden on mobile, visible md:flex):  
\- Navigation links: "Products" (with ChevronDown icon), "Customer Stories", "Resources", "Pricing"  
\- Font: Instrument Sans, text-sm, font-medium  
\- Color: text-white/80, hover:text-white  
\- Gap: gap-8

\*\*Right Section:\*\*  
\- "Book A Demo" link (hidden on small screens, sm:block)  
\- "Get Started" button: white background, black text, rounded-full, px-5 py-2.5, font-semibold

\#\#\# Hero Section Component

\*\*Container:\*\*  
\- Relative positioning, full width, min-h-screen  
\- Background color: \#000000 (pure black)  
\- Text color: white  
\- Overflow hidden

\*\*Background Video Layer:\*\*  
\- Video URL: https://stream.mux.com/T6oQJQ02cQ6N01TR6iHwZkKFkbepS34dkkIc9iukgy400g.m3u8  
\- Video implementation using HLS.js with Safari fallback  
\- Video properties: muted, loop, playsInline  
\- Object-fit: cover, opacity: 60%  
\- Poster image fallback: https://images.unsplash.com/photo-1647356191320-d7a1f80ca777?crop=entropy\&cs=tinysrgb\&fit=max\&fm=jpg\&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhYnN0cmFjdCUyMGRhcmslMjB0ZWNobm9sb2d5JTIwbmV1cmFsJTIwbmV0d29ya3xlbnwxfHx8fDE3Njg5NzIyNTV8MA\&ixlib=rb-4.1.0\&q=80\&w=1080

\*\*Video Overlay:\*\*  
\- Black overlay: bg-black/60 with backdrop-blur-\[2px\]

\*\*Decorative Gradients:\*\*  
\- Top-left gradient: position top-\[-20%\] left-\[20%\], size 600x600px, bg-blue-900/20, blur-\[120px\], mix-blend-screen  
\- Bottom-right gradient: position bottom-\[-10%\] right-\[20%\], size 500x500px, bg-indigo-900/20, blur-\[120px\], mix-blend-screen

\*\*Content Container:\*\*  
\- Max-width: 5xl (max-w-5xl)  
\- Center aligned (mx-auto, items-center, text-center)  
\- Z-index: 10, top margin: mt-20  
\- Vertical spacing: space-y-12

\*\*Pre-headline:\*\*  
\- Text: "Design at the speed of thought"  
\- Font: Instrument Serif  
\- Size: text-3xl (mobile), sm:text-5xl, lg:text-\[48px\]  
\- Line height: leading-\[1.1\]  
\- Color: white  
\- Animation: Motion fade up (opacity 0→1, y 20→0, duration 0.6s)

\*\*Main Headline:\*\*  
\- Text: "Build Faster"  
\- Font: Instrument Sans, font-semibold  
\- Size: text-6xl (mobile), sm:text-8xl, lg:text-\[136px\]  
\- Line height: leading-\[0.9\], letter spacing: tracking-tighter  
\- Gradient: bg-gradient-to-b from-white via-white to-\[\#b4c0ff\]  
\- Text effect: bg-clip-text text-transparent  
\- Animation: Motion scale (opacity 0→1, scale 0.9→1, delay 0.2s, duration 0.6s)

\*\*Subheadline:\*\*  
\- Text: "Create fully functional, SEO-optimized websites in seconds with our advanced AI engine."  
\- Font: Instrument Sans  
\- Size: text-lg (mobile), sm:text-\[20px\]  
\- Line height: leading-\[1.65\]  
\- Color: white, opacity-70  
\- Max width: max-w-xl  
\- Animation: Motion fade (opacity 0→0.7, delay 0.4s, duration 0.6s)

\*\*CTA Buttons:\*\*

Primary Button:  
\- Style: White pill-shaped with blue arrow  
\- Layout: pl-6 pr-2 py-2, rounded-full  
\- Background: white  
\- Text: "Start Building Free" (font-medium, text-lg, Instrument Sans, color \#0a0400)  
\- Arrow container: 40x40px circle, bg-\[\#3054ff\], hover:bg-\[\#2040e0\]  
\- Icon: ArrowRight (lucide-react), white, 20x20px  
\- Hover effect: shadow-\[0\_0\_20px\_rgba(255,255,255,0.3)\], scale-105

Secondary Button:  
\- Text: "See Examples"  
\- Style: text link with arrow  
\- Color: text-white/70, hover:text-white  
\- Background: backdrop-blur-sm, hover:bg-white/5  
\- Padding: px-4 py-2, rounded-lg  
\- Icon: ArrowRight with group-hover:translate-x-1 transition

Button Container:  
\- Layout: flex-col (mobile), sm:flex-row  
\- Gap: gap-6, items centered  
\- Animation: Motion fade up (opacity 0→1, y 20→0, delay 0.6s, duration 0.5s)

\#\# HLS.js Video Implementation  
\`\`\`tsx  
import { useEffect, useRef } from "react";  
import Hls from "hls.js";

const videoRef \= useRef\<HTMLVideoElement\>(null);  
const videoSrc \= "https://stream.mux.com/T6oQJQ02cQ6N01TR6iHwZkKFkbepS34dkkIc9iukgy400g.m3u8";

useEffect(() \=\> {  
  const video \= videoRef.current;  
  if (\!video) return;

  if (Hls.isSupported()) {  
    const hls \= new Hls();  
    hls.loadSource(videoSrc);  
    hls.attachMedia(video);  
    hls.on(Hls.Events.MANIFEST\_PARSED, () \=\> {  
      video.play().catch((e) \=\> console.log("Auto-play prevented:", e));  
    });  
    return () \=\> {  
      hls.destroy();  
    };  
  } else if (video.canPlayType("application/vnd.apple.mpegurl")) {  
    video.src \= videoSrc;  
    video.addEventListener("loadedmetadata", () \=\> {  
      video.play().catch((e) \=\> console.log("Auto-play prevented:", e));  
    });  
  }  
}, \[\]);  
\`\`\`

\#\# Motion Animations  
Import: \`import { motion } from "motion/react"\`

\- Pre-headline: initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}  
\- Main headline: initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2, duration: 0.6 }}  
\- Subheadline: initial={{ opacity: 0 }} animate={{ opacity: 0.7 }} transition={{ delay: 0.4, duration: 0.6 }}  
\- Buttons: initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6, duration: 0.5 }}

\#\# Color Palette  
\- Background: \#000000  
\- Primary text: white  
\- Secondary text: white/80, white/70  
\- Primary button background: white  
\- Primary button text: \#0a0400  
\- Primary button accent: \#3054ff, hover \#2040e0  
\- Gradient end color: \#b4c0ff  
\- Decorative gradients: blue-900/20, indigo-900/20

# Guia 49

Build a 404 "Page Not Found" hero page as a single full-viewport (100vh, no scroll) React \+ Vite \+ Tailwind CSS application using the DM Sans font and Google Material Symbols Rounded icons. The page must match the following specification exactly:

\---

\#\# Fonts & External Resources

\- \*\*Google Font:\*\* DM Sans (all weights, variable: \`opsz 9..40, wght 100..1000\`)  
\- \*\*Google Material Symbols Rounded:\*\* \`opsz,wght,FILL,GRAD@24,400,1,0\`  
\- \*\*Logo image:\*\* \`https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/Tests/logoipsum-415.svg\` (rendered with \`filter: brightness(0)\` to make it black, height 28px)  
\- \*\*Background spaceship image:\*\* \`https://pub-e68758f43067417dba612b2371819aa1.r2.dev/viktor-components/alien-spaceship.png\`

\---

\#\# Layout

The entire page is exactly \`100vh\` with \`overflow: hidden\` on html, body, and \`\#root\`. No scrolling. The body uses \`display: flex; flex-direction: column\`. The \`\#root\` div also uses \`height: 100vh; display: flex; flex-direction: column; overflow: hidden\`.

\---

\#\# Background

Body has a layered background:  
1\. The spaceship PNG centered at \`center 40%\`, sized with \`background-size: contain\`  
2\. A \`linear-gradient(to top left, \#F5F5F5, \#F7F7F7)\` covering the full page

Both are \`background-attachment: fixed\` and \`no-repeat\`.

\---

\#\# Color Variables (CSS custom properties)

\`\`\`  
\--text-main: \#1a1a1a  
\--text-secondary: \#888888  
\--bg-page: \#F5F5F5  
\--card-bg: \#ffffff  
\`\`\`

\---

\#\# Navbar

\- Max-width \`1100px\`, centered, padding \`28px 40px\`  
\- Has a dashed bottom border made with \`background-image: linear-gradient(to right, rgba(0,0,0,0.08) 2px, transparent 2px); background-size: 6px 1px\` on a \`::after\` pseudo-element  
\- \*\*Left:\*\* Logo (the SVG image \+ the text "nexto." in 20px bold, \-0.3px letter-spacing, color \#111, flex with 9px gap)  
\- \*\*Center:\*\* Nav links ("Our Team", "Solutions" with a dropdown arrow character, "Showcase", "News") \- 14px, weight 400, opacity 0.65, hover to opacity 1, gap 36px  
\- \*\*Right:\*\* CTA button "Let's Connect" \- dark gradient button (\`linear-gradient(180deg, \#2c2c2c 0%, \#111111 100%)\`), white text 13px weight 500, border-radius 40px, padding \`5px 16px 5px 5px\`. Has a white circular arrow icon (24px circle) on the LEFT side with a chevron SVG inside. Box-shadow \`0 4px 15px rgba(0,0,0,0.15)\`. On hover: translateY(-1px), stronger shadow, brightness(1.1).  
\- \*\*Hamburger (mobile only):\*\* 3 spans, 24px wide, 2px height, animates to X when active. Hidden on desktop, shown on mobile (\`display: flex\` at max-width 768px).

\---

\#\# Mobile Navigation

\- Fixed full-screen overlay, slides in from right with \`transform: translateX(100%)\` \-\> \`translateX(0)\`, cubic-bezier(0.77, 0, 0.175, 1\) transition  
\- On mobile: left-aligned, large links (38px, weight 800, letter-spacing \-1.5px), each with bottom border, padding 24px 0  
\- Last link is the CTA button styled same as navbar but with 32px arrow circle

\---

\#\# Main Content Area

\- \`flex: 1\`, centered both ways (\`align-items: center; justify-content: center\`), max-width 700px, padding \`20px 20px 30px\`  
\- \*\*Lost text:\*\* "Seems you've wandered off..." \- 15px, color \`--text-secondary\`, weight 400, margin-bottom 12px  
\- \*\*Title wrapper:\*\* \`position: relative; display: inline-block; margin-bottom: 14px\`  
  \- \*\*Cloud decoration:\*\* Material Symbols "cloud" icon, positioned \`top: \-18px; left: \-24px\`, font-size 42px, with gradient text fill (\`linear-gradient(to bottom, \#F7B2FB 50%, \#786EF1 80%, \#5588FB 100%)\` using \`-webkit-background-clip: text; \-webkit-text-fill-color: transparent\`), white drop-shadow outline, \`floatSlow\` animation (5s, 0.3s delay)  
  \- \*\*Heart decoration:\*\* Material Symbols "favorite" icon, positioned \`bottom: \-15px; right: 20px\`, font-size 32px, same gradient fill, white drop-shadow outline, \`floatSlow\` animation (4.5s, 1s delay)  
  \- \*\*Title:\*\* "Whoops\! Nothing here yet" \- \`font-size: clamp(34px, 5vw, 52px)\`, weight 500, letter-spacing \-1.5px, line-height 1.08, color \#0f0f0f  
\- \*\*Subtext:\*\* "Grab a 30-minute \`chat\` to explore your ideas, scope, and vision. We'll find common ground, sync and \`define\` a clear roadmap." \- 14px, color \`--text-secondary\`, line-height 1.7, max-width 470px, margin-bottom 28px. The words "chat" and "define" are in highlighted tags (inline-flex, background \#E0E2E7, 12.5px, weight 600, padding 2px 12px, border-radius 6px)

\---

\#\# Navigation Cards

\- Flex column, gap 12px, max-width 460px, positioned at bottom with \`margin-top: auto\`  
\- \*\*Card 1 "Main Page":\*\* House SVG icon (path: \`M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H5a1 1 0 01-1-1V9.5z\` with door \`M9 21V12h6v9\` in white). Subtitle: "Back where it all begins..."  
\- \*\*Card 2 "Showcase":\*\* Circle-dot SVG icon (circle r=9 filled, inner circle r=3.5 white). Subtitle: "Where we walk the walk"  
\- Each card: white background, border-radius 18px, padding 18px 22px, flex between, 1px border rgba(0,0,0,0.05), shadow \`0 2px 12px rgba(0,0,0,0.04)\`. On hover: translateY(-3px), shadow \`0 8px 28px rgba(0,0,0,0.08)\`.  
\- Icon container: 48px circle, background \#eaecf0, scales 1.05 on card hover  
\- Right chevron arrow (rsaquo character, 21px), translateX(6px) on hover  
\- Card title: 15px weight 600, subtitle: 12px color \`--text-secondary\`

\---

\#\# Animations

\`\`\`css  
@keyframes floatSlow {  
  0%, 100% { transform: translateY(0px) rotate(0deg); }  
  50% { transform: translateY(-10px) rotate(3deg); }  
}  
\`\`\`

\---

\#\# Responsive Breakpoints

\*\*768px and below:\*\*  
\- Hide nav-links and desktop CTA button, show hamburger  
\- Background-size: 90%, position: center 45%  
\- Navbar padding: 20px  
\- Title: 30px, decorations smaller  
\- Cards: full width, gap 10px, smaller padding/icons

\*\*480px and below:\*\*  
\- Title: 26px  
\- Background-size: 100%  
\- Decorations even smaller

\---

# Guia 50

Fonts  
Primary font: 'Nunito' from Google Fonts (weights: 400, 500, 600, 700, 800, 900\)  
Display/heading font: 'Feather Bold' from https://db.onlinewebfonts.com/c/14936bb7a4b6575fd2eee80a3ab52cc2?family=Feather+Bold  
Font stack fallback: 'Nunito', 'DIN Round Pro', \-apple-system, BlinkMacSystemFont, sans-serif  
Color Variables (CSS custom properties)

\--green: rgb(88, 204, 2\)  
\--green-hover: rgb(75, 178, 0\)  
\--green-shadow: \#61B800  
\--dark-blue: rgb(16, 15, 62\)  
\--blue: rgb(28, 176, 246\)  
\--gray-text: rgb(75, 75, 75\)  
\--gray-light: rgb(119, 119, 119\)  
\--border-color: rgb(229, 229, 229\)  
\--nav-text: rgb(175, 175, 175\)  
\--footer-green: \#4EC604  
\--red: \#FF4B4B  
\--orange: \#FF9600  
\--golden: \#FFC800  
Structure & Layout  
Fixed Navbar (64px height, white background, bottom border)  
Left side: Duolingo logo image (https://d35aaqx5ub95lt.cloudfront.net/images/splash/f92d5f2f7d56636846861c458c0d0b6c.svg, 140x33px), followed by a 1px vertical divider (24px tall), then "STYLE GUIDE" label (11px, uppercase, letter-spacing 1.5px, gray)  
Right side: Horizontal nav links \- "Colors", "Type", "Buttons", "Cards", "Components" (13px, bold, uppercase, 0.5px letter-spacing, gray, with green hover/active states and subtle green background on hover)  
Max-width: 1440px, centered  
Hero Section (centered, green-to-white gradient background)  
Headline: "duolingo design" in Feather Bold font, 52px, green color (\#58CC02), lowercase  
Description: "A comprehensive visual reference for the Duolingo design system covering colors, typography, button variants, cards, and UI components." \-- 17px, gray-light color, max-width 520px, 1.5 line-height  
Two buttons below: Primary "GET STARTED" button (green, white text, 12px border-radius, 4px green box-shadow for 3D effect, uppercase bold) and Secondary "I ALREADY HAVE AN ACCOUNT" button (transparent with 2px gray border, blue text, 4px gray box-shadow for 3D effect)  
Both buttons: 48px height, 24px horizontal padding, 15px font-size, 700 weight, uppercase  
Buttons have active state: box-shadow removed, translateY(4px)  
Padding: 56px top, 40px sides, 40px bottom  
Main Grid (2-column grid, no gap, max-width 1440px)  
Each panel has 36px vertical and 40px horizontal padding, bottom border and right border (border-color). Even panels have no right border.

Each panel has a section label: 11px, 800 weight, uppercase, 2px letter-spacing, gray (nav-text), with a 1px line extending to the right via ::after pseudo-element.

Panels in order (left-to-right, top-to-bottom):

Panel 1: Color Palette (light)  
Grid of 12 color swatches, grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)), 12px gap. Each swatch:

Square (aspect-ratio: 1), 12px border-radius, 1px border rgba(0,0,0,0.06)  
Hover: scale(1.05) with box-shadow 0 8px 24px rgba(0,0,0,0.12)  
Below swatch: name (12px, bold, gray-text) and hex value (10px, gray-light, semi-bold)  
Colors in order:

Green \-- rgb(88, 204, 2\) \-- \#58CC02  
Green Hover \-- rgb(75, 178, 0\) \-- \#4BB200  
Blue \-- rgb(28, 176, 246\) \-- \#1CB0F6  
Dark Blue \-- rgb(16, 15, 62\) \-- \#100F3E  
Red \-- \#FF4B4B  
Orange \-- \#FF9600  
Golden \-- \#FFC800  
Footer Green \-- \#4EC604  
Gray Text \-- rgb(75, 75, 75\) \-- \#4B4B4B  
Gray Light \-- rgb(119, 119, 119\) \-- \#777777  
Nav Text \-- rgb(175, 175, 175\) \-- \#AFAFAF  
Border \-- rgb(229, 229, 229\) \-- \#E5E5E5  
Panel 2: Typography (light)  
Vertical stack with 20px gap. Each row is a flex row (baseline-aligned, 20px gap) with a meta column (80px wide, right-aligned) showing size in blue (11px bold) and weight label below (10px, nav-text color), then the sample text.

Rows:

48px / Feather Bold \-- "Display" \-- green color, Feather Bold font  
32px / Bold 700 \-- "Heading One" \-- gray-text color  
28px / Feather Bold \-- "heading two" (lowercase) \-- green color, Feather Bold font  
18px / Medium 500 \-- "Body text for paragraphs and descriptions with comfortable reading line-height." \-- gray-light color, 1.6 line-height  
14px / Bold 700 \-- "CAPTION LABEL" \-- uppercase, nav-text color, 0.5px letter-spacing  
12px / Semi 600 \-- "Small utility text for metadata and hints" \-- gray-light color  
Panel 3: Button Variants (light)  
Vertical stack with 16px gap. Each row has an 80px label (10px, bold, uppercase, 1px letter-spacing, nav-text) then buttons with 12px gap, flex-wrap.

Rows:

"Primary" \-- 3 buttons: "GET STARTED" (green bg, white text, 4px green shadow), "SMALL" (same but 36px height, 13px font, 16px padding, 10px radius, 3px shadow), "DISABLED" (same as primary but opacity 0.45, pointer-events none)  
"Secondary" \-- 3 buttons: "LEARN MORE" (transparent, 2px \#CFCFCF border, blue text, 4px \#CFCFCF shadow), "SMALL" (same sizing as small primary), "DISABLED" (opacity 0.45)  
"Danger" \-- 2 buttons: "DELETE" (\#FF4B4B bg, white text, 4px \#CC3C3C shadow), "REMOVE" (small variant)  
"Ghost" \-- 1 button: "VIEW ALL" (no bg/border/shadow, green text, green bg on hover at 0.08 opacity)  
Panel 4: Dark Theme Buttons (dark-blue background)  
Section label and ::after line use white at 35% and 10% opacity respectively.

Two rows:

"GET STARTED" primary \+ "TRY 1 WEEK FREE" (white bg, dark-blue text, 4px \#88879F shadow, hover bg \#c8f040)  
Small variants of both  
Panel 5: Cards (light)  
2-column grid, 16px gap. Each card: white bg, 2px border (border-color), 16px border-radius. Hover: translateY(-4px), box-shadow 0 12px 32px rgba(0,0,0,0.08).

Card 1:

Image: https://images.pexels.com/photos/4145354/pexels-photo-4145354.jpeg?auto=compress\&cs=tinysrgb\&w=400\&h=200\&fit=crop (120px height, cover)  
Tag: "NEW" (green text, green bg at 10% opacity, 11px, 800 weight, uppercase, 6px radius, 3px/8px padding)  
Title: "Spanish for Beginners" (16px, bold, gray-text)  
Description: "Start your language journey with interactive lessons designed to build fluency." (13px, gray-light, 1.5 line-height)  
Footer (12px top border, 12px/16px padding): left "12 UNITS" (12px bold uppercase nav-text), right "START" (12px bold uppercase blue, hover opacity 0.7)  
Card 2:

Image: https://images.pexels.com/photos/267669/pexels-photo-267669.jpeg?auto=compress\&cs=tinysrgb\&w=400\&h=200\&fit=crop  
Tag: "POPULAR" (blue text, blue bg at 10% opacity)  
Title: "French Conversations"  
Description: "Practice real-world dialogue and improve pronunciation with native speakers."  
Footer: "8 UNITS" / "CONTINUE"  
Panel 6: Dark Theme Cards (dark-blue background)  
2-column grid, same structure but no images. Cards have bg rgba(255,255,255,0.06), border rgba(255,255,255,0.08). Titles are white, descriptions are white at 50% opacity, footer border is white at 8% opacity, footer text is white at 30% opacity.

Card 1:

Tag: "SUPER" (golden \#FFC800 text, golden bg at 15% opacity)  
Title: "Unlimited Hearts"  
Desc: "Keep learning without interruption with Super Duolingo benefits."  
Footer: "PREMIUM" / "UPGRADE"  
Card 2:

Tag: "PRO" (orange \#FF9600 text, orange bg at 15% opacity)  
Title: "Mastery Quizzes"  
Desc: "Challenge yourself with advanced assessments to test your skill level."  
Footer: "ADVANCED" / "TRY NOW"  
Panel 7: Components (light)  
Vertical stack with 20px gap. Each group has a label (10px bold uppercase, 1px letter-spacing, nav-text).

Badges: Flex row, 8px gap. Pill-shaped badges (4px/10px padding, 20px radius, 12px bold uppercase):

"COMPLETED" (green text, green bg 12%)  
"IN PROGRESS" (blue text, blue bg 12%)  
"FAILED" (red text, red bg 12%)  
"STREAK" (orange text, orange bg 12%)  
"PREMIUM" (golden-brown \#b8920f text, golden bg 15%)  
Input \+ Button: Flex row, 12px gap. Input (flex:1, 48px height, 16px padding, 2px border border-color, 12px radius, 15px font, 600 weight, focus border turns blue, placeholder is nav-text color 500 weight) \+ Primary "SUBSCRIBE" button.

Toggle: Flex row with two toggle switches. Each toggle is 48x28px. Track is border-color bg, 14px radius. Thumb is 22x22px white circle, 3px from edges, with 1px 3px rgba(0,0,0,0.15) shadow. Checked state: track turns green, thumb translates 20px right. Labels "Sound effects" and "Animations" (14px, 600 weight). First toggle is checked by default.

Progress: 3 progress bars in a column, 10px gap. Each row: flex, 12px gap, bar (flex:1, 12px height, border-color bg, 6px radius, overflow hidden), fill (6px radius, 0.6s ease width transition), value (12px bold, 32px wide, right-aligned).

85% green fill  
60% blue fill  
35% orange fill  
Tooltips & Streak: Flex row, 16px gap, center-aligned.

Tooltip trigger: "Hover me" (13px, bold, green text, green bg 8%, 8px/16px padding, 8px radius). On hover shows tooltip bubble above (dark-blue bg, white 12px 600-weight text, 6px/12px padding, 8px radius, 5px triangle arrow pointing down via ::after border trick).  
Streak counter: Inline-flex, 6px gap, 6px/14px padding, orange bg 10%, 20px radius. Fire emoji (18px) \+ "42" (16px, 800 weight, orange).  
Panel 8: Dark Theme Components (dark-blue background)  
Labels use white at 30% opacity.

Language Pills: Flex row, 8px gap. Each pill: inline-flex, 6px gap, 6px/12px padding, 2px border, 12px radius, cursor pointer, hover turns border green with subtle green bg.

"Spanish" (ACTIVE \-- green border, green bg 8%, white text) with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/59a90a2cedd48b751a8fd22014768fd7.svg  
"French" (inactive \-- white border 12%, white text 70%) with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/482fda142ee4abd728ebf4ccce5d3307.svg  
"German" with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/c71db846ffab7e0a74bc6971e34ad82e.svg  
"Japanese" with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/edea4fa18ff3e7d8c0282de3f102aaed.svg  
Flag images: 24x18px, object-fit contain. Pill text: 13px, bold.  
Avatar Group: Flex row with overlapping circular avatars (36px, 50% radius, 2px white border, \-8px margin-left except first). Images:

https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress\&cs=tinysrgb\&w=80\&h=80\&fit=crop  
https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress\&cs=tinysrgb\&w=80\&h=80\&fit=crop  
https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg?auto=compress\&cs=tinysrgb\&w=80\&h=80\&fit=crop  
Count badge "+5" (same 36px circle, \#f0f0f0 bg, 11px 800 weight, gray-light)  
Text next to group: "8 learners active" (13px, 600 weight, white 50% opacity)  
Progress (Dark): 2 bars, track bg is white 8%, values are white 60%:

72% golden fill  
45% green fill  
Badges (Dark):

"MASTERED" (green bg 15%, \#7ADB2E text)  
"REVIEW" (blue bg 15%, \#4DC4F8 text)  
"CROWN" (golden bg 15%, \#FFC800 text)  
Responsive Breakpoints  
900px and below:

Grid becomes single column, no right borders  
Hero h1: 36px  
Nav links hidden  
Cards grid becomes single column  
Hero buttons stack vertically, max-width 280px  
600px and below:

Hero padding: 40px 20px 32px  
Hero h1: 28px  
Panel padding: 28px 20px  
Color grid: 3 columns  
Type meta column: hidden  
Display type: 32px  
Button labels: hidden  
Input row: column direction

