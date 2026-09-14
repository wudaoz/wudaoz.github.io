# Portrait Photo Design

## Goal

Replace the illustrated circular avatar with the supplied portrait photograph and present it as a rectangular image.

## Design

- Create a web-optimized JPEG asset from `DSC06585-retouched.png` without altering the photograph's content.
- Display the portrait at 220 by 280 pixels on wide desktop layouts with square corners and `object-fit: cover`.
- Display it at 170 by 216 pixels on tablet layouts and 150 by 190 pixels on mobile layouts.
- Zoom the photograph to 125% inside the fixed rectangle and position the focal point slightly above center so the face and upper body are more prominent while some coastal background remains visible.
- Clip the enlarged photograph to the rectangular frame and retain the existing subtle shadow.
- Update the image alternative text to identify it as a portrait of Weiheng Wu.
- Bump the theme stylesheet query version so the rectangular dimensions load immediately.

## Verification

- Automated tests verify the new image path, meaningful alternative text, rectangular dimensions, and zero border radius.
- Desktop and mobile screenshots verify that the portrait remains well framed and does not overlap nearby content.
