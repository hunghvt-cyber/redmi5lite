# Dai Ca Minimal — Redmi Watch 5 Lite

For **Redmi Watch 5 Lite only**, 410 × 502 pixels.

## v2

- 12-hour time with a small AM/PM label, derived from the 24-hour clock source.
- Larger white digits on black.
- Centered battery percentage and battery icon above time.
- Vietnamese weekday and DD/MM date below.
- Watchface ID `928105002`; original v1 used `928105001`.

Build succeeds on Windows using GitHub Actions. Download `DaiCaMinimal-12h-v2` from the latest successful workflow run, extract it and install `DaiCaMinimal.bin` through an already connected Gadgetbridge on Android.

The original v1 was confirmed working on the user's watch. v2 is compiled and structurally checked, but still needs a physical-watch test.

## Editing

The normal watchface format used here does not provide an on-watch Edit panel. v2 does not add one. Different IDs let the watch distinguish v1 and v2; whether both remain installed depends on available watch storage and installer behavior.

`assets/watchface.zip.b64` contains the editable FPRJ and PNG assets. Open the decoded project in Mi Create/EasyFace to modify it. `design/build_v2.py` reproduces the art and project using Pillow and DejaVu Sans Bold (`--font` can point to another font file). No auth keys or device-specific credentials are needed to build.

Tools: [EasyFace](https://github.com/m0tral/EasyFace), [Mi Create](https://github.com/ooflet/Mi-Create), [Gadgetbridge](https://gadgetbridge.org/).
