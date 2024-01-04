from elevenlabs import generate, play, set_api_key, voices
from openai import OpenAI
import base64
import json
import time
import os
import errno
import io
from PIL import Image

# Set OpenAI Key
client = OpenAI(api_key="")

# Set 11Labs Key
set_api_key(api_key="")

# Set Voice ID
voice_id = ""


def encode_image(image):
    # Convert the image to bytes

    while True:
        try:
            return base64.b64encode(image).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
                     {
                         "role": "system",
                         "content": """
                You are Sir David Attenborough. Narrate the picture as if it is a nature documentary. Use maximum 60 words.
                Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                """,
                     },
                 ]
                 + script
                 + generate_new_line(base64_image),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    if response_text == "I'm sorry":
        return None
    else:
        return response_text


def generate_text(image):
    script = []

    # getting the base64 encoding
    base64_image = encode_image(image)

    analysis = analyze_image(base64_image, script=script)
    if analysis == None:
        analysis = analyze_image(base64_image, script=script)

    return analysis


def play_audio(analysis):
    # Elevenlabs
    audio = generate(analysis, voice=voice_id)

    unique_id = base64.urlsafe_b64encode(os.urandom(5)).decode("utf-8").rstrip("=")
    unique_id = f"David_{unique_id}"
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, unique_id)

    with open(file_path, "wb") as f:
        f.write(audio)

    return file_path


def main(image):
    script = []

    # Getting the base64 encoding
    base64_image = encode_image(image)

    # Analyze picture
    print("David is watching...")
    analysis = analyze_image(base64_image, script=script)
    if analysis == None:
        analysis = analyze_image(base64_image, script=script)

    audiofile = play_audio(analysis)

    return analysis, audiofile
