import os
import subprocess


# this function return the cpu_num, the current process is running on
def get_cpu():
    pid = os.getpid()
    result = subprocess.getoutput(f"sudo ps -o psr -p {pid}")
    return int(result.split('\n')[1])
