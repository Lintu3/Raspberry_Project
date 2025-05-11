import socket
import speech_recognition as sr

# Server configuration
server_ip = "192.168.1.102"
server_port = 8080

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Define the commands in English and Finnish
commands = {
    "en": {
        "turn on the light": "on", "turn off the light": "off", "turn on": "on",
        "start": "on", "light on": "on", "kitchen": "on", "turn on the kitchen": "on",
        "turn on the kitchen light": "on", "turn off the kitchen light": "off",
        "turn off the kitchen": "off", "kitchen off": "off", "shut down": "off",
        "turn off": "off", "stop": "off", "light off": "off", "stop the light": "off",
        "close": "close"
    },
    "fi": {
        "valo päälle": "on", "keittiö": "on", "päälle": "on", "valo päällä": "on",
        "valo": "on", "valo pois päältä": "off", "sammuta": "off", "valo pois": "off",
        "sammuta valo": "off", "sammu": "off", "sammuta keittiö": "off",
        "sammuta keittiön valo": "off", "sammuta keittiö valo": "off",
        "lopeta": "close"
    }
}
while True:
    try:
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            print("Kitchen light control: Works in Finnish aswell. Speak clearly.")
            
            # Adjust for ambient noise and record audio
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            
            # Record the audio
            # Use the microphone as the audio source
            audio = recognizer.listen(source)
        # initialize command
        command = ""
        # Recognize speech using Google Web Speech API
        # English or finnish commands
        commandE = recognizer.recognize_google(audio, language="en-US").lower()
        commandf = recognizer.recognize_google(audio, language="fi-FI").lower()
        command = commands["en"].get(commandE) or commands["fi"].get(commandf, "")
        # Print the recognized command
        print(f"You said: {commandE}")
        print(f"Sanoit:  {commandf}")
        # Check if the command is valid
        if command in ["on", "off"]:
            try:
                # Create a socket and connect to the server
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                
                # Send the command
                client_socket.send(command.encode('utf-8'))
                client_socket.close()
                print(f"Command '{command}' sent to Raspberry Pi.")
            except ConnectionError:
                print("Failed to connect to the server. Check the server IP and port.")
        else:
            print(f"'{command}' Try again.")
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio. Please try again.")
    except sr.RequestError as e:
        print(f"Could not process the audio input; {e}")
    except KeyboardInterrupt:
        print("Exiting the program.")
        break
    if command == "close":
        print("Exiting the program.")
        break