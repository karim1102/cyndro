Purpose
-------
This file gives immediate, actionable context for an AI coding agent working in this repository. It focuses on the concrete, discoverable structure and patterns so an agent can be productive without assumptions.

Repository snapshot
-------------------
- Single static landing page: [landing_page_V3.html](landing_page_V3.html)
- Empty folders present for future server code or assets: [controllers/](controllers), [includes/](includes), [img/](img)
- No package.json, build scripts, or tests detected — this is a plain static site

Big picture (what this project is)
---------------------------------
- A pre-MVP marketing + preview site for "Cyndro" (security visibility product). The HTML contains a static dashboard mockup (placeholder data) and a simple client-side theme toggle.
- No backend is implemented here; the presence of `controllers/` and `includes/` suggests planned server-side components but they are currently empty.

Key integration points
----------------------
- Form submissions: the contact form posts to an external Formspree URL `https://formspree.io/f/YOUR_FORM_ID` — update this ID when wiring real form handling.
- `logo.svg` is referenced from the root; ensure `img/` or repo root contains that asset when updating branding.

Project-specific conventions and patterns
---------------------------------------
- Styling: CSS is inlined inside the `<head>` of `landing_page_V3.html`. Small visual changes may be made inline; for larger refactors extract to a new CSS file and update the HTML link.
- Dark mode: controlled by adding/removing the `dark` class on `<body>` and persisted with `localStorage` under the key `theme`. Example: `localStorage.setItem('theme','dark')` and `body.classList.add('dark')`.
- Buttons: shared styles use `.btn`, with `.btn-primary` and `.btn-secondary` modifiers. Keep these class names when adding new CTAs.
- Dashboard mockup: static markup only — numeric values (e.g., `67/100`, `12 Issues`) are placeholders. When introducing real data, follow the existing semantic structure (e.g., `.risk-score-value`, `.stat-card > .stat-value`).

Developer workflows (how to preview, test, and iterate)
------------------------------------------------------
- Quick preview: open `landing_page_V3.html` in a browser (double-click) or run a lightweight static server:

```bash
# from repo root
python -m http.server 8000
# or (Node.js):
npx http-server -c-1 . -p 8000
```

- There is no build step. If you introduce npm/ tooling, add a clear `README.md` and `package.json` with start/build scripts.

Editing guidance for AI agents (practical rules)
---------------------------------------------
- Avoid assuming any server API exists. If you add dynamic behavior that requires a backend, either: (a) stub the API calls and document the expected endpoints, payloads, and responses, or (b) add a small local JSON/mock server and include explicit instructions for running it.
- When changing content or layout, prefer minimal, focused changes. This repo is an early-stage marketing site — preserve copy and intent unless the user asks for rewrites.
- For UI changes:
  - Keep responsive rules (media queries at 768px) intact unless improving mobile behavior.
  - Maintain class names for shared elements like `.btn`, `.dashboard-mockup`, `.risk-score-value` so future scripts can rely on them.
- If extracting CSS/JS into separate files, update `landing_page_V3.html` to reference them and include a short PR note explaining the split.

Examples from the codebase (explicit patterns to follow)
-----------------------------------------------------
- Theme toggle: `document.body.classList.toggle('dark')` + `localStorage` key `theme` (see [landing_page_V3.html](landing_page_V3.html)).
- Contact form: `<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">` — this is the live integration point to replace with a proper backend or third-party form ID.
- Dashboard values: selectors like `.risk-score-value`, `.stat-value`, `.alert-item` are used for static display; when populating dynamically, target these selectors.

PR checklist for agents
----------------------
- Preview changes in a browser (local server recommended).
- If you add or change external integrations (Formspree, analytics), document them in the PR description.
- Keep edits minimal and explain larger refactors (extracting CSS/JS or adding a build system) in the PR.

Where to look next (priority files/dirs)
--------------------------------------
- [landing_page_V3.html](landing_page_V3.html) — central source of UI, CSS, and client JS
- [controllers/](controllers) and [includes/](includes) — empty; check with maintainers before adding server logic here
- [img/](img) — expected place for images; `logo.svg` is referenced from root

If anything above is incorrect or you'd like a different focus (e.g., convert to a small Node static site, add a build system, or scaffold a backend), tell me which direction and I'll update these instructions.

-- end
