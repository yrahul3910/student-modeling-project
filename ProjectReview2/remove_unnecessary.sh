#!/bin/sh
rm $(ls | egrep -v "*.tex|*.pdf|*.png|*.sh|*.cpp|check")
rm *.gz
