#!/usr/bin/perl

BEGIN{
    unshift @INC, "./modules/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi";
}

print "Content-Type: text/xml\n\n";


use strict;
use warnings;
use CGI;
use DBI;
use Data::Dumper;
use Template;

my $query = new CGI;
my $locus = $query->param('locus');

#$locus = "AT1G01040";
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


my ($hash_ref, $nodes) = get_data();
print_xml($hash_ref);



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
	        Bait_locus,
            Prey_locus,
            BP_ID
        FROM
            bait,
            interact
        WHERE
            bait.Bait_ID = interact.Bait_ID AND
            (bait.Bait_locus = '$locus') OR ( interact.Prey_locus = '$locus')
        GROUP BY
            Prey_locus
        ;
            ";
    
    # Prepare and execute SQL statement
    my $sth = $dbh->prepare($sql) or die "Could not prepare statement: " . DBI->errstr;
	$sth->execute()
	    or die "Couldn't execute statement: " . $sth->errstr;

    # create variables and bind to columns
    my ($bp_id, $bait_locus, $prey_locus);
    $sth->bind_columns(\$bait_locus, \$prey_locus, \$bp_id);

    # Make all of the hashes, including the node hash
    my %protein_hash;
    my %node_hash;
    my @edges;
    
    while($sth->fetch()){
        my %temp_hash;
        
        $temp_hash{node_from} = $bait_locus;
        $temp_hash{node_to} = $prey_locus;
        $protein_hash{$bp_id} = \%temp_hash;
        push @edges, \%temp_hash;
        $node_hash{$bait_locus} = 1;
        $node_hash{$prey_locus} = 1;

    }   
    
    my @nodes;
    
    # For each of the nodes in the hash add it to the array
    foreach my $node(keys %node_hash){
        push @nodes, $node;
    }
    
    
    
    return \%protein_hash, \@nodes, \@edges;
}


##################################################
# print_xml
#
# DESCRIPTION: print the xml using the hash ref that was given
#
# IN
#       $interactions       : all of the interactions for this locus
#
# OUT
#       Nothing will be returned, all will be printed - John 3:42
#
##################################################
sub print_xml{
    my ($interactions, $nodes, $edges) = get_data();
    
    #Define all of the Template stuff
    my $interaction_xml = 'templates/interaction.xml';
    my $template = Template->new();
    
    my $data = {
                'interactions'  => $interactions,
                'nodes'         => $nodes,
                'edges'         => $edges
                };
    
    
    $template->process($interaction_xml, $data);


}
