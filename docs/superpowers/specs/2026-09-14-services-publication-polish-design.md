# Services and Publication Polish Design

## Goal

Update Weiheng Wu's homepage to present selected publications more clearly and add professional reviewing service from the supplied CV.

## Page Content

### About Me

- Keep the UCAS and SMU names bold, but render them as plain text rather than links.
- Keep Prof. David Lo linked to `http://www.mysmu.edu/faculty/davidlo/`.
- Keep the existing Google Scholar icon linked to Weiheng Wu's Google Scholar profile.

### Selected Publications

- Show four publications in reverse chronological order: USENIX Security 2026, AAAI 2026, IEEE TIFS 2025, and WWW 2025.
- Remove the ICASSP 2026 paper from the selected list.
- Keep paper titles linked to their existing paper or DOI URLs.
- Preserve author order, bold Weiheng Wu's name, and retain the existing equal-contribution asterisk.
- Split venue metadata into two lines:
  - First line: bold short venue and year, followed by a smaller muted full venue name.
  - Second line: CCF and CORE rankings in muted text.
- Use these venue names:
  - USENIX Security 2026: 35th USENIX Security Symposium
  - AAAI 2026: 40th AAAI Conference on Artificial Intelligence
  - IEEE TIFS 2025: IEEE Transactions on Information Forensics and Security
  - WWW 2025: The ACM Web Conference

### Services

- Add an unframed `Services` section after Selected Publications and before Research Interests.
- Show `External Reviewer` with the period `2023 - Present`.
- Show two compact rows:
  - Journals: IEEE TDSC, IEEE TIFS, IEEE ToN, IEEE TASE, IEEE ToR.
  - Conferences: WWW 2025 & 2026, AAAI 2026 & 2027, ICASSP 2026.
- ICASSP remains in Services because it is reviewing experience, even though the ICASSP paper is removed from Selected Publications.

## Interaction And Styling

- David Lo and paper-title links use the normal body color at rest and transition to the terracotta accent on hover and keyboard focus.
- Bold text inside a link inherits the link color so the David Lo hover state is visible.
- Full venue names and ranking lines use smaller, lighter text without badges or cards.
- The Services section follows the existing section rhythm and remains readable on narrow mobile layouts.
- Bump the stylesheet query version in `index.html` so local and hosted browsers load the new CSS instead of a cached copy.

## Verification

- Automated tests verify the four-paper order, author emphasis, venue structure, Services content, removed school links, retained David Lo and Google Scholar links, and CSS behavior.
- Preview the page at desktop and mobile widths and confirm that venue metadata wraps cleanly, timeline markers remain aligned, and hover states are visible.
