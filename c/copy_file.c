#define _CRT_SECURE_NO_WARNINGS

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define USAGE(prog_name) printf("usage: %s file_list source_path target_path\n", prog_name);

#define BUF_SIZE 1000

#ifdef _WIN32
#define PATH_SEP "\\"
#else
#define PATH_SEP "/"
#endif


int copy_file(const char* source, const char* target) {
    FILE* frout = fopen(target, "rb");
    if (frout != NULL) {
        printf("%s exists\n", target);
        fclose(frout);
        return EXIT_SUCCESS;
    }

    FILE* fin = fopen(source, "rb");

    if (fin == NULL) {
        perror(source);
        return EXIT_FAILURE;
    }

    FILE* fout = fopen(target, "wb");

    if (fout == NULL) {
        perror(target);
        fclose(fin);
        return EXIT_FAILURE;
    }

    int ret;
    char buff[BUF_SIZE];
    while (!feof(fin))
    {
        /* 从源文件中读取内容 */
        ret = fread(buff, 1, BUF_SIZE, fin);

        /* 把从源文件读取到的容写入到目标文件中 */
        fwrite(buff, ret, 1, fout);
    }

    fclose(fin);
    fclose(fout);

    return EXIT_SUCCESS;
}


int main(int argc, char* argv[]) {
    if (argc < 3) {
        USAGE(argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE* fp = fopen(argv[1], "r");

    if (fp == NULL)
    {
        // 把一个描述性错误消息输出到标准错误 stderr。首先输出字符串 str，后跟一个冒号，然后是一个空格。
        perror(argv[1]);
        exit(EXIT_FAILURE);
    }

    char line[BUF_SIZE];
    char source[BUF_SIZE];
    char target[BUF_SIZE];

    int return_code = EXIT_SUCCESS;

    while (!feof(fp)) {
        memset(source, 0, sizeof(source));
        memset(target, 0, sizeof(target));

        strcpy(source, argv[2]);
        strcpy(target, argv[3]);

        if (source + strlen(source) - 1 != PATH_SEP)
            strcat(source, PATH_SEP);

        if (target + strlen(target) - 1 != PATH_SEP)
            strcat(target, PATH_SEP);

        fgets(line, BUF_SIZE, fp);
        // 检索字符串 str1 开头连续有几个字符都不含字符串 str2 中的字符。
        // 此处用于去掉最后一个换行
        line[strcspn(line, "\n")] = 0;

        memcpy(source + strlen(source), line, 2);
        strcat(source, PATH_SEP);
        memcpy(source + strlen(source), line+2, 2);
        strcat(source, PATH_SEP);
        strcat(source, line);

        strcat(target, line);

        printf("%s, %s\n", source, target);

        if (copy_file(source, target) != 0) {
            return_code = EXIT_FAILURE;
            break;
        }
            
    }
    fclose(fp);
    return return_code;
}