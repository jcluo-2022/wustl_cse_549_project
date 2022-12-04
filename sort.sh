#!/bin/bash  
  
for((i=20;i<=24;i++));
do   
perf stat -e cache-misses ./412.py --input_size $i  >> result.txt  
done 
