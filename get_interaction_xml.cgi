#!/usr/bin/perl -T

use strict;
use warnings;
use CGI;
use DBI;
use Data::Dumper;

my $query = new CGI;
my $locus = $query->param('locus');


#####
## Here's all the MySQL initialization
#####
# MySQL database information
my $dbName = 'gsignal';	
my $host = "bioinfolab.unl.edu";
my $user = "gprotein";
my $password = "gpa";

# Connection info, connect
my $connectionInfo = "dbi:mysql:$dbName:$host";
my $dbh = DBI->connect($connectionInfo, $user, $password) 
    or die "Could not connect to $dbName: " . DBI->errstr;
    
    
####
# Here's just a test SQL
####







##################################################
# get_data
#
# DESCRIPTION: get all of the data needed for the interaction 
#             using the locus  
#
# IN
#       $locus            : locus of the protein to be found
#       @loci             : an array of multiple locus
#
# OUT
#       $hashref		  : a reference to a hash that will be
#                       used by XML::Simple 
##################################################
sub get_data{
    
    #######
    ###TODO
    #######
    ### Reduce this query so we can also get correlation coefficients
    my $sql = "
        SELECT
            Node_from,
            Node_to,
            Data_Type,
            PubMed
        FROM
            tair_nbrowseMay2010
    
            ";
    
    
    
    

    # Prepare and execute SQL statement
    my $sth = $dbh->prepare($sql) or die "Could not prepare statement: " . DBI->errstr;
	$sth->execute()
	    or die "Couldn't execute statement: " . $sth->errstr;

    # create variables and bind to columns
    my ($node_from, $node_to, $data_type, $pubMed);
    $sth->bind_columns(\$node_from, \$node_to, \$data_type, \$pubMed);
    
    while($sth->fetch()){
        my %temp_hash = ();
        

        $temp_hash{} = ;
        $temp_hash{} = ;
        $temp_hash{} = ;
        $temp_hash{} = ;
        
    }    
}
