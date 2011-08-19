my ONE BAIT QUERY = "
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
			
my ONE PREY QUERY = "
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