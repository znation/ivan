# Unified Plan — IVAN → Tolkien-Inspired Dark Fantasy Rewrite

## Status Overview

This plan unifies `HIGH_LEVEL_PLAN.md` (extensive research inventory) and `EXECUTION_PLAN.md` (creative design + technical pipeline). It is organized as a sequential, commit-per-task checklist. Each task has a `[ ]` checkbox; mark `[x]` after committing.

**LLM tool:** Use Claude directly for all narrative rewrites. Prompt templates for each content type are in `EXECUTION_PLAN.md` section 7.

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

#### 1. `Script/material.dat` — 17 remaining old references
- `BANANA_PEEL`, `BANANA_FLESH`, `HOLY_BANANA_FLESH`, `BANANA_STOLLEN` — all banana family materials must be renamed to mango/mango-pit equivalents
- `FROG_FLESH` → must rename to BLIGHTTOAD_FLESH
- `DARK_FROG_BLOOD`, `LIGHT_FROG_BLOOD` → `DARK_BLIGHTTOAD_BLOOD`, `LIGHT_BLIGHTTOAD_BLOOD` *(not in original plan)*

#### 2. `Script/item.dat` — ~22 remaining old references
- **Quest items with PostFixes:** `PostFix = "of Attnam"`, `"named Valpurus' Justifier"`, `"of Petrus"`, `"of the left nut of Petrus"`, `"of Valpurus"`, `"of Elpuri"`, `"of Xinroch"`
- **DescriptiveInfo text:** Multiple ~200-word lore descriptions referencing Decos, Richel, Petrus, Attnam, Tweraif, Xinroch, Elpuri, Valpuris Cathedral, etc.
- **Class names:** `banana`, `holybanana`, `bananapeels` classes still use old names in ITEM() macros

#### 3. `Script/char.dat` — ~29 remaining old references
- `FROG_FLESH` → BLIGHTTOAD_FLESH; `DARK_FROG_BLOOD`/`LIGHT_FROG_BLOOD` refs
- `banana`, `Bananagrower` character type names still use old naming

#### 4. Dungeon `.dat` files — only 3 need changes (others already clean)
| File | References |
|---|---|
| `Script/dungeons/NewAttnam.dat` | 14 |
| `Script/dungeons/Attnam.dat` | 9 |
| `Script/dungeons/XinrochTomb.dat` | 3 |
| All other 12 dungeon files | 0 (already clean) |

### B. C++ Source Files (Hardcoded Strings + Class Renames)

**Note:** Headers are updated in the same commit as their corresponding .cpp files — not as a separate phase — to keep the codebase compile-clean at every commit.

| File | References | Notes |
|---|---|---|
| `Main/Source/human.cpp` | ~62 | Largest; all dialogue strings, quest text |
| `Main/Source/game.cpp` | ~16 | Opening sequence, spawn calls |
| `Main/Source/worldmap.cpp` | 35 | Variable names in map-gen logic *(missing from original plan)* |
| `Main/Source/rooms.cpp` | ~13 | Cathedral text, bananadroparea, shop messages |
| `Main/Source/nonhuman.cpp` | ~10 | Ostrich AI, banana pickup/delivery |
| `Main/Source/lterras.cpp` | ~8 | Throne vision texts |
| `Main/Source/miscitem.cpp` | ~6 | banana::Zap(), slip message, encrypted scroll |
| `Main/Source/char.cpp` | ~4 | Evil ending, death score, function renames |
| `Main/Source/gods.cpp` | 2 | BANANA_FLESH in god blessing code |
| `Main/Source/materia.cpp` | 2 | HM_FROG_FLESH, CEM_FROG_FLESH |
| `Main/Source/team.cpp` | 1 | Holy Order dialogue |
| `Main/Source/gear.cpp` | ~5 | Artifact hit message strings |
| `Main/Source/cmdcraftfilters.cpp` | 3 | dynamic_cast<banana*> type casts *(missing from original plan)* |
| `Main/Source/cmdcraft.cpp` | 2 | Comments only *(missing from original plan)* |
| `Main/Source/stack.cpp` | 1 | Comment only *(missing from original plan)* |

### C. Header Files (updated with their paired .cpp)

| File | What Needs Changing | Paired With |
|------|-------------------|----|
| `Main/Include/item.h` | `banana`→`mango`, `holybanana`→`sacredmango`, `bananapeels`→`mangopits` class defs; `IsBanana()`→`IsMango()` | Task 2.10 (miscitem.cpp) |
| `Main/Include/miscitem.h` | ITEM() macros for renamed classes | Task 2.10 (miscitem.cpp) |
| `Main/Include/nonhuman.h` | `HasDroppedBananas`→`HasDroppedMangos` | Task 2.7 (nonhuman.cpp) |
| `Main/Include/human.h` | `CHARACTER(bananagrower,...)` → `croptender`; method renames | Task 2.1 (human.cpp) |
| `Main/Include/char.h` | Method declarations to match human.h renames | Task 2.8 (char.cpp) |
| `Main/Include/rooms.h` | `ROOM(bananadroparea, room)` → `ROOM(mangodroparea, room)` | Task 2.6 (rooms.cpp) |
| `Main/Include/confdef.h` | All BANANA_*/FROG_FLESH/ROOM_BANANA_DROP_AREA #defines | Task 2.6 (rooms.cpp) |
| `Main/Include/ivandef.h` | `CEM_FROG_FLESH`, `HM_FROG_FLESH` defines | Task 2.4 (materia.cpp) |
| `Main/Include/definesvalidator.h` | Update 27 validator checks to new names | Task 2.15 (final cleanup) |

### D. Lore Documents

#### `Doc/Lore/Fiction/` — 13 TXT files + 1 RTF
Attnam.txt, DwarvenWars.txt, EncounterWithKamikazeDwarf.txt, God_titles.txt, Hedgehogs.txt, HistoryOfDarkKnighthood.txt, HistoryOfGolems.txt, HolyBanana.txt, NewAttnamLegacy.txt, Ommel.txt, SaalThul.txt, Turox.txt, Vermis.txt, **Creation.rtf** *(missing from original plan)*

#### `Doc/Lore/HolyStack/` — 2 TXT + 2 RTF + media files
- `Titues.txt`, `ValpuriFAQ.txt` (TXT) — heavy rewrite needed
- `Mola_Mola.rtf`, `The_Great_Battle.rtf` (RTF) — pandoc convert first
- `Excisio.mp3`, `Incede_frater!.mp3`, `Valpuri_is_alive!.mp3` — rename *(missing from original plan)*
- `Valpuri.jpg`, `Valpuri2.jpg`, `Valpuri3.jpg`, `Valpuri_ON_MAHTAVA.JPG` — rename *(missing from original plan)*

### E. Documentation
- `MANUAL` (~400 lines, ~5 story references)
- `NEWS` (~640 lines, ~36+ story references)

### F. Audio Assets
- `enner.wav`, `ennerdeath.wav` → replace with Wraithstalker equivalents
- `Sound/SoundEffects.cfg` — update creature name references after reading its content

### G. Graphics Assets (~30 PNG files)
- `Enner.png` → `Wraithstalker.png`, `IVlad.png` → `Shadowpaw.png` (must-replace)
- `Char.png`, `Humanoid.png`, `Item.png`, terrain tiles, UI art (regenerate)
- `Font.png`, `Effect.png`, `FOW.png`, `Smiley.png`, `Cursor.png` (style change or keep)

---

## Unified Implementation Plan

### Pre-flight: Safety Checkpoint

```bash
git tag pre-rewrite-checkpoint
mkdir -p build && cd build && cmake .. && make -j$(nproc) 2>&1 | tail -20
```

---

### Phase 0: Setup Infrastructure + Validator Prep

#### Task 0.0: [x] Update `definesvalidator.h` to Accept New Names
**Why first:** The validator has 27 `#error` checks that fire on old names. Phase 1 dat changes remove old names, but Phase 2 C++ changes may lag — leaving a window where old names still exist in C++. Disabling or updating the validator first prevents spurious compile errors during the transition.

**Action:** Update all 27 `#error` checks in `Main/Include/definesvalidator.h` to validate the NEW names (MANGO_PIT, MANGO_FLESH, BLIGHTTOAD_FLESH, etc.) rather than the old ones.

**Verification:** `grep -c "#error" Main/Include/definesvalidator.h` → 0 (all checks removed/replaced — done as part of Task 2.15).

#### Task 0.1: [x] Install Local Inference Stack
- Virtualenv: `~/venv` — torch 2.9.1+rocm6.3, transformers 5.8.0, PIL 12.1.1, diffusers 0.38.0, soundfile 0.13.1, safetensors, accelerate
- GPU: AMD Radeon Pro Vega 48 (/dev/kfd exists) — **GPU blocked**: user needs `sudo usermod -aG render $USER` then re-login to gain `render` group access. Scripts fall back to CPU.
- ffmpeg: not installed — audio_generator.py uses pure-Python WAV writing (no ffmpeg dependency)
- `~/venv/bin/python tools/asset_gen/audio_generator.py` to invoke

#### Task 0.2: [x] Create `tools/asset_gen/` Package
```
tools/asset_gen/
├── __init__.py
├── image_generator.py    # Flux pipeline wrapper: --prompt --width --height --output
├── audio_generator.py    # MusicGen/Bark wrapper: --prompt --output --duration
├── outline_util.py       # PIL-based white-border outline for Item-outlined.png
├── balance_validator.py  # Reads old vs new .dat files, compares all numeric fields
└── asset_catalog.json    # Per-asset: filename, dimensions, pixel format, prompt, priority
```

**`balance_validator.py` must:**
- Parse `.dat` files extracting all numeric values (NutritionValue, StrengthValue, PriceModifier, Enchantment, Color RGB)
- Compare old vs new and output a diff report
- Exit nonzero if any numeric value changed

#### Task 0.3: [x] Populate `asset_catalog.json`
All 25 PNG files catalogued with exact dimensions, new filenames, generation prompts, and priorities.
- `must-replace` (2): Wraithstalker.png (800x600), Shadowpaw.png (800x600)
- `style-change` (16): Char, Humanoid, Item, terrain tiles, menus, fonts, Symbol, Effect, Smiley, Cursor
- `derived` (3): Char-outlined, Humanoid-outlined, Item-outlined (generated via outline_util.py)
- `keep` (2): FOW.png, Cursor.png
See `tools/asset_gen/asset_catalog.json` for full prompts.

---

### Phase 1: Complete Script Data File Rewrites

Text-only changes in `.dat` files; no C++ dependencies. Run grep verification after each file.

#### Task 1.1: [x] Rewrite `Script/material.dat` (17 references)

**Exact substitutions:**
| Old | New |
|---|---|
| `Config BANANA_PEEL` | `Config MANGO_PIT` |
| `NameStem = "banana peel"` | `NameStem = "mango pit"` |
| `NaturalForm = bananapeels` | `NaturalForm = mangopits` |
| `Config BANANA_FLESH` | `Config MANGO_FLESH` |
| `NameStem = "banana"` | `NameStem = "mango"` |
| `HardenedMaterial = BANANA_STOLLEN` | `HardenedMaterial = ATAVUS_STOLLEN` |
| `Config HOLY_BANANA_FLESH` | `Config SACRED_MANGO_FLESH` |
| `NameStem = "holy banana"` | `NameStem = "sacred mango"` |
| `SoftenedMaterial = BANANA_FLESH` | `SoftenedMaterial = MANGO_FLESH` |
| `EFFECT_HOLY_BANANA` | `EFFECT_SACRED_MANGO` |
| `CEM_HOLY_BANANA` | `CEM_SACRED_MANGO` |
| `Config BANANA_STOLLEN` | `Config ATAVUS_STOLLEN` |
| `NameStem = "banana stollen"` | `NameStem = "stollen of Atavus"` |
| `Config DARK_FROG_BLOOD` | `Config DARK_BLIGHTTOAD_BLOOD` |
| `NameStem = "dark frog blood"` | `NameStem = "dark blighttoad blood"` |
| `Config LIGHT_FROG_BLOOD` | `Config LIGHT_BLIGHTTOAD_BLOOD` |
| `NameStem = "light frog blood"` | `NameStem = "light blighttoad blood"` |

Use Claude to rewrite all DescriptiveInfo text for banana-family and frog-flesh materials.

**Verification:** `grep -c "banana\|Banana\|BANANA\|FROG_FLESH\|frog blood\|frog flesh" Script/material.dat` → 0

#### Task 1.2: [x] Rewrite `Script/item.dat` (22 references)

**Mechanical renames:**
| Old | New |
|---|---|
| `ITEM(banana,` | `ITEM(mango,` |
| `ITEM(holybanana, banana)` | `ITEM(sacredmango, mango)` |
| `ITEM(bananapeels,` | `ITEM(mangopits,` |
| `PostFix = "of Attnam"` | `PostFix = "of Oakhaven"` |
| `"named Valpurus' Justifier"` | `"named Valpuris' Justifier"` |
| `"of Petrus"` | `"of the Archpriest"` |
| `"of the left nut of Petrus"` | `"of the Archpriest's Relic"` |
| `"of Valpurus"` | `"of Valpuris"` |
| `"of Elpuri"` | `"of Malgorath"` |
| `"of Xinroch"` | `"of Khaz-Zadm"` |

Use Claude to rewrite DescriptiveInfo blocks for all named artifacts (Justifier, Shirt of Golden Hawk, Nethervane, Thunderfist, Soulthorn, Dawnbreaker).

**Verification:** `grep -c "banana\|Banana\|Valpurus\b\|Attnam\|Tweraif\|Elpuri\|Xinroch\|Decos\|Richel\|Petrus" Script/item.dat` → 0

#### Task 1.3: [x] Rewrite `Script/char.dat` (29 references)

**Mechanical renames:**
| Old | New |
|---|---|
| `FleshMaterial = FROG_FLESH` | `FleshMaterial = BLIGHTTOAD_FLESH` |
| `DARK_FROG_BLOOD` refs | `DARK_BLIGHTTOAD_BLOOD` |
| `LIGHT_FROG_BLOOD` refs | `LIGHT_BLIGHTTOAD_BLOOD` |
| Config `bananagrower` | Config `croptender` |
| `DefaultName = "banana grower"` | `DefaultName = "crop tender"` |
| `banana::Spawn()` in char.dat | `mango::Spawn()` |

Use Claude to rewrite creature descriptions and NPC dialogue strings.

**Verification:** `grep -c "FROG_FLESH\|frog blood\|banana\|Bananagrower" Script/char.dat` → 0

#### Task 1.4: [x] Rewrite 3 Dungeon `.dat` Files (others already clean)

**`Script/dungeons/NewAttnam.dat`** (14 references):
- All "New Attnam" / "Tweraif" → "Oakhaven"
- LevelMessage strings with new setting flavor
- `bananadroparea` room refs → `mangodroparea`
- `BANANA_TREE` terrain/decoration references

**`Script/dungeons/Attnam.dat`** (9 references):
- All "Attnam" → "Valpuris" (city name)
- Petrus/Valpurus NPC references → Archpriest Valerius Cordatus / Valpuris
- LevelMessage strings updated

**`Script/dungeons/XinrochTomb.dat`** (3 references):
- "Xinroch" → "Khaz-Zadm"
- Dark Knight order name updated

**Verification:** `grep -c "banana\|Banana\|Attnam\|Tweraif\|Xinroch\|Petrus\|Elpuri" Script/dungeons/NewAttnam.dat Script/dungeons/Attnam.dat Script/dungeons/XinrochTomb.dat` → 0 for all

---

### Phase 2: C++ Source Files + Matching Headers

**Key principle:** Each task updates BOTH the .cpp source AND its corresponding header in the same commit. This keeps the codebase compile-clean at every step.

#### Task 2.1: [x] `Main/Source/human.cpp` + `Main/Include/human.h` (~62 refs)

**Dialogue strings to rewrite with Claude:**
- `bananagrower::BeTalkedTo()` (~line 3279): banana farming → mango tending
- `bananagrower::GetAICommand()` (~line 3442): string messages only; preserve logic
- `priest::BeTalkedTo()` (~lines 650–840): Petrus quest chain → Archpriest Valerius Cordatus
- `necromancer::BeTalkedTo()` (~lines 5120–5240): Xinroch → Khaz-Zadm
- `tweraifpriest::BeTalkedTo()` (~lines 7100–7200): Freedom Quest lore with Oakhaven/Decimus
- `imperialist::BeTalkedTo()` (~lines 5500–5580): Decos Bananas Co. → Decimus Harvest Co.
- Civil war dialogues: `aslonawizard`, `aslonacaptain`, `harvan`, `lordregent`

**Function/identifier renames in human.cpp:**
| Old | New |
|---|---|
| `bananagrower::` (all method defs) | `croptender::` |
| `HasDroppedBananas` | `HasDroppedMangos` |
| `IsBananaGrower()` | `IsCropTender()` |
| `ReceiveHolyBanana()` | `ReceiveSacredMango()` |
| `AddHolyBananaConsumeEndMessage()` | `AddSacredMangoConsumeEndMessage()` |

**human.h (same commit):**
- `CHARACTER(bananagrower, humanoid)` → `CHARACTER(croptender, humanoid)`
- All method declarations matching above renames

**Verification:** `grep -c "banana\|Banana\|Petrus\|Tweraif\|Xinroch\|Decos\|Richel\|Elpuri\|bananagrower\|BananaGrow" Main/Source/human.cpp Main/Include/human.h` → 0

#### Task 2.2: [x] `Main/Source/game.cpp` (~16 remaining references)

**What to change:**
- Opening sequence text (~lines 790–830): banana colony → mango grove, Decos mansion → Decimus estate, Attnam description → Valpuris. Use Claude for narrative rewrite.
- `banana::Spawn()` (~line 913) → `mango::Spawn()`
- `holybanana::Spawn()` (~line 1056) → `sacredmango::Spawn()`
- Decos ad shirt contract dialogue (~lines 6430–6450) → Decimus harvest contract
- Any remaining `Valpurus` → `Valpuris`, `Elpuri` → `Malgorath`, `Petrus` → Archpriest

**Verification:** `grep -c "banana\|Banana\|Valpurus\b\|Attnam\|Tweraif\|Elpuri\|Xinroch\|Decos\|Richel\|Petrus" Main/Source/game.cpp` → 0

#### Task 2.3: [x] `Main/Source/gods.cpp` (2 references)
- Lines 797, 805: `BANANA_FLESH` → `MANGO_FLESH`
- No header changes needed.

#### Task 2.4: [x] `Main/Source/materia.cpp` + `Main/Include/ivandef.h` (2+2 refs)

**materia.cpp:**
- Line 278: `HM_FROG_FLESH` → `HM_BLIGHTTOAD_FLESH`
- Line 322: `CEM_FROG_FLESH` → `CEM_BLIGHTTOAD_FLESH`

**ivandef.h (same commit):**
- `CEM_FROG_FLESH` → `CEM_BLIGHTTOAD_FLESH`
- `HM_FROG_FLESH` → `HM_BLIGHTTOAD_FLESH`

#### Task 2.5: [x] `Main/Source/gear.cpp` (artifact hit messages)

| Old | New |
|---|---|
| `"Neerc Se-ulb's life-draining energies"` | `"Nethervane's life-draining energies"` |
| `"Mjolak's unholy energy"` | `"Thunderfist's unholy energy"` |
| `"Vermis sends %s on a sudden journey"` | `"Soulthorn sends %s on a sudden journey"` |
| `"full force of Turox"` | `"full force of Dawnbreaker"` |
| `"Turox's explosion"` | `"Dawnbreaker's explosion"` |

No header changes needed.

#### Task 2.6: [x] `Main/Source/rooms.cpp` + `Main/Include/rooms.h` + `Main/Include/confdef.h` (~13 refs)

**rooms.cpp:**
- `cathedral::Enter()` — Cathedral of Valpuris description text
- `bananadroparea::DropItem()` → `mangodroparea::DropItem()`: victory text, score entry
- `shop::DropItem()` (NEW_ATTNAM config) — Decos Bananas Co. → Decimus Harvest Co.
- `sumoarena::CheckDestroyTerrain()` — New Attnam → Oakhaven

**rooms.h (same commit):**
- `ROOM(bananadroparea, room)` → `ROOM(mangodroparea, room)`

**confdef.h (same commit):**
| Old | New |
|---|---|
| `ROOM_BANANA_DROP_AREA` | `ROOM_MANGO_DROP_AREA` |
| `BANANA_PEEL` | `MANGO_PIT` |
| `BANANA_FLESH` | `MANGO_FLESH` |
| `HOLY_BANANA_FLESH` | `SACRED_MANGO_FLESH` |
| `BANANA_STOLLEN` | `ATAVUS_STOLLEN` |
| `FROG_FLESH` | `BLIGHTTOAD_FLESH` |

#### Task 2.7: [x] `Main/Source/nonhuman.cpp` + `Main/Include/nonhuman.h` (~10 refs)

**nonhuman.cpp:**
- Ostrich AI: `HasDroppedBananas` → `HasDroppedMangos`; banana pickup/delivery loop messages
- Ostrich display name → "skygull" in relevant NPC configs
- Delivery loop: `banana` item casts → `mango`; `bananapeels` → `mangopits`

**nonhuman.h (same commit):**
- `HasDroppedBananas` → `HasDroppedMangos` field

#### Task 2.8: [x] `Main/Source/char.cpp` + `Main/Include/char.h` (story strings)

**char.cpp:**
- Evil ending victory text (~lines 1563–1580): Petrus → Archpriest, Avatar of Chaos title
- Death score entries referencing story states
- Function renames: `HasHeadOfElpuri()` → `HasHeartOfMalgorath()`, `HasPetrussNut()` → `HasArchpriestsRelic()`, `HasGoldenEagleShirt()` → `HasGoldenHawkTunic()`

**char.h (same commit):** matching method declarations renamed

#### Task 2.9: [x] `Main/Source/lterras.cpp` (throne victory texts)
- Attnam throne vision (~lines 248–283): Grandis Rana song → Tolkien-flavored epic verse with Claude
- Aslona throne vision (~lines 286–315): katana names → Muramasa/Masamune; "Long live the king!"
- Xinroch Tomb altar (~lines 795–828): Master Dark Knight title → Unholy Order of Infuscor

#### Task 2.10: [x] `Main/Source/miscitem.cpp` + `Main/Include/item.h` + `Main/Include/miscitem.h`

**miscitem.cpp:**
- Line 946: `"slipped on a banana peel"` → `"slipped on a mango pit"`
- Line 2267: encryptedscroll message Petrus → Archpriest
- Lines 2465, 2471, 2479: `banana::Zap()` messages → `mango::Zap()`
- Method implementations: `banana::Zap()` → `mango::Zap()`, etc.

**item.h (same commit):**
| Old | New |
|---|---|
| `class banana` | `class mango` |
| `class holybanana : public banana` | `class sacredmango : public mango` |
| `class bananapeels` | `class mangopits` |
| `IsBanana()` | `IsMango()` |
| `IsBananaPeel()` | `IsMangoPit()` |

**miscitem.h (same commit):**
| Old | New |
|---|---|
| `ITEM(banana, materialcontainer)` | `ITEM(mango, materialcontainer)` |
| `ITEM(holybanana, banana)` | `ITEM(sacredmango, mango)` |
| `ITEM(bananapeels, item)` | `ITEM(mangopits, item)` |

#### Task 2.11: [x] `Main/Source/team.cpp` (1 reference)
- Line 120: `"We will defend the Holy Order!"` → `"We will defend the Sacred Order of Valpuris!"`

#### Task 2.12: [x] `Main/Source/worldmap.cpp` (35 references) *(ADDED — missing from original plan)*

**Variable/identifier renames — preserve all logic, rename identifiers only:**
| Old | New |
|---|---|
| `int DistanceToAttnam` | `int DistanceToValpuris` |
| `DistanceToAttnam(d)` | `DistanceToValpuris(d)` |
| `loc1.DistanceToAttnam` | `loc1.DistanceToValpuris` |
| `PerfectForAttnam` | `PerfectForValpuris` |
| `PerfectForNewAttnam` | `PerfectForOakhaven` |
| `continent* PetrusLikes` | `continent* ArchpriestsLikes` |
| `PetrusLikes` (all uses) | `ArchpriestsLikes` |
| `v2 NewAttnamPos` | `v2 OakhavenPos` |
| `NewAttnamPos` (all uses) | `OakhavenPos` |
| `"Valpurus shall not carry more continents!"` | `"Valpuris shall not carry more continents!"` |

All 35 occurrences are within worldmap.cpp; no header changes needed.

#### Task 2.13: [x] `Main/Source/cmdcraftfilters.cpp` (3 references) *(ADDED — missing from original plan)*

**Must be done AFTER item.h is updated in Task 2.10** (class names must exist):
- Line 31: `dynamic_cast<banana*>` → `dynamic_cast<mango*>`
- Line 33: `dynamic_cast<bananapeels*>` → `dynamic_cast<mangopits*>`
- Line 72: `dynamic_cast<holybanana*>` → `dynamic_cast<sacredmango*>`

#### Task 2.14: [x] `Main/Source/cmdcraft.cpp` + `Main/Source/stack.cpp` (comments only) *(ADDED)*
- `cmdcraft.cpp` line 69: `//potions, mines... also bananas xD` → remove or update comment
- `cmdcraft.cpp` line 2458: TODO mentioning `kiwi/banana` → `kiwi/mango`
- `stack.cpp` comment `/* 4 bananas */` → `/* 4 mangos */`

#### Task 2.15: [x] `Main/Include/definesvalidator.h` — Finalize New Name Validation
After all source/header renames are complete, update all 27 `#error` checks to enforce the new names (MANGO_PIT, MANGO_FLESH, BLIGHTTOAD_FLESH, etc.). This locks in the new naming convention going forward.

---

### Phase 3: Lore Document Rewrites

Standalone text files; independent of each other. Use Claude with the style guide from EXECUTION_PLAN.md Section 5.

#### Fiction/ Directory

| Task | Status | File | Key Changes |
|---|---|---|---|
| 3.1 | [x] | `Attnam.txt` | Perttuera/Attnam/Valpuri/Decos/Petrus → Aethelgard/Valpuris/Decimus/Archpriest |
| 3.2 | [x] | `DwarvenWars.txt` | Locations → Khaz-zadm; Petrus → Archpriest Cordatus; valpuris crystals |
| 3.3 | [x] | `EncounterWithKamikazeDwarf.txt` | No old refs — already clean |
| 3.4 | [x] | `God_titles.txt` | Valpurus → Valpuris |
| 3.5 | [x] | `Hedgehogs.txt` | Attnamese Empire → Holy Imperium of Aethelgard |
| 3.6 | [x] | `HistoryOfDarkKnighthood.txt` | Xinroch→Khaz-Zadm, Nethervane/Thunderfist/Soulthorn renames |
| 3.7 | [x] | `HistoryOfGolems.txt` | No old refs — already clean |
| 3.8 | [x] | `HolyBanana.txt` | banana → mango throughout |
| 3.9 | [x] | `NewAttnamLegacy.txt` | Oakhaven/Decimus/mango/Wraithstalker throughout |
| 3.10 | [x] | `Ommel.txt` | ommel → brambleback; Attnamese Standard Tile → Imperial Standard Tile |
| 3.11 | [x] | `SaalThul.txt` | No old refs — already clean |
| 3.12 | [x] | `Turox.txt` | Turox → Dawnbreaker; Xinroch → Khaz-Zadm; Attnam → Valpuris |
| 3.13 | [x] | `Vermis.txt` | Vermis → Soulthorn; fried banana → fried mango; Attnamese → Valpurian |
| 3.14 | [x] | `Creation.rtf` *(added)* | Created Creation.txt with Valpuris/Aethelgard fixes; Creation.rtf kept as archive |

#### HolyStack/ Directory

| Task | Status | File | Key Changes |
|---|---|---|---|
| 3.15 | [x] | `Titues.txt` | All titles updated to Valpurian pantheon; Petrus → Archpriest Cordatus |
| 3.16 | [x] | `ValpuriFAQ.txt` | Full rewrite — in-character FAQ, all god/location/org refs updated |
| 3.17 | [x] | `README.txt` | Directory description updated to Valpuris; mp3/jpg filenames updated |
| 3.18 | [x] | `Mola_Mola.rtf` | Updated description reference in README (RTF archive kept) |
| 3.19 | [x] | `The_Great_Battle.rtf` | Updated description; Petrus → Archpriest Cordatus; Malgorath as archenemy |
| 3.20 | [x] | `Valpuri*.jpg` files *(added)* | Renamed: Valpuri→Valpuris, Valpuri2→Valpuris2, Valpuri3→Valpuris3, Valpuri_ON_MAHTAVA→Valpuris_ON_MAHTAVA |
| 3.21 | [x] | `Valpuri*.mp3` files *(added)* | Renamed: Valpuri_is_alive!→Valpuris_est_vivus!, Incede_frater!→Incede_miles!, Excisio→Exscindere |

---

### Phase 4: Documentation Updates

#### Task 4.1: [x] Rewrite `MANUAL`
- ~5 story references: forum name, website URL, Valpurus → Valpuris in alignment explanation
- Keep structure and formatting; only update setting-specific names

#### Task 4.2: [x] Rewrite `NEWS`
- ~36+ story references throughout historical changelog entries
- Keep dates and structure; adapt all setting-specific names

---

### Phase 5: Sound Effects

#### Task 5.1: [x] Inventory `Sound/SoundEffects.cfg`
Read the file. Identify all references to old creature/character names (enner, ostrich, frog, etc.). Document what needs renaming before proceeding.

#### Task 5.2: [x] Generate Wraithstalker Sound Effects
```bash
~/venv/bin/python tools/asset_gen/audio_generator.py \
  --prompt "[SOUND] deep predatory growl, dark forest beast, low rumbling bass" \
  --output Sound/wraithstalker.wav --duration 1.0
~/venv/bin/python tools/asset_gen/audio_generator.py \
  --prompt "[SOUND] agonized shriek, dark beast dying, screech fading into silence" \
  --output Sound/wraithstalkerdeath.wav --duration 2.0
```
Generated: wraithstalker.wav (47kB, 1.0s @ 24kHz), wraithstalkerdeath.wav (94kB, 2.0s @ 24kHz). Model: suno/bark-small on CPU.

#### Task 5.3: [x] Update `Sound/SoundEffects.cfg`
- Replace `enner.wav`/`ennerdeath.wav` → `wraithstalker.wav`/`wraithstalkerdeath.wav`
- Update any other old creature-name references found in Task 5.1

---

### Phase 6: Graphics Generation

Requires Phase 0 infrastructure. All dimensions come from `asset_catalog.json`.

#### Task 6.1: [ ] Generate `Wraithstalker.png` (replaces `Enner.png`)
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy roguelike monster sprite, massive predatory forest beast with glowing yellow eyes and shadowy fur, pixel art style on white background" \
  --width <from catalog> --height <from catalog> \
  --output Graphics/Wraithstalker.png
```
Update all code references: `grep -r "Enner.png" .` → rename to `Wraithstalker.png`.

#### Task 6.2: [ ] Generate `Shadowpaw.png` (replaces `IVlad.png`)
```bash
python tools/asset_gen/image_generator.py \
  --prompt "dark fantasy roguelike companion sprite, small dark bunny with glowing eyes, pixel art style on white background" \
  --width <from catalog> --height <from catalog> \
  --output Graphics/Shadowpaw.png
```
Update code references: `grep -r "IVlad.png" .` → rename to `Shadowpaw.png`.

#### Task 6.3: [ ] Generate Character Sprite Sheets
- `Char.png` — dark fantasy adventurer sprites
- `Humanoid.png` — NPC sprites (priest, knight, merchant, rebel)

#### Task 6.4: [ ] Generate Item Icons
- `Item.png` — fantasy RPG item icon sheet
- `Item-outlined.png` — generated via `python tools/asset_gen/outline_util.py --input Graphics/Item.png --output Graphics/Item-outlined.png`

#### Task 6.5: [ ] Generate Terrain Tiles
- `WTerra.png` — world map terrain (snow, glacier, desert, tundra, jungle, steppe)
- `OLTerra.png` — overworld tiles with landmarks
- `GLTerra.png` — ground/dungeon floor tiles

#### Task 6.6: [ ] Generate UI Art
- `Menu.png`, `Menu1-5.png` — dark fantasy menu screens with medieval borders
- `Symbol.png` — new IVAN emblem (shield with crossed swords and great tree)

#### Task 6.7: [ ] Remaining Assets (lower priority)
- `Font.png`, `Font2.png`, `Font3.png` — bitmap fonts (style change if desired)
- `Effect.png`, `FOW.png`, `Smiley.png`, `Cursor.png` — may keep or style-change

---

### Phase 7: Validation & Testing

#### Task 7.1: [x] Balance Validator
```bash
python3 tools/asset_gen/balance_validator.py \
  --git-ref pre-rewrite-checkpoint \
  --files Script/material.dat Script/item.dat Script/char.dat \
         Script/dungeons/Attnam.dat Script/dungeons/NewAttnam.dat Script/dungeons/XinrochTomb.dat \
         Script/olterra.dat \
  --output validation_report.txt
```
Verify all numeric values (PriceModifier, NutritionValue, StrengthValue, Color RGB, Enchantment) unchanged.
All 7 files: PASS — zero balance-critical numeric value changes detected.

#### Task 7.2: [x] Comprehensive String Search
```bash
grep -r "banana\|Banana\|BANANA_\|Valpurus\b\|Attnam\|Tweraif\|Elpuri\b\|Xinroch\|Decos\b\|Richel\b\|Petrus\b\|FROG_FLESH\|frog flesh\|frog blood\|OMMEL_\|bananagrower\|bananapeels\|holybanana" \
  --include="*.cpp" --include="*.h" --include="*.dat" --include="*.txt" --include="*.md" \
  . | grep -v ".git/" | grep -v "PLAN.md\|EXECUTION_PLAN.md\|HIGH_LEVEL_PLAN.md" \
  > missed_references.txt
wc -l missed_references.txt
```
Fix any remaining hits before proceeding.

#### Task 7.3: [x] Compile Test
```bash
mkdir -p build && cd build && cmake .. && make -j$(nproc) 2>&1 | tail -50
```
Zero errors required.

#### Task 7.4: [ ] Runtime Testing
- Launch game; verify opening sequence uses Oakhaven, Decimus, Archpriest
- Test Freedom Quest: slay Malgorath, return heart, receive freedom
- Test XinrochTomb: all text uses Khaz-Zadm / Unholy Order of Infuscor
- Test Aslona Civil War: Muramasa/Masamune; faction names correct
- Verify mango zapping, mangopit slipping work correctly
- Verify no "banana peel" slip message; "mango pit" appears instead

---

## Commit Strategy

After completing each task:
1. Stage specific files: `git add <file1> <file2> ...` (never `git add -A`)
2. Run the task's verification grep before committing
3. Commit: `git commit -m "Phase X.Y: [description]"`
4. Mark the task `[x]` in this PLAN.md

---

## Summary of Remaining Work

| Phase | Tasks | Files Changed | Effort |
|---|---|---|---|
| **Pre-flight** | Backup tag + compile check | — | 10 min |
| **0** | Infrastructure + validator prep | `tools/asset_gen/`, `definesvalidator.h` | 2–4 hrs |
| **1** | Script .dat files (4 tasks) | material.dat, item.dat, char.dat, 3 dungeon files | Medium-Heavy |
| **2** | C++ source + headers (15 tasks, paired) | 14 .cpp + 9 .h files | Heavy |
| **3** | Lore documents (21 tasks) | 13 TXT + 2 RTF + 6 media renames | Medium |
| **4** | Documentation (2 tasks) | MANUAL, NEWS | Light |
| **5** | Sound effects (3 tasks) | Sound/*.wav, SoundEffects.cfg | Medium |
| **6** | Graphics (7 tasks) | ~20 Graphics/*.png | Heavy (GPU time) |
| **7** | Validation + testing (4 tasks) | — | Medium |
| **TOTAL** | ~57 discrete tasks | ~50 files | ~2–3 weeks |
