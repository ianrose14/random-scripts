#!/usr/bin/perl -w
use strict;

my $in_handle = \*STDIN;

my $granularity = 100;
$granularity = shift(@ARGV) if (scalar(@ARGV) > 0);

my @data;
my $min_datum;
my $max_datum;

LINE: while (my $line = <$in_handle>) {
    next if $line =~ /^\s*$/ || $line =~ /^\s*#/;   # skip comments and blank lines
    chomp($line);

    my @fields = split(/\t/, $line);
    
    my $value = 0 + $fields[0];
    
    if (defined($max_datum)) {
	if ($value > $max_datum) {
	    $max_datum = $value;
	}
    }
    else {
	$max_datum = $value;
    }
    
    if (defined($min_datum)) {
	if ($value < $min_datum) {
	    $min_datum = $value;
	}
    }
    else {
	$min_datum = $value;
    }
    
    push @data, $value;
}

close($in_handle);

# sort data, ascending
@data = sort { $a <=> $b } @data;

my $x_spread = $max_datum - $min_datum;
my $y_step = 1 / $granularity;
my $last_print_x = 0;
my $last_print_y = 0;

# print first datum
print "$min_datum\t0\n";

my ($this_x, $this_y);

for (my $i=0; $i < @data; $i++) {
    $this_x = ($data[$i] - $min_datum) / $x_spread;
    $this_y = $i/scalar(@data);
    
    # if this_y is more than 1/[granularity] greater than last_print_y,
    #  then its time for a new data point to be printed
    if ($this_y >= ($last_print_y + $y_step)) {
	print "$data[$i]\t$this_y\n";
	$last_print_x = $this_x;
	$last_print_y = $this_y;
    }
}

# done
