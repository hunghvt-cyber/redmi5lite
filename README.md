## V4 update

The right column now uses T2-T7/CN, day above month with a short horizontal divider, and battery percentage below. The large time and all AOD PNGs are unchanged from V3. ID: `928105004`. Download artifact `DaiCaMinimal-Stacked-v4-AOD`. Source generator: `design/build_v4.py`.

# Dai Ca Minimal — Redmi Watch 5 Lite

For **Redmi Watch 5 Lite only**, 410 × 502 pixels.

## V3: Stacked 12-hour + outline AOD

- Large hour and minute in two rows, Barlow Condensed Bold at its natural proportions.
- 12-hour clock without AM/PM, as requested.
- Right column: Vietnamese weekday, DD/MM and battery percentage. No icons or weather.
- Separate AOD project: only hour/minute outlines, black background, no seconds, animation, or other information.
- AOD maximum nonblack pixel area over all 720 12-hour/minute combinations: 3.55%. This is a design metric, not a battery-life measurement.
- ID `928105003`; v1 `928105001`; v2 `928105002`.

Download `DaiCaMinimal-Stacked-v3-AOD` from the successful Windows workflow run, extract and install `DaiCaMinimal.bin` using an already connected Gadgetbridge on Android. Enable Always-on display in the watch's Display settings to test the included AOD layout. Real-device verification is still required for V3 and its AOD.

## Sources

`assets/watchface.zip.b64`: complete FPRJ and indexed-PNG assets, including `AOD/AOD.fprj`.

Reproduce V3 with Pillow installed: `python design/build_v3.py`. The Barlow Condensed font and its SIL Open Font License are in `design/fonts/`.

This build does not add an on-watch Edit panel. Different IDs let the watch distinguish versions; retention depends on watch storage and installer behavior.

Tools: [EasyFace](https://github.com/m0tral/EasyFace), [Mi Create](https://github.com/ooflet/Mi-Create), [Gadgetbridge](https://gadgetbridge.org/).
