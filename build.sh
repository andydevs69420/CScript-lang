#!/bin/bash
python3 -m PyInstaller --onefile --paths="src/astnode:src/object:src/cscriptvm:lib/*." --specpath="build" --distpath="bin" src/cscript.py