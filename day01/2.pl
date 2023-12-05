#!/usr/bin/perl

$sum = 0;

%forward_replacements = (
  one => 1,
  two => 2,
  three => 3,
  four => 4,
  five => 5,
  six => 6,
  seven => 7,
  eight => 8,
  nine => 9
);

%backward_replacements = (
  eno => 1,
  owt => 2,
  eerht => 3,
  ruof => 4,
  evif => 5,
  xis => 6,
  neves => 7,
  thgie => 8,
  enin => 9
);

$forward_replacement_keys = join("|", map {quotemeta} keys %forward_replacements);
$backward_replacement_keys = join("|", map {quotemeta} keys %backward_replacements);

# do one word/digit replacement from the front and back on separate strings
# because nineeighttworhtvxdtxp8twoneh should be 91
# and if using one string it would be 92
foreach (<STDIN>) {
  chomp;
  print("-----\n");

  # replace the first string number with its digit then throw out non-digits
  $forward = $_;
  print("$forward\n");
  $forward =~ s/($forward_replacement_keys)/$forward_replacements{$1}/;
  print("$forward\n");
  $forward =~ s/[a-z]//g;
  print("$forward\n");

  # reverse the string, replace the first backward string number with its 
  # digit then throw out non-digits
  $backward = reverse($_);
  print("$backward\n");
  $backward =~ s/($backward_replacement_keys)/$backward_replacements{$1}/;
  print("$backward\n");
  $backward =~ s/[a-z]//g;
  print("$backward\n");

  # first characters of forward/backward are the first/last digits
  $value = substr($forward, 0, 1) . substr($backward, 0, 1);
  print "$value\n";
  $sum += $value;
}

print $sum;