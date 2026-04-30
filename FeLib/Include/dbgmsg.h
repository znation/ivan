/**
 * Stub dbgmsg.h - provides no-op implementations for debugging macros
 * and the dbgmsg namespace when DBGMSG is defined.
 */

#ifndef INCLUDE_DBGMSG_H_
#define INCLUDE_DBGMSG_H_

#include <sstream>
#include <string>

/* ---- dbgmsg namespace stubs ---- */

namespace dbgmsg {

inline void SetDebugLogPath(const char*) {}

inline std::string getCurrentStackTrace(bool, int) { return ""; }
inline std::string getCurrentStackTrace(std::string, bool, bool) { return ""; }

inline void SigHndlr(int) {}

} /* namespace dbgmsg */

/* ---- Debug macro stubs (used when DBGMSG is defined) ---- */

#define DBGOE(s)
#define DBGSS(s)
#define DBG1(a)
#define DBG2(a, b)
#define DBG3(a, b, c)
#define DBG4(a, b, c, d)
#define DBG5(a, b, c, d, e)
#define DBG6(a, b, c, d, e, f)
#define DBG7(a, b, c, d, e, f, g)
#define DBG8(a, b, c, d, e, f, g, h)
#define DBG9(a, b, c, d, e, f, g, h, i)

#define DBGLN
#define DBGTOSTR_(str) #str
#define DBGTOSTR(str) DBGTOSTR_(str)
#define DBGB(B)
#define DBGSB(B)
#define DBGI(I)
#define DBGSI(I)
#define DBGIF(F)
#define DBGSF(F)
#define DBGC(C)
#define DBGSC(C)
#define DBGS(SS)
#define DBGSTK
#define DBGBREAKPOINT
#define DBGEXEC(cmds)
#define DBGSETV(id, val)
#define DBGGETV(id, defval) (defval)
#define DBGGETVD(id, defval) (defval)

#endif /* INCLUDE_DBGMSG_H_ */
