const url = '../static/data/unique_data.json';

// Populate dropdown with list of provinces
$.getJSON(url, function (data) {

        $.each(JSON.parse(data.ATC), function (index, item) {
            $('#dropdown-TCA').append($('<a></a>').attr('class', 'dropdown-item').text(item.Name));
        });

        $.each(JSON.parse(data.사업부), function (index, item) {
            $('#dropdown-사업부').append($('<a></a>').attr('class', 'dropdown-item').text(item.Name));
        });

        $.each(JSON.parse(data.사무소), function (index, item) {
            $('#dropdown-사무소').append($('<a></a>').attr('class', 'dropdown-item').text(item.Name));
        });

        $.each(JSON.parse(data.지역), function (index, item) {
            $('#dropdown-지역').append($('<a></a>').attr('class', 'dropdown-item').text(item.Name));
        });

        $('#dropdown-TCA a').click(function () {
            $('#options-TCA').text($(this).text());
        });

        $('#dropdown-사업부 a').click(function () {
            $('#options-사업부').text($(this).text());
        });

        $('#dropdown-사무소 a').click(function () {
            $('#options-사무소').text($(this).text());
        });

        $('#dropdown-지역 a').click(function () {
            $('#options-지역').text($(this).text());
        });

        $.each(JSON.parse(data.지역), function (index, item) {
            $('#dropdown-지역').append($('<a></a>').attr('class', 'dropdown-item').text(item.Name));
        });
    }
);

$(function () {
    $('a#calculate').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val()
        }, function (data) {
            $("#result").text(data.result);
        });
        return false;
    });
});







