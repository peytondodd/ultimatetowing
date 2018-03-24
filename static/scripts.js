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

    configure();
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
    $("#q").on("typeahead:selected", function(eventObject, suggestion, name) {
	// populate title 
	// place 'change' button next to it
	// fade in operator info form
	console.log("SELECTED: " + suggestion);
    });

    // Hide info window when text box has focus
    $("#q").focus(function(eventData) {
	// do something
    });

    // Re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
    // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
    document.addEventListener("contextmenu", function(event) {
        event.returnValue = true;
        event.stopPropagation && event.stopPropagation();
        event.cancelBubble && event.cancelBubble();
    }, true);

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





