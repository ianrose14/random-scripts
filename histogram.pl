#!/usr/bin/perl

use warnings;
use strict;

use ITR::Util qw(:functions);

my $column = 1;     # default=1
my $num_bins = 8;   # default=8
my ($start_bins, $stop_bins);

my $usage = "histogram [-c column] [-n num-bins] [-r start-bins] [-t stop-bins] [input-file]";

while (@ARGV > 0) {
    if ($ARGV[0] eq "-c") {
	shift(@ARGV);
	die "histogram: invalid column value: \"$ARGV[0]\"\n" if (!is_int($ARGV[0]));
	$column = shift(@ARGV);
    }
    elsif ($ARGV[0] eq "-n") {
	shift(@ARGV);
	die "histogram: invalid num-bins value: \"$ARGV[0]\"\n" if (!is_int($ARGV[0]));
	$num_bins = shift(@ARGV);
    }
    elsif ($ARGV[0] eq "-r") {
	shift(@ARGV);
	die "histogram: invalid start-bins value: \"$ARGV[0]\"\n" if (!is_number($ARGV[0]));
	$start_bins = shift(@ARGV);
    }
    elsif ($ARGV[0] eq "-t") {
	shift(@ARGV);
	die "histogram: invalid stop-bins value: \"$ARGV[0]\"\n" if (!is_number($ARGV[0]));
	$stop_bins = shift(@ARGV);
    }
    elsif ($ARGV[0] eq "-u" || $ARGV[0] eq "-h") {
        print "$usage\n";
        exit 0;
    }
    else {
	last;
    }
}

my $in_filename = shift(@ARGV);
my $in_handle;

if (defined($in_filename)) {
    open $in_handle, $in_filename or die "histogram: $in_filename: $!\n";
}
else {
    $in_handle = \*STDIN;
}

my $line_num = 1;
my $skip_cols = $column-1;
my @data;

while (my $line = <$in_handle>) {
    next if $line =~ /^\s*$/ || $line =~ /^\s*#/;   # skip comments and blank lines
    chomp($line);
    
    if ($line =~ /^\s*(?:\S+\s+){$skip_cols}([0-9e\.]+)(?:\s|$)/) {
	push @data, $1+0;
	
	$line_num++;
    }
};

close($in_handle);

exit 0 if @data == 0;

if (!defined($start_bins)) {
    $start_bins = min(@data);
}

if (!defined($stop_bins)) {
    $stop_bins = max(@data);
}

my $range = $stop_bins - $start_bins;
my @bins;

# special case: all values are identical
if ($range == 0) {
    $num_bins = 1;
    $bins[0] = scalar(@data);
}
else {
    for (my $i=0; $i < $num_bins; $i++) {
	$bins[$i] = 0;
    }
    
    my $index;
    
    for (my $i=0; $i < @data; $i++) {
	if ($data[$i] == $stop_bins) {
	    # special handling
	    $index = $num_bins-1;
	}
	else {
	    $index = int((($data[$i]-$start_bins)/$range)*$num_bins);
	}
	
	if (($index >= 0) && ($index < $num_bins)) {
	    $bins[$index]++;
	}
    }
}

for (my $i=0; $i < $num_bins; $i++) {
    print (($start_bins + $i*($range/$num_bins)), "\t", ($start_bins + ($i+1)*($range/$num_bins)), "\t", $bins[$i], "\n");
}

exit 0;
