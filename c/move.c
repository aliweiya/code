#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<dirent.h>
#include<fcntl.h>
#include<sys/sendfile.h>
#include<sys/stat.h> // fstat
#include<unistd.h>

void move_folder(char* old_folder, char* new_folder) {
    DIR *d;
    struct dirent *dir;
    char old_filename[100];
    char new_filename[100];
    d = opendir(old_folder);
    if (d) {
        while ((dir = readdir(d)) != NULL) {
            if (dir->d_type != DT_DIR) {
                memset(old_filename, 0, sizeof(old_filename));
                memset(new_filename, 0, sizeof(new_filename));
                strcat(old_filename, old_folder);
                strcat(old_filename, dir->d_name);
                strcat(new_filename, new_folder);
                strcat(new_filename, dir->d_name);
                if (access(new_filename, F_OK) == 0) {
                    // file exists
                    printf("%s exists\n", new_filename);
                    remove(old_filename);
                    continue;
                }

                printf("%s %s\n", old_filename, new_filename);
                int in = open(old_filename, O_RDONLY);
                int out = creat(new_filename, 0666);
                off_t bytesCopied = 0;
                struct stat fileinfo = {0};
                fstat(in, &fileinfo);
                int result = sendfile(out, in, &bytesCopied, fileinfo.st_size);

                close(in);
                close(out);
                remove(old_filename);
            }
        }
        closedir(d); 
    }
}

int main() {
    char*s = "ef";
    char *s_all = "0123456789abcdef";

    int len = strlen(s);
    int len_all = strlen(s_all);

    char old_path[100];
    char new_path[100];

    for (int i=0; i<len;i++) {
        for (int j=0;j<len_all;j++){
            for (int k=0;k<len_all;k++){
                memset(old_path, 0, sizeof(old_path));
                memset(new_path, 0, sizeof(new_path));
                sprintf(old_path, "/data1/rescan/r_%c/%c/%c/", s[i], s_all[j], s_all[k]);
                sprintf(new_path, "/data1/rescan/%c/%c/%c/", s[i], s_all[j], s_all[k]);
                printf("%s %s\n", old_path, new_path);
                move_folder(old_path, new_path);
            }
        }
    }
}
