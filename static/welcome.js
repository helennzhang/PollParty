let map;

function initMap() {
    const myLatLng = { lat: 38.9869, lng: 76.9426 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 4,
        center: myLatLng,
    });
};


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
            for (let i = 0; i < response.earlyVoteSites.length; i++) {
                const latLng = new google.maps.LatLng(response.earlyVoteSites[i].latitude, response.earlyVoteSites[i].longitude);
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                });
            }
        },
        error: (err) => { console.log(err) }
    });
});

