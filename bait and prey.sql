my ONE BAIT QUERY = "
		SELECT
			$interactTB.Prey_locus,
			$interactTB.Prey_cDNA_start,
	
			$tair.Short_desc, 
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
			
my ONE PREY QUERY = "
	SELECT
		$bait.Bait_locus,
		$interactTB.Prey_cDNA_start,

		$tair.Short_desc, 
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
		$corrCoef,
		$bait
	WHERE 
		$interactTB.Prey_locus = $tair.Locus AND
		$interactTB.BP_ID = $corrCoef.BP_ID AND
		$interactTB.Bait_ID = $bait.Bait_ID AND
		$interactTB.Prey_locus = $p_locus";
		

# This will get information on the protein that is currently being looked at so it can be displayed 
		# in the protein info box
my ONE BAIT INFO QUERY = "SELECT 
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


# This will get information on the protein that is currently being looked at so it can be displayed 
		# in the protein info box
my ONE PREY INFO QUERY = "SELECT 
	                    $baitTB.Bait_locus, 
						$baitTB.Bait_name,

						$tair.Short_desc,
						$tair.AA_len,

						count(*)
	                FROM 
						$tair,
						$interactTB
	                WHERE 
						$interactTB.Bait_locus = $tair.Locus AND
	                    $baitTB.Bait_ID = $bid;";
	
	