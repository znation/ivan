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

namespace detail {
template<typename T>
inline void print_to_stream(std::ostringstream& oss, T&& val) { oss << std::forward<T>(val); }
template<typename... Args>
inline void print_to_stream_all(std::ostringstream& oss, Args&&... args) {
    (void)std::initializer<int>{(print_to_stream(oss, std::forward<Args>(args)), 0)...};
}
} /* namespace detail */

template <typename... Args>
void PrintDebug(Args&&... args) {
    std::ostringstream oss;
    detail::print_to_stream_all(oss, std::forward<Args>(args)...);
    std::cerr << "[DBG] " << oss.str() << std::endl;
}

} /* namespace dbgmsg */

/* ---- Debug macros (used when DBGMSG is defined) ---- */

#define DBGOE(s) __extension__({ std::cerr << "[DBG] ERROR: " << (s) << std::endl; 0; })
#define DBGSS(s) __extension__({ std::cerr << "[DBG] " << (s) << std::endl; 0; })
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
#define DBGB(B) __extension__({ std::cerr << "[DBG] " << (B) << std::endl; 0; })
#define DBGSB(B) __extension__({ std::cerr << "[DBG] " << (B) << std::endl; 0; })
#define DBGI(I) __extension__({ std::cerr << "[DBG] " << (I) << std::endl; 0; })
#define DBGSI(I) __extension__({ std::cerr << "[DBG] " << (I) << std::endl; 0; })
#define DBGIF(F) __extension__({ std::cerr << "[DBG] " << (F) << std::endl; 0; })
#define DBGSF(F) __extension__({ std::cerr << "[DBG] " << (F) << std::endl; 0; })
#define DBGC(C) __extension__({ std::cerr << "[DBG] " << (C) << std::endl; 0; })
#define DBGSC(C) __extension__({ std::cerr << "[DBG] " << (C) << std::endl; 0; })
#define DBGS(SS) __extension__({ std::cerr << "[DBG] " << (SS) << std::endl; 0; })
#define DBGSTK \
    do { std::cerr << "[DBG] Stack: " << dbgmsg::getCurrentStackTrace(true, 5) << std::endl; } while(0)
#define DBGBREAKPOINT \
    do { __builtin_trap(); } while(0)
#define DBGEXEC(cmds) cmds
#define DBGSETV(id, val) ((void)0)
#define DBGGETV(id, defval) (defval)
#define DBGGETVD(id, defval) (defval)

#endif /* INCLUDE_DBGMSG_H_ */
