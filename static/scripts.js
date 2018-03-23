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
		cb_func(returnVal);
	    },
	    error: function(request,error) {
		console.log('Callback error.');
	    }
        });
        return false;
    }); 
})

function cb_func(data) {
    $("#companyNameTitle").fadeOut(100, function() {
	if(data == "") {
	    companyNameTitle = "Company name not found. Please enter a valid code.";
	} else {
	    companyNameTitle = data;
	}
	$("#companyNameTitle").text(companyNameTitle);
    });

    $("#companyNameTitle").fadeIn(250, function() {
	if(data != "") {
	    $("#operator_info_form").delay(1000).fadeIn("350");
	    hideCompanySelector();
	} else {
	    $("#operator_info_form").fadeOut("100");
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
    $("#companyid").val("");
    $("#company_name_form").animate({
	opacity: 1
    }, 300);
    $("#changeCompanyButton").fadeOut("150");
    $("#operator_info_form").fadeOut("150");
    $("#companyNameTitle").fadeOut("150");
}






