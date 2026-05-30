# Unified Plan — IVAN → Tolkien-Inspired Dark Fantasy Rewrite

## Status Overview

This plan unifies `HIGH_LEVEL_PLAN.md` (extensive research inventory) and `EXECUTION_PLAN.md` (creative design + technical pipeline). It is organized as a sequential, commit-per-task checklist.

---

## What Has Already Been Completed (3 commits on main branch)

| Commit | Description | Files Changed |
|--------|-------------|---------------|
| `89b158b` | Phase 2: Rewrite `Script/define.dat` — rename enums, effect IDs, material IDs, team IDs, dungeon IDs for dark fantasy rewrite | `Script/define.dat` only |
| `c15930c` | Phase 2 (cont): Complete OMMEL→BRAMBLEBACK and VALPURIUM/VALPURUS renames across all codebase | 20 files: Script/*.dat, Main/Include/confdef.h, ivandef.h, definesvalidator.h, char.cpp, cmdcraft.cpp, gear.cpp, god.cpp, gods.cpp, human.cpp, lterras.cpp, materia.cpp, team.cpp |
| `e7bba90` | Update Valpurus→Valpuris, Elpuri→Malgorath the Blight-Beast, Golden Eagle Shirt→Shirt of Golden Hawk, Attnam→Oakhaven; Rename story state variables | `Main/Source/game.cpp`, `Main/Source/human.cpp`, `PLAN.md` |

**What this means:** The define.dat enums have been renamed (OMMEL_→BRAMBLEBACK_, VALPURIUM→VALPURIS, etc.), and some high-level name swaps were done in game.cpp and human.cpp. However, **many old references remain** across the codebase that were NOT touched by these commits.

---

## What Remains — Detailed Inventory

### A. Script Data Files (Creative Content)

#### 1. `Script/material.dat` — 15 remaining old references
- `BANANA_PEEL`, `BANANA_FLESH`, `HOLY_BANANA_FLESH`, `BANANA_STOLLEN` — all banana family materials must be renamed to mango/mango-pit equivalents
- `FROG_FLESH` → must rename to BLIGHTTOAD_FLESH (the enum was already renamed in define.dat, but the material Config name and its ConsumeEndMessage/HitMessage references still use old names)

#### 2. `Script/item.dat` — ~27 remaining old references
- **Quest items with PostFixes:** `PostFix = "of Attnam"`, `"named Valpurus' Justifier"`, `"of Petrus"`, `"of the left nut of Petrus"`, `"of Valpurus"`, `"of Elpuri"`, `"of Xinroch"`
- **DescriptiveInfo text:** Multiple ~200-word lore descriptions referencing Decos, Richel, Petrus, Attnam, Tweraif, Xinroch, Elpuri, Valpuris Cathedral, etc.
- **Class names:** `banana`, `holybanana`, `bananapeels` classes still use old names in ITEM() macros

#### 3. `Script/char.dat` — ~30 remaining old references
- `FROG_FLESH` → BLIGHTTOAD_FLESH (enum renamed, but Config name and FleshMaterial references remain)
- `banana`, `Bananagrower` character type names still use old naming

#### 4. Dungeon `.dat` files — need review for remaining story text
All dungeon files in `Script/dungeons/` have been inventoried in HIGH_LEVEL_PLAN.md but not yet rewritten:
- `NewAttnam.dat`, `UnderwaterTunnel.dat`, `Attnam.dat`, `XinrochTomb.dat`, `AslonaCastle.dat`, `RebelCamp.dat`, `GoblinFort.dat`, `Pyramid.dat`, `BlackMarket.dat`, `FungalCave.dat`, `DarkForest.dat`, `Irinox.dat`, `Mondedr.dat`, `EmptyArea.dat`, `GloomyCaves.dat`

### B. C++ Source Files (Hardcoded Strings + Class Renames)

#### 5. `Main/Source/gods.cpp` — 2 references
- Lines 797, 805: `BANANA_FLESH` material reference in god blessing code

#### 6. `Main/Source/materia.cpp` — 2 references
- Line 278: `HM_FROG_FLESH` → needs rename to HM_BLIGHTTOAD_FLESH
- Line 322: `CEM_FROG_FLESH` → needs rename to CEM_BLIGHTTOAD_FLESH

#### 7. `Main/Source/rooms.cpp` — ~13 references
- Banana-specific logic in `bananadroparea`, Decos Bananas Co. shopkeeper message, New Attnam references

#### 8. `Main/Source/nonhuman.cpp` — ~10 references
- Ostrich AI: `HasDroppedBananas`, banana pickup/delivery loop tied to New Attnam/Tweraif

#### 9. Remaining C++ files with story strings (invented from HIGH_LEVEL_PLAN.md inventory)
The following files were inventoried but NOT yet modified after the 3 commits:
- `Main/Source/human.cpp` — ~62 remaining old references (Petrus, Decos, Richel, Attnam, Tweraif, Xinroch, Elpuri names in dialogue strings)
- `Main/Source/game.cpp` — ~16 remaining old references (opening sequence text, Richel Decos summons, letter to Petrus, Attnam description, banana present spawning)
- `Main/Source/gear.cpp` — artifact hit effect messages referencing Neerc Se-ulb, Mjolak, Vermis, Turox names
- `Main/Source/char.cpp` — death messages, evil ending victory text with Petrus/Mortifer references
- `Main/Source/lterras.cpp` — throne vision texts (Grandis Rana song, Petrus/Great Frog titles, Asamarum/E-numa sa-am katanas)
- `Main/Source/miscitem.cpp` — banana class methods (`banana::Zap()`, `bananapeels::StepOnEffect()`), "slipped on a banana peel" death message
- `Main/Source/team.cpp` — alarm ringing, angel dialogue ("We will defend the Holy Order!")

### C. Header Files (Class Definitions + Method Declarations)

#### 10. Header files needing class/method renames
| File | What Needs Changing |
|------|-------------------|
| `Main/Include/item.h` | `banana`, `holybanana`, `bananapeels` class definitions, `IsBanana()`, `IsBananaPeel()` methods |
| `Main/Include/miscitem.h` | `ITEM(banana, ...)`, `ITEM(holybanana, banana)`, `ITEM(bananapeels, item)` macros |
| `Main/Include/nonhuman.h` | `ostrich::HasDroppedBananas`, `IsBananaGrower()` method declarations |
| `Main/Include/human.h` | `CHARACTER(bananagrower, humanoid)`, `IsBananaGrower()`, `ReceiveHolyBanana()`, `AddHolyBananaConsumeEndMessage()` |
| `Main/Include/char.h` | `IsBananaGrower()`, `ReceiveHolyBanana()`, `AddHolyBananaConsumeEndMessage()` declarations |
| `Main/Include/rooms.h` | `ROOM(bananadroparea, room)` macro |
| `Main/Include/confdef.h` | `BANANA_PEEL`, `BANANA_FLESH`, `HOLY_BANANA_FLESH`, `BANANA_STOLLEN`, `FROG_FLESH`, `ROOM_BANANA_DROP_AREA` #define macros |
| `Main/Include/ivandef.h` | `CEM_FROG_FLESH`, `HM_FROG_FLESH` defines |
| `Main/Include/definesvalidator.h` | 27 validator checks for old names (BANANA_FLESH, BANANA_PEEL, etc.) |

### D. Lore Documents

#### 11. `Doc/Lore/Fiction/` — 14 TXT files
All need creative rewriting: Attnam.txt, DwarvenWars.txt, EncounterWithKamikazeDwarf.txt, God_titles.txt, Hedgehogs.txt, HistoryOfDarkKnighthood.txt, HistoryOfGolems.txt, HolyBanana.txt, NewAttnamLegacy.txt, Ommel.txt, SaalThul.txt, Turox.txt, Vermis.txt

#### 12. `Doc/Lore/HolyStack/` — 3 RTF + 2 TXT files
- `Titues.txt`, `ValpuriFAQ.txt` (TXT) — heavy rewrite needed
- `Mola_Mola.rtf`, `The_Great_Battle.rtf` (RTF) — need format conversion to TXT first, then rewrite

#### 13. Documentation files
- `MANUAL` (~400 lines, ~5 story references)
- `NEWS` (~640 lines, ~36+ story references)

### E. Audio Assets

#### 14. Sound effects (158 WAV files in `/Sound/`)
Most are generic combat/sfx. Some may need replacement:
- `enner.wav`, `ennerdeath.wav` — Enner Beast sounds → replace with Wraithstalker equivalents
- `siren4.wav`, `choir.wav`, `choir2.wav`, `cathedral.wav` — atmospheric, style change only

#### 15. Music (11 MIDI files in `/Music/`)
All generic dungeon/world themes — style change only, no replacement needed

### F. Graphics Assets

#### 16. PNG sprite sheets and tiles (~30+ files)
- `Char.png`, `Humanoid.png` — character sprites need full regeneration
- `Item.png`, `Item-outlined.png` — item icons need regeneration
- `WTerra.png`, `OLTerra.png`, `GLTerra.png` — terrain tiles need regeneration
- `Menu.png`, `Menu1-5.png`, `Symbol.png` — UI art needs regeneration
- `Enner.png` → Wraithstalker sprite, `IVlad.png` → Shadowpaw bunny sprite
- `Font.png`, `Font2.png`, `Font3.png` — font bitmaps (style change)
- `Effect.png`, `FOW.png`, `Smiley.png` — may keep or style-change

---

## Unified Implementation Plan

### Phase 0: Setup Audio/Visual Generation Infrastructure

Before generating any assets, we need to set up the tooling. This is a prerequisite for Phases 7+ (graphics) and optional for audio.

#### Task 0.1: Install Local Inference Stack
- **Image generation:** `wikeeyang/Flux2-Klein-9B-True-V2` via HuggingFace Diffusers
  - Requires: `pip install diffusers transformers accelerate torch soundfile safetensors`
  - GPU recommended (8GB+ VRAM), but CPU fallback possible with `accelerate`
  - Alternative for lower-end hardware: `stabilityai/stable-diffusion-xl-base-1.0` or `black-forest-labs/FLUX.1-schnell`
- **Audio generation:** For sound effects, use `facebook/musicgen-small` or `facebook/musicgen-medium` via Diffusers
  - MusicGen can generate short WAV clips from text prompts at command line
  - Alternative: `suno/bark` for voice/sfx, but MusicGen is more suitable for SFX
- **Audio conversion:** Install `ffmpeg` for converting between formats (MIDI→WAV if needed)

#### Task 0.2: Create Asset Generation Scripts
Create a Python package `tools/asset_gen/`:
```
tools/asset_gen/
├── __init__.py
├── image_generator.py    # Flux pipeline wrapper, batch generation
├── audio_generator.py    # MusicGen pipeline for SFX/music
├── asset_catalog.json    # JSON with dimensions/purposes/prompts per asset
└── utils.py              # Rate limiting, retry logic, validation
```

#### Task 0.3: Create Asset Catalog JSON
Generate a JSON file listing every PNG/WAV/MID that needs replacement, with:
- filename, current dimensions, pixel format
- purpose (sprite sheet, terrain tile, SFX, etc.)
- new creative prompt for the Tolkien-inspired setting
- priority level (must-replace vs style-change)

---

### Phase 1: Complete Script Data File Rewrites

These are text-only changes with no dependencies on other phases. Each `.dat` file is a self-contained unit.

#### Task 1.1: Rewrite `Script/material.dat`
**What to change:**
- Rename all banana-family materials: `BANANA_PEEL` → `MANGO_PIT`, `BANANA_FLESH` → `MANGO_FLESH`, `HOLY_BANANA_FLESH` → `SACRED_MANGO_FLESH`, `BANANA_STOLLEN` → `ATAVUS_STOLLEN`
- Rename `FROG_FLESH` → `BLIGHTTOAD_FLESH` (enum already renamed in define.dat)
- Rewrite all DescriptiveInfo text for materials that have lore descriptions
- Update cross-references: HardenedMaterial/SoftenedMaterial chains involving BANANA_STOLLEN

**How:** Use sed/grep to find all occurrences, then apply the EXECUTION_PLAN.md name mapping table. For descriptive text, use LLM generation with prompt template from section 7.2 of EXECUTION_PLAN.md.

**Verification:** `grep -c "BANANA_\|FROG_FLESH" Script/material.dat` should return 0 after completion.

#### Task 1.2: Rewrite `Script/item.dat`
**What to change:**
- Rename item classes in ITEM() macros: `banana` → `mango`, `holybanana` → `sacredmango`, `bananapeels` → `mangopits`
- Update all PostFix strings referencing old names (Attnam, Valpurus, Petrus, Elpuri, Xinroch, Decos)
- Rewrite all DescriptiveInfo text (~200-word lore blocks for unique items)
- Update god attachment references where god names changed

**How:** This is the largest single file (~8000 lines). Process in batches:
1. First pass: mechanical renames (class names, PostFix strings) using sed
2. Second pass: LLM-generated DescriptiveInfo rewrites for each unique item with lore
3. Third pass: cross-reference validation

**Verification:** `grep -c "banana\|Banana\|Valpurus\|Attnam\|Tweraif\|Elpuri\|Xinroch\|Decos\|Richel\|Petrus" Script/item.dat` should return 0.

#### Task 1.3: Rewrite `Script/char.dat`
**What to change:**
- Rename `FROG_FLESH` → `BLIGHTTOAD_FLESH` in FleshMaterial references
- Rename character types: `bananagrower` → `croptender`, update IsBananaGrower() references
- Rewrite creature descriptions and dialogue text referencing old names

**How:** Similar batch approach — mechanical renames first, then LLM for descriptive text.

**Verification:** `grep -c "FROG_FLESH\|banana\|Bananagrower" Script/char.dat` should return 0.

#### Task 1.4: Rewrite Dungeon `.dat` Files
Process each dungeon file in `Script/dungeons/`:
- Rename level descriptions and short descriptions (e.g., "New Attnam" → "Oakhaven", "Tomb of Xinroch" → "Crypt of Khaz-Zadm")
- Update all sign text referencing old names
- Rewrite LevelMessage strings with new setting flavor
- Update OTerrainMap references (BRICK_PROPAGANDA, BANANA_TREE, etc.)

**Order:** Start with story-critical dungeons first:
1. `NewAttnam.dat` — Freedom Quest starting area
2. `UnderwaterTunnel.dat` — Travel route
3. `Attnam.dat` — Cathedral city
4. `XinrochTomb.dat` — 11-level necromancy dungeon
5. `AslonaCastle.dat`, `RebelCamp.dat` — Civil war arcs
6. Remaining dungeons (GoblinFort, Pyramid, BlackMarket, FungalCave, etc.)

**Verification:** After each file, grep for old names to confirm zero matches.

---

### Phase 2: Complete C++ Source File Rewrites

These changes depend on the new names established in Phase 1. Process files from most-to-least story-critical.

#### Task 2.1: Rewrite `Main/Source/human.cpp` (~62 remaining references)
**What to change:** All hardcoded dialogue strings referencing old names:
- Petrus → Archpriest Valerius Cordatus (or just "Archpriest")
- Decos/Richel → Lord Regent Valerius Decimus
- Attnam/Tweraif → Oakhaven / Valpuris
- Elpuri → Malgorath the Blight-Beast
- Xinroch → Khaz-Zadm
- All quest dialogue text blocks (Petrus quest chain, XinrochTomb necromancer dialogue, Freedom Quest lore, Aslona civil war dialogues)

**How:** This is the largest C++ file (~246KB). Process by function:
1. `priest::BeTalkedTo()` — Petrus quest chain (~lines 650-840)
2. `necromancer::BeTalkedTo()` — XinrochTomb quest (~lines 5120-5240)
3. `tweraifpriest::BeTalkedTo()` — Freedom Quest lore (~lines 7100-7200)
4. `imperialist::BeTalkedTo()` — Decos Bananas Co. dialogue (~lines 5500-5580)
5. `aslonawizard::BeTalkedTo()`, `aslonacaptain::BeTalkedTo()`, `harvan::BeTalkedTo()`, `lordregent::BeTalkedTo()` — Civil war dialogues

**Verification:** `grep -c "Valpurus\|Attnam\|Tweraif\|Elpuri\|Xinroch\|Decos\|Richel\|Petrus" Main/Source/human.cpp` should return 0.

#### Task 2.2: Rewrite `Main/Source/game.cpp` (~16 remaining references)
**What to change:**
- Opening sequence text (lines ~790-830): banana colony, Decos mansion summons, letter delivery premise, Attnam description
- Banana present spawning (line 913): `banana::Spawn()` → `mango::Spawn()`
- Holy banana reference (line 1056): `holybanana::Spawn()` → `sacredmango::Spawn()`
- Decos ad shirt contract dialogue (lines ~6430-6450)

**How:** Direct string replacement + LLM rewrite for opening narrative.

#### Task 2.3: Rewrite `Main/Source/gods.cpp` (2 references)
- Lines 797, 805: `BANANA_FLESH` → `MANGO_FLESH` in god blessing code

#### Task 2.4: Rewrite `Main/Source/materia.cpp` (2 references)
- Line 278: `HM_FROG_FLESH` → `HM_BLIGHTTOAD_FLESH`
- Line 322: `CEM_FROG_FLESH` → `CEM_BLIGHTTOAD_FLESH`

#### Task 2.5: Rewrite `Main/Source/gear.cpp` (artifact hit effect messages)
**What to change:** Artifact names in ADD_MESSAGE strings:
- "Neerc Se-ulb's life-draining energies" → "Nethervane's life-draining energies"
- "Mjolak's unholy energy" → "Thunderfist's unholy energy"
- "Vermis sends %s on a sudden journey" → "Soulthorn sends %s on a sudden journey"
- "full force of Turox" / "Turox's explosion" → "Dawnbreaker" equivalents

**How:** Search for artifact name strings in ADD_MESSAGE calls and replace.

#### Task 2.6: Rewrite `Main/Source/rooms.cpp` (~13 references)
**What to change:**
- `cathedral::Enter()` — Cathedral of Valpuris description
- `bananadroparea::DropItem()` — Victory text (mango seedling planting), score entry
- `shop::DropItem()` (NEW_ATTNAM config) — Decos Bananas Co. monopoly message
- `sumoarena::CheckDestroyTerrain()` — New Attnam reference

**How:** Direct string replacement with new setting names.

#### Task 2.7: Rewrite `Main/Source/nonhuman.cpp` (~10 references)
**What to change:**
- Ostrich AI logic (lines ~725-806): `HasDroppedBananas`, banana pickup/delivery loop
- Replace with Skygull messenger bird behavior tied to Oakhaven

#### Task 2.8: Rewrite `Main/Source/char.cpp` (story strings)
**What to change:**
- Evil ending victory text (lines ~1563-1580): undead voice greeting, Petrus name, Avatar of Chaos title
- Death score entries referencing story states
- Function renames: `HasHeadOfElpuri()` → `HasHeartOfMalgorath()`, `HasPetrussNut()` → `HasArchpriestsRelic()`, `HasGoldenEagleShirt()` → `HasGoldenHawkTunic()`

#### Task 2.9: Rewrite `Main/Source/lterras.cpp` (throne victory texts)
**What to change:**
- Attnam throne vision (lines ~248-283): Grandis Rana song, Petrus/Great Frog titles, high priest victory text
- Aslona throne vision (lines ~286-315): katana names (Asamarum, E-numa sa-am), "Long live the king!"
- Xinroch Tomb altar victory (lines ~795-828): Master Dark Knight title, Unholy Order of Infuscor

#### Task 2.10: Rewrite `Main/Source/miscitem.cpp` (banana class strings)
**What to change:**
- Line 946: "slipped on a banana peel" → "slipped on a mango pit"
- Line 2267: encryptedscroll message referencing Petrus → Archpriest
- Lines 2465, 2471, 2479: banana::Zap() jam messages → mango::Zap()

#### Task 2.11: Rewrite `Main/Source/team.cpp` (2 references)
- Line 97: "You hear an alarm ringing." — keep or adapt
- Line 120: "We will defend the Holy Order!" → new setting-appropriate angel dialogue

---

### Phase 3: Header File Updates

These are mechanical renames that must match the changes in Phases 1-2.

#### Task 3.1: Update `Main/Include/item.h`
- Rename class definitions: `banana` → `mango`, `holybanana` → `sacredmango`, `bananapeels` → `mangopits`
- Rename methods: `IsBanana()` → `IsMango()`, `IsBananaPeel()` → `IsMangoPit()`

#### Task 3.2: Update `Main/Include/miscitem.h`
- Update ITEM() macros for renamed classes

#### Task 3.3: Update `Main/Include/nonhuman.h`
- Rename `HasDroppedBananas` → `HasDeliveredSkygulls` (or similar)
- Update method declarations

#### Task 3.4: Update `Main/Include/human.h`
- Rename `CHARACTER(bananagrower, humanoid)` → `CHARACTER(croptender, humanoid)`
- Rename methods: `IsBananaGrower()` → `IsCropTender()`, `ReceiveHolyBanana()` → `ReceiveSacredMango()`, `AddHolyBananaConsumeEndMessage()` → `AddSacredMangoConsumeEndMessage()`

#### Task 3.5: Update `Main/Include/char.h`
- Rename method declarations to match human.h changes

#### Task 3.6: Update `Main/Include/rooms.h`
- Rename `ROOM(bananadroparea, room)` → `ROOM(mangodroparea, room)` or new name

#### Task 3.7: Update `Main/Include/confdef.h`
- Rename #define macros: `BANANA_PEEL` → `MANGO_PIT`, `BANANA_FLESH` → `MANGO_FLESH`, `HOLY_BANANA_FLESH` → `SACRED_MANGO_FLESH`, `BANANA_STOLLEN` → `ATAVUS_STOLLEN`, `FROG_FLESH` → `BLIGHTTOAD_FLESH`, `ROOM_BANANA_DROP_AREA` → new name

#### Task 3.8: Update `Main/Include/ivandef.h`
- Rename `CEM_FROG_FLESH` → `CEM_BLIGHTTOAD_FLESH`, `HM_FROG_FLESH` → `HM_BLIGHTTOAD_FLESH`

#### Task 3.9: Update `Main/Include/definesvalidator.h`
- Update all 27 validator checks for renamed materials/effects

---

### Phase 4: Lore Document Rewrites

These are standalone text files that can be processed in any order. Each file is a self-contained unit.

#### Task 4.1: Rewrite `Doc/Lore/Fiction/Attnam.txt`
- History of Valpuris Cathedral and the Aethelgard Empire
- Replace all references to Perttuera, Pertturia, Attnam, Valpuri, Decos, Petrus

#### Task 4.2: Rewrite `Doc/Lore/Fiction/DwarvenWars.txt`
- Keep structure (epic history), rename locations/characters to Tolkien-inspired equivalents
- Khaz-zadm mines, Divine War artifacts

#### Task 4.3: Rewrite `Doc/Lore/Fiction/EncounterWithKamikazeDwarf.txt`
- First-person dwarf narrative — already partially aligned with new pantheon (Great Tree Puu)
- Update remaining old references

#### Task 4.4: Rewrite `Doc/Lore/Fiction/God_titles.txt`
- All Latin titles referencing Petrus, Valpurus/Valpuri, Great Frog → new pantheon titles

#### Task 4.5: Rewrite `Doc/Lore/Fiction/Hedgehogs.txt`
- Replace hedgehog lore with Thornback Porcupine equivalent

#### Task 4.6: Rewrite `Doc/Lore/Fiction/HistoryOfDarkKnighthood.txt`
- Rename Xinroch → Khaz-Zadm, Dark Knights → Unholy Order of Infuscor
- Update Divine War narrative

#### Task 4.7: Rewrite `Doc/Lore/Fiction/HistoryOfGolems.txt`
- Rename deities in golem creation lore

#### Task 4.8: Rewrite `Doc/Lore/Fiction/HolyBanana.txt`
- Replace with Sacred Mango origin story (Sage Orpheus → Seges, mango discovery)

#### Task 4.9: Rewrite `Doc/Lore/Fiction/NewAttnamLegacy.txt`
- Poem about Oakhaven under Decimus's tyranny

#### Task 4.10: Rewrite `Doc/Lore/Fiction/Ommel.txt`
- Replace with Brambleback creature encyclopedia entry

#### Task 4.11: Rewrite `Doc/Lore/Fiction/SaalThul.txt`
- Rename Saal'Thul → Shade Vespera, update deity/city references

#### Task 4.12: Rewrite `Doc/Lore/Fiction/Turox.txt`
- Rename Turox → Dawnbreaker, Fortress Prym → new name

#### Task 4.13: Rewrite `Doc/Lore/Fiction/Vermis.txt`
- Rename Vermis → Soulthorn, Karl → Brother Aldric the Scholar

#### Task 4.14: Convert and rewrite RTF files in `Doc/Lore/HolyStack/`
- `Mola_Mola.rtf`, `The_Great_Battle.rtf`: Convert to TXT using `pandoc` or `libreoffice --headless --convert-to txt`
- Then rewrite content with new setting names

#### Task 4.15: Rewrite `Doc/Lore/HolyStack/Titues.txt`
- All Latin titles referencing Petrus, Valpurus/Valpuri → new pantheon

#### Task 4.16: Rewrite `Doc/Lore/HolyStack/ValpuriFAQ.txt`
- Heavy rewrite — entire in-character FAQ for new setting
- Replace Linux/Windows parody with setting-appropriate tech references
- Update all god names, locations, organization acronyms

#### Task 4.17: Rewrite `Doc/Lore/HolyStack/README.txt`
- Directory description referencing Valpuri/Great Frog → new deity

---

### Phase 5: Documentation Updates

#### Task 5.1: Rewrite `MANUAL` file
- ~5 story references: forum name, website URL, Valpurus example in alignment explanation

#### Task 5.2: Rewrite `NEWS` changelog
- ~36+ story references throughout historical changelog entries
- Keep dates and structure; adapt all setting-specific names

---

### Phase 6: Sound Effects

#### Task 6.1: Identify WAV files needing replacement
- `enner.wav`, `ennerdeath.wav` — Enner Beast → Wraithstalker sounds
- Any other creature-specific SFX that reference renamed creatures

#### Task 6.2: Generate new sound effects using MusicGen
```bash
# Example: generate a forest predator roar
python tools/asset_gen/audio_generator.py \
  --prompt "dark fantasy forest predator growl, menacing, deep" \
  --output Sound/wraithstalker.wav \
  --duration 1.0
```

#### Task 6.3: Update `Sound/SoundEffects.cfg`
- Replace references to old creature names in regex patterns
- Update file references for replaced SFX

---

### Phase 7: Graphics Generation

This phase requires the infrastructure from Phase 0 and the creative design from EXECUTION_PLAN.md sections 1-6.

#### Task 7.1: Generate Character Sprite Sheets
**`Char.png`** — Dark fantasy adventurer sprites in medieval armor/clothing
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy roguelike character sprite sheet, medieval adventurer in worn leather and chainmail, pixel art style, 16x16 tiles on white background" \
  --width 256 --height 256 \
  --output Graphics/Char.png
```

**`Humanoid.png`** — Fantasy NPCs: priests, knights, merchants, rebels
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy roguelike humanoid NPC sprite sheet, various classes (priest in robes, knight in plate armor, merchant in cloak, rebel in leather), pixel art style, 16x16 tiles" \
  --width 256 --height 256 \
  --output Graphics/Humanoid.png
```

#### Task 7.2: Generate Item Icons
**`Item.png`**, **`Item-outlined.png`** — Fantasy RPG item icons
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy RPG item icon sheet, swords maces spears whips staves shields potions scrolls rings amulets, pixel art style on white background" \
  --width 256 --height 128 \
  --output Graphics/Item.png

# Then generate outlined version (white border) using image processing
python tools/asset_gen/utils.py outline --input Graphics/Item.png --output Graphics/Item-outlined.png
```

#### Task 7.3: Generate Terrain Tiles
**`WTerra.png`** — World terrain tiles (snow, glacier, desert, tundra, jungle, evergreen forest, steppe)
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy world map terrain tile set, snow plains glacier ice desert dunes tundra taiga dense evergreen forest rolling grassland, pixel art style, top-down view" \
  --width 512 --height 256 \
  --output Graphics/WTerra.png
```

**`OLTerra.png`** — Overworld terrain tiles with landmarks
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy overworld terrain tiles, cathedral ruins castle towers ancient stone walls forest paths mountain trails, pixel art style" \
  --width 512 --height 256 \
  --output Graphics/OLTerra.png
```

**`GLTerra.png`** — Ground terrain tiles (stone, gravel, bone, ice, coal, steel, obsidian)
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy dungeon ground tile set, stone floors gravel paths bone dust ice sheets coal seams dark steel obsidian, pixel art style" \
  --width 512 --height 256 \
  --output Graphics/GLTerra.png
```

#### Task 7.4: Generate UI Art
**`Menu.png`, `Menu1-5.png`** — Dark fantasy UI with medieval borders
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy game menu screen, ornate medieval border design, parchment texture, gothic lettering space for text, pixel art style" \
  --width 640 --height 480 \
  --output Graphics/Menu.png
```

**`Symbol.png`** — New IVAN logo: dark fantasy crest/emblem
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy game logo emblem, shield with crossed swords and a great tree, gothic design, pixel art style on transparent background" \
  --width 128 --height 128 \
  --output Graphics/Symbol.png
```

#### Task 7.5: Generate Creature Sprites
**`Enner.png` → `Wraithstalker.png`** — Large predatory forest creature with glowing eyes
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy roguelike monster sprite, massive predatory forest beast with glowing yellow eyes and shadowy fur, pixel art style on white background" \
  --width 256 --height 128 \
  --output Graphics/Wraithstalker.png
```

**`IVlad.png → Shadowpaw.png`** — Bunny companion sprite
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy roguelike pet sprite, small dark bunny with glowing eyes, pixel art style on white background" \
  --width 64 --height 64 \
  --output Graphics/Shadowpaw.png
```

#### Task 7.6: Generate Font Bitmaps (Style Change)
**`Font.png`, `Font2.png`, `Font3.png`** — Medieval/fantasy style bitmap fonts
```bash
python tools/asset_gen/image_generator.py \
  --prompt "medieval gothic bitmap font, complete ASCII character set including uppercase lowercase numbers punctuation, pixel art style on white background" \
  --width 512 --height 64 \
  --output Graphics/Font.png
```

#### Task 7.7: Generate Remaining Assets
- `Effect.png` — Fantasy spell effects (fire, lightning, dark energy, holy light)
- `FOW.png` — Fog of war overlay pattern
- `Smiley.png` — Expression sprites (keep or replace)
- `Cursor.png` — Fantasy arrow/crosshair cursor

---

### Phase 8: Validation & Testing

#### Task 8.1: Run Balance Validator
```bash
python tools/asset_gen/balance_validator.py \
  --old-backup backup_before_rewrite/ \
  --new-files Script/ \
  --output validation_report.txt
```
Verify all numerical values (PriceModifier, NutritionValue, StrengthValue, Color RGB, Enchantment levels) are unchanged.

#### Task 8.2: String Search for Missed References
```bash
# Check for any remaining old references across the entire codebase
grep -r "banana\|Banana\|BANANA_\|Valpurus\|Attnam\|Tweraif\|Elpuri\|Xinroch\|Decos\|Richel\|Petrus\|FROG_FLESH\|OMMEL_" \
  --include="*.cpp" --include="*.h" --include="*.dat" --include="*.txt" . | grep -v ".git/" > missed_references.txt

# If missed_references.txt is non-empty, fix remaining references
```

#### Task 8.3: Compile Test
```bash
mkdir build && cd build
cmake .. && make -j$(nproc)
```
Verify the project compiles without errors after all renames.

#### Task 8.4: Runtime Testing
- Launch the game and verify opening sequence displays correctly
- Test each story arc (Freedom Quest, XinrochTomb, Aslona Civil War)
- Verify all dialogue text uses new setting names
- Check that renamed classes work correctly (mango zapping, mangopit slipping, etc.)

---

## Commit Strategy

After completing each task above:
1. Stage changes: `git add -A`
2. Commit with descriptive message: `git commit -m "Phase X.Y: [description]"`
3. Update this PLAN.md to mark the completed task as `[x]`

This ensures every logical unit of work is tracked in git history and the plan stays synchronized with progress.

---

## Summary of Remaining Work by Category

| Category | Tasks | Estimated Effort |
|----------|-------|-----------------|
| **Script Data Files** | 1.1-1.4 (material.dat, item.dat, char.dat, dungeons/) | Heavy — ~20K lines total across all .dat files |
| **C++ Source Rewrites** | 2.1-2.11 (human.cpp, game.cpp, gear.cpp, rooms.cpp, etc.) | Heavy — ~500+ hardcoded strings to rewrite |
| **Header File Updates** | 3.1-3.9 (mechanical renames) | Light-Medium — straightforward find/replace |
| **Lore Documents** | 4.1-4.17 (14 TXT + 2 RTF converted) | Medium — ~50K words of creative text to rewrite |
| **Documentation** | 5.1-5.2 (MANUAL, NEWS) | Light — ~1000 lines total |
| **Sound Effects** | 6.1-6.3 (identify + generate replacements) | Medium — depends on how many SFX need replacement |
| **Graphics Generation** | 7.1-7.7 (~20 PNG files) | Heavy — requires GPU and inference time per asset |
| **Validation & Testing** | 8.1-8.4 (balance check, string search, compile, runtime) | Medium — thorough testing required |
