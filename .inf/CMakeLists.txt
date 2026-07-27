cmake_minimum_required(VERSION 3.15)

# 项目根目录
project(InfProjects C)

# 设置默认构建类型（可选）
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

# 手动指定项目文件夹列表（根据需要修改）
set(PROJECT_DIRECTORIES
    Install
    RegistryOverride
    Service
    # SubstituteExecution
    TemplateMatcher
    Test
    Tools
    Update
)

# 设置输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.static")

# 全局编译选项
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)
set(CMAKE_C_FLAGS_RELEASE "-O2 -s -fno-stack-protector -fno-PIC")

# 遍历所有子目录
foreach(SUBDIR ${PROJECT_DIRECTORIES})
    message(STATUS "Processing directory: ${SUBDIR}")
    
    # 检查目录是否存在
    if(NOT IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${SUBDIR})
        message(WARNING "Directory ${SUBDIR} does not exist - skipping")
        continue()
    endif()
    
    # 检查子目录是否有 CMakeLists.txt
    if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${SUBDIR}/CMakeLists.txt)
        message(WARNING "No CMakeLists.txt in ${SUBDIR} - skipping")
        continue()
    endif()
    
    message(STATUS "Found valid project directory: ${SUBDIR}")
    
    # 清除可能存在的旧缓存变量
    unset(${SUBDIR}_PROJECT_NAME CACHE)
    unset(${SUBDIR}_MAIN_SOURCE_FILE CACHE)
    unset(${SUBDIR}_RESOURCE_FILE CACHE)
    unset(${SUBDIR}_MANIFEST_FILE CACHE)
    unset(${SUBDIR}_BUILD_AS_DLL CACHE)
    unset(${SUBDIR}_LIBRARY_DIRS CACHE)  # 库目录变量
    unset(${SUBDIR}_INCLUDE_DIRS CACHE)  # 头文件目录变量
    unset(${SUBDIR}_LINK_LIBRARIES CACHE) # 链接库变量
    
    # 进入子目录，让其定义缓存变量
    add_subdirectory(${SUBDIR})
    
    # 重命名缓存变量，添加子目录前缀以避免冲突
    set(PROJECT_NAME "${${SUBDIR}_PROJECT_NAME}")
    set(MAIN_SOURCE_FILE "${${SUBDIR}_MAIN_SOURCE_FILE}")
    set(RESOURCE_FILE "${${SUBDIR}_RESOURCE_FILE}")
    set(MANIFEST_FILE "${${SUBDIR}_MANIFEST_FILE}")
    set(BUILD_AS_DLL "${${SUBDIR}_BUILD_AS_DLL}")
    set(LIBRARY_DIRS "${${SUBDIR}_LIBRARY_DIRS}")  # 获取子项目指定的库目录
    set(INCLUDE_DIRS "${${SUBDIR}_INCLUDE_DIRS}")  # 获取子项目指定的头文件目录
    set(LINK_LIBRARIES "${${SUBDIR}_LINK_LIBRARIES}") # 获取子项目需要链接的库
    
    # 验证必要变量是否定义
    set(REQUIRED_VARS PROJECT_NAME MAIN_SOURCE_FILE)
    set(MISSING_VARS "")
    
    foreach(VAR ${REQUIRED_VARS})
        if(NOT DEFINED ${VAR} OR "${${VAR}}" STREQUAL "")
            list(APPEND MISSING_VARS ${VAR})
        endif()
    endforeach()
    
    if(MISSING_VARS)
        message(WARNING "Missing required variables in ${SUBDIR}: ${MISSING_VARS} - skipping project")
        continue()
    endif()
    
    # 检查主源文件是否存在
    set(MAIN_FILE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/${SUBDIR}/${MAIN_SOURCE_FILE}")
    if(NOT EXISTS ${MAIN_FILE_PATH})
        message(WARNING "Main source file ${MAIN_SOURCE_FILE} not found in ${SUBDIR} (looked for: ${MAIN_FILE_PATH}) - skipping project")
        continue()
    endif()
    
    # 收集源文件
    set(SOURCES "${SUBDIR}/${MAIN_SOURCE_FILE}")
    
    # 处理资源文件（如果定义且存在）
    if(NOT "${RESOURCE_FILE}" STREQUAL "" AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${SUBDIR}/${RESOURCE_FILE}")
        list(APPEND SOURCES "${SUBDIR}/${RESOURCE_FILE}")
        message(STATUS "Added resource file for ${PROJECT_NAME}")
    endif()
    
    # 处理清单文件（如果定义且存在）
    set(MANIFEST_PATH "")
    if(NOT "${MANIFEST_FILE}" STREQUAL "" AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${SUBDIR}/${MANIFEST_FILE}")
        set(MANIFEST_PATH "${SUBDIR}/${MANIFEST_FILE}")
        list(APPEND SOURCES ${MANIFEST_PATH})
        message(STATUS "Added manifest file for ${PROJECT_NAME}")
    endif()
    
    # 判断是构建 DLL 还是 EXE
    if(BUILD_AS_DLL)
        message(STATUS "Building ${PROJECT_NAME} as DLL")
        add_library(${PROJECT_NAME} SHARED ${SOURCES})

        set_target_properties(${PROJECT_NAME} PROPERTIES
            ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.static"
            LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.lib"
            RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.lib"
        )

        if(WIN32)
            target_compile_definitions(${PROJECT_NAME} PRIVATE
                ${PROJECT_NAME}_EXPORTS
            )
        endif()
    else()
        message(STATUS "Building ${PROJECT_NAME} as EXE")
        add_executable(${PROJECT_NAME} ${SOURCES})
    endif()
    
    # 设置清单文件（如果存在）
    if(NOT "${MANIFEST_PATH}" STREQUAL "" AND MSVC)
        set_property(TARGET ${PROJECT_NAME} APPEND PROPERTY LINK_FLAGS 
            "/MANIFEST:EMBED /MANIFESTINPUT:${MANIFEST_PATH}")
    endif()
    
    # 添加子项目指定的库目录和头文件目录
    if(LIBRARY_DIRS)
        message(STATUS "Adding library directories for ${PROJECT_NAME}: ${LIBRARY_DIRS}")
        target_link_directories(${PROJECT_NAME} PRIVATE ${LIBRARY_DIRS})
    endif()
    
    if(INCLUDE_DIRS)
        message(STATUS "Adding include directories for ${PROJECT_NAME}: ${INCLUDE_DIRS}")
        target_include_directories(${PROJECT_NAME} PRIVATE ${INCLUDE_DIRS})
    endif()
    
    # 链接库 - 先链接全局库，再链接子项目指定的库
    target_link_libraries(${PROJECT_NAME}
        advapi32
        user32
        wtsapi32
        userenv
        psapi
        shell32
        kernel32
        gdi32
        netapi32
        ${LINK_LIBRARIES}
    )

    # 添加默认链接目录
    target_link_directories(${PROJECT_NAME} PRIVATE
        ./.Link
    )

    # 添加默认头文件目录
    target_include_directories(${PROJECT_NAME} PRIVATE
        ./.Link
    )

    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        "$<TARGET_FILE:${PROJECT_NAME}>"
        "${CMAKE_BINARY_DIR}/.dat/${PROJECT_NAME}$<$<BOOL:${BUILD_AS_DLL}>:.dll>.dat"
        COMMENT "Copying $<TARGET_FILE_NAME:${PROJECT_NAME}> to ${PROJECT_NAME}$<$<BOOL:${BUILD_AS_DLL}>:.dll>.dat"
    )
    
    message(STATUS "Successfully configured project: ${PROJECT_NAME}")
    
    # 清除变量，避免影响其他项目
    unset(PROJECT_NAME)
    unset(MAIN_SOURCE_FILE)
    unset(RESOURCE_FILE)
    unset(MANIFEST_FILE)
    unset(BUILD_AS_DLL)
    unset(LIBRARY_DIRS)
    unset(INCLUDE_DIRS)
    unset(LINK_LIBRARIES)
endforeach()

add_custom_target(clean-all
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_BINARY_DIR}/.bin"
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_BINARY_DIR}/.lib"
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_BINARY_DIR}/.dat"
    COMMAND ${CMAKE_COMMAND} -E remove "${CMAKE_BINARY_DIR}/CMakeCache.txt"
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_BINARY_DIR}/CMakeFiles"
    COMMENT "Cleaning all build outputs and cache..."
)
