#!/bin/bash

for i in {20..24}
do
	sudo taskset -c 0,1 perf stat -e l1d.replacement -e l2_lines_out.non_silent python3 parallel_main.py ${i}
done

