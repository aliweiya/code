project("cmake_project_structure")

# set source files
set(share2 share2.c)

# set make to a shared library
add_library(share2 SHARED ${share2})

# link share1
target_link_libraries(share2 share1)