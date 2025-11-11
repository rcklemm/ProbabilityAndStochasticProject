#include "util.h"

int main() {
    perf_cnt_init();
    
    start_instr_measure();
    // ---- measure ----
    for (volatile int i = 0; i < 100000; i++);
    // -----------------
    long long inst_count = stop_instr_measure();
    printf("1 Executed: %lld instructions\n", inst_count);
    

    start_instr_measure();
    for (volatile int i = 0; i < 10000; i++);
    inst_count = stop_instr_measure();
    printf("2 Executed: %lld instructions\n", inst_count);

    return 0;
}

