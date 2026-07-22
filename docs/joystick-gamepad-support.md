# Joystick/Gamepad Support - TODO List

## Overview

This document outlines the work items needed to add joystick/gamepad support to VALE. The game currently uses SDL2 for input handling, which provides built-in joystick and gamepad APIs. This implementation would allow players to use gamepads (Xbox, PlayStation, Switch Pro, generic USB controllers) in addition to keyboard/mouse controls.

---

## Phase 1: Foundation & Infrastructure

### [x] 1.1 Add SDL GameController initialization
**File:** `FeLib/Source/whandler.cpp`
- ✅ Added `SDL_GameControllerOpen()` calls during `globalwindowhandler::Init()`
- ✅ Track open gamepad controllers in a static array (`Gamepads[MAX_GAMEPADS]`)
- ✅ Handle controller connect/disconnect events via `SDL_CONTROLLERDEVICEADDED` / `SDL_CONTROLLERDEVICEREMOVED`
- ✅ Implemented `SDL_GameControllerClose()` on disconnect (via `CloseGamepad()`)

### [x] 1.2 Add joystick state tracking structures
**File:** `FeLib/Include/whandler.h` + `FeLib/Source/whandler.cpp`
- ✅ Created `gamepadstate` struct to hold gamepad state per controller
- ✅ Track which buttons are currently pressed/released (`ButtonState[SDL_CONTROLLER_BUTTON_MAX]`)
- ✅ Store analog stick positions (left stick X/Y, right stick X/Y) and trigger values (LT/RT)
- ✅ Added `GAMEPAD_DEADZONE` constant for drift prevention

### [x] 1.3 Add gamepad event polling to the main event loop
**File:** `FeLib/Source/whandler.cpp`
- ✅ Implemented `globalwindowhandler::ProcessGamepadInput()` method
- ✅ Maps gamepad buttons (A, B, X, Y, bumpers, D-pad) into the existing key buffer via `AddKeyToBuffer()`
- ✅ Called each frame in `GetKey()` for continuous polling
- ✅ Injects gamepad-derived keys as high-value constants (0xE1xx range) to avoid conflicts with normal keys

### [x] 1.4 Add configuration option for enabling/disabling gamepad
**File:** `Main/Source/iconf.cpp` + `Main/Include/iconf.h`
- ✅ Added `UseGamepad` truthoption in ivanconfig ("Enable gamepad/joystick support")
- ✅ Default is enabled (`true`)
- ✅ Changer method updates `globalwindowhandler::SetGamepadEnabled()`

---

## Phase 2: Movement Support

### [x] 2.1 Define gamepad movement mapping constants
**File:** `FeLib/Include/whandler.h`
- ✅ Reused existing axis constants (`GAMEPAD_LEFT_STICK_X/Y`, `GAMEPAD_RIGHT_STICK_X/Y`)
- ✅ Deadzone threshold already defined as `GAMEPAD_DEADZONE` (2000) in Phase 1
- Direction mapping: NW=0, N=1, NE=2, W=3, E=4, SW=5, S=6, SE=7, YOURSELF=8

### [x] 2.2 Implement left stick movement detection
**File:** `FeLib/Source/whandler.cpp`
- ✅ Implemented `globalwindowhandler::GetDirectionFromGamepad()` method
- ✅ Reads left analog stick axes (already normalized in `ProcessGamepadInput()`)
- ✅ Applies deadzone to prevent drift (`GAMEPAD_DEADZONE / 32767.0f`)
- ✅ Maps stick direction to one of the 8 movement directions using angle-based octant classification via `atan2`
- ✅ Supports both D-pad and left stick for movement (stick takes precedence over D-pad)
- ✅ Falls back to D-pad when stick is in deadzone

### [x] 2.3 Integrate gamepad movement into command dispatch
**File:** `Main/Source/char.cpp` + `Main/Source/game.cpp`
- ✅ Extended character's `GetPlayerCommand()` loop to check gamepad direction alongside regular move keys
- ✅ Added `globalwindowhandler::GetDirectionFromGamepad()` call that returns direction index 0-8
- ✅ Movement via gamepad uses the same `TryMove()` path as keyboard input
- ✅ Also extended `game::DirectionQuestion()` to accept gamepad directional input for prompts like "Which way do you want to open?"

### [x] 2.4 Implement right stick / camera control (optional)
**File:** `FeLib/Source/whandler.cpp` + `Main/Source/game.cpp`
- ✅ Implemented `globalwindowhandler::GetCameraDeltaFromGamepad()` method
- ✅ Reads right analog stick axes and returns v2 delta in tiles
- ✅ Integrated into game loop's main tick processing (`game::Run()`)
- ✅ Camera panning works in wilderness/world map mode with bounds clamping

---

## Phase 3: Command Dispatch Integration

### [x] 3.1 Add gamepad button-to-command mapping system
**File:** `FeLib/Source/whandler.cpp`
- ✅ Created a static `GamepadCommandMap` array mapping SDL_GameControllerButton indices to command key codes
- Uses SDL_GameControllerButton constants for portability across controller types
- Default mappings:
  - A/X → '.' (NOP / wait)
  - B → 'd' (drop item)
  - X/Y → ',' (pick up item) / 'i' (inventory)
  - LB → 'E' (equipment screen)
  - RB → 'D' (drink)
  - Start → 'S' (save and quit)
  - Back → '?' (show key layout / help)

### [x] 3.2 Implement gamepad button polling in the main loop
**File:** `FeLib/Source/whandler.cpp`
- ✅ Implemented `globalwindowhandler::GetGamepadButtonKey()` method
- Iterates through all connected gamepads each call, checking mapped buttons for newly pressed state
- Detects fresh presses by comparing current SDL_GameControllerGetButton result against ButtonState array (set in ProcessGamepadInput)
- Returns the corresponding command key code on first match, or 0 if no mapped button was pressed
- Single-press behavior: only triggers once per press (not repeated while held), unlike analog stick movement which is continuous

### [x] 3.3 Integrate with existing `GetCommand()` flow
**File:** `Main/Source/char.cpp`
- ✅ Added gamepad button check in `character::GetPlayerCommand()` before the command lookup loop
- When a mapped gamepad button is pressed, its key code replaces the keyboard-derived Key value
- Commands are dispatched through the exact same path as keyboard input (matching against `command::GetKey()`)
- No changes needed to the command class or command system - gamepad buttons reuse existing command infrastructure

### [x] 3.4 Handle movement commands via gamepad
**File:** `Main/Source/command.cpp`
- ✅ Movement commands (`Go`, `Kick`, attack directions, etc.) already use `GetDirectionVectorForKey()`
- Phase 2 integrated `GetDirectionFromGamepad()` into the movement check loop in GetPlayerCommand()
- Gamepad directional input (left stick + D-pad) works seamlessly with all direction-based commands
- Movement via gamepad uses the same `TryMove()` path as keyboard input

---

## Phase 4: Menu & UI Navigation

### [x] 4.1 Add gamepad navigation to menus (feio.cpp)
**File:** `FeLib/Source/feio.cpp`
- ✅ Extended `iosystem::Menu()` to accept gamepad input for up/down selection via D-pad/left stick
- ✅ Mapped A/X button (`GAMEPAD_A_BUTTON` / `GAMEPAD_X_BUTTON`) to "select" (confirm)
- ✅ Mapped B/Circle button (`GAMEPAD_B_BUTTON`) to "back" (returns -1 to signal cancellation)
- ✅ Supports D-pad for menu navigation (up/down directions mapped via `GAMEPAD_DPAD_UP`/`GAMEPAD_DPAD_DOWN`)

### [x] 4.2 Add gamepad support to StringQuestion / NumberQuestion
**File:** `FeLib/Source/feio.cpp`
- ✅ Added gamepad D-pad keys (`GAMEPAD_DPAD_LEFT`, `GAMEPAD_DPAD_RIGHT`) for cursor movement in text input fields
- ✅ Mapped A/X button (`GAMEPAD_A_BUTTON` / `GAMEPAD_X_BUTTON`) to confirm (same as Enter)
- ✅ Mapped B/Circle button (`GAMEPAD_B_BUTTON`) to backspace (same as Backspace key)
- ✅ Added gamepad D-pad up/down for history navigation in StringQuestion
- ✅ Updated input acceptance loops to recognize all gamepad keys alongside keyboard equivalents

### [x] 4.3 Add gamepad support to felist (list navigation)
**File:** `FeLib/Source/felist.cpp`
- ✅ Extended felist's `DrawFiltered()` to accept gamepad D-pad for scrolling through lists
- ✅ Added `GAMEPAD_DPAD_UP` and `GAMEPAD_DPAD_DOWN` alongside existing `KEY_UP`/`KEY_DOWN` checks
- ✅ Mapped A/X button (`GAMEPAD_A_BUTTON` / `GAMEPAD_X_BUTTON`) for entry selection (same as Enter)
- ✅ Mapped B/Circle button (`GAMEPAD_B_BUTTON`) for cancel/back (same as Escape)
- ✅ Works with all list-based UI: inventory, equipment screens, save game loader, etc.

---

## Phase 5: Configuration & Customization

### [ ] 5.1 Add gamepad button configuration UI
**File:** `Main/Source/iconf.cpp` + `Main/Include/iconf.h`
- Create a configuration screen where players can remap gamepad buttons to commands
- Similar to the existing custom key binding system (`SetupCustomKeys`)
- Store gamepad bindings in config file

### [ ] 5.2 Add deadzone and sensitivity settings
**File:** `Main/Source/iconf.cpp` + `Main/Include/iconf.h`
- Add configurable analog stick deadzone (numberoption)
- Add configurable movement speed / repeat rate for analog sticks
- Add trigger deadzone settings

### [ ] 5.3 Support multiple controller profiles
**File:** New or extended config system
- Allow saving different gamepad layouts per character or per play session
- Consider SDL_GameControllerDB for automatic controller mapping support

---

## Phase 6: Haptic Feedback & Advanced Features (Optional)

### [ ] 6.1 Add rumble/vibration feedback
**File:** `FeLib/Source/whandler.cpp` + audio/sfx integration
- Use `SDL_GameControllerRumble()` for haptic feedback on hits, blocks, pickups
- Tie into existing SFX system for synchronized audio + vibration

### [ ] 6.2 Add controller LED / RGB support (optional)
**File:** `FeLib/Source/whandler.cpp`
- Use `SDL_GameControllerSetLED()` to show player number or status via controller LEDs
- Useful for multiplayer or just visual flair

---

## Phase 7: Testing & Polish

### [ ] 7.1 Test with multiple controller types
- Xbox One / Series X|S controller
- PlayStation DualShock4 / DualSense
- Nintendo Switch Pro Controller
- Generic USB gamepads (Logitech, etc.)
- Steam Deck (SDL2 handles this well)

### [ ] 7.2 Handle hot-plugging
- Test connecting/disconnecting controllers while the game is running
- Ensure no crashes or lost input when controllers are swapped

### [ ] 7.3 Add controller detection status to main menu
**File:** `Main/Source/main.cpp` + `igraph.cpp`
- Show which controllers are connected on the main menu
- Display current button mappings in help screen (F1)

---

## Key Files Summary

| File | Purpose |
|------|---------|
| `FeLib/Include/whandler.h` | Window/input handler header - add gamepad state declarations |
| `FeLib/Source/whandler.cpp` | SDL event processing - add gamepad polling and button mapping |
| `Main/Include/command.h` | Command class definition - extend for gamepad key bindings |
| `Main/Source/command.cpp` | Command dispatch - integrate gamepad input into command flow |
| `Main/Include/game.h` | Game header - add gamepad direction detection methods |
| `Main/Source/game.cpp` | Main game logic - integrate `GetDirectionFromGamepad()` |
| `FeLib/Include/feio.h` / `feio.cpp` | Input/output system - extend menus for gamepad navigation |
| `Main/Include/iconf.h` / `iconf.cpp` | Configuration - add gamepad settings |
| `Main/Include/ivandef.h` | Constants - add gamepad button/axis constants |

## Key Functions to Modify

1. **`globalwindowhandler::Init()`** - Initialize SDL_GameController for connected controllers
2. **`globalwindowhandler::PollEvents()`** - Process controller events alongside keyboard/mouse
3. **`game::GetDirectionVectorForKey(int)`** - Also check gamepad stick/D-pad state
4. **`commandsystem::GetCommand(key)` flow** - Accept gamepad-derived keys
5. **`iosystem::Menu()`** - Accept gamepad navigation input

## Design Decisions to Make

1. **Input model**: Should gamepad buttons inject into the existing key buffer (simpler, less code change) or use a parallel dispatch path (more flexible)?
2. **Movement source**: Support both D-pad and left stick? Both simultaneously?
3. **Button mapping strategy**: Fixed default mappings vs fully configurable from day one?
4. **Controller count**: Single controller only at launch, or support for multiple controllers?
5. **SDL version**: Target SDL 2.x (already used) - use `SDL_GameController` API which abstracts different controller types

## Dependencies

- SDL2 already linked (see `FeLib/CMakeLists.txt`)
- No new external dependencies required
- Uses existing configuration system (`config.h`, `iconf.cpp`)
- Compatible with existing command/key binding infrastructure
