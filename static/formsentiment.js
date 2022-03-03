$(document).ready(() => {
    $('form').on('submit', (event) => {
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: { name: $('#text').val() }
        })
            .done((data) => {
                alert(data)
            });
        event.preventDefault();
    });
});
