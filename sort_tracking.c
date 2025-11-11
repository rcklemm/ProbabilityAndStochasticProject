#include <stdio.h>
#include <papi.h>

int main() {
    int retval;
    int EventSet = PAPI_NULL;
    long long values[1];

    if ((retval = PAPI_library_init(PAPI_VER_CURRENT)) != PAPI_VER_CURRENT) {
        printf("PAPI init error: %d\n", retval);
        return 1;
    }

    if ((retval = PAPI_create_eventset(&EventSet)) != PAPI_OK) {
        printf("PAPI_create_eventset failed: %d\n", retval);
        return 1;
    }

    if ((retval = PAPI_add_event(EventSet, PAPI_TOT_INS)) != PAPI_OK) {
        printf("PAPI_add_event failed: %d\n", retval);
        return 1;
    }

    if ((retval = PAPI_start(EventSet)) != PAPI_OK) {
        printf("PAPI_start failed: %d\n", retval);
        return 1;
    }

    // ---- measure ----
    for (volatile int i = 0; i < 100000; i++);
    // -----------------

    if ((retval = PAPI_stop(EventSet, values)) != PAPI_OK) {
        printf("PAPI_stop failed: %d\n", retval);
        return 1;
    }

    printf("Executed: %lld instructions\n", values[0]);

    PAPI_remove_event(EventSet, PAPI_TOT_INS);
    PAPI_destroy_eventset(&EventSet);
    PAPI_shutdown();

    return 0;
}

