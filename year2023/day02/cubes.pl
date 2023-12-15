#!/usr/bin/perl

# part 1
$sum_possible = 0;
$max_possible_red = 12;
$max_possible_green = 13;
$max_possible_blue = 14;

# part 2
$sum_power = 0;

foreach (<STDIN>) {
	chomp;
	$game_possible = 1;
	($game) = /^Game (\d+)/;
	print("game $game\n");
	@draws = split(/;/);

	$max_red = 0;
	$max_green = 0;
	$max_blue = 0;

	foreach $draw (@draws) {
		($red) = $draw =~ /(\d+) red/;
		($green) = $draw =~ /(\d+) green/;
		($blue) = $draw =~ /(\d+) blue/;
		print("r $red, g $green, b $blue\n");

		# part 1
		$game_possible = 0 if ($red > $max_possible_red || $green > $max_possible_green || $blue > $max_possible_blue);

		# part 2
		$max_red = $red if $red > $max_red;
		$max_green = $green if $green > $max_green;
		$max_blue = $blue if $blue > $max_blue;
	}

	$sum_possible += $game * $game_possible; # part 1
	$sum_power += $max_red * $max_green * $max_blue; # part 2
}

print "\n\npart 1: $sum_possible\npart 2: $sum_power\n";