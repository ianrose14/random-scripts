#!/usr/bin/perl -w
use strict;

my $in_handle = \*STDIN;

my @data;
my $min_datum;
my $max_datum;

my $perc = shift(@ARGV);

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
    
    push @data, (0 + $fields[0]);
}

close($in_handle);

my $total_count = scalar(@data);

my $i=1;

foreach my $datum (sort{$a <=> $b} (@data)) {
    if ($i >= ($total_count*$perc/100)) {
	print "$datum\n";
	exit 0;
    }
    
    $i++;
}

# done
