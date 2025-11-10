import telebot
from telebot.types import Message
import time
from threading import Thread

# Bot token
BOT_TOKEN = "TU_TOKEN_AQUÍ"
bot = telebot.TeleBot(BOT_TOKEN)

# Configuration
MAX_ARCHIVOS = 5  
BLOQUEO_MINUTOS = 15  
# Data storage
usuarios = {}  
bloqueados = {}  

def desbloquear_usuario(chat_id, user_id):
    time.sleep(BLOQUEO_MINUTOS * 60)
    if user_id in bloqueados:
        bloqueados.pop(user_id, None)
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True)


# Handling file-type messages
@bot.message_handler(content_types=["document"])
def manejar_archivos(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    miembro = bot.get_chat_member(chat_id, user_id)
    if miembro.status in ["administrator", "creator"]:
        return

    if user_id in bloqueados:
        bot.reply_to(message, f"🚫 @{username}, you are temporarily blocked from sending files for {BLOQUEO_MINUTOS} minutes.\n🚫 @{username}, estás temporalmente bloqueado para enviar archivos durante {BLOQUEO_MINUTOS} minutos.")
        return

    if user_id not in usuarios:
        usuarios[user_id] = 0
    usuarios[user_id] += 1

    archivos_restantes = MAX_ARCHIVOS - usuarios[user_id]

    if archivos_restantes > 0:
        bot.reply_to(
            message,
            f"📦 @{username}, you have {archivos_restantes}/{MAX_ARCHIVOS} files remaining to send.\n"
            f"📦 @{username}, te quedan {archivos_restantes}/{MAX_ARCHIVOS} archivos por enviar."
        )
    else:
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False)
        bloqueados[user_id] = True
        bot.reply_to(
            message,
            f"🚫 @{username}, you have reached the limit of {MAX_ARCHIVOS} files. You are blocked for {BLOQUEO_MINUTOS} minutes.\n"
            f"🚫 @{username}, has alcanzado el límite de {MAX_ARCHIVOS} archivos. Estás bloqueado durante {BLOQUEO_MINUTOS} minutos."
        )

        Thread(target=desbloquear_usuario, args=(chat_id, user_id)).start()


# /start command to explain how the bot works
@bot.message_handler(commands=["start"])
def start(message: Message):
    username = message.from_user.username or message.from_user.first_name
    bot.reply_to(
        message,
        (
            f"👋 Hello, @{username}! Welcome to the group management bot.\n\n"
            "📋 *How it works:*\n"
            f"1️⃣ Each user can send up to {MAX_ARCHIVOS} files.\n"
            f"2️⃣ If you exceed the limit, you will be temporarily blocked for {BLOQUEO_MINUTOS} minutes.\n"
            "3️⃣ Admins and the group owner are exempt from this rule.\n\n"
            "🌟 *Bot Developer:* SP-FUCKER\n"
            "💬 *Contact:* @Gh0stDeveloper\n\n"
            "Thank you for following the rules!"
        ),
        parse_mode="Markdown"
    )


# Custom command /reset to reset a user's file counter
@bot.message_handler(commands=["reset"])
def reset(message: Message):
    chat_id = message.chat.id
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username or message.reply_to_message.from_user.first_name

        miembro = bot.get_chat_member(chat_id, message.from_user.id)
        if miembro.status in ["administrator", "creator"]:
            usuarios[user_id] = 0
            bot.reply_to(
                message,
                f"🔄 File counter reset for @{username}.\n"
                f"🔄 Contador de archivos reiniciado para @{username}."
            )
        else:
            bot.reply_to(message, "🚫 You don't have permission to use this command.\n🚫 No tienes permisos para usar este comando.")
    else:
        bot.reply_to(message, "❌ Use this command by replying to a message.\n❌ Usa este comando respondiendo a un mensaje.")


# Handling new members in the group
@bot.message_handler(content_types=["new_chat_members"])
def bienvenida(message: Message):
    for nuevo in message.new_chat_members:
        username = nuevo.username or nuevo.first_name
        bot.send_message(
            message.chat.id,
            (
                f"🎉 Welcome @{username} to the group! 🎉\n"
                "📋 Please follow the group rules:\n"
                f"1️⃣ Each user can send up to {MAX_ARCHIVOS} files.\n"
                f"2️⃣ If you exceed the limit, you will be blocked for {BLOQUEO_MINUTOS} minutes.\n"
                "3️⃣ Respect other members and avoid spamming.\n\n"
                f"🎉 ¡Bienvenido/a @{username} al grupo! 🎉\n"
                "📋 Por favor, sigue las reglas del grupo:\n"
                f"1️⃣ Cada usuario puede enviar hasta {MAX_ARCHIVOS} archivos.\n"
                f"2️⃣ Si superas el límite, serás bloqueado durante {BLOQUEO_MINUTOS} minutos.\n"
                "3️⃣ Respeta a los demás miembros y evita enviar spam."
            )
        )


print("🤖 The bot is running...")
bot.infinity_polling()