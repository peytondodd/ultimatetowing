// Towing Application

// Company ID
companyid = "";

// Google Map
let map;

// Markers for map
let markers = [];

// Info window
let info = new google.maps.InfoWindow();

// Execute when the DOM is fully loaded
$(document).ready(function() {

    // Styles for map
    // https://developers.google.com/maps/documentation/javascript/styling
    let styles = [

        // Hide Google's labels
        {
            featureType: "all",
            elementType: "labels",
            stylers: [
                {visibility: "off"}
            ]
        },

        // Hide roads
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {visibility: "off"}
            ]
        }

    ];

    // Options for map
    // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    let options = {
	center: {lat: 43.7037, lng: -79.3646}, // Toronto, Canada
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 14,
        panControl: true,
        zoom: 12,
        zoomControl: true
    };

    // Get DOM node in which map will be instantiated
    let canvas = $("#map").get(0);

    // Instantiate map
    map = new google.maps.Map(canvas, options);

    // Configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);


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
    $('#request_ownership_form input').keyup(function() {
	var empty = $("#request_ownership_form").find("input").filter(function() {
	    return this.value === "";
	});
	if(empty.length) {
	   $(':input[type="submit"]').prop('disabled', true);
	} else {
	   $(':input[type="submit"]').prop('disabled', false);
	}
    });

    // onload requestownership.html - get companyid parameter
    if ( window.location.pathname == "/requestOwnership" ) {
	$("#companyid").val( getUrlParameter('companyid') );
    }

    if ( window.location.pathname == "/login" ) {
	$('#usertype>option:eq(1)').prop('selected', true);
    }

    // bind close message on clicking x
    $('.messageBox .x').click(function() {
	$(this).parent().fadeOut(function() {
	    $(this).remove();
	});
    });

    configureTypeahead();
});

function locateMe() {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(function(position) {
	    var pos = {
		lat: position.coords.latitude,
		lng: position.coords.longitude
	    };

	    var image = "/static/redtruck-40.png";
	    marker = new google.maps.Marker({
		position: pos,
		map: map,
		animation: google.maps.Animation.DROP,
		icon: image,
		title: 'Me :)'
	    });

	    marker.addListener('click', function() {
		info.open(map, marker);
	    });

	    info.setPosition(pos);
	    info.setContent('It\'s me! Mario');

	}, function() {
	    handleLocationError(true, info, map.getCenter());
	});
    } else {
	// Browser doesn't support Geolocation
	handleLocationError(false, info, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, info, pos) {
    info.setPosition(pos);
    info.setContent(browserHasGeolocation ?
	    'Error: The Geolocation service failed.' :
	    'Error: Your browser doesn\'t support geolocation.');
    info.open(map);
}

// Add marker for place to map
function addMarker(place)
{
    // var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    var image = 'http://icons.iconarchive.com/icons/icons-land/sport/24/Soccer-Ball-icon.png';
    var title = place.place_name + ' | ' + place.admin_name2 + ", " + place.admin_name1;
    var marker = new google.maps.Marker({
          position: {lat: place.latitude, lng: place.longitude},
          map: map,
          title: title,
          icon: image
    });

    markers.push(marker);

    marker.addListener("click", function(){

        let parameters = {
            geo: place.postal_code
        };

        $.getJSON("/articles", parameters, function(data, textStatus, jqXHR) {

            var content = "<ul class='articlelist'>";

            for (var article of data) {

                content += `<li>
                <a href="${article.link}" target="_blank">${article.title}</a>
                </li>`;
            }

            content += "</ul>";

            showInfo(marker,content);
        });

    });


}

var timeout;

// Configure application
function configure()
{
    // show my location
    locateMe();

    /*
    // Update UI after map has been dragged
    google.maps.event.addListener(map, "dragend", function() {

        // If info window isn't open
        // http://stackoverflow.com/a/12410385
        if (!info.getMap || !info.getMap())
        {
            locateMe();
        }

    });
    */
}


// Remove markers from map
function removeMarkers()
{

    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }

}


// Search database for typeahead's suggestions
function search(query, syncResults, asyncResults)
{
    // Get places matching query (asynchronously)
    let parameters = {
        q: query
    };
    $.getJSON("/search", parameters, function(data, textStatus, jqXHR) {

        // Call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    });
}


// Show info window at marker with content
function showInfo(marker, content)
{
    // Start div
    let div = "<div id='info'>";
    if (typeof(content) == "undefined")
    {
        // http://www.ajaxload.info/
        div += "<img alt='loading' src='/static/ajax-loader.gif'/>";
    }
    else
    {
        div += content;
    }

    // End div
    div += "</div>";

    // Set info window's content
    info.setContent(div);

    // Open info window (if not already open)
    info.open(map, marker);
}

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
	    // existing company - redirect to request ownership page (pass companyid parameter)
	    window.location.href = "/requestOwnership?companyid=" + companyid;
	}
    });
}

var timeout; 

function configureTypeahead() {
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
	// hide company search form 
	$("#company_name_form").fadeOut(200, function() {
	    $("#companyNameTitle").text(suggestion[1]);
	// show operator info form
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


info = new google.maps.InfoWindow;

function initMap() {
    // Create a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), {
	center: {lat: 43.7037, lng: -79.3646},
	zoom: 12,
	gestureHandling: 'greedy'
    });

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(function(position) {
	    var pos = {
		lat: position.coords.latitude,
		lng: position.coords.longitude
	    };

	    marker = new google.maps.Marker({
		position: pos,
		map: map,
		title: 'Me :)'
	    });

	    marker.addListener('click', function() {
		info.open(map, marker);
	    });

	    info.setPosition(pos);
	    info.setContent('It\'s me! Mario');
	    info.open(map);
	    map.setCenter(pos);

	}, function() {
	    handleLocationError(true, info, map.getCenter());
	});
    } else {
	// Browser doesn't support Geolocation
	handleLocationError(false, info, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, info, pos) {
    info.setPosition(pos);
    info.setContent(browserHasGeolocation ?
	    'Error: The Geolocation service failed.' :
	    'Error: Your browser doesn\'t support geolocation.');
    info.open(map);
}

