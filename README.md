# NarratorBot
 A Telegram bot repository designed for narrating descriptions of pictures sent to the bot, providing an interactive and accessible visual aid experience.

## Description 

This telegram bot is a creative adaptation of an idea originally proposed by [Charlie Holtz on Twitter](https://twitter.com/charliebholtz/status/1724815159590293764). 
The bots unique feature is its ability to narrate pictures sent by users in a voice reminiscent of David Attenborough, 
a renowned naturalist and broadcaster. When a user sends a picture to the bot, it processes the image and then generates 
a voice memo, imitating Attenborough's style of narration. This voice memo is then sent back to the user, providing an 
engaging and personalized experience. he bot blends technology with the charm of nature documentary-style storytelling, 
offering users a novel way to interact with their photos.

## Setup
Clone this repo, and setup and activate a virtualenv:

```
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```
Then, install the dependencies: `pip install -r requirements.txt`

Make a Replicate, OpenAI, and ElevenLabs account and set your tokens:

```
export OPENAI_API_KEY=<token>
export ELEVENLABS_API_KEY=<eleven-token>
```
Make a new voice in Eleven and get the voice id of that voice using their get voices API, or by clicking the flask icon next to the voice in the VoiceLab tab.

```
export ELEVENLABS_VOICE_ID=<voice-id>
```

## Configuring Your Telegram Bot

### Create a Bot on Telegram:
1. Use Telegram's BotFather to create a new bot. Send `/newbot` to BotFather and follow the instructions.
2. Once the bot is created, you will receive a bot token.

### Configuring the Bot Token:
1. Replace `your_telegram_bot_token_here` in the `.env` file with the token provided by BotFather.

### Run Your Project
In your terminal, run the bot:
`python3 bot.py`

## Deploying Your Bot:
- This bot is hosted on [Heroku](https://dashboard.heroku.com), a cloud platform that allows easy deployment and scaling. The included `Procfile` is used by Heroku to run the bot.

## Usage
After running or deploying the bot, send a picture. The bot will reply with an audio message describing your picture.


## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
A special thanks to the open-source community.

---

For further information or support, feel free to open an issue in this repository.

