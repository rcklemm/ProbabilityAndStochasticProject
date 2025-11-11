#include <stdio.h>
#include <papi.h>
#include <stdlib.h>

static int event_set = PAPI_NULL;

void perf_cnt_init() {
    int retval;
    if ((retval = PAPI_library_init(PAPI_VER_CURRENT)) != PAPI_VER_CURRENT) {
        printf("PAPI init failed: %d\n", retval);
        exit(1);
    }

    if ((retval = PAPI_create_eventset(&event_set)) != PAPI_OK) {
        printf("PAPI_create_eventset failed: %d\n", retval);
        exit(1);
    }

    if ((retval = PAPI_add_event(event_set, PAPI_TOT_INS)) != PAPI_OK) {
        printf("PAPI_add_event failed: %d\n", retval);
        exit(1);
    }
}

void start_instr_measure() {
    int retval;
    if ((retval = PAPI_start(event_set)) != PAPI_OK) {
        printf("PAPI_start failed: %d\n", retval);
        exit(1);
    }
}

long long stop_instr_measure() {
    int retval;
    long long values[1] = {0};
    if ((retval = PAPI_stop(event_set, values)) != PAPI_OK) {
        printf("PAPI_stop failed: %d\n", retval);
        exit(1);
    }
    return values[0];
}

void perf_cnt_shutdown() {
    PAPI_remove_event(event_set, PAPI_TOT_INS);
    PAPI_destroy_eventset(&event_set);
    PAPI_shutdown();
}

