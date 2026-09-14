# Services and Publication Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add professional reviewing service and improve publication metadata, links, and selected-paper content on Weiheng Wu's homepage.

**Architecture:** Keep the static single-page HTML structure and add semantic classes for venue metadata and Services content. Extend the existing Python HTML-parser tests to verify content and DOM structure, while CSS tests cover link interaction and responsive typography.

**Tech Stack:** HTML5, CSS3, Python `unittest` and `html.parser`.

---

### Task 1: Lock Content Requirements With Failing Tests

**Files:**
- Modify: `tests/test_publications.py`
- Modify: `tests/test_profile_layout.py`

- [x] **Step 1: Extend the publication parser and expectations**

Track `venue_short`, `venue_full`, and `venue_ranking` class content. Expect four publications in order, assert ICASSP is absent, and assert the exact full venue names and ranking lines.

- [x] **Step 2: Add profile and Services expectations**

Assert the Google Scholar URL, plain-text UCAS and SMU names without school links, the retained David Lo link, the `Services` section position, and the exact reviewer period, journal list, and conference list.

- [x] **Step 3: Add CSS behavior expectations**

Assert that section links transition from body text color to accent color on hover and focus, linked strong text inherits color, venue metadata is muted and smaller, and Services has narrow-screen layout rules.

- [x] **Step 4: Run tests and verify the new assertions fail for missing behavior**

Run: `python3 -m unittest discover -s tests -v`

Expected: failures for the old five-paper list, missing Services content, school anchors, old venue structure, old cache key, and missing CSS rules.

- [x] **Step 5: Commit failing tests**

```bash
git add tests/test_publications.py tests/test_profile_layout.py
git commit -m "test: specify services and publication metadata"
```

### Task 2: Implement Content And Markup

**Files:**
- Modify: `index.html`

- [x] **Step 1: Remove institution anchors while retaining emphasis**

Replace the UCAS and SMU anchor elements in About Me with plain `strong` elements, leaving the David Lo anchor unchanged.

- [x] **Step 2: Remove ICASSP and restructure venue metadata**

Delete the BTDA list item. For each remaining paper, add a `venue-line` containing `venue-short` and `venue-full`, followed by a `venue-ranking` line with the existing CCF and CORE values.

- [x] **Step 3: Add Services after Selected Publications**

Add an unframed section with `External Reviewer`, `2023 - Present`, and separate Journals and Conferences rows matching the CV.

- [x] **Step 4: Update the stylesheet cache key**

Change the active theme URL to `theme-claude.css?v=20260914-services`.

- [x] **Step 5: Run content tests**

Run: `python3 -m unittest tests.test_publications tests.test_profile_layout.ProfileContentTest -v`

Expected: content assertions pass; style assertions may still fail until Task 3.

### Task 3: Implement Styling And Interaction

**Files:**
- Modify: `assets/css/theme-claude.css`

- [x] **Step 1: Add visible link interaction**

Set section-body links to the normal text color, add a short color transition, change them to the accent color on hover and keyboard focus, and make nested `strong` elements inherit the link color.

- [x] **Step 2: Style publication metadata**

Keep the short venue prominent, render the full venue name and rankings in smaller muted text, and allow the venue line to wrap naturally without badges.

- [x] **Step 3: Style the Services list**

Use an unframed heading row and compact two-column definition rows on desktop. Stack each label above its value on narrow screens.

- [x] **Step 4: Run the full automated suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass.

- [x] **Step 5: Commit the implementation**

```bash
git add index.html assets/css/theme-claude.css
git commit -m "feat: add reviewing services and refine publications"
```

### Task 4: Visual Verification And Cleanup

**Files:**
- Verify: `index.html`
- Verify: `assets/css/theme-claude.css`

- [x] **Step 1: Open the cache-busted local preview**

Open `http://localhost:8000/?services=20260914` and confirm the server is serving the current `master` checkout.

- [x] **Step 2: Check desktop layout and interactions**

Confirm four publications, full venue names, ranking lines, Services placement, Google Scholar destination, and visible hover/focus color changes.

- [x] **Step 3: Check mobile layout**

At approximately 390 by 844 pixels, confirm Services rows stack, venue text wraps without clipping, and no content overlaps.

- [x] **Step 4: Run final repository checks**

Run: `python3 -m unittest discover -s tests -v`, `git diff --check`, and `git status --short --branch`.

Expected: all tests pass, no whitespace errors, and only intentionally ignored temporary preview artifacts remain untracked.
