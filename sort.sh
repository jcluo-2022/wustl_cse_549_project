#!/bin/bash  
  
for((i=20;i<=24;i++));
do   
perf stat -e cache-misses ./sortCore.py --input_size $i  >> result.txt
done 
