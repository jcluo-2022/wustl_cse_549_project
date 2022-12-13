#!/bin/bash
for core in 2 4 8
do
let process=core+core
for i in {20..24}
  do
    sudo perf stat -e l1d.replacement -e l2_lines_out.non_silent python3 ./parallel_merge.py --core ${core} --process ${process} --size ${i}
  done
done
