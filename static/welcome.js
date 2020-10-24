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
        success: (response) => { console.log(response) },
        error: (err) => { console.log(err) }
    });



});