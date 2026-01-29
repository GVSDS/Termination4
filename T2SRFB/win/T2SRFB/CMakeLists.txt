add_executable(T2SRFB4 WIN32
  buildTime.cxx
  ControlPanel.cxx
  ManagedListener.cxx
  QueryConnectDialog.cxx
  STrayIcon.cxx
  VNCServerService.cxx
  VNCServerWin32.cxx
  T2SRFB.cxx
  T2SRFB.rc)

target_include_directories(T2SRFB4 PUBLIC ${CMAKE_BINARY_DIR}/win)
target_include_directories(T2SRFB4 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(T2SRFB4 rfb rfb_win32 network rdr ws2_32.lib)

install(TARGETS T2SRFB4
  RUNTIME DESTINATION ${CMAKE_INSTALL_FULL_BINDIR}
)
