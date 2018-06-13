#! /usr/bin/env python3

# Copyright 2018 Red Book Connect LLC. operating as HotSchedules
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is a wrapper around the jdeps tool that ships with jdk 8 or later
# The simplest way to use it is to go to a directory with jar files in it and
# call the script passing in the name of one of the jar files. The script will
# return the jar files in the directory or the jre upon which the argument jar
# file depends.
#
# More than one jar file may be passed as an argument, in which case the each
# jar file on which at least one of the arguments depends will be returned, but
# each depended-upon jar file will only be listed once.

import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "target_jar",
    help="the jar whose dependencies you want",
    nargs="*")
parser.add_argument("-cp", "--classpath", default="*",
                    help="the classpath for jdeps to search for dependencies")
parser.add_argument("-f", "--file", help="the file containing the name(s) of\
 jar file(s) whose dependencies you want")

args = parser.parse_args()
if (not args.target_jar) and (not args.file):
    parser.print_help()
    sys.exit("at least one of target_jar and file must be specified")

jdeps_command = ["jdeps", "-cp", args.classpath, "-summary"]
# add jar names passed on command line
jdeps_command.extend(args.target_jar)
# add jar names from file
if args.file:
    with open(args.file, 'r') as file:
        file_contents = file.read()
        jar_file_names = file_contents.splitlines()
        jdeps_command.extend(jar_file_names)

jdeps_output = subprocess.check_output(jdeps_command)
lines = jdeps_output.decode("utf-8").splitlines()
depended_jars = [line.split(" -> ")[1] for line in lines]
unique_sorted_jars = sorted(set(depended_jars))
for jar in unique_sorted_jars:
    print(jar)
