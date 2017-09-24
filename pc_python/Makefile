#############################################################################
#
# Project Makefile
#
# (c) Wouter van Ooijen (www.voti.nl) 2016
#
# This file is in the public domain.
# 
#############################################################################

PROJECT := lemonator

# source files in this project (main.cpp is automatically assumed)
SOURCES := rs232.c

# header files in this project
HEADERS :=

# other places to look for files for this project
SEARCH  := 

# required for pybind11
CPP_RTTI          ?= -frtti 
CPP_EXCEPTIONS    ?= -fexceptions 
CPP_LANGUAGE      ?= -std=gnu++14

# set RELATIVE to the next higher directory and defer to the Makefile.due
RELATIVE := $(RELATIVE)../
include $(RELATIVE)Makefile.native
