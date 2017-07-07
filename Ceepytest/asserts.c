#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int assert_true(int expr) {
    if (expr)
        return 0;
    return -1;
}

int assert_str_eq(char* lh, char* rh) {
    return strcmp(lh, rh);
}

int test_failed(char* msg) {
    printf("    Sub-test failed with message:\n        %s\n", msg);
    return 1;
}

int test_passed(char* msg) {
    printf("    Sub-test passed with message:\n        %s\n", msg);
    return 0;
}