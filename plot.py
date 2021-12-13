#!/usr/bin/env python3

###################################################################################################
#
# The following script plots logged CPU and memory usage of a command line program.
#
# Usage:
#
# >>> log_performance.py [log-file]
#
# >>> log_performance.py [log-file] [other-log-file]
#
###################################################################################################

import os, sys
import matplotlib.pyplot as plt
import numpy as np


def get_data(logfile):

    data = open(logfile, "r").readlines()[1:]
    data = [datum.strip().split() for datum in data]
    time = np.array([datum[0] for datum in data]).astype(np.float64)
    mem = np.array([datum[1] for datum in data]).astype(np.float64)
    cpu = np.array([datum[2] for datum in data]).astype(np.float64) / 100.0
    del data
    
    return time, mem, cpu


def plot_single(logfile):

    time1, mem1, cpu1 = get_data(logfile)

    fig, axs = plt.subplots(2, 1, figsize=(8,6), sharex=True)

    #fig.suptitle("Psi4 Performance Benchmarking\n" + "DLPNO-MP2/aTZ, C$_{60}$H$_{122}$, 200GB/18c")

    axs[0].plot(time1, mem1, color="xkcd:blue")
    axs[0].set_xlabel("Time Elapsed (s)")
    axs[0].set_ylabel("Memory Usage (GB)")
    axs[0].set_xlim(0.0, time1[-1])
    axs[0].set_ylim(bottom=0)
    
    axs[1].plot(time1, cpu1, color="xkcd:blue")
    axs[1].set_xlabel("Time Elapsed (s)")
    axs[1].set_ylabel("Processor Usage")
    axs[1].set_xlim(0.0, time1[-1])
    axs[1].set_ylim(bottom=0, top = round(np.max(cpu1)) + 1)

    fig.tight_layout()
    plt.savefig(f"performance.pdf", transparent=True)
    plt.show()

def plot_comparison(logfile1, logfile2):

    time1, mem1, cpu1 = get_data(logfile1)
    time2, mem2, cpu2 = get_data(logfile2)

    time1 = 100.0 * (time1 / np.max(time1))
    time2 = 100.0 * (time2 / np.max(time2))

    fig, axs = plt.subplots(2, 1)

    axs[0].plot(time1, mem1, color="xkcd:blue", label=logfile1)
    axs[0].plot(time2, mem2, color="xkcd:red", label=logfile2)
    axs[0].set_xlabel("Time Elapsed (%)")
    axs[0].set_ylabel("Memory Usage (GB)")
    axs[0].set_xlim(0.0, time1[-1])
    axs[0].set_ylim(bottom=0)
    
    axs[1].plot(time1, cpu1, color="xkcd:blue")
    axs[1].plot(time2, cpu2, color="xkcd:red")
    axs[1].set_xlabel("Time Elapsed (%)")
    axs[1].set_ylabel("Processor Usage")
    axs[1].set_xlim(0.0, time1[-1])
    axs[1].set_ylim(bottom=0, top = round(max(np.max(cpu1), np.max(cpu2))) + 1)

    axs[0].legend()

    fig.tight_layout()
    plt.savefig(f"performance_compare.pdf", transparent=True)
    plt.show()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        logfile = sys.argv[1]
        plot_single(logfile)
    elif len(sys.argv) == 3:
        logfile1 = sys.argv[1]
        logfile2 = sys.argv[2]
        plot_comparison(logfile1, logfile2)
    else:
        print("Expected 2 or 3 arguments")
