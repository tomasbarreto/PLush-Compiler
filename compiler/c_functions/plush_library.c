#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_int(int x);

void print_int(int x) {
    printf("%d\n", x);
}

void print_string(char* s) {
    printf("%s\n", s);
}

void print_float(float x) {
    printf("%f\n", x);
}

void print_char(char x) {
    printf("%c\n", x);
}

int* get_array(int nr_positions) {
    int* ptr = (int*) malloc(nr_positions * sizeof(int));
    for (int i = 0; i < nr_positions; i++) {
        ptr[i] = i;
    }
    return ptr;
}

int** get_array2d(int dim1, int dim2) {
    int** ptr = (int**) malloc(dim1 * sizeof(int*));
    for (int i = 0; i < dim1; i++) {
        ptr[i] = (int*) malloc(dim2 * sizeof(int));
        for (int j = 0; j < dim2; j++) {
            ptr[i][j] = 1;
        }
    }
    return ptr;
}

char* concat_strings(const char* str1, const char* str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t totalLength = len1 + len2 + 1;

    char* result = (char*)malloc(totalLength * sizeof(char));
    if (result == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    strcpy(result, str1);
    strcat(result, str2);

    return result;
}

char* get_array2d_char(int nr_positions) {
    char* ptr = (char*) malloc(nr_positions * sizeof(char));
    for (int i = 0; i < nr_positions; i++) {
        ptr[i] = 'a';
    }
    return ptr;
}