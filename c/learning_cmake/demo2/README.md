aux_source_directory 命令会查找指定目录下的所有源文件，然后将结果存进指定变量名。

```cmake
cmake_minimum_required(VERSION 2.8)

project (Demo2)

aux_source_directory(. DIR_SRCS)

add_executable(Demo ${DIR_SRCS})
```

Make 会将当前目录所有源文件的文件名赋值给变量 DIR_SRCS ，再指示变量 DIR_SRCS 中的源文件需要编译成一个名称为 Demo 的可执行文件。