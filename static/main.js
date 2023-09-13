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

                // Добавляем ответ модели в историю беседы
                var chatHistory = $('#chat-history');
                var userMessage = $('<p class="user-message"></p>').text(userInput);
                var modelMessage = $('<p class="model-message"></p>').text(data.response);
                chatHistory.append(userMessage, modelMessage);
            },
            error: function(error) {
                console.error('Произошла ошибка:', error);
            }
        });

        // Очищаем поле ввода после отправки запроса
        $('#user-input').val('');
    });
});
