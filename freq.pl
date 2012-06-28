#!/usr/bin/env perl 

use warnings;
use strict;

my %dict;

while (<>) {
    chomp();
    next if length($_) == 0;

    if (defined($dict{$_})) {
	$dict{$_}++;
    }
    else {
	$dict{$_} = 1;
    }
}

foreach my $key (sort(keys(%dict))) {
    print "$key\t$dict{$key}\n";
}

exit 0;
