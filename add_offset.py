#!/usr/bin/python

# SPDX-FileCopyrightText: 2021 Edward Ly <contact@edward.ly>
#
# SPDX-License-Identifier: MIT

"""
File: add_offset.py
Last Updated: 24 March 2021
Python script to add a timing offset to all .sm and .ssc files found in the
specified directory.

Usage: add_offset.py [-d|--dir <directory>] [-o|--offset <offset>]
"""

import os
import sys, getopt
import math
import time

def add_offset(filedata, offset_amount):
    prefix = "#OFFSET:"
    newdata = filedata
    start = newdata.find(prefix)
    if start == -1:
        # zero offset is implied, so add "#OFFSET:" to the file
        newdata += os.linesep + "#OFFSET:" + str(offset_amount) + ";" + os.linesep
    else:
        start += 8
        end = newdata.find(";", start)
        offset = newdata[start:end]
        new_offset = "{:.6f}".format(float(offset) + offset_amount)
        newdata = newdata.replace(prefix + offset, prefix + new_offset)
    return newdata

def modify_file(path, fun, offset_amount):
    with open(path, "r", encoding = "utf8", newline = "") as f:
        filedata = f.read()
    newdata = fun(filedata, offset_amount)
    with open(path, "w", encoding = "utf8", newline = "") as f:
        f.write(newdata)

def print_help():
    print("add_offset.py [-d|--dir <directory>] [-o|--offset <offset>]")
    print("")
    print("Adds a timing offset to all .sm and .ssc files in the specified directory by the given offset amount (in seconds).")
    print("Defaults to the current directory and +0.009 offset, respectively, if not provided.")

def print_success(time):
    print(f"Done in {time:0.4f} seconds.")

def main(argv):
    # Parse command line arguments
    offset_amount = 0.009
    directory = "."
    try:
        opts, args = getopt.getopt(argv, "hd:o:", ["help", "dir=", "offset="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-d", "--dir"):
            directory = arg
            if not os.path.isdir(directory):
                print("Error: directory does not exist.")
                sys.exit(3)
        elif opt in ("-o", "--offset"):
            try:
                offset_amount = float(arg)
            except ValueError:
                print("Error: offset is not a valid number.")
                sys.exit(4)

            if math.isinf(offset_amount):
                print("Error: offset is not a valid number (inf).")
                sys.exit(5)
            if math.isnan(offset_amount):
                print("Error: offset is not a valid number (NaN).")
                sys.exit(6)
            if offset_amount == 0: # Do nothing
                sys.exit()

    tic = time.perf_counter()

    # Find all .sm and .ssc files and modify their offsets
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".sm") or file.endswith(".ssc"):
                modify_file(os.path.join(root, file), add_offset, offset_amount)

    toc = time.perf_counter()
    print_success(toc - tic)

if __name__ == "__main__":
    main(sys.argv[1:])
