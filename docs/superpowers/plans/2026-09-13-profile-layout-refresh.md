# Profile and Layout Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the homepage identity and research copy, consolidate the education and experience timeline, rename selected publications, and align timeline markers with their vertical line.

**Architecture:** Preserve the single-page static HTML structure and existing theme. Add focused standard-library tests for homepage content and CSS invariants, then make minimal edits to `index.html` and the duplicated active/fallback timeline rules.

**Tech Stack:** HTML5, CSS3, Python 3 standard library `html.parser`, `re`, and `unittest`

---

### Task 1: Add failing profile and layout checks

**Files:**
- Create: `tests/test_profile_layout.py`
- Read: `index.html`
- Read: `assets/css/theme-claude.css`
- Read: `assets/css/style-no-dark-mode_old.css`

- [x] **Step 1: Add HTML structure assertions**

Use `HTMLParser` to collect anchors, section headings, section text, and timeline item text. Assert:

- The navigation contains `Wu's Homepage` linked to `./index.html`.
- The visible email is `whwu [at] smu.edu.sg` and the mail link is `mailto:whwu@smu.edu.sg`.
- About Me contains `intrusion detection systems for network security` and `security issues in AI and agents`.
- `Prof. David Lo` links to `http://www.mysmu.edu/faculty/davidlo/`, followed by `(ACM and IEEE Fellow)`.
- There is one `Education & Experience` section with id `education-experience`, no separate education or experience sections, and timeline items ordered SMU, Alibaba, UCAS, SZU.
- The publication section heading is `Selected Publications`.

- [x] **Step 2: Add CSS marker assertions**

For both theme stylesheets, extract the `.timeline-item::after` rule and assert that it contains `box-sizing: border-box`, `left: -25px`, `width: 12px`, and `height: 12px`.

- [x] **Step 3: Run the new test and verify it fails**

Run: `python3 -m unittest tests/test_profile_layout.py -v`

Expected: FAIL because the current homepage still uses the old navigation, email, profile copy, separate sections, publication heading, and 10 px marker.

- [x] **Step 4: Commit the failing test**

Run:

```bash
git add tests/test_profile_layout.py
git commit -m "test profile and timeline layout"
```

### Task 2: Update homepage content and structure

**Files:**
- Modify: `index.html:5`
- Test: `tests/test_profile_layout.py`
- Test: `tests/test_publications.py`

- [x] **Step 1: Update navigation, email, metadata, and About Me**

Change the navigation to `<a href="./index.html">Wu's Homepage</a>`. Replace both email forms with the SMU address. Update the description and keywords for AI and agent security. Replace the About Me paragraphs with the approved M.S. research and current research text, and use the provided David Lo link and fellowship label.

- [x] **Step 2: Merge the timeline sections**

Replace the separate `education` and `experience` sections with one `education-experience` section titled `Education & Experience`. Reuse the existing item markup and order the four entries SMU, Alibaba, UCAS, SZU.

- [x] **Step 3: Rename the publication heading**

Change only the visible heading from `Publications` to `Selected Publications`; retain `id="publications"` and all paper content.

- [x] **Step 4: Run HTML tests**

Run: `python3 -m unittest tests/test_profile_layout.py tests/test_publications.py -v`

Expected: profile tests still fail only on CSS marker assertions; publication tests pass.

### Task 3: Correct marker alignment

**Files:**
- Modify: `assets/css/theme-claude.css:393`
- Modify: `assets/css/style-no-dark-mode_old.css:285`
- Test: `tests/test_profile_layout.py`

- [x] **Step 1: Apply the minimal marker geometry fix**

In both `.timeline-item::after` rules, add `box-sizing: border-box` and change width and height from 10 px to 12 px. Retain `left: -25px`, so the 12 px outer marker is centered at `-19px`, matching the 2 px line centered at `-19px`.

- [x] **Step 2: Run all tests**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass.

- [x] **Step 3: Preview desktop and mobile layouts**

Run: `python3 -m http.server 8000`, inspect the page at default width and 390 x 844, and confirm the merged timeline, marker alignment, navigation, profile copy, and publication heading render without overlap.

- [x] **Step 4: Commit the implementation**

Run:

```bash
git add index.html assets/css/theme-claude.css assets/css/style-no-dark-mode_old.css
git commit -m "refresh profile and timeline layout"
```

### Task 4: Final verification

**Files:**
- Verify: `index.html`
- Verify: `assets/css/theme-claude.css`
- Verify: `assets/css/style-no-dark-mode_old.css`
- Verify: `tests/test_profile_layout.py`
- Verify: `tests/test_publications.py`

- [x] **Step 1: Run the complete verification suite**

Run: `python3 -m unittest discover -s tests -v && git diff --check && git status --short --branch`

Expected: all tests pass, no whitespace errors, and only the implementation plan remains uncommitted before its final progress update.
