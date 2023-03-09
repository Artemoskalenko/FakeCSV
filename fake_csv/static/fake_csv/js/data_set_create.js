$("#data_set_create").click(function() {
    let list = document.querySelector('#datasets > tbody');
    let last_data_set = list.lastElementChild;
    if (last_data_set === null) {
        var next_id = 1
    } else {
        let last_data_set_th = last_data_set.querySelector('th');
        let last_data_set_id = last_data_set_th.getAttribute('id');
        var next_id = parseInt(last_data_set_id) + 1
    };

    $('#datasets > tbody').append(`<tr><th scope="row" id="${next_id}">${next_id}</th><td>Right now</td><td id="processing_button"><button style="background-color: #6c757d;" type="button" class="btn btn-secondary" disabled>Processing</button></td><td id="url_to_file"></td></tr>`);

    //AJAX запрос
    $.ajax({
        type: "GET",

        url: "generate_data/",

        data: {
            "rows": $("#rows_input").val(),
        },

        dataType: "text",

        cache: false,

        success: function (data) {
            let new_data_set = list.lastElementChild;
            $('#processing_button').empty();
            $('#processing_button').append(`<button type="button" class="btn btn-success" disabled="">Ready</button>`);
            $('#processing_button').attr('id', '');
            $('#url_to_file').append(`<a href="${data}" id="download-btn" download="" class="text-decoration-none">Download</a>`);
            $('#url_to_file').attr('id', '');
        }

    });
});