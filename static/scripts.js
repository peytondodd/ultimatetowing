// Towing Application
companyid = "";
$(document).ready(function() {

    // enable submit button when input string length is 9 
    $('#companyidcheck').on('change textInput input', function () {
	companyid = this.value;

	var btn = $("#checkCompanyButton");

	if (companyid.length==9){
	    btn.prop('disabled', false);

	} else {
	    btn.prop('disabled', true);
	}
    });

    // enable submit button when all input fields are filled
    $('#company_info_form input').keyup(function() {
	var empty = $("#company_info_form").find("input").filter(function() {
	    return this.value === "";
	});
	if(empty.length) {
	   $(':input[type="submit"]').prop('disabled', true);
	} else {
	   $(':input[type="submit"]').prop('disabled', false);
	}
    });

    $('#operator_info_form input').keyup(function() {
	var empty = $("#operator_info_form").find("input").filter(function() {
	    return this.value === "";
	});
	if(empty.length) {
	   $(':input[type="submit"]').prop('disabled', true);
	} else {
	   $(':input[type="submit"]').prop('disabled', false);
	}
    });

    configure();
});

/*
 *  check if company exists on submit 
 */
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
    $("#company_name_form").fadeOut(100, function() {
	if(data == "") {
	    // new company - show registration form
	    $("#company_info_form #companyid").val(companyid);
	    $("#company_info_form #companyidtitle").text("Reg. #: " + companyid);
	    $("#company_info_form").fadeIn(200);
	} else {
	    // existing company - redirect to request ownership page 
	    window.location.href = "/requestOwnership";
	}
    });
}

function hideCompanySelector() {
    //$("#company_name_form").fadeOut("100");
    $("#company_name_form").animate({
	opacity: 0
    }, 150, function() {
	$("#company_name_form").hide();
    });
    $("#changeCompanyButton").fadeIn("150");
}

function showCompanySelector() {
    //$("#companyid").val("");
    $("#company_name_form").show().animate({
	opacity: 1
    }, 300);
    $("#changeCompanyButton").fadeOut("150");
    $("#owner_info_form").fadeOut("150");
    $("#companyname").fadeOut("150");
}

var timeout; 

function configure() {
    // Configure typeahead
    $("#q").typeahead({
        highlight: false,
        minLength: 1
    },
    {
        display: function(suggestion) { return null; },
        limit: 5,
        source: function(value, syncResult, asyncResult) {


            if (timeout) {
                clearTimeout(timeout);
            }

            timeout = setTimeout(function() {
                searchCompany(value, syncResult, asyncResult);
            }, 50);

        },
        templates: {
            suggestion: function(data) {
                return "<div class='typeahead-row'>" +
			    "<div class='company-name'>" + data[1] + "</div>" + 
			    "<div class='company-id'>(" + data[0] + ")</div>" + 
			"</div>"
	    }
        }
    });

    // Re-center map after place is selected from drop-down
    $("#q").on("typeahead:selected", function(eventObject, suggestion) {
	// hide company name search form 
	$("#company_name_form").fadeOut(200, function() {
	    $("#companyNameTitle").text(suggestion[1]);
	    $("#operator_info_form").fadeIn(200, function() {
		$("#companyid").val(suggestion[0]);
	    });
	});
    });

    // Hide info window when text box has focus
    $("#q").focus(function(eventData) {
	// do something
    });

    // Give focus to text box
    $("#q").focus();

}

// Search database for typeahead's suggestions
function searchCompany(query, syncResults, asyncResults)
{
    // Get places matching query (asynchronously)
    let parameters = {
        q: query
    };
    $.getJSON("/searchCompany", parameters, function(data) {

        // Call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    });
}





