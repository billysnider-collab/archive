# The Dragonbone Chair Reading Companion — Design Specification

Version 1.0 · Built against live chapter data for chapters 1–6 of 55.

---

## 1. Design thesis

A reader's copy of a manuscript, not the manuscript itself.

The reference object is not an illuminated Bible in a glass case — it is a working scholar's copy, with the main text set clean and wide, and a **marginalia rail** running alongside it where a previous reader has scribbled notes. That rail is the signature element of this site and the thing it should be remembered for.

The spoiler mechanic lives in the margin. In **First Read** mode, foreshadowing notes appear as sealed marginal glosses — the ink is there, visibly, but struck through and unreadable, closed with a wax seal. In **Reread** mode they open into rubricated red annotations, the way a scribe's correction hand differs from the body hand. The reader can see that something was noticed at that exact point in the text without learning what.

This encodes the product's actual job: the site's value is knowing *where* the secrets are.

---

## 2. Color palette

All values from the brief. Two modes, both fully specified.

### First Read (default) — candlelit parchment

| Token | Hex | Use |
|---|---|---|
| `--parchment` | `#F4E8C1` | Page background |
| `--aged-paper` | `#EAD9A8` | Cards, raised surfaces, sidebar |
| `--ink` | `#1C1C1C` | Body text |
| `--forest` | `#1A2E1A` | Headings, header bar, footer |
| `--gold` | `#C9A227` | Accents, rules, progress bar, focus ring |
| `--wax` | `#7A1F1F` | Seals, spoiler markers, destructive actions |
| `--stone` | `#4A4A4A` | Secondary text, metadata, captions |
| `--night` | `#1B2A3A` | Reserved — Norn/cold references only |

### Reread — cold archive

| Token | Hex | Use |
|---|---|---|
| `--parchment` | `#12202D` | Page background (darkened night blue) |
| `--aged-paper` | `#1B2A3A` | Cards, raised surfaces |
| `--ink` | `#E8DFC4` | Body text (parchment inverted) |
| `--forest` | `#0E1822` | Header bar, footer |
| `--gold` | `#D9B84A` | Accents — lifted for contrast on dark |
| `--wax` | `#B84A4A` | Revealed spoiler text, open seals |
| `--stone` | `#9AA6B2` | Secondary text |

### Contrast verification (WCAG 2.1 AA)

| Pair | Ratio | Result |
|---|---|---|
| `#1C1C1C` on `#F4E8C1` | 15.1:1 | AAA |
| `#1A2E1A` on `#F4E8C1` | 12.4:1 | AAA |
| `#4A4A4A` on `#EAD9A8` | 6.9:1 | AA |
| `#7A1F1F` on `#F4E8C1` | 8.2:1 | AAA |
| `#E8DFC4` on `#12202D` | 13.6:1 | AAA |
| `#D9B84A` on `#12202D` | 8.3:1 | AAA |

Gold `#C9A227` on parchment is **2.1:1** — it fails text contrast and is therefore used **only** for rules, borders, bars, and decorative marks, never for text on a light background. On the forest header bar it reaches 4.9:1 and is permitted for small text there.

---

## 3. Typography

Google Fonts: `Cinzel`, `Lora`, `Inter`.

| Role | Face | Weights | Notes |
|---|---|---|---|
| Display / headings | **Cinzel** | 400, 600 | Roman capital forms. Used with restraint — page titles, chapter titles, section rules. Never below 14px; it is unreadable small. |
| Body | **Lora** | 400, 400i, 600 | All prose, recaps, card descriptions. Line height 1.7. |
| UI / labels | **Inter** | 400, 500, 600 | Buttons, tags, filters, metadata, pronunciation keys. Uppercase 0.08em tracking for eyebrows. |

### Type scale (1.25 major third, 17px base)

| Step | Size | Face | Use |
|---|---|---|---|
| Display | 3.25rem / 52px | Cinzel 400 | Home hero title |
| H1 | 2.25rem / 36px | Cinzel 600 | Chapter title, page titles |
| H2 | 1.5rem / 24px | Cinzel 400 | Section headings |
| H3 | 1.15rem / 18px | Inter 600 | Card names |
| Body | 1.0625rem / 17px | Lora 400 | Prose |
| Small | 0.875rem / 14px | Inter 400 | Metadata, tags |
| Micro | 0.75rem / 12px | Inter 600 | Eyebrows, uppercase labels |

**Chapter numerals** are set as Roman numerals in Cinzel 400 at 4rem, gold, with 0.06em tracking — `XII`, not `12`. This is the one purely decorative typographic move and it is confined to the chapter header and index cards. Arabic numerals appear alongside in Inter Micro so no one has to parse Roman numerals to navigate.

Measure is capped at **68 characters** for all prose.

---

## 4. Components

### Spoiler toggle
Segmented control, two options, persistent in the header on every page. Not a switch — a switch implies on/off, and neither of these modes is "off." Each segment carries a **label**, an **icon** (closed seal / open seal), and the selected segment carries a text badge reading `Foreshadowing hidden` or `Foreshadowing shown`. Mode is announced via `aria-live="polite"` on change. State does not rely on color.

### Sealed gloss (the marginalia rail)
The signature component. A foreshadowing entry in First Read renders as: a wax-seal disc in the margin, the clue text present in the DOM but visually struck and blurred, and a `Reveal` button. Reveal fades the blur out over 240ms and fades text in — no layout shift, because the collapsed and expanded heights are matched. Keyboard operable, `aria-expanded` on the button. In Reread mode, all glosses render open by default with a red rubricated left rule.

On mobile the rail collapses beneath the recap as a full-width accordion titled `Marginal notes`.

### Chapter card
Aged-paper ground, 1px gold hairline, Roman numeral top-left, title in Cinzel, 2-line recap clamp, and a small status row: read / unread, count of new characters, count of lore notes. Hover lifts 2px and draws a gold underline beneath the title.

### Character card
Name (Inter 600), pronunciation in stone italic beneath, role tag, first-appearance chapter chip, description clamped to 3 lines with an expander. A `New` or `Returning` marker uses both a shape (filled vs. hollow diamond) and color.

### Lore accordion
Term, category chips, chapter chips. Collapsed by default on chapter pages; expanded by default in the glossary. `<details>`-based so it works without JS.

### Quote block
Left gold rule, Lora italic at 1.25rem, speaker in Inter small caps beneath, theme chips, and a favorite toggle rendered as a small star that fills gold.

### Search
Global, in the header. Autocompletes across characters, locations, and lore terms. Results grouped by type with a type label. Arrow-key navigable, `role="combobox"` with `aria-activedescendant`.

### Progress bar
2px gold bar fixed to the top edge of the viewport, showing chapters marked read out of 55. On the chapter page it shows position within the book.

### Back to top
Wax-seal disc, bottom-right, appears after 600px of scroll. `aria-label="Back to top"`.

### Breadcrumb
`Home › Chapters › Chapter VI`. Inter Micro, stone, gold separators.

---

## 5. Page layouts

### Home
```
┌──────────────────────────────────────────────┐
│ ▁▁▁ gold progress rail ▁▁▁                   │
│ ✦ EMBLEM   Chapters Characters Lore Quotes   │
│            [First Read | Reread]   [search]  │
├──────────────────────────────────────────────┤
│                                              │
│        MEMORY, SORROW, AND THORN             │
│        THE DRAGONBONE CHAIR                  │
│        A chapter companion                   │
│                                              │
│        [ Start with Chapter I ]              │
│        [ Pick a chapter ]                    │
│                                              │
│   Reading mode: Foreshadowing hidden         │
├──────────────────────────────────────────────┤
│  Your progress   ▓▓▓▓░░░░░░░  3 of 55        │
│  Continue → Chapter IV: Cricket Cage         │
├──────────────────────────────────────────────┤
│  WHAT THIS IS                                │
│  Three short columns: recaps / who's who /   │
│  what to watch for                           │
└──────────────────────────────────────────────┘
```
Hero sits on parchment with an animated grain layer at 3% opacity and a very slow (40s) drift. Disabled entirely under `prefers-reduced-motion`.

### Chapter index
Responsive grid, `minmax(280px, 1fr)`. Filter row above: `All / Part One / Part Two / Part Three`, plus `Unread only`. **Note:** the source data has no `part` field, so the part filter is stubbed and hidden until that data exists.

### Chapter page (desktop)
```
┌───────────────────────────────────────────────────────┐
│ Home › Chapters › Chapter VI                          │
├───────────────────────────────────────────────────────┤
│  VI                                                   │
│  Six Silver Sparrows                                  │
│  Chapter 6 of 55        ▓▓░░░░░░░░░  11%              │
├────────────────────────────────┬──────────────────────┤
│ PREVIOUSLY ON                  │  MARGINAL NOTES      │
│ prose…                         │  ◈ sealed gloss      │
│                                │  ◈ sealed gloss      │
│ RECAP                          │  ◈ sealed gloss      │
│ prose…                         │  ◈ sealed gloss      │
│                                │                      │
│ WHO APPEARS                    │  SAY IT ALOUD        │
│ [card] [card] [card]           │  Term — pro-NUN-see  │
│                                │  Term — pro-NUN-see  │
│ WHERE                          │                      │
│ [card] [card]                  │  THEMES HERE         │
│                                │  Memory · Power      │
│ LORE                           │                      │
│ ▸ accordion                    │                      │
│ ▸ accordion                    │                      │
│                                │                      │
│ QUOTES                         │                      │
│ ▌ "…" — Binabik                │                      │
│                                │                      │
│ FOR DISCUSSION                 │                      │
│ 1. … 2. … 3. …                 │                      │
│                                │                      │
│ MAP UPDATE  (text note)        │                      │
├────────────────────────────────┴──────────────────────┤
│ ‹ V: The Tower Window        VII: (not yet added) ›    │
└───────────────────────────────────────────────────────┘
```
Grid is `1fr 320px` above 1024px, single column below, with the marginalia rail moving to sit directly after the recap.

### Character codex
Search field, then filters for `New in / Appears in` chapter range and status. Cards in a 3-up grid at 1440px, 2-up at 1024, 1-up at 375.

### Lore & glossary
Sticky A–Z jump rail on the left at desktop. Category filter chips across the top: `history · culture · religion · magic · places · people · creatures · prophecy · nature`. Entries as accordions, each ending with the chapters it appears in as clickable chips.

### Quotes & themes
Two-column masonry of quote blocks. Theme filter chips. Favorites filter.

### Map
**Deferred.** The source data provides only a text `map_hint` per location, with no coordinates. Location content currently surfaces as text cards on the chapter page and in a `Places` view. Ship the map when coordinates exist.

---

## 6. Interaction notes

| Interaction | Behavior | Duration |
|---|---|---|
| Route change | Fade + 8px rise on the main region | 220ms ease-out |
| Card hover | 2px lift, gold underline on title | 160ms |
| Spoiler reveal | Blur 6px→0, opacity 0.25→1 | 240ms ease-out |
| Mode switch | Cross-fade of background and surfaces | 300ms |
| Accordion | Height auto-transition | 200ms |
| Grain drift | Background-position loop | 40s linear infinite |
| Favorite | Star scale 1→1.2→1 | 180ms |

All motion is gated behind a `prefers-reduced-motion: reduce` block that reduces every duration to 1ms and stops the grain loop. A manual `Reduce motion` control is also offered in the footer for users whose OS setting isn't available to them.

Nothing autoplays. Nothing moves on scroll except the progress bar and the back-to-top button.

---

## 7. Responsive breakpoints

| Width | Layout |
|---|---|
| 375px | Single column. Hamburger nav. Marginalia inline after recap. Cards full width. Type base 16px. |
| 768px | Two-up card grids. Nav still collapsed. Chapter body single column. |
| 1024px | Full nav bar. Chapter page becomes `1fr 320px`. Sticky sidebar. |
| 1440px | Content max-width 1180px, centered. Three-up grids. Type base 17px. |

Line height 1.7 throughout body prose. Tap targets minimum 44×44px.

---

## 8. Accessibility checklist

- [x] All text pairs meet 4.5:1; large text meets 3:1
- [x] Gold is never used for text on light backgrounds
- [x] Mode and status never communicated by color alone — icon + text label always present
- [x] Semantic landmarks: `header`, `nav`, `main`, `aside`, `footer`
- [x] One `h1` per view; heading order never skips a level
- [x] Visible focus ring: 2px gold + 2px offset, plus a 1px ink inner ring so it is visible in both modes
- [x] Spoiler reveals are `<button>` elements with `aria-expanded`
- [x] Accordions use native `<details>`/`<summary>`
- [x] Search is a `role="combobox"` with keyboard navigation and `aria-activedescendant`
- [x] Mode changes announced via `aria-live="polite"`
- [x] Skip-to-content link as the first focusable element
- [x] `prefers-reduced-motion` respected; manual override provided
- [x] Alt text on the emblem; decorative rules marked `aria-hidden`
- [x] Zoom to 200% without horizontal scroll
- [x] Works without JavaScript for reading content (progressive enhancement on filters and search)

---

## 9. Asset list

| Asset | Status | Notes |
|---|---|---|
| Emblem — tower + sword | Built as inline SVG | Monoline, gold on forest |
| Parchment grain | Built as inline SVG `feTurbulence` | No image request; ~0.4kb |
| Decorative rule | Built as inline SVG | Diamond-and-line, used between sections |
| Wax seal disc | Built as CSS + SVG | Used for glosses and back-to-top |
| Icon set | Built as inline SVG sprite | book, person, scroll, quote, question, chevron, seal, star, search |
| Favicon | **Needed** | Derive from emblem, 32/180/512 |
| Character portraits | **Needed** | Currently initial-letter monogram placeholders on aged paper |
| Map of Osten Ard (SVG) | **Needed** | Blocked on location coordinates |
| Chapter header art | Optional | Currently a Roman numeral and rule; illustrations would improve the index |

---

## 10. Data gaps blocking full build

1. **49 of 55 chapters missing.** The site handles this — the index shows unwritten chapters as locked placeholders and `Next chapter` disables at 6.
2. **No `part` field.** The wireframe's "Part Two: Simon Pilgrim" line cannot be filled; the part filter is hidden.
3. **No location coordinates.** Map deferred.
4. **`spoiler_locked` is `false` on every record**, and `reread_notes` is `null` throughout. The two modes therefore differ only in the marginalia rail. If character and location entries get spoiler-locked variants, the mode difference becomes far more meaningful.
5. **Lore categories were inconsistent** in chapters 2–6 (`History/Culture` vs `Culture/History`). Normalized at build time to nine lowercase tags; upstream generation should emit these directly.
