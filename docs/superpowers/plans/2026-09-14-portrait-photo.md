# Portrait Photo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the circular illustrated avatar with a responsive rectangular portrait photograph.

**Architecture:** Keep the current sidebar markup and image styling, changing only the image asset, its accessible label, and responsive dimensions. Use a compressed JPEG for fast static-site delivery.

**Tech Stack:** HTML5, CSS3, macOS image conversion, Python `unittest`.

---

### Task 1: Specify Portrait Behavior

**Files:**
- Modify: `tests/test_profile_layout.py`

- [x] Add assertions for the portrait path, alternative text, rectangular desktop dimensions, square corners, and responsive tablet/mobile dimensions.
- [x] Run the profile tests and confirm they fail against the circular illustrated avatar.
- [x] Commit the failing test.

### Task 2: Add And Display The Portrait

**Files:**
- Create: `assets/img/weiheng-wu-portrait.jpg`
- Modify: `index.html`
- Modify: `assets/css/theme-claude.css`

- [x] Convert the supplied PNG to a web-optimized JPEG with a maximum dimension of 1200 pixels.
- [x] Update the avatar source and accessible alternative text.
- [x] Set desktop dimensions to 220 by 280 pixels with zero border radius and centered cover cropping.
- [x] Set tablet dimensions to 170 by 216 pixels and mobile dimensions to 150 by 190 pixels.
- [x] Bump the stylesheet query version to `20260914-portrait`.
- [x] Run all tests and commit the implementation.

### Task 3: Verify The Result

**Files:**
- Verify: `index.html`
- Verify: `assets/css/theme-claude.css`

- [x] Inspect desktop and 390-pixel mobile previews for framing, spacing, and overflow.
- [x] Run the complete test suite and repository checks.

### Task 4: Tighten The Portrait Crop

**Files:**
- Modify: `tests/test_profile_layout.py`
- Modify: `assets/css/theme-claude.css`

- [x] Add a failing assertion for a clipped 125% image zoom and upper-body focal point.
- [x] Move fixed dimensions to the avatar frame, clip overflow, and enlarge the image inside it.
- [x] Verify the crop at desktop and mobile sizes, run all tests, and commit the adjustment.
