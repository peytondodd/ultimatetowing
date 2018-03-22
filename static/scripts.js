// Towing Application
companyCode = "";
$(document).ready(function() {

    $("#company_code").keypress(function() {
	setTimeout(function() {

	    companyCode = $("#company_code").val();

	    if ($("#company_code").val().length>5){
		companyCode = $("#company_code").val().slice(0,5);
		$("#company_code").val(companyCode);
	    }

	    if ($("#company_code").val().length==5){
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
		companycode: companyCode
	    },
	    success: function(returnVal) {
		console.log("returned value: " + returnVal);
		cb_func(returnVal);
	    },
	    error: function(request,error) {
		alert('CALLBACK ERROR NIGGA');
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
    $("#company_code").val("");
    $("#company_name_form").animate({
	opacity: 1
    }, 300);
    $("#changeCompanyButton").fadeOut("150");
    $("#operator_info_form").fadeOut("150");
    $("#companyNameTitle").fadeOut("150");
}






