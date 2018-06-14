# jdeps-wrapper

This is a wrapper around the jdeps tool that ships with jdk 8 or later.
The simplest way to use it is to go to a directory with jar files in it and
call the script passing in the name of one of the jar files. The script will
return the jar files in the directory or the jre upon which the argument jar
file depends.

More than one jar file may be passed as an argument, in which case the each
jar file on which at least one of the arguments depends will be returned, but
each depended-upon jar file will only be listed once.
