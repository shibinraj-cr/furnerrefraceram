# Furner RefraCeram — Marketing Website

Pure-static, six-page marketing site for **Furner RefraCeram Private Limited**, a Kerala-based manufacturer of industrial refractory, abrasive, and chemical materials.

No build step. No framework. Just HTML, CSS, and a small vanilla-JS file. Open `index.html` in any modern browser and the site runs.

---

## Stack

- **HTML5** — semantic, one `<h1>` per page
- **Modern CSS** — custom properties, grid, flexbox, container-aware typography
- **Vanilla JS** — IntersectionObserver scroll reveals, mobile menu with focus trap, hero spark particles, dropdown, smooth scroll
- **Google Fonts** — Fraunces (display serif w/ italic), Manrope (body), JetBrains Mono (specs)
- **OpenStreetMap** — embedded location iframe on contact page
- Form submits via `mailto:` to `business@furner.in`

---

## Run locally

```sh
open index.html              # macOS — opens default browser
xdg-open index.html          # Linux
start index.html             # Windows
```

That's it. Everything is relative paths under `assets/`. The site fully works from `file://`.

If you'd rather serve over HTTP (recommended for testing the OSM iframe and to avoid any browser CORS oddities):

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

---

## File structure

```
.
├── index.html            Homepage
├── abrasives.html        9 product sections + spec sidebars
├── refractory.html       4 products + application matrix
├── chemicals.html        3 oxalate products + lab capability strip
├── about.html            Story + 4 values
├── contact.html          Info card (Registered Office) + form + map
├── consultation.html     Industrial-minerals advisory landing page
├── paver-chemco.html     Construction-chemicals division landing
├── README.md
├── .gitignore
└── assets/
    ├── styles.css        Full design system + responsive
    ├── main.js           All interactive behaviour
    ├── logo.png          Optimised from FRC_logo.png (~50 KB)
    ├── favicon.ico, favicon-16/32/64.png
    └── img/              Hero / atmospheric placeholders + product photos
        ├── _placeholders/  Backed-up procedural placeholders (reversible swap)
        └── paver/        Paver Chemco logos + product photography
```

### Multi-site positioning

The site reads as a multi-location Indian manufacturer (no Kerala / Mele Pattambi positioning). The footer bottom-bar on every page reads "Multiple production locations across India". The original registered office address is preserved on the contact page only, under a "Registered Office" label, alongside the OpenStreetMap iframe.

### Consultation page

`consultation.html` is a dedicated industrial-minerals advisory landing page covering specification, sourcing, refractory lining design, QC system design, and failure-mode analysis. It links from a top-level "Consultation" nav item on every page (between Materials and About) and from the Company column in every footer.

### Paver Chemco division

The Paver Chemco division has its own dedicated brand site at [paverchemco.in](https://www.paverchemco.in). The `paver-chemco.html` page on this Furner site introduces the division at a brand level, lists its six core products with images sourced directly from the live brand site, and links out to paverchemco.in for full product detail, the coverage calculator, the product selector, and dealer-locator information. Logo and product imagery in `assets/img/paver/` are downloaded copies of the originals from the Paver Chemco site — re-fetch from `https://www.paverchemco.in/images/products/*.jpg` if you need to refresh.

A `_gen_images.py` helper script is included at the project root — it generated the on-brand placeholder images. You can re-run it (`python3 _gen_images.py`, requires `pillow`) or delete it; it is not referenced by the site.

---

## ⚠️ About the imagery

The site uses two imagery sources at the moment:

1. **Product close-ups (12 files) and `lab-qc.jpg`** are placeholder visuals at `assets/img/prod-*.jpg` and `assets/img/lab-qc.jpg`. The original procedural placeholders are preserved at `assets/img/_placeholders/` so any swap is reversible. **Replace with owned, licensed, or commissioned photography before public launch.**
2. **Hero, atmospheric, category, facility, and texture images (~10 files)** are still **procedurally generated, on-brand placeholders** — gradients, scattered grain shapes, brick patterns. These should be replaced with real photography or AI-generated images for production launch.

The Paver Chemco product images at `assets/img/paver/` are downloaded copies from the Paver Chemco brand site (sister-brand context). Confirm rights before public launch as above.

**To replace any image:** drop a new file at the same path, keeping the filename and aspect ratio. The HTML picks it up with no code changes.

Recommended generation prompts (use Midjourney, DALL-E 3, Flux, or your tool of choice). All should be photorealistic, editorial-grade, dramatic side lighting, warm tungsten/ember highlights against cool charcoal shadows, no people, no text, no logos.

| File | Aspect | Prompt |
| :--- | :--- | :--- |
| `hero-crucible.jpg` | 16:10 | Macro photograph of molten alumina inside an industrial electric arc furnace, glowing orange-white core, dark refractory walls, sparks rising, dramatic chiaroscuro, shot on Phase One, ultra-detailed, cinematic |
| `hero-grain-macro.jpg` | 16:10 | Extreme macro of brown fused alumina abrasive grains scattered on matte black surface, individual angular crystals visible, copper and amber tones catching warm light, shallow DOF, editorial product photography |
| `texture-refractory.jpg` | 16:9 | Close-up of fired refractory brick surface, tabular alumina texture, off-white with subtle iron-oxide flecks, raking light revealing crystalline structure, museum-quality detail |
| `texture-chemicals.jpg` | 16:9 | Pristine white crystalline oxalic acid powder in laboratory glass beaker, soft northern window light, scientific glassware in soft focus background, clean editorial style |
| `prod-brown-alumina.jpg` | 4:5 | Macro of brown fused alumina grains piled on dark slate, rich chocolate-brown angular crystals with metallic sheen, single light source from upper left, fine art still life |
| `prod-white-alumina.jpg` | 4:5 | Macro of white fused alumina grains, pure snow-white crystalline aggregate on charcoal background, side-lit revealing sharp crystal facets, museum lighting |
| `prod-pink-alumina.jpg` | 4:5 | Macro of pink fused alumina grains, soft rose-pink crystalline material with chromium tint, on matte black, warm directional lighting, editorial |
| `prod-ruby-alumina.jpg` | 4:5 | Macro of ruby fused alumina grains, deep crimson-red abrasive crystals, jewel-like quality, single warm spotlight on charcoal slate |
| `prod-black-sic.jpg` | 4:5 | Macro of black silicon carbide grains, glittering anthracite-black crystals with iridescent peacock highlights, dramatic raking light, hyperreal detail |
| `prod-green-sic.jpg` | 4:5 | Macro of green silicon carbide grains, vivid emerald-green crystalline aggregate with metallic luster, on dark surface, side lighting |
| `prod-zirconia.jpg` | 4:5 | Macro of zirconia alumina abrasive grains, mottled grey-white-cream blend, angular fused crystals, editorial product photography |
| `prod-garnet.jpg` | 4:5 | Macro of natural garnet abrasive sand, deep burgundy and rust-red rounded grains, on matte black, warm window light |
| `prod-glass-bead.jpg` | 4:5 | Macro of clear glass beads piled together, perfect spheres catching light, refraction and reflection detail, scientific photography style |
| `prod-tabular-alumina.jpg` | 4:5 | Macro of tabular alumina aggregate, large off-white sintered crystals with hexagonal structure, raking light, geological precision |
| `prod-oxalic-acid.jpg` | 4:5 | Pure white crystalline oxalic acid in laboratory crystallizing dish, soft diffused light, scientific still life, clean clinical aesthetic |
| `prod-pto-pbo.jpg` | 4:5 | White crystalline potassium oxalate powder in glass laboratory vessel, cool laboratory lighting, editorial scientific photography |
| `category-abrasives.jpg` | 16:10 | Industrial abrasive grinding wheel cross-section showing bonded abrasive grains, dramatic side lighting, manufacturing aesthetic |
| `category-refractory.jpg` | 16:10 | Interior of operating industrial furnace lined with refractory bricks, glowing orange heat radiating, structural integrity visible, awe-inspiring scale |
| `category-chemicals.jpg` | 16:10 | Modern industrial chemical laboratory, gleaming stainless steel reactor vessels, soft top lighting, clean futurist industrial aesthetic |
| `lab-qc.jpg` | 16:10 | Laboratory bench with precision analytical instruments — particle size analyzer, electronic balance, sample vials in rack — soft cool light, no people, editorial |
| `facility.jpg` | 16:9 | Wide shot of clean modern industrial materials processing facility, large-format kilns and conveyor systems, golden hour light through high windows, architectural photography |
| `industries-bg.jpg` | 16:9 | Abstract industrial texture: layered patinas of fired ceramic, refractory, polished metal, dark warm tones, very subtle, suitable as section background |
| `og-image.jpg` | 1200×630 | Crop of `hero-crucible.jpg` with logo overlay top-left for social sharing |

After you generate, **spot-check each image** for AI artifacts (warped text, fake logos, plasticky surfaces) before committing. Save each as JPG, quality 80–85, and target file size under 500 KB.

---

## Deploy to Vercel

1. Initialise a git repo and push to GitHub:

   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin git@github.com:YOUR-ORG/furner-refraceram.git
   git push -u origin main
   ```

2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your GitHub repo.
3. Framework Preset: **Other**.
4. Build Command: *(leave empty)*.
5. Output Directory: *(leave empty — repo root is served)*.
6. Click **Deploy**. Done in under a minute.

### Custom domain

In the Vercel dashboard → **Project → Settings → Domains** → add `furner.in` (or any domain you own). Vercel will print the DNS records you need to add at your registrar — typically:

- `A` record `@` → `76.76.21.21`
- `CNAME` record `www` → `cname.vercel-dns.com.`

Propagation usually completes within 30 minutes. Vercel auto-provisions an SSL certificate.

---

## Swap mailto → real form backend

The contact form currently posts via `mailto:` so it works on any host with no backend. To swap in a hosted form service:

### Formspree

1. Sign up at [formspree.io](https://formspree.io), create a form, copy the endpoint (e.g. `https://formspree.io/f/abcd1234`).
2. In `contact.html`, change one line:

   ```html
   <!-- before -->
   <form class="form" data-reveal data-reveal-delay="1"
         action="mailto:business@furner.in" method="post" enctype="text/plain">

   <!-- after -->
   <form class="form" data-reveal data-reveal-delay="1"
         action="https://formspree.io/f/abcd1234" method="post">
   ```

3. Remove `enctype="text/plain"`. That's it — Formspree forwards every submission to `business@furner.in`.

### Web3Forms (no signup)

Same swap, with Web3Forms' endpoint and an `access_key` hidden input. See [web3forms.com](https://web3forms.com) for the snippet.

---

## Accessibility

- Semantic HTML, one `<h1>` per page, landmark roles
- `aria-label` on icon buttons and language regions
- Visible `:focus-visible` outlines (ember accent)
- Skip-link to `#main` content
- AA contrast minimum on all text/background pairings
- Mobile menu traps focus and closes on `Esc`
- `prefers-reduced-motion` disables sparks, marquee, dial spin, and scroll reveals

Tested for Lighthouse Accessibility ≥ 95. Re-run from Chrome DevTools after any large content edit.

---

## Browser support

- Chrome / Edge / Safari / Firefox — current and previous major
- iOS Safari 15+, Android Chrome current
- Graceful fallback: `IntersectionObserver` is feature-detected; reveals will simply show without animation if missing
- Backdrop-filter falls back to a solid background on older browsers

---

## License & content

The code in this repo is yours. The product copy, company information, addresses, and phone numbers belong to Furner RefraCeram Private Limited.
