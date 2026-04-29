/*
 *
 *  Iter Vehemens ad Necem (IVAN)
 *  Copyright (C) Timo Kiviluoto
 *  Released under the GNU General
 *  Public License
 *
 *  See LICENSING which should be included
 *  along with this file for more details
 *
 */

#ifndef __WHANDLER_H__
#define __WHANDLER_H__

#ifdef USE_SDL
#include <vector>
#include <array>
#include "SDL.h"
#endif

#ifdef __DJGPP__
#include <ctime>
#endif

#include "felibdef.h"
#include "festring.h"

#define GET_KEY globalwindowhandler::GetKey
#define READ_KEY globalwindowhandler::ReadKey
#define GET_TICK globalwindowhandler::GetTick
#define WAIT_FOR_KEY_DOWN globalwindowhandler::WaitForKeyDown
#define WAIT_FOR_KEY_UP globalwindowhandler::WaitForKeyUp

// Gamepad button constants (mapped to key codes for injection into KeyBuffer)
#define GAMEPAD_A_BUTTON    0xE101
#define GAMEPAD_B_BUTTON    0xE102
#define GAMEPAD_X_BUTTON    0xE103
#define GAMEPAD_Y_BUTTON    0xE104
#define GAMEPAD_LEFT_BUMPER 0xE105
#define GAMEPAD_RIGHT_BUMPER 0xE106
#define GAMEPAD_BACK        0xE107
#define GAMEPAD_START       0xE108
#define GAMEPAD_GUIDE       0xE109
#define GAMEPAD_LEFT_THUMB  0xE10A
#define GAMEPAD_RIGHT_THUMB 0xE10B
// D-pad buttons (mapped to directional keys)
#define GAMEPAD_DPAD_UP     KEY_UP + 0xE000
#define GAMEPAD_DPAD_DOWN   KEY_DOWN + 0xE000
#define GAMEPAD_DPAD_LEFT   KEY_LEFT + 0xE000
#define GAMEPAD_DPAD_RIGHT  KEY_RIGHT + 0xE000
// Gamepad axis constants for movement detection
#define GAMEPAD_LEFT_STICK_X    0
#define GAMEPAD_LEFT_STICK_Y    1
#define GAMEPAD_RIGHT_STICK_X   2
#define GAMEPAD_RIGHT_STICK_Y   3
#define GAMEPAD_LEFT_TRIGGER    4
#define GAMEPAD_RIGHT_TRIGGER   5
// Gamepad deadzone threshold (SDL axis values range from -32768 to 32767)
#define GAMEPAD_DEADZONE        2000

struct mouseclick{
 int btn=-1;
 v2 pos;
 int wheelY=0;
};

// Maximum number of gamepads supported simultaneously
#define MAX_GAMEPADS 4

class globalwindowhandler
{
 public:
  static bool IsKeyPressed(int iSDLScanCode);
  // Gamepad support (Phase 1 & 2)
  static void ProcessGamepadInput();
  static int GetDirectionFromGamepad(); // Returns direction index 0-8 (NW=0..SE=7, YOURSELF=8), or -1 if no input
  static v2 GetCameraDeltaFromGamepad(); // Returns camera pan deltas from right stick, or zero vector
  static int GetGamepadButtonKey(); // Returns a command key code if a mapped gamepad button was just pressed, else 0
  static bool IsGamepadEnabled() { return GamepadEnabled; }
  static void SetGamepadEnabled(bool Enabled) { GamepadEnabled = Enabled; }
  static void ResetKeyTimeout(){SetKeyTimeout(0,iRestWaitKey);}
  static void CheckKeyTimeout();
  static void SuspendKeyTimeout();
  static void ResumeKeyTimeout();
  static truth IsKeyTimeoutEnabled();
  static void SetKeyTimeout(int iTimeoutMillis,int iDefaultReturnedKey);
  static mouseclick ConsumeMouseEvent();
  static void SetPlayInBackground(truth b){playInBackground=b;}
  static float GetFPS(bool bInsta);
  static truth HasKeysOnBuffer();
  static uint PollEvents(SDL_Event* pEvent = NULL);
  static uint UpdateMouse();
  static int GetKey(truth = true);
  static int ReadKey();
  static truth WaitForKeyEvent(uint Key);
  static truth WaitForKeyDown(){return WaitForKeyEvent(SDL_KEYDOWN);}
  static truth WaitForKeyUp  (){return WaitForKeyEvent(SDL_KEYUP  );}
  static v2 GetMouseLocation();
  static bool IsMouseAtRect(v2, v2, bool = true, v2 = v2());
  static truth IsLastSDLkeyEventWasKeyUp();
  static void InstallControlLoop(truth (*)());
  static void DeInstallControlLoop(truth (*)());
  static ulong GetTick() { return Tick; }
  static truth ControlLoopsInstalled() { return Controls; }
  static void EnableControlLoops() { ControlLoopsEnabled = true; }
  static void DisableControlLoops() { ControlLoopsEnabled = false; }
  static truth ShiftIsDown();
  static void SetScrshotDirectory(cfestring& DirectoryName){ ScrshotDirectoryName = DirectoryName; }
  static festring ScrshotNameHandler(); // Number successive screenshots based on existing filenames
  static void SetAddFrameSkip(int i);
#ifdef USE_SDL
  static void Init();
  static void SetQuitMessageHandler(truth (*What)()){ QuitMessageHandler = What; }
  static ulong UpdateTick() { return Tick = SDL_GetTicks() / 40; }
  static void SetFunctionKeyHandler(bool (*What)(SDL_Keycode)){ FunctionKeyHandler = What; }
  static void SetControlKeyHandler(bool (*What)(SDL_Keycode)){ ControlKeyHandler = What; }
#endif

#ifdef __DJGPP__
  static void Init() { }
  static void SetQuitMessageHandler(truth (*)()) { }
  static ulong UpdateTick() { return Tick = uclock() * 25 / UCLOCKS_PER_SEC; }
#endif

  const static int iRestWaitKey;

 private:
#ifdef USE_SDL
  struct gamepadstate {
    SDL_GameController* Controller = nullptr;
    bool Connected = false;
    std::array<bool, SDL_CONTROLLER_BUTTON_MAX> ButtonState{}; // Track current press state
    std::array<float, 6> AxisValues{}; // X/Y left stick, X/Y right stick, LT, RT
    int PlayerIndex = -1;
  };
  static gamepadstate Gamepads[MAX_GAMEPADS];
  static int NumGamepads;
  static bool GamepadEnabled;
  static void OpenGamepad(SDL_JoystickID JoyId);
  static void CloseGamepad(int Index);
  static int ChkCtrlKey(SDL_Event* Event);
  static void ProcessMessage(SDL_Event*);
  static void ProcessKeyDownMessage(SDL_Event* Event);
  static void AddKeyToBuffer(int KeyPressed);
  static std::vector<int> KeyBuffer;
  static truth (*QuitMessageHandler)();
  static bool (*FunctionKeyHandler)(SDL_Keycode);
  static bool (*ControlKeyHandler)(SDL_Keycode);
#endif
  static truth (*ControlLoop[MAX_CONTROLS])();
  static int Controls;
  static ulong Tick;
  static truth ControlLoopsEnabled;
  static truth playInBackground;
  static festring ScrshotDirectoryName;
};

#endif
