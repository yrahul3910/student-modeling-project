#!/bin/sh
rm $(ls | egrep -v "*.tex|*.pdf|*.png|*.sh")
rm *.gz
