project("cmake_project_structure")

# set source files
set(share1 share1.c)

# set make to a shared library
add_library(share1 SHARED ${share1})