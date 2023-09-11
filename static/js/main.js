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
                // Успешный ответ от сервера
                var modelResponseContainer = $('#model-response-container');
                var modelResponse = $('#model-response');
                modelResponse.text(data.response);

                // Установите класс "success" для успешного ответа и удалите класс "error"
                modelResponseContainer.removeClass('error').addClass('success');
            },
            error: function(error) {
                // Ошибка от сервера
                console.error('Произошла ошибка:', error);

                var modelResponseContainer = $('#model-response-container');
                var modelResponse = $('#model-response');

                // Установите класс "error" для обработки ошибки и удалите класс "success"
                modelResponseContainer.removeClass('success').addClass('error');
                modelResponse.text('Произошла ошибка. Пожалуйста, попробуйте еще раз.');
            }
        });
    });
});
