# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The fundraising campaign website for "Home For Our City" — Christ Church Liverpool's £4.5m capital campaign to develop 145 Edge Lane. Live at https://homeforourcity.org.

## Tech stack & commands

There is no tech stack: the entire site is a single hand-written file, `index.html`, with all CSS and JavaScript inline. No framework, no dependencies, no build step, no lint, no tests.

- **Preview locally**: open `index.html` directly in a browser, or serve the folder with any static server (e.g. `python -m http.server`).
- **Deploy**: push to `main`. The site is served by GitHub Pages from this repo (`Crowe-create/homeforourcity`); the `CNAME` file maps it to homeforourcity.org. Every commit to `main` goes live within minutes — there is no staging environment.

## Architecture of index.html (~2,800 lines)

The file reads top to bottom as: meta/SEO → JSON-LD structured data → `<style>` block → markup → `<script>` block.

- **Hash-routed "pages"**: the site behaves like a multi-page site but is one document. Each page is a `<div id="page-XXX" class="page">` (home, story, challenge, achieves, partner, edgelane, costs, faq, privacy), toggled by `showPage()` in the script block. **When adding or removing a page, also update the `VALID_PAGES` array** near the top of the script, plus the nav, mobile drawer menu, and footer links.
- **Fundraising totaliser**: the raised amount is hard-coded in more than one place and they must be kept in sync — the display text in the `.totaliser-raised` div (e.g. "£1.64m"), the percentage calculation in `animateTotaliser()`, but keep the narrative amounts in the partner page the same ("already raised £1.1m … a further £3.4m"). Search the file for the current figure before updating.
- **Interactive widgets** are all vanilla JS at the bottom of the file: photo carousels (tracks/dots built from JS arrays), FAQ accordion, giving tabs, mobile drawer with swipe gestures, scroll-reveal animations, and a click-to-load embedded map (`loadMap()`).
- **Design tokens** live in `:root` CSS variables at the top of the `<style>` block (palette taken from the CCL print leaflet). Use these rather than raw hex values.

## Supporting files

- `photos/` — `hero.jpg` doubles as the Open Graph/social preview image (referenced by absolute URL in the meta tags); `photos/carousel/slideNN.jpg` feed the home-page carousel.
- `downloads/` — public PDFs (campaign summary, Gift Aid declaration) linked from the site.
- `sitemap.xml` — single-URL sitemap; bump `<lastmod>` on meaningful content changes.
- Analytics is a commented-out Plausible snippet in `<head>`, deliberately not enabled yet.

## Cautions

- This is a public charity site (UK Charity Commission no. 1125990). Contact details, charity number, and donation links (ChurchSuite: `ccl.churchsuite.com/donate/...`) appear in both the visible markup and the JSON-LD block — change them in both places.
- Because deploys are instant on push to `main`, verify changes locally before committing.
