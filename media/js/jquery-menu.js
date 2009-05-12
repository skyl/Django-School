/* ================================================================ 
This copyright notice must be untouched at all times.
Copyright (c) 2008 Stu Nicholls - stunicholls.com - all rights reserved.
=================================================================== */

$(document).ready(function(){
	if($("#topnav")) {
		$("#topnav dd").hide();
		$("#topnav dt b").click(function() {
			if(this.className.indexOf("clicked") != -1) {
				$(this).parent().next().slideUp(200);
				$(this).removeClass("clicked");
			}
			else {
				$("#topnav dt b").removeClass();
				$(this).addClass("clicked");
				$("#topnav dd:visible").slideUp(200);
				$(this).parent().next().slideDown(500);
			}
			return false;
		});
	}
});
