#!/usr/bin/perl -w

use strict;
use CGI;
use Data::Dumper;

my $DEBUG = 0;

print "Content-Type: text/html\n\n";

# clean up the directory first (remove one day or older files
system("find ./tmp/file*.txt -mtime +1 -exec rm {} \;");

my $job = $$; # the process id is used as the job ID
my $file = "file$job.txt";
my $file1 = "./tmp/$file";
my $file3 = "/emlab/Gsignal/cgi/tmp/$file";

my $buffer;
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

# Split information into name/value pairs
my @pairs = split(/&/, $buffer);
my %form;
foreach my $pair (@pairs)
{
    my ($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%(..)/pack("C", hex($1))/eg;
	$form{$name} = $value;
}
my $res;
if (defined $form{res}) {
    $res = $form{res};
}
elsif (defined $form{res2}) {
    $res = $form{res2};
}
elsif (defined $form{res3}) {
    $res = $form{res3};
}

if ($DEBUG) {
    print "res: $res " if (defined $res);
    print "file: $file";
}

open FILE, ">$file1" or die "Cannot open $file: $!\n";
print FILE "$res";
close FILE;

#print Dumper(%form);
if (defined $form{res}) {
    print "The table has all columns with the header line in TAB-delimited format:<br><br>";
}
elsif (defined $form{res2}) {
    print "The table has only 2 columns for Bait and Prey in TAIR locus IDs without the header line in TAB-delimited format.<br><br>";
}
elsif (defined $form{res3}) {
    print "The table has only 2 columns for Bait and Prey in gene names or TAIR IDs without the header line in TAB-delimited format.<br><br>";
}
print "<a target=\"_blank\" href=\"$file3\">$file</a><br><br>";
print "Click the link above to open the file.<br>";
print "Or right-click on the link to save the file directly on your local disk.<br>";

exit 0;
