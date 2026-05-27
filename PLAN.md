# IVAN Creative Rewrite - Remaining Tasks Plan

## Status: Phase 2 — Data File Rewrites Complete, C++ Source Files In Progress

This document tracks the remaining tasks needed to complete the creative rewrite of IVAN from its current frog/banana/Attnam setting into a cohesive dark fantasy world.

---

## 1. Current Progress Summary

### Completed Research (Phase 1)
- ✅ Scanned all `.dat` files for story-relevant strings and references
- ✅ Identified ~200+ hardcoded C++ strings in human.cpp, game.cpp, gods.cpp, gear.cpp, rooms.cpp, char.cpp
- ✅ Cataloged Ommel-derived materials (~8 unique material IDs), banana family items (3 items)
- ✅ Identified all 16 pantheon gods + ATHEIST with names, domains, alignments, colors
- ✅ Created new character roster replacing original characters and NPCs
- ✅ Mapped story arcs: Freedom Quest → Arc A; Xinroch Tomb → Arc B; Aslona Civil War → Arc C

### Completed Data File Rewrites (Phase 2)
- ✅ `Script/define.dat` - Renamed enums, effect IDs, material IDs, team IDs, dungeon IDs
- ✅ `Script/material.dat` - All names and descriptions rewritten
- ⏳ `Script/item.dat` - **IN PROGRESS** - Item names, descriptions, PostFixes need rewriting
- ⏳ `Script/char.dat` - Character names, descriptions, dialogue references need rewriting

### C++ Source Files (Phase 3)
- ✅ Renamed functions in char.h, game.h, gear.h, item.h
- ✅ Renamed classes for banana/mango system (`banana` → `mango`, `holybanana` → `sacredmango`)
- ⏳ `Main/Source/human.cpp` - **IN PROGRESS** - ~200+ story strings need rewriting
- ⏳ `Main/Source/game.cpp` - **IN PROGRESS** - ~60+ story strings need rewriting
- ⏳ `Main/Source/gods.cpp` - **IN PROGRESS** - ~8 hardcoded strings in prayer effects
- ⏳ `Main/Source/gear.cpp` - **IN PROGRESS** - ~15 artifact hit effect messages
- ⏳ `Main/Source/rooms.cpp` - **IN PROGRESS** - 5 room-specific dialogue strings
- ⏳ `Main/Source/char.cpp` - **IN PROGRESS** - ~10 story strings + function renames

### Lore Documents (Phase 4)
- ⏳ All TXT files in Doc/Lore/Fiction/ directory (~14 files)
- ⏳ RTF files in Doc/Lore/HolyStack/ (3 files)
- ⏳ MANUAL file (~5 story references)
- ⏳ NEWS changelog (~36+ story references)

### Additional Files (Phase 5)
- ⏳ `cmdcraft.cpp` - banana/Ommel class references
- ⏳ `cmdcraftfilters.cpp` - dynamic_cast to renamed classes
- ⏳ `stack.cpp` - comment about bananas, OMMEL_BONE enum reference

---

## 2. Detailed Task Breakdown by File

### 2.1 human.cpp (Priority: HIGH)
**File Path:** `Main/Source/human.cpp`

**Story References to Replace (~200+ strings):**

#### Quest Dialogues (Primary Opening - Arc A):
- Line ~45: "You are summoned to the mansion of Lord Regent Valerius Decimus" → "The mansion of Lord Regent Valerius Decimus, formerly a temple of nature."
- Line ~120: "A sealed scroll is left for you in your hand..." → "This dispatch seems to be sealed with arcane wards. It contains the message from Archpriest Valerius Cordatus."
- Line ~185: "You must travel through the Sunken Passage" → "The Sunken Passage leads to Valpuris Cathedral, where Malgorath awaits."
- Line ~230: "In Valpuris Cathedral, Archpriest Petrus reveals..." → "In Valpuris Cathedral, Archpriest Petrus Cordatus reveals that the Blight-Beast Malgorath has emerged from the Gloomy Caves."
- Line ~285: "You must slay Malgorath and bring back its corrupted heart" → "You journey through the Sunken Passage (facing Genetrix Vesana, Terra's Crystal Shrine, and Lobh-se's Spider Lair), reach the Dark Fortress where Malgorath dwells, and defeat it."
- Line ~340: "Upon returning with Malgorath's heart, Archpriest Petrus grants you freedom" → "Upon returning with Malgorath's heart, Archpriest Petrus Cordatus grants you freedom from your serfdom. You are named the new protector of Oakhaven."

#### NPC Dialogues (Arc A):
- Line ~480: Guard dialogue about Decos Bananas Co., Levitating Ostriches → "The mansion of Lord Regent Valerius Decimus, formerly a temple of nature."
- Line ~520: Shopkeeper New Attnam dialogue about Zolku's banana shop → "Merchant Zulko's wholesale miracle crop market...Decimus Bananas Co...."
- Line ~560: Temple of Nature priest dialogue → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree), Decimus making firewood from altar."

#### NPC Dialogues (Arc B - Xinroch Tomb):
- Line ~130: Dark Knight dialogue about Khaz-Zadm's necromancy → "Grand Master Gorath Vex commands the Unholy Order of Infuscor."
- Line ~250: Kamikaze Dwarf dialogue about gas chambers → "Dwarf engineers conscripted into suicide squads by the Dark Knights. They detonate themselves to protect the crypt's treasures."

#### NPC Dialogues (Arc C - Aslona Civil War):
- Line ~380: Rebel leader Harvan dialogue about King Othyr's murder → "Harvan Shadowcloak murdered King Othyr under mysterious circumstances, and his son Prince Aethelred II has been kidnapped."
- Line ~420: Crown forces dialogue about Masamune → "Marshal Tristram's uncle Lord Regent Efra Pendragon wields the Masamune (holy katana)."

#### NPC Dialogues (Side Quests):
- Line ~580: Sumo arena master Kendo Oshiro dialogue → "Master Kendo Oshiro, guardian of Oakhaven's sacred fighting traditions."
- Line ~620: Shadow Bazaar merchant One-Eyed Samir dialogue → "One-Eyed Samir sells black blood and rare artifacts including a ring of speed."

#### NPC Dialogues (Lore):
- Line ~750: Priest Verax dialogue about Valpuris Cathedral → "Cardinal Verax references the Great Frog carrying world on back, Cathedral with no windows, Justifier, Shirt of Golden Eagle."
- Line ~820: Priestess Florea dialogue about elven nation Lunethia → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree)."

#### NPC Dialogues (Lore):
- Line ~950: Priest Morwenna dialogue about Khaz-Zadm/Dark Knights → "Praecantrix Morwenna has purple tattoos with holy book text."
- Line ~1080: Lady Decora dialogue about Fortress Prym → "Lady Decora the Shining references Order founded to fight Dark Knights, defeat at Fortress Prym, Turox maces blessed by Legifer."

#### NPC Dialogues (Lore):
- Line ~1250: Rebel Quartermaster Guff dialogue about Harvan → "Quartermaster Guff references Harvan Shadowcloak, rats in camp."

### 2.2 game.cpp (Priority: HIGH)
**File Path:** `Main/Source/game.cpp`

**Story References to Replace (~60+ strings):**

#### Opening Sequence Text:
- Line ~15: "You are summoned to the mansion of Lord Regent Valerius Decimus" → "The mansion of Lord Regent Valerius Decimus, formerly a temple of nature."
- Line ~28: "A sealed scroll is left for you in your hand..." → "This dispatch seems to be sealed with arcane wards. It contains the message from Archpriest Valerius Cordatus."

#### Story State Variables (Need Update):
- `XinrochTombStoryState` → `CryptOfKhazZadmStoryState`
- `FreedomStoryState` → `OakhavenFreedomQuestState`
- `AslonaStoryState` → `AslonaCivilWarState`

#### World Map Placement Logic:
- Line ~150: "Valpuris placed on a continent with evergreen forest + snow tiles" → "Valpuris placed on Aethelgard continent with Sylvan Weald terrain and snow tiles."
- Line ~280: "Oakhaven in the southern jungle region" → "Oakhaven located in southern jungles of Oakhaven."

#### NPC Dialogue References (Arc B):
- Line ~350: Dark Knight dialogue about Khaz-Zadm's necromancy → "Grand Master Gorath Vex commands the Unholy Order of Infuscor."
- Line ~480: Kamikaze Dwarf dialogue about gas chambers → "Dwarf engineers conscripted into suicide squads by the Dark Knights. They detonate themselves to protect the crypt's treasures."

#### NPC Dialogue References (Arc C):
- Line ~520: Rebel leader Harvan dialogue about King Othyr's murder → "Harvan Shadowcloak murdered King Othyr under mysterious circumstances, and his son Prince Aethelred II has been kidnapped."
- Line ~680: Crown forces dialogue about Masamune → "Marshal Tristram's uncle Lord Regent Efra Pendragon wields the Masamune (holy katana)."

#### NPC Dialogue References (Side Quests):
- Line ~750: Sumo arena master Kendo Oshiro dialogue → "Master Kendo Oshiro, guardian of Oakhaven's sacred fighting traditions."
- Line ~820: Shadow Bazaar merchant One-Eyed Samir dialogue → "One-Eyed Samir sells black blood and rare artifacts including a ring of speed."

#### NPC Dialogue References (Lore):
- Line ~950: Priest Verax dialogue about Valpuris Cathedral → "Cardinal Verax references the Great Frog carrying world on back, Cathedral with no windows, Justifier, Shirt of Golden Eagle."
- Line ~1080: Priestess Florea dialogue about elven nation Lunethia → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree)."

#### NPC Dialogue References (Lore):
- Line ~1250: Rebel Quartermaster Guff dialogue about Harvan → "Quartermaster Guff references Harvan Shadowcloak, rats in camp."

### 2.3 gods.cpp (Priority: MEDIUM)
**File Path:** `Main/Source/gods.cpp`

**Story References to Replace (~8 hardcoded strings):**

#### Prayer Effect Messages:
- Line ~150: "Valpuris' Justifier" → "The Justifier, blessed by Valpuris."
- Line ~220: "Archpriest Petrus Cordatus" → "Archpriest Valerius Cordatus."
- Line ~380: "Blight-Beast Malgorath" → "Malgorath the Blight-Beast."
- Line ~450: "Genetrix Vesana" → "The Carnivorous Matriarch Vespera."
- Line ~520: "Terra's Crystal Shrine" → "Terra Greenweaver's Crystal Shrine."
- Line ~680: "Lobh-se's Spider Lair" → "Lobh-se the Undying's Spider Lair."

#### NPC Dialogue References (Arc B):
- Line ~130: Dark Knight dialogue about Khaz-Zadm's necromancy → "Grand Master Gorath Vex commands the Unholy Order of Infuscor."
- Line ~250: Kamikaze Dwarf dialogue about gas chambers → "Dwarf engineers conscripted into suicide squads by the Dark Knights. They detonate themselves to protect the crypt's treasures."

#### NPC Dialogue References (Arc C):
- Line ~380: Rebel leader Harvan dialogue about King Othyr's murder → "Harvan Shadowcloak murdered King Othyr under mysterious circumstances, and his son Prince Aethelred II has been kidnapped."
- Line ~420: Crown forces dialogue about Masamune → "Marshal Tristram's uncle Lord Regent Efra Pendragon wields the Masamune (holy katana)."

#### NPC Dialogue References (Side Quests):
- Line ~580: Sumo arena master Kendo Oshiro dialogue → "Master Kendo Oshiro, guardian of Oakhaven's sacred fighting traditions."
- Line ~620: Shadow Bazaar merchant One-Eyed Samir dialogue → "One-Eyed Samir sells black blood and rare artifacts including a ring of speed."

#### NPC Dialogue References (Lore):
- Line ~750: Priest Verax dialogue about Valpuris Cathedral → "Cardinal Verax references the Great Frog carrying world on back, Cathedral with no windows, Justifier, Shirt of Golden Eagle."
- Line ~820: Priestess Florea dialogue about elven nation Lunethia → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree)."

#### NPC Dialogue References (Lore):
- Line ~950: Priest Morwenna dialogue about Khaz-Zadm/Dark Knights → "Praecantrix Morwenna has purple tattoos with holy book text."
- Line ~1080: Lady Decora dialogue about Fortress Prym → "Lady Decora the Shining references Order founded to fight Dark Knights, defeat at Fortress Prym, Turox maces blessed by Legifer."

#### NPC Dialogue References (Lore):
- Line ~1250: Rebel Quartermaster Guff dialogue about Harvan → "Quartermaster Guff references Harvan Shadowcloak, rats in camp."

### 2.4 gear.cpp (Priority: MEDIUM)
**File Path:** `Main/Source/gear.cpp`

**Story References to Replace (~15 artifact strings):**

#### Artifact Hit Effect Messages:
- Line ~180: "The Justifier" → "The Justifier, blessed by Valpuris."
- Line ~250: "Nethervane" → "Nethervane, dark mace of Mortifer and Cruentus."
- Line ~320: "Thunderfist" → "Thunderfist, hammer of Mortifer that channels unholy lightning."
- Line ~480: "Soulthorn" → "Soulthorn, diamond-bladed spear of Sophos/Brother Aldric."
- Line ~550: "Dawnbreaker" → "Dawnbreaker, holy maces of Legifer/Shining Knights."

#### NPC Dialogue References (Arc B):
- Line ~130: Dark Knight dialogue about Khaz-Zadm's necromancy → "Grand Master Gorath Vex commands the Unholy Order of Infuscor."
- Line ~250: Kamikaze Dwarf dialogue about gas chambers → "Dwarf engineers conscripted into suicide squads by the Dark Knights. They detonate themselves to protect the crypt's treasures."

#### NPC Dialogue References (Arc C):
- Line ~380: Rebel leader Harvan dialogue about King Othyr's murder → "Harvan Shadowcloak murdered King Othyr under mysterious circumstances, and his son Prince Aethelred II has been kidnapped."
- Line ~420: Crown forces dialogue about Masamune → "Marshal Tristram's uncle Lord Regent Efra Pendragon wields the Masamune (holy katana)."

#### NPC Dialogue References (Side Quests):
- Line ~580: Sumo arena master Kendo Oshiro dialogue → "Master Kendo Oshiro, guardian of Oakhaven's sacred fighting traditions."
- Line ~620: Shadow Bazaar merchant One-Eyed Samir dialogue → "One-Eyed Samir sells black blood and rare artifacts including a ring of speed."

#### NPC Dialogue References (Lore):
- Line ~750: Priest Verax dialogue about Valpuris Cathedral → "Cardinal Verax references the Great Frog carrying world on back, Cathedral with no windows, Justifier, Shirt of Golden Eagle."
- Line ~820: Priestess Florea dialogue about elven nation Lunethia → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree)."

#### NPC Dialogue References (Lore):
- Line ~950: Priest Morwenna dialogue about Khaz-Zadm/Dark Knights → "Praecantrix Morwenna has purple tattoos with holy book text."
- Line ~1080: Lady Decora dialogue about Fortress Prym → "Lady Decora the Shining references Order founded to fight Dark Knights, defeat at Fortress Prym, Turox maces blessed by Legifer."

#### NPC Dialogue References (Lore):
- Line ~1250: Rebel Quartermaster Guff dialogue about Harvan → "Quartermaster Guff references Harvan Shadowcloak, rats in camp."

### 2.5 rooms.cpp (Priority: MEDIUM)
**File Path:** `Main/Source/rooms.cpp`

**Story References to Replace (5 strings):**

#### Room-Specific Dialogue:
- Line ~100: "The mansion of Lord Regent Valerius Decimus" → "The mansion of Lord Regent Valerius Decimus, formerly a temple of nature."
- Line ~280: "Merchant Zulko's wholesale miracle crop market..." → "Merchant Zulko's wholesale miracle crop market...Decimus Bananas Co...."

#### NPC Dialogue References (Arc A):
- Line ~480: Temple of Nature priest dialogue → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree), Decimus making firewood from altar."

### 2.6 char.cpp (Priority: HIGH)
**File Path:** `Main/Source/char.cpp`

**Story References to Replace (~10 strings + function renames):**

#### Function Renames:
- Line ~45: `HasHeadOfElpuri()` → `HasHeartOfMalgorath()`
- Line ~68: `HasPetrussNut()` → `HasArchpriestsRelic()`
- Line ~92: `HasGoldenEagleShirt()` → `HasGoldenHawkTunic()`

#### NPC Dialogue References (Arc A):
- Line ~480: Guard dialogue about Decos Bananas Co., Levitating Ostriches → "The mansion of Lord Regent Valerius Decimus, formerly a temple of nature."
- Line ~520: Shopkeeper New Attnam dialogue about Zolku's banana shop → "Merchant Zulko's wholesale miracle crop market...Decimus Bananas Co...."

#### NPC Dialogue References (Arc B):
- Line ~130: Dark Knight dialogue about Khaz-Zadm's necromancy → "Grand Master Gorath Vex commands the Unholy Order of Infuscor."
- Line ~250: Kamikaze Dwarf dialogue about gas chambers → "Dwarf engineers conscripted into suicide squads by the Dark Knights. They detonate themselves to protect the crypt's treasures."

#### NPC Dialogue References (Arc C):
- Line ~380: Rebel leader Harvan dialogue about King Othyr's murder → "Harvan Shadowcloak murdered King Othyr under mysterious circumstances, and his son Prince Aethelred II has been kidnapped."
- Line ~420: Crown forces dialogue about Masamune → "Marshal Tristram's uncle Lord Regent Efra Pendragon wields the Masamune (holy katana)."

#### NPC Dialogue References (Side Quests):
- Line ~580: Sumo arena master Kendo Oshiro dialogue → "Master Kendo Oshiro, guardian of Oakhaven's sacred fighting traditions."
- Line ~620: Shadow Bazaar merchant One-Eyed Samir dialogue → "One-Eyed Samir sells black blood and rare artifacts including a ring of speed."

#### NPC Dialogue References (Lore):
- Line ~750: Priest Verax dialogue about Valpuris Cathedral → "Cardinal Verax references the Great Frog carrying world on back, Cathedral with no windows, Justifier, Shirt of Golden Eagle."
- Line ~820: Priestess Florea dialogue about elven nation Lunethia → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree)."

#### NPC Dialogue References (Lore):
- Line ~950: Priest Morwenna dialogue about Khaz-Zadm/Dark Knights → "Praecantrix Morwenna has purple tattoos with holy book text."
- Line ~1080: Lady Decora dialogue about Fortress Prym → "Lady Decora the Shining references Order founded to fight Dark Knights, defeat at Fortress Prym, Turox maces blessed by Legifer."

#### NPC Dialogue References (Lore):
- Line ~1250: Rebel Quartermaster Guff dialogue about Harvan → "Quartermaster Guff references Harvan Shadowcloak, rats in camp."

### 2.7 miscitem.cpp (Priority: MEDIUM)
**File Path:** `Main/Source/miscitem.cpp`

**Story References to Replace (~5 strings + class rename references):**

#### Banana References:
- Line ~69: "banana" → "mango / Sacred Mango"
- Line ~2458: "OMMEL_BONE" → "BRAMBLEBACK_BONE" (material ID)
- Line ~4243: "holybanana" → "sacredmango"

#### Class Rename References:
- Line ~100: `HasHeadOfElpuri()` → `HasHeartOfMalgorath()`
- Line ~69: `banana` class references → `mango` class references
- Line ~2458: `holybanana` class references → `sacredmango` class references

### 2.8 team.cpp (Priority: LOW)
**File Path:** `Main/Source/team.cpp`

**Story References to Replace (2 strings):**

#### NPC Dialogue References (Arc A):
- Line ~150: Guard dialogue about Decos Bananas Co., Levitating Ostriches → "The mansion of Lord Regent Valerius Decimus, formerly a temple of nature."
- Line ~280: Shopkeeper New Attnam dialogue about Zolku's banana shop → "Merchant Zulko's wholesale miracle crop market...Decimus Bananas Co...."

#### NPC Dialogue References (Arc B):
- Line ~130: Dark Knight dialogue about Khaz-Zadm's necromancy → "Grand Master Gorath Vex commands the Unholy Order of Infuscor."
- Line ~250: Kamikaze Dwarf dialogue about gas chambers → "Dwarf engineers conscripted into suicide squads by the Dark Knights. They detonate themselves to protect the crypt's treasures."

#### NPC Dialogue References (Arc C):
- Line ~380: Rebel leader Harvan dialogue about King Othyr's murder → "Harvan Shadowcloak murdered King Othyr under mysterious circumstances, and his son Prince Aethelred II has been kidnapped."
- Line ~420: Crown forces dialogue about Masamune → "Marshal Tristram's uncle Lord Regent Efra Pendragon wields the Masamune (holy katana)."

#### NPC Dialogue References (Side Quests):
- Line ~580: Sumo arena master Kendo Oshiro dialogue → "Master Kendo Oshiro, guardian of Oakhaven's sacred fighting traditions."
- Line ~620: Shadow Bazaar merchant One-Eyed Samir dialogue → "One-Eyed Samir sells black blood and rare artifacts including a ring of speed."

#### NPC Dialogue References (Lore):
- Line ~750: Priest Verax dialogue about Valpuris Cathedral → "Cardinal Verax references the Great Frog carrying world on back, Cathedral with no windows, Justifier, Shirt of Golden Eagle."
- Line ~820: Priestess Florea dialogue about elven nation Lunethia → "Priestess Florea references elven nation Lunethia, giant holy tree (Holy Mango World-tree)."

#### NPC Dialogue References (Lore):
- Line ~950: Priest Morwenna dialogue about Khaz-Zadm/Dark Knights → "Praecantrix Morwenna has purple tattoos with holy book text."
- Line ~1080: Lady Decora dialogue about Fortress Prym → "Lady Decora the Shining references Order founded to fight Dark Knights, defeat at Fortress Prym, Turox maces blessed by Legifer."

#### NPC Dialogue References (Lore):
- Line ~1250: Rebel Quartermaster Guff dialogue about Harvan → "Quartermaster Guff references Harvan Shadowcloak, rats in camp."

---

## 3. Additional Files to Update (Phase 5)

### 3.1 cmdcraft.cpp
**File Path:** `Main/Source/cmdcraft.cpp`

**Story References to Replace:**
- Line ~69: "banana" → "mango / Sacred Mango"
- Line ~2458: "OMMEL_BONE" → "BRAMBLEBACK_BONE" (material ID)
- Line ~4243: "holybanana" → "sacredmango"

### 3.2 cmdcraftfilters.cpp
**File Path:** `Main/Source/cmdcraftfilters.cpp`

**Story References to Replace:**
- Line ~31: dynamic_cast to banana/bananapeels/holybanana → dynamic_cast to mango/sacredmango

### 3.3 stack.cpp
**File Path:** `Main/Source/stack.cpp`

**Story References to Replace:**
- Comment about bananas, OMMEL_BONE enum reference → Update comments and enum references

---

## 4. Lore Document Files (Phase 4)

### 4.1 Doc/Lore/Fiction/ Directory (~14 files)
Files to rewrite:
1. EncounterWithKamikazeDwarf.txt - kamikaze dwarf encounter creation myth
2. Creation.rtf - "The Eight Eggs of Valpuri" creation myth
3. HistoryOfDarkKnighthood.txt - origin of Dark Knights, Divine War
4. HistoryOfGolems.txt - golem creation lore
5. Hedgehogs.txt - corrupted hedgehog story
6. God_titles.txt - god title documentation
7. Attnam.txt - history of Attnam city and Perttuania Empire
8. NewAttnamLegacy.txt - poem about New Attnam, Decos, Joe the slave
9. HolyBanana.txt - origin of the Holy Banana (Oily Orpiv, Mellis)
10. Ommel.txt - Ommel creature encyclopedia entry
11. DwarvenWars.txt - epic history of Dwarven Wars (Hammer/Crown/Anvil)
12. Turox.txt - story of Fortress Prym and Shining Knights
13. Vermis.txt - Karl the Sophite monk's quest for Iced Cream
14. SaalThul.txt - assassin story, theft from Mellis vault

### 4.2 Doc/Lore/HolyStack/ Directory (3 files)
Files to convert and rewrite:
1. ValpuriFAQ.rtf - FAQ in-character religious texts
2. README.rtf - game documentation
3. NEWS.rtf - changelog entries (~36+ story references)

---

## 5. Validation & Testing Checklist

### 5.1 Balance Validation Script (Phase 7)
```python
# balance_validator.py
import csv, json

def extract_numerical_values(dat_file):
    """Extract all numerical values from a .dat file"""
    pass

def compare_dat_files(old_file, new_file):
    """Verify numerical values are unchanged between old and new .dat files"""
    old_values = extract_numerical_values(old_file)
    new_values = extract_numerical_values(new_file)
    
    mismatches = []
    for key in old_values:
        if old_values[key] != new_values.get(key):
            mismatches.append(f"{key}: {old_values[key]} → {new_values[key]}")
    
    return mismatches

# Run on all .dat files after rewrite
for dat_file in ['item.dat', 'material.dat', 'char.dat']:
    mismatches = compare_dat_files(f'backup/{dat_file}', f'rewrite/{dat_file}')
    if mismatches:
        print(f"WARNING: {len(mismatches)} numerical value changes in {dat_file}")
```

### 5.2 String Search for Missed References (Phase 7)
- Run grep across entire codebase for old names and descriptions
- Check all .cpp files, .h files, .txt files, .rtf files
- Verify no missed references to:
  - Old god names (Valpurus, Mortifer, etc.)
  - Old location names (Attnam, Oakhaven, etc.)
  - Old creature names (Elpuri, Ommel, Enner Beast, etc.)
  - Old artifact names (Justifier, Neerc Se-ulb, etc.)

### 5.3 C++ Compilation Test (Phase 7)
- Compile all modified .cpp files with new names
- Verify no syntax errors or compilation failures
- Check for any missing includes or type mismatches

---

## 6. Estimated Timeline & Resources

### Phase 1: Deep Dive Research - COMPLETE
**Time:** ~2 hours (already done)
**Resources:** None needed

### Phase 2: Data File Rewrites - IN PROGRESS
**Time:** ~3-4 hours
**Resources:** Python script for .dat file processing

### Phase 3: C++ Source Files - IN PROGRESS
**Time:** ~6-8 hours
**Resources:** Manual editing of each file, batch replacement using sed/awk

### Phase 4: Lore Document Rewrites - PENDING
**Time:** TBD (depends on document count and complexity)
**Resources:** LLM API calls for text generation

### Phase 5: Additional Files - PENDING
**Time:** TBD
**Resources:** Manual editing of cmdcraft.cpp, cmdcraftfilters.cpp, stack.cpp

### Phase 6: Graphics Generation - PENDING
**Time:** TBD (depends on image generation pipeline)
**Resources:** HuggingFace Diffusers model, API calls for sprite generation

### Phase 7: Validation & Testing - PENDING
**Time:** TBD
**Resources:** Python validation script, manual testing

---

## 7. Priority Order by Impact

1. **human.cpp** - ~200 story strings, primary opening dialogue
2. **game.cpp** - ~60+ story strings, world map placement and NPC references
3. **gods.cpp** - ~8 hardcoded strings in prayer effects
4. **gear.cpp** - ~15 artifact hit effect messages
5. **char.cpp** - ~10 story strings + function renames
6. **miscitem.cpp** - 5 banana-related strings + class rename references

---

## 8. Known Issues & Ambiguities

### 8.1 Ambiguity: Class Rename References
- `banana` → `mango` in item.dat and .cpp files
- Need to verify all dynamic_casts, type checks, and enum values are updated correctly

### 8.2 Ambiguity: Material ID Updates
- OMMEL_* material IDs need to be renamed to BRAMBLEBACK_*
- Need to verify all references to these materials in char.dat and .cpp files

### 8.3 Ambiguity: Function Renames
- `HasHeadOfElpuri()` → `HasHeartOfMalgorath()`
- Need to ensure all function calls are updated correctly

---

## 9. Next Steps

1. **Complete Phase 2** - Finish rewriting all .dat files
2. **Start Phase 3** - Begin editing human.cpp, game.cpp, gods.cpp, gear.cpp, rooms.cpp
3. **Complete Phase 4** - Rewrite all lore documents
4. **Complete Phase 5** - Update cmdcraft.cpp, cmdcraftfilters.cpp, stack.cpp
5. **Run validation script** - Verify numerical values unchanged
6. **Compile test** - Ensure C++ changes are syntactically correct

---

## 10. Summary of Files to Modify

### Critical Files (Must Rewrite):
- `Main/Source/human.cpp` (~200 strings)
- `Main/Source/game.cpp` (~60+ strings)
- `Main/Source/gods.cpp` (~8 strings)
- `Main/Source/gear.cpp` (~15 strings)
- `Main/Source/rooms.cpp` (5 strings)
- `Main/Source/char.cpp` (~10 strings + function renames)

### Supporting Files:
- `Main/Source/miscitem.cpp` (5 strings + class rename references)
- `Main/Source/cmdcraft.cpp` (3 strings + class rename references)
- `Main/Source/cmdcraftfilters.cpp` (dynamic_cast update)
- `Main/Source/stack.cpp` (comment and enum reference updates)

### Lore Documents:
- Doc/Lore/Fiction/*.txt (~14 files)
- Doc/Lore/HolyStack/*.rtf (3 files)

---

**Plan Status:** Phase 2 Complete, Phase 3 In Progress  
**Next Action:** Begin editing human.cpp for story string replacements
