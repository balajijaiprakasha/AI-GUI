import requests
import speech_recognition as sr
import pyttsx3
from googletrans import Translator


def speak(text):
    """Converts text to speech and speaks it."""
    print("\nAI பதில்:\n" + text + "\n")  # Print response as well
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listens to user input via microphone and converts it to text."""
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
            


def search_web(query):
    """Perform a web search and fetch a response in Tamil."""
    try:
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key=AIzaSyC3_DaJ7aUO5ftPIM5XwQEcKCBFJqAaJ18&cx=b14af902f05a140fb"
        response = requests.get(search_url)

        if response.status_code == 200:
            results = response.json().get("items", [])
            if results:
                snippets = [item.get("snippet", "") for item in results[:3]]
                full_snippet = " ".join(snippets)

                translator = Translator()
                tamil_snippet = translator.translate(full_snippet, src="en", dest="ta").text
                return tamil_snippet
            else:
                return "மன்னிக்கவும், தேடலில் எந்த தகவலும் கிடைக்கவில்லை."
        else:
            return f"மன்னிக்கவும், தேடலில் பிழை ஏற்பட்டுள்ளது: {response.status_code}"
    except Exception as e:
        return f"மன்னிக்கவும், தேடலில் பிழை ஏற்பட்டுள்ளது: {str(e)}"


def fetch_latest_news():
    """Fetches the latest news headlines and translates them into Tamil."""
    try:
        news_api_url = "https://newsapi.org/v2/top-headlines?category=sports&apiKey=d02f53d4eddf4517a7d46ecf6b14c9e9"
        response = requests.get(news_api_url)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            if articles:
                latest_news = articles[0].get("title", "சமீபத்திய செய்தி கிடைக்கவில்லை.")
                translator = Translator()
                tamil_news = translator.translate(latest_news, src="en", dest="ta").text
                return tamil_news
            else:
                return "மன்னிக்கவும், சமீபத்திய செய்தி கிடைக்கவில்லை."
        else:
            return "மன்னிக்கவும், செய்தி பெறுவதில் சிக்கல் ஏற்பட்டுள்ளது."
    except Exception as e:
        return f"மன்னிக்கவும், செய்தி பெறுவதில் பிழை ஏற்பட்டுள்ளது: {str(e)}"


def tamil_voice_assistant():
    """Tamil AI chatbot with speech-to-text and text-to-speech."""
    speak("வணக்கம்! தமிழ் AI voice chatbot உங்களுக்காக தயார்.")
    speak("உங்கள் கேள்வியை கேட்டுக்கொள்ளலாம். செய்திகளைப் பெற 'செய்தி' எனக் கூறவும்.")
    speak("வெளியேற 'விடை' எனக் கூறவும்.")

    while True:
        print("கேள்வியை குறியீடு செய்ய (வாய்ச் சரிபார்ப்பு: 'வாய்ஸ்', உள்ளீடு: 'உள்புகு')")
        mode = input("உள்ளீடு தேர்வு செய்யவும் (வாய்ஸ்/உள்புகு): ").strip().lower()

        if mode == "வாய்ஸ்":
            user_input = listen()
        else:
            user_input = input("கேள்வி: ").strip()

        if user_input is None:
            continue

        user_input = user_input.lower()
        if "விடை" in user_input:
            speak("வணக்கம்! இனி சந்திப்போம்.")
            break
        elif "செய்தி" in user_input:
            news_response = fetch_latest_news()
            speak(news_response)
        else:
            response = search_web(user_input)
            speak(response)


if __name__ == "__main__":
    tamil_voice_assistant()
