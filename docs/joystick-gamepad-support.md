# Joystick/Gamepad Support - TODO List

## Overview

This document outlines the work items needed to add joystick/gamepad support to IVAN. The game currently uses SDL2 for input handling, which provides built-in joystick and gamepad APIs. This implementation would allow players to use gamepads (Xbox, PlayStation, Switch Pro, generic USB controllers) in addition to keyboard/mouse controls.

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

### [ ] 2.1 Define gamepad movement mapping constants
**File:** `Main/Include/ivandef.h` or new file `Main/Include/gamepaddef.h`
- Define constants for gamepad button mappings (e.g., `GAMEPAD_LEFT_STICK_X`, `GAMEPAD_A_BUTTON`)
- Define deadzone thresholds for analog sticks
- Consider configurable mapping support

### [ ] 2.2 Implement left stick movement detection
**File:** `FeLib/Source/whandler.cpp` + `Main/Source/game.cpp`
- Read left analog stick (axis 0 = X, axis 1 = Y) in the gamepad state update
- Apply deadzone to prevent drift
- Map stick direction to one of the 8 movement directions (NW, N, NE, W, E, SW, S, SE) or "yourself" (center)
- Support both D-pad and left stick for movement

### [ ] 2.3 Integrate gamepad movement into `GetDirectionVectorForKey()`
**File:** `Main/Source/game.cpp`
- Extend `game::GetDirectionVectorForKey(int Key)` to also check gamepad state
- Add a new method like `game::GetDirectionFromGamepad()` that returns the current direction from gamepad input
- The function should return a direction vector based on left stick or D-pad position

### [ ] 2.4 Implement right stick / camera control (optional)
**File:** `Main/Source/game.cpp` + `FeLib/Source/whandler.cpp`
- If desired, allow right analog stick to control camera panning in wilderness/world map views
- Map right stick axes to camera movement deltas

---

## Phase 3: Command Dispatch Integration

### [ ] 3.1 Add gamepad button-to-command mapping system
**File:** `Main/Include/command.h` + `Main/Source/command.cpp`
- Extend the `command` class to support a fourth key binding (Key5) for gamepad buttons
- Or create a parallel gamepad command map that maps gamepad buttons to commands
- Consider using SDL_GameControllerButton constants for portability

### [ ] 3.2 Implement gamepad button polling in the main loop
**File:** `FeLib/Source/whandler.cpp` + `Main/Source/game.cpp`
- In the main game loop, check gamepad buttons each frame/tick
- When a gamepad button is pressed that maps to a command, dispatch it the same way keyboard input does
- Handle button repeat for movement (analog stick) vs single press for actions

### [ ] 3.3 Integrate with existing `GetCommand()` flow
**File:** `Main/Source/game.cpp`
- Wherever `GET_KEY()` is called and results are passed to command dispatch, also check gamepad state
- The key insight: commands are dispatched by matching a key against `command::GetKey()`. We need to either:
  - Option A: Inject gamepad-derived keys into the existing key buffer (simpler)
  - Option B: Add a parallel path that checks gamepad buttons directly (more flexible)

### [ ] 3.4 Handle movement commands via gamepad
**File:** `Main/Source/command.cpp`
- Movement commands (`Go`, `Kick`, attack directions, etc.) already use `GetDirectionVectorForKey()`
- Once step 2.3 is done, these will automatically work with gamepad input

---

## Phase 4: Menu & UI Navigation

### [ ] 4.1 Add gamepad navigation to menus (feio.cpp)
**File:** `FeLib/Source/feio.cpp`
- Extend `iosystem::Menu()` to accept gamepad input for up/down selection
- Map A/X button to "select" and B/Circle to "back"
- Support D-pad or left stick for menu navigation

### [ ] 4.2 Add gamepad support to StringQuestion / NumberQuestion
**File:** `FeLib/Source/feio.cpp`
- Allow gamepad buttons for cursor movement in text input fields
- Map A/X to confirm, B/Circle to backspace or cancel

### [ ] 4.3 Add gamepad support to felist (list navigation)
**File:** `FeLib/Include/felist.h` + `FeLib/Source/felist.cpp`
- Extend felist to accept gamepad input for scrolling through lists
- This is used extensively in inventory, equipment screens, etc.

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
