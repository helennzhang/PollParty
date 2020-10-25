let map;

function initMap() {
    const myLatLng = { lat: 38.9869, lng: -76.9426 };
    var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 4,
        center: myLatLng,
    });

    $("#form").submit(function (event) {
        event.preventDefault();

        const data = {
            address: $('#address').val(),
        }

        $.ajax({
            url: '/welcome/pollsites',
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: (response) => {
                $('#poll_list').empty();
                var bounds = new google.maps.LatLngBounds();
                for (let i = 0; i < response.earlyVoteSites.length; i++) {
                    var position = { lat: response.earlyVoteSites[i].latitude, lng: response.earlyVoteSites[i].longitude };
                    bounds.extend(position)
                    var marker = new google.maps.Marker({
                        position: position,
                        map: map,
                    });
                    map.fitBounds(bounds);
                    $("#poll_list").append(`<tr id=${response.earlyVoteSites[i].address.locationName}>
                    <td><input type="checkbox"/></td>
                    <td>` + response.earlyVoteSites[i].address.locationName + `</td>
                    <td>`+ response.earlyVoteSites[i].address.line1 + `</td>
                    <td>` + response.earlyVoteSites[i].address.city + `</td>
                    <td>` + response.earlyVoteSites[i].address.state + `</td>
                    <td>` + response.earlyVoteSites[i].address.zip + `</td>
                </tr>`);
                }
            },
            error: (err) => { console.log(err) }
        });
    });
}


document.getElementById("startParty").addEventListener('click', startParty, false);
function startParty() {
    var table = document.getElementById("table1");
    var checkBoxes = table.getElementsByTagName("INPUT");
    var message = {
        "locationName": "",
        "zip": ""
    }
    for (var i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            message["locationName"] = row.cells[1].innerHTML;
            message["zip"] = row.cells[5].innerHTML;
        }
    }
    console.log(message)
    
    $.ajax({
        url: '/welcome/createparty',
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(message),
        success: (response) => {
            
        },
        error: (err) => { console.log(err) }
    });
}

document.getElementById("joinParty").addEventListener('click', joinParty, false);
function joinParty() {
    var table = document.getElementById("table1");
    var checkBoxes = table.getElementsByTagName("INPUT");
    var message = {
        "locationName": "",
        "zip": ""
    }
    for (var i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            message["locationName"] = row.cells[1].innerHTML;
            message["zip"] = row.cells[5].innerHTML;
        }
    }
    console.log(message)

    $.ajax({
        url: '/welcome/joinparty',
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(message),
        success: (response) => {
            console.log(response)
        },
        error: (err) => { console.log(err) }
    });
}





