#!/bin/bash

for i in {20..24}
do
	sudo taskset --cpu-list 0-7 perf stat -e l1d.replacement -e l2_lines_out.non_silent python3 parallel_main.py ${i}
done

