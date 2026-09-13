# Publications Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the homepage with five selected publications, accurate author order, venue rankings, contribution emphasis, and durable paper links.

**Architecture:** Keep the existing static HTML publication list and CSS unchanged. Replace the list content in `index.html`, then use a small standard-library Python test to verify order, links, author emphasis, contribution markers, and ranking labels.

**Tech Stack:** HTML5, Python 3 standard library `html.parser` and `unittest`

---

### Task 1: Add publication structure checks

**Files:**
- Create: `tests/test_publications.py`
- Read: `index.html`

- [x] **Step 1: Write the failing test**

Create an `HTMLParser` collector that records each publication title, title link, author HTML, and venue text. Assert that the five expected titles appear in this order: Cutting the Fuse, BTDA, Sentient, SAURONEYES, Brewing Vodka. Assert that every title link uses HTTPS, `Weiheng Wu` is bold in all five entries, SAURONEYES contains two equal-contribution markers, and venue labels match the approved CCF/CORE values.

- [x] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests/test_publications.py -v`

Expected: FAIL because `index.html` currently contains four entries, has no linked titles or ranking labels, and uses the old order.

- [x] **Step 3: Commit the failing test**

Run:

```bash
git add tests/test_publications.py
git commit -m "test publication metadata"
```

### Task 2: Refresh publication content

**Files:**
- Modify: `index.html:167`
- Test: `tests/test_publications.py`

- [x] **Step 1: Replace the Publications list**

Keep the current list markup and update its entries to:

```html
<div class="title"><a href="PAPER_URL">PAPER_TITLE</a></div>
<div class="author">FULL_AUTHOR_LIST_WITH_WEIHENG_WU_BOLD</div>
<div class="periodical"><em><strong>VENUE YEAR</strong> (RANKINGS)</em></div>
```

Use these links:

- Cutting the Fuse: `https://www.usenix.org/system/files/usenixsecurity26-wu-weiheng.pdf`
- BTDA: `https://doi.org/10.1109/ICASSP55912.2026.11461917`
- Sentient: `https://ojs.aaai.org/index.php/AAAI/article/download/37115/41077`
- SAURONEYES: `https://doi.org/10.1109/TIFS.2025.3618381`
- Brewing Vodka: `https://doi.org/10.1145/3696410.3714563`

Use these venue labels:

- `USENIX Security 2026 (CCF-A, CORE A*)`
- `ICASSP 2026 (CCF-B)`
- `AAAI 2026 (CCF-A, CORE A*)`
- `IEEE TIFS 2025 (CCF-A)`
- `WWW 2025 (CCF-A, CORE A*)`

- [x] **Step 2: Run the structure test**

Run: `python3 -m unittest tests/test_publications.py -v`

Expected: PASS.

- [x] **Step 3: Check HTML diff quality**

Run: `git diff --check && git diff -- index.html`

Expected: no whitespace errors; diff contains only the approved publication updates and the existing equal-contribution changes.

- [x] **Step 4: Preview in a local browser**

Run: `python3 -m http.server 8000`

Open `http://localhost:8000`, confirm all five entries render in order, no text overlaps, the contribution note remains visible, and title links have valid HTTPS targets.

- [x] **Step 5: Commit the implementation**

Run:

```bash
git add index.html
git commit -m "refresh selected publications"
```

### Task 3: Final verification

**Files:**
- Verify: `index.html`
- Verify: `tests/test_publications.py`

- [x] **Step 1: Run all repository checks**

Run: `python3 -m unittest discover -s tests -v && git diff --check && git status --short --branch`

Expected: all tests pass, no whitespace errors, and only intentional plan metadata remains uncommitted if it has not been committed separately.

- [x] **Step 2: Report publication links and ranking behavior**

State that official direct PDFs are used for USENIX Security and AAAI; stable official DOI pages are used for ICASSP, TIFS, and WWW where a public direct PDF was not verified.
