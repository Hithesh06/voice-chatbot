import speech_recognition as sr
import pyttsx3
import openai

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speed

# Set up OpenAI API Key (replace with your key)
openai.api_key = "your-openai-api-key"

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=0) as source:  # Change index if needed
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
    except sr.RequestError:
        print("Speech Recognition API unavailable.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except OSError:
        print("Microphone not found. Check your audio settings.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None


def chat_with_openai(prompt):
    """Sends user input to OpenAI and gets a response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Sorry, I encountered an error."

# Main Chat Loop
if __name__ == "__main__":
    speak("Hello! How can I assist you?")
    
    while True:
        user_input = listen()
        if user_input:
            if "exit" in user_input or "quit" in user_input:
                speak("Goodbye!")
                break
            response = chat_with_openai(user_input)
            print("Bot:", response)
            speak(response)
