#/usr/bin/perl -T

use strict;
use warnings;
use Template;
use CGI;
use DBI;
use Data::Dumper;

my $query = new CGI;
my $bid = $query->param('bid');
my $nr = $query->param('nr');
my $sort = $query->param('sort');

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
	my $dbh = DBI->connect($connectionInfo, $user, $password) or die "Could not connect to $dbName: " . DBI->errstr;

	# MySQL table information
	my $baitTB = "bait";
	my $interactTB = "interact";
	my $libTB = "library";
	my $tair = "tair9";
	my $tairGO = "tair9_GO";
	my $tairSQ = "tair9_seq";
	my $corrCoef = "correlation";
	
#####
## Here's where all the MySQL stuff ends
#####

###
# We are going to need to decide if this is a:
## 1) Bait-prey interaction
##    if so: use the baid id ($bid)
## 2) Prey-bait interaction
##    if so: use the prey's locus (?)
###


my $id = 2;

my $header = 'templates/header_template.html';
my $protein_info = 'templates/protein_info_template.html';
my $footer = 'templates/footer_template.html';
my $file = 'templates/table_template.html';
my $vars = {
    'message'  => "hello charlie",
	'proteins' => \&get_data,
	'info'     => \&get_info,
	'id'       => $id
};

my $template = Template->new();

$template->process($header) 			
	or die "Template process failed!\n", $template->error(), "\n";

$template->process($protein_info, $vars) 
	or die "Template process failed!\n", $template->error(), "\n";
	
$template->process($file, $vars) 
	or die "Template process failed!\n", $template->error(), "\n";


	
##################################################
# get_info
#
# DESCRIPTION: get the info for this bait/prey 
#             using the bait_id/prey_id  
#
# IN
#       $bait_id/$prey_id : id of the protein to be found
#		$nr				  : BOOL to decide non-redundant
#		
#
# OUT
#       %proteins		  :   a hash with all the protein info
##################################################
sub get_info(){
    # These are the vars we need for this query
	#####
	# TODO
	# We need to be able to pass whether it is a bait or a prey 
	# so we can adjust the queries accordingly
	#####
    my $bid = shift;
    my $nr = shift;
    
    # This will get information on the protein that is currently being looked at so it can be displayed 
	# in the protein info box
    my $sql = "SELECT 
                    $baitTB.Bait_locus, 
					$baitTB.Bait_name,
					 
					$tair.Short_desc,
					$tair.AA_len,
					
					count(*)
                FROM 
                    $baitTB,
					$tair,
					$interactTB
                WHERE 
					$baitTB.Bait_locus = $tair.Locus AND
					$interactTB.Bait_ID = $baitTB.Bait_ID AND
                    $baitTB.Bait_ID = $bid;";
    my $sth = $dbh->prepare($sql)
        or die "Could not prepare statement: " . DBI->errstr;
    $sth->execute()
        or die "Couldn't execute statement: " . $sth->errstr;
    my ($blocus, $bname, $desc, $aa_length, $interactions);
    $sth->bind_columns(\$blocus, \$bname, \$desc, \$aa_length, \$interactions);
    $sth->fetch();

	# This long SQL query is to count how many significant proteins there are for each correlation attribute
	my ($count_ana, $count_mut, $count_dev, $count_stim);
	$sql = "SELECT 
					(SELECT 
						count(*) 
					FROM 
						$corrCoef,
						$interactTB 
					WHERE 
						Sig_anatomy=1 
					AND 
						$interactTB.BP_ID = $corrCoef.BP_ID 
					AND 
						$interactTB.Bait_ID = $bid) 
					AS 
						count_anatomy,

					(SELECT 
						count(*) 
					FROM 
						$corrCoef,
						$interactTB 
					WHERE 
						Sig_mutation=1 
					AND 
						$interactTB.BP_ID = $corrCoef.BP_ID 
					AND 
						$interactTB.Bait_ID = $bid) 
					AS 
						count_mutation,

					(SELECT 
						count(*) 
					FROM 
						$corrCoef,
						$interactTB 
					WHERE 
						Sig_development=1 
					AND 
						$interactTB.BP_ID = $corrCoef.BP_ID 
					AND 
						$interactTB.Bait_ID = $bid) 
					AS 
						count_development,

					(SELECT 
						count(*) 
					FROM 
						$corrCoef,
						$interactTB 
					WHERE 
						Sig_stimulus=1 
					AND 
						$interactTB.BP_ID = $corrCoef.BP_ID 
					AND 
						$interactTB.Bait_ID = $bid) 
					AS 
						count_stimulus							
			FROM
				dual
					;";
	
	# Prepare and execute the SQL statement
	$sth = $dbh->prepare($sql)
	   or die "Could not prepare statement: " . DBI->errstr;
	$sth->execute()
	   or die "Couldn't execute statement: " . $sth->errstr;
	
	# Bind each of the four colomns to a different variable
    $sth->bind_columns(\$count_ana, \$count_mut, \$count_dev, \$count_stim);
	$sth->fetch();

	# Store all of the gathered information in a temporary hash to be returned
    my $temp_hash = {
        'locus' => $blocus,
        'name' => $bname,
		'desc' => $desc,
		'aa'   => $aa_length,
		'int'  => $interactions,
		'count_ana' => $count_ana, 
		'count_mut' =>	$count_mut, 
		'count_dev' =>	$count_dev, 
		'count_stim' => $count_stim
    };
    
    return $temp_hash;
}

	
##################################################
# get_data
#
# DESCRIPTION: get an array of hashes by using the 
#             bait_id/prey_id  
#
# IN
#       $bait_id/$prey_id : id of the protein to be found
#		$nr				  : BOOL to decide non-redundant
#		$sort			  : string of what to sort by
#
# OUT
#       @proteins		  :   an array of hashes with all the proteins is returned
##################################################
sub get_data(){
	# These are the three vars we need for this sql query
	my $bid = shift;
	my $nr = shift;
	my $sort = shift;


	#####
	# TODO
	# We need to be able to pass whether it is a bait or a prey 
	# so we can adjust the queries accordingly
	#####


	# This is the MySQL query that I call to get all of the information (test for relevancy)
	####
	##TODO: reduce this query as much as possible as to only obtain info relevant to the table
	####
	my $sql = "
			SELECT
				$interactTB.BP_ID,
				$interactTB.Library,
				$interactTB.Prey_locus,
				$interactTB.Prey_cDNA_start,
				$interactTB.Notes,
				$interactTB.Candidate_ID, 
		
				$tair.Symbol1,
				$tair.Symbol2, 
				$tair.Short_desc, 
				$tair.Curator_summary, 
				$tair.Comp_desc, 
				$tair.AA_len, 
				
				$corrCoef.Corr_coeff_anatomy, 
				$corrCoef.Corr_coeff_development, 
				$corrCoef.Corr_coeff_mutation, 
				$corrCoef.Corr_coeff_stimulus, 
				$corrCoef.Sig_anatomy, 
				$corrCoef.Sig_development, 
				$corrCoef.Sig_mutation, 
				$corrCoef.Sig_stimulus
			FROM 
				$interactTB, 
				$tair, 
				$corrCoef
            WHERE 
				$interactTB.Prey_locus = $tair.Locus AND
				$interactTB.BP_ID = $corrCoef.BP_ID AND
				$interactTB.Bait_ID = $bid";
	# If we want the non-redundant results
	if ($nr) {
		$sql .= " GROUP BY $interactTB.Prey_locus";
	}

	# Finish the SQL with the semi-colon
	$sql .= ";";

	
	my $sth = $dbh->prepare($sql) or die "Could not prepare statement: " . DBI->errstr;
	
	$sth->execute()
	or die "Couldn't execute statement: " . $sth->errstr;
	
	# These are all the variables for running this query
	my ($bpid, $library, $plocus, $pcdna, $pnote, $cand_id, $sym1, $sym2, $desc, $curator, $comp, $plen, $corr_ana, $corr_dev, $corr_mut, $corr_stim, $sig_ana, $sig_dev, $sig_mut, $sig_stim);
	$sth->bind_columns(\$bpid, \$library, \$plocus, \$pcdna, \$pnote, \$cand_id, \$sym1, \$sym2, \$desc, \$curator, \$comp, \$plen, \$corr_ana, \$corr_dev, \$corr_mut, \$corr_stim, \$sig_ana, \$sig_dev, \$sig_mut, \$sig_stim);
	
	# This is the array with all of the proteins
	my @proteins = ();
	
	
	while($sth->fetch()){
		my %temp_hash = ();
		
		$temp_hash{plocus} = $plocus;
		$temp_hash{pcdna} = $pcdna;
		$temp_hash{desc} = $desc;
		$temp_hash{plen} = $plen;
		$temp_hash{corr_ana} = $corr_ana;
		$temp_hash{corr_dev} = $corr_dev;
		$temp_hash{corr_mut} = $corr_mut;
		$temp_hash{corr_stim} = $corr_stim;
		$temp_hash{sig_ana} = $sig_ana;
		$temp_hash{sig_dev} = $sig_dev;
		$temp_hash{sig_mut} = $sig_mut;
		$temp_hash{sig_stim} = $sig_stim;
		push @proteins, \%temp_hash;
	}
	
	return \@proteins;

}
