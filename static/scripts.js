// Towing Application
companyid = "";
$(document).ready(function() {

    $("#companyid").keypress(function() {
	setTimeout(function() {

	    companyid = $("#companyid").val();

	    if ($("#companyid").val().length>9){
		companyid = $("#companyid").val().slice(0,9);
		$("#companyid").val(companyid);
	    }

	    if ($("#companyid").val().length==9){
		$(':input[type="submit"]').prop('disabled', false);

	    } else {
		$(':input[type="submit"]').prop('disabled', true);
	    }

	},200);

    });

    $("#changeCompanyButton").click(showCompanySelector);
});

$(function() {
    $('#company_name_form').submit(function() {
        $.ajax({
            type: 'POST',
            url: '/getCompanyName',
            data: { 
		companyid: companyid
	    },
	    success: function(returnVal) {
		console.log("Business Incorporation #: " + returnVal);
		console.log(companyid);
		cb_func(companyid, returnVal);
	    },
	    error: function(request,error) {
		console.log('Callback error.');
	    }
        });
        return false;
    }); 
})

function cb_func(companyid, companyname) {
    $("#companyname").fadeOut(100, function() {
	this.companyid = companyid;
	this.companyname = companyname;
	if(companyname == "") {
	    companyname = companyid + " Ontario Inc.";
	} else {
	    companyname = companyname;
	}
	$("#companyname").text(companyname);
    });

    $("#companyname").fadeIn(250, function() {
	if(companyname != "") {
	    $("#ownerInfoWrapper").delay(1000).fadeIn("350");
	    hideCompanySelector();
	} else {
	    $("#ownerInfoWrapper").fadeIn("100");
	    hideCompanySelector();
	}
    });
}

function hideCompanySelector() {
    //$("#company_name_form").fadeOut("100");
    $("#company_name_form").animate({
	opacity: 0
    }, 300);
    $("#changeCompanyButton").fadeIn("150");
}

function showCompanySelector() {
    //$("#companyid").val("");
    $("#company_name_form").animate({
	opacity: 1
    }, 300);
    $("#changeCompanyButton").fadeOut("150");
    $("#owner_info_form").fadeOut("150");
    $("#companyname").fadeOut("150");
}






