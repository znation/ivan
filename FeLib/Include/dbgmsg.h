/**
 * dbgmsg.h - provides active implementations for debugging macros
 * and the dbgmsg namespace when DBGMSG is defined.
 */

#ifndef INCLUDE_DBGMSG_H_
#define INCLUDE_DBGMSG_H_

#include <iostream>
#include <sstream>
#include <string>

/* ---- dbgmsg namespace stubs ---- */

namespace dbgmsg {

inline void SetDebugLogPath(const char*) {}

inline std::string getCurrentStackTrace(bool, int) { return ""; }
inline std::string getCurrentStackTrace(std::string, bool, bool) { return ""; }

inline void SigHndlr(int) {}

template <typename... Args>
void PrintDebug(Args&&... args) {
    std::ostringstream oss;
    (oss << ... << args);
    std::cerr << "[DBG] " << oss.str() << std::endl;
}

} /* namespace dbgmsg */

/* ---- Debug macros (used when DBGMSG is defined) ---- */

#define DBGOE(s) \
    do { std::cerr << "[DBG] ERROR: " << (s) << std::endl; } while(0)
#define DBGSS(s) \
    do { std::cerr << "[DBG] " << (s) << std::endl; } while(0)
#define DBG1(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG2(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG3(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG4(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG5(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG6(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG7(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG8(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)
#define DBG9(a, ...) \
    do { dbgmsg::PrintDebug(a, ##__VA_ARGS__); } while(0)

#define DBGLN std::cerr << std::endl
#define DBGTOSTR_(str) #str
#define DBGTOSTR(str) DBGTOSTR_(str)
#define DBGB(B) \
    do { std::cerr << "[DBG] " << (B) << std::endl; } while(0)
#define DBGSB(B) \
    do { std::cerr << "[DBG] " << (B) << std::endl; } while(0)
#define DBGI(I) \
    do { std::cerr << "[DBG] " << (I) << std::endl; } while(0)
#define DBGSI(I) \
    do { std::cerr << "[DBG] " << (I) << std::endl; } while(0)
#define DBGIF(F) \
    do { std::cerr << "[DBG] " << (F) << std::endl; } while(0)
#define DBGSF(F) \
    do { std::cerr << "[DBG] " << (F) << std::endl; } while(0)
#define DBGC(C) \
    do { std::cerr << "[DBG] " << (C) << std::endl; } while(0)
#define DBGSC(C) \
    do { std::cerr << "[DBG] " << (C) << std::endl; } while(0)
#define DBGS(SS) \
    do { std::cerr << "[DBG] " << (SS) << std::endl; } while(0)
#define DBGSTK \
    do { std::cerr << "[DBG] Stack: " << dbgmsg::getCurrentStackTrace(true, 5) << std::endl; } while(0)
#define DBGBREAKPOINT \
    do { __builtin_trap(); } while(0)
#define DBGEXEC(cmds) cmds
#define DBGSETV(id, val) ((void)0)
#define DBGGETV(id, defval) (defval)
#define DBGGETVD(id, defval) (defval)

#endif /* INCLUDE_DBGMSG_H_ */
