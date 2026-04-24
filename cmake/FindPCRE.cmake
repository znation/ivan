# - Find PCRE2 (PCRE is deprecated, PCRE2 is the modern replacement)
# Find the native PCRE2 headers and libraries.
#
# PCRE_FOUND       - True if PCRE2 found.
# PCRE_LIBRARIES   - List of libraries when using PCRE2.
# PCRE_INCLUDE_DIRS - where to find pcre2.h, etc.

include(FindPkgConfig)
if(PKG_CONFIG_FOUND)
  pkg_check_modules(PCRE libpcre2-8)
  if(PCRE_FOUND)
    set(PCRE_INCLUDE_DIRS ${PCRE_INCLUDE_DIRS} ${PCRE_INCLUDEDIR})
    # PCRE_LIBRARIES is already set by pkg_check_modules
  endif()
endif()

if(NOT PCRE_FOUND)
  # Fallback to manual find_path/find_library for PCRE2
  find_path(PCRE_INCLUDE_DIR NAMES pcre2.h)
  find_library(PCRE_LIBRARY NAMES pcre2-8)
  
  if(PCRE_INCLUDE_DIR AND PCRE_LIBRARY)
    set(PCRE_FOUND TRUE)
    set(PCRE_LIBRARIES ${PCRE_LIBRARY})
    set(PCRE_INCLUDE_DIRS ${PCRE_INCLUDE_DIR})
  endif()
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(PCRE DEFAULT_MSG PCRE_LIBRARY PCRE_INCLUDE_DIR)

MARK_AS_ADVANCED(PCRE_INCLUDE_DIR PCRE_LIBRARY)