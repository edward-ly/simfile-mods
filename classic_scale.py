#!/usr/bin/python

"""
File: classic_scale.py
Author: Edward Ly (@_led_light)
Last Updated: 24 March 2021
Python script to (lazily) convert X-scale ratings to old-scale ratings for all
simfiles found in the current directory.

Usage: classic_scale.py [-d|--dir <directory>]

MIT License

Copyright (c) 2021 Edward Ly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys, getopt
import time

old_scale = ["0", "1", "1", "2", "3", "3", "4", "5", "5", "6", "7", "7", "8", "9", "9", "10", "10", "11", "12", "13", "14"]

def classic_scale_ini(filedata):
    newdata = filedata
    for i, line in enumerate(newdata):
        if newdata[i].find("#METERTYPE:DDR X;") != -1:
            newdata[i] = newdata[i].replace("#METERTYPE:DDR X;", "#METERTYPE:DDR;")
            break
    return newdata

def classic_scale_sm(filedata):
    prefix = "#NOTES:" # ratings are 4 lines down from every "#NOTES:"
    newdata = filedata
    for i, line in enumerate(newdata):
        start = newdata[i - 4].find(prefix)
        if start != -1:
            start += 5
            end = line.find(":", start)
            meter = line[start:end]
            new_meter = old_scale[int(meter)]
            newdata[i] = newdata[i].replace(meter, new_meter)
    return newdata

def classic_scale_ssc(filedata):
    prefix = "#METER:"
    newdata = filedata
    for i, line in enumerate(newdata):
        start = line.find(prefix)
        if start != -1:
            start += 7
            end = line.find(";", start)
            meter = line[start:end]
            new_meter = old_scale[int(meter)]
            newdata[i] = newdata[i].replace(meter, new_meter)
    return newdata

def modify_file(path, fun):
    with open(path, "r", encoding = "utf8", newline = "") as f:
        filedata = f.readlines()
    newdata = fun(filedata)
    with open(path, "w", encoding = "utf8", newline = "") as f:
        f.writelines(newdata)

def print_help():
    print("classic_scale.py [-d|--dir <directory>]")
    print("")
    print("Applies a simple X-scale to old-scale rating conversion to all .sm and .ssc files found in the specified directory.")
    print("Also changes the #METERTYPE value to \"DDR\" for all group.ini files found.")
    print("Defaults to the current directory if not provided.")

def print_success(time):
    print(f"Done in {time:0.3f} seconds.")
    print("")
    print("Note: the new ratings may not be completely accurate, so please make any additional adjustments yourself!")

def main(argv):
    # Parse command line arguments
    directory = "."
    try:
        opts, args = getopt.getopt(argv, "hd:", ["help", "dir="])
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

    tic = time.perf_counter()

    # Find all .sm/.ssc/.ini files and modify their ratings
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("group.ini"):
                modify_file(os.path.join(root, file), classic_scale_ini)
            if file.endswith(".sm"):
                modify_file(os.path.join(root, file), classic_scale_sm)
            if file.endswith(".ssc"):
                modify_file(os.path.join(root, file), classic_scale_ssc)

    toc = time.perf_counter()
    print_success(toc - tic)

if __name__ == "__main__":
    main(sys.argv[1:])
