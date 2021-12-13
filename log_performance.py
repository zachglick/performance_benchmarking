#!/usr/bin/env python3

###################################################################################################
#
# The following script monitors the CPU and memory usage of a terminal command by scraping `top`
#
# Usage:
#
# >>> log_performance.py [log-file-to-be-created] [command-line-arguments-to-be-run]
#
# For example:
#
# >>> log_performance.py 18c_log.txt psi4 -n18 input.dat -o 18c.out
#
###################################################################################################

import os
import sys
import subprocess
import time


# the name of the log file to be created
logfile = sys.argv[1]

# the command (potentially with additional arguments) to profile
program_args = sys.argv[2:]

# run the user-supplied command
process = subprocess.Popen(program_args)
pid = process.pid

tstart = time.time()

with open(logfile, "w") as fp:

    fp.write(f"Elapsed Time (s)   Physical Memory (GB)   CPU Usage (%)\n")

    while process.poll() is None:

        t_elapsed = time.time() - tstart

        # explanation for the top command:
        # -b          : batch mode, gets us plain text output
        # -p {pid}    : get info for only our process
        # -n1         : run a single frame
        top_process = subprocess.run(["top", "-b", "-p", str(pid), "-n1"], capture_output=True)
        top_output = top_process.stdout.decode("utf-8").strip()
        top_output = top_output.split("\n")[-1]
        top_data = top_output.strip().split()
        mem = top_data[5]

        # units
        if mem.endswith("g"):
            mem = mem[:-1]
        elif mem.endswith("m"):
            mem = float(mem[:-1]) / (1000.0)
            mem = str(round(mem, 1))
        else:
            mem = float(mem) / (1000.0 ** 2)
            mem = str(round(mem, 1))

        cpu = top_data[8]
        fp.write(f"{t_elapsed:16.1f}   {mem:>20s} {cpu:>15s}\n")
        fp.flush()
        time.sleep(1)
