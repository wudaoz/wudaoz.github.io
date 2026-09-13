# Anthropic-inspired Typography Refresh Design

## Goal

Make the homepage feel more recognizably Anthropic-inspired through typography while preserving the current warm palette, two-column layout, content, spacing, and interaction behavior.

## Selected Direction

Use the approved 1B pairing:

- `Newsreader` supplies the warm editorial character for the profile name, section headings, prose, news, education and experience text, and research-interest descriptions.
- `Source Sans 3` handles compact or information-dense interface text: navigation, publication titles, author lists, venue metadata, and footer text.
- `Ubuntu Mono` remains the email font so the address keeps its existing technical accent.

The proprietary Anthropic typefaces are not copied. These Google Fonts are publicly hosted substitutes chosen to reproduce a similar humanist editorial contrast.

## Font Loading

Replace the existing Inter-only Google Fonts request in `index.html` with a single request for:

- Newsreader weights 400, 500, and 600 with its optical-size axis.
- Source Sans 3 weights 400, 500, 600, and 700.

Keep the existing preconnect declarations and use `display=swap`. Every declaration must include local fallbacks so the page remains readable if Google Fonts is unavailable:

- Editorial stack: `"Newsreader", Georgia, "Times New Roman", serif`.
- Interface stack: `"Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.

## Typography Mapping

Define two CSS custom properties in `theme-claude.css` for the editorial and interface stacks. Apply them as follows:

- Body defaults to the editorial stack.
- Navigation and buttons use the interface stack.
- Profile name and section headings inherit the editorial stack at weight 600.
- Email retains its existing monospace stack.
- Timeline titles, details, and dates use the editorial stack, with existing sizes and colors unchanged.
- Publication titles, authors, venue lines, and equal-contribution note use the interface stack for dense scanning.
- Research-interest text remains editorial; emoji and icons are unaffected.
- Footer uses the interface stack.

No negative letter spacing or viewport-scaled font sizes will be introduced. Existing responsive font sizes remain unchanged.

## Compatibility

The current fallback stylesheet remains structurally unchanged. The active `theme-claude.css` owns the new font mapping, while the existing base styles continue to provide a readable fallback if the theme stylesheet fails to load.

## Verification

Add focused tests that verify:

- The Google Fonts URL requests both approved families and uses `display=swap`.
- The active theme declares both font-stack variables.
- Body, navigation, publications, and footer use the intended variables.
- The email retains its monospace font.

Run the complete existing test suite, check the diff for whitespace errors, and inspect the live page at desktop and 390 x 844 mobile sizes. Confirm that long publication titles and author lists wrap without overlap or layout shifts.
