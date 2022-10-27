#!/bin/bash
python3 -m PyInstaller --onefile --paths="src/astnode:src/object:src/cscriptvm:lib:tests" src/cscript.py