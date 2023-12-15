#!/usr/bin/perl
use Data::Dumper;

$have_directions = 0;
%nodes;
foreach (<STDIN>) {
	chomp;

	next unless m/\w/; # skip blank lines

	# first text line is directions
	unless ($have_directions) {
		@directions = split(//);
		$have_directions = 1;
		next;
	}

	# if here then it's a node
	($key) = $_ =~ /^(\w+)/;
	($left) = $_ =~ /(\w+),/;
	($right) = $_ =~ /, (\w+)/;

	$nodes{$key} = { "L" => $left, "R" => $right };
}

# print(Dumper(\%nodes));

$step = 0;
$node = "AAA";
$node = $nodes{$node}{$directions[$step++ % scalar(@directions)]} until ($node eq "ZZZ");

print($step);