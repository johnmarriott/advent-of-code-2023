#!/usr/bin/perl

$sum = 0;

foreach (<STDIN>) {
  chomp;
  s/[a-z]//g;
  $sum += substr($_, 0, 1) . chop;
}

print $sum;