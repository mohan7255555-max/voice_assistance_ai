import google.generativeai as genai
import speech_recognition as sr
import pyttsx3



genai.configure(api_key="YOUR_API_KEY_HERE") 
model = genai.GenerativeModel("gemini-1.5-flash")


engine = pyttsx3.init()

def speak(text):
    """Speak text using a background thread"""
    def run():
        engine.say(text)
        engine.runAndWait()
   


def listen():
    """Listen from microphone and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print(" Recognizing...")
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is not available right now.")
        return ""


def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Sorry, I couldn’t get a response."


speak("Hello! I am your Gemini-powered voice assistant. You can ask me anything.")

while True:
    query = listen()

    if not query:
        continue

    if "stop" in query or "exit" in query or "bye" in query:
        speak("Goodbye, have a nice day!")
        break

    
    answer = ask_gemini(query)
    print("Answer:", answer)
    speak(answer)
         