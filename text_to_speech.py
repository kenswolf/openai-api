from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input="You might be cool but your not moe dee",
)

response.stream_to_file(speech_file_path)

###################
###################
###################

import pygame
import time

def play_mp3(mp3_file):
    pygame.init()

    try:
        # Initialize the mixer module
        pygame.mixer.init()

        # Load the MP3 file
        pygame.mixer.music.load(mp3_file)

        # Play the MP3 file
        pygame.mixer.music.play()

        # Wait for the music to finish playing (blocking)
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    except pygame.error as e:
        print(f"Error: {e}")
    finally:
        # Quit the mixer module
        pygame.mixer.quit()

###################
###################
###################

play_mp3(speech_file_path)

