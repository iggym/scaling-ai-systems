# Improvement Tasks — Scaling AI Systems

Backlog of improvements for the repo and the GitHub Pages site
(<https://iggym.github.io/scaling-ai-systems/>), identified from a full review
of `index.html`, `metadata.json`, `README.md` and the twelve files in
`articles/` on 2026-10-06.

Priority: **P0** = broken for readers now · **P1** = credibility / discoverability · **P2** = quality & consistency · **P3** = nice to have.

---

## P0 — Broken right now

- [ ] **Fix mis-named article file.** `articles/five-teams-zero-owners.htmlfive-teams-zero-owners.html` should be `articles/five-teams-zero-owners.html`. `metadata.json` points to the correct name, so the card on the home page currently 404s. (`git mv` the file.)
- [ ] **De-duplicate article IDs.** `8472` is used by both *Who Owns the Agent?* and *The Sandbox Lie*. Assign a new unique ID to one of them and add a uniqueness check (see P2 validation script).
- [ ] **Fix broken share URLs.**
  - `leverage-lost.html` shares `https://iggym.github.io/scaling-ai-systems/leverage-lost` (missing `articles/` and `.html`).
  - Two share links end in an empty `url=` (`leverage-lost.html` X link, a LinkedIn link with `?url=`), and one Latitude quote has `&url=` empty.
  - Several articles share the site root instead of the article URL (`boundary-collapse-ai-org-design.html`, `cheap-tokens-massive-bills.html`, `ownership-void-org-design-ai-scale.html`, `who-owns-the-agent.html`).
  - Standardize on the canonical article URL, URL-encoded.
- [ ] **Escape metadata in `index.html`.** `cardHTML()` injects `title`, `hook`, `tags` and `path` via template strings into `innerHTML`. Add a small `escapeHTML()` helper so a stray `<`, `&` or quote in metadata cannot break the page.

## P1 — Credibility and trust

- [ ] **Hyperlink every citation.** None of the twelve articles link their sources; citations are plain text, and four articles have no citations block at all (`cheap-tokens-massive-bills`, `leverage-lost`, `ownership-void-org-design-ai-scale`, `who-owns-the-agent`). Add numbered, linked citations with in-text `[n]` markers.
- [ ] **Fact-check high-risk claims.** Verify against primary sources, or reframe as labelled composites:
  - *The Sandbox Lie*: PocketOS database deletion (Apr 2026), Amazon "Kiro" 13-hour Cost Explorer outage (Dec 2025), Swan AI $113,421.87 invoice, "token prices dropped 280x".
  - *Three-Team Trap* / *Own the Front Door* / *Five Teams, Zero Owners*: Klarna team sizes and backlog figures, Shopify memo consequences.
  - *Who Signed Off?* / *The Audit Bill Nobody Budgeted*: EU AI Act penalty math and per-decision log sizes.
  - *Cheap Tokens, Massive Bills*: Latitude $10k/day invoice.
- [ ] **Label numbers as reported / derived / assumed** in cost anatomies so readers can tell sourced data from illustration (see `docs/master-prompt-v1.md` §3).
- [ ] **Review publication dates.** `boundary-collapse-ai-org-design` is dated 2024-03-12 while its content and peers are 2025–2026; confirm or correct. Two articles share 2025-02-18 and three share 2025-03-14 — confirm intended ordering.
- [ ] **Normalize `research_window` format** to `YYYY-MM-DD to YYYY-MM-DD` (current values mix "Feb 13, 2024 - March 12, 2024", "through", en-dashes and "(W=5 draw)").
- [ ] **Add an About / methodology section** to the home page: who writes it, how research windows work, how numbers are sourced, corrections policy.

## P1 — Discoverability (SEO & sharing)

- [ ] **Add head metadata to every article and the index:** `meta description` (from `hook`), `link rel="canonical"`, Open Graph (`og:title`, `og:description`, `og:url`, `og:type`, `og:image`), Twitter card, `article:published_time`. Currently only `viewport` is present on every page.
- [ ] **Add JSON-LD** (`Article` on article pages, `WebSite` + `ItemList` on the index).
- [ ] **Create a default social card image** (`assets/og-default.png`, 1200×630) and optionally per-article cards.
- [ ] **Generate `sitemap.xml` and `robots.txt`** from `metadata.json`.
- [ ] **Add an RSS/Atom feed** (`feed.xml`) generated from `metadata.json` — the target audience reads via feed readers and newsletters.
- [ ] **Add a favicon** (SVG + PNG fallback) matching the orange "redline" mark.
- [ ] **Render article cards into `index.html` at build time (or add a `<noscript>` list).** The feed is client-side only, so crawlers and no-JS readers see "loading…".

## P2 — Consistency across articles

- [ ] **Adopt one shared design system.** Articles use ten different font stacks (Inter, Space Grotesk, Source Sans 3, Instrument Serif, Fraunces, DM Sans, Source Serif 4, JetBrains Mono…) and different color tokens. Extract a shared `assets/site.css` (tokens from `index.html`: `--dark`, `--paper`, `--orange`, `--teal`, `--yellow`, Libre Franklin / Inter / IBM Plex Mono) and migrate articles to it.
- [ ] **Extract shared components to `assets/site.js`**: reading-progress bar, reveal-on-scroll, three-things tracker, recall flip cards, share buttons, mobile drawer. Removes ~10–30 KB of duplicated inline code per article.
- [ ] **Use relative internal links.** Articles hard-code `https://iggym.github.io/scaling-ai-systems/` for Home (30 occurrences), which breaks local preview and forks. Use `../index.html`.
- [ ] **Unify `<title>` format** to `<Title> — Scaling AI Systems` (currently mixes `|`, `—`, `: subtitle`, and lowercase `scaling-ai-systems`; *When Code Replaces Departments* has no site suffix).
- [ ] **Clean up placeholder section headings** in *The Sandbox Lie* ("Bold Reframe", "Hidden Connections", "Credibility & Nuance", "Narrative Agency", "Data Storytelling") — these are prompt scaffolding labels, not reader-facing headings.
- [ ] **De-minify `the-audit-bill-nobody-budgeted.html`** class names (`a`, `bc`, `cm`, `pq`, …) so it can be maintained alongside the others.
- [ ] **Bring short articles up to standard.** *The Ownership Void* (~680 words), *Cheap Tokens, Massive Bills* (~630), *The Sandbox Lie* (~780) lack the cost anatomy / counterargument / actions sections that the strongest pieces have. Expand using the master prompt.
- [ ] **Resolve overlapping pairs.** Consider merging or explicitly cross-linking: *Leverage Lost* ↔ *The Hostage Architecture* (both vendor lock-in, same date 2026-04-17); *Who Signed Off?* ↔ *The Audit Bill Nobody Budgeted* (both EU AI Act audit, same date); *Who Owns the Agent?* ↔ *The Ownership Void* ↔ *Five Teams, Zero Owners* (all agent ownership).
- [ ] **Add "Related articles"** block at the end of each article (by shared tags).
- [ ] **Accessibility pass:** keyboard access and visible focus on sliders and flip cards, `aria-valuetext` on ranges, `role="img"` + title/desc on SVG charts, table captions, contrast check on `--muted` text (`#6a655c` on `#0d0d0b` in *Three-Team Trap* is 3.4:1 and fails AA for body text).

## P2 — Repo hygiene & tooling

- [ ] **Rewrite `README.md` to match the actual site.** It currently describes an inference-infrastructure guide (vLLM, PagedAttention, tensor parallelism, speculative decoding) that does not exist in the repo; the real content is org-design / cost-economics / compliance case studies. Also fix the broken markdown link inside the `git clone` code block.
- [ ] **Replace the Node-template `.gitignore`** with a minimal static-site one (`.DS_Store`, `*.log`, `.env*`, editor folders).
- [ ] **Add `scripts/validate.py`** (no dependencies) that checks: valid JSON; unique `id` and `slug`; every `path` exists; filename matches slug; date format; `research_window` format; required head tags present; no empty `url=` share links; reading time ≈ words/230.
- [ ] **Add a GitHub Actions workflow** running `validate.py` plus an HTML link checker (e.g. `lychee`) on PRs.
- [ ] **Add `CONTRIBUTING.md`** describing the article workflow: generate with `docs/master-prompt-v1.md` → fact-check → add file + metadata → validate → PR.
- [ ] **Add an article template** `articles/_template.html` implementing the shared design system and all required sections, so generated articles start from a known-good skeleton.
- [ ] **Fix footer copy** on the index: "the growth-stage layer of an eight-repo portfolio" is overwritten by `site.description` at runtime and references a portfolio the site never links. Either link the portfolio or drop it.

## P3 — Site features

- [ ] **Tag filter and search** on the home page (client-side over `metadata.json`).
- [ ] **Topic hubs / series pages** (Org Design, Cost Economics, Compliance, Vendor Strategy, Reliability) with a short intro and ordered reading list.
- [ ] **Pin a flagship article** (`pinned: true`) — the index supports it but nothing is pinned. *Three-Team Trap* or *Five Teams, Zero Owners* are the strongest candidates.
- [ ] **Real sparklines.** Card sparklines are identical decorative paths; drive them from a per-article `signal` array in metadata or remove them.
- [ ] **Newsletter / follow CTA** (RSS link, LinkedIn, email) in the footer and at the end of articles.
- [ ] **Custom `404.html`** that links back to the index.
- [ ] **Privacy-friendly analytics** (e.g. GoatCounter / Plausible) to learn which topics land.
- [ ] **Light theme** via `prefers-color-scheme` using the existing `--paper` token.
- [ ] **Print stylesheet** so leaders can share a clean PDF in planning meetings.
- [ ] **Cover the README's promised topics** (inference engines, KV cache, parallelism, quantization, cluster reliability) as a new series, or drop them from the README.

## Content pipeline ideas (next articles)

Gaps relative to the audience promise, suitable for `docs/master-prompt-v1.md`:

- [ ] Eval suites that stop catching regressions at 1M+ requests/day (reliability).
- [ ] The on-call rotation for an LLM feature: who gets paged when quality, not uptime, degrades (org-design).
- [ ] Prompt caching economics: when cache hit rate, not model price, sets the bill (cost-economics).
- [ ] Multi-region inference and data residency: the second compliance bill (compliance).
- [ ] Rate limits as an org constraint: quota allocation across teams (platform-architecture).
- [ ] GPU reservation vs. on-demand vs. API: the break-even curve (inference-infrastructure).
