#include "util.h"
#include <time.h>

int* read_list(const char* filename, int *outsz) {
    FILE *list_file = fopen(filename, "r");
    int retval;

    int num_entries;    
    if ((retval = fscanf(list_file, "%d", &num_entries)) != 1) {
        printf("File parsing failed!\n");
        exit(1);
    }
    *outsz = num_entries;

    int* arr = malloc(sizeof(int)*num_entries);
    for (int i = 0; i < num_entries; i++) {
        if ((retval = fscanf(list_file, "%d", &arr[i])) != 1) {
            printf("File parsing failed!\n");
        }
    }
    fclose(list_file);

    return arr;
}

void dump_list(const char* filename, int *arr, int size) {
    FILE *list_file = fopen(filename, "w");
    
    fprintf(list_file, "%d\n", size);

    for (int i = 0; i < size; i++) {
        fprintf(list_file, "%d ", arr[i]);
    }

    fclose(list_file);
    
    return;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;

    return;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[low];
    int i = low;
    int j = high;
    
    while (i < j) {
        while (arr[i] <= pivot && i <= high - 1) i++;

        while (arr[j] > pivot && j >= low + 1) j--;

        if (i < j) swap(&arr[i], &arr[j]);
    }
    
    swap(&arr[low], &arr[j]);

    return j;
}

void quick_sort(int arr[], int low, int high, int depth) {
    if (low < high) {
        start_instr_measure();
        int pi = partition(arr, low, high);
        long long inst_count = stop_instr_measure();        
        printf("%d depth: low=%d, high=%d, partition instructions=%lld\n", depth, low, high, inst_count);
    
        quick_sort(arr, low, pi - 1, depth + 1);
        quick_sort(arr, pi + 1, high, depth + 1);
    }
}

void print_arr(const char* msg, int arr[], size_t len) {
    printf("%s: ", msg);
    printf("[");
    for (size_t i = 0; i < len; i++) {
        printf("%d", arr[i]);
        if (i != len - 1) {
            printf(", ");
        }
    }
    printf("]\n");
}

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("USAGE: %s <infile> <outfile>\n", argv[0]);
        return 1;
    }

    perf_cnt_init();
    
    srand(time(NULL));

    int arrsz;
    int *to_sort = read_list(argv[1], &arrsz);
    //print_arr("ORIGINAL ARRAY", to_sort, arrsz);

    quick_sort(to_sort, 0, arrsz - 1, 0);    
    
    dump_list(argv[2], to_sort, arrsz);
    //print_arr("SORTED ARRAY", to_sort, arrsz);
    
    free(to_sort);
    perf_cnt_shutdown();

    return 0;
}

