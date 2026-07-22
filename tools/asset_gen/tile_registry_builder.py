#!/usr/bin/env python3
"""
tile_registry_builder.py — Parse VALE .dat files and build per-sheet tile registries.

Outputs one JSON file per sprite sheet to tools/asset_gen/tile_registries/.
Each JSON maps "col,row" grid coordinates to tile description dicts with
auto-generated AI prompts.

Usage:
    ~/venv/bin/python tools/asset_gen/tile_registry_builder.py
    # or for a single sheet:
    ~/venv/bin/python tools/asset_gen/tile_registry_builder.py --sheet GLTerra
"""

import re, json, argparse
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
SCRIPT_DIR = REPO / "Script"
OUT_DIR = Path(__file__).parent / "tile_registries"

# Material → readable description for prompts
MATERIAL_DESCRIPTIONS = {
    "GRANITE": "gray granite stone",
    "GRAVEL": "gray gravel stone",
    "GRASS": "green grass",
    "DARK_GRASS": "dark green grass",
    "SNOW": "white snow",
    "SAND": "sandy yellow ground",
    "FIR_WOOD": "fir wood planks",
    "BALSA_WOOD": "pale wood",
    "OAK_WOOD": "dark oak wood",
    "ICE": "blue-white ice",
    "LAVA": "glowing orange-red lava",
    "WATER": "blue-gray water",
    "DEEP_WATER": "dark deep water",
    "IRON": "dark iron metal",
    "STEEL": "gray steel metal",
    "GOLD": "bright gold metal",
    "SILVER": "shiny silver metal",
    "MITHRIL": "pale blue mithril",
    "MARBLE": "white marble stone",
    "BONE": "pale yellowed bone",
    "CRYSTAL": "translucent crystal",
    "OBSIDIAN": "black obsidian stone",
    "COAL": "black coal",
    "EMERALD": "green gemstone",
    "RUBY": "red gemstone",
    "DIAMOND": "clear gemstone",
    "SAPPHIRE": "blue gemstone",
    "AMETHYST": "purple gemstone",
    "TOPAZ": "yellow gemstone",
}


def material_desc(mat):
    return MATERIAL_DESCRIPTIONS.get(mat, mat.lower().replace("_", " ") if mat else "stone")


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", " ", text)
    return text


def match_braces(text, start):
    """Return (open_pos, close_pos) for the brace block starting at or after `start`."""
    open_pos = text.find('{', start)
    if open_pos == -1:
        return -1, -1
    depth = 1
    i = open_pos + 1
    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    return open_pos, i - 1  # positions of '{' and '}'


def extract_field_from_block(block, field_name):
    """Extract value of a field from within a block string."""
    m = re.search(rf'{field_name}\s*==?\s*"([^"]*)"', block)
    return m.group(1) if m else None


def extract_bitmap_pos(block):
    m = re.search(r'BitmapPos\s*=\s*(\d+)\s*,\s*(\d+)', block)
    return (int(m.group(1)), int(m.group(2))) if m else None


def extract_material(block):
    m = re.search(r'MainMaterialConfig\s*==?\s*([A-Z_][A-Z_0-9]*)', block)
    return m.group(1) if m else None


def extract_config_blocks(text):
    """
    Extract all named Config blocks with brace-matching.
    Returns list of (config_name, block_content, preceding_text) tuples.
    """
    blocks = []
    for m in re.finditer(r'Config\s+([A-Z_][A-Z_0-9]*)\s*;', text):
        config_name = m.group(1)
        open_pos, close_pos = match_braces(text, m.end())
        if open_pos == -1:
            continue
        block_content = text[open_pos + 1:close_pos]
        blocks.append((config_name, block_content, text[:m.start()]))
    return blocks


def extract_top_level_blocks(text):
    """
    Extract top-level named blocks (not Config blocks) for owterra.dat.
    Returns list of (block_name, block_content) tuples.
    """
    blocks = []
    for m in re.finditer(r'\n([a-z_][a-z_0-9]*)\s*\n?\s*\{', text):
        block_name = m.group(1)
        open_pos, close_pos = match_braces(text, m.end() - 1)
        if open_pos == -1:
            continue
        block_content = text[open_pos + 1:close_pos]
        # Skip the default/abstract blocks (glterrain, olterrain, etc.)
        if block_name in ('glterrain', 'olterrain', 'owterrain', 'solidterrain',
                          'liquidterrain', 'wall', 'tree', 'furniture', 'item',
                          'character', 'olterrain'):
            continue
        blocks.append((block_name, block_content))
    return blocks


def make_prompt(sheet, name, material, adjective="", extra=""):
    mat = material_desc(material)
    full_name = f"{adjective} {name}".strip() if adjective else name

    base = "dark fantasy Tolkien roguelike, 16x16 pixel art tile sprite, centered subject, flat colors, strong black outlines, no gradients, muted palette, top-down view"

    if sheet == "GLTerra":
        return f"{base}, dungeon underground {full_name}, {mat} texture, torch-lit stone, subterranean atmosphere. {extra}".strip()
    elif sheet == "WTerra":
        return f"{base}, overworld map icon, {full_name}, {mat}, small landmark symbol, bird's eye. {extra}".strip()
    elif sheet == "OLTerra":
        return f"{base}, outdoor level tile, {full_name}, {mat}, ground-level top-down. {extra}".strip()
    elif sheet == "Item":
        return f"dark fantasy roguelike item icon, 16x16 pixel art, {full_name}, made of {mat}, centered on black background, detailed small sprite, Tolkien aesthetic. {extra}".strip()
    elif sheet == "Char":
        return f"dark fantasy roguelike creature sprite, 16x16 pixel art, {full_name} body part, top-down, {mat} skin/material. {extra}".strip()
    elif sheet == "Humanoid":
        return f"dark fantasy roguelike humanoid sprite, 16x16 pixel art, {full_name}, side-facing body part tile, {mat}. {extra}".strip()
    elif sheet == "Symbol":
        return f"dark fantasy deity symbol icon, 16x16 pixel art, {full_name} divine sigil, heraldic emblem, gold or silver on dark background. {extra}".strip()
    elif sheet == "Effect":
        return f"dark fantasy magical effect sprite, 16x16 pixel art, {full_name} particle effect, glowing, high contrast on black. {extra}".strip()
    else:
        return f"{base}, {full_name}, {mat}. {extra}".strip()


# ─────────────────────────────────────────────
# Terrain parsers (glterra.dat / olterra.dat)
# ─────────────────────────────────────────────

def parse_terrain_dat(filepath, sheet_name):
    """
    Parse a terrain .dat file (glterra.dat or olterra.dat) using proper Config block extraction.
    Also scans top-level named blocks (door, stairs, altar, etc.) that aren't
    Config blocks, matching the pattern parse_item_dat already uses.
    Returns registry dict keyed by "col,row".
    """
    text = strip_comments(Path(filepath).read_text())
    registry = {}

    def add_entry(config_name, block_content, preceding):
        bitmappos = extract_bitmap_pos(block_content)
        if not bitmappos:
            return
        px, py = bitmappos
        col, row = px // 16, py // 16
        key = f"{col},{row}"

        # Extract fields from THIS block only
        ns = extract_field_from_block(block_content, "NameSingular") or \
             config_name.lower().replace("_", " ")
        adj = extract_field_from_block(block_content, "Adjective") or ""
        material = extract_material(block_content)

        # If material not in this block, look in parent block (non-Config content before this)
        if not material:
            # Find the enclosing parent block (everything after last 'IsAbstract = true' up to Config)
            parent_blocks = re.findall(r'\n([a-z_][a-z_0-9]*)\s*\n?\s*\{', preceding)
            parent_name = parent_blocks[-1] if parent_blocks else ""
            parent_mat_m = re.search(r'MainMaterialConfig\s*==?\s*([A-Z_][A-Z_0-9]*)',
                                     preceding[-600:])
            material = parent_mat_m.group(1) if parent_mat_m else ""

        # IsWall hint from parent preceding text
        is_wall = bool(re.search(r"IsWall\s*=\s*true", preceding[-1000:]))
        extra = "stone wall surface" if is_wall else ""

        display = f"{adj} {ns}".strip() if adj else ns

        entry = {
            "config": config_name,
            "name": display,
            "material": material,
            "pixel_x": px,
            "pixel_y": py,
            "prompt": make_prompt(sheet_name, display, material, extra=extra),
        }

        # Prefer first entry at a given position (keeps the most specific Config)
        if key not in registry:
            registry[key] = entry

    for config_name, block_content, preceding in extract_config_blocks(text):
        add_entry(config_name, block_content, preceding)

    for block_name, block_content in extract_top_level_blocks(text):
        add_entry(block_name, block_content, "")

    return registry


# ─────────────────────────────────────────────
# World-map terrain parser (owterra.dat)
# ─────────────────────────────────────────────

def parse_owterra(filepath):
    """
    Parse owterra.dat (world-map terrain — top-level named blocks).
    Returns registry dict keyed by "col,row".
    """
    text = strip_comments(Path(filepath).read_text())
    registry = {}

    for block_name, block_content in extract_top_level_blocks(text):
        bitmappos = extract_bitmap_pos(block_content)
        if not bitmappos:
            continue
        px, py = bitmappos
        col, row = px // 16, py // 16
        key = f"{col},{row}"

        stem = extract_field_from_block(block_content, "NameStem") or \
               block_name.replace("_", " ")

        entry = {
            "config": block_name,
            "name": stem,
            "material": "",
            "pixel_x": px,
            "pixel_y": py,
            "prompt": make_prompt("WTerra", stem, "", extra=f"location: {block_name}"),
        }

        if key not in registry:
            registry[key] = entry

    return registry


# ─────────────────────────────────────────────
# Item parser (item.dat)
# ─────────────────────────────────────────────

def parse_item_dat(filepath):
    """
    Parse item.dat using proper block extraction.
    Maps each unique BitmapPos to aggregated item name(s).
    Returns registry dict keyed by "col,row".
    """
    text = strip_comments(Path(filepath).read_text())
    registry = {}  # key → aggregation dict

    # Parse Config blocks first (items with multiple material configs)
    for config_name, block_content, preceding in extract_config_blocks(text):
        bitmappos = extract_bitmap_pos(block_content)
        if not bitmappos:
            continue
        _accumulate_item(registry, bitmappos, block_content, preceding)

    # Parse top-level item blocks (non-Config named items)
    for block_name, block_content in extract_top_level_blocks(text):
        bitmappos = extract_bitmap_pos(block_content)
        if not bitmappos:
            continue
        _accumulate_item(registry, bitmappos, block_content, "", block_name)

    # Convert to final entries
    final = {}
    for key, data in registry.items():
        names = data["names"][:3]
        materials = data["materials"][:2]
        name_str = " / ".join(names) if names else "item"
        mat_str = materials[0] if materials else ""
        final[key] = {
            "name": name_str,
            "material": mat_str,
            "pixel_x": data["pixel_x"],
            "pixel_y": data["pixel_y"],
            "prompt": make_prompt("Item", name_str, mat_str),
        }
    return final


def _accumulate_item(registry, bitmappos, block_content, preceding, block_name=""):
    px, py = bitmappos
    col, row = px // 16, py // 16
    key = f"{col},{row}"

    ns = extract_field_from_block(block_content, "NameSingular") or block_name.replace("_", " ")
    adj = extract_field_from_block(block_content, "Adjective") or ""
    pf = extract_field_from_block(block_content, "PostFix") or ""

    # Fall back to nearest preceding block name if no NameSingular
    if not ns and preceding:
        items = re.findall(r"\n([a-z_][a-z_0-9]*)\s*\n?\s*\{", preceding)
        ns = items[-1].replace("_", " ") if items else "item"

    display = f"{adj} {ns}".strip() if adj else ns
    if pf:
        display = f"{display} {pf}"

    material = extract_material(block_content)

    if key not in registry:
        registry[key] = {"names": [], "materials": [], "pixel_x": px, "pixel_y": py}
    if display and display not in registry[key]["names"]:
        registry[key]["names"].append(display)
    if material and material not in registry[key]["materials"]:
        registry[key]["materials"].append(material)


# ─────────────────────────────────────────────
# Character parser (char.dat)
# ─────────────────────────────────────────────

def parse_char_dat_humanoid(filepath):
    """
    Parse char.dat for Humanoid.png body-part BitmapPos fields using top-level blocks.
    Returns registry for Humanoid sheet, keyed by "col,row".
    """
    text = strip_comments(Path(filepath).read_text())
    registry = {}

    body_part_fields = {
        "LegBitmapPos":   "legs",
        "TorsoBitmapPos": "torso",
        "ArmBitmapPos":   "arms",
        "HeadBitmapPos":  "head",
    }

    # Process top-level character blocks (e.g., "farmer { ... }")
    for block_name, block_content in extract_top_level_blocks(text):
        # Also process nested Config blocks within character blocks
        sub_blocks = [(None, block_content)]  # (config_name, content)
        for cfg_m in re.finditer(r'Config\s+([A-Z_][A-Z_0-9]*)\s*;', block_content):
            cfg_name = cfg_m.group(1)
            op, cp = match_braces(block_content, cfg_m.end())
            if op != -1:
                sub_blocks.append((cfg_name, block_content[op+1:cp]))

        for _cfg, content in sub_blocks:
            # Get character display name
            ns = extract_field_from_block(content, "NameSingular") or \
                 extract_field_from_block(content, "DefaultName") or \
                 block_name.replace("_", " ")

            for field, part_name in body_part_fields.items():
                m = re.search(rf'{field}\s*=\s*(\d+)\s*,\s*(\d+)', content)
                if not m:
                    continue
                px, py = int(m.group(1)), int(m.group(2))
                col, row = px // 16, py // 16
                key = f"{col},{row}"

                if key not in registry:
                    registry[key] = {"names": [], "pixel_x": px, "pixel_y": py}
                entry_str = f"{ns} {part_name}"
                if entry_str not in registry[key]["names"]:
                    registry[key]["names"].append(entry_str)

    final = {}
    for key, data in registry.items():
        names = data["names"][:3]
        name_str = " / ".join(names) if names else "humanoid body part"
        final[key] = {
            "name": name_str,
            "pixel_x": data["pixel_x"],
            "pixel_y": data["pixel_y"],
            "prompt": make_prompt("Humanoid", name_str, ""),
        }
    return final


def parse_char_torso(filepath):
    """
    Parse char.dat for Char.png. Char.png is driven solely by TorsoBitmapPos
    on normaltorso-type creatures (simple beasts whose entire visible sprite
    is their "torso" — see normaltorso::GetGraphicsContainerIndex() in
    bodypart.cpp, the only body part that renders to GR_CHARACTER instead of
    GR_HUMANOID). Positions outside Char.png's 600x200 bounds belong to
    humanoid creatures' torsos, which render to Humanoid.png instead (already
    handled by parse_char_dat_humanoid).
    Returns registry for Char sheet, keyed by "col,row".
    """
    text = strip_comments(Path(filepath).read_text())
    registry = {}

    for m in re.finditer(r"(?<![A-Za-z])TorsoBitmapPos\s*=\s*(\d+)\s*,\s*(\d+)", text):
        px, py = int(m.group(1)), int(m.group(2))
        if px + 16 > 600 or py + 16 > 200:
            continue

        col, row = px // 16, py // 16
        key = f"{col},{row}"

        before = text[:m.start()]
        chars = re.findall(r"\n([a-z_][a-z_0-9]*)\s*\n?\s*\{", before)
        char_name = chars[-1] if chars else ""

        ns_m = re.search(r'NameSingular\s*=\s*"([^"]*)"', before[-600:])
        adj_m = re.search(r'Adjective\s*=\s*"([^"]+)"', before[-600:])
        name = ns_m.group(1) if ns_m else char_name.replace("_", " ")
        adj = adj_m.group(1) if adj_m else ""
        display = f"{adj} {name}".strip() if adj else name

        if key not in registry:
            registry[key] = {"names": [], "pixel_x": px, "pixel_y": py}
        if display and display not in registry[key]["names"]:
            registry[key]["names"].append(display)

    final = {}
    for key, data in registry.items():
        names = data["names"][:3]
        name_str = " / ".join(names) if names else "creature sprite"
        final[key] = {
            "name": name_str,
            "pixel_x": data["pixel_x"],
            "pixel_y": data["pixel_y"],
            "prompt": make_prompt("Char", name_str, ""),
        }
    return final


# Item.dat fields that render worn/wielded equipment overlays onto Humanoid.png
# (see UpdateArmorPicture / UpdateWieldedPicture call sites in bodypart.cpp —
# all of these target GR_HUMANOID, never GR_CHARACTER).
CHAR_OVERLAY_FIELDS = {
    "WieldedBitmapPos":         "wielded",
    "HelmetBitmapPos":          "worn on head",
    "TorsoArmorBitmapPos":      "worn on torso",
    "AthleteArmArmorBitmapPos": "worn on torso",
    "ArmArmorBitmapPos":        "worn on arm",
    "LegArmorBitmapPos":        "worn on leg",
    "BootBitmapPos":            "worn on foot",
    "CloakBitmapPos":           "worn as cloak",
    "BeltBitmapPos":            "worn as belt",
    "GauntletBitmapPos":        "worn as gauntlet",
}


def parse_item_dat_char_overlays(filepath):
    """
    Parse item.dat for the worn/wielded equipment overlay BitmapPos fields
    that render onto Humanoid.png. Returns registry keyed by "col,row".
    """
    text = strip_comments(Path(filepath).read_text())
    registry = {}

    def scan_block(block_content, block_name):
        ns = extract_field_from_block(block_content, "NameSingular") or \
             block_name.replace("_", " ")
        adj = extract_field_from_block(block_content, "Adjective") or ""
        display = f"{adj} {ns}".strip() if adj else ns

        for field, label in CHAR_OVERLAY_FIELDS.items():
            for m in re.finditer(rf"(?<![A-Za-z]){field}\s*=\s*(\d+)\s*,\s*(\d+)", block_content):
                px, py = int(m.group(1)), int(m.group(2))
                col, row = px // 16, py // 16
                key = f"{col},{row}"
                entry_str = f"{display} ({label})".strip()
                if key not in registry:
                    registry[key] = {"names": [], "pixel_x": px, "pixel_y": py}
                if entry_str not in registry[key]["names"]:
                    registry[key]["names"].append(entry_str)

    for config_name, block_content, preceding in extract_config_blocks(text):
        scan_block(block_content, config_name.lower())

    for block_name, block_content in extract_top_level_blocks(text):
        scan_block(block_content, block_name)

    final = {}
    for key, data in registry.items():
        names = data["names"][:3]
        name_str = " / ".join(names) if names else "equipment overlay"
        final[key] = {
            "name": name_str,
            "pixel_x": data["pixel_x"],
            "pixel_y": data["pixel_y"],
            "prompt": make_prompt("Humanoid", name_str, ""),
        }
    return final


# ─────────────────────────────────────────────
# Manual registries for sheets without .dat mapping
# ─────────────────────────────────────────────

def build_symbol_registry():
    """Symbol.png (400x600) — deity/god icon grid. Manual mapping from gods.cpp."""
    gods = [
        (0, 0, "Valpuris", "sun and anchor", "god of order and justice"),
        (1, 0, "Seges", "wheat sheaf", "goddess of harvest and plenty"),
        (2, 0, "Silva", "oak leaf and bow", "goddess of the wild hunt"),
        (3, 0, "Sophos", "open eye and quill", "god of knowledge and magic"),
        (4, 0, "Loricatus", "hammer and anvil", "god of smithing and craft"),
        (5, 0, "Mortifer", "hourglass and skull", "god of death and entropy"),
        (6, 0, "Infuscor", "inverted crown", "god of shadows and betrayal"),
        (7, 0, "Cruentus", "crossed blades", "god of war and bloodshed"),
        (8, 0, "Legifer", "scales of justice", "god of law and binding oaths"),
        (9, 0, "Nefas", "broken chain", "god of chaos and forbidden knowledge"),
        (10, 0, "Dulcis", "honey comb", "goddess of pleasure"),
        (11, 0, "Mellis", "cup and vine", "god of feasting"),
        (12, 0, "Scabies", "plague skull", "god of disease and filth"),
        (13, 0, "Atavus", "coiled serpent", "god of ancestry and memory"),
        (14, 0, "Verax", "sunburst eye", "god of truth and oaths"),
    ]
    registry = {}
    for col, row, name, symbol, domain in gods:
        key = f"{col},{row}"
        registry[key] = {
            "name": f"{name} symbol",
            "material": "",
            "pixel_x": col * 16,
            "pixel_y": row * 16,
            "prompt": (
                f"dark fantasy deity symbol, 16x16 pixel art icon, {name} divine sigil, "
                f"{symbol}, {domain}, Tolkien pantheon, heraldic gold on dark background, "
                f"flat colors, strong outline, no gradients"
            ),
        }
    return registry


def build_effect_registry():
    """Effect.png (128x64) — combat spell/impact tiles."""
    effects = [
        (0, 0, "fire blast", "orange-red flames"),
        (1, 0, "ice shard", "blue-white ice crystal"),
        (2, 0, "lightning bolt", "yellow electric spark"),
        (3, 0, "acid splash", "green corrosive liquid"),
        (4, 0, "holy light", "white-gold divine radiance"),
        (5, 0, "shadow bolt", "dark purple shadow energy"),
        (6, 0, "poison cloud", "sickly green toxic mist"),
        (7, 0, "physical impact", "gray impact sparks"),
        (0, 1, "explosion flash", "bright orange-white detonation"),
        (1, 1, "sound wave", "blue-white concentric rings"),
        (2, 1, "blood spatter", "crimson red droplets"),
        (3, 1, "smoke puff", "dark gray smoke wisp"),
        (4, 1, "magic spark", "violet-white magical energy"),
        (5, 1, "water splash", "blue water droplets"),
        (6, 1, "stone shatter", "gray rock fragments"),
        (7, 1, "healing glow", "soft green restoration light"),
    ]
    registry = {}
    for col, row, name, description in effects:
        key = f"{col},{row}"
        registry[key] = {
            "name": name,
            "pixel_x": col * 16,
            "pixel_y": row * 16,
            "prompt": (
                f"dark fantasy roguelike combat effect sprite, 16x16 pixel art, "
                f"{name}: {description}, particle effect, high contrast on black background, "
                f"flat colors, glowing, no gradients"
            ),
        }
    return registry


def build_smiley_registry():
    """
    Smiley.png (144x48) — HUD player health face strip.
    3 tiles wide × 3 tiles tall = 48×48 per face, 3 faces total.
    Actually: the strip is 144×48, so 3 faces of 48×48 each (3×3 tiles).
    We treat each 48×48 face as a single generation unit (col in units of 3 tiles).
    """
    faces = [
        (0, "healthy adventurer face", "confident alert expression", "full health"),
        (1, "wounded adventurer face", "pained grimace", "badly hurt"),
        (2, "dying adventurer face", "pale terrified expression", "near death"),
    ]
    registry = {}
    for face_idx, name, expression, state in faces:
        # Each face occupies 3 columns of 16px = 48px wide
        for dc in range(3):
            for dr in range(3):
                col = face_idx * 3 + dc
                row = dr
                key = f"{col},{row}"
                registry[key] = {
                    "name": name,
                    "pixel_x": col * 16,
                    "pixel_y": row * 16,
                    # All sub-tiles of a face share a prompt — generator assembles
                    "_face_idx": face_idx,
                    "_face_col": dc,
                    "_face_row": dr,
                    "prompt": (
                        f"dark fantasy roguelike HUD portrait, 48x48 pixel art, "
                        f"{name}, {expression}, adventurer health indicator, {state}, "
                        f"helmet and armor, muted palette, strong black outline, "
                        f"no gradients, centered face in frame"
                    ),
                }
    return registry


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

SHEET_BUILDERS = {
    "GLTerra":   lambda: parse_terrain_dat(SCRIPT_DIR / "glterra.dat", "GLTerra"),
    "OLTerra":   lambda: parse_terrain_dat(SCRIPT_DIR / "olterra.dat", "OLTerra"),
    "WTerra":    lambda: parse_owterra(SCRIPT_DIR / "owterra.dat"),
    "Item":      lambda: parse_item_dat(SCRIPT_DIR / "item.dat"),
    "Char":      lambda: parse_char_torso(SCRIPT_DIR / "char.dat"),
    "Humanoid":  lambda: {**parse_item_dat_char_overlays(SCRIPT_DIR / "item.dat"),
                          **parse_char_dat_humanoid(SCRIPT_DIR / "char.dat")},
    "Symbol":    build_symbol_registry,
    "Effect":    build_effect_registry,
    "Smiley":    build_smiley_registry,
}


def build_all(sheets=None):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = sheets or list(SHEET_BUILDERS.keys())
    for sheet in targets:
        if sheet not in SHEET_BUILDERS:
            print(f"Unknown sheet: {sheet}")
            continue
        print(f"Building registry: {sheet} ...", end=" ", flush=True)
        registry = SHEET_BUILDERS[sheet]()
        out_path = OUT_DIR / f"{sheet.lower()}_tiles.json"
        out_path.write_text(json.dumps(registry, indent=2))
        print(f"{len(registry)} tiles → {out_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Build VALE tile registries from .dat files.")
    parser.add_argument("--sheet", help="Build only this sheet (e.g. GLTerra). Default: all.")
    args = parser.parse_args()
    build_all([args.sheet] if args.sheet else None)


if __name__ == "__main__":
    main()
