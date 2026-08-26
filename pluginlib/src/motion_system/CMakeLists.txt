cmake_minimum_required(VERSION 3.8)
project(motion_system)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(pluginlib REQUIRED)

add_executable(test_plugin src/test_plugin.cpp)
target_include_directories(test_plugin PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(test_plugin pluginlib)
install(TARGETS test_plugin
DESTINATION lib/${PROJECT_NAME})

# 构建插件共享库（库名需与 spin_motion_plugins.xml 的 <library path> 一致）
add_library(spin_motion_control SHARED
  src/spin_motion_control.cpp
)
target_include_directories(spin_motion_control PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(spin_motion_control pluginlib)

# 导出插件描述文件到 ament index
pluginlib_export_plugin_description_file(motion_system spin_motion_plugins.xml)

# 安装
install(TARGETS spin_motion_control
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

ament_export_include_directories(include)
ament_export_libraries(spin_motion_control)
ament_export_dependencies(pluginlib)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
