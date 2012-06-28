#!/usr/bin/perl -w
use strict;

# import file of handy subroutines
# Note: probably have to alter this path on different systems 
use Utils_ITR;

# NOTE: ASSUMES SORTED INPUT

my $filename = shift(@ARGV);
my $in_handle;

if (defined($filename) && ($filename ne "-")) {
    open $in_handle, $filename or die "dupes.pl: $filename: $!\n";
}
else {
    $in_handle = \*STDIN;
}

my $last_line;

while (my $line = <$in_handle>) {
    chomp($line);
    
    if (defined($last_line)) {
	if ($last_line eq $line) {
	    # duplicate!
	    print "$line\n";
	}
    }
    
    $last_line = $line;
}

close($in_handle);

# done
