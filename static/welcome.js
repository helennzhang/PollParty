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
                var bounds = new google.maps.LatLngBounds();
                for (let i = 0; i < response.earlyVoteSites.length; i++) {
                    var position = { lat: response.earlyVoteSites[i].latitude, lng: response.earlyVoteSites[i].longitude };
                    bounds.extend(position)
                    var marker = new google.maps.Marker({
                        position: position,
                        map: map,
                    });
                    map.fitBounds(bounds);
                }
            },
            error: (err) => { console.log(err) }
        });
    });
}




