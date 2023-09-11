from flask import Flask, render_template, jsonify, request
import os
import openai

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Установите ваш API-ключ от OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-3.5-turbo"  # Выбираем подходящую модель

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
    return render_template('image3.html')

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
        return jsonify({'response': model_response})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
