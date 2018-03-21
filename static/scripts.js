// Towing Application

$(document).ready(function() {
    $("#company_code").keypress(function() {
	setTimeout(function() {
	    if ($("#company_code").val().length>5){
		$("#company_code").val($("#company_code").val().slice(0,5));
	    }
	},300);
    });
});
