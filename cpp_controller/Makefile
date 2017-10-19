#############################################################################
#
# Project Makefile
#
# (c) Wouter van Ooijen (www.voti.nl) 2016
#
# This file is in the public domain.
#
#############################################################################

PROJECT := cpp/main
# source files in this project (main.cpp is automatically assumed)
SOURCES := rs232.c cpp/lemonator_controller.cpp
# header files in this project
HEADERS := cpp/lemonator_controller.hpp cpp/simulator_lemonator_proxy.hpp

# other places to look for files for this project
SEARCH  :=

EXE 	:= lemonator.exe

# set RELATIVE to the next higher directory and defer to the Makefile.due
RELATIVE := $(RELATIVE)../
include $(RELATIVE)Makefile.native
