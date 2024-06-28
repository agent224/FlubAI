r"""
         _____                    _____            _____                    _____
         /\    \                  /\    \          /\    \                  /\    \
        /::\    \                /::\____\        /::\____\                /::\    \
       /::::\    \              /:::/    /       /:::/    /               /::::\    \
      /::::::\    \            /:::/    /       /:::/    /               /::::::\    \
     /:::/\:::\    \          /:::/    /       /:::/    /               /:::/\:::\    \
    /:::/__\:::\    \        /:::/    /       /:::/    /               /:::/__\:::\    \
   /::::\   \:::\    \      /:::/    /       /:::/    /               /::::\   \:::\    \
  /::::::\   \:::\    \    /:::/    /       /:::/    /      _____    /::::::\   \:::\    \
 /:::/\:::\   \:::\    \  /:::/    /       /:::/____/      /\    \  /:::/\:::\   \:::\ ___\
/:::/  \:::\   \:::\____\/:::/____/       |:::|    /      /::\____\/:::/__\:::\   \:::|    |
\::/    \:::\   \::/    /\:::\    \       |:::|____\     /:::/    /\:::\   \:::\  /:::|____|
 \/____/ \:::\   \/____/  \:::\    \       \:::\    \   /:::/    /  \:::\   \:::\/:::/    /
          \:::\    \       \:::\    \       \:::\    \ /:::/    /    \:::\   \::::::/    /
           \:::\____\       \:::\    \       \:::\    /:::/    /      \:::\   \::::/    /
            \::/    /        \:::\    \       \:::\__/:::/    /        \:::\  /:::/    /
             \/____/          \:::\    \       \::::::::/    /          \:::\/:::/    /
                               \:::\    \       \::::::/    /            \::::::/    /
                                \:::\____\       \::::/    /              \::::/    /
                                 \::/    /        \::/____/                \::/____/
                                  \/____/          ~~                       ~~
                                     By: Levi Schaffner
                                    The Hell of a AI Bot
"""
import base64
from dotenv import load_dotenv
import streamlit as st
import numpy as np
import sounddevice as sd
import pyaudio # Records audio from microphone
import wave # Supports the .wav format
from openai import OpenAI # ChatGPT
import os # Operating System
from gtts import gTTS # Text-To-Speach
import pygame # Plays audio
import time
import speech_recognition as sr
#WEBSITE
#--------------------------------------------------------------------------
path = "response.mp3" # Text-To-Speach mp3 file name
st.title(":blue[FlubAI]", anchor=None, help=None,)

def configure():
    load_dotenv()

language = 'en'
load_dotenv()

print("""
    ________  _____  _____  _____  ______    
|_   __  ||_   _||_   _||_   _||_   _ \   
  | |_ \_|  | |    | |    | |    | |_) |  
  |  _|     | |   _| '    ' |    |  __'.  
 _| |_     _| |__/ |\ \__/ /    _| |__) | 
|_____|   |________| `.__.'    |_______/  

    """)
st.subheader("The Hell of a AI Bot")

print("The Hell of a AI Bot")
st.info("FlubAI is in development expect bugs",  icon=None)
st.divider()
print("================================================================")
st.markdown("Conversation Start")
print("*Conversation Start*")

assistant_response = ("I can help you with anything and everything!")

myobj = gTTS(text=assistant_response, lang=language, slow=False)

myobj.save("response.mp3")
audio_file = open('response.mp3', 'rb')
audio_bytes = audio_file.read()
audio_base64 = base64.b64encode(audio_bytes).decode()
audio_html = f"""
<audio autoplay>
  <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
  Your browser does not support the audio element.
</audio>
"""
st.markdown(audio_html, unsafe_allow_html=True)
st.markdown("Bot: " + assistant_response)
print("Bot: " + assistant_response)

end_program = False
while not end_program:
    configure()
    # Function to continuously monitor microphone input
    client = OpenAI( #Open AI key
        api_key=st.secrets["API_KEY"]
    )
    def monitor_microphone():
        # Initialize a variable to store the state (True if there's input, False otherwise)
        is_input = False

        # Define callback function to capture microphone input
        def callback(indata, frames, time, status):
            nonlocal is_input
            # Check if any input is detected (RMS amplitude threshold can be adjusted)
            if np.max(np.abs(indata)) > 0.05:
                is_input = True
                time.sleep(0.2)
                if np.max(np.abs(indata)) > 0.05:
                    chunk = 1024  # Record in chunks of 1024 samples
                    sample_format = pyaudio.paInt16  # 16 bits per sample
                    channels = 2
                    fs = 44100  # Record at 44100 samples per second
                    seconds = 2
                    filename = "output.wav"

                    p = pyaudio.PyAudio()  # Create an interface to PortAudio



                    stream = p.open(format=sample_format,
                                    channels=channels,
                                    rate=fs,
                                    frames_per_buffer=chunk,
                                    input=True)

                    frames = []  # Initialize array to store frames

                    # Store data in chunks for 3 seconds
                    if np.max(np.abs(indata)) < 0.05:
                        time.sleep(2)
                        if np.max(np.abs(indata)) < 0.05:
                            data = stream.read(chunk)
                            frames.append(data)

                    # Stop and close the stream
                    stream.stop_stream()
                    stream.close()
                    # Terminate the PortAudio interface
                    p.terminate()



                    # Save the recorded data as a WAV file
                    wf = wave.open(filename, 'wb')
                    wf.setnchannels(channels)
                    wf.setsampwidth(p.get_sample_size(sample_format))
                    wf.setframerate(fs)
                    wf.writeframes(b''.join(frames))
                    wf.close()

            else:
                is_input = False
    # Call the function to monitor microphone input
    monitor_microphone()

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 2
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio



    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    audio_file = open("output.wav", "rb")
    transcript = client.audio.translations.create(
        model='whisper-1',
        file=audio_file
    )
    st.markdown("You: "  + transcript.text)
    print("You: "  + transcript.text)

    get_input = transcript.text

    if get_input.lower() == "goodbye" or get_input.lower() == "exit":
        end_program = True
        print("Have a great day!")
    else:
        system_data = [
            {"role": "system", "content": "You are a bot that allways gives the wrong answer."
                                          "You are cocky and make fun of the user by roasting them."
                                          "If the user asks if the information you provide is truthfull "
                                          "You must explain your purpose and that"
                                          "the information you provide is not truthfull."
                                          "You are very casual"
                                          "You act like you know everything"
                                          "Your name is Flub"
                                          "You act like you know everything and dont tell people that you dumb"
                                          "You have one braincell"},
            {"role": "user", "content": get_input}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=system_data
        )
        assistant_response = response.choices[0].message.content
        system_data.append({"role": "assistant", "content": assistant_response})
        myobj = gTTS(text=assistant_response, lang=language, slow=False)
        pygame.mixer.init()
        myobj.save("response.mp3")

        pygame.mixer.music.load(path)

        # Play the loaded mp3 file
        st.markdown("Bot: " + assistant_response)
        print("Bot: " + assistant_response)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        pygame.mixer.music.unload()
        os.remove(path)
