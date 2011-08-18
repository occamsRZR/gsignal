window.onload=function(){


/* Image w/ description tooltip v2.0
* Created: April 23rd, 2010. This notice must stay intact for usage 
* Author: Dynamic Drive at http://www.dynamicdrive.com/
* Visit http://www.dynamicdrive.com/ for full source code
*/


var ddimgtooltip={

	tiparray:function(){
		
		var tooltips=[]
		//define each tooltip below: tooltip[inc]=['path_to_image', 'optional desc', optional_CSS_object]
		//For desc parameter, backslash any special characters inside your text such as apotrophes ('). Example: "I\'m the king of the world"
		//For CSS object, follow the syntax: {property1:"cssvalue1", property2:"cssvalue2", etc}
			//tooltips[0]=["red_balloon.gif", "Here is a red balloon<br /> on a white background", {background:"#FFFFFF", color:"black", border:"5px ridge darkblue"}]
			//tooltips[1]=["duck2.gif", "Here is a duck on a light blue background.", {background:"#DDECFF", width:"200px"}]
			//tooltips[2]=["../dynamicindex14/winter.jpg"]
			//tooltips[3]=["../dynamicindex17/bridge.gif", "Bridge to somewhere.", {background:"white", font:"bold 12px Arial"}]
			
			//TAIR's NBrowse images
			tooltips[1]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/TGA1.jpg"]
			tooltips[2]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/AGB1.jpg"]
			tooltips[3]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/NDL1.jpg"]
			tooltips[4]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/SYP23.jpg"]
			tooltips[5]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/RGS1.jpg"]
			tooltips[6]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/GPA1.jpg"]
			tooltips[7]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/RACK1C.jpg"]
			tooltips[8]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/Phosducin.jpg"]
			tooltips[9]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/ATARD1.jpg"]
			tooltips[10]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/GPA1.jpg"]
			tooltips[11]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/UNE16.jpg"]
			tooltips[12]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/Esterase-Lipase.jpg"]
			tooltips[13]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/PRN.jpg"]
			tooltips[14]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/ATARD3.jpg"]
			tooltips[15]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/ATARD4.jpg"]
			tooltips[16]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/CDC48B.jpg"]
			tooltips[17]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/RACK1A.jpg"]
			tooltips[18]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/RACK1B.jpg"]
			tooltips[19]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/VAP27.jpg"]
			tooltips[20]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/ANNAT1.jpg"]
			tooltips[21]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/ATARD2.jpg"]
			tooltips[22]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/GPA1.jpg"]
			
			//our interactions shown using NBrowse images
			tooltips[51]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT5G65210.jpg"]
			tooltips[52]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT4G34460.jpg"]
			tooltips[53]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT5G56750.jpg"]
			tooltips[54]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT4G17730.jpg"]
			tooltips[55]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT3G26090.jpg"]
			tooltips[56]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT2G26300caGPA1.jpg"]
			tooltips[57]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT3G18130.jpg"]
			tooltips[58]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT5G14240.jpg"]
			tooltips[59]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT4G14716.jpg"]
			tooltips[510]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT2G26300wtGPA1.jpg"]
			tooltips[511]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT4G13640.jpg"]
			tooltips[512]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT1G52760.jpg"]
			tooltips[513]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT3G59220.jpg"]
			tooltips[514]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT2G26400.jpg"]
			tooltips[515]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT5G43850.jpg"]
			tooltips[516]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT2G03670.jpg"]
			tooltips[517]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT1G18080.jpg"]
			tooltips[518]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT1G48630.jpg"]
			tooltips[519]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT3G60600.jpg"]
			tooltips[520]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT1G35720.jpg"]
			tooltips[521]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT4G14710.jpg"]
			tooltips[522]=["/emlab/Gsignal/files/NBrowseStaticImages/BaitsPrey/AT2G26300.jpg"]
			
			//library definitions
			tooltips[1000]=["","Arabidopsis thaliana Matchmaker cDNA (Clontech), 3wk-old green vegetative tissue, cv. Columbia, 3x10e6 independent clones; Insert size = 0,6-4,0 kb, average 1,2kb; oligo-(dT) and random primed cDNA", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1001]=["","A. thaliana Suspension Culture, oligo-(dT) primed cDNA", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1002]=["","Arabidopsis thaliana cv. Columbia, oligo-(dT) primed cDNA, plants grown in liquid culture, treated with flg22", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1003]=["","Arabidopsis thaliana cv. Columbia, oligo-(dT) primed cDNA, plants grown in liquid culture", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1004]=["","Arabidopsis thaliana cv. Columbia, seeds treated at 4C for 2 days and then transferred to 22C continuous light for 7 days. Roots were harvested and used to isolate RNA", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1005]=["","Etiolated Seedlings, Arabidopsis thaliana cv. Columbia, seeds were treated at 4C for 2 days and then transferred to 22C in the dark for 48 hours. Whole seedlings were used to isolate RNA", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1006]=["","cDNA library from glucose treated 7-day old A.t Col0 seedlings grown in liquid culture. (1% sucrose 7days, no sucrose 2 days, 6% glucose 3 hours)", {font:"12px Arial",color:"#002224", width:"200px"}]
			tooltips[1007]=["","Pool of ~1000 Arabidopsis Transcription Factors", {font:"12px Arial",color:"#002224"}]
			tooltips[1008]=["","cDNA from Arabidopsis leaf tissue infected with P. Syringae", {font:"12px Arial",color:"#002224"}]
			
			//tooltips[$num]=["/emlab/Gsignal/files/NBrowseStaticImages/TAIRbait/$bname.jpg"];
		return tooltips //do not remove/change this line
	}(),

	tooltipoffsets: [20, 20], //additional x and y offset from mouse cursor for tooltips

	//***** NO NEED TO EDIT BEYOND HERE

	tipprefix: 'imgtip', //tooltip ID prefixes

	createtip:function($, tipid, tipinfo){
		if ($('#'+tipid).length==0){ //if this tooltip doesn't exist yet
			return $('<div id="' + tipid + '" class="ddimgtooltip" />').html(
				'<div style="text-align:center"><img src="' + tipinfo[0] + '" /></div>'
				+ ((tipinfo[1])? '<div style="text-align:left; margin-top:5px">'+tipinfo[1]+'</div>' : '')
				)
			.css(tipinfo[2] || {})
			.appendTo(document.body)
		}
		return null
	},
	
	
	
	
	
	

	positiontooltip:function($, $tooltip, e){
		var x=e.pageX+this.tooltipoffsets[0], y=e.pageY+this.tooltipoffsets[1]
		var tipw=$tooltip.outerWidth(), tiph=$tooltip.outerHeight(), 
		x=(x+tipw>$(document).scrollLeft()+$(window).width())? x-tipw-(ddimgtooltip.tooltipoffsets[0]*2) : x
		y=(y+tiph>$(document).scrollTop()+$(window).height())? $(document).scrollTop()+$(window).height()-tiph-10 : y
		$tooltip.css({left:x, top:y})
	},
	
	showbox:function($, $tooltip, e){
		$tooltip.show()
		this.positiontooltip($, $tooltip, e)
	},

	hidebox:function($, $tooltip){
		$tooltip.hide()
	},


	init:function(targetselector){
		jQuery(document).ready(function($){
			var tiparray=ddimgtooltip.tiparray
			var $targets=$(targetselector)
			if ($targets.length==0)
				return
			var tipids=[]
			$targets.each(function(){
				var $target=$(this)
				$target.attr('rel').match(/\[(\d+)\]/) //match d of attribute rel="imgtip[d]"
				var tipsuffix=parseInt(RegExp.$1) //get d as integer
				var tipid=this._tipid=ddimgtooltip.tipprefix+tipsuffix //construct this tip's ID value and remember it
				var $tooltip=ddimgtooltip.createtip($, tipid, tiparray[tipsuffix])
				$target.mouseenter(function(e){
					var $tooltip=$("#"+this._tipid)
					ddimgtooltip.showbox($, $tooltip, e)
				})
				$target.mouseleave(function(e){
					var $tooltip=$("#"+this._tipid)
					ddimgtooltip.hidebox($, $tooltip)
				})
				$target.mousemove(function(e){
					var $tooltip=$("#"+this._tipid)
					ddimgtooltip.positiontooltip($, $tooltip, e)
				})
				if ($tooltip){ //add mouseenter to this tooltip (only if event hasn't already been added)
					$tooltip.mouseenter(function(){
						ddimgtooltip.hidebox($, $(this))
					})
				}
			})

		}) //end dom ready
	}
}

//ddimgtooltip.init("targetElementSelector")
ddimgtooltip.init("*[rel^=imgtip]")


}