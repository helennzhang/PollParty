let map;

function initMap() {
    const myLatLng = { lat: -25.363, lng: 131.044 };
    const map = new google.maps.Map($("#map"), {
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
            const sites = response.earlyVoteSites;
            for (let i = 0; i < sites.length; i++) {
                new google.maps.Marker({
                    position: { lat: sites[i].latitude, lng: sites[i].longitude },
                    map,
                });
            }
        },
        error: (err) => { console.log(err) }
    });
});

