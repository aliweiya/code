cmake_minimum_required(VERSION 2.8)

project(Demo3)

aux_source_directory(. DIR_SRCS)

# 指明本项目包含一个子目录 math，这样 math 目录下的 CMakeLists.txt 文件和源代码也会被处理 。
add_subdirectory(math)

add_executable(Demo main.cc)

# 指明可执行文件 Demo 需要连接一个名为 MathFunctions 的链接库 。
target_link_libraries(Demo MathFunctions)