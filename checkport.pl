#!/usr/bin/env perl

use strict;
use warnings;
use IO::Socket;

my $usage = "$0 IP PORT [PROTO]\n";

my $ip = shift or die $usage;
my $port = shift or die $usage;

print "Attempting to connect to $ip:$port via TCP.\n";

my $sock = IO::Socket::INET->new(PeerAddr=>$ip,
				 PeerPort=>$port,
				 Proto=>'tcp',
				 Timeout=>10)
    or die "IO::Socket::INET->new: $@\n";

if ($sock->connected) {
    print "connected!\n";
} else {
    print "not connected.\n";
}

$sock->close();

exit 0;
