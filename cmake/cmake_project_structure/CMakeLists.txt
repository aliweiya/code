# 最低版本要求，必须
cmake_minimum_required(VERSION 3.0)

# 工程名称
project("cmake_project_structure")

add_compile_options(-std=c99)

# 添加include目录
include_directories(${PROJECT_SOURCE_DIR}/include)

# 添加链接库查找目录，库查找序按照参数顺序从向右查
link_directories(${PROJECT_BINARY_DIR}/libs /usr.local/libs /usr/lib)

# 设置可执行文件目录，同样设成和库目录相同
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/out)

# 添加子目录（每个子目录下都必须有自已的CMakeLists.txt文件
add_subdirectory(share1)
add_subdirectory(share2)
add_subdirectory(test)