from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import openai
import subprocess
import threading

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

openai.api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-3.5-turbo"  # Выбираем подходящую модель

# Список сообщений для хранения истории беседы
chat_history = []

lama_app_started = False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image1')
def image1():
    return render_template('image1.html')


@app.route('/image2')
def image2():
    return render_template('image2.html')


@app.route('/image3')
def image3():
    return redirect('http://127.0.0.1:7860/image3')

@app.route('/generate-response', methods=['POST'])
def generate_response():
    user_input = request.form['user_input']

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        model_response = response['choices'][0]['message']['content']

        # Добавляем сообщение в историю беседы
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": model_response})

        # Возвращаем историю беседы клиенту
        return jsonify({'response': model_response, 'chat_history': chat_history})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

@app.route('/gradio-app')
def gradio_app():
    return redirect(url_for('gradio_interface'))


if __name__ == '__main__':
    # Запустите Lama.py в отдельном потоке при запуске основного приложения
    if not lama_app_started:
        lama_thread = threading.Thread(target=subprocess.Popen, args=(["python", "Lama.py"],))
        lama_thread.start()
        lama_app_started = True

    # Запустите основное приложение app.py
    app.run(debug=True)