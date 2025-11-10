# FILE: main.py
# DESCRIPTION: Main bot execution file

import telebot
import logging
from datetime import datetime
from bot_config import BotConfig, ConfigManager
from user_manager import UserManager
from bot_commands import BotCommands

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(BotConfig.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def main():
    """Main bot execution function"""
    
    # Initialize configuration
    ConfigManager.initialize_config()
    setup_logging()
    
    # Load configuration
    config_data = ConfigManager.load_config()
    token = config_data['token']
    
    if not token:
        print("❌ No bot token found. Please check your configuration.")
        return
    
    # Initialize bot
    bot = telebot.TeleBot(token)
    
    # Initialize managers
    config_manager = ConfigManager()
    user_manager = UserManager()
    
    # Initialize commands
    bot_commands = BotCommands(bot, config_manager, user_manager)
    bot_commands.register_handlers()
    
    # Update bot start time in statistics
    stats_data = config_manager.load_stats_data()
    stats_data['bot_start_time'] = datetime.now().isoformat()
    config_manager.save_stats_data(stats_data)
    
    print(f"🤖 {BotConfig.BOT_NAME} v{BotConfig.BOT_VERSION} is running...")
    print(f"📊 Configuration loaded from: {BotConfig.CONFIG_FILE}")
    print(f"👥 Users database: {BotConfig.USERS_FILE}")
    print(f"📈 Statistics: {BotConfig.STATS_FILE}")
    print("📍 Press Ctrl+C to stop the bot")
    
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Bot error: {e}")

if __name__ == "__main__":
    main()