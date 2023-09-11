// main.js

$(document).ready(function() {
    $('#user-input-form').submit(function(event) {
        event.preventDefault();
        var userInput = $('#user-input').val();

        $.ajax({
            type: 'POST',
            url: '/generate-response',
            data: {
                user_input: userInput
            },
            success: function(data) {
                // Обновляем содержимое элемента с id "model-response" данными, полученными от сервера
                $('#model-response').text(data.response);
            },
            error: function(error) {
                console.error('Произошла ошибка:', error);
            }
        });
    });
});
