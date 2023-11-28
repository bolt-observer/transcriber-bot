import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import settings
import asyncio
import os
from pydub import AudioSegment
from pywhispercpp.model import Model

import nest_asyncio
nest_asyncio.apply()


# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe(input_file):
    model = Model(settings.MODEL_PATH,print_realtime=False)
    segments = model.transcribe(input_file)
    joined_text = " ".join(segment.text for segment in segments)
    return joined_text

async def help(update: Update, context: CallbackContext) -> None:
    help_text = """
    Hello. I'm TranscriberBot - your friendly AI helper. 
I will help you with transcriptions of audio files.
    
Currently I only support english language but I'm working on my multilingual skills.
    
If you have any questions about me you can contact my creator @aaaljaz
    """
    await update.message.reply_text(help_text)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me an audio file or forward a voice message and I will transcribe it for you. Currently only supports english language.')


async def download_file(update: Update, context: CallbackContext) -> None:
    audio_message = update.message.effective_attachment
    new_file = await context.bot.get_file(audio_message.file_id)
    if hasattr(audio_message,"file_name"):
        file_name = audio_message.file_name
    else:
        file_name = f"voice_{audio_message.file_id}.ogg"
    await new_file.download_to_drive(file_name)
    try:
        msg = transcribe(file_name)
    except Exception as e:
        msg = "Transcription failed. Please try again."
    await update.message.reply_text(f'Transcription for {file_name}:\n {msg}')
    # delete file
    os.remove(file_name)


async def main() -> None:

    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(None, download_file))


    # Run the bot until it is stopped
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())