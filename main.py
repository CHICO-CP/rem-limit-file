# Developer by: @DevPhant0m
# Channel: @TEAM_CHICO_CP

import telebot
import os
import json
from datetime import datetime, timedelta

# Check if API.json exists and create it if not
if not os.path.exists('API.json'):
    with open('API.json', 'w') as api_file:
        token = input("Enter the bot token: ")
        group_id = input("Enter the allowed group ID (leave it blank to allow all groups): ")
        private_id = input("Enter the allowed private chat ID (leave it blank to not allow exceptions): ")
        data = {
            'token': token,
            'group_id': group_id if group_id else None,
            'private_id': private_id if private_id else None
        }
        json.dump(data, api_file, indent=4)
else:
    with open('API.json', 'r') as api_file:
        data = json.load(api_file)
        token = data['token']
        group_id = data['group_id']
        private_id = data['private_id']

# Initialize the bot
bot = telebot.TeleBot(token)

# Check if users.json exists, if not create it
if not os.path.exists('users.json'):
    with open('users.json', 'w') as users_file:
        json.dump({}, users_file)

# Load user information
with open('users.json', 'r') as users_file:
    users_data = json.load(users_file)

# Constants to define file limit and block duration
FILE_LIMIT = 3
BLOCK_DURATION = timedelta(hours=12)

# Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot. This bot limits sending files to 3 per user.")

# Command /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "This bot allows you to send a maximum of 3 files. If you exceed the limit, you won't be able to send any more files.")

# Function to check if the chat is allowed
def is_chat_allowed(chat_id):
    if group_id is None:
        return True  # If no group ID is configured, allow all chats
    return str(chat_id) == str(group_id)

# Function to check if the user is an exception (allowed private ID)
def is_user_exception(user_id):
    if private_id is None:
        return False  # If no private ID is configured, no exceptions
    return str(user_id) == str(private_id)

# Check if the user is blocked
def is_user_blocked(user_id):
    if str(user_id) in users_data and 'block_until' in users_data[str(user_id)]:
        return datetime.now() < datetime.fromisoformat(users_data[str(user_id)]['block_until'])
    return False

# Handle sent files
@bot.message_handler(content_types=['document'])
def handle_files(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the chat is allowed
    if not is_chat_allowed(chat_id):
        bot.reply_to(message, "This bot is not allowed in this group.")
        return

    # Check if the user is an exception
    if is_user_exception(user_id):
        bot.reply_to(message, "Your user is exempt from the file limit.")
        return

    # Check if the user is blocked
    if is_user_blocked(user_id):
        bot.reply_to(message, "You are temporarily blocked from sending files.")
        return

    # Get the user's record, initialize if it does not exist
    if str(user_id) not in users_data:
        users_data[str(user_id)] = {'sent_files': 0, 'block_until': None}

    sent_files = users_data[str(user_id)]['sent_files']

    # Check if the user has reached the file limit
    if sent_files >= FILE_LIMIT:
        users_data[str(user_id)]['block_until'] = (datetime.now() + BLOCK_DURATION).isoformat()  # Block for 12 hours
        bot.reply_to(message, "You have reached the limit of 3 files. You are now blocked for 12 hours.")
    else:
        users_data[str(user_id)]['sent_files'] += 1
        remaining_files = FILE_LIMIT - users_data[str(user_id)]['sent_files']
        bot.reply_to(message, f"File received. You have {remaining_files} files left to send.")

    # Save updated user data
    with open('users.json', 'w') as users_file:
        json.dump(users_data, users_file, indent=4)

# Start the bot
print("Bot is running...")
bot.polling()
