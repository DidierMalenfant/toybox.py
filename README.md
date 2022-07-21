# toybox.py

A dependency management system for Lua on the [Playdate](https://play.date).

This is an experimental Python implementation of [toybox](https://github.com/jm/toybox) by Jeremy McAnally.

TODO:

* Resolve version numbers correctly (>=, <=, etc...)
* Connect Lua code by generating toyboxes.lua.
* Connect C code by generating toyboxes.mk and toyboxes.h.
* Setup basic Makefile project if none is present.
* Make info command point out when dependencies have not been installed.
* Copy any Luacheck std if it's present in a toybox.
* Add support for git submodules instead of cloning.
* Add unit tests.
* Implement update single dependency command.
* Documentation.
* Make it available on pip.
* Set up a toybox registery (toystore?) on Github to refer to dependencies with a single name (i.e. pdutility).

* * *

Copyright (c) 2022 Didier Malenfant.
