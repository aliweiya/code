#include <stdio.h>
#include <stdlib.h>

#include "../include/share1.h"

int test(int a) {
    for (int i=0; i<a; i++) {
        printf("add(%d+%d)=%d\n", i, i, add(i, i));
    }
    return 0;
}