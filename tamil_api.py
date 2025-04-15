from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__, static_folder='static')
CORS(app)
translator = Translator()

# Text-to-Speech using gTTS
def speak_text(text):
    print("\nAI பதில்:\n" + text + "\n")
    tts = gTTS(text=text, lang='ta')
    audio_path = os.path.join(app.static_folder, "response.mp3")
    tts.save(audio_path)
    return "/static/response.mp3"

# Speech-to-Text using Google
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("உங்கள் கேள்வியை கேட்கலாம்...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="ta-IN")
            print("நீங்கள் கூறியது:", text)
            return text
        except sr.UnknownValueError:
            return "மன்னிக்கவும், உங்கள் வாக்கியத்தை புரிந்துகொள்ள முடியவில்லை."
        except sr.RequestError:
            return "மன்னிக்கவும், உங்கள் வாக்கியத்தை செயலாக்க முடியவில்லை."

# Web Search
def search_web(query):
    try:
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key=AIzaSyC3_DaJ7aUO5ftPIM5XwQEcKCBFJqAaJ18&cx=b14af902f05a140fb"
        response = requests.get(search_url)
        if response.status_code == 200:
            results = response.json().get("items", [])
            if results:
                snippets = [item.get("snippet", "") for item in results[:3]]
                full_snippet = " ".join(snippets)
                tamil_snippet = translator.translate(full_snippet, src="en", dest="ta").text
                return tamil_snippet
            else:
                return "மன்னிக்கவும், தேடலில் எந்த தகவலும் கிடைக்கவில்லை."
        else:
            return f"மன்னிக்கவும், தேடலில் பிழை ஏற்பட்டுள்ளது: {response.status_code}"
    except Exception as e:
        return f"மன்னிக்கவும், தேடலில் பிழை ஏற்பட்டுள்ளது: {str(e)}"

# News Fetch
def fetch_latest_news():
    try:
        news_api_url = "https://newsapi.org/v2/top-headlines?category=sports&apiKey=d02f53d4eddf4517a7d46ecf6b14c9e9"
        response = requests.get(news_api_url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                latest = articles[0].get("title", "சமீபத்திய செய்தி கிடைக்கவில்லை.")
                tamil_news = translator.translate(latest, src="en", dest="ta").text
                return tamil_news
            else:
                return "மன்னிக்கவும், சமீபத்திய செய்தி கிடைக்கவில்லை."
        else:
            return "மன்னிக்கவும், செய்தி பெறுவதில் சிக்கல் ஏற்பட்டுள்ளது."
    except Exception as e:
        return f"மன்னிக்கவும், செய்தி பெறுவதில் பிழை ஏற்பட்டுள்ளது: {str(e)}"

@app.route("/")
def home():
    return jsonify({"message": "Tamil Voice Assistant API is running."})

@app.route("/text-query", methods=["POST"])
def text_query():
    data = request.get_json()
    user_input = data.get("query", "").strip().lower()

    if "விடை" in user_input:
        reply = "வணக்கம்! இனி சந்திப்போம்."
    elif "செய்தி" in user_input:
        reply = fetch_latest_news()
    else:
        reply = search_web(user_input)

    return jsonify({"response": reply})

@app.route("/voice-query", methods=["GET"])
def voice_query():
    transcription = listen()
    if "விடை" in transcription:
        reply = "வணக்கம்! இனி சந்திப்போம்."
    elif "செய்தி" in transcription:
        reply = fetch_latest_news()
    else:
        reply = search_web(transcription)
    return jsonify({"response": reply})

@app.route("/speak", methods=["POST"])
def speak_endpoint():
    data = request.get_json()
    text = data.get("text", "")
    audio_path = speak_text(text)
    return jsonify({"message": "Spoken successfully.", "audio_url": audio_path})

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
