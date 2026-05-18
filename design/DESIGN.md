---
name: Obsidian Command
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c4c9ac'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#8e9379'
  outline-variant: '#444933'
  surface-tint: '#abd600'
  primary: '#ffffff'
  on-primary: '#283500'
  primary-container: '#c3f400'
  on-primary-container: '#556d00'
  inverse-primary: '#506600'
  secondary: '#c8c6c5'
  on-secondary: '#313030'
  secondary-container: '#474746'
  on-secondary-container: '#b7b5b4'
  tertiary: '#ffffff'
  on-tertiary: '#21323e'
  tertiary-container: '#d2e5f5'
  on-tertiary-container: '#556774'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#c3f400'
  primary-fixed-dim: '#abd600'
  on-primary-fixed: '#161e00'
  on-primary-fixed-variant: '#3c4d00'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#d2e5f5'
  tertiary-fixed-dim: '#b6c9d8'
  on-tertiary-fixed: '#0b1d29'
  on-tertiary-fixed-variant: '#374956'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: JetBrains Mono
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: JetBrains Mono
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: JetBrains Mono
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0em
  body-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.15em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0em
spacing:
  unit: 4px
  gutter: 16px
  margin: 24px
  container-max: 1440px
---

## Brand & Style

The design system is an avant-garde, "Tech-Noir" interpretation of developer environments. It moves away from friendly, rounded AI tropes toward a high-fidelity, engineering-first aesthetic. The personality is precise, authoritative, and sophisticated—evoking the feeling of a high-end physical hardware terminal or a specialized forensic tool.

We utilize a **Modern Brutalist** style characterized by:
- **Obsidian Foundations:** Deep, near-black backgrounds that provide a canvas for high-contrast data.
- **Monochromatic Rigor:** A primary reliance on greyscale, punctured by a singular, aggressive accent.
- **Technical Detail:** 1px "wireframe" aesthetics, micro-grids, and status-driven glows.
- **Intentional Friction:** High information density that rewards the professional user's expertise rather than over-simplifying the interface.

## Colors

The palette is strictly dark-mode, designed to minimize eye strain while maximizing the "pop" of critical data points.

- **Primary (Acid Green - #CCFF00):** Used for primary actions, success states, and active terminal cursors. It represents the "pulse" of the system.
- **Neutral (Obsidian - #0A0A0A):** The base layer. It should feel bottomless and void-like.
- **Secondary (Anthracite - #1A1A1A):** Used for surface elevation and container backgrounds to differentiate from the void.
- **Accent (Electric Orange - #FF4D00):** Reserved for warnings, critical errors, or high-priority interrupts.
- **Data Greys:** A range of low-saturation greys (e.g., #4D4D4D) are used for secondary text and inactive 1px borders to maintain the wireframe feel.

## Typography

The design system utilizes **JetBrains Mono** exclusively to maintain a hardware-centric feel. We create hierarchy through extreme weight contrast and letter-spacing adjustments rather than font variety.

- **Display & Headlines:** Use ExtraBold or Bold weights with tight letter-spacing to create a "blocked" look.
- **Body Text:** Standard weight with generous line height for readability in technical contexts.
- **Labels:** Use "Label-Caps" for UI metadata (e.g., section headers, input labels). High tracking (letter-spacing) is essential here to reference vintage engineering blueprints.
- **Micro-Copy:** Small font sizes remain legible due to the monospaced nature of the typeface.

## Layout & Spacing

The layout philosophy is based on a **Rigid Grid System** that mimics a technical schematic.

- **The 4px Baseline:** Every element, padding, and margin must be a multiple of 4px to ensure mathematical alignment.
- **12-Column Grid:** On desktop, use a 12-column grid with 1px borders as visible gutters where possible to reinforce the "Brutalist" structure.
- **Visible Architecture:** Instead of invisible margins, use subtle 1px lines (#262626) to separate sidebar, header, and main content areas.
- **Density:** Information density should be high. Space is used as a functional separator, not just for "breathing room."

## Elevation & Depth

Depth in this design system is achieved through **Tonal Layering and Glow**, not traditional shadows.

- **Flat Stack:** Objects do not "float" with shadows. Instead, elevated elements use a slightly lighter background (#1A1A1A) or a 1px border (#333333).
- **Glow Indicators:** Use "Outer Glow" sparingly for active states. A 2px-4px blur of the Acid Green color creates a "backlit" CRT effect for status lights.
- **Scanline Overlays:** High-priority containers may feature a subtle, repeating horizontal linear gradient at 2px intervals with 3% opacity to mimic terminal monitors.
- **Transparency:** Use semi-transparent obsidian backgrounds (90% opacity) for overlays to keep the underlying grid visible, maintaining a sense of "layered data."

## Shapes

The shape language is **Strictly Geometric and Sharp**.

- **Zero Radius:** All buttons, containers, and input fields use 0px border radius. This reinforces the hardware/industrial aesthetic.
- **Chamfered Edges:** For special "Hero" components (like a main CTA or a primary status badge), a 45-degree clipped corner (chamfer) can be used to add a military-spec or futuristic industrial feel.
- **1px Borders:** Borders are the primary way to define shape. They should be crisp, never blurred, and often use slightly different shades of grey to indicate hierarchy.

## Components

- **Buttons:** 0px radius. Primary buttons are solid Acid Green with black text. Secondary buttons are transparent with a 1px white or grey border. Hover states should "invert" or trigger a flicker effect.
- **Input Fields:** Bottom-border only or a full 1px box. Focus state triggers a solid Acid Green 1px border and a blinking square cursor.
- **Chips/Status:** Small, rectangular boxes. Use a "Glow" dot (4px circle) next to text to indicate "Live" or "Active" states.
- **Cards:** No shadows. Defined by a 1px border (#262626). The header of the card should be separated by a 1px horizontal line.
- **Scrollbars:** Ultra-thin (4px), non-rounded, Acid Green on a black track.
- **Progress Bars:** Segmented blocks (stepped) rather than a smooth continuous fill, resembling vintage loading bars.
- **Terminal Micro-interactions:** Use "typewriter" reveals for text loading and momentary "glitch" transitions (chromatic aberration) for screen state changes.