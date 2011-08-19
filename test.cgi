#/usr/bin/perl -T

use strict;
use warnings;
use Template;
use CGI;
use DBI;
use Data::Dumper;

my $query = new CGI;
my $view = $query->param('view');
my $bid = $query->param('bait_id');
my $p_locus = $query->param('plocus');
my $nr = $query->param('nr');
my $sig = $query->param('sig');

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

my ($info_sql, $data_sql) = build_queries($view, $bid, $p_locus, $sig, $nr);


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
# build_queries
#
# DESCRIPTION: build the queries for the methods 
#             using the bait_id/prey_locus
#			 as well as the view and other params  
#
# IN
#       $view			  : if we want to view either...
#								-view all by each bait
#								-view all by each prey
#								-view a summary (how to group?)
#		$id				  : id of the protein to be found
#		$nr				  : BOOL to decide non-redundant
#		
#
# OUT
#       %proteins		  :   a hash with all the protein info
##################################################
sub build_queries{
	my ($view, $bid, $p_locus, $sig, $nr) = @_;
	
	my ($info_sql, $data_sql);
	
	
#### --------------------------------------------------------------------
##   This section is deciding what kind of page/query we need to build	

	# If we want to view all of the interactions by each bait
	if($view eq "baits"){
		### TODO
		
	}
	# If we want to view all of the interactions by each prey locus
	elsif($view eq "preys"){
		### TODO
		
	}
	# If we want to view all of the interactions as a summary (ALL interactions are displayed)
	elsif($view eq "summary"){
		### TODO
		
	}
	# This only tests if the first four params are undefined, if so... just display a summary
	elsif(($view == undef)  && ($bid == undef) && ($p_locus == undef) && ($sig == undef)){
		$view = "summary";
		# Here we might just end up re-calling this method
	}
	# Else the rest of these must be Bait specific or Prey specific interactions
	else{
		# If, for some reason, both the bait and prey is defined...
		if($bid && $p_locus){
			print "AHOY THERE MATEY! \n\n\n\n";
			# Just throw this line up there and exit the program.
			exit;
		}
		# Else if the Bait ID is defined, we can start building our query.
		elsif($bid){
			
		}
		# Else if the Prey locus is defined, we can start building our query.
		elsif($p_locus){
			
		}
		# Here, we assume neither are defined... for right now let's just throw another error and quit.
		else{
			print "AHOY THERE MATEY! \n\n\n\n";
			# Just throw this line up there and exit the program.
			exit;
		}
		
		
		
	}
	
#### --------------------------------------------------------------------
	
	return ($info_sql, $data_sql);
}


	
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
    my $bid = shift;
	my $p_locus = shift;
	my $sig = shift;
	my $nr = shift;
	
	
	
	#####
	# TODO
	# We need to be able to pass whether it is a bait or a prey 
	# so we can adjust the queries accordingly
	# -----------
	# How this will work:
	# -----------
	# One of five things need to happen:
	#	1) We want a view of all of the interactions by the bait
	#		?view=baits
	#	2) We want a view of all the interactions by the prey
	#		?view=preys
	#	3) We want to view one bait's interactions by using the bait ID
	#		?bait_id=XX
	#	4) We want to view one of the prey's interactions by using the prey locus
	#		?plocus=XXXXXXXXXX
	#	5) We want to view a summary of all the interactions
	#		?view=summary
	#####
	
	
    
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
# get_significant_count
#
# DESCRIPTION: get the number of significant 
#             correlation coefficient for each bait/prey  
#
# IN
#       $id				  : id of the protein to be found
#		$nr				  : BOOL to decide non-redundant
#
# OUT
#       @proteins		  :   an array of hashes with all the proteins is returned
##################################################
sub get_significant_count{
	
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
	my $sth = $dbh->prepare($sql)
	   or die "Could not prepare statement: " . DBI->errstr;
	$sth->execute()
	   or die "Couldn't execute statement: " . $sth->errstr;
	
	# Bind each of the four colomns to a different variable
    $sth->bind_columns(\$count_ana, \$count_mut, \$count_dev, \$count_stim);
	$sth->fetch();
	
	return ($count_ana, $count_mut, $count_dev, $count_stim);
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
	my $p_locus = shift;
	my $sig = shift;
	my $nr = shift;


	#####
	# TODO
	# We need to be able to pass whether it is a bait or a prey 
	# so we can adjust the queries accordingly
	# -----------
	# How this will work:
	# -----------
	# One of five things need to happen:
	#	1) We want a view of all of the interactions by the bait
	#		?view=baits
	#	2) We want a view of all the interactions by the prey
	#		?view=preys
	#	3) We want to view one bait's interactions by using the bait ID
	#		?bait_id=XX
	#	4) We want to view one of the prey's interactions by using the prey locus
	#		?plocus=XXXXXXXXXX
	#	5) We want to view a summary of all the interactions
	#		?view=summary
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
