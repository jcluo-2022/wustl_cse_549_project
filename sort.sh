#!/bin/bash  
    
perf stat -e cache-misses, L1-dcache-loads, L1-dcache-load-misses, L1-dcache-stores, L1-dcache-store-misses, L2-cache-loads, L2-cache-load-misses, L2-cache-stores, L2-cache-store-misses ./main.py >> result.txt  

