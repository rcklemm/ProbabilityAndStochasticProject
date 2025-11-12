all: sort_tracking.c util.h
	gcc sort_tracking.c -g -Wall -Wextra -o sort_tracking_O0 -O0 -lpapi
	gcc sort_tracking.c -Wall -Wextra -o sort_tracking_O1 -O1 -lpapi
	gcc sort_tracking.c -Wall -Wextra -o sort_tracking_O2 -O2 -lpapi
	gcc sort_tracking.c -Wall -Wextra -o sort_tracking_O3 -O3 -lpapi

clean:
	rm -f sort_tracking_O0 sort_tracking_O1 sort_tracking_O2 sort_tracking_O3

