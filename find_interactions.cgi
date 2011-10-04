#!/usr/bin/perl -T

BEGIN{
    unshift @INC, "./modules/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi";
}

print "Content-Type: text/html\n\n";

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

#$p_locus = "AT3G05920";

#$p_locus = "AT1G02870";

$bid = 2;

my ($info_sql, $data_sql) = build_queries();


my $header = 'templates/header_template.html';
my $protein_info = 'templates/protein_info_template.html';
my $footer = 'templates/footer_template.html';
my $file = 'templates/table_template.html';

my $proteins = &get_data($data_sql);
my $info = &get_info($info_sql);

my $vars = {
	'proteins' => $proteins,
	'info'     => $info
};

my $template = Template->new();

$template->process($header) 			
	or die "Template process failed!\n", $template->error(), "\n";

$template->process($protein_info, $vars) 
	or die "Template process failed!\n", $template->error(), "\n";
	
$template->process($file, $vars) 
	or die "Template process failed!\n", $template->error(), "\n";

$template->process($footer) 
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
	
	
	# all of these should be available in all of the methods.
	#my ($view, $bid, $p_locus, $sig, $nr) = @_;
	
	my ($info_sql, $data_sql);
	
	$info_sql = "";
	my $select_statement;
	my $select_info_statement;
	
	my $from_statement = "
		FROM 
			$interactTB, 
			$tair, 
			$corrCoef";
	
	my $where_statement = "";
	
#### --------------------------------------------------------------------
##   This section is deciding what kind of page/query we need to build	

	if($view){
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
	}
	# This only tests if the first four params are undefined, if so... just display a summary
	elsif(!($view)  && !($bid) && !($p_locus) && !($sig)){
		$view = "summary";
		print "WHOA THERE NELLY, there was nothing defined!\n";
		# Here we might just end up re-calling this method
	}
	# Else the rest of these must be Bait specific or Prey specific interactions
	else{
		
		# This is the select statement for our SQL query
		# This will be different depending on what we want to view:
		#   All of the prey-baits or just one set of interactions
		$select_statement = "
			SELECT
				$corrCoef.Corr_coeff_anatomy, 
				$corrCoef.Corr_coeff_development, 
				$corrCoef.Corr_coeff_mutation, 
				$corrCoef.Corr_coeff_stimulus, 
				$corrCoef.Sig_anatomy, 
				$corrCoef.Sig_development, 
				$corrCoef.Sig_mutation, 
				$corrCoef.Sig_stimulus,
				
				$tair.Short_desc, 
				$tair.AA_len,
				";
				
				
		# If, for some reason, both the bait and prey is defined...
		if($bid && $p_locus){
			print "AHOY THERE MATEY! \n\n\n\n";
			# Just throw this line up there and exit the program.
			exit;
		}
		# Else if the Bait ID is defined, we can start building our query.
		elsif($bid){
			### This first part will just be the data_sql
			# This is the select part of the SQL query
			$select_statement .= "
				$interactTB.Prey_locus,
				$interactTB.Prey_cDNA_start
			";
			
			# This is the where part of our SQL query
			$where_statement = "
				WHERE 
					$interactTB.Prey_locus = $tair.Locus AND
					$interactTB.BP_ID = $corrCoef.BP_ID AND
					$interactTB.Bait_ID = $bid;
			";
			
			# We then need to combine the statements to obtain our data_sql query.
			$data_sql = $select_statement . $from_statement . $where_statement;
			
			### This second part will be the info_sql
			# We neeed to just make an all new select statement
			$select_statement = "
				SELECT
					COUNT(*),
					
					$tair.Short_desc,
					$tair.AA_len,
					
					$baitTB.Bait_locus,
					$baitTB.Bait_name";
			# And probably a new from statement as well
			$from_statement = "
				FROM
					$interactTB,
					$tair,
					$corrCoef,
					$baitTB
			";
			# And most definitely a new where statement
			$where_statement = "
				WHERE
					$tair.Locus = $baitTB.Bait_locus AND
					$interactTB.BP_ID = $corrCoef .BP_ID AND
					$baitTB.Bait_ID = $interactTB.Bait_ID AND
					$interactTB.Bait_ID = $bid;
			";
			
			# This is going to be a combination of the data_sql as well as adding
			# a couple SELECT fields
			$info_sql = $select_statement . $from_statement . $where_statement;
		}
		# Else if the Prey locus is defined, we can start building our query.
		elsif($p_locus){
			# This is the select part of the SQL query
			$select_statement .= "
				$baitTB.Bait_locus,
				$interactTB.Prey_cDNA_start
			";
			
			# For this case, we need to add a line to our From statment
			$from_statement .= ",
				$baitTB";
			
			# This statment makes sure we get the right 
			$where_statement = "
				WHERE 
					$baitTB.Bait_locus = $tair.Locus AND
					$interactTB.BP_ID = $corrCoef.BP_ID AND
					$interactTB.Bait_ID = $baitTB.Bait_ID AND
					$interactTB.Prey_locus = '$p_locus';
			";
			
			# We then need to combine the statements to obtain our data_sql query.
			$data_sql = $select_statement . $from_statement . $where_statement;
			
			### This second part will be the info_sql
			# We neeed to just make an all new select statement
			$select_statement = "
				SELECT
					COUNT(*),
					
					$tair.Short_desc,
					$tair.AA_len,
					
					$interactTB.Prey_locus,
					$interactTB.Prey_locus";
			# And probably a new from statement as well
			$from_statement = "
				FROM
					$interactTB,
					$tair,
					$corrCoef
			";
			# And most definitely a new where statement
			$where_statement = "
				WHERE
					$tair.Locus = $interactTB.Prey_locus AND
					$interactTB.BP_ID = $corrCoef.BP_ID AND
					$interactTB.Prey_locus = '$p_locus';
			";
			
			# This is going to be a combination of the data_sql as well as adding
			# a couple SELECT fields
			$info_sql = $select_statement . $from_statement . $where_statement;
			
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
    my $sql = shift;

    my $sth = $dbh->prepare($sql)
        or die "Could not prepare statement: " . DBI->errstr;
    $sth->execute()
        or die "Couldn't execute statement: " . $sth->errstr;
    my ($interactions, $desc, $aa_length, $locus, $name);
    $sth->bind_columns(\$interactions, \$desc, \$aa_length, \$locus, \$name);
    $sth->fetch();

	my ($count_ana, $count_mut, $count_dev, $count_stim) = get_significant_count();

	# Store all of the gathered information in a temporary hash to be returned
    my $temp_hash = {
        'locus' => $locus,
        'name' => $name,
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
#       $count_ana	 	  :   the anatomy count
#		$count_mut		  :   the mutation count
# 		$count_dev		  :   the development count
#		$count_stim		  :   the stimulus count
##################################################
sub get_significant_count{
	
	my $query = "";
	
	# If we have our bait_id defined, make the query equal to it
	if($bid){
		$query = "$interactTB.Bait_ID = $bid";
	}
	# If we have our prey_locus defined, make the query equal to it.
	elsif($p_locus){
		$query = "$interactTB.Prey_locus = '$p_locus'";
	}
	else{
		print "I don't know if this is right!";
		exit;
	}
	
	# This long SQL query is to count how many significant proteins there are for each correlation attribute
	my $sql = "SELECT 
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
						$query) 
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
						$query) 
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
						$query) 
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
						$query) 
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
	
	# Initialize the variables to store our counts.
	my ($count_ana, $count_mut, $count_dev, $count_stim);
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
    my $sql = shift;

	my $sth = $dbh->prepare($sql) or die "Could not prepare statement: " . DBI->errstr;
	
	$sth->execute()
	or die "Couldn't execute statement: " . $sth->errstr;
	
	# These are all the variables for running this query
	my ($locus, $cdna, $desc, $length, $corr_ana, $corr_dev, $corr_mut, $corr_stim, $sig_ana, $sig_dev, $sig_mut, $sig_stim);
	$sth->bind_columns(\$corr_ana, \$corr_dev, \$corr_mut, \$corr_stim, \$sig_ana, \$sig_dev, \$sig_mut, \$sig_stim, \$desc, \$length, \$locus, \$cdna);
	
	# This is the array with all of the proteins
	my @proteins = ();
		
	while($sth->fetch()){
		my %temp_hash = ();
		
		$temp_hash{locus} = $locus;
		$temp_hash{cdna} = $cdna;
		$temp_hash{desc} = $desc;
		$temp_hash{len} = $length;
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
