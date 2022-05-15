import speech_recognition as sr
import webbrowser as web
from playsound import playsound

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        playsound('./1.mpeg')
        audio = r.listen(source)
        playsound('./2.mpeg')
        try:
            dest = r.recognize_google(audio)
            print("You have said : " + dest)
        except Exception as e:
            print("Error : " + str(e))

if __name__ == "__main__":
    main()