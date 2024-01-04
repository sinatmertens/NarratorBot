from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging
import requests
import json
import narrator
import io
import os

logger = logging.getLogger(__name__)


def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """
    sender_name = update.message['chat']['first_name']

    # Print to console
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if not update.message.photo:
        # If the sender sends a text message, inform to send a picture
        context.bot.send_message(update.message.chat_id,
                                 f"Hello {sender_name}! Send me any picture, and I'll swiftly return an audio file describing the details, bringing your images to life through sound.")

    if update.message.photo:

        # Downloading the image from the telegram server
        try:
            photo_id = update.message.photo[1]['file_id']
        except IndexError:
            photo_id = update.message.photo[0]['file_id']

        photo_path = requests.get(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/getFile?file_id={photo_id}")
        photo_path = photo_path.content.decode('utf-8')
        photo_url = json.loads(photo_path)['result']['file_path']
        photo_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/{photo_url}"
        photo = requests.get(photo_url)
        photo = photo.content

        if photo:
            print(f"Downloaded the picture from {sender_name}")

            context.bot.send_message(update.message.chat_id,
                                     f"Marvelous {sender_name}! Allow me a moment to study your image and craft your audio file...")

            analysis, audiofile = narrator.main(photo)

            if analysis:
                context.bot.send_message(update.message.chat_id,
                                         f"{analysis}")

            if audiofile:

                context.bot.send_audio(update.message.chat_id, audio=open(audiofile, 'rb'))
                os.remove(audiofile)

            else:
                context.bot.send_message(update.message.chat_id,
                                         f"Well there has been some kind of mistake it seems.")

            context.bot.send_message(update.message.chat_id,
                                     f"There you go. Come back if you want me to observe something else. Farewell!")


def main() -> None:
    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
