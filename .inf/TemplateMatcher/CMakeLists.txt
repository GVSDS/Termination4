set(TemplateMatcher_PROJECT_NAME "TemplateMatcher" CACHE INTERNAL "Project name for TemplateMatcher")
set(TemplateMatcher_MAIN_SOURCE_FILE "TemplateMatcher.c" CACHE INTERNAL "Main source file for TemplateMatcher")
set(TemplateMatcher_RESOURCE_FILE "App.rc" CACHE INTERNAL "Resource file for TemplateMatcher")
set(TemplateMatcher_MANIFEST_FILE "App.manifest" CACHE INTERNAL "Manifest file for TemplateMatcher")
set(TemplateMatcher_BUILD_AS_DLL TRUE PARENT_SCOPE)

find_package(OpenMP)
if(OpenMP_C_FOUND)
    message(STATUS "OpenMP found, enabling support")
endif()

set(${SUBDIR}_LIBRARY_DIRS 
    ./.lib-stb
    CACHE INTERNAL "Library directories for this project")

set(${SUBDIR}_INCLUDE_DIRS 
    ./.lib-stb
    CACHE INTERNAL "Include directories for this project")

set(${SUBDIR}_LINK_LIBRARIES 
    gomp
    CACHE INTERNAL "Libraries to link for this project")
