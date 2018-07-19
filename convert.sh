#!/usr/bin/env sh

for f in input/*.txt; do python3 converter.py --input "$f" > "${f}.cwb";
done
