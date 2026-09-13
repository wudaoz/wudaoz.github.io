# Anthropic-inspired Typography Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the generic Inter typography with the approved Newsreader and Source Sans 3 pairing while preserving the homepage layout and responsive behavior.

**Architecture:** Keep the static single-page structure and introduce two font-stack custom properties in the active Claude theme. Load both public font families from one Google Fonts request, map editorial and information-dense regions explicitly, and protect the mapping with standard-library tests.

**Tech Stack:** HTML5, CSS3 custom properties, Google Fonts, Python 3 `unittest` and regular expressions

---

### Task 1: Add failing typography contract tests

**Files:**
- Modify: `tests/test_profile_layout.py`
- Read: `index.html`
- Read: `assets/css/theme-claude.css`

- [x] **Step 1: Add a typography test class**

Add tests that read the raw homepage and active theme CSS:

```python
class TypographyStyleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets/css/theme-claude.css").read_text(encoding="utf-8")

    def test_approved_google_fonts_are_loaded(self):
        self.assertIn("family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600", self.html)
        self.assertIn("family=Source+Sans+3:wght@400;500;600;700", self.html)
        self.assertIn("display=swap", self.html)

    def test_theme_defines_editorial_and_interface_stacks(self):
        self.assertIn('--claude-font-editorial: "Newsreader", Georgia, "Times New Roman", serif;', self.css)
        self.assertIn('--claude-font-interface: "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;', self.css)

    def test_type_roles_are_mapped(self):
        self.assertRegex(self.css, r"body\.theme-claude\s*\{[^}]*font-family: var\(--claude-font-editorial\);")
        self.assertRegex(self.css, r"\.top-nav\s*\{[^}]*font-family: var\(--claude-font-interface\);")
        self.assertRegex(self.css, r"\.publications\s*\{[^}]*font-family: var\(--claude-font-interface\);")
        self.assertRegex(self.css, r"\.site-footer\s*\{[^}]*font-family: var\(--claude-font-interface\);")

    def test_email_keeps_monospace_role(self):
        match = re.search(r"\.site-email\s*\{([^}]+)\}", self.css)
        self.assertIsNotNone(match)
        self.assertIn('font-family: "Ubuntu Mono", "SF Mono", monospace;', match.group(1))
```

- [x] **Step 2: Run the typography tests and verify the expected failure**

Run: `python3 -m unittest tests.test_profile_layout.TypographyStyleTest -v`

Expected: FAIL because the page still loads Inter and the active theme does not define or map the two approved font stacks.

- [x] **Step 3: Commit the failing tests**

```bash
git add tests/test_profile_layout.py
git commit -m "test typography roles"
```

### Task 2: Implement the approved typography mapping

**Files:**
- Modify: `index.html:19-21`
- Modify: `assets/css/theme-claude.css:6-17`
- Modify: `assets/css/theme-claude.css:66-72`
- Test: `tests/test_profile_layout.py`

- [x] **Step 1: Replace the Google Fonts request**

Replace the Inter-only request with:

```html
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
```

- [x] **Step 2: Define the two font stacks**

Add these properties to `:root`:

```css
--claude-font-editorial: "Newsreader", Georgia, "Times New Roman", serif;
--claude-font-interface: "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

- [x] **Step 3: Map typography roles**

Set the body to `var(--claude-font-editorial)`. Add `font-family: var(--claude-font-interface)` to `.top-nav`, `.publications`, and `.site-footer`. Keep the email declaration, colors, and responsive rules unchanged.

- [x] **Step 4: Run the focused and complete test suites**

Run: `python3 -m unittest tests.test_profile_layout.TypographyStyleTest -v`

Expected: four typography tests pass.

Run: `python3 -m unittest discover -s tests -v`

Expected: all existing and new tests pass.

- [x] **Step 5: Commit the implementation**

```bash
git add index.html assets/css/theme-claude.css
git commit -m "refresh Anthropic-inspired typography"
```

### Task 3: Verify rendering and repository state

**Files:**
- Verify: `index.html`
- Verify: `assets/css/theme-claude.css`
- Verify: `tests/test_profile_layout.py`

- [x] **Step 1: Inspect the desktop preview**

Open `http://localhost:8000`, refresh the page, and verify that the profile name, section headings, prose, timeline, publications, and footer use the intended font roles without overlap.

- [x] **Step 2: Inspect the mobile preview**

Set the browser viewport to 390 x 844. Verify that the navigation, About Me paragraphs, merged timeline, long publication titles, author lists, and footer wrap cleanly. Reset the viewport afterward.

- [x] **Step 3: Run final verification**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass with zero failures.

Run: `git diff --check`

Expected: no output.

Run: `git status --short --branch`

Expected: the implementation commits are clean except for the implementation plan progress update and the temporary `.superpowers` visual-comparison directory.

- [x] **Step 4: Commit the completed plan**

```bash
git add docs/superpowers/plans/2026-09-13-anthropic-typography-refresh.md
git commit -m "document typography refresh plan"
```

### Task 4: Match the approved 1B preview metrics

**Files:**
- Modify: `tests/test_profile_layout.py`
- Modify: `assets/css/theme-claude.css`
- Modify: `docs/superpowers/specs/2026-09-13-anthropic-typography-refresh-design.md`

- [x] **Step 1: Add a failing regression test for the preview metrics**

Assert that the profile name is 31 px with 1.05 line height, section headings are 20 px with 1.2 line height, and About Me prose is 17 px with 1.55 line height. Require an explicit editorial font declaration on all three roles.

- [x] **Step 2: Verify the test fails against the old dimensions**

Run: `python3 -m unittest tests.test_profile_layout.TypographyStyleTest.test_selected_typography_metrics_match_the_1b_preview -v`

Expected: FAIL because the production profile name is still 28 px with 1.2 line height and the other approved 1B metrics are absent.

- [x] **Step 3: Apply the exact desktop metrics from the approved preview**

Update the three active-theme rules without altering compact mobile overrides, colors, margins, or layout structure.

- [x] **Step 4: Run all tests and inspect the refreshed desktop preview**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass, and the refreshed About Me region visibly matches the approved 1B hierarchy.
