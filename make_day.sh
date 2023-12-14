#!/bin/zsh

if [[ $# == 0 ]] 
then
  day=$( date +%d )
else
  day=$1
fi

mkdir "day$day"
cd "day$day"
touch readme.md
touch input.txt
touch sample.txt
echo "#!/usr/bin/env python" > 1.py