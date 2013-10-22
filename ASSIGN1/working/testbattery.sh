#!/bin/bash

for f in $tests;
do
    python program.py $f
done

mv RushHour/*.s* RushHour/finalA/

for f in $tests;
do
    python program.py $f -s
done

mv RushHour/*.s* RushHour/finalBFS/
