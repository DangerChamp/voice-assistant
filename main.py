import speech_recognition as sr
from gtts import gTTS
import winsound
from pydub import AudioSegment
import pyautogui
import webbrowser

recognizer = sr.Recognizer()


def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None


def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang="en")
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)


listeningToTask = False
deleteTask = False


def main():
    global tasks
    global listeningToTask
    global deleteTask
    while True:
        command = listen_for_command()

        triggerKeyword = "hey"

        if command and triggerKeyword in command or listeningToTask:
            if listeningToTask:
                tasks = open("tasks.txt", "a")
                tasks.write(command + "\n")
                listeningToTask = False
                tasks.close()
                tasks = open("tasks.txt", "r")
                respond(
                    "Adding "
                    + command
                    + " to your task list. You have "
                    + str(len(tasks.readlines()))
                    + " currently in your list."
                )
                except TypeError:
                    respond("Could you please repeat that?")
                tasks.close()
            elif deleteTask:
                tasks = open("tasks.txt", "r")
                taskList = tasks.readlines()
                tasks.close()
                tasks = open("tasks.txt", "w")
                for task in taskList:
                    if command in task:
                        respond("Deleting " + task)
                    else:
                        tasks.write(task)
                tasks.close()
                deleteTask = False
                    else:
                        respond("Task '" + command + "' not found in the task list.")
                        deleteTask = False
                except TypeError:
                    respond("Could you please repeat that?")
            elif "add" and "task" in command:
                listeningToTask = True
                respond("Sure, what is the task?")
            elif "list tasks" in command:
                tasks = open("tasks.txt", "r")
                respond("Sure. Your tasks are:")
                for task in tasks:
                    respond(task)
                tasks.close()
            elif "delete" and "task" in command:
                deleteTask = True
                respond("What task would you like to delete?")
            elif "take" and "screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                respond("I took a screenshot for you.")
            elif "open chrome" in command:
                respond("Opening Chrome.")
                webbrowser.open("https://www.google.com")
            elif "exit" in command:
                respond("Goodbye!")
                tasks.close()
                break
            else:
                respond("Sorry, I'm not sure how to handle that command.")


if __name__ == "__main__":
    main()
