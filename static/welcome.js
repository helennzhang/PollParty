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
                    $("#poll_list").append(`<tr>
                    <th>` + response.earlyVoteSites[i].address.locationName + `</th>
                    <td>`+ response.earlyVoteSites[i].address.line1 + `</td>
                    <td>` + response.earlyVoteSites[i].address.city + `</td>
                    <td>` + response.earlyVoteSites[i].address.state + `</td>
                    <td>` + response.earlyVoteSites[i].address.zip + `</td>
                    <td><button class="btn btn-primary">Start a Party</button></td>
                    <td><button class="btn btn-primary">Join a Party</button></td>
                </tr>`);
                }
            },
            error: (err) => { console.log(err) }
        });
    });
}





