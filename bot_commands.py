# FILE: bot_commands.py
# DESCRIPTION: Bot command handlers

import telebot
from datetime import datetime
from bot_config import BotConfig, ConfigManager
from user_manager import UserManager

class BotCommands:
    """Handle all bot commands"""
    
    def __init__(self, bot, config_manager, user_manager):
        self.bot = bot
        self.config_manager = config_manager
        self.user_manager = user_manager
        
        # Load initial data
        self.config_data = config_manager.load_config()
        self.users_data = config_manager.load_users_data()
        self.stats_data = config_manager.load_stats_data()
        
        # Set admin ID
        BotConfig.ADMIN_ID = self.config_data.get('admin_id')
    
    def register_handlers(self):
        """Register all message handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.command_start(message)
        
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.command_help(message)
        
        @self.bot.message_handler(commands=['stats'])
        def handle_stats(message):
            self.command_stats(message)
        
        @self.bot.message_handler(commands=['myinfo'])
        def handle_myinfo(message):
            self.command_myinfo(message)
        
        @self.bot.message_handler(commands=['reset'])
        def handle_reset(message):
            self.command_reset(message)
        
        @self.bot.message_handler(commands=['admin'])
        def handle_admin(message):
            self.command_admin(message)
        
        @self.bot.message_handler(commands=['broadcast'])
        def handle_broadcast(message):
            self.command_broadcast(message)
        
        @self.bot.message_handler(content_types=['document'])
        def handle_documents(message):
            self.handle_file_upload(message)
    
    def command_start(self, message):
        """Handle /start command"""
        welcome_text = f"""
🛡️ *Welcome to {BotConfig.BOT_NAME} v{BotConfig.BOT_VERSION}* 🛡️

*Secure File Management Bot*

📊 *Key Features:*
• File upload limits per user
• Smart blocking system
• User activity tracking
• Admin management tools

🔧 *Available Commands:*
`/start` - Show this welcome message
`/help` - Detailed help and instructions
`/stats` - Your personal statistics
`/myinfo` - Your current status and limits
`/reset` - Reset your file count (Admin only)

⚙️ *File Limits:*
• Maximum {BotConfig.FILE_LIMIT} files per user
• {BotConfig.BLOCK_DURATION.seconds // 3600} hour block on limit exceed
• Real-time tracking

👨💻 *Developer:* Ghost Developer
        """
        self.bot.reply_to(message, welcome_text, parse_mode='Markdown')
    
    def command_help(self, message):
        """Handle /help command"""
        help_text = f"""
📖 *{BotConfig.BOT_NAME} - Help Guide* 📖

*File Management System:*
• You can upload up to {BotConfig.FILE_LIMIT} files
• Limits reset automatically after block period
• All file types are supported
• Maximum file size: {BotConfig.MAX_FILE_SIZE // (1024*1024)}MB

*User Commands:*
`/start` - Welcome message and bot info
`/help` - This help message
`/stats` - View your upload statistics
`/myinfo` - Check your current status

*Admin Commands:* (Restricted)
`/reset @username` - Reset user's file count
`/admin` - Admin panel
`/broadcast` - Send message to all users

*How It Works:*
1. Upload files normally
2. Bot tracks your file count
3. Get notified about remaining files
4. Temporary block if limit exceeded
5. Automatic unblock after {BotConfig.BLOCK_DURATION.seconds // 3600} hours

*Need Assistance?*
Contact the administrator for help.
        """
        self.bot.reply_to(message, help_text, parse_mode='Markdown')
    
    def command_stats(self, message):
        """Handle /stats command"""
        user_id = message.from_user.id
        user_data = UserManager.get_user_data(user_id, self.users_data)
        stats = UserManager.get_user_stats(user_data)
        
        stats_text = f"""
📊 *Your Statistics*

📁 *File Usage:*
• Files sent this period: `{stats['sent_files']}/{BotConfig.FILE_LIMIT}`
• Remaining files: `{stats['remaining_files']}`
• Total files sent: `{stats['total_files_sent']}`

🔒 *Status:*
• Blocked: `{'Yes' if stats['is_blocked'] else 'No'}`
{ f"• Time remaining: `{stats['block_remaining']}`" if stats['is_blocked'] else ""}

📅 *Account Info:*
• First seen: `{stats['first_seen'][:10]}`
• Last activity: `{user_data['last_activity'][:19]}`
        """
        self.bot.reply_to(message, stats_text, parse_mode='Markdown')
    
    def command_myinfo(self, message):
        """Handle /myinfo command"""
        user_id = message.from_user.id
        user_data = UserManager.get_user_data(user_id, self.users_data)
        stats = UserManager.get_user_stats(user_data)
        
        status_icon = "🔴" if stats['is_blocked'] else "🟢"
        status_text = "BLOCKED" if stats['is_blocked'] else "ACTIVE"
        
        info_text = f"""
👤 *Your Information*

{status_icon} *Status:* {status_text}
📁 *Files this period:* {stats['sent_files']}/{BotConfig.FILE_LIMIT}
🎯 *Remaining:* {stats['remaining_files']} files

{ f"⏰ *Block expires in:* {stats['block_remaining']}" if stats['is_blocked'] else "✅ *You can upload files*"}
        """
        self.bot.reply_to(message, info_text, parse_mode='Markdown')
    
    def command_reset(self, message):
        """Handle /reset command (Admin only)"""
        user_id = message.from_user.id
        
        # Check if user is admin
        if str(user_id) != str(BotConfig.ADMIN_ID):
            self.bot.reply_to(message, "❌ This command is for administrators only.")
            return
        
        # Reset all users
        for user_id_str, user_data in self.users_data.items():
            UserManager.reset_user_files(user_data)
        
        self.config_manager.save_users_data(self.users_data)
        self.bot.reply_to(message, "✅ All user file counts have been reset.")
    
    def command_admin(self, message):
        """Handle /admin command (Admin only)"""
        user_id = message.from_user.id
        
        if str(user_id) != str(BotConfig.ADMIN_ID):
            self.bot.reply_to(message, "❌ Access denied.")
            return
        
        total_users = len(self.users_data)
        active_users = sum(1 for user_data in self.users_data.values() 
                          if not UserManager.is_user_blocked(user_data))
        blocked_users = total_users - active_users
        
        admin_text = f"""
👑 *Admin Panel*

📈 *Statistics:*
• Total users: `{total_users}`
• Active users: `{active_users}`
• Blocked users: `{blocked_users}`
• Bot uptime: `Calculating...`

⚙️ *Quick Actions:*
• Use `/reset` to reset all users
• Use `/broadcast` to message all users
• Check logs in `{BotConfig.LOG_FILE}`

🔧 *Configuration:*
• File limit: `{BotConfig.FILE_LIMIT}`
• Block duration: `{BotConfig.BLOCK_DURATION.seconds // 3600} hours`
• Max file size: `{BotConfig.MAX_FILE_SIZE // (1024*1024)}MB`
        """
        self.bot.reply_to(message, admin_text, parse_mode='Markdown')
    
    def command_broadcast(self, message):
        """Handle /broadcast command (Admin only)"""
        user_id = message.from_user.id
        
        if str(user_id) != str(BotConfig.ADMIN_ID):
            self.bot.reply_to(message, "❌ Access denied.")
            return
        
        broadcast_text = message.text.replace('/broadcast', '').strip()
        if not broadcast_text:
            self.bot.reply_to(message, "❌ Please provide a message to broadcast.")
            return
        
        # This would need to be implemented with proper user tracking
        self.bot.reply_to(message, "📢 Broadcast feature - Implementation needed")
    
    def handle_file_upload(self, message):
        """Handle file uploads"""
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if chat is allowed
        if not self.is_chat_allowed(chat_id):
            self.bot.reply_to(message, "❌ This bot is not allowed in this chat.")
            return
        
        # Check if user is admin (unlimited access)
        if str(user_id) == str(BotConfig.ADMIN_ID):
            self.bot.reply_to(message, "✅ File received (Admin - No limits)")
            return
        
        # Get user data
        user_data = UserManager.get_user_data(user_id, self.users_data)
        
        # Check if user is blocked
        if UserManager.is_user_blocked(user_data):
            block_until = datetime.fromisoformat(user_data['block_until'])
            time_remaining = block_until - datetime.now()
            self.bot.reply_to(message, 
                             f"❌ You are blocked from sending files.\n"
                             f"Time remaining: {str(time_remaining).split('.')[0]}")
            return
        
        # Check file limit
        if user_data['sent_files'] >= BotConfig.FILE_LIMIT:
            UserManager.block_user(user_data, BotConfig.BLOCK_DURATION)
            self.config_manager.save_users_data(self.users_data)
            self.bot.reply_to(message, 
                             f"❌ You've reached the limit of {BotConfig.FILE_LIMIT} files.\n"
                             f"You are now blocked for {BotConfig.BLOCK_DURATION.seconds // 3600} hours.")
            return
        
        # Process file upload
        UserManager.increment_file_count(user_data)
        self.config_manager.save_users_data(self.users_data)
        
        remaining_files = BotConfig.FILE_LIMIT - user_data['sent_files']
        self.bot.reply_to(message, 
                         f"✅ File received successfully!\n"
                         f"📁 Remaining files: {remaining_files}/{BotConfig.FILE_LIMIT}")
    
    def is_chat_allowed(self, chat_id):
        """Check if the chat is allowed"""
        allowed_group_id = self.config_data.get('allowed_group_id')
        if allowed_group_id is None:
            return True  # Allow all chats if no group ID configured
        return str(chat_id) == str(allowed_group_id)