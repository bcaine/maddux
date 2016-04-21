#!/bin/sh

make clean
sphinx-apidoc -o ./source/ ./../../maddux/
make html
