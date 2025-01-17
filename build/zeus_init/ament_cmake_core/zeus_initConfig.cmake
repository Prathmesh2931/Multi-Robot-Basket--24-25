# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_zeus_init_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED zeus_init_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(zeus_init_FOUND FALSE)
  elseif(NOT zeus_init_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(zeus_init_FOUND FALSE)
  endif()
  return()
endif()
set(_zeus_init_CONFIG_INCLUDED TRUE)

# output package information
if(NOT zeus_init_FIND_QUIETLY)
  message(STATUS "Found zeus_init: 0.0.0 (${zeus_init_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'zeus_init' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${zeus_init_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(zeus_init_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${zeus_init_DIR}/${_extra}")
endforeach()
