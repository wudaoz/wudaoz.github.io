# Profile and Layout Refresh Design

## Goal

Update the homepage profile information and navigation, consolidate education and work history, rename the publications section, and correct the timeline marker alignment.

## Content Changes

- Change the top-left navigation label from `Home` to `Wu's Homepage`.
- Point the navigation link to `./index.html` so it works from both a local file and GitHub Pages without opening a directory index.
- Replace the displayed email and mail link with `whwu@smu.edu.sg`.
- Update About Me to state that the M.S. research focused on intrusion detection systems for network security.
- Update the current research description to focus on security issues in AI and agents.
- Link `Prof. David Lo` to `http://www.mysmu.edu/faculty/davidlo/` and append `(ACM and IEEE Fellow)`.
- Update the page metadata to reflect AI and agent security instead of Coding Agents.
- Rename `Publications` to `Selected Publications` while retaining the existing `id="publications"` anchor.

## Education and Experience

Replace the separate Education and Experience sections with one `Education & Experience` section and one continuous timeline. Order entries by most recent start date:

1. Singapore Management University (SMU) - Research Engineer with Prof. David Lo, 2026 - Present
2. Alibaba Group - Research Intern, 2025 - 2026
3. University of Chinese Academy of Sciences (UCAS) - M.S. in Cyberspace Security, 2023 - 2026
4. Shenzhen University (SZU) - B.E. in Electronic Information Engineering, 2019 - 2023

Use the section id `education-experience`. Keep the existing timeline item markup and typography.

## Timeline Alignment Fix

The line is 2 px wide at `left: -20px`, so its center is `-19px`. The current marker uses a 10 px content box plus two 2 px borders at `left: -25px`, giving it a 14 px outer diameter and a center at `-18px`.

Set the marker to `box-sizing: border-box` with a 12 px width and height while retaining `left: -25px`. Its center then becomes `-19px`, exactly matching the line. Apply the same rule to both loaded theme stylesheets so the fallback and active theme remain consistent.

## Verification

- Extend the static HTML tests to check the navigation label and local-safe link, email values, About Me wording and David Lo link, merged timeline order, and selected-publications heading.
- Add a CSS assertion that the timeline marker uses border-box sizing and a 12 px diameter in both stylesheets.
- Run the full unit test suite.
- Preview at desktop and mobile widths and verify that the timeline line passes through the marker center and that all text wraps without overlap.
