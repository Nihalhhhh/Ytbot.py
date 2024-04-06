import os
import logging
from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from pytube import YouTube

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Hi there! I am a YouTube video downloader bot. Simply send me a YouTube video link, and I will provide you with options to download the video in different resolutions.')

# Define a function to handle incoming messages
def message_handler(update, context):
    # Get the text message from the update
    message_text = update.message.text
    
    # Check if the message contains a YouTube video link
    if 'youtube.com/watch?v=' in message_text:
        try:
            # Extract the YouTube video URL from the message
            url = message_text.split(' ')[0]
            
            # Create a YouTube object
            yt = YouTube(url)
            
            # Get available video streams
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            
            # Create a list of available resolutions
            resolutions = [f"{stream.resolution} - {stream.mime_type.split('/')[1]}" for stream in streams]
            
            # Send a message to the user to select a resolution
            update.message.reply_text('Select a resolution for downloading:', reply_markup=ReplyKeyboardMarkup([resolutions], one_time_keyboard=True))
            
            # Save the available streams and YouTube object in the user's context
            context.user_data['streams'] = streams
            context.user_data['yt'] = yt
        except Exception as e:
            update.message.reply_text(f'Error: {str(e)}')

def main():
    # Set up the Telegram Bot
    updater = Updater("6941885870:AAGt7uBdRfaB20V5GXPcyWAmbv5K33Vcihc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add a command handler to handle the /start command
    dp.add_handler(CommandHandler("start", start))

    # Add a message handler to handle incoming messages
    dp.add_handler(MessageHandler(None, message_handler))

    # Start the Bot
    updater.start_polling()
    updater.idle()
