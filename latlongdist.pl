#!/usr/bin/env perl
use warnings;
use strict;
use Math::Trig qw(great_circle_distance deg2rad);

# To calculate the distance between London (51.3N 0.5W) 
# and Tokyo (35.7N 139.8E) in kilometers: 

die "usage: latlongdist.pl LAT1 LONG1 LAT2 LONG2\n" if scalar(@ARGV) != 4;

my ($lat1, $long1, $lat2, $long2) = @ARGV;

# Notice the 90 - latitude: phi zero is at the North Pole.
my @L = (deg2rad(0 - $long1), deg2rad(90 - $lat1));
my @T = (deg2rad(0 - $long2),deg2rad(90 - $lat1));

my $km = great_circle_distance(@L, @T, 6378);

my $a = ($lat1 - $lat2);
my $b = ($long1 - $long2);
my $c = sqrt($a**2 + $b**2);

print "c = $c, km = $km\n";
