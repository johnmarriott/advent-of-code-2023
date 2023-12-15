#!/usr/bin/perl
use Data::Dumper;

$have_directions = 0;
%nodes;
@starting_nodes; # nodes that end in A
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

	push(@starting_nodes, $key) if $key =~ /A$/;
}

# instead of running each path at the same time, run
# each separately and find the lcm of them
@node_steps;
foreach $starting_node (@starting_nodes) {
	$step = 0;
	$node = $starting_node;
	until ($node =~ /Z$/) {
		$direction = $directions[$step++ % scalar(@directions)];
		#print(Dumper($nodes{$node}));
		#print("step $step at $node, going $direction");
		$node = $nodes{$node}{$direction};
		#print(" to $node\n");
	}
	print("$starting_node -> $node in $step steps\n");

	push(@node_steps, $step);
}

$starting_node_steps = join(", ", @node_steps);

# the LCM is only a solution because of the given data.  If there were a case
# like path 1 can go from A to Z in 5 steps and Z to Z in 2 steps and path
# 2 can go from A to Z in 7 steps, then the answer is 7 but the LCM of A to Z
# steps is 35
system("python -c 'import math; print(math.lcm($starting_node_steps))'")
