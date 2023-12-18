from flask import Flask, render_template, request, jsonify, send_file
from chatbot import Chatbot
from speech_tools import speech_to_text, text_to_speech

app = Flask(__name__)

chat_history = []
chatbot = Chatbot()

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/button')
def button():
    return render_template('button.html')

@app.route('/send_text_message', methods=['POST'])
def send_text_message():
    user_input = request.form['text_input']
    chatbot_response = send_message(user_input)
    return jsonify({'success': True, 'message': chatbot_response, 'style': 'is-success'})

@app.route('/send_audio_message', methods=['POST'])
def send_audio_message():
    audio = request.files['audio_input']
    audio.save("input.webm")
    user_input = speech_to_text(audio.read())
    chatbot_response = send_message(user_input)
    return jsonify({'success': True, 'message': chatbot_response, 'style': 'is-success'})

@app.route('/get_chat_history')
def get_chat_history():
    return jsonify(chat_history)

@app.route('/clear_chat_history', methods=['POST'])
def clear_chat_history():
    chat_history.clear()
    clear_chatbot_history()
    return jsonify({'success': True, 'message': 'Chat history cleared on the server.'})

@app.route('/create_message_audio', methods=['POST'])
def create_message_audio():
    message = request.form['message_text']
    file_name = text_to_speech(message)
    return send_file(file_name, mimetype="audio/opus", as_attachment=True, download_name=file_name)

def send_message(user_input):
     # Append user input to the chat history with sender information
    chat_history.append({'sender': 'User', 'message': user_input, 'style': 'default'})
    # Get the chatbot's response (modify this part based on your actual chatbot logic)
    chatbot_response = get_chatbot_response(user_input)
    # Append chatbot's response to the chat history with sender information and style
    chat_history.append({'sender': 'ChatGPT', 'message': chatbot_response, 'style': 'is-success'})
    return chatbot_response

def get_chatbot_response(user_input):
    bot_response = chatbot.process_message(user_input)
    return bot_response

def clear_chatbot_history():
    global chatbot
    chatbot = Chatbot()

if __name__ == '__main__':
    app.run(debug=True)
