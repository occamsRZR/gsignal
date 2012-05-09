#!/usr/bin/perl
use strict;
use warnings;
use DBI;
use Data::Dumper;
use Getopt::Std;

# MySQL database name
my $db = "gsignal";

our ($opt_h, $opt_u, $opt_p, $opt_H, $opt_t, $opt_f, $opt_g); 



getopts('hu:p:H:t:f:g:');

if ($opt_h) {
        die "\nUsage: load_tair [options]",
            "\n[options]",
            "\n -h : print this help message",
            "\n -u user_ID: MySQL user ID",
            "\n -p password: MySQL password",
            "\n -H host_name: MySQL host name [default: localhost]",
            "\n -t table_name: MySQL table name",
            "\n -f function_file: TAIR function file",
            "\n -g gene_model_file: TAIR representative gene model file",
	    	"\n\n";
}

# Set the defaults for getopts
unless($opt_u){
    $opt_u = "gprotein";
}
unless($opt_p){
    $opt_p = "gpa";
}
unless($opt_H){
    $opt_H = "bioinfolab.unl.edu";
}
unless($opt_g){
    $opt_g = "TAIR10_pep_20110103_representative_gene_model";
}
unless($opt_f){
    $opt_f = "TAIR10_functional_descriptions";
}
unless($opt_t){
    $opt_t = "tair10";
}

print "This should be the user: $opt_u\n";

#####
## Here's all the MySQL initialization
#####
# MySQL database information
my $dbName = 'gsignal';	
my $host = $opt_H;
my $user = $opt_u;
my $password = $opt_p;
my $table = $opt_t;

# Connection info, connect
my $connectionInfo = "dbi:mysql:$dbName:$host";
my $dbh = DBI->connect($connectionInfo, $user, $password) 
    or die "Could not connect to $dbName: " . DBI->errstr;

my $loci_ref = unique_loci();

my $gene_file = $opt_g;
my $function_file = $opt_f;
$loci_ref = read_tair_flat_files($gene_file, $loci_ref);
check_table();
create_table($loci_ref);
update_table($loci_ref, $function_file);


##################################################
# unique_loci
#
# DESCRIPTION: make a hash of all the unique locii
#
# IN
#       NOTHING           :   we only need to get the locii from the DB   
#		                        
# OUT
#       %loci       	  :   a hash with each locii
##################################################
sub unique_loci{
    my %loci = ();
    
    my $sql = "
                SELECT
                    Prey_locus,
                    Bait_locus
                FROM
                    interact,
                    bait
                ";
    # prepare and execute statement
    my $sth = $dbh->prepare($sql) 
        or die "Could not prepare statement: " . DBI->errstr;
    $sth->execute()
        or die "Couldn't execute statement: " . $sth->errstr;
    my ($prey_locus, $bait_locus);
    $sth->bind_columns(\$prey_locus, \$bait_locus);
    
    # Fetch all of the records
    while($sth->fetch()){
        $loci{$prey_locus} = 1;
        $loci{$bait_locus} = 1;        
    }
    print "There are this many proteins in the loci hash:  ";
    print scalar(keys %loci);
    print "\n\n";
    return \%loci;
}



##################################################
# read_tair_flat_files
#
# DESCRIPTION: read both of the flat files from TAIR
#
# IN
#       $gene_file        :  this is the tair file for the gene models
#		                        
# OUT
#       $loci_ref         :  this is the reference to the loci_hash
##################################################
sub read_tair_flat_files{
    my $gene_file = shift;
    my $loci_ref = shift;
    # deref
    my %loci_hash = %$loci_ref;
    open(my $GENE, "<", $gene_file)
        or die "Could not open the gene file!\n";
        
    my ($locus, $gmodel, $sym1, $sym2, $des, $chr, $start, $end, $strand);
    my $gene;
    my $nline = 0;
    my $len;
    my $found_loc;

    # While reading the gene file, update the loci hash
    while(my $line = <$GENE>){
        chomp($line);
        if ($line =~ /^>(\S+) \| Symbols: (.*) \| (.*) \| (.*) (\S+) LENGTH=(\d+)/) { 
            ($locus, $gmodel, $sym1, $sym2, $des, $chr, $start, $end, $strand) = 
                ("", "", "", "", "", "", "", "");
    #	    print STDERR "$line";
            ($gmodel, $sym1, $des, $chr, $strand, $len) = ($1, $2, $3, $4, $5, $6);
            if ($gmodel) {
                $gmodel =~ /^(\S+)\.(\d+)/;
                $locus = $1;
            }
            else {
                die "Locus missing. Something is wrong.\n";
            }
            # First symbol = Symbol1, the rest -> Symbol2
            if ($sym1 =~ /(\S+), /) {
                $sym1 = $1;
                $sym2 = $';
            }
            if ($chr =~ /chr(\S+):(\d+)\-(\d+)/) {
                $chr = $1;
                $start = $2;
                $end = $3;
            }
            if ($strand =~ /REVERSE/) {
                $strand = '-';
            }
            else {
                $strand = '+';
            }
            
            $gene = {};
            $gene->{'locus'} = $locus;
            $gene->{'gmodel'} = $gmodel;
            $gene->{'symbol1'} = $sym1;
            $gene->{'symbol2'} = $sym2;
            $gene->{'desc'} = $des;
            $gene->{'chromo'} = $chr;
            $gene->{'start'} = $start;
            $gene->{'end'} = $end;
            $gene->{'strand'} = $strand;
            $gene->{'length'} = $len;

            if($loci_hash{$locus}){
                $loci_hash{$locus} = $gene;
            }
            $len = 0;
            ++$nline;
            print STDERR "$nline " if ($nline % 1000 == 0);
        }
        
    }
    close($GENE) or die "Could not close the gene file!\n";
    
    $loci_ref = \%loci_hash;
    return $loci_ref;
}

##################################################
# check_table
#
# DESCRIPTION: This will check to see if table exists
#             
#
# IN
#               NOTHING
#       get (global) data from what is passed in the options
#                               
# OUT
#               NOTHING
##################################################
sub check_table{
    # Check if the table already exists
    my ($sth, $sql);
    $sth = $dbh->prepare("show tables") or die "$DBI::errstr\n";
    $sth->execute();
    my @row;
    $opt_t = 0;
    while (@row = $sth->fetchrow()) {
        if ($table eq $row[0]) {
            $opt_t = 1;
            last;
        }
    }
    if ($opt_t) {
        print "\n$table table exists. Delete? [y|N] ";
        my $opt = <STDIN>;
        if ($opt =~ /^[Nn]/) {
            exit 0;
        }
        else {
            print " Deleting $table table\n";
            $sql = "drop table $table";
            $sth = $dbh->do($sql) or die "$DBI::errstr\n";
        }
    }
}

##################################################
# create_table
#
# DESCRIPTION: This will create the database with 
#             the data collected from the gene file
#
# IN
#       $loci_ref        :  this is the tair file for the functions
#                               
#		                        
# OUT
#               NOTHING
##################################################
sub create_table{
    my $loci_ref = shift;
    my %loci_hash = %$loci_ref;
    
    # create the table
    my $createTable = "
        CREATE TABLE $table (
            Locus varchar(30) NOT NULL,
            Gene_model varchar(30) NOT NULL,
            Symbol1 varchar(30),
            Symbol2 varchar(30),
            Short_desc text,
            Curator_summary text,
            Comp_desc text,
            Chromosome varchar(2),
            Start int(20),
            End int(20),
            Strand varchar(1) NOT NULL,
            AA_len int(10) NOT NULL,
            N_model int(5) NOT NULL,
            PRIMARY KEY (Locus)
        )";
    my $sth = $dbh->prepare($createTable) 
        or die "Could not prepare the create table statement: " . DBI->errstr;
    $sth->execute()
        or die "Could not execute the create table statemetn: " . $sth->errstr;
}

##################################################
# update_table
#
# DESCRIPTION: This will update the database with 
#             the data collected from the function file
#
# IN
#           $loci_ref        :  this is the tair file for the functions
#           $function_file    :  this is the tair file for the functions
#                               
#		                        
# OUT
#       @sql_queries	  :   an array with all of the queries
##################################################
sub update_table{
    my $loci_ref = shift;
    my $function_file = shift;
    my %loci_hash = %$loci_ref;
    
    # Setting MySQL table coloumn heads
    my @thead =("Locus", "Gene_model", "Symbol1", "Symbol2", "Short_desc", 
        "Curator_summary", "Comp_desc", "Chromosome", "Start", "End", "Strand", "AA_len", "N_model");
    my $cols = join(',', @thead);
    my $ncols = @thead;
    
    my ($val, $n, $i);
    print STDERR " MySQL table has $ncols fields: $cols\n";
    
    print STDERR "\nPopulating $table table\n";
    
    
    open(my $FUNCTION, "<", $function_file) or die "Could not open the function file!\n";
    my ($type, $curator, $comp, $gene, $locus, $gmodel, $sql, $sth, $des);
    my @models;
    my $found;
    my $ngene = 0;
    print STDERR "Entries done: ";
    while (my $line = <$FUNCTION>) {
        next if ($line =~ /^Model_name/); # skip the header line
        chomp($line);
        ($gmodel, $type, $des, $curator, $comp) = split('\t', $line);
        next if ($type !~ /protein_coding/);
    
        # Find the gene model
        $gmodel =~ /(\S+)\./;
        $locus = $1;
        # Do the next line (record) unless we have it in our hash
        next unless($loci_hash{$locus});
        # If we've ran across this before, just add up the number of variants
        if ($loci_hash{$locus}  && $loci_hash{$locus}->{variants}) {
            $loci_hash{$locus}->{'variants'}++; # counting splicing variants
            next;
        }
        elsif($loci_hash{$locus}) {
            $loci_hash{$locus}->{'variants'} = 1;
        }
       
        $val = $dbh->quote($loci_hash{$locus}->{'locus'}) . ',' . $dbh->quote($gmodel) . ',';
        
        if ($loci_hash{$locus}->{'symbol1'}) {
            $val .= $dbh->quote($loci_hash{$locus}->{'symbol1'}) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($loci_hash{$locus}->{'symbol2'}) {
            $val .= $dbh->quote($loci_hash{$locus}->{'symbol2'}) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($loci_hash{$locus}->{'desc'}) {
            $val .= $dbh->quote($loci_hash{$locus}->{'desc'}) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($curator) {
            $val .= $dbh->quote($curator) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($comp) {
            $val .= $dbh->quote($comp) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($loci_hash{$locus}->{'chromo'}) {
            $val .= $dbh->quote($loci_hash{$locus}->{'chromo'}) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($loci_hash{$locus}->{'start'}) {
            $val .= $dbh->quote($loci_hash{$locus}->{'start'}) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        if ($loci_hash{$locus}->{'end'}) {
            $val .= $dbh->quote($loci_hash{$locus}->{'end'}) . ',';
        }
        else {
            $val .= 'NULL,';
        }
        $val .= $dbh->quote($loci_hash{$locus}->{'strand'}) . ',';
        $val .= $dbh->quote($loci_hash{$locus}->{'length'}) . ',\'1\'';
    
    #	print STDERR $val;
        $sql = "insert into $table ($cols) values ($val)";
    #	print STDERR "$sql\n";
        $sth = $dbh->do($sql) or die "$DBI::errstr\n";
        ++$ngene;
        print STDERR "$ngene " if ($ngene % 1000 == 0);
    }
    close $FUNCTION or die "Could not close the function file!\n";
    print STDERR "\n$ngene entries processed\n";
    print STDERR "Now processing splice variants\n";
       
    # Updating table with N_model data if it's > 1
    my $nmodel = 0;
    my $loci = 0;
    foreach my $locus (keys %loci_hash) {
        #print "Variants: scalar($loci_hash{$locus}->{'variants'})\n";
        if($loci_hash{$locus} == 1){
            next;
        }
        my $variants = scalar($loci_hash{$locus}->{'variants'});
        if ($variants > 1) {
            $sql = "
                UPDATE
                    $table 
                SET 
                    N_model = $loci_hash{$locus}->{'variants'} 
                WHERE 
                    Locus = \"$locus\"
                    ";
            $sth = $dbh->do($sql) or die "$DBI::errstr\n";
            $nmodel++;
        }
        $loci++;
    }
    print STDERR "$nmodel entries have splicing variants\n";
}