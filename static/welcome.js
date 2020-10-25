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
                    <td>
                    <input type="checkbox" name="bar" /> </td>
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

function myfunc() {
    var valueList = [];
    $('#poll_list tr').each(function () {
        $(this).find("input[name='bar']:checked").each(function () {
            var values = [];
            $(this).closest("td").siblings("td").each(function () {
                values.push($(this).text());
            });
            valueList.push(values.join(", "));
        });
    });
    console.log("(" + valueList.join("),(") + ")");
}

$("#startParty").click(function (event) {
    console.log(event);
    myfunc();
});


